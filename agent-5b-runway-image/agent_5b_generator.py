"""
Agent 5b: Runway Gen-4 Image Style Anchor Generator
"""

import requests
import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class RunwayImageGenerator:
    def __init__(self, mock_mode=None):
        self.api_key = os.getenv("RUNWAY_API_KEY")
        self.model = "gen-4-image"
        self.output_dir = Path("style_anchors")
        self.output_dir.mkdir(exist_ok=True)

        # Auto-detect mock mode
        if mock_mode is None:
            if not self.api_key:
                print(f"⚠️  RUNWAY_API_KEY not found, running in MOCK MODE")
                self.mock_mode = True
            else:
                print(f"✅ Runway API key found")
                self.mock_mode = False
        else:
            self.mock_mode = mock_mode
            if mock_mode:
                print("🧪 Running in MOCK MODE (testing)")

    def generate_style_anchor(self, scene_data, style_anchors):
        """
        Generate Artistic/Stylized Reference Image
        """
        print(f"🎨 Generating Runway image for Scene {scene_data['id']}...")

        # Create prompt
        prompt = self._create_prompt(scene_data, style_anchors)

        # MOCK MODE: Return mock data without API call
        if self.mock_mode:
            print(f"🧪 MOCK MODE: Skipping actual API call")
            return {
                "scene_id": scene_data["id"],
                "image_path": None,
                "prompt": prompt,
                "model": "runway-gen4",
                "status": "mock_success",
                "note": "Mock mode - no actual image generated. Set RUNWAY_API_KEY for real generation."
            }

        # API Call (real mode)
        try:
            response = requests.post(
                "https://api.runwayml.com/v1/gen4/image",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": prompt,
                    "aspect_ratio": "16:9",
                    "style": style_anchors.get("artistic_style", "cinematic")
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                image_id = result["id"]

                # Wait for completion
                image_url = self._wait_for_image(image_id)

                if image_url:
                    # Download
                    image_data = requests.get(image_url).content

                    # Save
                    filename = f"ref_image_scene_{scene_data['id']:03d}_runway.png"
                    filepath = self.output_dir / filename
                    with open(filepath, "wb") as f:
                        f.write(image_data)

                    print(f"✅ Runway: {filepath}")
                    return {
                        "scene_id": scene_data["id"],
                        "image_path": str(filepath),
                        "prompt": prompt,
                        "model": "runway-gen4",
                        "status": "success"
                    }

            return {
                "scene_id": scene_data["id"],
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }

        except Exception as e:
            return {
                "scene_id": scene_data["id"],
                "status": "error",
                "error": str(e)
            }

    def _create_prompt(self, scene, style):
        """Create optimized Runway prompt"""
        return f"""{scene['description']}

Visual Style: {style.get('artistic_style', 'cinematic')}
Colors: {', '.join(style.get('colors', []))}
Mood: {scene.get('mood', 'energetic')}
Lighting: {style.get('lighting', 'dramatic')}
Camera: {scene.get('camera_angle', 'wide shot')}
Aesthetic: Film grain, professional photography
"""

    def _wait_for_image(self, image_id, max_wait=60):
        """Poll until image ready"""
        for _ in range(max_wait):
            response = requests.get(
                f"https://api.runwayml.com/v1/gen4/image/{image_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "completed":
                    return result.get("image_url")

            time.sleep(1)

        return None

if __name__ == "__main__":
    # Test
    generator = RunwayImageGenerator()

    test_scene = {
        "id": 2,
        "description": "Dancer in neon-lit club",
        "mood": "euphoric",
        "camera_angle": "Medium shot"
    }

    test_style = {
        "artistic_style": "neon-cyberpunk",
        "colors": ["#FF00FF", "#00FFFF"],
        "lighting": "Neon lights, high contrast"
    }

    result = generator.generate_style_anchor(test_scene, test_style)
    print(json.dumps(result, indent=2))
