"""
Agent 8 Training Dashboard
Beautiful HTML visualization of training metrics
Stand: 12.11.2025
"""

from typing import Dict
from datetime import datetime
import logging

from agent_8_storyboard_bridge import Agent8StoryboardBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Agent8TrainingDashboard:
    """HTML dashboard for Agent 8 training metrics"""

    def __init__(self):
        self.bridge = Agent8StoryboardBridge()

    def render_html(self) -> str:
        """Render complete HTML dashboard"""
        try:
            data = self.bridge.get_dashboard_data()
            if data["status"] != "success":
                return self._error_html(data.get("error", "Unknown error"))

            html = self._html_header()
            html += self._overview_section(data["overview"])
            html += self._genre_section(data["by_genre"])
            html += self._recommendations_section(data["recommendations"])
            html += self._recent_section(data["recent_validations"])
            html += self._html_footer()

            return html

        except Exception as e:
            logger.error(f"❌ Render failed: {e}")
            return self._error_html(str(e))

    def _html_header(self) -> str:
        """HTML header with CSS"""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Agent 8 Training Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 32px; margin-bottom: 8px; }
        .header p { font-size: 16px; opacity: 0.9; }
        .content { padding: 32px; }
        .section { margin-bottom: 32px; }
        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: #333;
            margin-bottom: 16px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .metric-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            color: #667eea;
            margin: 8px 0;
        }
        .status-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: 600;
            margin-top: 8px;
        }
        .status-excellent { background: #d4edda; color: #155724; }
        .status-good { background: #d1ecf1; color: #0c5460; }
        .status-fair { background: #fff3cd; color: #856404; }
        .status-poor { background: #f8d7da; color: #721c24; }
        .genre-row {
            background: #f8f9fa;
            padding: 16px;
            margin: 8px 0;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            border-left: 4px solid #667eea;
        }
        .genre-name { font-weight: 600; color: #333; }
        .genre-stats { display: flex; gap: 24px; }
        .genre-stat { text-align: center; }
        .genre-stat-label { font-size: 11px; color: #666; text-transform: uppercase; }
        .genre-stat-value { font-size: 16px; font-weight: 700; color: #667eea; }
        .rec-card {
            background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 100%);
            padding: 16px;
            margin: 8px 0;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }
        .rec-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
        .rec-genre { font-weight: 600; }
        .rec-text { font-size: 14px; color: #555; line-height: 1.5; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #dee2e6;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
        }
        tr:hover { background: #f8f9fa; }
        .score-bar {
            width: 100%;
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 4px;
        }
        .score-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        .footer {
            text-align: center;
            padding: 16px;
            background: #f8f9fa;
            color: #999;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Agent 8 Training Dashboard</h1>
            <p>Video Generation Quality Assurance - Training Metrics</p>
        </div>
        <div class="content">
"""

    def _overview_section(self, overview: Dict) -> str:
        """Overview metrics section"""
        status_class = f"status-{overview['system_status']}"
        return f"""
        <div class="section">
            <h2 class="section-title">📊 System Overview</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Validations</div>
                    <div class="metric-value">{overview['total_validations']}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Avg Quality</div>
                    <div class="metric-value">{overview['avg_quality_score']:.2f}</div>
                    <div class="score-bar">
                        <div class="score-fill" style="width: {overview['avg_quality_score']*100}%"></div>
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Success Rate</div>
                    <div class="metric-value">{overview['success_rate']*100:.0f}%</div>
                    <div class="score-bar">
                        <div class="score-fill" style="width: {overview['success_rate']*100}%"></div>
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">System Status</div>
                    <div class="status-badge {status_class}">{overview['status_message']}</div>
                </div>
            </div>
        </div>
"""

    def _genre_section(self, by_genre: Dict) -> str:
        """Per-genre stats section"""
        html = '<div class="section"><h2 class="section-title">🎵 Genre Performance</h2>'
        for genre, stats in by_genre.items():
            html += f"""
        <div class="genre-row">
            <div class="genre-name">{genre.upper()}</div>
            <div class="genre-stats">
                <div class="genre-stat">
                    <div class="genre-stat-label">Count</div>
                    <div class="genre-stat-value">{stats['count']}</div>
                </div>
                <div class="genre-stat">
                    <div class="genre-stat-label">Avg Score</div>
                    <div class="genre-stat-value">{stats['avg_score']:.2f}</div>
                </div>
                <div class="genre-stat">
                    <div class="genre-stat-label">Ready</div>
                    <div class="genre-stat-value">{stats['ready_rate']*100:.0f}%</div>
                </div>
                <div class="genre-stat">
                    <div class="genre-stat-label">Success</div>
                    <div class="genre-stat-value">{stats['success_rate']*100:.0f}%</div>
                </div>
            </div>
        </div>
"""
        html += '</div>'
        return html

    def _recommendations_section(self, recs: Dict) -> str:
        """Recommendations section"""
        html = '<div class="section"><h2 class="section-title">💡 Recommendations</h2>'
        for genre, rec in recs.items():
            html += f"""
        <div class="rec-card">
            <div class="rec-header">
                <div class="rec-genre">{genre.upper()}</div>
                <div>{rec['status']}</div>
            </div>
            <div class="rec-text">{rec['recommendation']}</div>
        </div>
"""
        html += '</div>'
        return html

    def _recent_section(self, recent: list) -> str:
        """Recent validations table"""
        html = '''<div class="section">
            <h2 class="section-title">📋 Recent Validations</h2>
            <table>
                <tr>
                    <th>Time</th>
                    <th>Genre</th>
                    <th>Type</th>
                    <th>Quality</th>
                    <th>Ready</th>
                    <th>Generated</th>
                </tr>
'''
        for v in recent:
            ts = v['timestamp'][:19].replace('T', ' ')
            ready = "✓" if v['ready'] else "✗"
            gen = "✓" if v.get('generation_success') else "⏳" if v.get('generation_success') is None else "✗"
            html += f'''
                <tr>
                    <td>{ts}</td>
                    <td>{v['genre']}</td>
                    <td>{v['prompt_type']}</td>
                    <td>{v['quality_score']:.2f}</td>
                    <td>{ready}</td>
                    <td>{gen}</td>
                </tr>
'''
        html += '</table></div>'
        return html

    def _html_footer(self) -> str:
        """HTML footer"""
        return f'''
        </div>
        <div class="footer">
            Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
'''

    def _error_html(self, error: str) -> str:
        """Error page"""
        return f'''<!DOCTYPE html>
<html>
<head><title>Dashboard Error</title></head>
<body style="font-family: Arial; padding: 40px; background: #f8d7da;">
    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 32px; border-radius: 8px;">
        <h1 style="color: #721c24;">❌ Dashboard Error</h1>
        <p>Failed to render dashboard:</p>
        <pre>{error}</pre>
    </div>
</body>
</html>'''

    def save_html(self, path: str = "agent_8_dashboard.html"):
        """Save dashboard as HTML file"""
        try:
            html = self.render_html()
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info(f"✅ Dashboard saved to {path}")
            print(f"✅ Dashboard saved to {path}")
        except Exception as e:
            logger.error(f"❌ Save failed: {e}")
            raise


if __name__ == "__main__":
    print("=" * 80)
    print("AGENT 8 TRAINING DASHBOARD - TEST")
    print("=" * 80)

    dashboard = Agent8TrainingDashboard()

    print("\n1. Generating HTML dashboard...")
    dashboard.save_html("agent_8_dashboard.html")

    print("\n2. Dashboard stats:")
    html = dashboard.render_html()
    print(f"  HTML length: {len(html)} chars")
    print(f"  Sections: {html.count('section-title')}")

    print("\n" + "=" * 80)
    print("✅ Dashboard test completed!")
    print("Open agent_8_dashboard.html in browser")
    print("=" * 80)
