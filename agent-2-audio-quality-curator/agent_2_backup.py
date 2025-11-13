
import argparse
import json
import logging
import os
import time
from typing import Dict, List, Any, Tuple

import librosa
import numpy as np
from scipy.signal import find_peaks

# --- Konfiguration des Loggings ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_audio(file_path: str) -> Dict[str, Any]:
    """Analysiert eine Audio-Datei und extrahiert Qualitätsmetriken.

    Args:
        file_path (str): Der Pfad zur Audio-Datei.

    Returns:
        Dict[str, Any]: Ein Dictionary mit den extrahierten Metriken.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Die Datei {file_path} wurde nicht gefunden.")

    try:
        y, sr = librosa.load(file_path, sr=None)
        
        # --- Grundlegende Metriken ---
        bitrate_kbps = librosa.get_samplerate(file_path) // 1000  # Annäherung
        duration_seconds = librosa.get_duration(y=y, sr=sr)
        channels = y.ndim

        # --- Fortgeschrittene Metriken ---
        dynamic_range_db = np.max(y) - np.min(y)
        snr_db = calculate_snr(y)
        frequency_peaks_hz = find_frequency_peaks(y, sr)

        return {
            "file": file_path,
            "file_size_mb": os.path.getsize(file_path) / (1024 * 1024),
            "bitrate_kbps": bitrate_kbps,
            "sample_rate_hz": sr,
            "duration_seconds": duration_seconds,
            "channels": channels,
            "dynamic_range_db": dynamic_range_db,
            "snr_db": snr_db,
            "frequency_peaks_hz": frequency_peaks_hz,
        }
    except Exception as e:
        logging.error(f"Fehler bei der Analyse von {file_path}: {e}")
        raise

def calculate_snr(y: np.ndarray) -> float:
    """Berechnet das Signal-to-Noise Ratio (SNR).

    Args:
        y (np.ndarray): Das Audiosignal.

    Returns:
        float: Das berechnete SNR in dB.
    """
    signal_power = np.mean(y**2)
    noise_power = np.mean(y[:1000]**2)  # Annahme: Rauschen am Anfang
    snr = 10 * np.log10(signal_power / noise_power)
    return float(snr)

def find_frequency_peaks(y: np.ndarray, sr: int) -> List[float]:
    """Findet die Top 5 Frequenz-Peaks.

    Args:
        y (np.ndarray): Das Audiosignal.
        sr (int): Die Sample-Rate.

    Returns:
        List[float]: Eine Liste der Top 5 Frequenz-Peaks in Hz.
    """
    fft_result = np.abs(np.fft.rfft(y))
    peaks, _ = find_peaks(fft_result, height=np.max(fft_result) * 0.1)
    peak_freqs = librosa.fft_frequencies(sr=sr, n_fft=len(fft_result) * 2 - 2)
    top_peaks = sorted(peak_freqs[peaks], reverse=True)[:5]
    return [float(f) for f in top_peaks]

def calculate_quality_score(metrics: Dict[str, Any]) -> Tuple[int, str]:
    """Berechnet den Quality Score basierend auf den Metriken.

    Args:
        metrics (Dict[str, Any]): Die extrahierten Audio-Metriken.

    Returns:
        Tuple[int, str]: Der Quality Score (0-100) und das Rating.
    """
    score = 50
    if metrics["bitrate_kbps"] >= 320:
        score += 15
    if metrics["sample_rate_hz"] >= 48000:
        score += 15
    if metrics["channels"] >= 2:
        score += 15
    if metrics["dynamic_range_db"] >= 12:
        score += 15
    if metrics["snr_db"] >= 40:
        score += 15
    if metrics["duration_seconds"] >= 180:
        score += 15
    
    score = min(100, score)

    if score >= 90:
        rating = "Excellent"
    elif score >= 70:
        rating = "Good"
    elif score >= 50:
        rating = "Fair"
    else:
        rating = "Poor"
        
    return score, rating

def get_recommendations(metrics: Dict[str, Any]) -> List[str]:
    """Erstellt Empfehlungen zur Qualitätsverbesserung.

    Args:
        metrics (Dict[str, Any]): Die extrahierten Audio-Metriken.

    Returns:
        List[str]: Eine Liste von Empfehlungen.
    """
    recommendations = []
    if metrics["bitrate_kbps"] < 192:
        recommendations.append("Erhöhe Bitrate für bessere Qualität")
    if metrics["sample_rate_hz"] < 44100:
        recommendations.append("Erhöhe Sample-Rate auf mindestens 44.1 kHz")
    if metrics["dynamic_range_db"] < 8:
        recommendations.append("Verbessere den Mix - zu niedrige Dynamik")
    if metrics["snr_db"] < 30:
        recommendations.append("Reduziere Hintergrundgeräusche")
        
    if not recommendations:
        recommendations.append("Sample-Rate ist auf Standard-Level - OK")

    return recommendations

def main(audio_file_path: str):
    """Hauptfunktion zur Analyse und Bewertung der Audio-Datei.

    Args:
        audio_file_path (str): Der Pfad zur Audio-Datei.
    """
    try:
        metrics = analyze_audio(audio_file_path)
        quality_score, quality_rating = calculate_quality_score(metrics)
        recommendations = get_recommendations(metrics)

        results = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            **metrics,
            "quality_score": quality_score,
            "quality_rating": quality_rating,
            "recommendations": recommendations,
        }

        with open("results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        # --- Konsolenausgabe ---
        print("--- Audio Quality Analysis ---")
        print(f"File: {results['file']}")
        print(f"Quality Score: {results['quality_score']}/100 ({results['quality_rating']})")
        print("Recommendations:")
        for rec in results['recommendations']:
            print(f"- {rec}")

    except Exception as e:
        logging.error(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analysiert und bewertet die Qualität von Audio-Dateien.")
    parser.add_argument("audio_file", help="Der Pfad zur Audio-Datei (MP3, WAV, FLAC, OGG).")
    args = parser.parse_args()
    
    main(args.audio_file)
