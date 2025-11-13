"""
Agent 8 Metrics Collection System
Tracks validation events and training data for continuous improvement
Stand: 12.11.2025
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Agent8MetricsCollector:
    """Collects and analyzes Agent 8 validation metrics"""

    def __init__(self, db_path: str = "data/agent_8_metrics.json"):
        self.db_path = db_path
        self._ensure_db()
        self.data = self._load()

    def _ensure_db(self):
        """Create database file if not exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({
                    "metadata": {"version": "1.0", "created": datetime.now().isoformat()},
                    "summary": {"total": 0, "avg_quality": 0.0, "success_rate": 0.0},
                    "records": [],
                    "by_genre": {},
                    "by_type": {}
                }, f, indent=2)

    def record_validation(
        self,
        prompt: str,
        prompt_type: str,
        genre: str,
        quality_score: float,
        issues: List[str],
        fixes: List[str],
        ready: bool,
        storyboard_id: Optional[str] = None
    ) -> str:
        """
        Record a validation event

        Returns:
            validation_id: Unique ID for this validation
        """
        val_id = f"val_{int(datetime.now().timestamp() * 1000)}"

        record = {
            "id": val_id,
            "timestamp": datetime.now().isoformat(),
            "storyboard_id": storyboard_id,
            "prompt_snippet": prompt[:150] + "..." if len(prompt) > 150 else prompt,
            "prompt_type": prompt_type,
            "genre": genre,
            "quality_score": quality_score,
            "ready": ready,
            "issues": issues[:5],
            "fixes": fixes[:5],
            "generation_success": None,
            "generation_quality": None,
            "user_rating": None,
            "user_notes": None
        }

        self.data["records"].append(record)
        self._update_stats()
        self._save()

        logger.info(f"✅ Recorded {val_id}: {genre} ({prompt_type}) - Score: {quality_score:.2f}")
        return val_id

    def add_generation_feedback(
        self,
        validation_id: str,
        success: bool,
        quality: float
    ) -> bool:
        """Add real-world generation feedback"""
        for rec in self.data["records"]:
            if rec["id"] == validation_id:
                rec["generation_success"] = success
                rec["generation_quality"] = quality
                rec["feedback_timestamp"] = datetime.now().isoformat()
                self._update_stats()
                self._save()
                logger.info(f"✅ Feedback added to {validation_id}")
                return True

        logger.warning(f"⚠️ Validation {validation_id} not found")
        return False

    def add_user_feedback(
        self,
        validation_id: str,
        rating: int,
        notes: str
    ) -> bool:
        """Add manual user feedback (1-5 stars)"""
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be 1-5")

        for rec in self.data["records"]:
            if rec["id"] == validation_id:
                rec["user_rating"] = rating
                rec["user_notes"] = notes
                self._save()
                logger.info(f"✅ User feedback: {rating} stars")
                return True

        return False

    def _update_stats(self):
        """Update summary statistics"""
        records = self.data["records"]
        if not records:
            return

        # Overall stats
        self.data["summary"]["total"] = len(records)
        self.data["summary"]["avg_quality"] = sum(r["quality_score"] for r in records) / len(records)

        # Success rate (only records with feedback)
        with_feedback = [r for r in records if r["generation_success"] is not None]
        if with_feedback:
            successes = sum(1 for r in with_feedback if r["generation_success"])
            self.data["summary"]["success_rate"] = successes / len(with_feedback)

        # Per-genre stats
        genres = {}
        for rec in records:
            g = rec["genre"]
            if g not in genres:
                genres[g] = {"scores": [], "ready": 0, "success": 0, "total_feedback": 0}

            genres[g]["scores"].append(rec["quality_score"])
            if rec["ready"]:
                genres[g]["ready"] += 1
            if rec["generation_success"] is not None:
                genres[g]["total_feedback"] += 1
                if rec["generation_success"]:
                    genres[g]["success"] += 1

        self.data["by_genre"] = {
            g: {
                "count": len(d["scores"]),
                "avg_score": sum(d["scores"]) / len(d["scores"]),
                "ready_rate": d["ready"] / len(d["scores"]),
                "success_rate": d["success"] / d["total_feedback"] if d["total_feedback"] > 0 else 0
            }
            for g, d in genres.items()
        }

        # Per-type stats
        types = {}
        for rec in records:
            t = rec["prompt_type"]
            if t not in types:
                types[t] = {"scores": [], "success": 0, "total_feedback": 0}

            types[t]["scores"].append(rec["quality_score"])
            if rec["generation_success"] is not None:
                types[t]["total_feedback"] += 1
                if rec["generation_success"]:
                    types[t]["success"] += 1

        self.data["by_type"] = {
            t: {
                "count": len(d["scores"]),
                "avg_score": sum(d["scores"]) / len(d["scores"]),
                "success_rate": d["success"] / d["total_feedback"] if d["total_feedback"] > 0 else 0
            }
            for t, d in types.items()
        }

    def get_summary(self) -> Dict:
        """Get current metrics summary"""
        self._update_stats()
        return {
            "summary": self.data["summary"],
            "by_genre": self.data["by_genre"],
            "by_type": self.data["by_type"],
            "timestamp": datetime.now().isoformat()
        }

    def get_recommendations(self) -> Dict:
        """Get genre-specific recommendations"""
        recs = {}
        for genre, stats in self.data["by_genre"].items():
            score = stats["avg_score"]

            if score > 0.85:
                status = "🟢 Excellent"
                rec = f"✅ {genre}: Performing excellently. Can relax some parameters."
            elif score > 0.75:
                status = "🟡 Good"
                rec = f"✓ {genre}: Good performance. Monitor consistency."
            elif score > 0.65:
                status = "🟠 Fair"
                rec = f"⚠️ {genre}: Fair. Consider adjusting auto-fix rules."
            else:
                status = "🔴 Needs Work"
                rec = f"⚠️ {genre}: Needs attention. Review validation rules."

            recs[genre] = {
                "status": status,
                "avg_score": f"{score:.2f}",
                "success_rate": f"{stats['success_rate']*100:.1f}%",
                "recommendation": rec
            }

        return recs

    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Get recent validation records"""
        return list(reversed(self.data["records"][-limit:]))

    def _save(self):
        """Save to disk"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def _load(self) -> Dict:
        """Load from disk"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"metadata": {}, "summary": {}, "records": [], "by_genre": {}, "by_type": {}}


if __name__ == "__main__":
    print("=" * 80)
    print("AGENT 8 METRICS COLLECTOR - TEST")
    print("=" * 80)

    # Test metrics collection
    collector = Agent8MetricsCollector()

    # Record validation
    print("\n1. Recording validation...")
    val_id = collector.record_validation(
        prompt="Woman walks to window in modern apartment...",
        prompt_type="veo_3.1",
        genre="reggaeton",
        quality_score=0.85,
        issues=["Dialog too long"],
        fixes=["Trimmed dialog"],
        ready=True,
        storyboard_id="scene_001"
    )
    print(f"✓ Validation ID: {val_id}")

    # Add feedback
    print("\n2. Adding generation feedback...")
    collector.add_generation_feedback(val_id, success=True, quality=0.88)

    # Get summary
    print("\n3. Metrics Summary:")
    summary = collector.get_summary()
    print(json.dumps(summary, indent=2))

    # Get recommendations
    print("\n4. Recommendations:")
    recs = collector.get_recommendations()
    for genre, rec in recs.items():
        print(f"\n{rec['status']} {genre}")
        print(f"  {rec['recommendation']}")

    print("\n" + "=" * 80)
    print("✅ Test completed!")
    print("=" * 80)
