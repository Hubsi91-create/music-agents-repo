import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class QCMetrics:
    video_quality_score: float  # 0.0-1.0
    audio_quality_score: float  # 0.0-1.0
    sync_score: float  # 0.0-1.0
    genre_compliance: float  # 0.0-1.0
    overall_score: float  # Weighted average
    pass_fail: bool
    issues: List[str]
    recommendations: List[str]

@dataclass
class QCReport:
    video_id: str
    timestamp: str
    metrics: QCMetrics
    passed: bool
    feedback_to_agent8: str
    feedback_to_agent5: str

class Agent9QualityController:
    def __init__(self, config_path: str = "config_agent9.json"):
        self.config = self.load_config(config_path)
        self.qc_rules = self.initialize_qc_rules()

    def load_config(self, path: str) -> Dict:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return self.get_default_config()

    def get_default_config(self) -> Dict:
        return {
            "quality_thresholds": {
                "video_quality_min": 0.75,
                "audio_quality_min": 0.80,
                "sync_min": 0.85,
                "genre_compliance_min": 0.80,
                "overall_pass_threshold": 0.80
            },
            "genres": {
                "reggaeton": {"motion_intensity": 0.7, "sync_tolerance": 0.1},
                "edm": {"motion_intensity": 0.9, "sync_tolerance": 0.05},
                "hiphop": {"motion_intensity": 0.6, "sync_tolerance": 0.08},
                "pop": {"motion_intensity": 0.5, "sync_tolerance": 0.12},
                "rb_soul": {"motion_intensity": 0.4, "sync_tolerance": 0.15}
            },
            "rules": {
                "frame_rate": "24fps or 30fps",
                "resolution": "1920x1080 minimum",
                "bit_rate": "5000-15000 kbps",
                "color_depth": "24-bit minimum"
            }
        }

    def initialize_qc_rules(self) -> Dict:
        return {
            "video_quality": [
                "Check frame rate (24fps, 30fps)",
                "Check resolution (min 1920x1080)",
                "Check bit rate (5000-15000 kbps)",
                "Check color grading consistency",
                "Check for artifacts/glitches",
                "Check lighting consistency"
            ],
            "audio_quality": [
                "Check audio levels (-18dB to -6dB)",
                "Check for clipping",
                "Check for background noise",
                "Check stereo/mono consistency",
                "Check audio codec (AAC preferred)"
            ],
            "sync": [
                "Check audio-visual sync",
                "Check beat alignment",
                "Check scene transitions sync",
                "Check motion sync with music"
            ],
            "genre_specific": {
                "reggaeton": ["Smooth transitions", "Warm color grading", "Groove alignment"],
                "edm": ["Fast cuts OK", "Neon colors", "Beat-perfect timing"],
                "hiphop": ["High contrast", "Slow-motion effects", "Flow sync"],
                "pop": ["Bright colors", "Clean cuts", "Rhythm alignment"],
                "rb_soul": ["Warm tones", "Smooth motion", "Intimate feel"]
            }
        }

    def analyze_video(self, video_path: str, metadata: Dict, genre: str) -> QCReport:
        logger.info(f"🎬 Starting QC analysis: {video_path}")

        # Analyze each dimension
        video_score = self.check_video_quality(video_path, metadata)
        audio_score = self.check_audio_quality(video_path, metadata)
        sync_score = self.check_sync(metadata)
        genre_score = self.check_genre_compliance(metadata, genre)

        # Calculate overall
        overall = (video_score * 0.3 + audio_score * 0.3 + sync_score * 0.2 + genre_score * 0.2)

        # Determine pass/fail
        threshold = self.config["quality_thresholds"]["overall_pass_threshold"]
        passed = overall >= threshold

        # Generate report
        issues = self.identify_issues(video_score, audio_score, sync_score, genre_score)
        recommendations = self.generate_recommendations(issues, genre)

        metrics = QCMetrics(
            video_quality_score=video_score,
            audio_quality_score=audio_score,
            sync_score=sync_score,
            genre_compliance=genre_score,
            overall_score=overall,
            pass_fail=passed,
            issues=issues,
            recommendations=recommendations
        )

        report = QCReport(
            video_id=metadata.get("id", "unknown"),
            timestamp=datetime.now().isoformat(),
            metrics=metrics,
            passed=passed,
            feedback_to_agent8=self.generate_agent8_feedback(metrics),
            feedback_to_agent5=self.generate_agent5_feedback(metrics)
        )

        logger.info(f"✅ QC Complete: {video_path} - {'PASS' if passed else 'FAIL'} ({overall:.2f})")
        return report

    def check_video_quality(self, video_path: str, metadata: Dict) -> float:
        score = 1.0
        issues = []

        # Check resolution
        res = metadata.get("resolution", "unknown")
        if res != "1920x1080":
            score -= 0.1
            issues.append(f"Resolution {res} (expected 1920x1080)")

        # Check frame rate
        fps = metadata.get("fps", 0)
        if fps not in [24, 30]:
            score -= 0.1
            issues.append(f"FPS {fps} (expected 24 or 30)")

        # Check bitrate
        bitrate = metadata.get("bitrate", 0)
        if bitrate < 5000 or bitrate > 15000:
            score -= 0.15
            issues.append(f"Bitrate {bitrate} (expected 5000-15000)")

        # Check for artifacts
        artifact_count = metadata.get("detected_artifacts", 0)
        if artifact_count > 5:
            score -= 0.2
            issues.append(f"{artifact_count} artifacts detected")

        return max(0.0, score)

    def check_audio_quality(self, video_path: str, metadata: Dict) -> float:
        score = 1.0

        # Check audio levels
        audio_level = metadata.get("audio_level_db", -12)
        if audio_level > -6 or audio_level < -18:
            score -= 0.15

        # Check for clipping
        if metadata.get("clipping_detected", False):
            score -= 0.25

        # Check background noise
        noise_level = metadata.get("noise_level_db", -60)
        if noise_level > -40:
            score -= 0.2

        return max(0.0, score)

    def check_sync(self, metadata: Dict) -> float:
        # Check audio-visual sync (from metadata)
        sync_offset = metadata.get("sync_offset_ms", 0)

        # Allow small offsets (<=100ms usually OK)
        if abs(sync_offset) > 100:
            return 0.6
        elif abs(sync_offset) > 50:
            return 0.8
        else:
            return 1.0

    def check_genre_compliance(self, metadata: Dict, genre: str) -> float:
        genre_rules = self.config["genres"].get(genre, {})
        score = 1.0

        # Check motion intensity
        motion = metadata.get("motion_intensity", 0)
        expected_motion = genre_rules.get("motion_intensity", 0.5)
        if abs(motion - expected_motion) > 0.2:
            score -= 0.2

        # Check color grading
        if not metadata.get("color_grading_applied", False):
            score -= 0.15

        return max(0.0, score)

    def identify_issues(self, video_score: float, audio_score: float, sync_score: float, genre_score: float) -> List[str]:
        issues = []

        if video_score < 0.75:
            issues.append("❌ Video quality below threshold")
        if audio_score < 0.80:
            issues.append("❌ Audio quality below threshold")
        if sync_score < 0.85:
            issues.append("❌ Sync issues detected")
        if genre_score < 0.80:
            issues.append("❌ Genre compliance issues")

        return issues

    def generate_recommendations(self, issues: List[str], genre: str) -> List[str]:
        recommendations = []

        if any("Video quality" in i for i in issues):
            recommendations.append("✓ Re-encode video with higher bitrate")
        if any("Audio quality" in i for i in issues):
            recommendations.append("✓ Re-mix audio with proper levels")
        if any("Sync" in i for i in issues):
            recommendations.append("✓ Adjust timing or re-render")

        return recommendations

    def generate_agent8_feedback(self, metrics: QCMetrics) -> str:
        if metrics.overall_score < 0.70:
            return "❌ REJECT: Prompt needs revision. Video quality too low."
        elif metrics.overall_score < 0.80:
            return "⚠️ WARNING: Prompt may need refinement. Consider stricter validation."
        else:
            return "✅ APPROVE: Prompt validation was effective. Video quality excellent."

    def generate_agent5_feedback(self, metrics: QCMetrics) -> str:
        feedback = f"Video QC Report:\n"
        feedback += f"Overall Score: {metrics.overall_score:.2f}\n"
        feedback += f"Video: {metrics.video_quality_score:.2f} | "
        feedback += f"Audio: {metrics.audio_quality_score:.2f} | "
        feedback += f"Sync: {metrics.sync_score:.2f}\n"

        if metrics.issues:
            feedback += f"Issues: {', '.join(metrics.issues)}\n"
        if metrics.recommendations:
            feedback += f"Recommendations: {', '.join(metrics.recommendations)}\n"

        return feedback

    def save_report(self, report: QCReport, output_path: str = "qc_report.json"):
        with open(output_path, 'w') as f:
            json.dump({
                "video_id": report.video_id,
                "timestamp": report.timestamp,
                "passed": report.passed,
                "metrics": asdict(report.metrics),
                "feedback_agent8": report.feedback_to_agent8,
                "feedback_agent5": report.feedback_to_agent5
            }, f, indent=2)
        logger.info(f"📊 QC Report saved: {output_path}")
