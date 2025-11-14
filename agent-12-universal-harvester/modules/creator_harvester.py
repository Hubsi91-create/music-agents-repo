"""
Creator Harvester - Agent 6 InfluencerMatcher Integration

Harvests creator/influencer data from YouTube, TikTok, Instagram, and Reddit
for collaboration matching and audience analysis.

Author: Universal Harvester System
Version: 1.0.0
"""

from typing import List, Dict, Any
import requests
from datetime import datetime
import logging
from .base_harvester import BaseHarvester

logging.basicConfig(level=logging.INFO)


class CreatorHarvester(BaseHarvester):
    """Harvests creator/influencer data for collaboration matching."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__("creator_harvester", config)
        import os
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')

    def get_data_sources(self) -> List[Dict[str, str]]:
        sources = []
        if 'youtube' in self.enabled_sources and self.youtube_api_key:
            sources.append({'name': 'YouTube Creators', 'url': 'https://www.googleapis.com/youtube/v3/channels', 'type': 'api'})
        if 'tiktok' in self.enabled_sources:
            sources.append({'name': 'TikTok Creators', 'url': 'https://tiktok.com', 'type': 'scrape'})
        return sources

    def extract_raw_data(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        if 'YouTube' in source['name']:
            return self._harvest_youtube_creators()
        return []

    def parse_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_data = []
        for item in raw_data:
            parsed_item = {
                'id': item.get('id', ''),
                'name': item.get('name', ''),
                'platform': item.get('platform', 'unknown'),
                'followers': item.get('followers', 0),
                'engagement_rate': item.get('engagement_rate', 0.0),
                'content_type': item.get('content_type', ''),
                'niche': item.get('niche', 'general'),
                'audience': {
                    'demographics': item.get('demographics', {}),
                    'interests': item.get('interests', [])
                },
                'source_url': item.get('url', ''),
                'harvested_at': datetime.now().isoformat()
            }
            parsed_data.append(parsed_item)
        return parsed_data

    def score_data_quality(self, data_item: Dict[str, Any]) -> float:
        followers = data_item.get('followers', 0)
        engagement_rate = data_item.get('engagement_rate', 0.0)

        import math
        follower_score = min(4.0, math.log10(max(1, followers)) / 2)
        engagement_score = min(3.0, engagement_rate * 30)
        audience_score = 2.0
        growth_score = 1.0

        return min(10.0, follower_score + engagement_score + audience_score + growth_score)

    def get_analysis_prompt(self, data: List[Dict[str, Any]]) -> str:
        return f"""Analyze these {len(data)} creators for collaboration:

1. BEST CREATOR MATCHES (Top 20 with fit scores)
2. AUDIENCE OVERLAP ANALYSIS
3. COLLABORATION POTENTIAL SCORES
4. ENGAGEMENT RATE PATTERNS
5. NICHE RECOMMENDATIONS

Return structured JSON with creator IDs and match scores."""

    def _harvest_youtube_creators(self) -> List[Dict[str, Any]]:
        if not self.youtube_api_key:
            return []
        self.logger.warning("YouTube creator harvest needs channel IDs")
        return []