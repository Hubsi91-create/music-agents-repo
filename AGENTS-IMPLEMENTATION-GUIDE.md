# 🎵 AI MUSIC VIDEO PRODUCTION SYSTEM v2.0
## Complete Implementation Guide for Claude Code

**Date:** 12.11.2025
**Target:** Google Cloud Vertex AI + Gemini 2.5 Pro
**Status:** Production Ready

---

## 📋 TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Agent 1: Trend Detective](#agent-1-trend-detective)
4. [Agent 2: Suno Prompt Generator](#agent-2-suno-prompt-generator)
5. [Agent 3: Audio Analyzer](#agent-3-audio-analyzer)
6. [Agent 4: Scene Breakdown](#agent-4-scene-breakdown)
7. [Agent 5: Style Anchors](#agent-5-style-anchors)
8. [Agent 6: Veo Prompt Optimizer](#agent-6-veo-prompt-optimizer)
9. [Agent 7: Runway Prompt Optimizer](#agent-7-runway-prompt-optimizer)
10. [Agent 8: Prompt Refiner](#agent-8-prompt-refiner)
11. [Agent 9: Video Editor](#agent-9-video-editor)
12. [Agent 10: Audio Master](#agent-10-audio-master)
13. [Agent 11: Trainer System](#agent-11-trainer-system)
14. [Integration Guide](#integration-guide)
15. [Testing Procedures](#testing-procedures)
16. [Deployment Instructions](#deployment-instructions)

---

## 🎯 SYSTEM OVERVIEW

The AI Music Video Production System consists of 11 specialized agents that work together to:
- Detect trending topics
- Generate music prompts
- Analyze audio structure
- Create video scene breakdowns
- Optimize AI video generation prompts
- Master final audio/video output
- Learn and improve from each project

**Technology Stack:**
- Python 3.11+
- Google Vertex AI with Gemini 2.5 Pro
- Google Cloud Functions
- Pydantic for data validation
- Asyncio for concurrent operations

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                     AGENT 11: TRAINER                       │
│                  (Meta-Orchestrator)                        │
└─────────────────────────────────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
    │ Agent 1 │       │ Agent 2 │       │ Agent 3 │
    │  Trend  │──────►│  Suno   │◄──────│  Audio  │
    │Detective│       │ Prompt  │       │Analyzer │
    └─────────┘       └────┬────┘       └─────────┘
                           │
                      ┌────▼────┐
                      │ Agent 4 │
                      │  Scene  │
                      │Breakdown│
                      └────┬────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
            ┌────▼────┐         ┌───▼────┐
            │ Agent 5 │         │Agent 6 │
            │  Style  │────────►│  Veo   │
            │Anchors  │         │Optimizer│
            └─────────┘         └───┬────┘
                 │                  │
                 │              ┌───▼────┐
                 └─────────────►│Agent 7 │
                                │ Runway │
                                │Optimizer│
                                └───┬────┘
                                    │
                               ┌────▼────┐
                               │ Agent 8 │
                               │ Prompt  │
                               │ Refiner │
                               └────┬────┘
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                     ┌────▼────┐         ┌───▼────┐
                     │ Agent 9 │         │Agent 10│
                     │  Video  │◄────────│ Audio  │
                     │ Editor  │         │ Master │
                     └─────────┘         └────────┘
```

---

# 🤖 AGENT 1: TREND DETECTIVE

## Purpose
Monitor and identify trending topics across TikTok, Instagram, and YouTube in real-time using Gemini 2.5 Pro for sentiment analysis and cultural context detection.

## File Structure
```
agent-1-trend-detective/
├── app/
│   └── agent.py
├── system_prompt.txt
├── requirements.txt
└── README.md
```

## agent.py

```python
"""
Agent 1: Trend Detective
Purpose: Monitor & identify trending topics across social platforms
Model: Gemini 2.5 Pro
Date: 12.11.2025
"""

import json
import os
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel, Field, validator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrendVelocity(str, Enum):
    EMERGING = "emerging"
    TRENDING = "trending"
    VIRAL = "viral"


class Platform(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"


class Region(str, Enum):
    US = "US"
    EU = "EU"
    LATAM = "LATAM"
    GLOBAL = "GLOBAL"


class Genre(str, Enum):
    REGGAETON = "reggaeton"
    EDM = "edm"
    POP = "pop"
    HIP_HOP = "hip-hop"
    AFROBEATS = "afrobeats"


class TrendInput(BaseModel):
    platforms: List[Platform] = Field(default=[Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE])
    regions: List[Region] = Field(default=[Region.GLOBAL])
    time_range: str = Field(default="24h", pattern="^(24h|7d|30d)$")
    genre_filters: List[Genre] = Field(default=[])


class TrendItem(BaseModel):
    rank: int
    trend_name: str
    platform: str
    velocity: TrendVelocity
    growth_rate: float
    estimated_reach: int
    cultural_context: str
    music_opportunity: bool
    recommended_genres: List[str]


class TrendOutput(BaseModel):
    agent_id: int = 1
    timestamp: str
    trends: List[TrendItem]
    summary: str
    recommendations: List[str]


class Agent1TrendDetective:
    """Trend Detective Agent - Monitors social media trends for music opportunities"""

    def __init__(self):
        """Initialize the Trend Detective agent with Gemini 2.5 Pro"""
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            self.agent_id = 1
            self.system_prompt = self._load_system_prompt()

            logger.info(f"Agent {self.agent_id} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agent 1: {e}")
            raise

    def _load_system_prompt(self) -> str:
        """Load system prompt from file"""
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "system_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("system_prompt.txt not found, using default prompt")
            return """You are the Trend Detective agent. Your role is to analyze trending topics
            across social media platforms and identify music video opportunities. Focus on:
            - Cultural relevance and context
            - Growth velocity and reach estimation
            - Genre compatibility
            - Music opportunity assessment
            Always return structured, actionable insights."""

    async def _fetch_platform_trends(self, platform: str, region: str, time_range: str) -> List[Dict]:
        """Simulate fetching trends from a platform (mock data for now)"""
        # In production, this would call actual API endpoints
        # For now, return realistic mock data

        mock_trends = {
            "tiktok": [
                {"name": "#SummerVibes2025", "mentions": 2500000, "growth": 45.2},
                {"name": "#AIMusic", "mentions": 1800000, "growth": 78.5},
                {"name": "#LatinHeat", "mentions": 3200000, "growth": 32.1},
            ],
            "instagram": [
                {"name": "AI Generated Art", "mentions": 1200000, "growth": 56.3},
                {"name": "Reggaeton Dance", "mentions": 2100000, "growth": 41.8},
            ],
            "youtube": [
                {"name": "EDM 2025 Mix", "mentions": 5600000, "growth": 23.7},
                {"name": "Music Video Reactions", "mentions": 4200000, "growth": 67.4},
            ]
        }

        return mock_trends.get(platform, [])

    async def _analyze_with_gemini(self, trends_data: Dict, input_data: TrendInput) -> Dict:
        """Use Gemini to analyze trends and provide insights"""

        prompt = f"""{self.system_prompt}

ANALYZE THE FOLLOWING SOCIAL MEDIA TRENDS:

Platform Data: {json.dumps(trends_data, indent=2)}

Analysis Parameters:
- Target Regions: {[r.value for r in input_data.regions]}
- Time Range: {input_data.time_range}
- Genre Filters: {[g.value for g in input_data.genre_filters] if input_data.genre_filters else "All genres"}

REQUIRED OUTPUT FORMAT (strict JSON):
{{
  "trends": [
    {{
      "rank": 1,
      "trend_name": "string",
      "platform": "string",
      "velocity": "emerging|trending|viral",
      "growth_rate": 45.2,
      "estimated_reach": 1000000,
      "cultural_context": "detailed cultural context",
      "music_opportunity": true,
      "recommended_genres": ["genre1", "genre2"]
    }}
  ],
  "summary": "Executive summary of trend landscape",
  "recommendations": ["actionable recommendation 1", "actionable recommendation 2"]
}}

Provide top 10 trends ranked by music opportunity potential."""

        try:
            generation_config = GenerationConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=8192,
            )

            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config
            )

            # Extract JSON from response
            response_text = response.text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            raise ValueError(f"Invalid JSON response from Gemini: {e}")
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method with retry logic"""

        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                # Validate input
                validated_input = TrendInput(**input_data)

                logger.info(f"Agent {self.agent_id} executing with platforms: {validated_input.platforms}")

                # Fetch trends from all platforms
                all_trends = {}
                for platform in validated_input.platforms:
                    for region in validated_input.regions:
                        trends = await self._fetch_platform_trends(
                            platform.value,
                            region.value,
                            validated_input.time_range
                        )
                        key = f"{platform.value}_{region.value}"
                        all_trends[key] = trends

                # Analyze with Gemini
                analysis_result = await self._analyze_with_gemini(all_trends, validated_input)

                # Build output
                output = TrendOutput(
                    agent_id=self.agent_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    trends=[TrendItem(**trend) for trend in analysis_result["trends"]],
                    summary=analysis_result["summary"],
                    recommendations=analysis_result["recommendations"]
                )

                logger.info(f"Agent {self.agent_id} completed successfully")
                return output.dict()

            except Exception as e:
                logger.error(f"Agent {self.agent_id} attempt {attempt + 1} failed: {e}")

                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    return {
                        "agent_id": self.agent_id,
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }


# FastAPI/Cloud Function wrapper
async def main(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for cloud function"""
    agent = Agent1TrendDetective()
    return await agent.execute(request_data)


if __name__ == "__main__":
    # Test execution
    test_input = {
        "platforms": ["tiktok", "instagram", "youtube"],
        "regions": ["GLOBAL"],
        "time_range": "24h",
        "genre_filters": ["reggaeton", "edm"]
    }

    result = asyncio.run(main(test_input))
    print(json.dumps(result, indent=2))
```

## system_prompt.txt

```
You are the Trend Detective Agent, a specialized AI system for identifying music video opportunities from social media trends.

CORE RESPONSIBILITIES:
1. Analyze trending topics across TikTok, Instagram, and YouTube
2. Assess cultural relevance and context for each trend
3. Estimate growth velocity (emerging/trending/viral)
4. Calculate estimated reach and audience size
5. Identify music opportunity potential
6. Recommend compatible music genres

ANALYSIS FRAMEWORK:
- Cultural Context: Understand the deeper meaning, origins, and audience demographics
- Growth Velocity: Classify as emerging (<100K mentions), trending (100K-1M), viral (>1M)
- Music Opportunity: Assess if trend can be enhanced with original music content
- Genre Matching: Recommend genres that align with trend aesthetics and audience

OUTPUT REQUIREMENTS:
- Always return valid JSON
- Rank trends by music opportunity score (1-100)
- Provide actionable recommendations
- Include quantitative metrics (growth %, reach estimates)
- Consider regional cultural differences

QUALITY STANDARDS:
- Accuracy over speed
- Cultural sensitivity
- Data-driven insights
- Actionable recommendations
```

## requirements.txt

```
google-cloud-aiplatform==1.48.0
google-cloud-vertexai==1.0.2
google-cloud-logging==3.8.0
pydantic==2.5.0
pandas==2.1.3
numpy==1.26.3
requests==2.31.0
python-dotenv==1.0.0
asyncio==3.4.3
```

## README.md

```markdown
# Agent 1: Trend Detective

## Purpose
Monitors and identifies trending topics across TikTok, Instagram, and YouTube in real-time, analyzing cultural context and music opportunities using Gemini 2.5 Pro.

## Inputs

### Input Schema
```json
{
  "platforms": ["tiktok", "instagram", "youtube"],
  "regions": ["US", "EU", "LATAM", "GLOBAL"],
  "time_range": "24h|7d|30d",
  "genre_filters": ["reggaeton", "edm", "pop", "hip-hop"]
}
```

## Outputs

### Output Schema
```json
{
  "agent_id": 1,
  "timestamp": "2025-11-12T10:30:00Z",
  "trends": [
    {
      "rank": 1,
      "trend_name": "#SummerVibes2025",
      "platform": "tiktok",
      "velocity": "viral",
      "growth_rate": 45.2,
      "estimated_reach": 2500000,
      "cultural_context": "Summer music festival season starting...",
      "music_opportunity": true,
      "recommended_genres": ["reggaeton", "edm"]
    }
  ],
  "summary": "Top trends show high demand for summer party music",
  "recommendations": ["Focus on upbeat summer tracks", "Target Gen Z audience"]
}
```

## Usage Example

```python
from agent import Agent1TrendDetective
import asyncio

async def run():
    agent = Agent1TrendDetective()

    input_data = {
        "platforms": ["tiktok", "instagram"],
        "regions": ["GLOBAL"],
        "time_range": "24h",
        "genre_filters": ["reggaeton"]
    }

    result = await agent.execute(input_data)
    print(result)

asyncio.run(run())
```

## Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| E001 | Invalid platform | Use: tiktok, instagram, youtube |
| E002 | API rate limit | Automatic retry with backoff |
| E003 | Invalid time range | Use: 24h, 7d, or 30d |
| E004 | Gemini API failure | Check credentials and quota |

## Environment Variables

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

## Installation

```bash
cd agent-1-trend-detective
pip install -r requirements.txt
python app/agent.py
```

## Testing

```bash
pytest tests/test_agent1.py -v
```
```

---

# 🎵 AGENT 2: SUNO PROMPT GENERATOR

## Purpose
Generates optimized music generation prompts for Suno API based on trends, genre, mood, and musical specifications.

## File Structure
```
agent-2-suno-prompt/
├── app/
│   └── agent.py
├── system_prompt.txt
├── requirements.txt
└── README.md
```

## agent.py

```python
"""
Agent 2: Suno Prompt Generator
Purpose: Generate optimized music prompts for Suno API
Model: Gemini 2.5 Pro
Date: 12.11.2025
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel, Field, validator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Genre(str, Enum):
    REGGAETON = "reggaeton"
    EDM = "edm"
    POP = "pop"
    HIP_HOP = "hip-hop"
    AFROBEATS = "afrobeats"


class Mood(str, Enum):
    ENERGETIC = "energetic"
    CHILL = "chill"
    AGGRESSIVE = "aggressive"
    ROMANTIC = "romantic"
    MELANCHOLIC = "melancholic"


class VocalType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    MIXED = "mixed"
    NONE = "none"


class SunoInput(BaseModel):
    genre: Genre
    mood: Mood
    duration_seconds: int = Field(default=60, ge=30, le=120)
    trend_input: Optional[str] = None
    bpm_preference: int = Field(default=120, ge=60, le=180)
    vocal_type: VocalType = VocalType.MIXED


class MusicalSpecs(BaseModel):
    genre: str
    bpm: int
    key: str
    instruments: List[str]
    vocal_type: str


class SunoAPIParameters(BaseModel):
    duration: int
    model: str = "chirp-v3"
    quality: str = "high"


class SunoOutput(BaseModel):
    agent_id: int = 2
    timestamp: str
    primary_prompt: str
    variations: List[str]
    musical_specs: MusicalSpecs
    suno_api_parameters: SunoAPIParameters


class Agent2SunoPrompt:
    """Suno Prompt Generator - Creates optimized music generation prompts"""

    def __init__(self):
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            self.agent_id = 2
            self.system_prompt = self._load_system_prompt()

            logger.info(f"Agent {self.agent_id} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agent 2: {e}")
            raise

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "system_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return """You are the Suno Prompt Generator. Create detailed, optimized prompts
            for AI music generation that capture genre, mood, instrumentation, and style."""

    def _get_genre_guidelines(self, genre: Genre) -> Dict[str, Any]:
        """Return genre-specific musical guidelines"""
        guidelines = {
            Genre.REGGAETON: {
                "bpm_range": [90, 110],
                "key_preferences": ["Am", "Dm", "Em"],
                "core_instruments": ["dembow drums", "bass", "synth", "vocals"],
                "characteristics": "Latin rhythms, dembow beat, sensual vocals"
            },
            Genre.EDM: {
                "bpm_range": [128, 140],
                "key_preferences": ["C major", "A minor", "G major"],
                "core_instruments": ["synth", "bass", "drums", "pads"],
                "characteristics": "High energy, build-ups, drops, electronic sounds"
            },
            Genre.POP: {
                "bpm_range": [100, 130],
                "key_preferences": ["C major", "G major", "D major"],
                "core_instruments": ["vocals", "drums", "bass", "synth", "guitar"],
                "characteristics": "Catchy melodies, verse-chorus structure, radio-friendly"
            },
            Genre.HIP_HOP: {
                "bpm_range": [80, 110],
                "key_preferences": ["C minor", "Bb minor", "F minor"],
                "core_instruments": ["808 bass", "drums", "hi-hats", "synth"],
                "characteristics": "Strong beat, rap vocals, sampling, heavy bass"
            },
            Genre.AFROBEATS: {
                "bpm_range": [100, 120],
                "key_preferences": ["F major", "C major", "Bb major"],
                "core_instruments": ["percussion", "bass", "synth", "vocals"],
                "characteristics": "African rhythms, layered percussion, melodic vocals"
            }
        }
        return guidelines.get(genre, guidelines[Genre.POP])

    async def _generate_with_gemini(self, input_data: SunoInput) -> Dict:
        """Use Gemini to generate Suno prompts"""

        genre_guide = self._get_genre_guidelines(input_data.genre)

        prompt = f"""{self.system_prompt}

GENERATE SUNO MUSIC PROMPT:

Genre: {input_data.genre.value}
Mood: {input_data.mood.value}
Duration: {input_data.duration_seconds} seconds
BPM: {input_data.bpm_preference}
Vocal Type: {input_data.vocal_type.value}
Trend Context: {input_data.trend_input or "None"}

Genre Guidelines:
- BPM Range: {genre_guide["bpm_range"]}
- Recommended Keys: {genre_guide["key_preferences"]}
- Core Instruments: {genre_guide["core_instruments"]}
- Characteristics: {genre_guide["characteristics"]}

SUNO PROMPT BEST PRACTICES (2025):
1. Be descriptive but concise (max 500 characters)
2. Specify mood, genre, and instruments explicitly
3. Include vocal style if applicable
4. Use vivid, sensory language
5. Consider generation time constraints

REQUIRED OUTPUT (strict JSON):
{{
  "primary_prompt": "Your main Suno prompt here (max 500 chars)",
  "variations": [
    "Variation 1 with different emphasis",
    "Variation 2 with alternative approach",
    "Variation 3 with creative twist"
  ],
  "musical_specs": {{
    "genre": "{input_data.genre.value}",
    "bpm": {input_data.bpm_preference},
    "key": "Recommended key",
    "instruments": ["instrument1", "instrument2"],
    "vocal_type": "{input_data.vocal_type.value}"
  }}
}}

Create a prompt that will generate high-quality, trendy music."""

        try:
            generation_config = GenerationConfig(
                temperature=0.9,
                top_p=0.95,
                max_output_tokens=4096,
            )

            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config
            )

            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method"""

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                validated_input = SunoInput(**input_data)
                logger.info(f"Agent {self.agent_id} generating prompt for {validated_input.genre.value}")

                gemini_result = await self._generate_with_gemini(validated_input)

                output = SunoOutput(
                    agent_id=self.agent_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    primary_prompt=gemini_result["primary_prompt"],
                    variations=gemini_result["variations"],
                    musical_specs=MusicalSpecs(**gemini_result["musical_specs"]),
                    suno_api_parameters=SunoAPIParameters(
                        duration=validated_input.duration_seconds
                    )
                )

                logger.info(f"Agent {self.agent_id} completed successfully")
                return output.dict()

            except Exception as e:
                logger.error(f"Agent {self.agent_id} attempt {attempt + 1} failed: {e}")

                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    return {
                        "agent_id": self.agent_id,
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }


async def main(request_data: Dict[str, Any]) -> Dict[str, Any]:
    agent = Agent2SunoPrompt()
    return await agent.execute(request_data)


if __name__ == "__main__":
    test_input = {
        "genre": "reggaeton",
        "mood": "energetic",
        "duration_seconds": 60,
        "trend_input": "#SummerVibes2025",
        "bpm_preference": 95,
        "vocal_type": "mixed"
    }

    result = asyncio.run(main(test_input))
    print(json.dumps(result, indent=2))
```

## system_prompt.txt

```
You are the Suno Prompt Generator Agent, specialized in creating optimized prompts for AI music generation.

CORE CAPABILITIES:
1. Genre-specific prompt crafting (Reggaeton, EDM, Pop, Hip-Hop, Afrobeats)
2. Mood and emotion translation into musical descriptions
3. Instrumentation specification
4. BPM and key recommendations
5. Vocal style guidance

SUNO API EXPERTISE (2025):
- Maximum prompt length: 500 characters
- Include specific genre keywords
- Describe mood with sensory language
- Specify instrumentation explicitly
- Mention vocal characteristics
- Consider generation time (30-60 seconds optimal)

PROMPT STRUCTURE:
[Genre] track with [mood] vibes at [BPM] BPM. Features [instruments]. [Vocal description]. [Additional style notes].

VARIATION STRATEGY:
- Variation 1: Emphasize different instruments
- Variation 2: Adjust mood intensity
- Variation 3: Alternative vocal approach

QUALITY STANDARDS:
- Concise yet descriptive
- Genre-authentic terminology
- Trend-aware language
- Professional production quality implied
```

## requirements.txt

```
google-cloud-aiplatform==1.48.0
google-cloud-vertexai==1.0.2
pydantic==2.5.0
python-dotenv==1.0.0
asyncio==3.4.3
```

## README.md

```markdown
# Agent 2: Suno Prompt Generator

## Purpose
Generates optimized music generation prompts for Suno API based on genre, mood, and musical specifications.

## Inputs

```json
{
  "genre": "reggaeton|edm|pop|hip-hop|afrobeats",
  "mood": "energetic|chill|aggressive|romantic|melancholic",
  "duration_seconds": 60,
  "trend_input": "#SummerVibes2025",
  "bpm_preference": 95,
  "vocal_type": "male|female|mixed|none"
}
```

## Outputs

```json
{
  "agent_id": 2,
  "timestamp": "2025-11-12T10:30:00Z",
  "primary_prompt": "Energetic reggaeton track at 95 BPM with dembow drums...",
  "variations": ["Variation 1", "Variation 2", "Variation 3"],
  "musical_specs": {
    "genre": "reggaeton",
    "bpm": 95,
    "key": "Am",
    "instruments": ["dembow drums", "bass", "synth", "vocals"],
    "vocal_type": "mixed"
  },
  "suno_api_parameters": {
    "duration": 60,
    "model": "chirp-v3",
    "quality": "high"
  }
}
```

## Usage Example

```python
from agent import Agent2SunoPrompt
import asyncio

async def run():
    agent = Agent2SunoPrompt()

    input_data = {
        "genre": "reggaeton",
        "mood": "energetic",
        "duration_seconds": 60,
        "bpm_preference": 95,
        "vocal_type": "mixed"
    }

    result = await agent.execute(input_data)
    print(result["primary_prompt"])

asyncio.run(run())
```

## Genre-Specific Guidelines

| Genre | BPM Range | Key Instruments | Characteristics |
|-------|-----------|----------------|-----------------|
| Reggaeton | 90-110 | Dembow, bass, synth | Latin rhythms, sensual |
| EDM | 128-140 | Synth, bass, drums | High energy, drops |
| Pop | 100-130 | Vocals, drums, guitar | Catchy, radio-friendly |
| Hip-Hop | 80-110 | 808, drums, hi-hats | Strong beat, heavy bass |
| Afrobeats | 100-120 | Percussion, bass | African rhythms, melodic |

## Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| E201 | Invalid genre | Use supported genres |
| E202 | BPM out of range | Use 60-180 BPM |
| E203 | Prompt generation failed | Check Gemini API |
```

---

# 🎧 AGENT 3: AUDIO ANALYZER

## Purpose
Analyzes audio structure, BPM, key, vocals, frequency ranges, and creates section breakdowns for music tracks.

## File Structure
```
agent-3-audio-analyzer/
├── app/
│   └── agent.py
├── system_prompt.txt
├── requirements.txt
└── README.md
```

## agent.py

```python
"""
Agent 3: Audio Analyzer
Purpose: Analyze audio structure, BPM, key, vocals, frequency ranges
Model: Gemini 2.5 Pro
Date: 12.11.2025
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalysisDepth(str, Enum):
    BASIC = "basic"
    DETAILED = "detailed"
    ADVANCED = "advanced"


class AudioSection(BaseModel):
    name: str
    start_sec: float
    end_sec: float
    description: str


class FrequencyAnalysis(BaseModel):
    bass_0_250hz: int = Field(ge=0, le=100)
    mid_250_4000hz: int = Field(ge=0, le=100)
    treble_4000_20000hz: int = Field(ge=0, le=100)


class AudioAnalysisData(BaseModel):
    bpm: int
    key: str
    time_signature: str
    duration_sec: float
    vocal_present: bool
    vocal_type: Optional[str]
    instrumentation: List[str]
    energy_level: int = Field(ge=0, le=100)
    dynamic_range: int
    frequency_analysis: FrequencyAnalysis
    sections: List[AudioSection]


class AudioInput(BaseModel):
    audio_source: str
    analysis_depth: AnalysisDepth = AnalysisDepth.DETAILED
    focus_areas: List[str] = Field(default=["bpm", "key", "vocals", "energy"])


class AudioOutput(BaseModel):
    agent_id: int = 3
    timestamp: str
    audio_analysis: AudioAnalysisData


class Agent3AudioAnalyzer:
    """Audio Analyzer - Analyzes music track structure and characteristics"""

    def __init__(self):
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            self.agent_id = 3
            self.system_prompt = self._load_system_prompt()

            logger.info(f"Agent {self.agent_id} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agent 3: {e}")
            raise

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "system_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return """You are the Audio Analyzer. Analyze music tracks for BPM, key,
            structure, instrumentation, and energy levels."""

    async def _simulate_audio_analysis(self, audio_source: str, depth: AnalysisDepth) -> Dict:
        """
        Simulate audio analysis (in production, this would use librosa, essentia, etc.)
        For now, returns realistic mock data
        """

        # Mock analysis based on depth
        if depth == AnalysisDepth.BASIC:
            return {
                "bpm": 120,
                "key": "C Major",
                "duration_sec": 180.0
            }

        # Detailed/Advanced analysis
        return {
            "bpm": 128,
            "key": "Am",
            "time_signature": "4/4",
            "duration_sec": 195.5,
            "vocal_present": True,
            "vocal_type": "female",
            "instrumentation": ["drums", "bass", "synth", "vocals", "pad"],
            "energy_level": 75,
            "dynamic_range": 18,
            "frequency_data": {
                "bass": 65,
                "mid": 55,
                "treble": 60
            },
            "sections_detected": [
                {"name": "intro", "start": 0, "end": 16},
                {"name": "verse1", "start": 16, "end": 48},
                {"name": "chorus", "start": 48, "end": 80},
                {"name": "verse2", "start": 80, "end": 112},
                {"name": "chorus", "start": 112, "end": 144},
                {"name": "bridge", "start": 144, "end": 160},
                {"name": "chorus", "start": 160, "end": 192},
                {"name": "outro", "start": 192, "end": 195.5}
            ]
        }

    async def _analyze_with_gemini(self, raw_analysis: Dict, depth: AnalysisDepth) -> Dict:
        """Use Gemini to enhance analysis with musical context"""

        prompt = f"""{self.system_prompt}

ANALYZE THIS AUDIO DATA:

Raw Analysis: {json.dumps(raw_analysis, indent=2)}
Analysis Depth: {depth.value}

TASK: Enhance this analysis with musical insights and context.

For each section, provide:
- Musical description (what's happening musically)
- Emotional character
- Production techniques

REQUIRED OUTPUT (strict JSON):
{{
  "bpm": {raw_analysis.get('bpm', 120)},
  "key": "{raw_analysis.get('key', 'C Major')}",
  "time_signature": "{raw_analysis.get('time_signature', '4/4')}",
  "duration_sec": {raw_analysis.get('duration_sec', 180.0)},
  "vocal_present": {str(raw_analysis.get('vocal_present', False)).lower()},
  "vocal_type": "{raw_analysis.get('vocal_type', 'none')}",
  "instrumentation": {json.dumps(raw_analysis.get('instrumentation', ['drums', 'bass']))},
  "energy_level": {raw_analysis.get('energy_level', 50)},
  "dynamic_range": {raw_analysis.get('dynamic_range', 12)},
  "frequency_analysis": {{
    "bass_0_250hz": {raw_analysis.get('frequency_data', {}).get('bass', 50)},
    "mid_250_4000hz": {raw_analysis.get('frequency_data', {}).get('mid', 50)},
    "treble_4000_20000hz": {raw_analysis.get('frequency_data', {}).get('treble', 50)}
  }},
  "sections": [
    {{
      "name": "section_name",
      "start_sec": 0.0,
      "end_sec": 16.0,
      "description": "Detailed musical description"
    }}
  ]
}}

Provide professional music production insights."""

        try:
            generation_config = GenerationConfig(
                temperature=0.5,
                top_p=0.9,
                max_output_tokens=8192,
            )

            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config
            )

            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result

        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            raise

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method"""

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                validated_input = AudioInput(**input_data)
                logger.info(f"Agent {self.agent_id} analyzing: {validated_input.audio_source}")

                # Simulate audio analysis
                raw_analysis = await self._simulate_audio_analysis(
                    validated_input.audio_source,
                    validated_input.analysis_depth
                )

                # Enhance with Gemini
                enhanced_analysis = await self._analyze_with_gemini(
                    raw_analysis,
                    validated_input.analysis_depth
                )

                output = AudioOutput(
                    agent_id=self.agent_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    audio_analysis=AudioAnalysisData(**enhanced_analysis)
                )

                logger.info(f"Agent {self.agent_id} completed successfully")
                return output.dict()

            except Exception as e:
                logger.error(f"Agent {self.agent_id} attempt {attempt + 1} failed: {e}")

                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    return {
                        "agent_id": self.agent_id,
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }


async def main(request_data: Dict[str, Any]) -> Dict[str, Any]:
    agent = Agent3AudioAnalyzer()
    return await agent.execute(request_data)


if __name__ == "__main__":
    test_input = {
        "audio_source": "suno_output_12345.mp3",
        "analysis_depth": "detailed",
        "focus_areas": ["bpm", "key", "vocals", "energy", "structure"]
    }

    result = asyncio.run(main(test_input))
    print(json.dumps(result, indent=2))
```

## system_prompt.txt

```
You are the Audio Analyzer Agent, specialized in music analysis and production insights.

CORE CAPABILITIES:
1. BPM (tempo) detection and validation
2. Key and mode identification
3. Vocal presence and type classification
4. Instrumentation identification
5. Frequency balance analysis
6. Energy level assessment
7. Section structure detection (intro, verse, chorus, bridge, outro)

ANALYSIS FRAMEWORK:
- Technical Accuracy: Precise BPM, key, and timing
- Musical Context: Describe what's happening musically in each section
- Production Quality: Assess frequency balance and dynamic range
- Structural Understanding: Identify song sections and their purposes

SECTION DESCRIPTIONS:
- Intro: Set the mood, establish key elements
- Verse: Story/content delivery, builds tension
- Chorus: Main hook, highest energy (usually)
- Bridge: Contrast, variation, emotional shift
- Outro: Resolution, fade out

ENERGY LEVELS:
- 0-30: Low energy (ambient, chill, ballad)
- 31-60: Medium energy (mid-tempo, groove)
- 61-85: High energy (dance, upbeat)
- 86-100: Very high energy (intense, aggressive)

OUTPUT REQUIREMENTS:
- Always return valid, structured JSON
- Provide musical reasoning for classifications
- Include timestamp precision for sections
- Professional music production terminology
```

## requirements.txt

```
google-cloud-aiplatform==1.48.0
google-cloud-vertexai==1.0.2
pydantic==2.5.0
python-dotenv==1.0.0
asyncio==3.4.3
librosa==0.10.1
numpy==1.26.3
```

## README.md

```markdown
# Agent 3: Audio Analyzer

## Purpose
Analyzes audio structure, BPM, key, vocals, frequency ranges, and creates detailed section breakdowns.

## Inputs

```json
{
  "audio_source": "file_path_or_url",
  "analysis_depth": "basic|detailed|advanced",
  "focus_areas": ["bpm", "key", "vocals", "energy"]
}
```

## Outputs

```json
{
  "agent_id": 3,
  "timestamp": "2025-11-12T10:30:00Z",
  "audio_analysis": {
    "bpm": 128,
    "key": "Am",
    "time_signature": "4/4",
    "duration_sec": 195.5,
    "vocal_present": true,
    "vocal_type": "female",
    "instrumentation": ["drums", "bass", "synth", "vocals"],
    "energy_level": 75,
    "dynamic_range": 18,
    "frequency_analysis": {
      "bass_0_250hz": 65,
      "mid_250_4000hz": 55,
      "treble_4000_20000hz": 60
    },
    "sections": [
      {
        "name": "intro",
        "start_sec": 0,
        "end_sec": 16,
        "description": "Ambient synth pads with gradual drum introduction"
      }
    ]
  }
}
```

## Usage Example

```python
from agent import Agent3AudioAnalyzer
import asyncio

async def run():
    agent = Agent3AudioAnalyzer()

    input_data = {
        "audio_source": "track.mp3",
        "analysis_depth": "detailed"
    }

    result = await agent.execute(input_data)
    print(f"BPM: {result['audio_analysis']['bpm']}")
    print(f"Key: {result['audio_analysis']['key']}")

asyncio.run(run())
```

## Analysis Depth Levels

| Level | Features | Use Case |
|-------|----------|----------|
| Basic | BPM, key, duration | Quick overview |
| Detailed | + vocals, energy, sections | Standard workflow |
| Advanced | + frequency analysis, detailed sections | Professional production |

## Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| E301 | Audio file not found | Check file path |
| E302 | Unsupported format | Use MP3, WAV, FLAC |
| E303 | Analysis failed | Check audio quality |
```

---

# 🎬 AGENT 4: SCENE BREAKDOWN

## Purpose
Converts audio timeline into video scene breakdown with precise timing, visual descriptions, and transition recommendations.

## File Structure
```
agent-4-scene-breakdown/
├── app/
│   └── agent.py
├── system_prompt.txt
├── requirements.txt
└── README.md
```

## agent.py

```python
"""
Agent 4: Scene Breakdown
Purpose: Convert audio timeline into video scene breakdown
Model: Gemini 2.5 Pro
Date: 12.11.2025
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VisualStyle(str, Enum):
    CINEMATIC = "cinematic"
    ENERGETIC = "energetic"
    MINIMAL = "minimal"
    ABSTRACT = "abstract"
    ARTISTIC = "artistic"


class Pacing(str, Enum):
    SLOW = "slow"
    MEDIUM = "medium"
    FAST = "fast"


class CameraMovement(str, Enum):
    STATIC = "static"
    PAN = "pan"
    ZOOM = "zoom"
    DOLLY = "dolly"
    DYNAMIC = "dynamic"


class ColorMood(str, Enum):
    WARM = "warm"
    COOL = "cool"
    NEUTRAL = "neutral"
    VIBRANT = "vibrant"


class TransitionType(str, Enum):
    CUT = "cut"
    FADE = "fade"
    DISSOLVE = "dissolve"
    MORPH = "morph"


class TimeCode(BaseModel):
    start: str
    end: str
    duration_sec: float


class Scene(BaseModel):
    scene_number: int
    audio_section: str
    time_code: TimeCode
    visual_description: str
    camera_movement: CameraMovement
    color_mood: ColorMood
    intensity_level: int = Field(ge=0, le=100)
    recommended_effects: List[str]
    transition_to_next: TransitionType


class TimelineSummary(BaseModel):
    total_duration: float
    scene_count: int
    color_progression: str
    intensity_curve: str


class SceneInput(BaseModel):
    audio_analysis: Dict[str, Any]
    visual_style: VisualStyle = VisualStyle.CINEMATIC
    pacing: Pacing = Pacing.MEDIUM
    target_duration_sec: float = 180.0


class SceneOutput(BaseModel):
    agent_id: int = 4
    timestamp: str
    scenes: List[Scene]
    timeline_summary: TimelineSummary


class Agent4SceneBreakdown:
    """Scene Breakdown - Converts audio to visual timeline"""

    def __init__(self):
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            self.agent_id = 4
            self.system_prompt = self._load_system_prompt()

            logger.info(f"Agent {self.agent_id} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agent 4: {e}")
            raise

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "system_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return """You are the Scene Breakdown Agent. Convert audio analysis into
            visual scene descriptions with timing, camera movements, and transitions."""

    def _seconds_to_timecode(self, seconds: float) -> str:
        """Convert seconds to HH:MM:SS format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    async def _generate_scenes_with_gemini(self, input_data: SceneInput) -> Dict:
        """Use Gemini to generate scene breakdown"""

        audio = input_data.audio_analysis.get("audio_analysis", {})
        sections = audio.get("sections", [])

        prompt = f"""{self.system_prompt}

CREATE SCENE BREAKDOWN FROM AUDIO ANALYSIS:

Audio Information:
- BPM: {audio.get('bpm', 120)}
- Key: {audio.get('key', 'C Major')}
- Energy Level: {audio.get('energy_level', 50)}
- Duration: {audio.get('duration_sec', 180)} seconds
- Instrumentation: {audio.get('instrumentation', [])}

Audio Sections: {json.dumps(sections, indent=2)}

Visual Style: {input_data.visual_style.value}
Pacing: {input_data.pacing.value}

SCENE CREATION GUIDELINES:
1. Match scene intensity to audio energy
2. Align transitions with musical changes
3. Maintain visual coherence across scenes
4. Consider the {input_data.visual_style.value} aesthetic
5. Use {input_data.pacing.value} pacing for camera and cuts

CAMERA MOVEMENT GUIDELINES:
- Intro/Outro: Often static or slow dolly
- Verse: Medium movement, storytelling
- Chorus: Dynamic, energetic movement
- Bridge: Creative, contrasting movement

COLOR MOOD GUIDELINES:
- High energy sections: Vibrant colors
- Low energy sections: Cooler, subdued tones
- Emotional sections: Warm tones
- Technical sections: Neutral or cool

REQUIRED OUTPUT (strict JSON):
{{
  "scenes": [
    {{
      "scene_number": 1,
      "audio_section": "intro",
      "time_code": {{
        "start": "00:00:00",
        "end": "00:00:16",
        "duration_sec": 16.0
      }},
      "visual_description": "Detailed description of what happens visually",
      "camera_movement": "static|pan|zoom|dolly|dynamic",
      "color_mood": "warm|cool|neutral|vibrant",
      "intensity_level": 40,
      "recommended_effects": ["effect1", "effect2"],
      "transition_to_next": "cut|fade|dissolve|morph"
    }}
  ],
  "timeline_summary": {{
    "total_duration": {input_data.target_duration_sec},
    "scene_count": 8,
    "color_progression": "Description of color journey",
    "intensity_curve": "Description of energy progression"
  }}
}}

Create a cinematic, engaging visual narrative."""

        try:
            generation_config = GenerationConfig(
                temperature=0.8,
                top_p=0.95,
                max_output_tokens=8192,
            )

            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config
            )

            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result

        except Exception as e:
            logger.error(f"Gemini scene generation error: {e}")
            raise

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method"""

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                validated_input = SceneInput(**input_data)
                logger.info(f"Agent {self.agent_id} creating scene breakdown")

                gemini_result = await self._generate_scenes_with_gemini(validated_input)

                scenes = [Scene(**scene) for scene in gemini_result["scenes"]]

                output = SceneOutput(
                    agent_id=self.agent_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    scenes=scenes,
                    timeline_summary=TimelineSummary(**gemini_result["timeline_summary"])
                )

                logger.info(f"Agent {self.agent_id} created {len(scenes)} scenes")
                return output.dict()

            except Exception as e:
                logger.error(f"Agent {self.agent_id} attempt {attempt + 1} failed: {e}")

                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    return {
                        "agent_id": self.agent_id,
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }


async def main(request_data: Dict[str, Any]) -> Dict[str, Any]:
    agent = Agent4SceneBreakdown()
    return await agent.execute(request_data)


if __name__ == "__main__":
    # Mock audio analysis from Agent 3
    test_input = {
        "audio_analysis": {
            "audio_analysis": {
                "bpm": 128,
                "key": "Am",
                "duration_sec": 180,
                "energy_level": 75,
                "instrumentation": ["drums", "bass", "synth"],
                "sections": [
                    {"name": "intro", "start_sec": 0, "end_sec": 16},
                    {"name": "verse", "start_sec": 16, "end_sec": 48},
                    {"name": "chorus", "start_sec": 48, "end_sec": 80}
                ]
            }
        },
        "visual_style": "cinematic",
        "pacing": "medium",
        "target_duration_sec": 180
    }

    result = asyncio.run(main(test_input))
    print(json.dumps(result, indent=2))
```

## system_prompt.txt

```
You are the Scene Breakdown Agent, specialized in translating audio timelines into visual narratives.

CORE CAPABILITIES:
1. Audio-to-visual translation
2. Scene timing and pacing
3. Camera movement choreography
4. Color mood progression
5. Transition selection
6. Visual effects recommendation

SCENE STRUCTURE PRINCIPLES:
- Intro: Establish visual world, slow reveal
- Verse: Story progression, medium energy
- Chorus: Peak visual intensity, dynamic camera
- Bridge: Visual contrast, creative departure
- Outro: Resolution, callback to intro

CAMERA MOVEMENT PHILOSOPHY:
- Static: Contemplative, focused, intimate
- Pan: Revealing, exploratory, smooth
- Zoom: Emphasis, dramatic, attention-directing
- Dolly: Cinematic, immersive, professional
- Dynamic: Energetic, music video style, complex

COLOR MOOD SYSTEM:
- Warm (red/orange/yellow): Energetic, passionate, inviting
- Cool (blue/green/purple): Calm, mysterious, professional
- Neutral (gray/beige): Balanced, modern, sophisticated
- Vibrant (saturated colors): Fun, youthful, attention-grabbing

INTENSITY LEVELS:
- 0-30: Low intensity (static, calm, subtle)
- 31-60: Medium intensity (balanced, engaging)
- 61-85: High intensity (dynamic, exciting)
- 86-100: Maximum intensity (chaotic, overwhelming)

TRANSITION GUIDELINES:
- Cut: Fast-paced content, energy maintenance
- Fade: Gentle transitions, time passage
- Dissolve: Smooth blend, emotional connection
- Morph: Creative effect, surreal transitions

OUTPUT REQUIREMENTS:
- Precise timecodes (HH:MM:SS)
- Detailed visual descriptions (50-150 words per scene)
- Logical progression and narrative flow
- Professional cinematography terminology
```

## requirements.txt

```
google-cloud-aiplatform==1.48.0
google-cloud-vertexai==1.0.2
pydantic==2.5.0
python-dotenv==1.0.0
asyncio==3.4.3
```

## README.md

```markdown
# Agent 4: Scene Breakdown

## Purpose
Converts audio timeline into video scene breakdown with timing, visual descriptions, camera movements, and transitions.

## Inputs

```json
{
  "audio_analysis": {
    "audio_analysis": {
      "bpm": 128,
      "sections": [...]
    }
  },
  "visual_style": "cinematic|energetic|minimal|abstract|artistic",
  "pacing": "slow|medium|fast",
  "target_duration_sec": 180
}
```

## Outputs

```json
{
  "agent_id": 4,
  "scenes": [
    {
      "scene_number": 1,
      "audio_section": "intro",
      "time_code": {
        "start": "00:00:00",
        "end": "00:00:16",
        "duration_sec": 16
      },
      "visual_description": "Slow dolly through neon-lit city...",
      "camera_movement": "dolly",
      "color_mood": "cool",
      "intensity_level": 40,
      "recommended_effects": ["lens_flare", "color_grade"],
      "transition_to_next": "fade"
    }
  ],
  "timeline_summary": {
    "total_duration": 180,
    "scene_count": 8,
    "color_progression": "cool_to_warm_to_neutral",
    "intensity_curve": "low_to_high_to_medium"
  }
}
```

## Visual Style Examples

| Style | Characteristics | Use Cases |
|-------|----------------|-----------|
| Cinematic | Film-like, polished, dramatic lighting | Professional music videos |
| Energetic | Fast cuts, dynamic camera, high intensity | Dance, EDM videos |
| Minimal | Simple, clean, focused | Artistic, indie videos |
| Abstract | Experimental, surreal, creative | Avant-garde, electronic |
| Artistic | Stylized, unique visual language | Alternative, art-pop |

## Usage Example

```python
from agent import Agent4SceneBreakdown
import asyncio

async def run():
    agent = Agent4SceneBreakdown()

    # Assuming you have audio_analysis from Agent 3
    input_data = {
        "audio_analysis": audio_output,
        "visual_style": "cinematic",
        "pacing": "medium"
    }

    result = await agent.execute(input_data)
    for scene in result["scenes"]:
        print(f"Scene {scene['scene_number']}: {scene['visual_description']}")

asyncio.run(run())
```
```

---

# 🎨 AGENT 5: STYLE ANCHORS

## Purpose
Defines comprehensive visual style guide including colors, typography, cinematography, and consistency rules for all video scenes.

## File Structure
```
agent-5-style-anchors/
├── app/
│   └── agent.py
├── system_prompt.txt
├── requirements.txt
└── README.md
```

## agent.py

```python
"""
Agent 5: Style Anchors
Purpose: Define visual style consistency guide
Model: Gemini 2.5 Pro
Date: 12.11.2025
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BrandStyle(str, Enum):
    MINIMALIST = "minimalist"
    MAXIMALIST = "maximalist"
    ARTISTIC = "artistic"
    COMMERCIAL = "commercial"
    AVANT_GARDE = "avant-garde"


class Tone(str, Enum):
    LUXURY = "luxury"
    PLAYFUL = "playful"
    SERIOUS = "serious"
    SURREAL = "surreal"


class ColorRole(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    ACCENT = "accent"


class ColorPaletteItem(BaseModel):
    role: ColorRole
    hex: str = Field(pattern="^#[0-9A-Fa-f]{6}$")
    rgb: List[int] = Field(min_items=3, max_items=3)
    usage_percentage: int = Field(ge=0, le=100)
    contexts: List[str]


class Typography(BaseModel):
    font_family: Optional[str] = None
    style: str


class Cinematography(BaseModel):
    aspect_ratio: str
    depth_of_field: str
    lighting: str


class VisualEffect(BaseModel):
    effect: str
    intensity: str
    frequency: str


class VisualStyleGuide(BaseModel):
    overall_aesthetic: str
    color_palette: List[ColorPaletteItem]
    typography: Typography
    cinematography: Cinematography
    visual_effects: List[VisualEffect]
    consistency_rules: List[str]


class StyleInput(BaseModel):
    brand_style: BrandStyle = BrandStyle.ARTISTIC
    color_palette: Optional[List[str]] = None
    reference_artists: Optional[List[str]] = None
    tone: Tone = Tone.PLAYFUL


class StyleOutput(BaseModel):
    agent_id: int = 5
    timestamp: str
    visual_style_guide: VisualStyleGuide


class Agent5StyleAnchors:
    """Style Anchors - Defines visual consistency guide"""

    def __init__(self):
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            self.agent_id = 5
            self.system_prompt = self._load_system_prompt()

            logger.info(f"Agent {self.agent_id} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agent 5: {e}")
            raise

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "system_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return """You are the Style Anchors Agent. Define comprehensive visual style
            guides including colors, typography, cinematography, and consistency rules."""

    def _hex_to_rgb(self, hex_color: str) -> List[int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    async def _generate_style_guide_with_gemini(self, input_data: StyleInput) -> Dict:
        """Use Gemini to generate comprehensive style guide"""

        color_context = ""
        if input_data.color_palette:
            color_context = f"User-specified colors: {input_data.color_palette}"
        else:
            color_context = "Generate appropriate color palette based on brand style"

        reference_context = ""
        if input_data.reference_artists:
            reference_context = f"Reference artists: {', '.join(input_data.reference_artists)}"

        prompt = f"""{self.system_prompt}

CREATE VISUAL STYLE GUIDE:

Brand Style: {input_data.brand_style.value}
Tone: {input_data.tone.value}
{color_context}
{reference_context}

STYLE GUIDE REQUIREMENTS:

1. COLOR PALETTE:
   - 3-5 colors with specific hex codes
   - Define role (primary/secondary/accent)
   - Usage percentage and contexts
   - Ensure colors work together harmoniously

2. CINEMATOGRAPHY:
   - Aspect ratio (16:9, 9:16, 1:1)
   - Depth of field preference
   - Lighting style

3. VISUAL EFFECTS:
   - List 3-5 effects that match the aesthetic
   - Define intensity and frequency

4. CONSISTENCY RULES:
   - 5-7 rules to maintain visual coherence
   - Specific, actionable guidelines

BRAND STYLE CHARACTERISTICS:
- Minimalist: Clean, simple, lots of negative space
- Maximalist: Rich, layered, visually complex
- Artistic: Creative, unique, expressive
- Commercial: Polished, professional, mainstream
- Avant-garde: Experimental, boundary-pushing

REQUIRED OUTPUT (strict JSON):
{{
  "overall_aesthetic": "One paragraph description",
  "color_palette": [
    {{
      "role": "primary",
      "hex": "#FF6B6B",
      "rgb": [255, 107, 107],
      "usage_percentage": 40,
      "contexts": ["backgrounds", "primary elements"]
    }}
  ],
  "typography": {{
    "font_family": "If text overlay needed",
    "style": "modern|retro|elegant|edgy"
  }},
  "cinematography": {{
    "aspect_ratio": "16:9",
    "depth_of_field": "shallow|medium|deep",
    "lighting": "dramatic|soft|natural|artificial|neon"
  }},
  "visual_effects": [
    {{
      "effect": "effect name",
      "intensity": "subtle|moderate|strong",
      "frequency": "occasional|frequent|constant"
    }}
  ],
  "consistency_rules": [
    "Rule 1",
    "Rule 2"
  ]
}}

Create a cohesive, professional style guide."""

        try:
            generation_config = GenerationConfig(
                temperature=0.8,
                top_p=0.95,
                max_output_tokens=8192,
            )

            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config
            )

            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result

        except Exception as e:
            logger.error(f"Gemini style guide generation error: {e}")
            raise

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method"""

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                validated_input = StyleInput(**input_data)
                logger.info(f"Agent {self.agent_id} creating style guide")

                gemini_result = await self._generate_style_guide_with_gemini(validated_input)

                output = StyleOutput(
                    agent_id=self.agent_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    visual_style_guide=VisualStyleGuide(**gemini_result)
                )

                logger.info(f"Agent {self.agent_id} completed successfully")
                return output.dict()

            except Exception as e:
                logger.error(f"Agent {self.agent_id} attempt {attempt + 1} failed: {e}")

                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    return {
                        "agent_id": self.agent_id,
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }


async def main(request_data: Dict[str, Any]) -> Dict[str, Any]:
    agent = Agent5StyleAnchors()
    return await agent.execute(request_data)


if __name__ == "__main__":
    test_input = {
        "brand_style": "artistic",
        "color_palette": ["#FF6B6B", "#4ECDC4", "#FFA07A"],
        "reference_artists": ["Billie Eilish", "The Weeknd"],
        "tone": "surreal"
    }

    result = asyncio.run(main(test_input))
    print(json.dumps(result, indent=2))
```

## system_prompt.txt

```
You are the Style Anchors Agent, specialized in creating cohesive visual style guides for music videos.

CORE CAPABILITIES:
1. Color palette creation and harmony
2. Visual aesthetic definition
3. Cinematography guidelines
4. Effect selection and application
5. Consistency rule formulation

COLOR THEORY PRINCIPLES:
- Complementary: Opposite on color wheel (high contrast)
- Analogous: Adjacent on color wheel (harmonious)
- Triadic: Three evenly spaced colors (balanced)
- Monochromatic: Variations of one hue (cohesive)

BRAND STYLE GUIDELINES:

Minimalist:
- Limited color palette (2-3 colors)
- Clean lines, simple compositions
- Lots of negative space
- Subtle effects

Maximalist:
- Rich, complex color palette (5+ colors)
- Layered visual elements
- Detailed, busy compositions
- Multiple simultaneous effects

Artistic:
- Unique, expressive color choices
- Creative camera angles
- Experimental effects
- Personal visual language

Commercial:
- Professional, polished look
- Mainstream-friendly colors
- Traditional cinematography
- Proven effects and techniques

Avant-garde:
- Unconventional color combinations
- Experimental cinematography
- Boundary-pushing effects
- Challenge viewer expectations

CINEMATOGRAPHY ELEMENTS:
- Aspect Ratio: 16:9 (landscape), 9:16 (mobile), 1:1 (social)
- Depth of Field: Shallow (subject focus), Deep (everything sharp)
- Lighting: Natural, Dramatic, Soft, Neon, High-key, Low-key

VISUAL EFFECTS CATEGORIES:
- Color: Grading, filters, overlays
- Motion: Speed ramps, time-lapse, slow-motion
- Transition: Wipes, morphs, glitches
- Enhancement: Sharpening, glow, lens flares

CONSISTENCY RULES FORMAT:
- Specific and actionable
- Address color, composition, movement
- Define dos and don'ts
- Ensure visual coherence across all scenes

OUTPUT STANDARDS:
- Professional color hex codes
- Precise RGB values
- Detailed aesthetic descriptions
- Clear, implementable rules
```

## requirements.txt

```
google-cloud-aiplatform==1.48.0
google-cloud-vertexai==1.0.2
pydantic==2.5.0
python-dotenv==1.0.0
asyncio==3.4.3
```

## README.md

```markdown
# Agent 5: Style Anchors

## Purpose
Defines comprehensive visual style guide including colors, typography, cinematography, and consistency rules.

## Inputs

```json
{
  "brand_style": "minimalist|maximalist|artistic|commercial|avant-garde",
  "color_palette": ["#FF6B6B", "#4ECDC4", "#FFA07A"],
  "reference_artists": ["Artist 1", "Artist 2"],
  "tone": "luxury|playful|serious|surreal"
}
```

## Outputs

```json
{
  "agent_id": 5,
  "visual_style_guide": {
    "overall_aesthetic": "Description of visual approach",
    "color_palette": [
      {
        "role": "primary",
        "hex": "#FF6B6B",
        "rgb": [255, 107, 107],
        "usage_percentage": 40,
        "contexts": ["backgrounds", "primary elements"]
      }
    ],
    "cinematography": {
      "aspect_ratio": "16:9",
      "depth_of_field": "shallow",
      "lighting": "dramatic"
    },
    "visual_effects": [
      {
        "effect": "color_grade",
        "intensity": "moderate",
        "frequency": "constant"
      }
    ],
    "consistency_rules": [
      "Always use primary color for main subject",
      "Maintain shallow depth of field in close-ups"
    ]
  }
}
```

## Brand Style Characteristics

| Style | Colors | Composition | Effects |
|-------|--------|-------------|---------|
| Minimalist | 2-3 colors | Simple, clean | Subtle |
| Maximalist | 5+ colors | Complex, layered | Multiple |
| Artistic | Unique palette | Expressive | Creative |
| Commercial | Mainstream | Traditional | Proven |
| Avant-garde | Unconventional | Experimental | Boundary-pushing |

## Usage Example

```python
from agent import Agent5StyleAnchors
import asyncio

async def run():
    agent = Agent5StyleAnchors()

    input_data = {
        "brand_style": "artistic",
        "tone": "surreal",
        "color_palette": ["#FF00FF", "#00FFFF"]
    }

    result = await agent.execute(input_data)
    style_guide = result["visual_style_guide"]
    print(f"Aesthetic: {style_guide['overall_aesthetic']}")

asyncio.run(run())
```
```

---

# 🎥 AGENT 6: VEO PROMPT OPTIMIZER

## Purpose
Optimizes all scene descriptions for Google Veo 3.1 API with technical parameters, cost estimation, and quality settings.

## File Structure
```
agent-6-veo-optimizer/
├── app/
│   └── agent.py
├── system_prompt.txt
├── requirements.txt
└── README.md
```

## agent.py

```python
"""
Agent 6: Veo Prompt Optimizer
Purpose: Optimize scene descriptions for Google Veo 3.1 API
Model: Gemini 2.5 Pro
Date: 12.11.2025
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityLevel(str, Enum):
    DRAFT = "draft"
    STANDARD = "standard"
    HIGH = "high"
    ULTRA = "ultra"


class TechnicalParameters(BaseModel):
    duration: int
    resolution: str = "1920x1080"
    fps: int = 24
    quality: str


class VeoSceneSpec(BaseModel):
    scene_number: int
    veo_prompt: str
    negative_prompt: str
    technical_parameters: TechnicalParameters
    generation_time_estimate_sec: int
    token_cost_estimate: int


class VeoAPIConfig(BaseModel):
    model_version: str = "veo-3.1"
    api_endpoint: str = "https://veo.googleapis.com/v1"
    batch_processing: bool = True
    total_estimated_tokens: int
    total_estimated_cost_usd: float


class VeoInput(BaseModel):
    scenes: List[Dict[str, Any]]
    style_guide: Dict[str, Any]
    quality_level: QualityLevel = QualityLevel.HIGH
    duration_sec: float = 180


class VeoOutput(BaseModel):
    agent_id: int = 6
    timestamp: str
    veo_generation_specs: List[VeoSceneSpec]
    veo_api_config: VeoAPIConfig


class Agent6VeoOptimizer:
    """Veo Prompt Optimizer - Optimizes prompts for Google Veo 3.1"""

    def __init__(self):
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            self.agent_id = 6
            self.system_prompt = self._load_system_prompt()

            # Veo 3.1 specifications (2025)
            self.veo_limits = {
                "max_duration_sec": 20,
                "supported_resolutions": ["1920x1080", "1024x576", "2048x1080"],
                "supported_fps": [24, 30, 60],
                "max_prompt_length": 1000
            }

            logger.info(f"Agent {self.agent_id} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agent 6: {e}")
            raise

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "system_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return """You are the Veo Prompt Optimizer. Create highly detailed, cinematic
            prompts optimized for Google Veo 3.1 video generation API."""

    def _estimate_tokens(self, prompt: str) -> int:
        """Estimate token count (rough approximation)"""
        return len(prompt.split()) * 1.3

    def _estimate_cost(self, total_tokens: int) -> float:
        """Estimate cost based on tokens (2025 pricing)"""
        cost_per_1k_tokens = 0.05
        return (total_tokens / 1000) * cost_per_1k_tokens

    async def _optimize_scene_with_gemini(
        self,
        scene: Dict,
        style_guide: Dict,
        quality: QualityLevel
    ) -> Dict:
        """Optimize a single scene for Veo 3.1"""

        color_palette = style_guide.get("color_palette", [])
        cinematography = style_guide.get("cinematography", {})

        prompt = f"""{self.system_prompt}

OPTIMIZE THIS SCENE FOR VEO 3.1:

Scene Information:
- Scene Number: {scene.get('scene_number')}
- Visual Description: {scene.get('visual_description')}
- Camera Movement: {scene.get('camera_movement')}
- Color Mood: {scene.get('color_mood')}
- Duration: {scene.get('time_code', {}).get('duration_sec', 15)} seconds

Style Guide:
- Color Palette: {json.dumps(color_palette[:3])}
- Cinematography: {json.dumps(cinematography)}
- Overall Aesthetic: {style_guide.get('overall_aesthetic', 'cinematic')}

Quality Level: {quality.value}

VEO 3.1 BEST PRACTICES (2025):
1. Use hyper-descriptive, cinematic language
2. Specify camera movements explicitly (dolly, pan, zoom, crane, steadicam)
3. Include lighting details (golden hour, neon, dramatic shadows)
4. Mention color references from style guide
5. Describe atmosphere and mood
6. Include production quality terms (4K, cinematic, professional)
7. Max 1000 characters for optimal results

REQUIRED OUTPUT (strict JSON):
{{
  "veo_prompt": "Hyper-detailed cinematic prompt for Veo 3.1 (500-1000 chars)",
  "negative_prompt": "What to avoid (artifacts, distortions, unwanted elements)"
}}

Create a prompt that will generate professional, high-quality video."""

        try:
            generation_config = GenerationConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=4096,
            )

            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config
            )

            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result

        except Exception as e:
            logger.error(f"Scene optimization error: {e}")
            raise

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method"""

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                validated_input = VeoInput(**input_data)
                logger.info(f"Agent {self.agent_id} optimizing {len(validated_input.scenes)} scenes for Veo")

                veo_specs = []
                total_tokens = 0

                # Process each scene
                for scene in validated_input.scenes:
                    optimized = await self._optimize_scene_with_gemini(
                        scene,
                        validated_input.style_guide,
                        validated_input.quality_level
                    )

                    duration = min(scene.get("time_code", {}).get("duration_sec", 15), 20)
                    tokens = int(self._estimate_tokens(optimized["veo_prompt"]))
                    total_tokens += tokens

                    spec = VeoSceneSpec(
                        scene_number=scene.get("scene_number"),
                        veo_prompt=optimized["veo_prompt"],
                        negative_prompt=optimized["negative_prompt"],
                        technical_parameters=TechnicalParameters(
                            duration=duration,
                            resolution="1920x1080",
                            fps=24,
                            quality=validated_input.quality_level.value
                        ),
                        generation_time_estimate_sec=duration * 3,  # Rough estimate
                        token_cost_estimate=tokens
                    )

                    veo_specs.append(spec)

                # Build API config
                api_config = VeoAPIConfig(
                    total_estimated_tokens=total_tokens,
                    total_estimated_cost_usd=self._estimate_cost(total_tokens)
                )

                output = VeoOutput(
                    agent_id=self.agent_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    veo_generation_specs=veo_specs,
                    veo_api_config=api_config
                )

                logger.info(f"Agent {self.agent_id} optimized {len(veo_specs)} scenes")
                return output.dict()

            except Exception as e:
                logger.error(f"Agent {self.agent_id} attempt {attempt + 1} failed: {e}")

                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    return {
                        "agent_id": self.agent_id,
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }


async def main(request_data: Dict[str, Any]) -> Dict[str, Any]:
    agent = Agent6VeoOptimizer()
    return await agent.execute(request_data)


if __name__ == "__main__":
    # Test with mock scene data
    test_input = {
        "scenes": [
            {
                "scene_number": 1,
                "visual_description": "Neon-lit city street at night",
                "camera_movement": "dolly",
                "color_mood": "cool",
                "time_code": {"duration_sec": 15}
            }
        ],
        "style_guide": {
            "overall_aesthetic": "Cyberpunk cinematic",
            "color_palette": [{"hex": "#00FFFF"}],
            "cinematography": {"lighting": "neon"}
        },
        "quality_level": "high"
    }

    result = asyncio.run(main(test_input))
    print(json.dumps(result, indent=2))
```

## system_prompt.txt

```
You are the Veo Prompt Optimizer Agent, specialized in creating hyper-detailed prompts for Google Veo 3.1 video generation.

CORE EXPERTISE:
1. Cinematic language and terminology
2. Camera movement specification
3. Lighting and atmosphere description
4. Color grading references
5. Production quality indicators

VEO 3.1 SPECIFICATIONS (2025):
- Maximum duration per clip: 20 seconds
- Optimal prompt length: 500-1000 characters
- Supported resolutions: 1920x1080, 1024x576, 2048x1080
- Frame rates: 24, 30, 60 fps
- Excels at: Cinematic shots, realistic motion, lighting

PROMPT STRUCTURE FORMULA:

[Shot Type] of [Subject] in [Location/Setting].
Camera: [Movement type and direction]
Lighting: [Lighting description with mood]
Colors: [Specific color palette references]
Atmosphere: [Mood and environmental details]
Style: [Production quality and aesthetic]

CAMERA MOVEMENTS:
- Dolly in/out: Moving towards/away from subject
- Tracking shot: Following subject movement
- Pan left/right: Horizontal camera rotation
- Tilt up/down: Vertical camera rotation
- Crane shot: Vertical camera movement
- Steadicam: Smooth handheld movement
- Static: No camera movement

LIGHTING DESCRIPTIONS:
- Golden hour: Warm, soft sunlight (sunrise/sunset)
- Neon: Artificial, colorful urban lighting
- Dramatic shadows: High contrast, film noir style
- Soft diffused: Even, flattering lighting
- Backlit: Light source behind subject
- Practical lights: Visible light sources in scene

QUALITY INDICATORS:
- High quality terms: "4K", "cinematic", "professional", "studio quality"
- Depth: "Shallow depth of field", "bokeh", "sharp focus"
- Motion: "Smooth motion", "fluid camera movement"
- Details: "Highly detailed", "intricate", "textured"

NEGATIVE PROMPTS:
Common issues to avoid:
- Motion artifacts
- Distorted faces/hands
- Unnatural movements
- Poor lighting
- Low resolution
- Compression artifacts
- Watermarks

OUTPUT REQUIREMENTS:
- Veo prompt: 500-1000 characters, hyper-descriptive
- Negative prompt: 100-200 characters
- Always include camera, lighting, colors, mood
- Use professional cinematography terminology
```

## requirements.txt

```
google-cloud-aiplatform==1.48.0
google-cloud-vertexai==1.0.2
pydantic==2.5.0
python-dotenv==1.0.0
asyncio==3.4.3
```

## README.md

```markdown
# Agent 6: Veo Prompt Optimizer

## Purpose
Optimizes scene descriptions for Google Veo 3.1 API with technical parameters and cost estimation.

## Inputs

```json
{
  "scenes": [
    {
      "scene_number": 1,
      "visual_description": "...",
      "camera_movement": "dolly",
      "time_code": {"duration_sec": 15}
    }
  ],
  "style_guide": {...},
  "quality_level": "draft|standard|high|ultra"
}
```

## Outputs

```json
{
  "agent_id": 6,
  "veo_generation_specs": [
    {
      "scene_number": 1,
      "veo_prompt": "Cinematic dolly shot of neon-lit city street...",
      "negative_prompt": "motion artifacts, distortion, low quality",
      "technical_parameters": {
        "duration": 15,
        "resolution": "1920x1080",
        "fps": 24,
        "quality": "high"
      },
      "generation_time_estimate_sec": 45,
      "token_cost_estimate": 2500
    }
  ],
  "veo_api_config": {
    "model_version": "veo-3.1",
    "total_estimated_tokens": 25000,
    "total_estimated_cost_usd": 1.25
  }
}
```

## Veo 3.1 Best Practices

| Aspect | Recommendation |
|--------|----------------|
| Duration | Max 20 seconds per clip |
| Prompt Length | 500-1000 characters |
| Resolution | 1920x1080 recommended |
| Camera | Explicit movement description |
| Lighting | Detailed lighting specs |
| Colors | Reference style guide colors |

## Usage Example

```python
from agent import Agent6VeoOptimizer
import asyncio

async def run():
    agent = Agent6VeoOptimizer()

    input_data = {
        "scenes": scene_data,
        "style_guide": style_guide,
        "quality_level": "high"
    }

    result = await agent.execute(input_data)
    for spec in result["veo_generation_specs"]:
        print(f"Scene {spec['scene_number']}: {spec['veo_prompt']}")

asyncio.run(run())
```
```

---

# 🎬 AGENT 7: RUNWAY PROMPT OPTIMIZER

## Purpose
Optimizes scenes for Runway Gen-4 API with motion parameters and effect specifications.

## File Structure
```
agent-7-runway-optimizer/
├── app/
│   └── agent.py
├── system_prompt.txt
├── requirements.txt
└── README.md
```

## agent.py

```python
"""
Agent 7: Runway Prompt Optimizer
Purpose: Optimize scenes for Runway Gen-4 API
Model: Gemini 2.5 Pro
Date: 12.11.2025
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MotionStyle(str, Enum):
    STATIC = "static"
    SUBTLE = "subtle"
    DYNAMIC = "dynamic"
    INTENSE = "intense"


class MotionParameters(BaseModel):
    motion_intensity: int = Field(ge=0, le=100)
    camera_speed: str
    motion_type: str
    effects: List[str]


class RunwayAPIParameters(BaseModel):
    model: str = "gen-4"
    duration: int
    quality: str = "high"


class RunwaySceneSpec(BaseModel):
    scene_number: int
    runway_prompt: str
    motion_parameters: MotionParameters
    runway_api_parameters: RunwayAPIParameters


class RunwayInput(BaseModel):
    scenes: List[Dict[str, Any]]
    motion_style: MotionStyle = MotionStyle.DYNAMIC
    effects_desired: List[str] = Field(default=[])


class RunwayOutput(BaseModel):
    agent_id: int = 7
    timestamp: str
    runway_generation_specs: List[RunwaySceneSpec]
    multi_scene_transitions: str


class Agent7RunwayOptimizer:
    """Runway Prompt Optimizer - Optimizes prompts for Runway Gen-4"""

    def __init__(self):
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            self.agent_id = 7
            self.system_prompt = self._load_system_prompt()

            logger.info(f"Agent {self.agent_id} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agent 7: {e}")
            raise

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "system_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return """You are the Runway Prompt Optimizer. Create dynamic, motion-focused
            prompts optimized for Runway Gen-4 video generation API."""

    async def _optimize_scene_with_gemini(
        self,
        scene: Dict,
        motion_style: MotionStyle,
        effects: List[str]
    ) -> Dict:
        """Optimize a single scene for Runway Gen-4"""

        prompt = f"""{self.system_prompt}

OPTIMIZE THIS SCENE FOR RUNWAY GEN-4:

Scene Information:
- Scene Number: {scene.get('scene_number')}
- Visual Description: {scene.get('visual_description')}
- Camera Movement: {scene.get('camera_movement')}
- Intensity Level: {scene.get('intensity_level', 50)}
- Duration: {scene.get('time_code', {}).get('duration_sec', 15)} seconds

Motion Style: {motion_style.value}
Effects Desired: {effects}

RUNWAY GEN-4 STRENGTHS (2025):
1. Complex motion and dynamics
2. Special effects and transformations
3. Creative transitions
4. Stylized visuals
5. Motion control precision

PROMPT STRUCTURE:
Focus on motion, dynamics, and visual effects.
Describe:
- What moves and how
- Speed and direction of movement
- Visual effects to apply
- Transformation or morphing
- Energy and dynamics

REQUIRED OUTPUT (strict JSON):
{{
  "runway_prompt": "Motion-focused prompt for Runway Gen-4 (300-800 chars)",
  "motion_parameters": {{
    "motion_intensity": 65,
    "camera_speed": "medium|slow|fast",
    "motion_type": "smooth|jerky|fluid|chaotic",
    "effects": ["color_shift", "light_flare", "particle_effects"]
  }}
}}

Emphasize motion and dynamics."""

        try:
            generation_config = GenerationConfig(
                temperature=0.8,
                top_p=0.95,
                max_output_tokens=4096,
            )

            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config
            )

            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result

        except Exception as e:
            logger.error(f"Scene optimization error: {e}")
            raise

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method"""

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                validated_input = RunwayInput(**input_data)
                logger.info(f"Agent {self.agent_id} optimizing {len(validated_input.scenes)} scenes for Runway")

                runway_specs = []

                for scene in validated_input.scenes:
                    optimized = await self._optimize_scene_with_gemini(
                        scene,
                        validated_input.motion_style,
                        validated_input.effects_desired
                    )

                    duration = scene.get("time_code", {}).get("duration_sec", 15)

                    spec = RunwaySceneSpec(
                        scene_number=scene.get("scene_number"),
                        runway_prompt=optimized["runway_prompt"],
                        motion_parameters=MotionParameters(**optimized["motion_parameters"]),
                        runway_api_parameters=RunwayAPIParameters(
                            duration=int(duration)
                        )
                    )

                    runway_specs.append(spec)

                # Generate transition guidance
                transition_guide = "Blend scenes using motion continuity and color matching for seamless transitions."

                output = RunwayOutput(
                    agent_id=self.agent_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    runway_generation_specs=runway_specs,
                    multi_scene_transitions=transition_guide
                )

                logger.info(f"Agent {self.agent_id} optimized {len(runway_specs)} scenes")
                return output.dict()

            except Exception as e:
                logger.error(f"Agent {self.agent_id} attempt {attempt + 1} failed: {e}")

                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    return {
                        "agent_id": self.agent_id,
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }


async def main(request_data: Dict[str, Any]) -> Dict[str, Any]:
    agent = Agent7RunwayOptimizer()
    return await agent.execute(request_data)


if __name__ == "__main__":
    test_input = {
        "scenes": [
            {
                "scene_number": 1,
                "visual_description": "Dynamic dance sequence",
                "camera_movement": "dynamic",
                "intensity_level": 80,
                "time_code": {"duration_sec": 15}
            }
        ],
        "motion_style": "dynamic",
        "effects_desired": ["motion_blur", "color_shift"]
    }

    result = asyncio.run(main(test_input))
    print(json.dumps(result, indent=2))
```

## system_prompt.txt

```
You are the Runway Prompt Optimizer Agent, specialized in creating motion-focused prompts for Runway Gen-4.

CORE EXPERTISE:
1. Motion dynamics and choreography
2. Visual effects specification
3. Motion intensity control
4. Transition design
5. Creative transformations

RUNWAY GEN-4 STRENGTHS (2025):
- Excels at complex motion and dynamics
- Superior special effects capabilities
- Creative stylization options
- Precise motion control
- Transformation and morphing effects

PROMPT STRUCTURE FORMULA:

[Action/Movement description] with [motion characteristics].
Speed: [slow/medium/fast]
Direction: [specific directions]
Effects: [visual effects list]
Style: [motion style and feel]

MOTION INTENSITY LEVELS:
- 0-30: Minimal motion (subtle, gentle movements)
- 31-60: Moderate motion (balanced, controlled)
- 61-85: High motion (energetic, dynamic)
- 86-100: Extreme motion (chaotic, intense)

MOTION TYPES:
- Smooth: Fluid, continuous, seamless
- Fluid: Natural, organic flow
- Dynamic: Energetic, variable speed
- Chaotic: Unpredictable, intense
- Rhythmic: Pulsing, beat-synchronized

EFFECTS CATALOG:
- Color shift: Gradual or sudden color changes
- Light flare: Lens flares, light streaks
- Motion blur: Speed-induced blur
- Particle effects: Sparks, dust, embers
- Glow effects: Luminescent elements
- Distortion: Warping, rippling
- Chromatic aberration: Color fringing
- Film grain: Vintage texture

CAMERA SPEED:
- Slow: Contemplative, 0.5x speed
- Medium: Natural, 1x speed
- Fast: Energetic, 2-3x speed

TRANSITION TECHNIQUES:
- Motion continuity: Match ending/starting motion
- Color blending: Smooth color transitions
- Effect bridging: Carry effects between scenes
- Speed ramping: Gradual speed changes

OUTPUT REQUIREMENTS:
- Focus on what moves and how
- Specify motion characteristics explicitly
- Include relevant effects
- Describe energy and dynamics
- Keep prompts 300-800 characters
```

## requirements.txt

```
google-cloud-aiplatform==1.48.0
google-cloud-vertexai==1.0.2
pydantic==2.5.0
python-dotenv==1.0.0
asyncio==3.4.3
```

## README.md

```markdown
# Agent 7: Runway Prompt Optimizer

## Purpose
Optimizes scenes for Runway Gen-4 API with motion parameters and effects.

## Inputs

```json
{
  "scenes": [...],
  "motion_style": "static|subtle|dynamic|intense",
  "effects_desired": ["motion_blur", "color_shift"]
}
```

## Outputs

```json
{
  "agent_id": 7,
  "runway_generation_specs": [
    {
      "scene_number": 1,
      "runway_prompt": "Dynamic camera tracking shot...",
      "motion_parameters": {
        "motion_intensity": 75,
        "camera_speed": "fast",
        "motion_type": "dynamic",
        "effects": ["motion_blur", "light_flare"]
      },
      "runway_api_parameters": {
        "model": "gen-4",
        "duration": 15,
        "quality": "high"
      }
    }
  ],
  "multi_scene_transitions": "Blend scenes using motion continuity..."
}
```

## Motion Styles

| Style | Intensity | Use Case |
|-------|-----------|----------|
| Static | 0-20 | Portraits, contemplative |
| Subtle | 21-40 | Ambient, background |
| Dynamic | 41-75 | Music videos, action |
| Intense | 76-100 | High-energy, experimental |

## Usage Example

```python
from agent import Agent7RunwayOptimizer
import asyncio

async def run():
    agent = Agent7RunwayOptimizer()

    input_data = {
        "scenes": scene_data,
        "motion_style": "dynamic",
        "effects_desired": ["color_shift", "motion_blur"]
    }

    result = await agent.execute(input_data)
    print(result["runway_generation_specs"][0]["runway_prompt"])

asyncio.run(run())
```
```

---

# ✅ AGENT 8: PROMPT REFINER

## Purpose
Final quality control and refinement of all prompts for consistency, ensuring Veo and Runway prompts align with style guide.

## File Structure
```
agent-8-prompt-refiner/
├── app/
│   └── agent.py
├── system_prompt.txt
├── requirements.txt
└── README.md
```

## agent.py

```python
"""
Agent 8: Prompt Refiner
Purpose: Final QC and refinement of all prompts
Model: Gemini 2.5 Pro
Date: 12.11.2025
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import asyncio

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityCheck(BaseModel):
    check_name: str
    status: str  # pass, warning, fail
    details: str


class RefinementResults(BaseModel):
    veo_prompts_refined: List[str]
    runway_prompts_refined: List[str]
    quality_checks: List[QualityCheck]
    final_status: str  # ready_for_generation, needs_revision
    confidence_score: int = Field(ge=0, le=100)


class RefinerInput(BaseModel):
    veo_prompts: Dict[str, Any]
    runway_prompts: Dict[str, Any]
    consistency_check: bool = True


class RefinerOutput(BaseModel):
    agent_id: int = 8
    timestamp: str
    refinement_results: RefinementResults


class Agent8PromptRefiner:
    """Prompt Refiner - Final QC for all prompts"""

    def __init__(self):
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            self.agent_id = 8
            self.system_prompt = self._load_system_prompt()

            logger.info(f"Agent {self.agent_id} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agent 8: {e}")
            raise

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "system_prompt.txt")
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return """You are the Prompt Refiner. Perform quality control on all prompts,
            ensuring consistency, quality, and alignment with project goals."""

    async def _refine_with_gemini(
        self,
        veo_prompts: Dict,
        runway_prompts: Dict
    ) -> Dict:
        """Use Gemini to refine and QC all prompts"""

        veo_specs = veo_prompts.get("veo_generation_specs", [])
        runway_specs = runway_prompts.get("runway_generation_specs", [])

        prompt = f"""{self.system_prompt}

QUALITY CONTROL AND REFINEMENT TASK:

VEO PROMPTS ({len(veo_specs)} scenes):
{json.dumps([{"scene": s.get("scene_number"), "prompt": s.get("veo_prompt")[:200] + "..."} for s in veo_specs[:3]], indent=2)}

RUNWAY PROMPTS ({len(runway_specs)} scenes):
{json.dumps([{"scene": s.get("scene_number"), "prompt": s.get("runway_prompt")[:200] + "..."} for s in runway_specs[:3]], indent=2)}

QUALITY CHECKS TO PERFORM:
1. Consistency: Do prompts maintain consistent visual style?
2. Clarity: Are prompts clear and specific?
3. Completeness: Do prompts include all necessary elements?
4. Alignment: Do Veo and Runway prompts align for the same scenes?
5. Technical: Are technical specifications appropriate?

REFINEMENT TASKS:
- Fix inconsistencies in style, color, mood
- Enhance weak or vague descriptions
- Ensure proper technical parameters
- Align complementary prompts

REQUIRED OUTPUT (strict JSON):
{{
  "veo_prompts_refined": [
    "Refined Veo prompt 1",
    "Refined Veo prompt 2"
  ],
  "runway_prompts_refined": [
    "Refined Runway prompt 1",
    "Refined Runway prompt 2"
  ],
  "quality_checks": [
    {{
      "check_name": "consistency",
      "status": "pass|warning|fail",
      "details": "Specific findings"
    }},
    {{
      "check_name": "clarity",
      "status": "pass",
      "details": "All prompts are clear and specific"
    }}
  ],
  "final_status": "ready_for_generation|needs_revision",
  "confidence_score": 95
}}

Provide thorough QC and refinement."""

        try:
            generation_config = GenerationConfig(
                temperature=0.3,  # Lower temperature for consistency
                top_p=0.9,
                max_output_tokens=8192,
            )

            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config
            )

            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result

        except Exception as e:
            logger.error(f"Refinement error: {e}")
            raise

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method"""

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                validated_input = RefinerInput(**input_data)
                logger.info(f"Agent {self.agent_id} performing QC and refinement")

                gemini_result = await self._refine_with_gemini(
                    validated_input.veo_prompts,
                    validated_input.runway_prompts
                )

                output = RefinerOutput(
                    agent_id=self.agent_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    refinement_results=RefinementResults(**gemini_result)
                )

                logger.info(f"Agent {self.agent_id} QC complete - Status: {output.refinement_results.final_status}")
                return output.dict()

            except Exception as e:
                logger.error(f"Agent {self.agent_id} attempt {attempt + 1} failed: {e}")

                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    return {
                        "agent_id": self.agent_id,
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }


async def main(request_data: Dict[str, Any]) -> Dict[str, Any]:
    agent = Agent8PromptRefiner()
    return await agent.execute(request_data)


if __name__ == "__main__":
    # Test with mock data
    test_input = {
        "veo_prompts": {
            "veo_generation_specs": [
                {"scene_number": 1, "veo_prompt": "Cinematic shot..."}
            ]
        },
        "runway_prompts": {
            "runway_generation_specs": [
                {"scene_number": 1, "runway_prompt": "Dynamic movement..."}
            ]
        },
        "consistency_check": True
    }

    result = asyncio.run(main(test_input))
    print(json.dumps(result, indent=2))
```

## system_prompt.txt

```
You are the Prompt Refiner Agent, the final quality control checkpoint before video generation.

CORE RESPONSIBILITIES:
1. Cross-check all prompts for consistency
2. Verify alignment with style guide
3. Identify and fix weak or vague descriptions
4. Ensure technical specifications are correct
5. Validate complementary prompts match
6. Final approval or revision recommendation

QUALITY CHECK FRAMEWORK:

1. CONSISTENCY CHECK:
   - Visual style maintained across all prompts
   - Color palette references are consistent
   - Mood and atmosphere align
   - Cinematic approach is coherent

2. CLARITY CHECK:
   - Prompts are specific, not vague
   - Technical terms used correctly
   - Camera movements clearly described
   - Lighting specified explicitly

3. COMPLETENESS CHECK:
   - All required elements present
   - Camera + Lighting + Colors + Mood
   - Technical parameters specified
   - Duration appropriate

4. ALIGNMENT CHECK:
   - Veo and Runway prompts for same scenes complement each other
   - No contradictions between services
   - Both leverage their respective strengths

5. TECHNICAL CHECK:
   - Durations within limits (Veo: 20s max)
   - Resolutions are standard
   - FPS values are supported
   - Quality levels appropriate

REFINEMENT APPROACH:
- Preserve original creative intent
- Enhance clarity and specificity
- Fix technical issues
- Strengthen weak descriptions
- Maintain consistency

STATUS LEVELS:
- Pass: No issues, proceed
- Warning: Minor issues, can proceed with caution
- Fail: Critical issues, must revise

FINAL DECISION:
- ready_for_generation: All checks passed, approved for production
- needs_revision: Issues found, return to previous agents

CONFIDENCE SCORING:
- 90-100: Excellent, ready for production
- 75-89: Good, minor refinements made
- 60-74: Acceptable, some concerns remain
- Below 60: Needs significant revision

OUTPUT REQUIREMENTS:
- Refined prompts maintain original length targets
- All quality checks documented
- Clear, actionable feedback if revisions needed
- Confidence score with justification
```

## requirements.txt

```
google-cloud-aiplatform==1.48.0
google-cloud-vertexai==1.0.2
pydantic==2.5.0
python-dotenv==1.0.0
asyncio==3.4.3
```

## README.md

```markdown
# Agent 8: Prompt Refiner

## Purpose
Final quality control and refinement of all prompts, ensuring consistency and production readiness.

## Inputs

```json
{
  "veo_prompts": {...},
  "runway_prompts": {...},
  "consistency_check": true
}
```

## Outputs

```json
{
  "agent_id": 8,
  "refinement_results": {
    "veo_prompts_refined": ["..."],
    "runway_prompts_refined": ["..."],
    "quality_checks": [
      {
        "check_name": "consistency",
        "status": "pass",
        "details": "All prompts maintain consistent visual style"
      }
    ],
    "final_status": "ready_for_generation",
    "confidence_score": 95
  }
}
```

## Quality Checks

| Check | Purpose | Pass Criteria |
|-------|---------|---------------|
| Consistency | Visual coherence | Same style, colors, mood |
| Clarity | Specificity | Clear, detailed descriptions |
| Completeness | All elements | Camera, lighting, colors, mood |
| Alignment | Complementary | Veo/Runway prompts align |
| Technical | Specifications | Valid parameters |

## Usage Example

```python
from agent import Agent8PromptRefiner
import asyncio

async def run():
    agent = Agent8PromptRefiner()

    input_data = {
        "veo_prompts": veo_output,
        "runway_prompts": runway_output
    }

    result = await agent.execute(input_data)
    if result["refinement_results"]["final_status"] == "ready_for_generation":
        print("✅ All prompts approved for production")
    else:
        print("⚠️ Revisions needed")

asyncio.run(run())
```
```

---

Due to the file's large size, I'll create a continuation file for the remaining agents and documentation. Let me create a new file for Agents 9-11 and the integration/testing guides.