â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
"""
Screenplay Generator Module for Agent 4
Specialized in writing complete screenplays for music videos.
"""

import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class ScreenplayGenerator:
    """
    Generates production-ready screenplays for music videos
    with proper screenplay formatting and structure.
    """

    SCREENPLAY_SECTIONS = [
        "title_page",
        "scene_headings",
        "action_descriptions",
        "character_descriptions",
        "dialogue",
        "transitions",
        "technical_notes"
    ]

    def __init__(self, model):
        """Initialize with Gemini model instance."""
        self.model = model

    def generate_screenplay(self, video_concepts: Dict[str, Any], 
                           veo_prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate complete screenplay for music video from concepts.

        Args:
            video_concepts: Video concepts from Agent 3
            veo_prompts: Veo prompts from VeoPromptGenerator

        Returns:
            List of screenplay sections with full content
        """
        logger.info("Generating comprehensive screenplay")

        screenplay_sections = []

        try:
            # Section 1: Title page
            screenplay_sections.append(self._generate_title_page(video_concepts))

            # Section 2: Scene headings and descriptions
            screenplay_sections.extend(self._generate_scene_sections(video_concepts, veo_prompts))

            # Section 3: Technical notes
            screenplay_sections.append(self._generate_technical_notes(video_concepts))

            # Section 4: Production notes
            screenplay_sections.append(self._generate_production_notes(video_concepts))

            logger.info(f"Generated screenplay with {len(screenplay_sections)} sections")
            return screenplay_sections

        except Exception as e:
            logger.error(f"Error generating screenplay: {e}")
            raise

    def _generate_title_page(self, video_concepts: Dict[str, Any]) -> Dict[str, str]:
        """Generate screenplay title page."""
        title = video_concepts.get("song_title", "Untitled Music Video")

        title_page = f"""MUSIC VIDEO SCREENPLAY

Title: {title}

Format: Music Video Screenplay
Duration: {video_concepts.get('duration_seconds', 'Unknown')} seconds
Genre: {video_concepts.get('genre', 'Unknown')}
Visual Style: {video_concepts.get('visual_direction', {}).get('visual_style', 'Cinematic')}

Created by: Video Production Specialist Agent 4
Generated: [TIMESTAMP]

---

CREATIVE VISION:
{video_concepts.get('visual_direction', {}).get('overall_concept', 'N/A')}

TARGET MOOD: {video_concepts.get('visual_direction', {}).get('target_mood', 'N/A')}"""

        return {
            "section_name": "Title Page",
            "section_type": "title_page",
            "content": title_page,
            "order": 1
        }

    def _generate_scene_sections(self, video_concepts: Dict[str, Any], 
                                 veo_prompts: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate scene-by-scene screenplay sections."""
        scene_sections = []
        scenes = video_concepts.get("scene_breakdown", [])

        for idx, scene in enumerate(scenes):
            scene_num = scene.get("scene_number", idx + 1)

            # Find corresponding Veo prompt
            veo_prompt = next((p for p in veo_prompts if p.get("scene_number") == scene_num), None)

            # Format as screenplay scene
            scene_content = self._format_scene_as_screenplay(scene, veo_prompt)

            scene_sections.append({
                "section_name": f"Scene {scene_num}",
                "section_type": "scene",
                "scene_number": scene_num,
                "content": scene_content,
                "order": idx + 2,
                "duration_seconds": scene.get("duration_seconds", 0),
                "visual_elements": scene.get("visual_elements", []),
                "special_effects": scene.get("special_effects", [])
            })

        return scene_sections

    def _format_scene_as_screenplay(self, scene: Dict[str, Any], 
                                    veo_prompt: Dict[str, Any] = None) -> str:
        """Format individual scene as proper screenplay text."""
        scene_num = scene.get("scene_number", 1)
        duration = scene.get("duration_seconds", 0)
        description = scene.get("description", "")
        camera_angle = scene.get("camera_angle", "")
        elements = scene.get("visual_elements", [])
        effects = scene.get("special_effects", [])

        screenplay = f"""INT./EXT. - SCENE {scene_num} - {duration}s

TIME CODE: 00:00:{scene_num:02d}

SCENE HEADING:
Scene {scene_num}: {description}

ACTION:
{description}

Visible Elements:
{self._format_list(elements)}

Camera Angle: {camera_angle}

Special Effects:
{self._format_list(effects)}"""

        if veo_prompt:
            screenplay += f"""

VEO 3 GENERATION PROMPT:
{veo_prompt.get('prompt_text', 'N/A')}"""

        return screenplay

    def _generate_technical_notes(self, video_concepts: Dict[str, Any]) -> Dict[str, str]:
        """Generate technical notes section."""
        cinematography = video_concepts.get("cinematography", {})
        production = video_concepts.get("production_notes", {})
        colors = video_concepts.get("color_palette", {})

        technical_notes = f"""CINEMATOGRAPHY SPECIFICATIONS:

Camera Techniques:
{self._format_list(cinematography.get('camera_techniques', []))}

Lighting Strategy:
{cinematography.get('lighting_strategy', 'N/A')}

Movement Style:
{cinematography.get('movement_style', 'N/A')}

Recommended Equipment:
{self._format_list(cinematography.get('recommended_equipment', []))}

COLOR PALETTE:

Primary Colors:
{self._format_list(colors.get('primary_colors', []))}

Secondary Colors:
{self._format_list(colors.get('secondary_colors', []))}

Color Psychology:
{colors.get('color_psychology', 'N/A')}

PRODUCTION REQUIREMENTS:

Complexity Level: {production.get('estimated_complexity', 'N/A').upper()}
Budget Tier: {production.get('budget_considerations', 'N/A')}
Production Timeline: {production.get('timeline_estimate', 'N/A')}

Key Challenges:
{self._format_list(production.get('key_challenges', []))}"""

        return {
            "section_name": "Technical Notes",
            "section_type": "technical_notes",
            "content": technical_notes,
            "order": 98
        }

    def _generate_production_notes(self, video_concepts: Dict[str, Any]) -> Dict[str, str]:
        """Generate production guidelines and notes."""
        production_notes = """PRODUCTION GUIDELINES:

1. PRE-PRODUCTION:
   - Review all scene breakdowns and visual directions
   - Finalize location scouts based on visual concepts
   - Coordinate with cinematography team on equipment needs
   - Plan for weather contingencies (if outdoor scenes)

2. ON SET:
   - Monitor color palette consistency
   - Ensure lighting matches cinematography specifications
   - Document alternative takes for each scene
   - Communicate with VFX team on special effects integration

3. POST-PRODUCTION:
   - Color grade according to palette specifications
   - Integrate Veo 3 generated footage where applicable
   - Apply special effects in post
   - Synchronize audio with visual timing

4. MUSIC SYNCHRONIZATION:
   - Align scene transitions with music structure
   - Time crucial visual moments with lyrical/instrumental peaks
   - Consider music tempo for motion speed and cuts

5. QUALITY ASSURANCE:
   - Review final cut against all scene specifications
   - Verify color palette consistency throughout
   - Ensure all technical requirements are met
   - Get final approval from creative director"""

        return {
            "section_name": "Production Guidelines",
            "section_type": "production_notes",
            "content": production_notes,
            "order": 99
        }

    @staticmethod
    def _format_list(items: List[str]) -> str:
        """Format list items for screenplay."""
        if not items:
            return "- None specified"
        return "
".join([f"- {item}" for item in items])

    def validate_screenplay(self, screenplay_sections: List[Dict[str, Any]]) -> bool:
        """Validate screenplay structure and completeness."""
        section_types = [s.get("section_type") for s in screenplay_sections]

        # Must have at least title and scenes
        if "title_page" not in section_types or "scene" not in section_types:
            logger.warning("Screenplay missing required sections")
            return False

        # Check each section has required fields
        for section in screenplay_sections:
            required = ["section_name", "section_type", "content"]
            if not all(field in section for field in required):
                logger.warning(f"Section missing required fields: {section.get('section_name')}")
                return False

        return True

    def export_as_pdf_ready(self, screenplay_sections: List[Dict[str, Any]]) -> str:
        """
        Export screenplay in format ready for PDF conversion.

        Args:
            screenplay_sections: Complete screenplay sections

        Returns:
            Formatted text ready for PDF
        """
        output = []

        # Sort by order
        sorted_sections = sorted(screenplay_sections, key=lambda x: x.get("order", 999))

        for section in sorted_sections:
            output.append(f"
{'='*80}
")
            output.append(f"{section.get('section_name', 'Section')}
")
            output.append(f"{'='*80}
")
            output.append(f"{section.get('content', '')}
")

        return "
".join(output)



â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
