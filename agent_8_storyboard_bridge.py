"""
Agent 8 Storyboard Integration Bridge
4 APIs for connecting Storyboard App with Agent 8 training system
Stand: 12.11.2025
"""

import json
from typing import Dict, Optional
from datetime import datetime
import logging

from agent_8_metrics import Agent8MetricsCollector
from agent_8_prompt_refiner import Agent8PromptRefiner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Agent8StoryboardBridge:
    """Bridge between Storyboard App and Agent 8"""

    def __init__(
        self,
        config_path: str = "config_agent8.json",
        metrics_db: str = "data/agent_8_metrics.json"
    ):
        try:
            self.metrics = Agent8MetricsCollector(metrics_db)
            self.agent8 = Agent8PromptRefiner(config_path)
            logger.info("✅ Agent8StoryboardBridge initialized")
        except Exception as e:
            logger.error(f"❌ Init failed: {e}")
            raise

    # ═══════════════════════════════════════════════════════════════════════
    # API 1: VALIDATE FROM STORYBOARD
    # ═══════════════════════════════════════════════════════════════════════

    def validate_prompt_from_storyboard(
        self,
        prompt: str,
        prompt_type: str,
        genre: str,
        storyboard_scene_id: str
    ) -> Dict:
        """
        Validate prompt from Storyboard UI

        Called when user clicks "Validate" button

        Returns:
            Dict with validation results, refined prompt, metrics
        """
        try:
            logger.info(f"🔍 Validating: {genre} ({prompt_type})")

            # Run Agent 8 validation
            report = self.agent8.validate_and_refine(prompt, prompt_type, genre)

            # Record in metrics
            val_id = self.metrics.record_validation(
                prompt=prompt,
                prompt_type=prompt_type,
                genre=genre,
                quality_score=report.validation_scores.overall_quality_score,
                issues=[i.message for i in report.issues_found],
                fixes=[f.fix_type for f in report.auto_fixes_applied],
                ready=report.ready_for_generation,
                storyboard_id=storyboard_scene_id
            )

            return {
                "status": "success",
                "validation_id": val_id,
                "validation": {
                    "quality_score": report.validation_scores.overall_quality_score,
                    "quality_rating": report.estimated_quality_rating,
                    "ready_for_generation": report.ready_for_generation,
                    "scores": {
                        "structural": report.validation_scores.structural,
                        "genre": report.validation_scores.genre_compliance,
                        "artifacts": report.validation_scores.artifact_risk,
                        "consistency": report.validation_scores.consistency,
                        "performance": report.validation_scores.performance_optimization
                    },
                    "issues": [{"severity": i.severity, "message": i.message} for i in report.issues_found],
                    "recommendations": report.recommendations
                },
                "refined_prompt": report.refined_prompt,
                "original_prompt": report.original_prompt,
                "auto_fixes": [f.fix_type for f in report.auto_fixes_applied],
                "generation_mode": report.generation_mode_recommendation,
                "genre_detected": report.genre_detected,
                "metrics": self.metrics.get_summary(),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Validation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    # ═══════════════════════════════════════════════════════════════════════
    # API 2: GENERATION FEEDBACK
    # ═══════════════════════════════════════════════════════════════════════

    def send_generation_feedback(
        self,
        validation_id: str,
        generation_success: bool,
        generation_quality_score: float,
        error_message: Optional[str] = None
    ) -> Dict:
        """
        Send generation feedback from Agent 5c/5d

        Called after video generation completes

        Returns:
            Dict with updated metrics and recommendations
        """
        try:
            logger.info(f"📊 Feedback for {validation_id}: {generation_success}")

            success = self.metrics.add_generation_feedback(
                validation_id,
                generation_success,
                generation_quality_score
            )

            if not success:
                return {
                    "status": "error",
                    "error": f"Validation {validation_id} not found",
                    "timestamp": datetime.now().isoformat()
                }

            return {
                "status": "success",
                "message": f"Feedback recorded for {validation_id}",
                "updated_metrics": self.metrics.get_summary(),
                "recommendations": self.metrics.get_recommendations(),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Feedback failed: {e}")
            return {"status": "error", "error": str(e), "timestamp": datetime.now().isoformat()}

    # ═══════════════════════════════════════════════════════════════════════
    # API 3: GET DASHBOARD DATA
    # ═══════════════════════════════════════════════════════════════════════

    def get_dashboard_data(self) -> Dict:
        """
        Get dashboard data for Storyboard UI

        Returns:
            Dict with overview, per-genre stats, recommendations
        """
        try:
            logger.info("📈 Fetching dashboard data")

            summary = self.metrics.get_summary()
            recs = self.metrics.get_recommendations()
            recent = self.metrics.get_recent(10)

            # Determine system status
            avg_q = summary["summary"]["avg_quality"]
            if avg_q > 0.85:
                status = "excellent"
                msg = "🟢 Excellent performance"
            elif avg_q > 0.75:
                status = "good"
                msg = "🟢 Good performance"
            elif avg_q > 0.65:
                status = "fair"
                msg = "🟡 Fair - needs monitoring"
            else:
                status = "poor"
                msg = "🔴 Needs attention"

            return {
                "status": "success",
                "overview": {
                    "total_validations": summary["summary"]["total"],
                    "avg_quality_score": summary["summary"]["avg_quality"],
                    "success_rate": summary["summary"].get("success_rate", 0.0),
                    "system_status": status,
                    "status_message": msg,
                    "last_updated": summary["timestamp"]
                },
                "by_genre": summary["by_genre"],
                "by_prompt_type": summary["by_type"],
                "recommendations": recs,
                "recent_validations": [
                    {
                        "id": r["id"],
                        "timestamp": r["timestamp"],
                        "genre": r.get("genre", r.get("input", {}).get("genre", "unknown")),
                        "prompt_type": r.get("prompt_type", r.get("input", {}).get("prompt_type", "unknown")),
                        "quality_score": r.get("quality_score", r.get("validation", {}).get("quality_score", 0.0)),
                        "ready": r.get("ready", r.get("validation", {}).get("ready_for_generation", False)),
                        "generation_success": r.get("generation_success", r.get("generation_feedback", {}).get("success")),
                        "storyboard_id": r.get("storyboard_id")
                    }
                    for r in recent
                ],
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Dashboard failed: {e}")
            return {"status": "error", "error": str(e), "timestamp": datetime.now().isoformat()}

    # ═══════════════════════════════════════════════════════════════════════
    # API 4: MANUAL USER FEEDBACK
    # ═══════════════════════════════════════════════════════════════════════

    def send_manual_feedback(
        self,
        validation_id: str,
        user_satisfaction: int,
        notes: str
    ) -> Dict:
        """
        Send manual user feedback from Storyboard UI

        Args:
            validation_id: ID from validation
            user_satisfaction: 1-5 stars
            notes: User comments

        Returns:
            Dict with confirmation
        """
        try:
            logger.info(f"💬 Manual feedback: {user_satisfaction} stars")

            if not 1 <= user_satisfaction <= 5:
                return {
                    "status": "error",
                    "error": "Satisfaction must be 1-5",
                    "timestamp": datetime.now().isoformat()
                }

            success = self.metrics.add_user_feedback(
                validation_id,
                user_satisfaction,
                notes
            )

            if not success:
                return {
                    "status": "error",
                    "error": f"Validation {validation_id} not found",
                    "timestamp": datetime.now().isoformat()
                }

            return {
                "status": "success",
                "message": "User feedback recorded",
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Manual feedback failed: {e}")
            return {"status": "error", "error": str(e), "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    print("=" * 80)
    print("AGENT 8 STORYBOARD BRIDGE - TEST")
    print("=" * 80)

    bridge = Agent8StoryboardBridge()

    # Test API 1: Validation
    print("\n1. Testing validation...")
    result = bridge.validate_prompt_from_storyboard(
        prompt="""[IDENTITY] Woman, 30s
        [CINEMATOGRAPHY] Dolly-in
        [ENVIRONMENT] Modern apartment
        [PERFORMANCE] Walks to window
        [AUDIO] Dialogue: "Thinking"
        [NEGATIVES] No watermark""",
        prompt_type="veo_3.1",
        genre="reggaeton",
        storyboard_scene_id="scene_001"
    )
    print(f"Status: {result['status']}")
    print(f"Quality: {result['validation']['quality_score']:.2f}")
    val_id = result.get('validation_id')

    # Test API 2: Generation feedback
    print("\n2. Testing generation feedback...")
    fb_result = bridge.send_generation_feedback(val_id, True, 0.88)
    print(f"Status: {fb_result['status']}")

    # Test API 3: Dashboard
    print("\n3. Testing dashboard...")
    dash = bridge.get_dashboard_data()
    print(f"Status: {dash['status']}")
    print(f"Total: {dash['overview']['total_validations']}")

    # Test API 4: Manual feedback
    print("\n4. Testing manual feedback...")
    manual = bridge.send_manual_feedback(val_id, 5, "Perfect!")
    print(f"Status: {manual['status']}")

    print("\n" + "=" * 80)
    print("✅ All APIs tested!")
    print("=" * 80)
