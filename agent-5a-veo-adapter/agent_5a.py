# -*- coding: utf-8 -*-
import json
import sys

def transform_to_veo_prompt(screenplay_data):
    """
    Transformiert Screenplay zu Veo 3.1 Prompts.
    """
    
    veo_prompts = {
        "model": "veo-3.1",
        "timestamp": screenplay_data.get("timestamp"),
        "music_title": screenplay_data.get("music_title"),
        "prompts": []
    }
    
    for scene in screenplay_data.get("screenplay", []):
        veo_prompt = {
            "scene": scene["scene_number"],
            "duration": scene["duration_seconds"],
            "veo_prompt": generate_veo_prompt(scene, screenplay_data.get("quality_score", 85))
        }
        veo_prompts["prompts"].append(veo_prompt)
    
    return veo_prompts

def generate_veo_prompt(scene, quality_score):
    """
    Generiert einen Veo 3.1 optimierten Prompt.
    """
    base_prompt = scene["screenplay_text"]
    mood = ", ".join(scene.get("mood", ["professional"]))
    
    if quality_score >= 85:
        veo_spec = "4K professional cinema, cinematic color grading, professional lighting"
    elif quality_score >= 70:
        veo_spec = "1080p professional, clean lighting, professional color"
    else:
        veo_spec = "720p standard quality"
    
    return f"{base_prompt}. {mood}. {veo_spec}. Professional music video production."

def main():
    if len(sys.argv) < 2:
        print("[Agent 5a] Veo 3.1 Prompt Adapter")
        print("Usage: python agent_5a.py <screenplay_json_file>")
        sys.exit(1)
    
    try:
        screenplay_file = sys.argv[1]
        
        print(f"[Agent 5a] Transformiere zu Veo 3.1 Prompts...")
        
        with open(screenplay_file, 'r', encoding='utf-8') as f:
            screenplay = json.load(f)
        
        veo_data = transform_to_veo_prompt(screenplay)
        
        with open('veo_prompts.json', 'w', encoding='utf-8') as f:
            json.dump(veo_data, f, indent=2, ensure_ascii=False)
        
        print(f"[SUCCESS] Veo 3.1 Prompts erstellt für {len(veo_data['prompts'])} Szenen")
        print(f"[SAVED] Gespeichert in: veo_prompts.json")
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
