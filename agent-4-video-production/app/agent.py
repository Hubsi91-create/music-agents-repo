â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
"""
Agent 4: Video Production Specialist (Combined Veo + Screenplay)
Vertex AI ADK Agent with dual integrated modules for video prompt generation and screenplay writing.
Production-ready implementation with full error handling and orchestration.
"""

import os
import json
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import storage
from veo_prompt_generator import VeoPromptGenerator
from screenplay_generator import ScreenplayGenerator

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
BUCKET_NAME = os.getenv("GCP_BUCKET_NAME", "video-production-bucket")

class VideoProductionSpecialist:
    """
    Dual-function agent combining Veo prompt generation and screenplay writing.
    This is ONE agent with TWO integrated modules, not two separate agents.
    """

    def __init__(self):
        """Initialize the Video Production Specialist with both modules."""
        try:
            vertexai.init(project=PROJECT_ID, location=REGION)
            self.model = GenerativeModel(MODEL_ID)
            self.storage_client = storage.Client()
            self.veo_generator = VeoPromptGenerator(self.model)
            self.screenplay_generator = ScreenplayGenerator(self.model)
            logger.info(f"Initialized VideoProductionSpecialist with {MODEL_ID}")
            logger.info("Loaded VEO prompt generator module")
            logger.info("Loaded Screenplay generator module")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}")
            raise

    def validate_concepts(self, video_concepts: dict) -> bool:
        """
        Validate video concepts from Agent 3.

        Args:
            video_concepts: Dictionary from Agent 3 output

        Returns:
            Boolean indicating validation success
        """
        required_sections = [
            "visual_direction",
            "cinematography",
            "color_palette",
            "scene_breakdown",
            "production_notes"
        ]

        for section in required_sections:
            if section not in video_concepts:
                logger.warning(f"Missing required section: {section}")
                return False

        if not video_concepts.get("scene_breakdown") or not isinstance(video_concepts["scene_breakdown"], list):
            logger.warning("scene_breakdown must be a non-empty list")
            return False

        return True

    def process_video_concepts(self, video_concepts: dict) -> dict:
        """
        Main orchestration method combining both modules.
        Takes video concepts and outputs both Veo prompts and screenplay.

        Args:
            video_concepts: Complete video concepts from Agent 3 including:
                - visual_direction
                - cinematography
                - color_palette
                - scene_breakdown
                - production_notes

        Returns:
            Dictionary with structure:
            {
                "veo_prompts": [...],
                "screenplay_sections": [...],
                "orchestration_metadata": {...}
            }
        """
        if not self.validate_concepts(video_concepts):
            raise ValueError("Invalid video concepts structure")

        logger.info("Starting dual-module production processing")

        try:
            # Module 1: Generate Veo prompts
            logger.info("Module 1/2: Generating Google Veo 3 AI video prompts...")
            veo_prompts = self.veo_generator.generate_veo_prompts(video_concepts)
            logger.info(f"Generated {len(veo_prompts)} Veo prompts")

            # Module 2: Generate screenplay
            logger.info("Module 2/2: Generating complete screenplay...")
            screenplay_sections = self.screenplay_generator.generate_screenplay(
                video_concepts,
                veo_prompts
            )
            logger.info(f"Generated screenplay with {len(screenplay_sections)} sections")

            # Combine outputs
            production_output = {
                "veo_prompts": veo_prompts,
                "screenplay_sections": screenplay_sections,
                "orchestration_metadata": {
                    "processed_at": datetime.utcnow().isoformat(),
                    "video_title": video_concepts.get("song_title", "Unknown"),
                    "total_scenes": len(video_concepts.get("scene_breakdown", [])),
                    "total_veo_prompts": len(veo_prompts),
                    "screenplay_word_count": self._count_screenplay_words(screenplay_sections),
                    "production_status": "ready_for_filming"
                }
            }

            logger.info("Production processing complete")
            return production_output

        except Exception as e:
            logger.error(f"Error during production processing: {str(e)}")
            raise

    def _count_screenplay_words(self, screenplay_sections: List[dict]) -> int:
        """Count total words in screenplay sections."""
        total_words = 0
        for section in screenplay_sections:
            if "content" in section:
                total_words += len(section["content"].split())
        return total_words

    def save_production_output(self, production_data: dict, output_prefix: str = None) -> Dict[str, str]:
        """
        Save both Veo prompts and screenplay to Cloud Storage.

        Args:
            production_data: Combined output from process_video_concepts
            output_prefix: Optional prefix for output files

        Returns:
            Dictionary with paths to saved files
        """
        if output_prefix is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            output_prefix = f"production_{timestamp}"

        saved_paths = {}

        try:
            # Save Veo prompts
            veo_filename = f"{output_prefix}_veo_prompts.json"
            veo_path = self._upload_to_storage(
                {
                    "veo_prompts": production_data["veo_prompts"],
                    "metadata": production_data["orchestration_metadata"]
                },
                veo_filename
            )
            saved_paths["veo_prompts"] = veo_path
            logger.info(f"Saved Veo prompts to {veo_path}")

            # Save screenplay
            screenplay_filename = f"{output_prefix}_screenplay.json"
            screenplay_path = self._upload_to_storage(
                {
                    "screenplay_sections": production_data["screenplay_sections"],
                    "metadata": production_data["orchestration_metadata"]
                },
                screenplay_filename
            )
            saved_paths["screenplay"] = screenplay_path
            logger.info(f"Saved screenplay to {screenplay_path}")

            # Save combined output
            combined_filename = f"{output_prefix}_combined.json"
            combined_path = self._upload_to_storage(production_data, combined_filename)
            saved_paths["combined"] = combined_path
            logger.info(f"Saved combined output to {combined_path}")

            return saved_paths

        except Exception as e:
            logger.error(f"Error saving production output: {str(e)}")
            raise

    def _upload_to_storage(self, data: dict, filename: str) -> str:
        """Upload data to Cloud Storage with fallback to local storage."""
        try:
            bucket = self.storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(filename)
            blob.upload_from_string(
                json.dumps(data, indent=2),
                content_type="application/json"
            )
            return f"gs://{BUCKET_NAME}/{filename}"
        except Exception as gcs_error:
            logger.warning(f"Could not save to Cloud Storage: {gcs_error}")
            # Fallback to local file
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return filename

    def process_batch_concepts(self, concepts_list: List[dict]) -> List[dict]:
        """
        Process multiple video concepts in batch.

        Args:
            concepts_list: List of video concepts from Agent 3

        Returns:
            List of production outputs
        """
        results = []
        for idx, concepts in enumerate(concepts_list):
            try:
                logger.info(f"Processing batch item {idx + 1}/{len(concepts_list)}")
                production_output = self.process_video_concepts(concepts)
                results.append(production_output)
            except Exception as e:
                logger.error(f"Error processing concepts {idx}: {str(e)}")
                results.append({"error": str(e), "index": idx})

        return results

    def export_for_production_team(self, production_data: dict, format: str = "json") -> str:
        """
        Export production data in formats suitable for production teams.

        Args:
            production_data: Combined production output
            format: Export format ("json", "markdown", "plaintext")

        Returns:
            Formatted export string
        """
        if format == "markdown":
            return self._export_markdown(production_data)
        elif format == "plaintext":
            return self._export_plaintext(production_data)
        else:
            return json.dumps(production_data, indent=2)

    def _export_markdown(self, production_data: dict) -> str:
        """Export as Markdown for easy sharing and documentation."""
        output = []
        output.append(f"# Video Production Brief")
        output.append(f"Generated: {production_data['orchestration_metadata']['processed_at']}
")

        output.append("## Veo 3 AI Video Prompts
")
        for idx, prompt in enumerate(production_data["veo_prompts"], 1):
            output.append(f"### Scene {idx}
")
            output.append(f"**Duration**: {prompt.get('duration_seconds', 'N/A')}s
")
            output.append(f"**Prompt**: {prompt.get('prompt_text', 'N/A')}
")
            output.append("")

        output.append("## Screenplay
")
        for section in production_data["screenplay_sections"]:
            output.append(f"### {section.get('section_name', 'Section')}
")
            output.append(f"{section.get('content', '')}
")
            output.append("")

        return "
".join(output)

    def _export_plaintext(self, production_data: dict) -> str:
        """Export as plaintext for quick reading."""
        output = []
        output.append("VIDEO PRODUCTION SPECIALIST OUTPUT")
        output.append("=" * 80)
        output.append(f"Title: {production_data['orchestration_metadata']['video_title']}")
        output.append(f"Generated: {production_data['orchestration_metadata']['processed_at']}")
        output.append(f"Status: {production_data['orchestration_metadata']['production_status']}")
        output.append("")

        output.append("VEO 3 PROMPTS:")
        output.append("-" * 40)
        for idx, prompt in enumerate(production_data["veo_prompts"], 1):
            output.append(f"
[Scene {idx}]")
            output.append(f"Duration: {prompt.get('duration_seconds', 'N/A')}s")
            output.append(f"Prompt: {prompt.get('prompt_text', 'N/A')}")

        output.append("

SCREENPLAY:")
        output.append("-" * 40)
        for section in production_data["screenplay_sections"]:
            output.append(f"
{section.get('section_name', 'Section')}")
            output.append(section.get('content', ''))

        return "
".join(output)


def main():
    """Main entry point for the agent."""
    logger.info("Starting Video Production Specialist Agent")

    try:
        agent = VideoProductionSpecialist()

        # Example usage with sample concepts from Agent 3
        sample_concepts = {
            "visual_direction": {
                "overall_concept": "A high-energy urban chase through neon-lit streets with cinematic transitions",
                "visual_style": "Modern cinematic with cyberpunk elements",
                "target_mood": "Intense, energetic, futuristic"
            },
            "cinematography": {
                "camera_techniques": ["tracking shots", "slow-motion", "match cuts"],
                "lighting_strategy": "Neon gels with high contrast",
                "movement_style": "Dynamic with fast cuts",
                "recommended_equipment": ["RED camera", "Steadicam", "Drones"]
            },
            "color_palette": {
                "primary_colors": ["#FF00FF", "#00FFFF", "#000000"],
                "secondary_colors": ["#FFFF00", "#FF0000"],
                "color_psychology": "Vibrant, stimulating, futuristic"
            },
            "scene_breakdown": [
                {
                    "scene_number": 1,
                    "duration_seconds": 15,
                    "description": "Opening pursuit scene",
                    "visual_elements": ["neon signs", "moving vehicles"],
                    "camera_angle": "Wide establishing shot",
                    "special_effects": ["motion blur", "color grading"]
                },
                {
                    "scene_number": 2,
                    "duration_seconds": 20,
                    "description": "Mid-song climax",
                    "visual_elements": ["crowds", "laser lights"],
                    "camera_angle": "Close-ups with quick cuts",
                    "special_effects": ["particle effects", "slow-motion"]
                }
            ],
            "production_notes": {
                "estimated_complexity": "high",
                "key_challenges": ["Weather", "Permits"],
                "budget_considerations": "High-budget production",
                "timeline_estimate": "3-4 weeks"
            },
            "song_title": "Neon Rush"
        }

        # Process concepts through both modules
        production_output = agent.process_video_concepts(sample_concepts)
        logger.info(f"Production output generated: {json.dumps(production_output, indent=2)}")

        # Save outputs
        saved_paths = agent.save_production_output(production_output)
        logger.info(f"Output saved to: {saved_paths}")

        # Export in different formats
        markdown_export = agent.export_for_production_team(production_output, format="markdown")
        logger.info(f"Markdown export preview:
{markdown_export[:500]}...")

        return production_output

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()



â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
