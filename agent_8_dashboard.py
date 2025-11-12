"""
AGENT 8 TRAINING DASHBOARD
Beautiful HTML dashboard for Storyboard App integration
Shows training progress, metrics, and recommendations

Stand: 12. November 2025
Version: 1.0
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

from agent_8_storyboard_bridge import Agent8StoryboardBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Agent8TrainingDashboard:
    """
    Training dashboard for Storyboard App

    Features:
    - Beautiful HTML rendering
    - Real-time metrics display
    - Genre-specific recommendations
    - Training progress visualization
    - Recent validation history
    """

    def __init__(
        self,
        config_path: str = "config_agent8.json",
        metrics_db_path: str = "data/agent_8_metrics.json"
    ):
        """
        Initialize dashboard

        Args:
            config_path: Path to Agent 8 config
            metrics_db_path: Path to metrics database
        """
        try:
            self.bridge = Agent8StoryboardBridge(config_path, metrics_db_path)
            logger.info("✅ Agent8TrainingDashboard initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize dashboard: {e}")
            raise

    def render_html_dashboard(self) -> str:
        """
        Render complete HTML dashboard

        Returns:
            str: Complete HTML document
        """
        try:
            logger.info("📊 Rendering HTML dashboard...")

            # Get dashboard data
            data = self.bridge.get_dashboard_data()

            if data["status"] != "success":
                return self._render_error_page(data.get("error", "Unknown error"))

            dashboard = data

            # Build HTML
            html = self._build_html_header()
            html += self._build_overview_section(dashboard["overview"])
            html += self._build_genre_stats_section(dashboard["by_genre"])
            html += self._build_prompt_type_stats_section(dashboard["by_prompt_type"])
            html += self._build_recommendations_section(dashboard["recommendations"])
            html += self._build_recent_validations_section(dashboard["recent_validations"])
            html += self._build_html_footer()

            logger.info("✅ Dashboard rendered successfully")

            return html

        except Exception as e:
            logger.error(f"❌ Failed to render dashboard: {e}")
            return self._render_error_page(str(e))

    def _build_html_header(self) -> str:
        """Build HTML header with CSS styles"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent 8 Training Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 36px;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 18px;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .section {
            margin-bottom: 40px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 700;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .metric-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        }

        .metric-label {
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }

        .metric-subtitle {
            font-size: 14px;
            color: #999;
        }

        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-top: 10px;
        }

        .status-excellent {
            background: #d4edda;
            color: #155724;
        }

        .status-good {
            background: #d1ecf1;
            color: #0c5460;
        }

        .status-fair {
            background: #fff3cd;
            color: #856404;
        }

        .status-poor {
            background: #f8d7da;
            color: #721c24;
        }

        .genre-row {
            background: #f8f9fa;
            padding: 20px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .genre-name {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            flex: 1;
        }

        .genre-stats {
            display: flex;
            gap: 30px;
            flex: 2;
        }

        .genre-stat {
            text-align: center;
        }

        .genre-stat-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }

        .genre-stat-value {
            font-size: 20px;
            font-weight: 700;
            color: #667eea;
        }

        .recommendation-card {
            background: linear-gradient(135deg, #e0f7fa 0%, #f3e5f5 100%);
            padding: 20px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .recommendation-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .recommendation-genre {
            font-size: 16px;
            font-weight: 600;
            color: #333;
        }

        .recommendation-status {
            font-size: 14px;
            padding: 4px 12px;
            border-radius: 12px;
            background: white;
        }

        .recommendation-text {
            font-size: 14px;
            color: #555;
            line-height: 1.6;
        }

        .validation-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        .validation-table th {
            background: #f8f9fa;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #dee2e6;
        }

        .validation-table td {
            padding: 15px;
            border-bottom: 1px solid #dee2e6;
            color: #555;
        }

        .validation-table tr:hover {
            background: #f8f9fa;
        }

        .score-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }

        .score-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s;
        }

        .timestamp {
            text-align: center;
            color: #999;
            font-size: 14px;
            padding: 20px;
            background: #f8f9fa;
        }

        .success-badge {
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }

        .success-yes {
            background: #d4edda;
            color: #155724;
        }

        .success-no {
            background: #f8d7da;
            color: #721c24;
        }

        .success-pending {
            background: #fff3cd;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Agent 8 Training Dashboard</h1>
            <p>Video Generation Quality Assurance System - Training Metrics</p>
        </div>
        <div class="content">
"""

    def _build_overview_section(self, overview: Dict) -> str:
        """Build overview metrics section"""
        status_class = f"status-{overview['system_status']}"

        return f"""
        <div class="section">
            <h2 class="section-title">📊 System Overview</h2>

            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Validations</div>
                    <div class="metric-value">{overview['total_validations']}</div>
                    <div class="metric-subtitle">All time</div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">Average Quality Score</div>
                    <div class="metric-value">{overview['avg_quality_score']:.2f}</div>
                    <div class="metric-subtitle">Out of 1.00</div>
                    <div class="score-bar">
                        <div class="score-fill" style="width: {overview['avg_quality_score']*100}%"></div>
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">Success Rate</div>
                    <div class="metric-value">{overview['success_rate']*100:.1f}%</div>
                    <div class="metric-subtitle">{overview['success_count']} successful generations</div>
                    <div class="score-bar">
                        <div class="score-fill" style="width: {overview['success_rate']*100}%"></div>
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">System Status</div>
                    <div class="status-badge {status_class}">
                        {overview['status_message']}
                    </div>
                    <div class="metric-subtitle">Last updated: {overview['last_updated'][:19]}</div>
                </div>
            </div>
        </div>
"""

    def _build_genre_stats_section(self, by_genre: Dict) -> str:
        """Build per-genre statistics section"""
        html = """
        <div class="section">
            <h2 class="section-title">🎵 Genre Performance</h2>
"""

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
                        <div class="genre-stat-label">Ready Rate</div>
                        <div class="genre-stat-value">{stats['ready_rate']*100:.0f}%</div>
                    </div>
                    <div class="genre-stat">
                        <div class="genre-stat-label">Success Rate</div>
                        <div class="genre-stat-value">{stats['success_rate']*100:.0f}%</div>
                    </div>
                </div>
            </div>
"""

        html += """
        </div>
"""
        return html

    def _build_prompt_type_stats_section(self, by_prompt_type: Dict) -> str:
        """Build per-prompt-type statistics section"""
        html = """
        <div class="section">
            <h2 class="section-title">🎬 Prompt Type Performance</h2>
            <div class="metric-grid">
"""

        for ptype, stats in by_prompt_type.items():
            html += f"""
            <div class="metric-card">
                <div class="metric-label">{ptype}</div>
                <div class="metric-value">{stats['count']}</div>
                <div class="metric-subtitle">
                    Avg Score: {stats['avg_score']:.2f} |
                    Success: {stats['success_rate']*100:.1f}%
                </div>
                <div class="score-bar">
                    <div class="score-fill" style="width: {stats['avg_score']*100}%"></div>
                </div>
            </div>
"""

        html += """
            </div>
        </div>
"""
        return html

    def _build_recommendations_section(self, recommendations: Dict) -> str:
        """Build recommendations section"""
        html = """
        <div class="section">
            <h2 class="section-title">💡 Recommendations</h2>
"""

        for genre, rec in recommendations.items():
            html += f"""
            <div class="recommendation-card">
                <div class="recommendation-header">
                    <div class="recommendation-genre">{rec['genre'].upper()}</div>
                    <div class="recommendation-status">{rec['status']}</div>
                </div>
                <div class="recommendation-text">
                    {rec['recommendation']}
                </div>
                <div class="metric-subtitle" style="margin-top: 10px;">
                    Score: {rec['avg_score']} | Success Rate: {rec['success_rate']} | Count: {rec['count']}
                </div>
            </div>
"""

        html += """
        </div>
"""
        return html

    def _build_recent_validations_section(self, validations: List[Dict]) -> str:
        """Build recent validations table"""
        html = """
        <div class="section">
            <h2 class="section-title">📋 Recent Validations</h2>
            <table class="validation-table">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Genre</th>
                        <th>Type</th>
                        <th>Quality Score</th>
                        <th>Ready</th>
                        <th>Generation</th>
                    </tr>
                </thead>
                <tbody>
"""

        for val in validations:
            timestamp = val['timestamp'][:19].replace('T', ' ')
            ready_badge = "✓ Yes" if val['ready'] else "✗ No"

            if val['generation_success'] is True:
                gen_badge = '<span class="success-badge success-yes">✓ Success</span>'
            elif val['generation_success'] is False:
                gen_badge = '<span class="success-badge success-no">✗ Failed</span>'
            else:
                gen_badge = '<span class="success-badge success-pending">⏳ Pending</span>'

            html += f"""
                <tr>
                    <td>{timestamp}</td>
                    <td>{val['genre']}</td>
                    <td>{val['prompt_type']}</td>
                    <td>
                        {val['quality_score']:.2f}
                        <div class="score-bar" style="margin-top: 5px;">
                            <div class="score-fill" style="width: {val['quality_score']*100}%"></div>
                        </div>
                    </td>
                    <td>{ready_badge}</td>
                    <td>{gen_badge}</td>
                </tr>
"""

        html += """
                </tbody>
            </table>
        </div>
"""
        return html

    def _build_html_footer(self) -> str:
        """Build HTML footer"""
        return f"""
        </div>
        <div class="timestamp">
            Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""

    def _render_error_page(self, error: str) -> str:
        """Render error page"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Error</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 40px;
            background: #f8d7da;
            color: #721c24;
        }}
        .error-container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #721c24; }}
    </style>
</head>
<body>
    <div class="error-container">
        <h1>❌ Dashboard Error</h1>
        <p>Failed to render dashboard:</p>
        <pre>{error}</pre>
    </div>
</body>
</html>
"""

    def save_dashboard_html(self, output_path: str = "agent_8_dashboard.html") -> None:
        """
        Save dashboard as HTML file

        Args:
            output_path: Path to save HTML file
        """
        try:
            html = self.render_html_dashboard()

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            logger.info(f"✅ Dashboard saved to {output_path}")
            print(f"✅ Dashboard saved to {output_path}")

        except Exception as e:
            logger.error(f"❌ Failed to save dashboard: {e}")
            raise


# ─────────────────────────────────────────────────────────────────────────────
# USAGE EXAMPLE
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 80)
    print("AGENT 8 TRAINING DASHBOARD - TEST")
    print("=" * 80)

    # Initialize dashboard
    dashboard = Agent8TrainingDashboard()

    # Render and save HTML
    print("\n1. Generating HTML dashboard...")
    dashboard.save_dashboard_html("agent_8_dashboard.html")

    # Also print to console
    print("\n2. Dashboard HTML Preview:")
    print("-" * 80)
    html = dashboard.render_html_dashboard()
    print(f"HTML Length: {len(html)} characters")
    print(f"Contains {html.count('metric-card')} metric cards")
    print(f"Contains {html.count('genre-row')} genre rows")

    print("\n" + "=" * 80)
    print("✅ Dashboard test completed successfully!")
    print("Open agent_8_dashboard.html in your browser to view")
    print("=" * 80)
