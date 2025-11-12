# -*- coding: utf-8 -*-
"""
Audio Analyzer Module
Provides audio analysis utilities for the Audio Quality Curator
"""

import librosa
import numpy as np
from typing import Dict, Any

def analyze_audio_file(file_path: str) -> Dict[str, Any]:
    """
    Analyze audio file and return metrics.

    Args:
        file_path: Path to audio file

    Returns:
        Dictionary containing audio metrics
    """
    try:
        y, sr = librosa.load(file_path)

        duration = librosa.get_duration(y=y, sr=sr)
        rms = librosa.feature.rms(y=y)[0]
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

        return {
            'duration': duration,
            'sample_rate': sr,
            'rms_mean': float(np.mean(rms)),
            'spectral_centroid_mean': float(np.mean(spectral_centroid))
        }
    except Exception as e:
        raise Exception(f"Audio analysis failed: {str(e)}")
