class StoryboardDashboardWidget:
    def __init__(self, agent8_bridge):
        self.bridge = agent8_bridge

    def render_compact_widget(self) -> str:
        try:
            metrics = self.bridge.get_dashboard_data()["dashboard"]["overview"]
        except:
            return "<div>Agent 8 not available</div>"

        return f'''<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 8px;">
            <h3>📊 Agent 8</h3>
            <div>Validations: <strong>{metrics['total_validations']}</strong><br>
            Quality: <strong>{metrics['avg_quality']:.2f}</strong><br>
            Status: <strong>{metrics['status']}</strong></div>
        </div>'''

    def render_full_dashboard(self) -> str:
        try:
            metrics = self.bridge.get_dashboard_data()["dashboard"]
        except:
            return "<html><body><p>Agent 8 not available</p></body></html>"

        overview = metrics["overview"]
        genre_html = "".join([f'<div class="genre-row"><strong>{g}</strong><br>Score: {s["avg_score"]:.2f} | Ready: {s["ready_rate"]*100:.0f}%</div>'
                             for g, s in metrics.get("by_genre", {}).items()])

        return f'''<!DOCTYPE html><html><head><title>Agent 8 Dashboard</title>
        <style>body{{font-family: Arial; margin: 0; padding: 20px; background: #f5f5f5;}}
        .container{{max-width: 1200px; margin: 0 auto;}}
        .card{{background: white; border-radius: 8px; padding: 20px; margin: 15px 0;}}
        .metric{{display: inline-block; margin: 10px 20px 10px 0;}}
        .metric-value{{font-size: 24px; font-weight: bold; color: #667eea;}}
        .genre-row{{background: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 4px solid #667eea;}}
        </style></head><body><div class="container">
        <h1>📊 Agent 8 Training Dashboard</h1>
        <div class="card"><h2>Overall Metrics</h2>
        <div class="metric"><div class="metric-value">{overview['total_validations']}</div><div>Validations</div></div>
        <div class="metric"><div class="metric-value">{overview['avg_quality']:.2f}</div><div>Avg Quality</div></div>
        <div class="metric"><div class="metric-value">{overview['success_rate']*100:.1f}%</div><div>Success</div></div>
        </div><div class="card"><h2>Per-Genre Performance</h2>{genre_html}</div>
        </div></body></html>'''

    def save_dashboard_html(self, path: str = "agent_8_dashboard.html"):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.render_full_dashboard())
        return f"Dashboard saved to {path}"
