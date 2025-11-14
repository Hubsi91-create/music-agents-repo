"""
Agent 5a: Nanobanana (Gemini 2.5 Flash Image) Style Anchor Generator
"""

from google.auth import default
import requests
import json
from pathlib import Path

class NanobananaImageGenerator:
    def __init__(self):
        self.credentials, self.project = default()
        self.model = "gemini-2.5-flash-image"
        self.output_dir = Path("style_anchors")
        self.output_dir.mkdir(exist_ok=True)

    def generate_style_anchor(self, scene_data, style_anchors):
        """
        Generate Character-consistent Style Reference Image
        """
        print(f"🎨 Generating Nanobanana image for Scene {scene_data['id']}...")

        # Create prompt
        prompt = self._create_prompt(scene_data, style_anchors)

        # API Call
        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generate",
                headers={
                    "Authorization": f"Bearer {self.credentials.token}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": prompt,
                    "aspectRatio": "16:9",
                    "quality": "high"
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                image_url = result.get("image", {}).get("url")

                if image_url:
                    # Download
                    image_data = requests.get(image_url).content

                    # Save
                    filename = f"ref_image_scene_{scene_data['id']:03d}_nanobanana.png"
                    filepath = self.output_dir / filename
                    with open(filepath, "wb") as f:
                        f.write(image_data)

                    print(f"✅ Nanobanana: {filepath}")
                    return {
                        "scene_id": scene_data["id"],
                        "image_path": str(filepath),
                        "prompt": prompt,
                        "model": "nanobanana",
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
        """Create optimized Nanobanana prompt"""
        return f"""
Scene: {scene['description']}

Character:
- Type: {style.get('character', {}).get('description', 'Lead dancer')}
- Outfit: {style.get('character', {}).get('outfit', 'Urban streetwear')}
- Expression: {scene.get('mood', 'confident')}

Setting:
- Location: {scene.get('location', 'Urban warehouse')}
- Lighting: {style.get('lighting', 'Golden hour')}
- Time: {scene.get('time', 'Dawn')}

Visual Style:
- Colors: {', '.join(style.get('colors', ['#FFA500']))}
- Mood: {scene.get('mood', 'energetic')}
- Aesthetic: Cinematic, photorealistic, film grain

Technical:
- Aspect Ratio: 16:9
- Camera: {scene.get('camera_angle', 'Wide shot')}
- Focus: Sharp, cinematic depth of field

IMPORTANT: Maintain character consistency, preserve facial features.
"""

if __name__ == "__main__":
    # Test
    generator = NanobananaImageGenerator()

    test_scene = {
        "id": 1,
        "description": "Lead dancer enters empty warehouse at dawn",
        "location": "Urban warehouse",
        "mood": "confident",
        "camera_angle": "Wide shot",
        "time": "Dawn"
    }

    test_style = {
        "character": {
            "description": "Female dancer, athletic",
            "outfit": "Black crop top, cargo pants"
        },
        "lighting": "Golden hour",
        "colors": ["#FFA500", "#FFD700"]
    }

    result = generator.generate_style_anchor(test_scene, test_style)
    print(json.dumps(result, indent=2))
