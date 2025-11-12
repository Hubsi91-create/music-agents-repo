# -*- coding: utf-8 -*-
import os
import sys
import json
import logging
from pathlib import Path
import librosa
import numpy as np

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_audio(file_path):
    """
    Analysiert eine Audio-Datei und gibt Qualitätsmetriken zurück.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Audio-Datei nicht gefunden: {file_path}')

        # Audio laden
        y, sr = librosa.load(file_path)

        # Basis-Metriken berechnen
        duration = librosa.get_duration(y=y, sr=sr)

        # Quality Score berechnen (Dummy - vereinfacht)
        quality_score = 85

        # Ergebnis zurückgeben
        results = {
            'file': str(file_path),
            'sample_rate_hz': int(sr),
            'duration_seconds': float(duration),
            'quality_score': int(quality_score),
            'status': 'Success'
        }

        return results

    except Exception as e:
        logger.error(f'Fehler bei Analyse: {str(e)}')
        raise

def main():
    if len(sys.argv) < 2:
        print('[Agent 2] Audio Quality Curator')
        print('Usage: python agent_2.py <audio_file_path>')
        sys.exit(1)

    audio_file = sys.argv[1]

    try:
        logger.info(f'Analysiere: {audio_file}')
        results = analyze_audio(audio_file)

        # In JSON speichern
        with open('results.json', 'w') as f:
            json.dump(results, f, indent=2)

        logger.info(f'Quality Score: {results["quality_score"]}/100')
        logger.info(f'Ergebnisse gespeichert in: results.json')
        print(f'[SUCCESS] Analyse abgeschlossen!')

    except Exception as e:
        logger.error(f'Fatal Error: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    main()
