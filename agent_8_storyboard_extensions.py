from typing import Dict, Callable
import logging

logger = logging.getLogger(__name__)

class StoryboardAgent8Extensions:
    def __init__(self, storyboard_app):
        self.app = storyboard_app
        self.agent8_bridge = None

    def register_all_extensions(self):
        self.register_validate_button()
        self.register_metrics_panel()
        self.register_dashboard_tab()
        logger.info("✅ All Agent 8 UI Extensions registered")

    def register_validate_button(self):
        def on_validate_clicked(scene_id: str, prompt: str, prompt_type: str, genre: str):
            result = self.agent8_bridge.validate_prompt_from_storyboard(
                prompt=prompt, prompt_type=prompt_type, genre=genre, storyboard_scene_id=scene_id
            )
            self.show_validation_feedback(result)
            self.refresh_metrics_panel()

        if hasattr(self.app, 'register_button'):
            self.app.register_button(name="validate_prompt", label="🔍 Validate with Agent 8",
                                   callback=on_validate_clicked, position="prompt_editor_toolbar")
        logger.info("✅ Validate Button registered")

    def show_validation_feedback(self, result: Dict):
        validation = result["validation"]
        score = validation["quality_score"]
        status = "🟢 Excellent" if score > 0.85 else "🟡 Good" if score > 0.75 else "🔴 Needs Work"
        feedback = f"{status}\nQuality: {score:.2f}/1.0\nReady: {'✅ YES' if result['ready_for_generation'] else '❌ NO'}"
        if hasattr(self.app, 'show_panel'):
            self.app.show_panel(title="Agent 8 Validation", content=feedback, panel_type="feedback")

    def register_metrics_panel(self):
        def get_metrics():
            if not self.agent8_bridge:
                return "Agent 8 not ready"
            metrics = self.agent8_bridge.get_dashboard_data()["dashboard"]["overview"]
            return f"📊 AGENT 8\nTotal: {metrics['total_validations']}\nQuality: {metrics['avg_quality']:.2f}\nStatus: {metrics['status']}"

        if hasattr(self.app, 'register_sidebar_panel'):
            self.app.register_sidebar_panel(name="agent8_metrics", title="Agent 8 Metrics",
                                           content_func=get_metrics, position="right_sidebar")

    def register_dashboard_tab(self):
        def show_dashboard():
            if self.agent8_bridge:
                dashboard = self.agent8_bridge.get_dashboard_data()
                if hasattr(self.app, 'show_modal'):
                    self.app.show_modal(title="Agent 8 Dashboard", content=str(dashboard), modal_type="full_screen")

        if hasattr(self.app, 'register_main_tab'):
            self.app.register_main_tab(name="agent8_dashboard", label="📊 Agent 8",
                                      callback=show_dashboard, icon="📊")

    def refresh_metrics_panel(self):
        if hasattr(self.app, 'refresh_sidebar_panel'):
            self.app.refresh_sidebar_panel("agent8_metrics")
