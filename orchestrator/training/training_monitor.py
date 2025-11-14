"""
Training Monitor - Tracking & Reporting System

Tracks training metrics, generates reports, and monitors system health.
Provides comprehensive analytics and visualization of training progress.

Author: Music Video Production System
Version: 1.0.0
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict

logging.basicConfig(level=logging.INFO)


class TrainingMonitor:
    """
    Training Monitor for holistic training pipeline.

    Tracks:
    - Agent-specific metrics
    - System-wide performance
    - Training trends over time
    - Quality improvements
    """

    def __init__(self, metrics_file: str = None):
        """
        Initialize Training Monitor.

        Args:
            metrics_file: Path to metrics database file
        """
        self.logger = logging.getLogger("TrainingMonitor")

        # Metrics storage
        if metrics_file is None:
            metrics_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
            os.makedirs(metrics_dir, exist_ok=True)
            metrics_file = os.path.join(metrics_dir, 'training_metrics.json')

        self.metrics_file = metrics_file
        self.metrics = self._load_metrics()

        # Current session metrics
        self.session_metrics = defaultdict(list)

        self.logger.info(f"Training Monitor initialized (metrics: {metrics_file})")

    def _load_metrics(self) -> Dict[str, List[Any]]:
        """Load historical metrics from file."""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            else:
                return self._initialize_metrics()
        except Exception as e:
            self.logger.error(f"Error loading metrics: {str(e)}")
            return self._initialize_metrics()

    def _initialize_metrics(self) -> Dict[str, List[Any]]:
        """Initialize empty metrics structure."""
        return {
            'agent_1_trend_accuracy': [],
            'agent_2_audio_quality': [],
            'agent_3_concept_creativity': [],
            'agent_4_screenplay_quality': [],
            'agent_5a_veo_output_quality': [],
            'agent_5b_runway_output_quality': [],
            'agent_6_match_accuracy': [],
            'agent_7_metadata_quality': [],
            'agent_8_prompt_quality': [],
            'agent_9_sound_quality': [],
            'agent_10_distribution_reach': [],
            'agent_11_training_effectiveness': [],
            'system_overall_quality': [],
            'training_speed_ms': [],
            'success_rate': [],
            'training_history': []
        }

    def _save_metrics(self):
        """Save metrics to file."""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
            self.logger.debug("Metrics saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving metrics: {str(e)}")

    # ============================================================
    # METRIC LOGGING
    # ============================================================

    def log_agent_metrics(self, agent_name: str, metrics_dict: Dict[str, Any]):
        """
        Log metrics for a specific agent.

        Args:
            agent_name: Name of the agent (e.g., 'agent_1')
            metrics_dict: Dictionary with metrics:
                {
                    'success': bool,
                    'time_ms': int,
                    'improvement': float,
                    'data_count': int,
                    'error': str (optional)
                }
        """
        try:
            timestamp = datetime.now().isoformat()

            # Create metric entry
            metric_entry = {
                'timestamp': timestamp,
                'agent': agent_name,
                **metrics_dict
            }

            # Log to session metrics
            self.session_metrics[agent_name].append(metric_entry)

            # Get quality score (mock for now - would be real in production)
            quality_score = self._calculate_quality_score(agent_name, metrics_dict)

            # Log to historical metrics
            metric_key = f"{agent_name}_quality" if agent_name != 'system' else 'system_overall_quality'

            if metric_key not in self.metrics:
                self.metrics[metric_key] = []

            self.metrics[metric_key].append({
                'timestamp': timestamp,
                'score': quality_score,
                'improvement': metrics_dict.get('improvement', 0),
                'time_ms': metrics_dict.get('time_ms', 0)
            })

            # Log training speed
            if metrics_dict.get('time_ms'):
                self.metrics['training_speed_ms'].append({
                    'timestamp': timestamp,
                    'agent': agent_name,
                    'time_ms': metrics_dict['time_ms']
                })

            # Log success rate
            success = metrics_dict.get('success', False)
            self.metrics['success_rate'].append({
                'timestamp': timestamp,
                'agent': agent_name,
                'success': success
            })

            self.logger.info(f"Logged metrics for {agent_name}: quality={quality_score:.2f}")

        except Exception as e:
            self.logger.error(f"Error logging metrics for {agent_name}: {str(e)}")

    def log_training_event(self, event_type: str, data: Dict[str, Any]):
        """
        Log a training event.

        Args:
            event_type: Type of event (e.g., 'holistic_training_complete')
            data: Event data
        """
        try:
            event_entry = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'data': data
            }

            if 'training_history' not in self.metrics:
                self.metrics['training_history'] = []

            self.metrics['training_history'].append(event_entry)

            # Save after major events
            self._save_metrics()

            self.logger.info(f"Logged training event: {event_type}")

        except Exception as e:
            self.logger.error(f"Error logging training event: {str(e)}")

    # ============================================================
    # IMPROVEMENT CALCULATION
    # ============================================================

    def calculate_improvement(self, agent_name: str, iterations: int = 7) -> Tuple[str, float]:
        """
        Calculate improvement trend over last N training runs.

        Args:
            agent_name: Name of agent
            iterations: Number of previous runs to analyze

        Returns:
            Tuple of (trend, percentage)
            - trend: 'up', 'down', or 'stable'
            - percentage: improvement percentage
        """
        try:
            metric_key = f"{agent_name}_quality"

            if metric_key not in self.metrics or len(self.metrics[metric_key]) < 2:
                return ('stable', 0.0)

            # Get last N scores
            recent_scores = self.metrics[metric_key][-iterations:]
            scores = [entry['score'] for entry in recent_scores]

            if len(scores) < 2:
                return ('stable', 0.0)

            # Calculate trend
            first_half_avg = sum(scores[:len(scores)//2]) / (len(scores)//2)
            second_half_avg = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)

            percentage_change = ((second_half_avg - first_half_avg) / first_half_avg) * 100

            if percentage_change > 1.0:
                trend = 'up'
            elif percentage_change < -1.0:
                trend = 'down'
            else:
                trend = 'stable'

            return (trend, percentage_change)

        except Exception as e:
            self.logger.error(f"Error calculating improvement for {agent_name}: {str(e)}")
            return ('stable', 0.0)

    # ============================================================
    # REPORT GENERATION
    # ============================================================

    def generate_daily_report(self) -> str:
        """
        Generate comprehensive daily training report.

        Returns:
            Formatted report string
        """
        try:
            report_date = datetime.now().strftime("%Y-%m-%d")

            # Calculate overall metrics
            overall_quality = self._calculate_overall_quality()
            system_trend, system_improvement = self.calculate_improvement('system', iterations=7)

            # Build report
            report = []
            report.append("╔" + "="*78 + "╗")
            report.append(f"║  DAILY TRAINING REPORT [{report_date}]".ljust(79) + "║")

            # Get latest training duration
            latest_training = self._get_latest_training()
            if latest_training:
                duration = latest_training.get('total_time_minutes', 0)
                report.append(f"║  Training Duration: {duration:.2f} minutes".ljust(79) + "║")

            report.append(f"║  Overall System Quality: {overall_quality:.1f}/10 ({system_improvement:+.1f}%)".ljust(79) + "║")
            report.append("╠" + "="*78 + "╣")

            # Agent-specific reports
            agents = [
                ('agent_1', 'Trend Detective'),
                ('agent_2', 'Audio Curator'),
                ('agent_3', 'Video Concept'),
                ('agent_4', 'Screenplay Generator'),
                ('agent_5a', 'Veo Generator'),
                ('agent_5b', 'Runway Generator'),
                ('agent_6', 'Influencer Matcher'),
                ('agent_7', 'Distribution Metadata'),
                ('agent_8', 'Prompt Refiner'),
                ('agent_9', 'Sound Designer'),
                ('agent_10', 'Master Distributor'),
                ('agent_11', 'Meta Trainer'),
            ]

            for agent_name, display_name in agents:
                agent_report = self._generate_agent_section(agent_name, display_name)
                report.extend(agent_report)

            # Recommendations
            report.append("╠" + "="*78 + "╣")
            report.append("║ RECOMMENDATIONS FOR NEXT RUN:".ljust(79) + "║")

            recommendations = self._generate_recommendations()
            for rec in recommendations:
                report.append(f"║ - {rec}".ljust(79) + "║")

            report.append(f"║ - Current trajectory: {system_trend.upper()} {self._get_trend_arrow(system_trend)}".ljust(79) + "║")
            report.append("╚" + "="*78 + "╝")

            report_text = "\n".join(report)

            # Save report to file
            self._save_report(report_text, report_date)

            return report_text

        except Exception as e:
            self.logger.error(f"Error generating daily report: {str(e)}")
            return f"Error generating report: {str(e)}"

    def _generate_agent_section(self, agent_name: str, display_name: str) -> List[str]:
        """Generate report section for a specific agent."""
        section = []

        try:
            metric_key = f"{agent_name}_quality"

            if metric_key in self.metrics and self.metrics[metric_key]:
                latest = self.metrics[metric_key][-1]
                quality = latest.get('score', 0)
                improvement = latest.get('improvement', 0)
                time_ms = latest.get('time_ms', 0)

                # Get previous score for comparison
                prev_quality = 0
                if len(self.metrics[metric_key]) > 1:
                    prev_quality = self.metrics[metric_key][-2].get('score', 0)

                quality_change = quality - prev_quality

                status = "✅ Improved" if quality_change >= 0 else "⚠️  Declined"

                section.append(f"║ {display_name} ({agent_name})".ljust(79) + "║")
                section.append(f"║   Quality: {quality:.1f}/10 ({quality_change:+.1f} vs yesterday)".ljust(79) + "║")
                section.append(f"║   Processing: {time_ms/1000:.2f}s".ljust(79) + "║")
                section.append(f"║   Status: {status}".ljust(79) + "║")
            else:
                section.append(f"║ {display_name} ({agent_name})".ljust(79) + "║")
                section.append(f"║   Status: No data available".ljust(79) + "║")

            section.append("╠" + "="*78 + "╣")

        except Exception as e:
            self.logger.error(f"Error generating section for {agent_name}: {str(e)}")
            section.append(f"║ {display_name} ({agent_name}) - Error".ljust(79) + "║")
            section.append("╠" + "="*78 + "╣")

        return section

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on current metrics."""
        recommendations = []

        try:
            # Find lowest performing agent
            lowest_agent = self._find_lowest_performing_agent()
            if lowest_agent:
                recommendations.append(f"Focus on {lowest_agent} (lowest score)")

            # Check for agents needing more data
            if len(self.session_metrics) > 0:
                for agent_name, metrics_list in self.session_metrics.items():
                    if metrics_list and metrics_list[-1].get('data_count', 0) < 20:
                        recommendations.append(f"Increase data for {agent_name}")

            # General recommendation
            if not recommendations:
                recommendations.append("All agents performing well - continue current strategy")

        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            recommendations.append("Unable to generate recommendations")

        return recommendations[:3]  # Max 3 recommendations

    # ============================================================
    # SYSTEM HEALTH
    # ============================================================

    def get_system_health(self) -> Dict[str, Any]:
        """
        Get overall system health status.

        Returns:
            Dict with system health metrics
        """
        try:
            overall_quality = self._calculate_overall_quality()
            trend, improvement = self.calculate_improvement('system', iterations=7)

            # Count agents needing attention (quality < 7.0)
            agents_needing_attention = []
            for agent_name in ['agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5a',
                             'agent_5b', 'agent_6', 'agent_7', 'agent_8', 'agent_9',
                             'agent_10', 'agent_11']:
                metric_key = f"{agent_name}_quality"
                if metric_key in self.metrics and self.metrics[metric_key]:
                    latest_score = self.metrics[metric_key][-1].get('score', 0)
                    if latest_score < 7.0:
                        agents_needing_attention.append(agent_name)

            # Calculate next training time (default: tomorrow at 3 AM)
            next_training = datetime.now() + timedelta(days=1)
            next_training = next_training.replace(hour=3, minute=0, second=0, microsecond=0)

            return {
                'overall_quality': round(overall_quality, 1),
                'trend': trend,
                'improvement_percent': round(improvement, 1),
                'agents_online': 11,  # Total agents
                'agents_needing_attention': agents_needing_attention,
                'next_training': next_training.isoformat(),
                'estimated_video_quality': round(min(10.0, overall_quality + 1.0), 1)
            }

        except Exception as e:
            self.logger.error(f"Error getting system health: {str(e)}")
            return {
                'overall_quality': 0,
                'trend': 'unknown',
                'error': str(e)
            }

    # ============================================================
    # EXPORT METRICS
    # ============================================================

    def export_metrics(self, format: str = 'json', output_file: str = None) -> str:
        """
        Export metrics for analytics.

        Args:
            format: 'json' or 'csv'
            output_file: Output file path

        Returns:
            Path to exported file
        """
        try:
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = os.path.join(os.path.dirname(__file__), '..', 'analytics')
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, f"metrics_export_{timestamp}.{format}")

            if format == 'json':
                with open(output_file, 'w') as f:
                    json.dump(self.metrics, f, indent=2)
            elif format == 'csv':
                # CSV export would be implemented here
                self.logger.warning("CSV export not yet implemented")
                return None
            else:
                raise ValueError(f"Unsupported format: {format}")

            self.logger.info(f"Metrics exported to {output_file}")
            return output_file

        except Exception as e:
            self.logger.error(f"Error exporting metrics: {str(e)}")
            return None

    # ============================================================
    # HELPER METHODS
    # ============================================================

    def _calculate_quality_score(self, agent_name: str, metrics_dict: Dict[str, Any]) -> float:
        """Calculate quality score for agent based on metrics."""
        # Mock implementation - in production would use actual quality metrics
        import random
        base_score = 7.0
        improvement = metrics_dict.get('improvement', 0)
        success = metrics_dict.get('success', False)

        score = base_score + improvement / 10.0
        if not success:
            score -= 1.0

        return max(0.0, min(10.0, score))

    def _calculate_overall_quality(self) -> float:
        """Calculate overall system quality."""
        try:
            if 'system_overall_quality' in self.metrics and self.metrics['system_overall_quality']:
                return self.metrics['system_overall_quality'][-1].get('score', 7.5)
            else:
                # Calculate from agent averages
                total_score = 0
                count = 0

                for agent_num in range(1, 12):
                    key = f"agent_{agent_num}_quality" if agent_num != 5 else "agent_5a_quality"
                    if key in self.metrics and self.metrics[key]:
                        total_score += self.metrics[key][-1].get('score', 0)
                        count += 1

                return (total_score / count) if count > 0 else 7.5
        except:
            return 7.5

    def _find_lowest_performing_agent(self) -> Optional[str]:
        """Find agent with lowest quality score."""
        try:
            lowest_score = 10.0
            lowest_agent = None

            for agent_name in ['agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5a',
                             'agent_5b', 'agent_6', 'agent_7', 'agent_8', 'agent_9',
                             'agent_10', 'agent_11']:
                metric_key = f"{agent_name}_quality"
                if metric_key in self.metrics and self.metrics[metric_key]:
                    score = self.metrics[metric_key][-1].get('score', 10.0)
                    if score < lowest_score:
                        lowest_score = score
                        lowest_agent = agent_name

            return lowest_agent
        except:
            return None

    def _get_latest_training(self) -> Optional[Dict[str, Any]]:
        """Get latest training event data."""
        try:
            if 'training_history' in self.metrics and self.metrics['training_history']:
                return self.metrics['training_history'][-1].get('data', {})
        except:
            pass
        return None

    def _get_trend_arrow(self, trend: str) -> str:
        """Get arrow symbol for trend."""
        if trend == 'up':
            return '↑'
        elif trend == 'down':
            return '↓'
        else:
            return '→'

    def _save_report(self, report_text: str, report_date: str):
        """Save report to file."""
        try:
            reports_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
            os.makedirs(reports_dir, exist_ok=True)

            report_file = os.path.join(reports_dir, f"daily_report_{report_date}.txt")

            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_text)

            self.logger.info(f"Report saved to {report_file}")

        except Exception as e:
            self.logger.error(f"Error saving report: {str(e)}")


# ============================================================
# STANDALONE EXECUTION
# ============================================================

if __name__ == '__main__':
    print("Training Monitor - Standalone execution")
    print("\nGenerating sample report...\n")

    monitor = TrainingMonitor()

    # Log some sample metrics
    for i in range(5):
        monitor.log_agent_metrics('agent_1', {
            'success': True,
            'time_ms': 1200 + i*100,
            'improvement': 0.5 + i*0.3,
            'data_count': 50
        })

    # Generate report
    report = monitor.generate_daily_report()
    print(report)
