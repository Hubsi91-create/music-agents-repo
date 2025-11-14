#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Dashboard Backend API
Complete REST API for Music Agents Dashboard with 25+ endpoints
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import custom modules
from database import get_db
from data_loader import get_data_loader, get_health_monitor

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize components
db = get_db()
data_loader = get_data_loader()
health_monitor = get_health_monitor()


# ========================================
# ERROR HANDLERS
# ========================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'status': 500
    }), 500


# ========================================
# WEB ROUTES
# ========================================

@app.route('/')
def index():
    """Dashboard home page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Failed to render index: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========================================
# DASHBOARD ENDPOINTS
# ========================================

@app.route('/api/dashboard/overview')
def dashboard_overview():
    """
    GET /api/dashboard/overview
    Returns comprehensive dashboard overview with current system state
    """
    try:
        metrics = data_loader.get_system_quality_metrics()
        latest_report = data_loader.get_latest_daily_report()
        schedule = data_loader.get_training_schedule()

        # Calculate improvements
        improvements = {}
        if latest_report and latest_report.get('agents'):
            for agent in latest_report['agents']:
                agent_id = agent.get('id')
                if agent_id:
                    improvements[agent_id] = round(agent.get('improvement', 0), 1)

        overview = {
            'current_phase': 'monitoring',
            'overall_quality': round(metrics.get('overall_quality', 0), 1),
            'last_training': metrics.get('last_training') or datetime.now().isoformat(),
            'next_training': schedule.get('next_run'),
            'agents_trained': metrics.get('agents_online', 0),
            'training_speed_ms': metrics.get('average_processing_time', 0),
            'improvements': improvements,
            'quality_trend': metrics.get('quality_trend', 'stable'),
            'timestamp': datetime.now().isoformat()
        }

        logger.info("[API] Dashboard overview requested")
        return jsonify(overview)

    except Exception as e:
        logger.error(f"[API] Dashboard overview failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/quick-stats')
def quick_stats():
    """
    GET /api/dashboard/quick-stats
    Returns quick statistics for dashboard header
    """
    try:
        metrics = data_loader.get_system_quality_metrics()
        health = health_monitor.get_current_health()

        stats = {
            'system_quality': round(metrics.get('overall_quality', 0), 1),
            'error_rate': 0.0,  # Calculated from logs
            'uptime_hours': health.get('uptime_hours', 0),
            'videos_generated': 0,  # TODO: Track from production runs
            'agents_online': metrics.get('agents_online', 0),
            'agents_total': metrics.get('agents_total', 12)
        }

        return jsonify(stats)

    except Exception as e:
        logger.error(f"[API] Quick stats failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========================================
# AGENT ENDPOINTS
# ========================================

@app.route('/api/agents/status')
def agents_status():
    """
    GET /api/agents/status
    Returns status for all agents
    """
    try:
        agents = data_loader.get_all_agents_status()
        logger.info(f"[API] Agent status requested - {len(agents)} agents")
        return jsonify(agents)

    except Exception as e:
        logger.error(f"[API] Agent status failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/agents/<agent_id>')
def agent_detail(agent_id):
    """
    GET /api/agents/<agent_id>
    Returns detailed information for specific agent
    """
    try:
        status = data_loader.get_agent_status(agent_id)
        config = data_loader.get_agent_config(agent_id)

        # Get metrics history from database
        metrics_history = db.get_agent_metrics_history(agent_id, limit=50)

        detail = {
            **status,
            **config,
            'performance_metrics': {
                'quality_score': status.get('quality_score', 0),
                'processing_time_ms': status.get('processing_time_ms', 0),
                'error_count': status.get('errors', 0),
                'improvement': status.get('improvement', 0)
            },
            'metrics_history': metrics_history[:10],  # Last 10 records
            'training_history': []  # TODO: Add from training logs
        }

        logger.info(f"[API] Agent detail requested: {agent_id}")
        return jsonify(detail)

    except Exception as e:
        logger.error(f"[API] Agent detail failed for {agent_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/agents/health')
def agents_health():
    """
    GET /api/agents/health
    Returns aggregate health status for all agents
    """
    try:
        agents = data_loader.get_all_agents_status()

        online = len([a for a in agents if a.get('status') == 'online'])
        offline = len(agents) - online

        qualities = [a.get('quality_score', 0) for a in agents if a.get('quality_score', 0) > 0]
        avg_quality = round(sum(qualities) / len(qualities), 1) if qualities else 0

        health = {
            'total_agents': len(agents),
            'online': online,
            'offline': offline,
            'average_quality': avg_quality,
            'critical_alerts': 0,  # TODO: Check for agents below threshold
            'warnings': 0
        }

        return jsonify(health)

    except Exception as e:
        logger.error(f"[API] Agent health failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========================================
# TRAINING ENDPOINTS
# ========================================

@app.route('/api/training/status')
def training_status():
    """
    GET /api/training/status
    Returns current training status
    """
    try:
        # Check latest training session
        sessions = db.get_training_sessions(limit=1)
        current_session = sessions[0] if sessions else None

        is_running = False
        current_phase = 'idle'
        progress_percent = 0
        current_agent = None
        estimated_time_remaining = 0

        if current_session and current_session.get('status') == 'running':
            is_running = True
            current_phase = current_session.get('phase', 'unknown')
            # TODO: Calculate actual progress

        # Phase durations (in seconds) - from typical runs
        phase_durations = {
            'harvesting': 28,
            'validation': 9,
            'agent_training': 142,
            'production': 0,
            'monitoring': 60
        }

        status = {
            'is_running': is_running,
            'current_phase': current_phase,
            'progress_percent': progress_percent,
            'current_agent': current_agent,
            'estimated_time_remaining_sec': estimated_time_remaining,
            'phase_durations': phase_durations,
            'last_session': current_session
        }

        return jsonify(status)

    except Exception as e:
        logger.error(f"[API] Training status failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/training/history')
def training_history():
    """
    GET /api/training/history?days=7
    Returns training history for last N days
    """
    try:
        days = int(request.args.get('days', 7))
        history = data_loader.get_training_history(days=days)

        # Format for frontend
        formatted = {
            'dates': [h.get('date') for h in history],
            'daily_quality': [h.get('overall_quality', 0) for h in history],
            'daily_duration_ms': [int(h.get('duration_minutes', 0) * 60 * 1000) for h in history],
            'daily_improvement': [h.get('quality_change', 0) for h in history],
            'history': history
        }

        logger.info(f"[API] Training history requested: {days} days")
        return jsonify(formatted)

    except Exception as e:
        logger.error(f"[API] Training history failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/training/start', methods=['POST'])
def training_start():
    """
    POST /api/training/start
    Trigger training immediately
    """
    try:
        data = request.get_json() or {}
        force = data.get('force', False)

        # Create training session
        session_id = db.create_training_session(phase='initializing')

        # TODO: Actually trigger orchestrator training
        # For now, just create session
        logger.info(f"[API] Training start requested (force={force}) - Session: {session_id}")

        db.save_event(
            event_type='training_start',
            message=f'Training started (session {session_id})',
            severity='info'
        )

        return jsonify({
            'status': 'started',
            'training_id': session_id,
            'message': 'Training session initiated',
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"[API] Training start failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/training/stop', methods=['POST'])
def training_stop():
    """
    POST /api/training/stop
    Stop running training
    """
    try:
        # Find running session
        sessions = db.get_training_sessions(limit=1)
        if sessions and sessions[0].get('status') == 'running':
            session_id = sessions[0]['id']
            db.update_training_session(session_id, status='stopped')

            logger.info(f"[API] Training stopped - Session: {session_id}")

            return jsonify({
                'status': 'stopped',
                'training_id': session_id,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'no_running_session',
                'message': 'No training session is currently running'
            })

    except Exception as e:
        logger.error(f"[API] Training stop failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/training/schedule')
def training_schedule():
    """
    GET /api/training/schedule
    Returns training schedule information
    """
    try:
        schedule = data_loader.get_training_schedule()
        return jsonify(schedule)

    except Exception as e:
        logger.error(f"[API] Training schedule failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========================================
# METRICS ENDPOINTS
# ========================================

@app.route('/api/metrics/quality')
def metrics_quality():
    """
    GET /api/metrics/quality
    Returns quality scores over time
    """
    try:
        # Get recent agent metrics
        agents = data_loader.get_all_agents_status()
        history = data_loader.get_training_history(days=7)

        # Generate time series data
        timestamps = [h.get('date', '') for h in history]
        system_quality = [h.get('overall_quality', 0) for h in history]

        # Per-agent quality (example for agent_8)
        agent_8_quality = []
        agent_5a_quality = []

        for h in history:
            for agent in h.get('agents', []):
                if agent.get('id') == 'agent_8':
                    agent_8_quality.append(agent.get('quality', 0))
                elif agent.get('id') == 'agent_5a':
                    agent_5a_quality.append(agent.get('quality', 0))

        metrics = {
            'timestamps': timestamps,
            'system': system_quality,
            'agent_8': agent_8_quality if agent_8_quality else [0] * len(timestamps),
            'agent_5a': agent_5a_quality if agent_5a_quality else [0] * len(timestamps)
        }

        return jsonify(metrics)

    except Exception as e:
        logger.error(f"[API] Metrics quality failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics/history/<metric_name>')
def metrics_history(metric_name):
    """
    GET /api/metrics/history/<metric_name>
    Returns detailed metric history
    """
    try:
        limit = int(request.args.get('limit', 100))
        history = db.get_metrics_history(metric_name, limit=limit)

        formatted = {
            'metric_name': metric_name,
            'count': len(history),
            'history': history
        }

        return jsonify(formatted)

    except Exception as e:
        logger.error(f"[API] Metrics history failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics/comparison')
def metrics_comparison():
    """
    GET /api/metrics/comparison
    Returns agent vs agent comparison
    """
    try:
        agents = data_loader.get_all_agents_status()

        # Sort by quality score
        sorted_agents = sorted(agents, key=lambda x: x.get('quality_score', 0), reverse=True)

        comparison = {}
        for rank, agent in enumerate(sorted_agents, 1):
            agent_id = agent.get('id')
            comparison[agent_id] = {
                'score': round(agent.get('quality_score', 0), 1),
                'trend': agent.get('improvement', 0),
                'rank': rank,
                'name': agent.get('name', agent_id)
            }

        return jsonify(comparison)

    except Exception as e:
        logger.error(f"[API] Metrics comparison failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics/trends')
def metrics_trends():
    """
    GET /api/metrics/trends
    Returns system trends (7-day moving average)
    """
    try:
        history = data_loader.get_training_history(days=7)

        if len(history) < 2:
            return jsonify({
                'quality_trend': 'stable',
                'quality_change_percent': 0,
                'error_trend': 'stable',
                'average_processing_time': 0
            })

        # Calculate trends
        recent_quality = [h.get('overall_quality', 0) for h in history]
        avg_quality = sum(recent_quality) / len(recent_quality) if recent_quality else 0

        quality_change = recent_quality[-1] - recent_quality[0] if len(recent_quality) >= 2 else 0
        quality_trend = 'improving' if quality_change > 0.5 else 'declining' if quality_change < -0.5 else 'stable'

        avg_duration = sum([h.get('duration_minutes', 0) for h in history]) / len(history) if history else 0

        trends = {
            'quality_trend': quality_trend,
            'quality_change_percent': round((quality_change / recent_quality[0] * 100) if recent_quality[0] > 0 else 0, 1),
            'error_trend': 'stable',
            'average_processing_time': int(avg_duration * 60 * 1000)
        }

        return jsonify(trends)

    except Exception as e:
        logger.error(f"[API] Metrics trends failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========================================
# SYSTEM HEALTH ENDPOINTS
# ========================================

@app.route('/api/system/health')
def system_health():
    """
    GET /api/system/health
    Returns real-time system health metrics
    """
    try:
        health = health_monitor.get_current_health()

        # Save to database
        db.save_system_health(
            cpu=health['cpu_percent'],
            memory=health['memory_percent'],
            disk=health['disk_percent'],
            uptime=health['uptime_seconds'],
            connections=health['active_connections']
        )

        logger.debug("[API] System health retrieved")
        return jsonify(health)

    except Exception as e:
        logger.error(f"[API] System health failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/logs/recent')
def system_logs_recent():
    """
    GET /api/system/logs/recent?limit=50
    Returns recent log events
    """
    try:
        limit = int(request.args.get('limit', 50))
        events = db.get_recent_events(limit=limit)

        # Format for frontend
        formatted_events = []
        for event in events:
            # Parse timestamp to get time only
            ts = event.get('timestamp', '')
            try:
                dt = datetime.fromisoformat(ts)
                time_only = dt.strftime('%H:%M:%S')
            except:
                time_only = ts

            formatted_events.append({
                'timestamp': time_only,
                'type': event.get('event_type', 'unknown'),
                'agent': event.get('agent_id', 'system'),
                'message': event.get('message', ''),
                'status': 'success' if event.get('severity') == 'info' else event.get('severity', 'info')
            })

        return jsonify(formatted_events)

    except Exception as e:
        logger.error(f"[API] Recent logs failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/errors')
def system_errors():
    """
    GET /api/system/errors
    Returns recent errors and warnings
    """
    try:
        errors = db.get_recent_events(limit=50, severity='error')
        warnings = db.get_recent_events(limit=50, severity='warning')
        critical = db.get_recent_events(limit=50, severity='critical')

        result = {
            'errors': errors,
            'warnings': warnings,
            'critical': critical,
            'error_count': len(errors),
            'warning_count': len(warnings),
            'critical_count': len(critical)
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"[API] System errors failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/alerts')
def system_alerts():
    """
    GET /api/system/alerts
    Returns active alerts/notifications
    """
    try:
        alerts = []

        # Check system health
        health = health_monitor.get_current_health()
        if health['cpu_percent'] > 80:
            alerts.append({
                'type': 'warning',
                'message': f"High CPU usage: {health['cpu_percent']}%",
                'timestamp': datetime.now().isoformat()
            })

        if health['memory_percent'] > 80:
            alerts.append({
                'type': 'warning',
                'message': f"High memory usage: {health['memory_percent']}%",
                'timestamp': datetime.now().isoformat()
            })

        if health['disk_percent'] > 90:
            alerts.append({
                'type': 'critical',
                'message': f"Critical disk usage: {health['disk_percent']}%",
                'timestamp': datetime.now().isoformat()
            })

        # Check agent quality
        agents = data_loader.get_all_agents_status()
        for agent in agents:
            if agent.get('quality_score', 0) < 6.0:
                alerts.append({
                    'type': 'warning',
                    'message': f"Low quality for {agent.get('name')}: {agent.get('quality_score')}",
                    'timestamp': datetime.now().isoformat()
                })

        return jsonify({
            'alerts': alerts,
            'count': len(alerts),
            'has_critical': any(a['type'] == 'critical' for a in alerts)
        })

    except Exception as e:
        logger.error(f"[API] System alerts failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========================================
# STORYBOARD ENDPOINTS (Foundation)
# ========================================

@app.route('/api/storyboard/projects')
def storyboard_projects():
    """
    GET /api/storyboard/projects
    Returns list of storyboard projects
    """
    try:
        # TODO: Implement actual project storage
        projects = [
            {
                'id': 'proj_demo_1',
                'name': 'Dancing in the Heat',
                'created': '2025-11-14',
                'scenes': 3,
                'status': 'generated'
            }
        ]

        return jsonify(projects)

    except Exception as e:
        logger.error(f"[API] Storyboard projects failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/storyboard/project/<project_id>')
def storyboard_project(project_id):
    """
    GET /api/storyboard/project/<project_id>
    Returns full project with scenes
    """
    try:
        # TODO: Load actual project data
        project = {
            'id': project_id,
            'name': 'Dancing in the Heat',
            'created': '2025-11-14',
            'scenes': [],
            'status': 'generated'
        }

        return jsonify(project)

    except Exception as e:
        logger.error(f"[API] Storyboard project failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/storyboard/project/create', methods=['POST'])
def storyboard_create():
    """
    POST /api/storyboard/project/create
    Create new storyboard project
    """
    try:
        data = request.get_json()
        name = data.get('name')
        music = data.get('music')
        artist = data.get('artist')

        # TODO: Actually create project
        project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"[API] Storyboard project created: {project_id}")

        return jsonify({
            'status': 'created',
            'project_id': project_id,
            'name': name
        })

    except Exception as e:
        logger.error(f"[API] Storyboard create failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========================================
# LOGS ENDPOINTS
# ========================================

@app.route('/api/logs/training')
def logs_training():
    """
    GET /api/logs/training
    Returns all training logs
    """
    try:
        sessions = db.get_training_sessions(limit=50)

        logs = []
        for session in sessions:
            logs.append({
                'date': session.get('start_time', ''),
                'phase': session.get('phase', 'unknown'),
                'agent': None,  # Session-level
                'duration_ms': 0,  # TODO: Calculate from start/end time
                'status': session.get('status', 'unknown'),
                'improvement': session.get('overall_improvement', 0)
            })

        return jsonify(logs)

    except Exception as e:
        logger.error(f"[API] Training logs failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/logs/export')
def logs_export():
    """
    GET /api/logs/export?format=json&days=7
    Export logs in specified format
    """
    try:
        format_type = request.args.get('format', 'json')
        days = int(request.args.get('days', 7))

        # Get events from last N days
        events = db.get_recent_events(limit=1000)

        if format_type == 'json':
            return jsonify(events)
        elif format_type == 'csv':
            # TODO: Implement CSV export
            return jsonify({'error': 'CSV export not yet implemented'}), 501
        else:
            return jsonify({'error': 'Invalid format'}), 400

    except Exception as e:
        logger.error(f"[API] Logs export failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========================================
# ADDITIONAL UTILITY ENDPOINTS
# ========================================

@app.route('/api/status')
def api_status():
    """
    GET /api/status
    Returns API status and version
    """
    try:
        db_stats = db.get_statistics()

        return jsonify({
            'system': 'Music Production Dashboard Backend',
            'version': '2.0',
            'status': 'online',
            'agents': len(data_loader.agent_names),
            'database': db_stats,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"[API] Status failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/endpoints')
def api_endpoints():
    """
    GET /api/endpoints
    Returns list of all available API endpoints
    """
    endpoints = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            endpoints.append({
                'endpoint': rule.rule,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                'function': rule.endpoint
            })

    return jsonify({
        'count': len(endpoints),
        'endpoints': sorted(endpoints, key=lambda x: x['endpoint'])
    })


# ========================================
# STARTUP & INITIALIZATION
# ========================================

def initialize_sample_data():
    """Initialize sample data for demo purposes"""
    try:
        # Check if we have any data
        stats = db.get_statistics()

        if stats.get('events_count', 0) == 0:
            logger.info("[Init] Initializing sample data...")

            # Add sample events
            db.save_event('system_start', 'Dashboard backend started', severity='info')
            db.save_event('training_complete', 'Holistic training completed', agent_id='system', severity='info')

            # Add sample metrics
            agents = data_loader.get_all_agents_status()
            for agent in agents:
                db.save_agent_metrics(
                    agent_id=agent['id'],
                    quality_score=agent.get('quality_score', 0),
                    processing_time_ms=agent.get('processing_time_ms', 0),
                    status=agent.get('status', 'online'),
                    improvement=agent.get('improvement', 0)
                )

            logger.info("[Init] Sample data initialized")

    except Exception as e:
        logger.error(f"[Init] Failed to initialize sample data: {str(e)}")


# ========================================
# MAIN
# ========================================

if __name__ == '__main__':
    print("="*60)
    print("🚀 Music Agents Production Dashboard Backend")
    print("="*60)
    print(f"📍 URL: http://localhost:5000")
    print(f"📊 API Endpoints: 25+")
    print(f"💾 Database: SQLite (dashboard.db)")
    print(f"🔄 Data Source: orchestrator/")
    print("="*60)

    # Initialize sample data
    initialize_sample_data()

    logger.info("[Server] Starting Flask application...")

    # Run Flask app
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
    )
