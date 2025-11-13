â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Agent 4: Video Production Specialist (Combined Veo + Screenplay)

## Overview

The Video Production Specialist is a dual-module Vertex AI ADK agent that combines two integrated functions:

1. **Veo 3 Prompt Generator**: Creates optimized Google Veo 3 AI video generation prompts
2. **Screenplay Generator**: Writes complete, production-ready screenplays for music videos

**Important**: This is ONE agent with TWO coordinated modules, NOT two separate agents. Both modules process the same video concepts simultaneously and integrate their outputs into a cohesive production pipeline.

## Architecture

```
Agent 4 (Main Orchestrator)
â”œâ”€â”€ Module 1: Veo 3 Prompt Generator
â”‚   â”œâ”€â”€ Prompt optimization
â”‚   â”œâ”€â”€ Token efficiency
â”‚   â””â”€â”€ Technical specification
â”œâ”€â”€ Module 2: Screenplay Generator
â”‚   â”œâ”€â”€ Screenplay formatting
â”‚   â”œâ”€â”€ Scene composition
â”‚   â””â”€â”€ Production notes
â””â”€â”€ Integration Layer
    â”œâ”€â”€ Cross-module validation
    â”œâ”€â”€ Consistency checking
    â””â”€â”€ Combined output assembly
```

## Features

### Veo 3 Prompt Generation
- Optimized prompts for Google Veo 3 video synthesis
- Token-efficient prompt engineering
- Technical parameter optimization (resolution, duration, motion)
- Color palette integration
- Scene continuity management
- Confidence scoring for prompts

### Screenplay Writing
- Industry-standard screenplay formatting
- Music video-specific structure and timing
- Technical specifications for production teams
- Equipment and resource recommendations
- Pre-/on-set/post-production guidelines
- Music synchronization instructions

### Dual-Module Integration
- Simultaneous processing of video concepts
- Cross-module validation and consistency checking
- Integrated output combining both modules
- Scene-by-scene alignment
- Technical requirement consistency

## Requirements

- Python 3.9+
- Google Cloud SDK
- Vertex AI ADK access
- GCP Project with enabled APIs:
  - Vertex AI API
  - Cloud Storage API
  - Cloud Logging API

## Installation

### 1. Set up environment variables
```bash
export GCP_PROJECT_ID="your-gcp-project-id"
export GCP_BUCKET_NAME="your-gcs-bucket-name"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### 2. Install dependencies
```bash
make install
```

### 3. Ensure module files are in same directory
```
agent-4/
â”œâ”€â”€ agent.py
â”œâ”€â”€ veo_prompt_generator.py
â”œâ”€â”€ screenplay_generator.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ Makefile
â”œâ”€â”€ system_prompt.txt
â””â”€â”€ README.md
```

## Usage

### Running Locally

```bash
make run
```

### Programmatic Usage

```python
from agent import VideoProductionSpecialist
import json

# Initialize agent (loads both modules)
agent = VideoProductionSpecialist()

# Load video concepts from Agent 3
with open('agent3_output.json', 'r') as f:
    video_concepts = json.load(f)

# Process through both modules
production_output = agent.process_video_concepts(video_concepts)

# Save outputs (Veo prompts + screenplay)
saved_paths = agent.save_production_output(production_output)

print(f"Veo prompts saved to: {saved_paths['veo_prompts']}")
print(f"Screenplay saved to: {saved_paths['screenplay']}")
```

### Export Formats

```python
# Export as Markdown for sharing
markdown = agent.export_for_production_team(production_output, format="markdown")

# Export as plaintext
plaintext = agent.export_for_production_team(production_output, format="plaintext")

# Export as JSON (default)
json_output = agent.export_for_production_team(production_output, format="json")
```

### Batch Processing

```python
# Process multiple video concepts
concepts_list = [concepts1, concepts2, concepts3]
results = agent.process_batch_concepts(concepts_list)
```

## Deployment

### Deploy to Vertex AI

```bash
make deploy PROJECT_ID=your-project-id REGION=us-central1
```

Creates Cloud Function endpoint:
```bash
curl -X POST https://REGION-PROJECT_ID.cloudfunctions.net/video-production-agent-4 \
  -H "Content-Type: application/json" \
  -d @video_concepts.json
```

## Output Structure

### Combined Output Format

```json
{
  "veo_prompts": [
    {
      "scene_number": 1,
      "duration_seconds": 15,
      "prompt_text": "Optimized Veo 3 prompt...",
      "visual_elements": [...],
      "special_effects": [...],
      "confidence_score": 0.92
    }
  ],
  "screenplay_sections": [
    {
      "section_name": "Title Page",
      "section_type": "title_page",
      "content": "Screenplay text..."
    },
    {
      "section_name": "Scene 1",
      "section_type": "scene",
      "content": "INT./EXT. - LOCATION - 15s..."
    }
  ],
  "orchestration_metadata": {
    "processed_at": "2025-01-15T10:30:00Z",
    "video_title": "Song Title",
    "total_scenes": 6,
    "total_veo_prompts": 6,
    "screenplay_word_count": 2847,
    "production_status": "ready_for_filming"
  }
}
```

### Veo Prompts Output

Each prompt includes:
- Scene number and duration
- Optimized prompt text for Veo 3
- Visual elements and special effects
- Technical specifications
- Confidence score (0.7-1.0)

### Screenplay Output

Each screenplay section includes:
- Section name and type
- Full screenplay-formatted content
- Technical notes for production
- Timing and synchronization information

## Module Details

### Veo 3 Prompt Generator (veo_prompt_generator.py)

**Key Methods:**
- `generate_veo_prompts()`: Converts concepts to Veo 3 prompts
- `_build_veo_prompt()`: Creates individual scene prompts
- `validate_veo_prompt()`: Validates prompt structure
- `optimize_for_veo_constraints()`: Optimizes for token limits

**Key Features:**
- Token-aware prompt generation (<500 tokens per prompt)
- Technical specification builder
- Confidence scoring
- Veo 3 constraint validation

### Screenplay Generator (screenplay_generator.py)

**Key Methods:**
- `generate_screenplay()`: Generates complete screenplay
- `_generate_title_page()`: Creates title page section
- `_generate_scene_sections()`: Creates scene-by-scene content
- `_format_scene_as_screenplay()`: Formats scenes in screenplay format
- `export_as_pdf_ready()`: Exports for PDF conversion

**Key Features:**
- Industry-standard screenplay formatting
- Scene numbering and timing
- Technical specification integration
- Production guidelines generation

## API Configuration

### Model Configuration
- **Model**: gemini-2.5-pro
- **Region**: us-central1
- **Temperature**: 0.8 (creativity balanced with consistency)
- **Max Output Tokens**: 4096

### Veo 3 Parameters
- **Token Limit**: ~500 per prompt
- **Supported Effects**: motion_blur, slow_motion, transitions, etc.
- **Resolution Options**: 720p, 1080p, 2K, 4K
- **Duration**: 5-60 seconds per generation

## Performance Notes

- **Processing Time**: ~30-60 seconds for typical 6-scene video
- **Module Parallelization**: Both modules process simultaneously
- **Token Usage**: ~3000-4000 tokens per full video production
- **Cost Estimate**: $0.10-$0.25 per complete production pipeline

## Error Handling

Comprehensive error handling for:
- Invalid video concept structure
- Missing required fields
- Cloud Storage connectivity issues
- Model API failures
- JSON serialization errors

All errors are logged with full context and appropriate fallbacks.

## Troubleshooting

### "Module not found" Error
Ensure `veo_prompt_generator.py` and `screenplay_generator.py` are in the same directory as `agent.py`.

### "Failed to initialize agent"
```bash
gcloud services enable aiplatform.googleapis.com
```

### Prompts Too Long
Module automatically trims prompts exceeding Veo 3 token limits. Check confidence_score < 0.8.

## Integration with Agent 3

**Expected Input** (from Agent 3):
```python
{
  "visual_direction": {...},
  "cinematography": {...},
  "color_palette": {...},
  "scene_breakdown": [...],
  "production_notes": {...},
  "song_title": "..."
}
```

**Output** (ready for production team):
```python
{
  "veo_prompts": [...],      # For Veo 3 video generation
  "screenplay_sections": [...], # For filming and production
  "orchestration_metadata": {...}
}
```

## System Prompt

See `system_prompt.txt` for the complete 300+ word system prompt that governs both modules with:
- Module-specific identities and competencies
- Veo 3 prompt engineering guidelines
- Screenplay writing standards
- Integration and coordination rules
- Quality standards for both modules

## Cost Estimation

Based on Vertex AI pricing:
- Input tokens: ~$0.075 per 1M
- Output tokens: ~$0.30 per 1M
- **Estimated cost per production**: $0.15-$0.30

## Contributing

To extend the agent:
1. Add new methods to respective modules
2. Update system prompt with new capabilities
3. Add validation in orchestration layer
4. Test cross-module consistency
5. Document new features

## Architecture Diagrams

### Input-Output Flow
```
Agent 3 Output (Video Concepts)
    â†“
Agent 4 Initialization
    â”œâ”€â”€ Load Veo Prompt Generator
    â””â”€â”€ Load Screenplay Generator
    â†“
Process Concepts
    â”œâ”€â”€ Module 1: Generate Veo Prompts
    â””â”€â”€ Module 2: Generate Screenplay
    â†“
Integrate Outputs
    â”œâ”€â”€ Cross-validate modules
    â”œâ”€â”€ Align scene numbers
    â””â”€â”€ Combine into production package
    â†“
Save to Cloud Storage
    â”œâ”€â”€ Veo prompts JSON
    â”œâ”€â”€ Screenplay JSON
    â””â”€â”€ Combined output JSON
    â†“
Export Options
    â”œâ”€â”€ JSON (raw data)
    â”œâ”€â”€ Markdown (for sharing)
    â””â”€â”€ Plaintext (for reading)
```

## Support

For issues or questions, refer to:
- Vertex AI ADK documentation
- Google Veo 3 API reference
- Screenplay formatting standards (Studio Standard)

## License

Internal use only. All rights reserved.
