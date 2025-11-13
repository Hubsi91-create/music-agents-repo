â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Agent 3: Video Concept Collaborator

## Overview

The Video Concept Collaborator is a Vertex AI ADK agent specialized in creating comprehensive visual direction and storyboard concepts for music videos. It transforms song metadata into production-ready creative briefs with cinematographic recommendations, color palettes, and scene-by-scene breakdowns.

## Features

- **Visual Concept Generation**: Creates original, cinematically viable concepts aligned with song metadata
- **Cinematography Expertise**: Recommends specific camera techniques, lighting strategies, and equipment
- **Color Palette Development**: Generates mood-appropriate color schemes with psychological justification
- **Scene Breakdown Architecture**: Structures videos into logical, music-aligned scenes
- **Production Assessment**: Evaluates feasibility, budget implications, and timeline estimates
- **Batch Processing**: Handle multiple songs in a single run
- **Cloud Storage Integration**: Saves concepts to Google Cloud Storage with automatic fallback to local storage
- **Comprehensive Logging**: Full error tracking and operational visibility

## Requirements

- Python 3.9+
- Google Cloud SDK
- Vertex AI ADK access
- GCP Project with enabled APIs:
  - Vertex AI API
  - Cloud Storage API
  - Cloud Logging API

## Installation

### 1. Clone or download the agent files
```bash
cd agent-3-video-concept
```

### 2. Set up environment variables
```bash
export GCP_PROJECT_ID="your-gcp-project-id"
export GCP_BUCKET_NAME="your-gcs-bucket-name"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### 3. Install dependencies
```bash
make install
```

## Usage

### Running Locally

```bash
make run
```

### Programmatic Usage

```python
from agent import VideoConceptCollaborator

# Initialize agent
agent = VideoConceptCollaborator()

# Define song metadata
song = {
    "title": "Neon Dreams",
    "artist": "Synthwave Collective",
    "genre": "Synthwave",
    "mood": "Energetic, nostalgic, mysterious",
    "duration": 240,
    "bpm": 128,
    "lyrics_themes": ["Urban landscapes", "Neon lights", "Late night drives"]
}

# Generate concepts
concepts = agent.generate_visual_concepts(song)

# Save to Cloud Storage
saved_path = agent.save_concepts(concepts)
print(f"Concepts saved to: {saved_path}")
```

### Batch Processing

```python
songs = [
    {"title": "Song 1", "genre": "Reggaeton", "mood": "Energetic", "duration": 180},
    {"title": "Song 2", "genre": "Pop", "mood": "Uplifting", "duration": 200},
]

results = agent.process_batch(songs)
```

## Deployment

### Deploy to Vertex AI

```bash
make deploy PROJECT_ID=your-project-id REGION=us-central1
```

This creates a Cloud Function endpoint that can be invoked with HTTP requests:

```bash
curl -X POST https://REGION-PROJECT_ID.cloudfunctions.net/video-concept-agent-3 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Song Title",
    "genre": "Reggaeton",
    "mood": "Energetic",
    "duration": 240
  }'
```

## Output Structure

The agent returns a JSON object with the following structure:

```json
{
  "visual_direction": {
    "overall_concept": "...",
    "visual_style": "...",
    "target_mood": "..."
  },
  "cinematography": {
    "camera_techniques": [...],
    "lighting_strategy": "...",
    "movement_style": "...",
    "recommended_equipment": [...]
  },
  "color_palette": {
    "primary_colors": [...],
    "secondary_colors": [...],
    "color_psychology": "..."
  },
  "scene_breakdown": [
    {
      "scene_number": 1,
      "duration_seconds": 15,
      "description": "...",
      "visual_elements": [...],
      "camera_angle": "...",
      "special_effects": [...]
    }
  ],
  "production_notes": {
    "estimated_complexity": "low|medium|high",
    "key_challenges": [...],
    "budget_considerations": "...",
    "timeline_estimate": "..."
  },
  "generated_at": "2025-01-15T10:30:00Z",
  "song_title": "..."
}
```

## API Configuration

### Model Configuration
- **Model**: gemini-2.5-pro
- **Region**: us-central1
- **Temperature**: 0.8 (balanced creativity with consistency)
- **Top P**: 0.95
- **Top K**: 40
- **Max Output Tokens**: 4096

## Error Handling

The agent includes comprehensive error handling for:
- Missing or invalid input fields
- JSON parsing failures
- Cloud Storage connectivity issues
- Model API failures
- Invalid project configuration

All errors are logged with full context for debugging.

## System Prompt

The agent uses a detailed 300+ word system prompt that establishes:
- Expert identity and 15+ years of experience
- Core responsibilities and professional standards
- Genre-specific considerations
- Output structure and validation criteria
- Ethical guardrails and creative principles

See `system_prompt.txt` for the complete prompt.

## Performance Optimization

- **Streaming**: Concepts are generated with optimized token usage
- **Caching**: Metadata validation results are cached when processing batches
- **Parallel Processing**: Batch operations can be parallelized using cloud tasks
- **Storage**: Automatic local fallback if Cloud Storage is unavailable

## Troubleshooting

### "Failed to initialize agent"
Ensure GCP credentials are set and Vertex AI API is enabled:
```bash
gcloud services enable aiplatform.googleapis.com
```

### "Invalid JSON in response"
The model may occasionally generate malformed JSON. The agent includes retry logic in production deployments.

### "Permission denied" on Cloud Storage
Verify the service account has storage.objects.create permission on the target bucket.

## Cost Estimation

Pricing based on Vertex AI:
- Input tokens: ~$0.075 per 1M tokens
- Output tokens: ~$0.30 per 1M tokens
- Estimated cost per concept: $0.05 - $0.15

## Contributing

To extend the agent:
1. Add new analysis methods to the `VideoConceptCollaborator` class
2. Update the system prompt with new capabilities
3. Add corresponding tests
4. Follow the existing code style and documentation patterns

## Support

For issues, questions, or feature requests, contact the development team or refer to the Vertex AI documentation.

## License

Internal use only. All rights reserved.




â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
