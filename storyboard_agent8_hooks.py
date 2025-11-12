import logging
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)

class StoryboardAgent8Hooks:
    def __init__(self, agent8_bridge):
        self.bridge = agent8_bridge
        self.hooks: Dict[str, List[Callable]] = {}

    def on_prompt_created(self, scene_id: str, prompt: str, prompt_type: str, genre: str):
        logger.info(f"📝 New prompt created: {scene_id}")
        validation = self.bridge.validate_prompt_from_storyboard(
            prompt=prompt, prompt_type=prompt_type, genre=genre, storyboard_scene_id=scene_id
        )
        self.trigger_hook("prompt_validated", validation)

    def on_video_generation_completed(self, validation_id: str, success: bool, quality_score: float, error_message: str = None):
        logger.info(f"✅ Video generation completed: {validation_id}")
        feedback = self.bridge.send_generation_feedback(
            validation_id=validation_id, generation_success=success,
            generation_quality_score=quality_score, error_message=error_message
        )
        self.trigger_hook("generation_completed", feedback)

    def on_user_feedback(self, validation_id: str, satisfaction: int, notes: str):
        logger.info(f"💬 User feedback: {validation_id} ({satisfaction} stars)")
        self.bridge.send_manual_feedback(validation_id=validation_id, user_satisfaction=satisfaction, notes=notes)
        self.trigger_hook("user_feedback", {"validation_id": validation_id, "satisfaction": satisfaction})

    def register_hook(self, hook_name: str, callback: Callable):
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)

    def trigger_hook(self, hook_name: str, data: Dict):
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in hook {hook_name}: {e}")
