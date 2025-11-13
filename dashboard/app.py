from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Web-Routen
@app.route('/')
def index():
    """Haupt-Dashboard laden"""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """System-Status abrufen"""
    return jsonify({
        "system": "7-Agent Music Production",
        "version": "1.0",
        "status": "PRODUCTION_READY",
        "agents": 7,
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
            {"id": 5, "name": "Prompt Generator", "status": "ACTIVE", "icon": "⚡"},
            {"id": 6, "name": "Influencer Matcher", "status": "ACTIVE", "icon": "👥"},
            {"id": 7, "name": "Distribution Manager", "status": "ACTIVE", "icon": "📤"}
        ]
    })

if __name__ == '__main__':
    print("🚀 Music-Agents Dashboard startet...")
    print("📍 http://localhost:5000")
    app.run(debug=True, port=5000, host='127.0.0.1')
