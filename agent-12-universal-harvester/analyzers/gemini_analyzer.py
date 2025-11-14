"""
Gemini Analyzer - Shared AI Analysis Engine

Uses Google Gemini API to analyze harvested data from all harvesters.
Provides intelligent insights, recommendations, and pattern recognition.

Author: Universal Harvester System
Version: 1.0.0
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)


class GeminiAnalyzer:
    """
    Centralized Gemini AI Analyzer for all harvesters.

    Uses Google's Gemini 2.5 Flash model to analyze harvested data
    and extract actionable insights.
    """

    # System prompts for different harvester types
    SYSTEM_PROMPTS = {
        'trend_harvester': """You are a Trend Analysis Expert for Music Video Production.
Analyze the provided trending data and identify:
1. TOP 10 current trends with scores (1-10)
2. EMERGING trends that are gaining momentum
3. Dominant music genres and styles
4. Viral patterns and characteristics
5. Actionable recommendations for content creators

Return structured JSON with trend rankings and insights.""",

        'audio_harvester': """You are an Audio Curation Expert for Music Video Production.
Analyze the provided audio data and identify:
1. Best tracks for video production (with scores)
2. BPM/Mood recommendations by genre
3. Production quality trends
4. Sound characteristics that perform well
5. Audio pairing recommendations

Return structured JSON with audio recommendations and quality scores.""",

        'screenplay_harvester': """You are a Screenplay & Story Expert for Music Videos.
Analyze the provided story data and identify:
1. Trending story structures and patterns
2. Popular character archetypes
3. Emotional arc templates
4. Dialogue patterns that resonate
5. Story recommendations for music videos

Return structured JSON with story patterns and recommendations.""",

        'creator_harvester': """You are a Creator Matching Expert for Music Videos.
Analyze the provided creator data and identify:
1. Best creator matches for different content types
2. Audience overlap analysis
3. Collaboration potential scores
4. Engagement rate patterns
5. Creator recommendations by niche

Return structured JSON with creator matches and scores.""",

        'distribution_harvester': """You are a Distribution Strategy Expert for Music Videos.
Analyze the provided distribution data and identify:
1. Optimal title patterns for maximum CTR
2. Best hashtag combinations by platform
3. Optimal posting times for each platform
4. Viral hook patterns
5. Distribution strategy recommendations

Return structured JSON with distribution tactics and timing.""",

        'sound_harvester': """You are a Sound Design Expert for Music Production.
Analyze the provided sound design data and identify:
1. Trending production techniques
2. Popular effect chain patterns
3. Best VST/tool combinations
4. Innovation patterns in sound design
5. Technical recommendations for producers

Return structured JSON with sound design techniques and recommendations."""
    }

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash-exp"):
        """
        Initialize Gemini Analyzer.

        Args:
            api_key: Google AI API key (if None, reads from env)
            model: Gemini model to use
        """
        self.logger = logging.getLogger("GeminiAnalyzer")

        # Get API key
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY')
        if not self.api_key:
            self.logger.warning("No Google AI API key found. Set GOOGLE_AI_API_KEY env var.")
            self.enabled = False
            return

        # Configure Gemini
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model)
            self.enabled = True
            self.logger.info(f"Gemini Analyzer initialized with model: {model}")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini: {str(e)}")
            self.enabled = False

    def analyze_data(self, data: List[Dict[str, Any]], analysis_type: str,
                     prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze harvested data using Gemini.

        Args:
            data: List of harvested data items
            analysis_type: Type of harvester (e.g., 'trend_harvester')
            prompt: Custom prompt (if None, uses default system prompt)

        Returns:
            Dict with analysis results and insights
        """
        if not self.enabled:
            return {
                'error': 'Gemini not enabled',
                'insights': {},
                'timestamp': datetime.now().isoformat()
            }

        try:
            # Get system prompt
            system_prompt = self.SYSTEM_PROMPTS.get(analysis_type, "")

            # Prepare data for analysis (limit size)
            data_summary = self._prepare_data_for_analysis(data, max_items=100)

            # Build full prompt
            full_prompt = f"""{system_prompt}

DATA TO ANALYZE:
{json.dumps(data_summary, indent=2)}

{prompt if prompt else ''}

Provide a detailed analysis in JSON format with actionable insights."""

            # Generate analysis
            self.logger.info(f"Analyzing {len(data)} items with Gemini ({analysis_type})")
            response = self.model.generate_content(full_prompt)

            # Parse response
            analysis_result = self._parse_gemini_response(response.text)

            return {
                'status': 'success',
                'insights': analysis_result,
                'analyzed_items': len(data),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Gemini analysis failed: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'insights': {},
                'timestamp': datetime.now().isoformat()
            }

    def extract_insights(self, data: List[Dict[str, Any]], category: str) -> Dict[str, Any]:
        """
        Extract key insights from data.

        Args:
            data: List of data items
            category: Category for insight extraction

        Returns:
            Dict with extracted insights
        """
        if not self.enabled:
            return {'error': 'Gemini not enabled'}

        try:
            prompt = f"""Extract the most important insights from this {category} data.
Focus on actionable recommendations and key patterns.
Return top 5 insights with importance scores (1-10).

Data: {json.dumps(data[:50], indent=2)}"""

            response = self.model.generate_content(prompt)
            insights = self._parse_gemini_response(response.text)

            return {
                'category': category,
                'insights': insights,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Insight extraction failed: {str(e)}")
            return {'error': str(e)}

    def summarize_findings(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize analysis findings into concise recommendations.

        Args:
            analysis_results: Full analysis results

        Returns:
            Dict with summary and top recommendations
        """
        if not self.enabled:
            return {'error': 'Gemini not enabled'}

        try:
            prompt = f"""Summarize these analysis results into:
1. Executive summary (2-3 sentences)
2. Top 3 recommendations
3. Action items for content creators

Analysis Results: {json.dumps(analysis_results, indent=2)}"""

            response = self.model.generate_content(prompt)
            summary = self._parse_gemini_response(response.text)

            return {
                'summary': summary,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Summarization failed: {str(e)}")
            return {'error': str(e)}

    # ============================================================
    # SPECIALIZED ANALYSIS METHODS
    # ============================================================

    def analyze_trends(self, trend_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Specialized trend analysis."""
        prompt = """Identify:
1. Top 10 trends with viral potential scores
2. Emerging trends in early growth phase
3. Declining trends to avoid
4. Genre dominance patterns
5. Best trends for new creators"""

        return self.analyze_data(trend_data, 'trend_harvester', prompt)

    def analyze_audio_quality(self, audio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Specialized audio quality analysis."""
        prompt = """Evaluate:
1. Production quality patterns
2. BPM trends by genre
3. Mood/Energy recommendations
4. Audio characteristics of viral tracks
5. Best tracks for video pairing"""

        return self.analyze_data(audio_data, 'audio_harvester', prompt)

    def analyze_story_patterns(self, screenplay_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Specialized screenplay pattern analysis."""
        prompt = """Identify:
1. Viral story structures
2. Character archetypes that resonate
3. Emotional arc patterns
4. Dialogue techniques
5. Story templates for music videos"""

        return self.analyze_data(screenplay_data, 'screenplay_harvester', prompt)

    def analyze_creator_matches(self, creator_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Specialized creator matching analysis."""
        prompt = """Evaluate:
1. Creator-content fit scores
2. Audience overlap patterns
3. Collaboration potential
4. Engagement rate patterns
5. Niche recommendations"""

        return self.analyze_data(creator_data, 'creator_harvester', prompt)

    def analyze_distribution_strategy(self, distribution_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Specialized distribution strategy analysis."""
        prompt = """Optimize:
1. Title patterns for max CTR
2. Hashtag combinations by platform
3. Optimal posting times
4. Viral hook structures
5. Platform-specific tactics"""

        return self.analyze_data(distribution_data, 'distribution_harvester', prompt)

    def analyze_sound_design(self, sound_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Specialized sound design analysis."""
        prompt = """Identify:
1. Trending production techniques
2. Effect chain patterns
3. Popular VST/tool combinations
4. Innovation patterns
5. Technical recommendations"""

        return self.analyze_data(sound_data, 'sound_harvester', prompt)

    # ============================================================
    # UTILITY METHODS
    # ============================================================

    def _prepare_data_for_analysis(self, data: List[Dict[str, Any]],
                                   max_items: int = 100) -> List[Dict[str, Any]]:
        """
        Prepare data for Gemini analysis (limit size, clean data).

        Args:
            data: Full data list
            max_items: Maximum items to include

        Returns:
            Cleaned and limited data list
        """
        # Limit number of items
        limited_data = data[:max_items]

        # Remove large fields that aren't needed for analysis
        cleaned_data = []
        for item in limited_data:
            cleaned_item = {}
            for key, value in item.items():
                # Skip very large fields
                if isinstance(value, str) and len(value) > 500:
                    cleaned_item[key] = value[:500] + "..."
                elif key not in ['raw_html', 'full_transcript', 'image_data']:
                    cleaned_item[key] = value
            cleaned_data.append(cleaned_item)

        return cleaned_data

    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Gemini response (handles JSON and text responses).

        Args:
            response_text: Raw response from Gemini

        Returns:
            Parsed dict
        """
        try:
            # Try to extract JSON from markdown code blocks
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_str = response_text[json_start:json_end].strip()
                return json.loads(json_str)
            elif '```' in response_text:
                # Try generic code block
                json_start = response_text.find('```') + 3
                json_end = response_text.find('```', json_start)
                json_str = response_text[json_start:json_end].strip()
                return json.loads(json_str)
            else:
                # Try direct JSON parse
                return json.loads(response_text)

        except json.JSONDecodeError:
            # If not JSON, return as text
            self.logger.warning("Response not in JSON format, returning as text")
            return {
                'raw_response': response_text,
                'parsed': False
            }

    def test_connection(self) -> bool:
        """
        Test Gemini API connection.

        Returns:
            True if connection successful
        """
        if not self.enabled:
            return False

        try:
            response = self.model.generate_content("Say 'OK' if you can read this.")
            return 'ok' in response.text.lower()
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False

    def __repr__(self) -> str:
        status = "enabled" if self.enabled else "disabled"
        return f"<GeminiAnalyzer status='{status}'>"