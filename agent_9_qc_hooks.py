import logging
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)

class Agent9QCHooks:
    def __init__(self, quality_controller, agent8_bridge=None, agent5_callback=None):
        self.qc = quality_controller
        self.agent8_bridge = agent8_bridge
        self.agent5_callback = agent5_callback
        self.hooks: Dict[str, List[Callable]] = {}

    def on_video_generated(self, video_path: str, metadata: Dict, genre: str):
        logger.info(f"🎬 QC: Video generated - {video_path}")

        # Run QC analysis
        report = self.qc.analyze_video(video_path, metadata, genre)

        # Send feedback to Agent 8
        if self.agent8_bridge:
            self.send_to_agent8(report)

        # Send feedback to Agent 5
        if self.agent5_callback:
            self.agent5_callback(report)

        # Trigger hooks
        self.trigger_hook("qc_complete", report)

        return report

    def send_to_agent8(self, report: Dict):
        logger.info(f"📊 Sending QC feedback to Agent 8: {report.video_id}")
        # Send feedback for training improvement
        self.agent8_bridge.send_generation_feedback(
            validation_id=report.video_id,
            generation_success=report.passed,
            generation_quality_score=report.metrics.overall_score
        )

    def register_hook(self, hook_name: str, callback: Callable):
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)
        logger.info(f"✅ Hook registered: {hook_name}")

    def trigger_hook(self, hook_name: str, data: Dict):
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in hook {hook_name}: {e}")
