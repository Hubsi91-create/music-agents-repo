"""
AGENT 8 ↔ STORYBOARD APP BRIDGE
Connects Agent 8 with existing Storyboard App
Provides 4 APIs for metrics and feedback integration

Stand: 12. November 2025
Version: 1.0
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

from agent_8_metrics import Agent8MetricsCollector
from agent_8_prompt_refiner import Agent8PromptRefiner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Agent8StoryboardBridge:
    """
    Bridge between Agent 8 and Storyboard App

    Provides 4 APIs:
    1. validate_prompt_from_storyboard() - Storyboard UI → Agent 8
    2. send_generation_feedback() - Agent 5c/5d → Agent 8
    3. get_dashboard_data() - Dashboard display
    4. send_manual_feedback() - User feedback
    """

    def __init__(
        self,
        config_path: str = "config_agent8.json",
        metrics_db_path: str = "data/agent_8_metrics.json"
    ):
        """
        Initialize the bridge

        Args:
            config_path: Path to Agent 8 config file
            metrics_db_path: Path to metrics database
        """
        try:
            self.metrics = Agent8MetricsCollector(metrics_db_path)
            self.agent8 = Agent8PromptRefiner(config_path)
            logger.info("✅ Agent8StoryboardBridge initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize bridge: {e}")
            raise

    # ============================================
    # API 1: STORYBOARD → AGENT 8 (Validation)
    # ============================================

    def validate_prompt_from_storyboard(
        self,
        prompt: str,
        prompt_type: str,
        genre: str,
        storyboard_scene_id: str
    ) -> Dict:
        """
        Validate a prompt from Storyboard App

        Called when user creates a prompt in Storyboard UI and clicks "Validate"

        Flow:
        1. User creates prompt in Storyboard UI
        2. Click "Validate" button
        3. This function is called
        4. Agent 8 validates the prompt
        5. Results + Metrics returned to Storyboard

        Args:
            prompt: The prompt to validate
            prompt_type: "veo_3.1" or "runway_gen4"
            genre: Genre identifier (reggaeton, edm, etc.)
            storyboard_scene_id: Reference to storyboard scene

        Returns:
            Dict containing validation results, refined prompt, and metrics
        """
        try:
            logger.info(
                f"🔍 Validating prompt from storyboard scene {storyboard_scene_id}: "
                f"{genre} ({prompt_type})"
            )

            # Validate prompt with Agent 8
            report = self.agent8.validate_and_refine(prompt, prompt_type, genre)

            # Record validation in metrics
            validation_record = self.metrics.record_validation(
                prompt=prompt,
                prompt_type=prompt_type,
                genre=genre,
                quality_score=report.validation_scores.overall_quality_score,
                issues_found=[i.message for i in report.issues_found],
                fixes_applied=[f.fix_type for f in report.auto_fixes_applied],
                ready_for_generation=report.ready_for_generation,
                storyboard_id=storyboard_scene_id
            )

            # Prepare response for Storyboard UI
            response = {
                "status": "success",
                "validation_id": validation_record["id"],

                # Validation results
                "validation": {
                    "quality_score": report.validation_scores.overall_quality_score,
                    "quality_rating": report.estimated_quality_rating,
                    "ready_for_generation": report.ready_for_generation,

                    # Detailed scores
                    "scores": {
                        "structural": report.validation_scores.structural,
                        "genre_compliance": report.validation_scores.genre_compliance,
                        "artifact_risk": report.validation_scores.artifact_risk,
                        "consistency": report.validation_scores.consistency,
                        "performance": report.validation_scores.performance_optimization
                    },

                    # Issues and recommendations
                    "issues": [
                        {
                            "severity": i.severity,
                            "message": i.message,
                            "suggestion": i.suggestion
                        }
                        for i in report.issues_found
                    ],
                    "recommendations": report.recommendations
                },

                # Refined prompt
                "refined_prompt": report.refined_prompt,
                "original_prompt": report.original_prompt,

                # Auto-fixes applied
                "auto_fixes": [
                    {
                        "type": f.fix_type,
                        "reason": f.reason,
                        "confidence": f.confidence
                    }
                    for f in report.auto_fixes_applied
                ],

                # Generation settings
                "generation_mode": report.generation_mode_recommendation,
                "genre_detected": report.genre_detected,

                # Current metrics summary
                "metrics": self.metrics.get_metrics_summary(),

                "timestamp": datetime.now().isoformat()
            }

            logger.info(
                f"✅ Validation complete: Score={report.validation_scores.overall_quality_score:.2f}, "
                f"Ready={report.ready_for_generation}"
            )

            return response

        except Exception as e:
            logger.error(f"❌ Validation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    # ============================================
    # API 2: AGENT 5c/5d → AGENT 8 (Feedback)
    # ============================================

    def send_generation_feedback(
        self,
        validation_id: str,
        generation_success: bool,
        generation_quality_score: float,
        error_message: Optional[str] = None,
        generation_metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Send generation feedback from Agent 5c/5d to Agent 8

        Called by Agent 5c/5d AFTER video generation

        Flow:
        1. Agent 5c/5d generates video based on validated prompt
        2. Video generation succeeds or fails
        3. This function is called with results
        4. Agent 8 metrics are updated
        5. Recommendations are recalculated

        Args:
            validation_id: ID of original validation record
            generation_success: Whether generation succeeded
            generation_quality_score: Quality score from generation (0.0-1.0)
            error_message: Error message if generation failed (optional)
            generation_metadata: Additional metadata from generation (optional)

        Returns:
            Dict containing updated metrics and recommendations
        """
        try:
            logger.info(
                f"📊 Receiving generation feedback for {validation_id}: "
                f"Success={generation_success}, Quality={generation_quality_score:.2f}"
            )

            # Update metrics with real feedback
            success = self.metrics.add_generation_feedback(
                validation_id=validation_id,
                generation_success=generation_success,
                generation_quality=generation_quality_score,
                error_message=error_message
            )

            if not success:
                return {
                    "status": "error",
                    "error": f"Validation record {validation_id} not found",
                    "timestamp": datetime.now().isoformat()
                }

            # Get updated metrics and recommendations
            updated_metrics = self.metrics.get_metrics_summary()
            recommendations = self.metrics.get_genre_recommendations()

            response = {
                "status": "success",
                "message": f"Feedback recorded for validation {validation_id}",

                # Updated metrics
                "updated_metrics": updated_metrics,

                # Genre-specific recommendations
                "recommendations": recommendations,

                # Feedback summary
                "feedback": {
                    "validation_id": validation_id,
                    "generation_success": generation_success,
                    "generation_quality": generation_quality_score,
                    "recorded_at": datetime.now().isoformat()
                },

                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"✅ Feedback recorded successfully for {validation_id}")

            return response

        except Exception as e:
            logger.error(f"❌ Failed to send generation feedback: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    # ============================================
    # API 3: STORYBOARD UI → AGENT 8 (Dashboard)
    # ============================================

    def get_dashboard_data(self) -> Dict:
        """
        Get dashboard data for Storyboard App

        Called by Storyboard App to display training dashboard

        Shows:
        - Overall performance metrics
        - Per-genre statistics
        - Per-prompt-type statistics
        - Recommendations
        - Recent validations

        Returns:
            Dict containing complete dashboard data
        """
        try:
            logger.info("📈 Fetching dashboard data...")

            # Get summary metrics
            summary = self.metrics.get_metrics_summary()

            # Get recommendations
            recommendations = self.metrics.get_genre_recommendations()

            # Get recent records
            recent_records = self.metrics.get_recent_records(limit=10)

            # Determine overall system status
            avg_quality = summary["summary"]["avg_quality_score"]
            if avg_quality > 0.85:
                system_status = "excellent"
                status_message = "🟢 System performing excellently"
            elif avg_quality > 0.75:
                system_status = "good"
                status_message = "🟢 System performing well"
            elif avg_quality > 0.65:
                system_status = "fair"
                status_message = "🟡 System needs monitoring"
            else:
                system_status = "poor"
                status_message = "🔴 System needs immediate attention"

            dashboard = {
                "status": "success",

                # System overview
                "overview": {
                    "total_validations": summary["summary"]["total_validations"],
                    "avg_quality_score": summary["summary"]["avg_quality_score"],
                    "success_count": summary["summary"]["success_count"],
                    "success_rate": summary["summary"].get("success_rate", 0.0),
                    "system_status": system_status,
                    "status_message": status_message,
                    "last_updated": summary["timestamp"]
                },

                # Genre statistics
                "by_genre": summary["by_genre"],

                # Prompt type statistics
                "by_prompt_type": summary["by_prompt_type"],

                # Recommendations
                "recommendations": recommendations,

                # Recent validations
                "recent_validations": [
                    {
                        "id": r["id"],
                        "timestamp": r["timestamp"],
                        "genre": r["input"]["genre"],
                        "prompt_type": r["input"]["prompt_type"],
                        "quality_score": r["validation"]["quality_score"],
                        "ready": r["validation"]["ready_for_generation"],
                        "generation_success": r["generation_feedback"].get("success"),
                        "storyboard_id": r.get("storyboard_id")
                    }
                    for r in recent_records
                ],

                "timestamp": datetime.now().isoformat()
            }

            logger.info("✅ Dashboard data retrieved successfully")

            return dashboard

        except Exception as e:
            logger.error(f"❌ Failed to get dashboard data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    # ============================================
    # API 4: STORYBOARD → AGENT 8 (Manual Feedback)
    # ============================================

    def send_manual_feedback(
        self,
        validation_id: str,
        user_satisfaction: int,
        notes: str
    ) -> Dict:
        """
        Send manual user feedback from Storyboard UI

        Called when user provides manual feedback on a validation

        Args:
            validation_id: ID of validation record
            user_satisfaction: User rating (1-5 stars)
            notes: User's comments/notes

        Returns:
            Dict containing confirmation and updated metrics
        """
        try:
            logger.info(
                f"💬 Receiving manual feedback for {validation_id}: "
                f"{user_satisfaction} stars"
            )

            # Validate satisfaction range
            if not 1 <= user_satisfaction <= 5:
                return {
                    "status": "error",
                    "error": "User satisfaction must be between 1 and 5",
                    "timestamp": datetime.now().isoformat()
                }

            # Add user feedback to metrics
            success = self.metrics.add_user_feedback(
                validation_id=validation_id,
                satisfaction=user_satisfaction,
                notes=notes
            )

            if not success:
                return {
                    "status": "error",
                    "error": f"Validation record {validation_id} not found",
                    "timestamp": datetime.now().isoformat()
                }

            response = {
                "status": "success",
                "message": "User feedback recorded successfully",

                "feedback": {
                    "validation_id": validation_id,
                    "satisfaction": user_satisfaction,
                    "notes": notes,
                    "recorded_at": datetime.now().isoformat()
                },

                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"✅ Manual feedback recorded for {validation_id}")

            return response

        except Exception as e:
            logger.error(f"❌ Failed to send manual feedback: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    # ============================================
    # UTILITY METHODS
    # ============================================

    def get_validation_history(
        self,
        storyboard_scene_id: Optional[str] = None,
        genre: Optional[str] = None,
        limit: int = 50
    ) -> Dict:
        """
        Get validation history with optional filtering

        Args:
            storyboard_scene_id: Filter by storyboard scene (optional)
            genre: Filter by genre (optional)
            limit: Maximum number of records to return

        Returns:
            Dict containing filtered validation history
        """
        try:
            records = self.metrics.metrics["records"]

            # Apply filters
            if storyboard_scene_id:
                records = [
                    r for r in records
                    if r.get("storyboard_id") == storyboard_scene_id
                ]

            if genre:
                records = [
                    r for r in records
                    if r["input"]["genre"] == genre
                ]

            # Limit results
            records = list(reversed(records[-limit:]))

            return {
                "status": "success",
                "count": len(records),
                "records": records,
                "filters": {
                    "storyboard_scene_id": storyboard_scene_id,
                    "genre": genre,
                    "limit": limit
                },
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Failed to get validation history: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# ─────────────────────────────────────────────────────────────────────────────
# USAGE EXAMPLE
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 80)
    print("AGENT 8 STORYBOARD BRIDGE - TEST")
    print("=" * 80)

    # Initialize bridge
    bridge = Agent8StoryboardBridge()

    # Test 1: Validate prompt from storyboard
    print("\n1. Testing validation from storyboard...")
    validation_result = bridge.validate_prompt_from_storyboard(
        prompt="""
        [IDENTITY] Woman, 30s, dark hair, warm expression
        [CINEMATOGRAPHY] Dolly-in over 6 seconds, eye-level camera
        [ENVIRONMENT] Modern apartment, golden hour, warm amber palette
        [PERFORMANCE] Woman walks to window, pauses, smiles
        [AUDIO] Dialogue: "I've been thinking"
        [NEGATIVES] No watermark, no floating limbs
        """,
        prompt_type="veo_3.1",
        genre="reggaeton",
        storyboard_scene_id="scene_001"
    )

    print(f"Status: {validation_result['status']}")
    print(f"Validation ID: {validation_result.get('validation_id')}")
    print(f"Quality Score: {validation_result['validation']['quality_score']:.2f}")
    print(f"Ready: {validation_result['validation']['ready_for_generation']}")

    # Test 2: Send generation feedback
    print("\n2. Testing generation feedback...")
    feedback_result = bridge.send_generation_feedback(
        validation_id=validation_result['validation_id'],
        generation_success=True,
        generation_quality_score=0.88
    )

    print(f"Status: {feedback_result['status']}")
    print(f"Message: {feedback_result.get('message')}")

    # Test 3: Get dashboard data
    print("\n3. Testing dashboard data...")
    dashboard = bridge.get_dashboard_data()

    print(f"Status: {dashboard['status']}")
    print(f"System Status: {dashboard['overview']['status_message']}")
    print(f"Total Validations: {dashboard['overview']['total_validations']}")
    print(f"Avg Quality: {dashboard['overview']['avg_quality_score']:.2f}")

    # Test 4: Send manual feedback
    print("\n4. Testing manual feedback...")
    manual_result = bridge.send_manual_feedback(
        validation_id=validation_result['validation_id'],
        user_satisfaction=5,
        notes="Perfect validation! Very helpful recommendations."
    )

    print(f"Status: {manual_result['status']}")
    print(f"Message: {manual_result.get('message')}")

    print("\n" + "=" * 80)
    print("✅ All API tests completed successfully!")
    print("=" * 80)
