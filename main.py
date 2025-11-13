"""
AGENT 8 - GOOGLE CLOUD FUNCTIONS ENTRY POINT
Deployment Target: Google Cloud Functions (europe-west3)
"""

import functions_framework
from flask import jsonify
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Agent 8
try:
    from agent_8_prompt_refiner import Agent8PromptRefiner
    logger.info("✅ Agent 8 imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import Agent 8: {e}")
    agent8 = None

# Initialize Agent 8 globally (cold start optimization)
try:
    agent8 = Agent8PromptRefiner("config_agent8.json")
    logger.info("✅ Agent 8 initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Agent 8: {e}")
    agent8 = None


@functions_framework.http
def validate_prompt(request):
    """
    Google Cloud Function Entry Point

    HTTP Endpoint for prompt validation

    Request Format (POST):
    {
        "prompt": "VEO prompt text",
        "prompt_type": "veo_3.1" or "runway_gen4",
        "genre": "reggaeton" | "edm" | "hiphop" | "pop" | "rb_soul"
    }

    Response Format:
    {
        "status": "success",
        "timestamp": "2025-11-13T...",
        "validation": {
            "quality_score": 0.82,
            "ready_for_generation": true,
            "issues_count": 2,
            "issues": ["issue1", "issue2"],
            "recommendations": ["rec1", "rec2"]
        },
        "refined_prompt": "improved prompt text",
        "generation_mode": "Standard"
    }
    """

    # Set CORS headers for browser access
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    # Health check
    if request.method == 'GET':
        return (jsonify({
            "status": "healthy",
            "service": "Agent 8 - Prompt Refiner & Validator",
            "version": "1.0",
            "region": "europe-west3",
            "agent8_initialized": agent8 is not None,
            "timestamp": datetime.now().isoformat()
        }), 200, headers)

    # Validation endpoint
    if request.method != 'POST':
        return (jsonify({"error": "Method not allowed. Use POST."}), 405, headers)

    # Check if Agent 8 is initialized
    if not agent8:
        logger.error("Agent 8 not initialized")
        return (jsonify({
            "status": "error",
            "error": "Agent 8 not initialized. Check logs."
        }), 500, headers)

    try:
        # Parse request
        request_json = request.get_json(silent=True)

        if not request_json:
            return (jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400, headers)

        # Extract parameters
        prompt = request_json.get("prompt", "")
        prompt_type = request_json.get("prompt_type", "veo_3.1")
        genre = request_json.get("genre", "pop")

        # Validate input
        if not prompt:
            return (jsonify({
                "status": "error",
                "error": "prompt field is required"
            }), 400, headers)

        if prompt_type not in ["veo_3.1", "runway_gen4"]:
            return (jsonify({
                "status": "error",
                "error": f"Invalid prompt_type: {prompt_type}. Use 'veo_3.1' or 'runway_gen4'"
            }), 400, headers)

        logger.info(f"📥 Validation request: {prompt_type} ({genre})")

        # Run Agent 8 validation
        report = agent8.validate_and_refine(prompt, prompt_type, genre)

        # Format response
        response_data = {
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

        logger.info(f"✅ Validation complete: Score={response_data['validation']['quality_score']}")

        return (jsonify(response_data), 200, headers)

    except Exception as e:
        logger.error(f"❌ Validation error: {e}")
        import traceback
        traceback.print_exc()

        return (jsonify({
            "status": "error",
            "error": str(e)
        }), 500, headers)


# For local testing with Functions Framework
if __name__ == "__main__":
    # This allows local testing with: functions-framework --target=validate_prompt
    print("🚀 Agent 8 Cloud Function")
    print("📍 For local testing: functions-framework --target=validate_prompt --port=8080")
    print("📍 Test with: curl -X POST http://localhost:8080 -H 'Content-Type: application/json' -d '{\"prompt\":\"test\",\"prompt_type\":\"veo_3.1\"}'")
