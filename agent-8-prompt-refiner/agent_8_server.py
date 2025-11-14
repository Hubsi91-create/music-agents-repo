"""
AGENT 8 - HTTP SERVER
Macht Agent 8 als REST API verfügbar für Agent 6/7 Integration
"""

from flask import Flask, request, jsonify
import logging
import json
from datetime import datetime
from typing import Dict, Optional

# Import existing Agent 8
try:
    from agent_8_prompt_refiner import Agent8PromptRefiner
except ImportError:
    print("❌ ERROR: agent_8_prompt_refiner.py not found!")
    print("Make sure you're in the music-agents-repo root directory")
    exit(1)

# Setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Initialize Agent 8
try:
    agent8 = Agent8PromptRefiner("config_agent8.json")
    logger.info("✅ Agent 8 initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Agent 8: {e}")
    agent8 = None


@app.route('/', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Agent 8 HTTP Server",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/validate', methods=['POST'])
def validate():
    """
    Main validation endpoint

    Input:
    {
        "prompt": "VEO prompt text",
        "prompt_type": "veo_3.1" or "runway_gen4",
        "genre": "reggaeton" or others
    }

    Output:
    {
        "status": "success",
        "validation": {
            "quality_score": 0.82,
            "ready_for_generation": true,
            "issues": [...],
            "recommendations": [...]
        },
        "refined_prompt": "improved prompt text",
        "generation_mode": "Standard"
    }
    """

    if not agent8:
        return jsonify({"error": "Agent 8 not initialized"}), 500

    try:
        # Get request data
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Extract parameters
        prompt = data.get("prompt")
        prompt_type = data.get("prompt_type", "veo_3.1")
        genre = data.get("genre", "pop")

        # Validate input
        if not prompt:
            return jsonify({"error": "prompt field is required"}), 400

        if prompt_type not in ["veo_3.1", "runway_gen4"]:
            return jsonify({"error": f"Invalid prompt_type: {prompt_type}"}), 400

        logger.info(f"📥 Validation request: {prompt_type} ({genre})")

        # Run Agent 8 validation
        report = agent8.validate_and_refine(prompt, prompt_type, genre)

        # Format response
        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "validation": {
                "quality_score": round(report.validation_scores.overall_quality_score, 2),
                "ready_for_generation": report.ready_for_generation,
                "issues_count": len(report.issues_found),
                "issues": [issue.message for issue in report.issues_found[:5]],
                "recommendations": report.recommendations[:3]
            },
            "refined_prompt": report.refined_prompt,
            "generation_mode": report.generation_mode_recommendation
        }

        logger.info(f"✅ Validation complete: Score={response['validation']['quality_score']}")

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"❌ Validation error: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def detailed_health():
    """Detailed health check"""
    return jsonify({
        "status": "operational",
        "service": "Agent 8 HTTP Server",
        "version": "1.0",
        "agent8_initialized": agent8 is not None,
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "GET /",
            "GET /health",
            "POST /validate",
            "GET /metrics (future)"
        ]
    }), 200


@app.route('/test', methods=['POST'])
def test_validation():
    """Test endpoint with predefined prompts"""

    test_prompts = {
        "veo_simple": {
            "prompt": "A serene beach at sunset with gentle waves, warm golden lighting, 4K cinematic",
            "prompt_type": "veo_3.1",
            "genre": "pop"
        },
        "runway_simple": {
            "prompt": "Dynamic hip-hop music video scene with urban dancers, high contrast, fast cuts",
            "prompt_type": "runway_gen4",
            "genre": "hiphop"
        }
    }

    if not agent8:
        return jsonify({"error": "Agent 8 not initialized"}), 500

    try:
        # Get test type from request
        data = request.get_json() or {}
        test_type = data.get("test_type", "veo_simple")

        if test_type not in test_prompts:
            return jsonify({"error": f"Unknown test type: {test_type}"}), 400

        # Get test prompt data
        test_data = test_prompts[test_type]
        prompt = test_data["prompt"]
        prompt_type = test_data["prompt_type"]
        genre = test_data["genre"]

        logger.info(f"🧪 Test validation request: {test_type}")

        # Run Agent 8 validation
        report = agent8.validate_and_refine(prompt, prompt_type, genre)

        # Format response
        response = {
            "status": "success",
            "test_type": test_type,
            "timestamp": datetime.now().isoformat(),
            "validation": {
                "quality_score": round(report.validation_scores.overall_quality_score, 2),
                "ready_for_generation": report.ready_for_generation,
                "issues_count": len(report.issues_found),
                "issues": [issue.message for issue in report.issues_found[:5]],
                "recommendations": report.recommendations[:3]
            },
            "refined_prompt": report.refined_prompt,
            "generation_mode": report.generation_mode_recommendation
        }

        logger.info(f"✅ Test validation complete: Score={response['validation']['quality_score']}")

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"❌ Test validation error: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# Google Cloud Function Entry Point
def validate_prompt(request):
    """
    Google Cloud Function Entry Point
    Konvertiert Cloud Request zu Flask Request
    """
    try:
        # Check if agent8 is initialized
        if not agent8:
            return {"error": "Agent 8 not initialized"}, 500

        # Parse JSON from request
        request_json = request.get_json()

        if not request_json:
            return {"error": "No JSON data provided"}, 400

        # Extract parameters
        prompt = request_json.get("prompt", "")
        prompt_type = request_json.get("prompt_type", "veo_3.1")
        genre = request_json.get("genre", "pop")

        if not prompt:
            return {"error": "prompt field is required"}, 400

        logger.info(f"📥 Cloud validation request: {prompt_type} ({genre})")

        # Run Agent 8 validation
        report = agent8.validate_and_refine(prompt, prompt_type, genre)

        # Format response
        result = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "validation": {
                "quality_score": round(report.validation_scores.overall_quality_score, 2),
                "ready_for_generation": report.ready_for_generation,
                "issues_count": len(report.issues_found),
                "issues": [issue.message for issue in report.issues_found[:5]],
                "recommendations": report.recommendations[:3]
            },
            "refined_prompt": report.refined_prompt,
            "generation_mode": report.generation_mode_recommendation
        }

        logger.info(f"✅ Cloud validation complete: Score={result['validation']['quality_score']}")

        return result, 200

    except Exception as e:
        logger.error(f"❌ Cloud validation error: {e}")
        return {
            "error": str(e),
            "status": "error"
        }, 500


if __name__ == "__main__":
    logger.info("🚀 Starting Agent 8 HTTP Server")
    logger.info("📍 http://localhost:5000")
    logger.info("📝 POST /validate - Main validation endpoint")
    logger.info("🏥 GET /health - Detailed health check")
    logger.info("🧪 POST /test - Test validation")

    # Run Flask server
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        threaded=True
    )
