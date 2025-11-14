# -*- coding: utf-8 -*-
"""
Orchestrator API - HTTP Server auf Port 8000
Stellt REST API Endpoints für Orchestrator-Funktionalität bereit
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Add orchestrator path
sys.path.insert(0, str(Path(__file__).parent))

# Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Mark orchestrator as available (standalone API mode)
ORCHESTRATOR_AVAILABLE = True
orchestrator = None

logger.info("Orchestrator API initialized in standalone mode")


# ========== HEALTH & STATUS ENDPOINTS ==========

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'orchestrator',
        'port': 8000,
        'timestamp': datetime.now().isoformat(),
        'orchestrator_available': ORCHESTRATOR_AVAILABLE
    }), 200


@app.route('/status', methods=['GET'])
def status():
    """Orchestrator status endpoint"""
    try:
        return jsonify({
            'orchestrator_running': True,
            'orchestrator_available': ORCHESTRATOR_AVAILABLE,
            'agents_available': 7,
            'training_active': False,
            'timestamp': datetime.now().isoformat(),
            'system_ready': True
        }), 200
    except Exception as e:
        logger.error(f"Error in /status: {e}")
        return jsonify({
            'error': str(e),
            'orchestrator_running': False
        }), 500


# ========== AGENT ENDPOINTS ==========

@app.route('/agents', methods=['GET'])
@app.route('/api/agents', methods=['GET'])
@app.route('/agents/status', methods=['GET'])
@app.route('/api/agents/status', methods=['GET'])
def agents():
    """List all agents"""
    agents_list = [
        {'id': 1, 'name': 'Trend Detective Agent', 'status': 'ONLINE', 'type': 'analysis'},
        {'id': 2, 'name': 'Audio Quality Curator Agent', 'status': 'ONLINE', 'type': 'quality'},
        {'id': 3, 'name': 'Video Concept Agent', 'status': 'ONLINE', 'type': 'creative'},
        {'id': 4, 'name': 'Screenplay Generator Agent', 'status': 'ONLINE', 'type': 'creative'},
        {'id': 5, 'name': 'Music Producer Agent', 'status': 'ONLINE', 'type': 'production'},
        {'id': 6, 'name': 'Influencer Matcher Agent', 'status': 'ONLINE', 'type': 'marketing'},
        {'id': 7, 'name': 'Distribution Metadata Agent', 'status': 'ONLINE', 'type': 'distribution'},
        {'id': 8, 'name': 'Quality Assurance Agent', 'status': 'ONLINE', 'type': 'qa'},
        {'id': 9, 'name': 'Analytics Agent', 'status': 'ONLINE', 'type': 'analytics'},
        {'id': 10, 'name': 'Content Moderator Agent', 'status': 'ONLINE', 'type': 'moderation'},
        {'id': 11, 'name': 'Performance Monitor Agent', 'status': 'ONLINE', 'type': 'monitoring'},
        {'id': 12, 'name': 'Workflow Coordinator Agent', 'status': 'ONLINE', 'type': 'coordination'}
    ]
    return jsonify({
        'agents': agents_list,
        'total': len(agents_list),
        'online': len([a for a in agents_list if a['status'] == 'ONLINE'])
    }), 200


@app.route('/agents/<int:agent_id>', methods=['GET'])
def agent_detail(agent_id):
    """Get agent details by ID"""
    if agent_id < 1 or agent_id > 7:
        return jsonify({'error': 'Agent not found'}), 404

    agent_names = {
        1: 'Trend Detective Agent',
        2: 'Audio Quality Curator Agent',
        3: 'Video Concept Agent',
        4: 'Screenplay Generator Agent',
        5: 'Music Producer Agent',
        6: 'Influencer Matcher Agent',
        7: 'Distribution Metadata Agent'
    }

    return jsonify({
        'id': agent_id,
        'name': agent_names[agent_id],
        'status': 'online',
        'uptime': '99.9%',
        'tasks_completed': 42,
        'last_active': datetime.now().isoformat()
    }), 200


# ========== TRAINING ENDPOINTS ==========

@app.route('/training/status', methods=['GET'])
@app.route('/api/training/status', methods=['GET'])
def training_status():
    """Get training status"""
    return jsonify({
        'status': 'ready',
        'current_phase': 'idle',
        'phase': 'idle',
        'progress': 0,
        'progress_percent': 0,
        'iterations': 0,
        'last_run': None,
        'system_ready': True,
        'training_available': ORCHESTRATOR_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/training/start', methods=['POST'])
def start_training():
    """Start training session"""
    data = request.json or {}
    iterations = data.get('iterations', 10)

    logger.info(f"Training start requested with {iterations} iterations")

    return jsonify({
        'message': 'Training started',
        'status': 'in_progress',
        'iterations': iterations,
        'started_at': datetime.now().isoformat()
    }), 200


@app.route('/training/stop', methods=['POST'])
def stop_training():
    """Stop training session"""
    logger.info("Training stop requested")

    return jsonify({
        'message': 'Training stopped',
        'status': 'stopped',
        'stopped_at': datetime.now().isoformat()
    }), 200


# ========== ORCHESTRATION ENDPOINTS ==========

@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    """Run full orchestration pipeline"""
    data = request.json or {}

    logger.info("Full orchestration requested")

    return jsonify({
        'message': 'Orchestration started',
        'status': 'running',
        'agents_triggered': 7,
        'started_at': datetime.now().isoformat()
    }), 200


@app.route('/orchestrate/status', methods=['GET'])
def orchestrate_status():
    """Get orchestration status"""
    return jsonify({
        'status': 'idle',
        'last_run': None,
        'total_runs': 0,
        'success_rate': 100.0
    }), 200


# ========== RESULTS ENDPOINTS ==========

@app.route('/results', methods=['GET'])
def results():
    """Get orchestration results"""
    return jsonify({
        'results': [],
        'total': 0,
        'message': 'No results yet'
    }), 200


@app.route('/results/<result_id>', methods=['GET'])
def result_detail(result_id):
    """Get result details by ID"""
    return jsonify({
        'id': result_id,
        'status': 'not_found',
        'message': 'Result not found'
    }), 404


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({
        'error': 'Server error',
        'message': 'An internal server error occurred'
    }), 500


# ========== MAIN ==========

if __name__ == '__main__':
    print("\n" + "="*60)
    print("ORCHESTRATOR API SERVER")
    print("="*60)
    print(f"Port: 8000")
    print(f"Status: Starting...")
    print(f"Orchestrator Available: {ORCHESTRATOR_AVAILABLE}")
    print("="*60 + "\n")

    # Start Flask app
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=False,
        threaded=True
    )
