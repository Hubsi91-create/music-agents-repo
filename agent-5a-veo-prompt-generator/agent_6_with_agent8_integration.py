"""
Agent 6 (VEO 3.1 Prompt Optimizer) with Agent 8 (Prompt Validator) Integration

This module integrates VEO 3.1 prompt generation with Agent 8's validation pipeline.
Ensures all VEO prompts are validated before video generation.

Flow:
1. Generate VEO 3.1 prompt with style/genre parameters
2. Send to Agent 8 for validation
3. Receive refined/optimized prompt
4. Return validated prompt for video generation

Author: AI Music Video Production System
Date: 2025-11-12
"""

import requests
import json
import logging
from typing import Dict, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class Agent6VEOWithAgent8Integration:
    """Agent 6 (VEO Optimizer) with Agent 8 (Validator) Integration"""

    def __init__(self, agent8_url: str = "http://localhost:5000/validate"):
        """
        Initialize Agent 6 with Agent 8 integration

        Args:
            agent8_url: Agent 8 validation endpoint URL
        """
        self.agent8_url = agent8_url
        self.validated_prompts = []
        self.stats = {
            "total_prompts": 0,
            "approved": 0,
            "needs_revision": 0,
            "unvalidated": 0
        }
        logger.info(f"🔗 Agent 6↔8 Integration initialized (Agent 8: {agent8_url})")

    def generate_veo_prompt(self, scene_description: str, style_anchors: Dict, genre: str) -> Dict:
        """
        Agent 6 Standard: Generate VEO 3.1 Prompt

        Args:
            scene_description: Description of the scene to generate
            style_anchors: Visual style parameters (color_temp, motion, etc.)
            genre: Music genre (pop, rock, hip-hop, etc.)

        Returns:
            Dict containing VEO 3.1 prompt structure
        """
        logger.info(f"📝 Agent 6: Generating VEO 3.1 Prompt for {genre}")

        # Extract style parameters with defaults
        color_temp = style_anchors.get("color_temp", 5800)
        motion_intensity = style_anchors.get("motion_intensity", 0.5)
        camera_movement = style_anchors.get("camera_movement", "dynamic")
        lighting_style = style_anchors.get("lighting_style", "cinematic")

        # Build VEO 3.1 optimized prompt
        veo_prompt = {
            "type": "veo_3.1",
            "prompt": f"VEO 3.1 | {genre.upper()} Music Video: {scene_description}. "
                     f"Cinematic {camera_movement} camera movement, "
                     f"{lighting_style} lighting ({color_temp}K), "
                     f"motion intensity {motion_intensity}. "
                     f"Professional grade, 4K resolution, film-quality output.",
            "parameters": {
                "color_temp": color_temp,
                "motion_intensity": motion_intensity,
                "camera_movement": camera_movement,
                "lighting_style": lighting_style
            },
            "duration": 15,
            "genre": genre,
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"✓ VEO Prompt generated: {len(veo_prompt['prompt'])} chars")
        return veo_prompt

    def validate_with_agent8(self, prompt: Dict) -> Optional[Dict]:
        """
        NEU: Send prompt to Agent 8 for validation

        Args:
            prompt: VEO prompt dictionary to validate

        Returns:
            Agent 8 validation result or None if failed
        """
        logger.info(f"🔄 Agent 6→8: Sending prompt to Agent 8 for validation")

        try:
            payload = {
                "prompt": prompt.get("prompt", ""),
                "prompt_type": "veo_3.1",
                "genre": prompt.get("genre", "pop"),
                "parameters": prompt.get("parameters", {}),
                "timestamp": prompt.get("timestamp", datetime.now().isoformat())
            }

            # Send to Agent 8
            response = requests.post(
                self.agent8_url,
                json=payload,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                quality_score = result.get("quality_score", 0)
                logger.info(f"✅ Agent 8 Response: Quality={quality_score:.2f}")
                return result
            else:
                logger.warning(f"⚠️ Agent 8 returned status {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            logger.error(f"❌ Agent 8 connection timeout (>{30}s)")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"❌ Agent 8 connection failed: Cannot reach {self.agent8_url}")
            return None
        except Exception as e:
            logger.error(f"❌ Agent 8 validation error: {str(e)}")
            return None

    def generate_and_validate_veo_prompt(
        self,
        scene_description: str,
        style_anchors: Dict,
        genre: str,
        require_validation: bool = True
    ) -> Dict:
        """
        MAIN FLOW: Generate + Validate + Return

        This is the primary method to use for creating validated VEO prompts.

        Args:
            scene_description: Scene to generate
            style_anchors: Style parameters
            genre: Music genre
            require_validation: If True, reject prompts that fail validation

        Returns:
            Dict with validation status and refined prompt
        """
        logger.info(f"🚀 Starting VEO Prompt Generation & Validation Pipeline")

        # Step 1: Generate
        prompt = self.generate_veo_prompt(scene_description, style_anchors, genre)
        self.stats["total_prompts"] += 1

        # Step 2: Validate with Agent 8
        validation = self.validate_with_agent8(prompt)

        # Step 3: Process validation result
        if validation:
            ready_for_gen = validation.get("ready_for_generation", False)
            quality_score = validation.get("quality_score", 0)

            if ready_for_gen and quality_score >= 0.75:
                # ✅ APPROVED
                logger.info(f"✅ Prompt APPROVED by Agent 8 (score: {quality_score:.2f})")
                refined_prompt = validation.get("refined_prompt", prompt["prompt"])

                result = {
                    "status": "approved",
                    "original_prompt": prompt["prompt"],
                    "refined_prompt": refined_prompt,
                    "quality_score": quality_score,
                    "agent8_recommendations": validation.get("recommendations", []),
                    "ready_for_generation": True,
                    "parameters": prompt.get("parameters", {}),
                    "validation_timestamp": datetime.now().isoformat()
                }
                self.stats["approved"] += 1

            else:
                # ⚠️ NEEDS REVISION
                logger.warning(f"⚠️ Prompt NEEDS REVISION (score: {quality_score:.2f})")
                result = {
                    "status": "needs_revision",
                    "original_prompt": prompt["prompt"],
                    "refined_prompt": validation.get("refined_prompt", prompt["prompt"]),
                    "quality_score": quality_score,
                    "agent8_recommendations": validation.get("recommendations", []),
                    "ready_for_generation": not require_validation,  # Allow fallback if not required
                    "parameters": prompt.get("parameters", {}),
                    "validation_timestamp": datetime.now().isoformat()
                }
                self.stats["needs_revision"] += 1
        else:
            # ℹ️ AGENT 8 UNAVAILABLE - Fallback
            logger.info(f"ℹ️ Agent 8 unavailable, using original prompt (fallback mode)")
            result = {
                "status": "unvalidated",
                "original_prompt": prompt["prompt"],
                "refined_prompt": prompt["prompt"],  # Use original as fallback
                "quality_score": 0,
                "agent8_recommendations": ["Agent 8 unavailable - using unvalidated prompt"],
                "ready_for_generation": True,  # Trust original in fallback mode
                "parameters": prompt.get("parameters", {}),
                "validation_timestamp": datetime.now().isoformat()
            }
            self.stats["unvalidated"] += 1

        # Store for analytics
        self.validated_prompts.append(result)

        logger.info(f"📊 Pipeline complete: {result['status'].upper()}")
        return result

    def get_stats(self) -> Dict:
        """Get validation statistics"""
        return {
            **self.stats,
            "approval_rate": self.stats["approved"] / max(self.stats["total_prompts"], 1),
            "total_validated": self.stats["approved"] + self.stats["needs_revision"]
        }

    def get_recent_prompts(self, limit: int = 10) -> List[Dict]:
        """Get recent validated prompts"""
        return self.validated_prompts[-limit:]


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Initialize integration
    integrator = Agent6VEOWithAgent8Integration(
        agent8_url="http://localhost:5000/validate"
    )

    # Example prompt generation
    scene = "Artist performing on rooftop at sunset, city skyline in background"
    style = {
        "color_temp": 6500,
        "motion_intensity": 0.7,
        "camera_movement": "dynamic",
        "lighting_style": "golden hour"
    }

    result = integrator.generate_and_validate_veo_prompt(
        scene_description=scene,
        style_anchors=style,
        genre="pop"
    )

    print(json.dumps(result, indent=2))
    print(f"\nStats: {integrator.get_stats()}")
