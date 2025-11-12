â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
"""
VEO Prompt Generator Module for Agent 4
Specialized in generating optimized Google Veo 3 AI video generation prompts.
"""

import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class VeoPromptGenerator:
    """
    Generates production-ready prompts specifically optimized for Google Veo 3
    video generation capabilities and constraints.
    """

    def __init__(self, model):
        """Initialize with Gemini model instance."""
        self.model = model
        self.veo_token_limit = 500  # Approximate token limit per prompt
        self.supported_effects = [
            "motion_blur", "slow_motion", "fast_motion", "transitions",
            "color_grading", "particles", "lighting", "camera_movement"
        ]

    def generate_veo_prompts(self, video_concepts: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Convert video concepts into Veo 3-optimized prompts for each scene.

        Args:
            video_concepts: Complete video concept data from Agent 3

        Returns:
            List of Veo prompts, one per scene
        """
        logger.info("Generating Veo 3 prompts from concepts")

        veo_prompts = []
        scenes = video_concepts.get("scene_breakdown", [])
        cinematography = video_concepts.get("cinematography", {})
        colors = video_concepts.get("color_palette", {})

        for scene in scenes:
            try:
                veo_prompt = self._build_veo_prompt(
                    scene=scene,
                    cinematography=cinematography,
                    colors=colors,
                    overall_concepts=video_concepts.get("visual_direction", {})
                )
                veo_prompts.append(veo_prompt)
            except Exception as e:
                logger.error(f"Error generating prompt for scene {scene.get('scene_number')}: {e}")

        logger.info(f"Generated {len(veo_prompts)} Veo prompts")
        return veo_prompts

    def _build_veo_prompt(self, scene: Dict, cinematography: Dict, 
                          colors: Dict, overall_concepts: Dict) -> Dict[str, Any]:
        """
        Build individual Veo 3 prompt for a specific scene.

        Args:
            scene: Individual scene from breakdown
            cinematography: Cinematography specifications
            colors: Color palette information
            overall_concepts: Overall visual direction

        Returns:
            Veo 3 optimized prompt dictionary
        """
        scene_num = scene.get("scene_number", 1)
        duration = scene.get("duration_seconds", 10)

        # Build visual description
        visual_description = self._build_visual_description(scene, cinematography, colors)

        # Build technical specifications
        technical_specs = self._build_technical_specs(scene, cinematography, duration)

        # Combine into Veo prompt format
        veo_prompt_text = f"""{visual_description}

TECHNICAL SPECIFICATIONS:
{technical_specs}

DURATION: {duration} seconds
QUALITY: 4K, 24fps
ASPECT_RATIO: 16:9
STYLE: {overall_concepts.get('visual_style', 'cinematic')}
"""

        return {
            "scene_number": scene_num,
            "duration_seconds": duration,
            "prompt_text": veo_prompt_text.strip(),
            "visual_elements": scene.get("visual_elements", []),
            "camera_angle": scene.get("camera_angle", ""),
            "special_effects": scene.get("special_effects", []),
            "color_palette": colors.get("primary_colors", []),
            "prompt_token_count": len(veo_prompt_text.split()),
            "veo_version": "3.1",
            "confidence_score": self._calculate_prompt_confidence(veo_prompt_text)
        }

    def _build_visual_description(self, scene: Dict, cinematography: Dict, colors: Dict) -> str:
        """Build the visual description component of the Veo prompt."""
        elements = scene.get("visual_elements", [])
        camera = scene.get("camera_angle", "")
        description = scene.get("description", "")

        color_str = ", ".join(colors.get("primary_colors", [])[:3])
        techniques = ", ".join(cinematography.get("camera_techniques", [])[:3])

        visual_desc = f"""{description}

VISUAL ELEMENTS: {', '.join(elements)}
CAMERA ANGLE: {camera}
CINEMATOGRAPHY: {techniques}
COLOR SCHEME: {color_str}
LIGHTING: {cinematography.get('lighting_strategy', 'cinematic')}"""

        return visual_desc

    def _build_technical_specs(self, scene: Dict, cinematography: Dict, duration: int) -> str:
        """Build technical specifications for Veo generation."""
        effects = scene.get("special_effects", [])
        movement = cinematography.get("movement_style", "dynamic")

        specs = f"""- Duration: {duration}s
- Movement Type: {movement}
- Effects: {', '.join(effects[:3]) if effects else 'None'}
- Motion Intensity: {'high' if duration < 15 else 'medium'}
- Transition Style: smooth cuts"""

        return specs

    def _calculate_prompt_confidence(self, prompt_text: str) -> float:
        """
        Calculate confidence score for prompt quality.
        Returns value between 0 and 1.
        """
        # Simple heuristic-based scoring
        min_length = 100
        optimal_length = 400
        max_length = 600

        prompt_length = len(prompt_text)

        if prompt_length < min_length:
            return 0.5
        elif prompt_length > max_length:
            return 0.8
        else:
            # Peak confidence around optimal length
            distance_from_optimal = abs(prompt_length - optimal_length)
            confidence = 0.95 - (distance_from_optimal / optimal_length * 0.15)
            return max(0.7, min(1.0, confidence))

    def validate_veo_prompt(self, prompt: Dict[str, Any]) -> bool:
        """Validate that prompt meets Veo 3 requirements."""
        required_fields = ["scene_number", "duration_seconds", "prompt_text"]

        for field in required_fields:
            if field not in prompt:
                logger.warning(f"Missing required field: {field}")
                return False

        prompt_length = len(prompt["prompt_text"].split())
        if prompt_length > 1000:
            logger.warning(f"Prompt too long ({prompt_length} tokens)")
            return False

        return True

    def optimize_for_veo_constraints(self, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Optimize prompts for Veo 3 constraints and requirements.

        Args:
            prompts: List of Veo prompts to optimize

        Returns:
            Optimized prompt list
        """
        optimized = []

        for prompt in prompts:
            # Trim if too long
            text = prompt["prompt_text"]
            if len(text.split()) > self.veo_token_limit:
                text = " ".join(text.split()[:self.veo_token_limit]) + "..."
                prompt["prompt_text"] = text
                logger.info(f"Trimmed prompt for scene {prompt['scene_number']}")

            # Ensure valid effects
            valid_effects = [e for e in prompt.get("special_effects", []) 
                           if e in self.supported_effects]
            prompt["special_effects"] = valid_effects

            optimized.append(prompt)

        return optimized



â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
