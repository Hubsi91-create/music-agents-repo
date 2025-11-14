"""
Sound Harvester - Agent 9 SoundDesigner Integration

Harvests sound design data including production techniques, effect chains,
VST recommendations, and audio engineering trends.

Author: Universal Harvester System
Version: 1.0.0
"""

from typing import List, Dict, Any
import requests
import praw
from datetime import datetime
import logging
from .base_harvester import BaseHarvester

logging.basicConfig(level=logging.INFO)


class SoundHarvester(BaseHarvester):
    """Harvests sound design and production technique data."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__("sound_harvester", config)
        import os
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')

        if self.reddit_client_id and self.reddit_client_secret:
            self.reddit = praw.Reddit(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent='SoundHarvester/1.0'
            )
        else:
            self.reddit = None

    def get_data_sources(self) -> List[Dict[str, str]]:
        sources = []
        if 'reddit' in self.enabled_sources and self.reddit:
            sources.extend([
                {'name': 'Reddit MusicProduction', 'url': 'r/musicproduction', 'type': 'scrape'},
                {'name': 'Reddit AudioEngineering', 'url': 'r/audioengineering', 'type': 'scrape'},
                {'name': 'Reddit SynthRecipes', 'url': 'r/synthrecipes', 'type': 'scrape'}
            ])
        if 'beatport' in self.enabled_sources:
            sources.append({'name': 'Beatport Charts', 'url': 'https://beatport.com', 'type': 'scrape'})
        if 'youtube' in self.enabled_sources:
            sources.append({'name': 'YouTube Production', 'url': 'https://youtube.com', 'type': 'scrape'})
        return sources

    def extract_raw_data(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        if 'Reddit' in source['name']:
            return self._harvest_reddit(source['url'])
        return []

    def parse_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_data = []
        for item in raw_data:
            parsed_item = {
                'id': item.get('id', ''),
                'title': item.get('title', ''),
                'technique': item.get('technique', ''),
                'tools': {
                    'vsts': item.get('vsts', []),
                    'hardware': item.get('hardware', []),
                    'daws': item.get('daws', [])
                },
                'effect_chain': item.get('effect_chain', []),
                'genre': item.get('genre', 'general'),
                'engagement': {
                    'upvotes': item.get('upvotes', 0),
                    'comments': item.get('comments', 0)
                },
                'source_url': item.get('url', ''),
                'harvested_at': datetime.now().isoformat()
            }
            parsed_data.append(parsed_item)
        return parsed_data

    def score_data_quality(self, data_item: Dict[str, Any]) -> float:
        engagement = data_item.get('engagement', {})
        upvotes = engagement.get('upvotes', 0)
        comments = engagement.get('comments', 0)

        import math
        quality_score = min(4.0, math.log10(max(1, upvotes)) / 2)
        community_score = min(3.0, math.log10(max(1, comments)) / 2)
        innovation_score = 2.0
        recency_score = 1.0

        return min(10.0, quality_score + community_score + innovation_score + recency_score)

    def get_analysis_prompt(self, data: List[Dict[str, Any]]) -> str:
        return f"""Analyze these {len(data)} sound design resources:

1. TRENDING SOUND DESIGN TECHNIQUES
2. BEST VST/TOOL COMBINATIONS
3. EFFECT CHAIN RECOMMENDATIONS
4. PRODUCTION WORKFLOW PATTERNS
5. GENRE-SPECIFIC SOUND DESIGN

Return structured JSON with techniques and tool recommendations."""

    def _harvest_reddit(self, subreddit_name: str) -> List[Dict[str, Any]]:
        if not self.reddit:
            return []
        try:
            subreddit = self.reddit.subreddit(subreddit_name.replace('r/', ''))
            items = []
            for post in subreddit.hot(limit=50):
                # Extract VST/tool mentions
                vsts = self._extract_vsts(post.title + ' ' + post.selftext)
                items.append({
                    'id': post.id,
                    'title': post.title,
                    'technique': self._extract_technique(post.title),
                    'vsts': vsts,
                    'upvotes': post.score,
                    'comments': post.num_comments,
                    'url': f"https://reddit.com{post.permalink}"
                })
            self.logger.info(f"Harvested {len(items)} sound design items from {subreddit_name}")
            return items
        except Exception as e:
            self.logger.error(f"Reddit harvest failed: {str(e)}")
            return []

    def _extract_vsts(self, text: str) -> List[str]:
        """Extract VST plugin names from text."""
        common_vsts = ['Serum', 'Massive', 'Omnisphere', 'Kontakt', 'Sylenth1', 'Nexus',
                       'Electra', 'Vital', 'Pigments', 'Phaseplant', 'Diva', 'Spire']
        found_vsts = []
        text_lower = text.lower()
        for vst in common_vsts:
            if vst.lower() in text_lower:
                found_vsts.append(vst)
        return found_vsts

    def _extract_technique(self, text: str) -> str:
        """Extract production technique from text."""
        techniques = {
            'compression': ['compress', 'compression', 'compressor'],
            'eq': ['eq', 'equalize', 'equalizer'],
            'reverb': ['reverb', 'room', 'hall'],
            'delay': ['delay', 'echo'],
            'synthesis': ['synth', 'synthesis', 'oscillator'],
            'mixing': ['mix', 'mixing', 'balance'],
            'mastering': ['master', 'mastering', 'limiter']
        }
        text_lower = text.lower()
        for technique, keywords in techniques.items():
            if any(keyword in text_lower for keyword in keywords):
                return technique
        return 'general'