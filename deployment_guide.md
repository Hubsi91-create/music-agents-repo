# AGENT 8: PROMPT REFINER & VALIDATOR
## Deployment Guide - Google Cloud Vertex AI
**Stand:** 12. November 2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ÜBERSICHT

Agent 8 ist ein Quality Assurance System für Video Generation Prompts:
- **Input:** Rohe VEO 3.1 / Runway Gen-4 Prompts von Agent 6 & 5b
- **Output:** Validierte, optimierte Prompts + JSON Quality Report
- **Deployment:** Google Cloud Functions (HTTP Trigger)
- **Architecture:** Lokal VSCode/PowerShell → Claude Code → Google Cloud

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## DATEIEN

```
music-agents-repo/
├── agent_8_prompt_refiner.py     # Main Python Agent
├── config_agent8.json            # Genre Profiles & Validation Rules
├── requirements.txt              # Python Dependencies
└── deployment_guide.md           # This File
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 1: LOKALE ENTWICKLUNG

### 1.1 VSCode / PowerShell Setup

```powershell
# Navigate to repository
cd C:\path\to\music-agents-repo

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Lokales Testing

```powershell
# Run agent locally
python agent_8_prompt_refiner.py
```

**Erwarteter Output:**
```
================================================================================
AGENT 8: PROMPT REFINER & VALIDATOR - TEST RUN
================================================================================
{
  "prompt_type": "veo_3.1",
  "genre_detected": "reggaeton",
  "original_prompt": "...",
  "refined_prompt": "...",
  "validation_scores": {
    "structural": 0.85,
    "genre_compliance": 0.90,
    "artifact_risk": 0.75,
    "consistency": 0.80,
    "performance_optimization": 0.85,
    "overall_quality_score": 0.82
  },
  "ready_for_generation": true,
  "generation_mode_recommendation": "veo_standard"
}
================================================================================
✓ Ready for generation in veo_standard
Quality Score: 0.82
Estimated Rating: 4.1/5.0 stars
================================================================================
```

### 1.3 Claude Code Optimierung

```powershell
# In VSCode Terminal
claude code optimize agent_8_prompt_refiner.py
```

Claude Code wird:
- Type Hints hinzufügen
- Error Handling verbessern
- Logging integrieren
- Production-Ready machen

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 2: GOOGLE CLOUD DEPLOYMENT

### 2.1 Google Cloud Setup

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 2.2 Deploy as Cloud Function

```bash
# Deploy Agent 8
gcloud functions deploy agent-8-prompt-refiner \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point validate_prompt \
  --source . \
  --memory 512MB \
  --timeout 60s \
  --region us-central1
```

**Deployment Output:**
```
Deploying function (may take a while)...
✓ Deployment successful
Function URL: https://us-central1-YOUR-PROJECT.cloudfunctions.net/agent-8-prompt-refiner
```

### 2.3 Upload Config File

```bash
# Upload config to Cloud Function
gcloud functions deploy agent-8-prompt-refiner \
  --update-env-vars CONFIG_PATH=config_agent8.json \
  --source .
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 3: INTEGRATION MIT AGENT PIPELINE

### 3.1 HTTP API Usage

**Request Format:**
```bash
curl -X POST https://us-central1-YOUR-PROJECT.cloudfunctions.net/agent-8-prompt-refiner \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your VEO 3.1 or Runway Gen-4 prompt here",
    "prompt_type": "veo_3.1",
    "genre": "reggaeton"
  }'
```

**Response Format:**
```json
{
  "prompt_type": "veo_3.1",
  "genre_detected": "reggaeton",
  "original_prompt": "...",
  "refined_prompt": "...",
  "validation_scores": {
    "overall_quality_score": 0.85
  },
  "ready_for_generation": true,
  "generation_mode_recommendation": "veo_standard",
  "estimated_quality_rating": 4.25
}
```

### 3.2 Integration mit Agent 6 & 5b

**Agent 6 (Prompt Generator) → Agent 8 (Validator) → Agent 5b (Video Generator)**

```python
# In Agent 6 code:
import requests

# Generate prompt
veo_prompt = generate_veo_prompt(...)

# Send to Agent 8 for validation
response = requests.post(
    "https://us-central1-YOUR-PROJECT.cloudfunctions.net/agent-8-prompt-refiner",
    json={
        "prompt": veo_prompt,
        "prompt_type": "veo_3.1",
        "genre": "reggaeton"
    }
)

validation_report = response.json()

# Check if ready for generation
if validation_report["ready_for_generation"]:
    # Send refined prompt to Agent 5b
    refined_prompt = validation_report["refined_prompt"]
    send_to_agent_5b(refined_prompt, validation_report["generation_mode_recommendation"])
else:
    # Log issues and retry or manual review
    print(validation_report["recommendations"])
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 4: MONTHLY PERPLEXITY UPDATES

### 4.1 Update Workflow (Jeden 1. Montag im Monat)

**Schritt 1: Deep Research in Perplexity Pro**
```
Query: "Comprehensive analysis: Latest VEO 3.1 and Runway Gen-4 prompt
optimization techniques 2025. Focus on:
- New artifact patterns discovered
- Updated genre-specific parameters
- Improved auto-fix rules
- Best practices for lip-sync accuracy
- Motion continuity improvements"
```

**Schritt 2: Findings zu Claude Opus 4.1**
```
Prompt: "Analyze these Perplexity findings and update config_agent8.json:

[Paste Perplexity Output]

Generate JSON updates for:
1. artifact_detection.veo_risks (neue Patterns?)
2. artifact_detection.runway_risks (neue Patterns?)
3. genres[].auto_negatives (aktualisierte Negatives?)
4. auto_fix_rules (verbesserte Fix-Logik?)

Output nur die geänderten JSON Sections, nicht die ganze Config."
```

**Schritt 3: Updates mergen**
```bash
# Backup current config
cp config_agent8.json config_agent8.json.backup

# Edit config_agent8.json with Claude's suggestions
# (Manually merge JSON updates)

# Test locally
python agent_8_prompt_refiner.py

# Redeploy
gcloud functions deploy agent-8-prompt-refiner \
  --source . \
  --update-env-vars CONFIG_PATH=config_agent8.json
```

**Schritt 4: Documentation**
```bash
# Create changelog entry
echo "$(date): Updated config based on Perplexity findings" >> CHANGELOG.md
git add config_agent8.json CHANGELOG.md
git commit -m "Update Agent 8 config - Monthly Perplexity refresh"
git push
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 5: MONITORING & MAINTENANCE

### 5.1 Cloud Function Logs

```bash
# View real-time logs
gcloud functions logs read agent-8-prompt-refiner --limit 50

# Filter for errors
gcloud functions logs read agent-8-prompt-refiner \
  --filter "severity>=ERROR" \
  --limit 100
```

### 5.2 Performance Metrics

**Google Cloud Console → Cloud Functions → agent-8-prompt-refiner:**
- Invocations per day
- Average execution time
- Error rate
- Memory usage

**Target Metrics:**
- Average execution time: < 2 seconds
- Error rate: < 0.5%
- Memory usage: < 300MB

### 5.3 Quality Tracking

**Track validation scores over time:**
```python
# Add logging to agent_8_prompt_refiner.py
import logging
from google.cloud import logging as cloud_logging

client = cloud_logging.Client()
logger = client.logger('agent-8-quality-scores')

# After validation
logger.log_struct({
    'timestamp': datetime.now().isoformat(),
    'genre': report.genre_detected,
    'quality_score': report.validation_scores.overall_quality_score,
    'ready': report.ready_for_generation
})
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## TROUBLESHOOTING

### Problem: "Module not found" Error

**Lösung:**
```bash
# Verify requirements.txt is deployed
gcloud functions describe agent-8-prompt-refiner --format="value(sourceUploadUrl)"

# Redeploy with explicit dependencies
gcloud functions deploy agent-8-prompt-refiner \
  --source . \
  --runtime python311
```

### Problem: Config File Not Found

**Lösung:**
```bash
# Ensure config_agent8.json is in the same directory
ls -la config_agent8.json

# Redeploy
gcloud functions deploy agent-8-prompt-refiner --source .
```

### Problem: Timeout Errors

**Lösung:**
```bash
# Increase timeout to 120 seconds
gcloud functions deploy agent-8-prompt-refiner \
  --timeout 120s \
  --memory 1024MB
```

### Problem: Invalid JSON Response

**Lösung:**
```python
# Add error handling in validate_prompt function
try:
    report = agent.validate_and_refine(...)
    return flask.Response(report.to_json(), mimetype='application/json')
except Exception as e:
    return flask.jsonify({"error": str(e)}), 500
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## KOSTENMANAGEMENT

### Google Cloud Functions Pricing (Stand 2025)

**Free Tier:**
- 2M invocations/month
- 400,000 GB-seconds/month
- 200,000 GHz-seconds/month

**Estimated Costs für Agent 8:**
- 10,000 invocations/month @ 512MB / 2s execution
- **$0.00** (innerhalb Free Tier)

**Bei > 2M invocations/month:**
- ~$0.40 per million additional invocations
- ~$0.0000025 per GB-second

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECURITY BEST PRACTICES

### 1. Authentication

```bash
# Remove --allow-unauthenticated for production
gcloud functions deploy agent-8-prompt-refiner \
  --no-allow-unauthenticated

# Create service account
gcloud iam service-accounts create agent-8-invoker \
  --display-name "Agent 8 Invoker"

# Grant invoke permission
gcloud functions add-iam-policy-binding agent-8-prompt-refiner \
  --member="serviceAccount:agent-8-invoker@YOUR-PROJECT.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.invoker"
```

### 2. Input Validation

Already implemented in code:
- Required fields validation
- Prompt type verification
- Genre validation with fallback

### 3. Rate Limiting

```bash
# Add Cloud Endpoints for rate limiting
# (optional for production)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## NÄCHSTE SCHRITTE

1. **Local Testing:** Run `python agent_8_prompt_refiner.py`
2. **Optimize with Claude:** Use Claude Code for production hardening
3. **Deploy to Cloud:** Follow Phase 2 deployment steps
4. **Integrate Pipeline:** Connect Agent 6 → Agent 8 → Agent 5b
5. **Schedule Updates:** Set calendar reminder for monthly Perplexity refresh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SUPPORT & DOCUMENTATION

**Internal Documentation:**
- Agent 1-7 Specs: `/docs/agents/`
- Pipeline Architecture: `/docs/pipeline_overview.md`
- Genre Profiles: `config_agent8.json`

**External Resources:**
- Google Cloud Functions Docs: https://cloud.google.com/functions/docs
- VEO 3.1 API Docs: (wenn verfügbar)
- Runway Gen-4 API Docs: https://docs.runwayml.com/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**AGENT 8 DEPLOYMENT GUIDE - COMPLETE**

Stand: 12. November 2025
Version: 1.0
Status: Production Ready
