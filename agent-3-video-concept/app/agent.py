â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
"""
Agent 3: Video Concept Collaborator
Vertex AI ADK Agent for creating visual direction and storyboard concepts for music videos.
Production-ready implementation with full error handling and Google Cloud integration.
"""

import os
import json
import logging
from typing import Optional, Any
from datetime import datetime
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.agentic.tools import Tool, Runnable
from google.cloud import storage
import anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
REGION = "us-central1"
MODEL_ID = "gemini-2.5-pro"
BUCKET_NAME = os.getenv("GCP_BUCKET_NAME", "video-concepts-bucket")

class VideoConceptCollaborator:
    """Main agent class for video concept generation."""

    def __init__(self):
        """Initialize the Video Concept Collaborator agent."""
        try:
            vertexai.init(project=PROJECT_ID, location=REGION)
            self.model = GenerativeModel(MODEL_ID)
            self.storage_client = storage.Client()
            logger.info(f"Initialized VideoConceptCollaborator with model {MODEL_ID}")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}")
            raise

    def validate_input(self, song_metadata: dict) -> bool:
        """
        Validate input song metadata.

        Args:
            song_metadata: Dictionary containing song information

        Returns:
            Boolean indicating validation success
        """
        required_fields = ["title", "genre", "duration", "mood"]
        for field in required_fields:
            if field not in song_metadata:
                logger.warning(f"Missing required field: {field}")
                return False
        return True

    def generate_visual_concepts(self, song_metadata: dict) -> dict:
        """
        Generate comprehensive visual concepts for a music video.

        Args:
            song_metadata: Dictionary with keys:
                - title: Song title
                - artist: Artist name
                - genre: Music genre
                - mood: Overall mood/emotion
                - duration: Video duration in seconds
                - bpm: Beats per minute (optional)
                - lyrics_themes: Main themes in lyrics (optional)

        Returns:
            Dictionary containing visual concepts, cinematography notes, and scene breakdown
        """
        if not self.validate_input(song_metadata):
            raise ValueError("Invalid input: missing required fields")

        logger.info(f"Generating visual concepts for: {song_metadata.get('title')}")

        prompt = self._build_concept_prompt(song_metadata)

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.8,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 4096,
                }
            )

            # Parse response as JSON
            concept_data = self._parse_response(response.text)
            concept_data["generated_at"] = datetime.utcnow().isoformat()
            concept_data["song_title"] = song_metadata.get("title")

            logger.info("Successfully generated visual concepts")
            return concept_data

        except Exception as e:
            logger.error(f"Error generating concepts: {str(e)}")
            raise

    def _build_concept_prompt(self, song_metadata: dict) -> str:
        """Build the prompt for concept generation."""
        return f"""You are an expert music video director and visual conceptualizer. 
Analyze the following song metadata and create comprehensive visual concepts for a music video.

SONG METADATA:
- Title: {song_metadata.get('title', 'Unknown')}
- Artist: {song_metadata.get('artist', 'Unknown')}
- Genre: {song_metadata.get('genre', 'Unknown')}
- Mood: {song_metadata.get('mood', 'Unknown')}
- Duration: {song_metadata.get('duration', 0)} seconds
- BPM: {song_metadata.get('bpm', 'Not specified')}
- Lyrical Themes: {song_metadata.get('lyrics_themes', 'Not specified')}

Generate a JSON response with the following structure:
{{
    "visual_direction": {{
        "overall_concept": "5-7 sentence description of the video concept",
        "visual_style": "Specific visual style (e.g., cinematic, abstract, performance-based)",
        "target_mood": "Intended emotional response from viewer"
    }},
    "cinematography": {{
        "camera_techniques": ["technique1", "technique2", ...],
        "lighting_strategy": "Detailed lighting approach",
        "movement_style": "Dynamic or static, fast cuts or long takes",
        "recommended_equipment": ["equipment1", "equipment2", ...]
    }},
    "color_palette": {{
        "primary_colors": ["color1", "color2", "color3"],
        "secondary_colors": ["color4", "color5"],
        "color_psychology": "Why these colors work for this song"
    }},
    "scene_breakdown": [
        {{
            "scene_number": 1,
            "duration_seconds": 15,
            "description": "What happens in this scene",
            "visual_elements": ["element1", "element2"],
            "camera_angle": "e.g., wide shot, close-up, birds-eye",
            "special_effects": ["effect1", "effect2"]
        }}
    ],
    "production_notes": {{
        "estimated_complexity": "low/medium/high",
        "key_challenges": ["challenge1", "challenge2"],
        "budget_considerations": "Estimated budget tier",
        "timeline_estimate": "Production timeline estimate"
    }}
}}

Ensure the response is valid JSON only, with no additional text."""

    def _parse_response(self, response_text: str) -> dict:
        """Parse and validate the model response as JSON."""
        try:
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")

            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            raise

    def save_concepts(self, concepts: dict, output_path: str = None) -> str:
        """
        Save generated concepts to Cloud Storage or local file.

        Args:
            concepts: Generated concept data
            output_path: Optional custom output path

        Returns:
            Path where concepts were saved
        """
        try:
            if output_path is None:
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                output_path = f"concepts_{timestamp}.json"

            # Save to Cloud Storage if bucket is available
            try:
                bucket = self.storage_client.bucket(BUCKET_NAME)
                blob = bucket.blob(output_path)
                blob.upload_from_string(
                    json.dumps(concepts, indent=2),
                    content_type="application/json"
                )
                logger.info(f"Saved concepts to gs://{BUCKET_NAME}/{output_path}")
                return f"gs://{BUCKET_NAME}/{output_path}"
            except Exception as gcs_error:
                logger.warning(f"Could not save to Cloud Storage: {gcs_error}")
                # Fallback to local file
                with open(output_path, 'w') as f:
                    json.dump(concepts, f, indent=2)
                logger.info(f"Saved concepts to local file: {output_path}")
                return output_path

        except Exception as e:
            logger.error(f"Error saving concepts: {str(e)}")
            raise

    def process_batch(self, songs_list: list) -> list:
        """
        Process multiple songs in batch.

        Args:
            songs_list: List of song metadata dictionaries

        Returns:
            List of generated concepts
        """
        results = []
        for idx, song in enumerate(songs_list):
            try:
                logger.info(f"Processing batch item {idx + 1}/{len(songs_list)}")
                concepts = self.generate_visual_concepts(song)
                results.append(concepts)
            except Exception as e:
                logger.error(f"Error processing song {idx}: {str(e)}")
                results.append({"error": str(e), "song": song.get("title")})

        return results


def main():
    """Main entry point for the agent."""
    logger.info("Starting Video Concept Collaborator Agent")

    try:
        agent = VideoConceptCollaborator()

        # Example usage
        sample_song = {
            "title": "Neon Dreams",
            "artist": "Synthwave Collective",
            "genre": "Synthwave/Retrowave",
            "mood": "Energetic, nostalgic, mysterious",
            "duration": 240,
            "bpm": 128,
            "lyrics_themes": ["Urban landscapes", "Neon lights", "Late night drives", "Futuristic hope"]
        }

        concepts = agent.generate_visual_concepts(sample_song)
        logger.info(f"Generated concepts: {json.dumps(concepts, indent=2)}")

        saved_path = agent.save_concepts(concepts)
        logger.info(f"Concepts saved to: {saved_path}")

        return concepts

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()



â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
