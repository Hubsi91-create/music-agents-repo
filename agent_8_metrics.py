"""
AGENT 8 METRICS COLLECTION SYSTEM
Collects training data from real validations
Called by Storyboard App and Agent 5c/5d

Stand: 12. November 2025
Version: 1.0
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ValidationRecord:
    """Single validation record with all context"""
    id: str
    timestamp: str
    storyboard_id: Optional[str]

    # Input data
    prompt_snippet: str
    prompt_type: str
    genre: str

    # Validation output
    quality_score: float
    ready_for_generation: bool
    issues_count: int
    issues: List[str]
    fixes_count: int
    fixes: List[str]

    # Real-world feedback (optional)
    generation_success: Optional[bool] = None
    generation_quality: Optional[float] = None
    feedback_timestamp: Optional[str] = None

    # User feedback (optional)
    user_satisfaction: Optional[int] = None
    user_notes: Optional[str] = None
    user_feedback_timestamp: Optional[str] = None


class Agent8MetricsCollector:
    """
    Central metrics & training data system for Agent 8

    Tracks:
    - All validation events
    - Real-world generation feedback
    - User manual feedback
    - Performance trends per genre/prompt type
    """

    def __init__(self, db_path: str = "data/agent_8_metrics.json"):
        """
        Initialize metrics collector

        Args:
            db_path: Path to JSON database file
        """
        self.db_path = db_path
        self.ensure_db_exists()
        self.metrics = self.load_metrics()

    def ensure_db_exists(self) -> None:
        """Create data folder and JSON if not exists"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

            if not os.path.exists(self.db_path):
                initial_db = {
                    "metadata": {
                        "version": "1.0",
                        "created": datetime.now().isoformat(),
                        "last_updated": datetime.now().isoformat()
                    },
                    "summary": {
                        "total_validations": 0,
                        "success_count": 0,
                        "avg_quality_score": 0.0,
                        "success_rate": 0.0
                    },
                    "records": [],
                    "by_genre": {},
                    "by_prompt_type": {}
                }

                with open(self.db_path, 'w', encoding='utf-8') as f:
                    json.dump(initial_db, f, indent=2, ensure_ascii=False)

                logger.info(f"✅ Created metrics database at {self.db_path}")

        except Exception as e:
            logger.error(f"❌ Failed to create database: {e}")
            raise

    def record_validation(
        self,
        prompt: str,
        prompt_type: str,
        genre: str,
        quality_score: float,
        issues_found: List[str],
        fixes_applied: List[str],
        ready_for_generation: bool,
        storyboard_id: Optional[str] = None,
        actual_generation_success: Optional[bool] = None,
        generation_quality_score: Optional[float] = None
    ) -> Dict:
        """
        Record a validation event with full context

        Called by:
        1. Agent 8 (after each validation)
        2. Agent 5c/5d (after video generation with feedback)
        3. Storyboard App (manual feedback)

        Args:
            prompt: The validated prompt (will be truncated for storage)
            prompt_type: "veo_3.1" or "runway_gen4"
            genre: Genre identifier
            quality_score: Overall quality score (0.0-1.0)
            issues_found: List of issue messages
            fixes_applied: List of applied fixes
            ready_for_generation: Whether prompt is ready
            storyboard_id: Reference to storyboard scene (optional)
            actual_generation_success: Real generation result (optional)
            generation_quality_score: Real quality from generation (optional)

        Returns:
            Dict containing the created record
        """
        try:
            record_id = f"val_{int(datetime.now().timestamp() * 1000)}"

            record_data = {
                "id": record_id,
                "timestamp": datetime.now().isoformat(),
                "storyboard_id": storyboard_id,

                # Input
                "input": {
                    "prompt": prompt[:200] + "..." if len(prompt) > 200 else prompt,
                    "prompt_type": prompt_type,
                    "genre": genre
                },

                # Validation output
                "validation": {
                    "quality_score": quality_score,
                    "ready_for_generation": ready_for_generation,
                    "issues_count": len(issues_found),
                    "issues": issues_found[:10],  # Top 10 only
                    "fixes_count": len(fixes_applied),
                    "fixes": fixes_applied[:10]   # Top 10 only
                },

                # Real-world feedback (optional)
                "generation_feedback": {
                    "success": actual_generation_success,
                    "quality_score": generation_quality_score,
                    "feedback_timestamp": None
                },

                # User feedback (optional)
                "user_feedback": {
                    "satisfaction": None,
                    "notes": None,
                    "timestamp": None
                }
            }

            # Add to records
            self.metrics["records"].append(record_data)

            # Update summary
            self.update_summary()

            # Save to disk
            self.save_metrics()

            logger.info(
                f"✅ Recorded validation {record_id}: "
                f"{genre} ({prompt_type}) - Score: {quality_score:.2f}"
            )

            return record_data

        except Exception as e:
            logger.error(f"❌ Failed to record validation: {e}")
            raise

    def add_generation_feedback(
        self,
        validation_id: str,
        generation_success: bool,
        generation_quality: float,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Add real-world generation feedback to existing validation record

        Called by Agent 5c/5d AFTER video generation

        Args:
            validation_id: ID of original validation record
            generation_success: Whether generation succeeded
            generation_quality: Quality score from generation (0.0-1.0)
            error_message: Error message if generation failed (optional)

        Returns:
            bool: True if feedback was added, False if record not found
        """
        try:
            for record in self.metrics["records"]:
                if record["id"] == validation_id:
                    record["generation_feedback"]["success"] = generation_success
                    record["generation_feedback"]["quality_score"] = generation_quality
                    record["generation_feedback"]["feedback_timestamp"] = datetime.now().isoformat()

                    if error_message:
                        record["generation_feedback"]["error"] = error_message

                    logger.info(
                        f"✅ Added generation feedback to {validation_id}: "
                        f"Success={generation_success}, Quality={generation_quality:.2f}"
                    )

                    self.update_summary()
                    self.save_metrics()
                    return True

            logger.warning(f"⚠️ Validation record {validation_id} not found")
            return False

        except Exception as e:
            logger.error(f"❌ Failed to add generation feedback: {e}")
            raise

    def add_user_feedback(
        self,
        validation_id: str,
        satisfaction: int,
        notes: str
    ) -> bool:
        """
        Add manual user feedback to validation record

        Called by Storyboard App when user provides feedback

        Args:
            validation_id: ID of validation record
            satisfaction: User satisfaction rating (1-5 stars)
            notes: User's notes/comments

        Returns:
            bool: True if feedback was added, False if record not found
        """
        try:
            if not 1 <= satisfaction <= 5:
                raise ValueError("Satisfaction must be between 1 and 5")

            for record in self.metrics["records"]:
                if record["id"] == validation_id:
                    record["user_feedback"]["satisfaction"] = satisfaction
                    record["user_feedback"]["notes"] = notes
                    record["user_feedback"]["timestamp"] = datetime.now().isoformat()

                    logger.info(
                        f"✅ Added user feedback to {validation_id}: "
                        f"{satisfaction} stars"
                    )

                    self.save_metrics()
                    return True

            logger.warning(f"⚠️ Validation record {validation_id} not found")
            return False

        except Exception as e:
            logger.error(f"❌ Failed to add user feedback: {e}")
            raise

    def update_summary(self) -> None:
        """Update aggregated statistics"""
        try:
            records = self.metrics["records"]

            if not records:
                return

            # Overall stats
            self.metrics["summary"]["total_validations"] = len(records)

            # Success stats (only from records with feedback)
            records_with_feedback = [
                r for r in records
                if r["generation_feedback"]["success"] is not None
            ]

            if records_with_feedback:
                successes = sum(
                    1 for r in records_with_feedback
                    if r["generation_feedback"]["success"]
                )
                self.metrics["summary"]["success_count"] = successes
                self.metrics["summary"]["success_rate"] = (
                    successes / len(records_with_feedback)
                )

            # Average quality score
            scores = [r["validation"]["quality_score"] for r in records]
            self.metrics["summary"]["avg_quality_score"] = sum(scores) / len(scores)

            # By genre
            self._update_genre_stats(records)

            # By prompt type
            self._update_prompt_type_stats(records)

            # Update timestamp
            self.metrics["metadata"]["last_updated"] = datetime.now().isoformat()

        except Exception as e:
            logger.error(f"❌ Failed to update summary: {e}")
            raise

    def _update_genre_stats(self, records: List[Dict]) -> None:
        """Update per-genre statistics"""
        by_genre = {}

        for record in records:
            genre = record["input"]["genre"]

            if genre not in by_genre:
                by_genre[genre] = {
                    "count": 0,
                    "scores": [],
                    "ready_count": 0,
                    "success_count": 0,
                    "total_with_feedback": 0
                }

            by_genre[genre]["count"] += 1
            by_genre[genre]["scores"].append(record["validation"]["quality_score"])

            if record["validation"]["ready_for_generation"]:
                by_genre[genre]["ready_count"] += 1

            if record["generation_feedback"]["success"] is not None:
                by_genre[genre]["total_with_feedback"] += 1
                if record["generation_feedback"]["success"]:
                    by_genre[genre]["success_count"] += 1

        # Calculate final stats
        self.metrics["by_genre"] = {}
        for genre, data in by_genre.items():
            self.metrics["by_genre"][genre] = {
                "count": data["count"],
                "avg_score": sum(data["scores"]) / len(data["scores"]),
                "ready_rate": data["ready_count"] / data["count"],
                "success_rate": (
                    data["success_count"] / data["total_with_feedback"]
                    if data["total_with_feedback"] > 0 else 0.0
                )
            }

    def _update_prompt_type_stats(self, records: List[Dict]) -> None:
        """Update per-prompt-type statistics"""
        by_type = {}

        for record in records:
            ptype = record["input"]["prompt_type"]

            if ptype not in by_type:
                by_type[ptype] = {
                    "count": 0,
                    "scores": [],
                    "success": 0,
                    "total_with_feedback": 0
                }

            by_type[ptype]["count"] += 1
            by_type[ptype]["scores"].append(record["validation"]["quality_score"])

            if record["generation_feedback"]["success"] is not None:
                by_type[ptype]["total_with_feedback"] += 1
                if record["generation_feedback"]["success"]:
                    by_type[ptype]["success"] += 1

        # Calculate final stats
        self.metrics["by_prompt_type"] = {}
        for ptype, data in by_type.items():
            self.metrics["by_prompt_type"][ptype] = {
                "count": data["count"],
                "avg_score": sum(data["scores"]) / len(data["scores"]),
                "success_rate": (
                    data["success"] / data["total_with_feedback"]
                    if data["total_with_feedback"] > 0 else 0.0
                )
            }

    def get_metrics_summary(self) -> Dict:
        """
        Get current metrics summary for dashboard

        Returns:
            Dict containing summary, genre stats, and prompt type stats
        """
        self.update_summary()

        return {
            "summary": self.metrics["summary"],
            "by_genre": self.metrics["by_genre"],
            "by_prompt_type": self.metrics["by_prompt_type"],
            "timestamp": datetime.now().isoformat()
        }

    def get_genre_recommendations(self) -> Dict:
        """
        Analyze data and provide genre-specific recommendations

        Returns:
            Dict with recommendations per genre
        """
        summary = self.get_metrics_summary()
        recommendations = {}

        for genre, stats in summary["by_genre"].items():
            avg_score = stats["avg_score"]
            success_rate = stats["success_rate"]

            # Determine status
            if avg_score > 0.85:
                status = "🟢 Excellent"
                recommendation = (
                    f"✅ {genre}: Performing exceptionally well. "
                    f"Can relax some auto-fix parameters for faster processing."
                )
            elif avg_score > 0.75:
                status = "🟡 Good"
                recommendation = (
                    f"✓ {genre}: Good performance. "
                    f"Monitor for consistency and maintain current settings."
                )
            elif avg_score > 0.65:
                status = "🟠 Fair"
                recommendation = (
                    f"⚠️ {genre}: Moderate performance. "
                    f"Consider increasing auto-fix aggressiveness or adjusting dialog limits."
                )
            else:
                status = "🔴 Needs Work"
                recommendation = (
                    f"⚠️ {genre}: Needs immediate attention. "
                    f"Review validation rules and increase quality thresholds."
                )

            recommendations[genre] = {
                "genre": genre,
                "status": status,
                "avg_score": f"{avg_score:.2f}",
                "success_rate": f"{success_rate*100:.1f}%",
                "recommendation": recommendation,
                "count": stats["count"]
            }

        return recommendations

    def get_recent_records(self, limit: int = 10) -> List[Dict]:
        """
        Get most recent validation records

        Args:
            limit: Maximum number of records to return

        Returns:
            List of recent records (newest first)
        """
        records = self.metrics["records"]
        return list(reversed(records[-limit:]))

    def save_metrics(self) -> None:
        """Save metrics to disk"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"❌ Failed to save metrics: {e}")
            raise

    def load_metrics(self) -> Dict:
        """
        Load metrics from disk

        Returns:
            Dict containing all metrics data
        """
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    "metadata": {},
                    "summary": {},
                    "records": [],
                    "by_genre": {},
                    "by_prompt_type": {}
                }

        except Exception as e:
            logger.error(f"❌ Failed to load metrics: {e}")
            return {
                "metadata": {},
                "summary": {},
                "records": [],
                "by_genre": {},
                "by_prompt_type": {}
            }


# ─────────────────────────────────────────────────────────────────────────────
# USAGE EXAMPLE
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 80)
    print("AGENT 8 METRICS COLLECTOR - TEST")
    print("=" * 80)

    # Initialize collector
    collector = Agent8MetricsCollector("data/agent_8_metrics.json")

    # Record a validation
    print("\n1. Recording validation...")
    record = collector.record_validation(
        prompt="Woman, 30s, walks to window in modern apartment, warm lighting...",
        prompt_type="veo_3.1",
        genre="reggaeton",
        quality_score=0.85,
        issues_found=["Dialog exceeds 7 words"],
        fixes_applied=["too_long_dialog"],
        ready_for_generation=True,
        storyboard_id="scene_001"
    )
    print(f"✓ Recorded: {record['id']}")

    # Add generation feedback
    print("\n2. Adding generation feedback...")
    success = collector.add_generation_feedback(
        validation_id=record['id'],
        generation_success=True,
        generation_quality=0.88
    )
    print(f"✓ Feedback added: {success}")

    # Get metrics summary
    print("\n3. Metrics Summary:")
    summary = collector.get_metrics_summary()
    print(json.dumps(summary, indent=2))

    # Get recommendations
    print("\n4. Genre Recommendations:")
    recommendations = collector.get_genre_recommendations()
    for genre, rec in recommendations.items():
        print(f"\n{rec['status']} {genre}")
        print(f"  Score: {rec['avg_score']} | Success: {rec['success_rate']}")
        print(f"  {rec['recommendation']}")

    print("\n" + "=" * 80)
    print("✅ Test completed successfully!")
    print("=" * 80)
