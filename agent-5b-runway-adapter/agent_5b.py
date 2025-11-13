# -*- coding: utf-8 -*-
import json
import sys

def transform_to_runway_prompt(screenplay_data):
    """
    Transformiert Screenplay zu Runway ML Prompts.
    """
    
    runway_prompts = {
        "model": "runway-gen3",
        "timestamp": screenplay_data.get("timestamp"),
        "music_title": screenplay_data.get("music_title"),
        "prompts": []
    }
    
    for scene in screenplay_data.get("screenplay", []):
        runway_prompt = {
            "scene": scene["scene_number"],
            "duration": scene["duration_seconds"],
            "runway_prompt": generate_runway_prompt(scene, screenplay_data.get("quality_score", 85))
        }
        runway_prompts["prompts"].append(runway_prompt)
    
    return runway_prompts

def generate_runway_prompt(scene, quality_score):
    """
    Generiert einen Runway Gen-3 optimierten Prompt.
    """
    base_prompt = scene["screenplay_text"]
    mood = ", ".join(scene.get("mood", ["professional"]))
    
    if quality_score >= 85:
        runway_spec = "HD 1080p, smooth motion, professional transitions, color graded"
    elif quality_score >= 70:
        runway_spec = "HD quality, smooth motion, professional transitions"
    else:
        runway_spec = "SD quality, standard motion"
    
    return f"{base_prompt}. {mood}. {runway_spec}. Music video production quality."

def main():
    if len(sys.argv) < 2:
        print("[Agent 5b] Runway Gen-3 Prompt Adapter")
        print("Usage: python agent_5b.py <screenplay_json_file>")
        sys.exit(1)
    
    try:
        screenplay_file = sys.argv[1]
        
        print(f"[Agent 5b] Transformiere zu Runway Gen-3 Prompts...")
        
        with open(screenplay_file, 'r', encoding='utf-8') as f:
            screenplay = json.load(f)
        
        runway_data = transform_to_runway_prompt(screenplay)
        
        with open('runway_prompts.json', 'w', encoding='utf-8') as f:
            json.dump(runway_data, f, indent=2, ensure_ascii=False)
        
        print(f"[SUCCESS] Runway Gen-3 Prompts erstellt für {len(runway_data['prompts'])} Szenen")
        print(f"[SAVED] Gespeichert in: runway_prompts.json")
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
