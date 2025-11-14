from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Configure paths
BASE_DIR = Path(__file__).parent.parent
PIPELINE_OUTPUT = BASE_DIR / "pipeline_output"
STYLE_ANCHORS_DIR = BASE_DIR / "style_anchors"

# Web-Routen
@app.route('/')
def index():
    """Haupt-Dashboard laden"""
    return render_template('index.html')

@app.route('/storyboard')
def storyboard():
    """Style Anchor Review Storyboard laden"""
    return render_template('storyboard.html')

@app.route('/api/status')
def status():
    """System-Status abrufen"""
    return jsonify({
        "system": "Music Video Production with Style Anchors",
        "version": "2.0",
        "status": "PRODUCTION_READY",
        "agents": 9,
        "features": ["Style Anchor Generation", "Visual Review", "Video Prompts"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/agents')
def agents():
    """Alle Agent-Informationen"""
    return jsonify({
        "agents": [
            {"id": 1, "name": "Music Inspiration Generator", "status": "ACTIVE", "icon": "🎵"},
            {"id": 2, "name": "Audio Quality Curator", "status": "ACTIVE", "icon": "🎚️"},
            {"id": 3, "name": "Video Concept Creator", "status": "ACTIVE", "icon": "🎬"},
            {"id": 4, "name": "Screenplay Writer", "status": "ACTIVE", "icon": "📝"},
            {"id": "5a-img", "name": "Nanobanana Image Generator", "status": "ACTIVE", "icon": "📸"},
            {"id": "5b-img", "name": "Runway Image Generator", "status": "ACTIVE", "icon": "🎨"},
            {"id": "5a", "name": "VEO Adapter", "status": "ACTIVE", "icon": "⚡"},
            {"id": "5b", "name": "Runway Adapter", "status": "ACTIVE", "icon": "🎬"},
            {"id": 6, "name": "Influencer Matcher", "status": "ACTIVE", "icon": "👥"},
            {"id": 7, "name": "Distribution Manager", "status": "ACTIVE", "icon": "📤"}
        ]
    })

@app.route('/api/style-anchors')
def get_style_anchors():
    """Load generated style anchors from pipeline output"""
    try:
        # Try to load from pipeline output
        anchors_file = PIPELINE_OUTPUT / "style_anchors_generated.json"

        if not anchors_file.exists():
            return jsonify({
                "error": "No style anchors found",
                "message": "Run the pipeline first: python pipeline_with_style_anchors.py screenplay.json",
                "path": str(anchors_file)
            }), 404

        with open(anchors_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": "Failed to load style anchors",
            "message": str(e)
        }), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve style anchor images"""
    try:
        # Images are in style_anchors/ directory
        return send_from_directory(STYLE_ANCHORS_DIR, filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/approve-scene/<int:scene_number>', methods=['POST'])
def approve_scene(scene_number):
    """Approve a specific scene's style anchors"""
    # TODO: Update approval status in database or file
    return jsonify({
        "status": "approved",
        "scene_number": scene_number,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/reject-scene/<int:scene_number>', methods=['POST'])
def reject_scene(scene_number):
    """Reject a specific scene's style anchors"""
    # TODO: Update rejection status
    return jsonify({
        "status": "rejected",
        "scene_number": scene_number,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Music-Agents Dashboard startet...")
    print("📍 http://localhost:5000")
    app.run(debug=True, port=5000, host='127.0.0.1')
