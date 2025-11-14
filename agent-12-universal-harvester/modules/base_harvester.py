"""
Base Harvester Template - Abstract Base Class for All Harvesters

This is the foundation class that ALL harvesters inherit from.
Provides common functionality for data harvesting, quality scoring,
Gemini analysis, and database operations.

Author: Universal Harvester System
Version: 1.0.0
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import logging
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseHarvester(ABC):
    """
    Abstract Base Class for all Harvesters.

    All specific harvesters (Trend, Audio, Screenplay, etc.) inherit from this class
    and implement the abstract methods while using the shared functionality.
    """

    def __init__(self, harvester_name: str, config: Dict[str, Any]):
        """
        Initialize the Base Harvester

        Args:
            harvester_name: Name of the harvester (e.g., "trend_harvester")
            config: Configuration dictionary for this harvester
        """
        self.harvester_name = harvester_name
        self.config = config
        self.logger = logging.getLogger(f"Harvester.{harvester_name}")
        self.quality_threshold = config.get('quality_threshold', 7.0)
        self.enabled_sources = config.get('sources', [])

        # Import dependencies (lazy loading)
        self._gemini_analyzer = None
        self._database = None

        self.logger.info(f"Initialized {harvester_name} with threshold {self.quality_threshold}")

    # ============================================================
    # ABSTRACT METHODS - Must be implemented by each subclass
    # ============================================================

    @abstractmethod
    def get_data_sources(self) -> List[Dict[str, str]]:
        """
        Get list of data sources to harvest from.

        Returns:
            List of dicts with keys: 'name', 'url', 'type'
            Example: [
                {'name': 'YouTube Trending', 'url': 'https://...', 'type': 'api'},
                {'name': 'Reddit Music', 'url': 'https://...', 'type': 'scrape'}
            ]
        """
        pass

    @abstractmethod
    def extract_raw_data(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Extract raw data from a specific source.

        Args:
            source: Source dict from get_data_sources()

        Returns:
            List of raw data items (unstructured)
        """
        pass

    @abstractmethod
    def parse_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parse and structure the raw data into a standardized format.

        Args:
            raw_data: Raw data items from extract_raw_data()

        Returns:
            List of structured, parsed data items
        """
        pass

    @abstractmethod
    def score_data_quality(self, data_item: Dict[str, Any]) -> float:
        """
        Calculate quality score for a single data item.

        Args:
            data_item: Single parsed data item

        Returns:
            Quality score between 0.0 and 10.0
        """
        pass

    @abstractmethod
    def get_analysis_prompt(self, data: List[Dict[str, Any]]) -> str:
        """
        Generate the Gemini analysis prompt for this harvester's data.

        Args:
            data: List of harvested data items

        Returns:
            Prompt string for Gemini API
        """
        pass

    # ============================================================
    # SHARED METHODS - Available to all harvesters
    # ============================================================

    def harvest(self, force: bool = False) -> Dict[str, Any]:
        """
        Main harvest method - orchestrates the entire harvesting process.

        Args:
            force: If True, bypass cache and force fresh harvest

        Returns:
            Dict with keys: 'status', 'data', 'count', 'timestamp'
        """
        start_time = time.time()
        self.logger.info(f"Starting harvest for {self.harvester_name}")

        try:
            # Check cache first (unless force=True)
            if not force:
                cached_data = self.get_cached_data(hours=24)
                if cached_data:
                    self.logger.info(f"Using cached data ({len(cached_data)} items)")
                    return {
                        'status': 'success',
                        'source': 'cache',
                        'data': cached_data,
                        'count': len(cached_data),
                        'timestamp': datetime.now().isoformat()
                    }

            # Harvest from all sources
            all_raw_data = []
            sources = self.get_data_sources()

            for source in sources:
                if source['name'].lower() not in [s.lower() for s in self.enabled_sources]:
                    self.logger.info(f"Skipping disabled source: {source['name']}")
                    continue

                try:
                    self.logger.info(f"Harvesting from {source['name']}")
                    raw_data = self.extract_raw_data(source)
                    all_raw_data.extend(raw_data)
                    self.logger.info(f"Extracted {len(raw_data)} items from {source['name']}")
                except Exception as e:
                    self.logger.error(f"Error harvesting {source['name']}: {str(e)}")
                    continue

            if not all_raw_data:
                raise Exception("No data extracted from any source")

            # Parse the data
            self.logger.info(f"Parsing {len(all_raw_data)} raw items")
            parsed_data = self.parse_data(all_raw_data)

            # Score data quality
            self.logger.info("Scoring data quality")
            scored_data = []
            for item in parsed_data:
                try:
                    score = self.score_data_quality(item)
                    item['quality_score'] = score
                    if score >= self.quality_threshold:
                        scored_data.append(item)
                except Exception as e:
                    self.logger.error(f"Error scoring item: {str(e)}")
                    continue

            self.logger.info(f"Kept {len(scored_data)}/{len(parsed_data)} items above threshold {self.quality_threshold}")

            # Analyze with Gemini
            self.logger.info("Analyzing data with Gemini")
            analyzed_data = self.analyze_with_gemini(scored_data)

            # Save to database
            self.logger.info("Saving to database")
            self.save_to_database(analyzed_data)

            # Log harvest event
            execution_time = int((time.time() - start_time) * 1000)  # ms
            self.log_harvest_event('success', len(analyzed_data), execution_time)

            self.logger.info(f"Harvest completed successfully in {execution_time}ms")

            return {
                'status': 'success',
                'source': 'fresh',
                'data': analyzed_data,
                'count': len(analyzed_data),
                'timestamp': datetime.now().isoformat(),
                'execution_time_ms': execution_time
            }

        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            self.logger.error(f"Harvest failed: {str(e)}")
            self.log_harvest_event('error', 0, execution_time, str(e))

            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def analyze_with_gemini(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze harvested data using Gemini API.

        Args:
            data: List of scored data items

        Returns:
            Data with added 'gemini_analysis' field
        """
        try:
            # Lazy load Gemini analyzer
            if self._gemini_analyzer is None:
                from ..analyzers.gemini_analyzer import GeminiAnalyzer
                self._gemini_analyzer = GeminiAnalyzer()

            # Get analysis prompt
            prompt = self.get_analysis_prompt(data)

            # Analyze with Gemini
            analysis_result = self._gemini_analyzer.analyze_data(
                data=data,
                analysis_type=self.harvester_name,
                prompt=prompt
            )

            # Add analysis to data
            for item in data:
                item['gemini_analysis'] = analysis_result.get('insights', {})
                item['analyzed_at'] = datetime.now().isoformat()

            return data

        except Exception as e:
            self.logger.error(f"Gemini analysis failed: {str(e)}")
            # Return data without analysis if Gemini fails
            for item in data:
                item['gemini_analysis'] = {'error': str(e)}
            return data

    def save_to_database(self, data: List[Dict[str, Any]]) -> None:
        """
        Save harvested data to the central database.

        Args:
            data: List of analyzed data items
        """
        try:
            # Lazy load database
            if self._database is None:
                from ..database.harvested_data import HarvestedDataDB
                self._database = HarvestedDataDB()

            # Save each item
            for item in data:
                self._database.save_harvested_data(
                    harvester_name=self.harvester_name,
                    data=item
                )

            self.logger.info(f"Saved {len(data)} items to database")

        except Exception as e:
            self.logger.error(f"Database save failed: {str(e)}")
            raise

    def get_cached_data(self, hours: int = 24) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached data from database if available and fresh.

        Args:
            hours: Maximum age of cached data in hours

        Returns:
            Cached data or None if not available/expired
        """
        try:
            # Lazy load database
            if self._database is None:
                from ..database.harvested_data import HarvestedDataDB
                self._database = HarvestedDataDB()

            # Get latest data
            cached_data = self._database.get_latest_data(
                source_type=self.harvester_name,
                max_age_hours=hours
            )

            return cached_data if cached_data else None

        except Exception as e:
            self.logger.error(f"Cache retrieval failed: {str(e)}")
            return None

    def log_harvest_event(self, status: str, count: int, execution_time: int,
                          error_message: str = None) -> None:
        """
        Log a harvest event to the database.

        Args:
            status: 'success', 'error', or 'warning'
            count: Number of items harvested
            execution_time: Execution time in milliseconds
            error_message: Error message if status='error'
        """
        try:
            # Lazy load database
            if self._database is None:
                from ..database.harvested_data import HarvestedDataDB
                self._database = HarvestedDataDB()

            self._database.log_harvest_event(
                harvester_name=self.harvester_name,
                status=status,
                record_count=count,
                execution_time=execution_time,
                error_message=error_message
            )

        except Exception as e:
            self.logger.error(f"Harvest logging failed: {str(e)}")

    def get_harvest_stats(self) -> Dict[str, Any]:
        """
        Get harvest statistics for this harvester.

        Returns:
            Dict with harvest statistics
        """
        try:
            # Lazy load database
            if self._database is None:
                from ..database.harvested_data import HarvestedDataDB
                self._database = HarvestedDataDB()

            return self._database.get_harvest_stats(self.harvester_name)

        except Exception as e:
            self.logger.error(f"Stats retrieval failed: {str(e)}")
            return {}

    # ============================================================
    # UTILITY METHODS
    # ============================================================

    def filter_by_quality(self, data: List[Dict[str, Any]],
                          min_score: float = None) -> List[Dict[str, Any]]:
        """
        Filter data by quality score.

        Args:
            data: List of data items with 'quality_score'
            min_score: Minimum score (defaults to quality_threshold)

        Returns:
            Filtered data list
        """
        threshold = min_score if min_score is not None else self.quality_threshold
        return [item for item in data if item.get('quality_score', 0) >= threshold]

    def deduplicate_data(self, data: List[Dict[str, Any]],
                         key: str = 'id') -> List[Dict[str, Any]]:
        """
        Remove duplicate items based on a key.

        Args:
            data: List of data items
            key: Key to use for deduplication

        Returns:
            Deduplicated data list
        """
        seen = set()
        unique_data = []

        for item in data:
            identifier = item.get(key)
            if identifier and identifier not in seen:
                seen.add(identifier)
                unique_data.append(item)

        return unique_data

    def sort_by_quality(self, data: List[Dict[str, Any]],
                        descending: bool = True) -> List[Dict[str, Any]]:
        """
        Sort data by quality score.

        Args:
            data: List of data items with 'quality_score'
            descending: If True, sort highest to lowest

        Returns:
            Sorted data list
        """
        return sorted(
            data,
            key=lambda x: x.get('quality_score', 0),
            reverse=descending
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.harvester_name}' threshold={self.quality_threshold}>"