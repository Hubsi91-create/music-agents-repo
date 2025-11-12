# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime

def generate_video_concept(music_title, music_duration, quality_score):
    """
    Generiert ein Video-Konzept basierend auf Musik-Metadaten.
    """

    if quality_score >= 85:
        concept_type = "Premium High-Quality"
        scenes = [
            {"scene": 1, "duration": 10, "description": "Intro mit Logo Animation"},
            {"scene": 2, "duration": 30, "description": "Main Performance"},
            {"scene": 3, "duration": 20, "description": "Outro mit Credits"}
        ]
    elif quality_score >= 70:
        concept_type = "Standard Quality"
        scenes = [
            {"scene": 1, "duration": 5, "description": "Quick Intro"},
            {"scene": 2, "duration": 40, "description": "Performance Showcase"},
            {"scene": 3, "duration": 10, "description": "Outro"}
        ]
    else:
        concept_type = "Basic Quality"
        scenes = [
            {"scene": 1, "duration": 3, "description": "Fade In"},
            {"scene": 2, "duration": music_duration - 6, "description": "Single Shot"},
            {"scene": 3, "duration": 3, "description": "Fade Out"}
        ]

    concept = {
        "timestamp": datetime.now().isoformat(),
        "music_title": music_title,
        "music_duration_seconds": music_duration,
        "quality_score": quality_score,
        "concept_type": concept_type,
        "total_video_duration": sum([s["duration"] for s in scenes]),
        "scenes": scenes,
        "recommended_resolution": "1920x1080" if quality_score >= 85 else "1280x720",
        "recommended_fps": 60 if quality_score >= 85 else 30
    }

    return concept

def main():
    if len(sys.argv) < 4:
        print("[Agent 3] Video Concept Collaborator")
        print("Usage: python agent_3.py <music_title> <duration_seconds> <quality_score>")
        sys.exit(1)

    try:
        music_title = sys.argv[1]
        duration = float(sys.argv[2])
        quality = int(sys.argv[3])

        print(f"[Agent 3] Generiere Video-Konzept für: {music_title}")

        concept = generate_video_concept(music_title, duration, quality)

        with open('concept.json', 'w', encoding='utf-8') as f:
            json.dump(concept, f, indent=2, ensure_ascii=False)

        print(f"[SUCCESS] Video-Konzept erstellt: {concept['concept_type']}")
        print(f"[INFO] Total Video Duration: {concept['total_video_duration']}s")
        print(f"[SAVED] Concept gespeichert in: concept.json")

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
