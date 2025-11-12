# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime

def generate_screenplay(music_title, music_duration, video_concept, quality_score):
    """
    Generiert ein detailliertes Drehbuch basierend auf Video-Konzept.
    """
    
    # Parse Video Concept
    scenes = video_concept.get("scenes", [])
    
    # Screenplay erstellen
    screenplay = {
        "timestamp": datetime.now().isoformat(),
        "music_title": music_title,
        "music_duration_seconds": music_duration,
        "quality_score": quality_score,
        "concept_type": video_concept.get("concept_type", "Standard"),
        "screenplay": []
    }
    
    # Für jede Szene ein Screenplay-Element
    for scene in scenes:
        screenplay_scene = {
            "scene_number": scene["scene"],
            "duration_seconds": scene["duration"],
            "concept_description": scene["description"],
            "screenplay_text": generate_scene_screenplay(
                scene["scene"], 
                scene["description"], 
                quality_score
            ),
            "visual_elements": extract_visual_elements(scene["description"]),
            "mood": extract_mood(scene["description"], quality_score)
        }
        screenplay["screenplay"].append(screenplay_scene)
    
    return screenplay

def generate_scene_screenplay(scene_num, description, quality_score):
    """
    Generiert detaillierten Text für jede Szene.
    """
    
    if quality_score >= 85:
        detail_level = "ULTRA DETAILED"
    elif quality_score >= 70:
        detail_level = "DETAILED"
    else:
        detail_level = "BASIC"
    
    return f"[Scene {scene_num} - {detail_level}] {description}"

def extract_visual_elements(description):
    """
    Extrahiert visuelle Elemente aus der Beschreibung.
    """
    keywords = ["animation", "transition", "effect", "camera", "lighting"]
    elements = []
    
    for keyword in keywords:
        if keyword.lower() in description.lower():
            elements.append(keyword)
    
    return elements if elements else ["standard_shot"]

def extract_mood(description, quality_score):
    """
    Extrahiert Stimmung basierend auf Quality Score.
    """
    moods = {
        90: ["cinematic", "professional", "premium"],
        70: ["professional", "clean"],
        50: ["basic", "standard"]
    }
    
    if quality_score >= 85:
        return moods[90]
    elif quality_score >= 70:
        return moods[70]
    else:
        return moods[50]

def main():
    if len(sys.argv) < 4:
        print("[Agent 4] Screenplay Generator")
        print("Usage: python agent_4.py <music_title> <duration> <concept_json_file> <quality_score>")
        sys.exit(1)
    
    try:
        music_title = sys.argv[1]
        duration = float(sys.argv[2])
        concept_file = sys.argv[3]
        quality = int(sys.argv[4])
        
        print(f"[Agent 4] Generiere Drehbuch für: {music_title}")
        print(f"[INFO] Lese Konzept aus: {concept_file}")
        
        # Konzept aus Datei laden
        with open(concept_file, 'r', encoding='utf-8') as f:
            concept_json = json.load(f)
        
        # Screenplay generieren
        screenplay = generate_screenplay(music_title, duration, concept_json, quality)
        
        # In JSON speichern
        with open('screenplay.json', 'w', encoding='utf-8') as f:
            json.dump(screenplay, f, indent=2, ensure_ascii=False)
        
        print(f"[SUCCESS] Screenplay erstellt mit {len(screenplay['screenplay'])} Szenen")
        print(f"[SAVED] Screenplay gespeichert in: screenplay.json")
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
