#!/usr/bin/env python3
"""
MUSIC VIDEO PRODUCTION PIPELINE WITH STYLE ANCHORS
==================================================

Full workflow:
1. Agent 4: Generate Screenplay
2. Agent 5a & 5b: Generate Style Anchor Images
3. [USER REVIEW] Approve style anchors in Storyboard App
4. Agent 5a & 5b: Generate Video Prompts with approved style anchors
5. Generate final videos

Usage:
    python pipeline_with_style_anchors.py screenplay.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Import new image generators
sys.path.append(str(Path(__file__).parent / "agent-5a-nanobanana-image"))
sys.path.append(str(Path(__file__).parent / "agent-5b-runway-image"))

try:
    from agent_5a_generator import NanobananaImageGenerator
    from agent_5b_generator import RunwayImageGenerator
    print("✅ Image generators imported successfully")
except ImportError as e:
    print(f"❌ Failed to import image generators: {e}")
    print("⚠️  Install dependencies: pip install google-auth python-dotenv requests")
    sys.exit(1)


class StyleAnchorPipeline:
    """Orchestrates the complete pipeline with style anchors"""

    def __init__(self, screenplay_file):
        self.screenplay_file = Path(screenplay_file)
        self.output_dir = Path("pipeline_output")
        self.output_dir.mkdir(exist_ok=True)

        # Initialize generators
        self.nanobanana = NanobananaImageGenerator()
        self.runway = RunwayImageGenerator()

        # Load screenplay
        with open(self.screenplay_file, 'r', encoding='utf-8') as f:
            self.screenplay = json.load(f)

        print(f"📋 Loaded screenplay: {self.screenplay.get('music_title', 'Unknown')}")
        print(f"📝 Scenes: {len(self.screenplay.get('screenplay', []))}")

    def step1_generate_style_anchors(self):
        """Step 1: Generate style anchor images for all scenes"""
        print("\n" + "="*60)
        print("STEP 1: GENERATING STYLE ANCHOR IMAGES")
        print("="*60)

        results = {
            "timestamp": datetime.now().isoformat(),
            "screenplay_file": str(self.screenplay_file),
            "music_title": self.screenplay.get("music_title"),
            "scenes": []
        }

        # Default style anchors (can be customized per project)
        default_style = {
            "character": {
                "description": "Lead performer, confident presence",
                "outfit": "Modern urban style"
            },
            "lighting": "Cinematic, dramatic lighting",
            "colors": ["#FF6B6B", "#4ECDC4", "#FFD93D"],
            "artistic_style": "cinematic"
        }

        for scene in self.screenplay.get("screenplay", []):
            print(f"\n🎬 Processing Scene {scene['scene_number']}...")

            # Prepare scene data
            scene_data = {
                "id": scene["scene_number"],
                "description": scene.get("screenplay_text", scene.get("concept_description", "")),
                "mood": ", ".join(scene.get("mood", ["professional"])),
                "location": scene.get("location", "Studio"),
                "camera_angle": scene.get("camera_angle", "Wide shot")
            }

            # Generate both style anchors
            nanobanana_result = self.nanobanana.generate_style_anchor(scene_data, default_style)
            runway_result = self.runway.generate_style_anchor(scene_data, default_style)

            # Store results
            scene_result = {
                "scene_number": scene["scene_number"],
                "nanobanana": nanobanana_result,
                "runway": runway_result,
                "status": "pending_review"
            }
            results["scenes"].append(scene_result)

        # Save results
        results_file = self.output_dir / "style_anchors_generated.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Style anchors generated!")
        print(f"📁 Results saved to: {results_file}")
        print(f"\n⏭️  NEXT STEP: Review style anchors in Storyboard App")
        print(f"   → Open: http://localhost:5000/storyboard")

        return results

    def step2_generate_video_prompts(self, approved_anchors_file=None):
        """Step 2: Generate video prompts with approved style anchors"""
        print("\n" + "="*60)
        print("STEP 2: GENERATING VIDEO PROMPTS WITH STYLE ANCHORS")
        print("="*60)

        # Load approved style anchors (or use generated ones)
        if approved_anchors_file:
            with open(approved_anchors_file, 'r', encoding='utf-8') as f:
                style_anchors = json.load(f)
        else:
            # Use generated anchors (for testing)
            anchors_file = self.output_dir / "style_anchors_generated.json"
            if anchors_file.exists():
                with open(anchors_file, 'r', encoding='utf-8') as f:
                    style_anchors = json.load(f)
            else:
                print("❌ No style anchors found. Run step 1 first.")
                sys.exit(1)

        # Generate VEO prompts with reference images
        veo_prompts = self._generate_veo_prompts_with_anchors(style_anchors)

        # Generate Runway prompts with reference images
        runway_prompts = self._generate_runway_prompts_with_anchors(style_anchors)

        # Save prompts
        veo_file = self.output_dir / "veo_prompts_with_anchors.json"
        runway_file = self.output_dir / "runway_prompts_with_anchors.json"

        with open(veo_file, 'w', encoding='utf-8') as f:
            json.dump(veo_prompts, f, indent=2, ensure_ascii=False)

        with open(runway_file, 'w', encoding='utf-8') as f:
            json.dump(runway_prompts, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Video prompts generated with style anchors!")
        print(f"📁 VEO prompts: {veo_file}")
        print(f"📁 Runway prompts: {runway_file}")
        print(f"\n⏭️  NEXT STEP: Generate videos using VEO/Runway APIs")

        return {"veo": veo_prompts, "runway": runway_prompts}

    def _generate_veo_prompts_with_anchors(self, style_anchors):
        """Generate VEO prompts with reference images"""
        veo_data = {
            "model": "veo-3.1",
            "timestamp": datetime.now().isoformat(),
            "music_title": self.screenplay.get("music_title"),
            "prompts": []
        }

        for scene_anchor in style_anchors.get("scenes", []):
            scene_num = scene_anchor["scene_number"]

            # Find corresponding screenplay scene
            screenplay_scene = next(
                (s for s in self.screenplay.get("screenplay", []) if s["scene_number"] == scene_num),
                None
            )

            if not screenplay_scene:
                continue

            # Get Nanobanana anchor (photorealistic for VEO)
            nanobanana = scene_anchor.get("nanobanana", {})

            prompt_data = {
                "scene": scene_num,
                "duration": screenplay_scene.get("duration_seconds", 10),
                "veo_prompt": nanobanana.get("prompt", screenplay_scene.get("screenplay_text", "")),
                "reference_image": nanobanana.get("image_path"),
                "style_anchor_status": nanobanana.get("status", "unknown")
            }

            veo_data["prompts"].append(prompt_data)

        return veo_data

    def _generate_runway_prompts_with_anchors(self, style_anchors):
        """Generate Runway prompts with reference images"""
        runway_data = {
            "model": "runway-gen4",
            "timestamp": datetime.now().isoformat(),
            "music_title": self.screenplay.get("music_title"),
            "prompts": []
        }

        for scene_anchor in style_anchors.get("scenes", []):
            scene_num = scene_anchor["scene_number"]

            # Find corresponding screenplay scene
            screenplay_scene = next(
                (s for s in self.screenplay.get("screenplay", []) if s["scene_number"] == scene_num),
                None
            )

            if not screenplay_scene:
                continue

            # Get Runway anchor (artistic/stylized for Runway)
            runway = scene_anchor.get("runway", {})

            prompt_data = {
                "scene": scene_num,
                "duration": screenplay_scene.get("duration_seconds", 10),
                "runway_prompt": runway.get("prompt", screenplay_scene.get("screenplay_text", "")),
                "reference_image": runway.get("image_path"),
                "style_anchor_status": runway.get("status", "unknown")
            }

            runway_data["prompts"].append(prompt_data)

        return runway_data

    def run_full_pipeline(self):
        """Run the complete pipeline"""
        print("\n" + "🎬"*30)
        print("MUSIC VIDEO PRODUCTION PIPELINE WITH STYLE ANCHORS")
        print("🎬"*30)

        # Step 1: Generate style anchors
        style_anchors = self.step1_generate_style_anchors()

        # Pause for user review (in production, this would wait for manual approval)
        print("\n" + "⏸️"*30)
        print("PIPELINE PAUSED FOR USER REVIEW")
        print("⏸️"*30)
        print("\nTo continue:")
        print("1. Review style anchors in Storyboard App")
        print("2. Approve/reject anchors")
        print("3. Run: python pipeline_with_style_anchors.py --step2")
        print("\nFor testing (skip review):")
        print("   python pipeline_with_style_anchors.py --full-auto")

        return style_anchors


def main():
    if len(sys.argv) < 2:
        print("📋 USAGE:")
        print("   python pipeline_with_style_anchors.py <screenplay.json>")
        print("\nOPTIONS:")
        print("   --step1              Generate style anchors only")
        print("   --step2              Generate video prompts (after review)")
        print("   --full-auto          Run full pipeline without review pause")
        sys.exit(1)

    screenplay_file = sys.argv[1]

    if not Path(screenplay_file).exists():
        print(f"❌ File not found: {screenplay_file}")
        sys.exit(1)

    pipeline = StyleAnchorPipeline(screenplay_file)

    # Check for options
    if "--full-auto" in sys.argv:
        print("🤖 Running in FULL AUTO mode (skipping review)")
        pipeline.step1_generate_style_anchors()
        pipeline.step2_generate_video_prompts()
    elif "--step2" in sys.argv:
        pipeline.step2_generate_video_prompts()
    else:
        # Default: Step 1 only (pause for review)
        pipeline.run_full_pipeline()


if __name__ == "__main__":
    main()
