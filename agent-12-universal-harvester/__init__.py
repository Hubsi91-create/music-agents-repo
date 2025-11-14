"""
Agent 12 - Universal Harvester

Central data harvesting system for Music Video Production Agents.
Provides harvested data to Agents 1-11 for self-improvement.

Author: Universal Harvester System
Version: 1.0.0
"""

from .modules.trend_harvester import TrendHarvester
from .modules.audio_harvester import AudioHarvester
from .modules.screenplay_harvester import ScreenplayHarvester
from .modules.creator_harvester import CreatorHarvester
from .modules.distribution_harvester import DistributionHarvester
from .modules.sound_harvester import SoundHarvester
from .analyzers.gemini_analyzer import GeminiAnalyzer
from .database.harvested_data import HarvestedDataDB

__version__ = "1.0.0"
__all__ = [
    'TrendHarvester',
    'AudioHarvester',
    'ScreenplayHarvester',
    'CreatorHarvester',
    'DistributionHarvester',
    'SoundHarvester',
    'GeminiAnalyzer',
    'HarvestedDataDB'
]