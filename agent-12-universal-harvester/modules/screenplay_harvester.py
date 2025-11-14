"""
Screenplay Harvester - Agent 4 ScreenplayGenerator Integration

Harvests story ideas, screenplay patterns, and narrative structures
from Reddit writing communities, GitHub, and story platforms.

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


class ScreenplayHarvester(BaseHarvester):
    """
    Harvests screenplay and story data for music videos.

    Data Sources:
    - Reddit Writing Communities
    - GitHub Screenplay Collections
    - Story Platforms (Wattpad, AO3)
    - YouTube Script Analysis
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__("screenplay_harvester", config)

        import os
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.github_token = os.getenv('GITHUB_TOKEN')

        if self.reddit_client_id and self.reddit_client_secret:
            self.reddit = praw.Reddit(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent='ScreenplayHarvester/1.0'
            )
        else:
            self.reddit = None

    def get_data_sources(self) -> List[Dict[str, str]]:
        sources = []
        if 'reddit' in self.enabled_sources and self.reddit:
            sources.extend([
                {'name': 'Reddit WritingPrompts', 'url': 'r/WritingPrompts', 'type': 'scrape'},
                {'name': 'Reddit Screenwriting', 'url': 'r/Screenwriting', 'type': 'scrape'},
                {'name': 'Reddit Storytelling', 'url': 'r/shortstories', 'type': 'scrape'}
            ])
        if 'github' in self.enabled_sources:
            sources.append({'name': 'GitHub Screenplays', 'url': 'https://api.github.com/search/repositories', 'type': 'api'})
        return sources

    def extract_raw_data(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        if 'Reddit' in source['name']:
            return self._harvest_reddit(source['url'])
        elif 'GitHub' in source['name']:
            return self._harvest_github()
        return []

    def parse_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_data = []
        for item in raw_data:
            parsed_item = {
                'id': item.get('id', ''),
                'title': item.get('title', ''),
                'story_type': item.get('story_type', 'unknown'),
                'structure': {
                    'setup': item.get('setup', ''),
                    'conflict': item.get('conflict', ''),
                    'resolution': item.get('resolution', '')
                },
                'characters': item.get('characters', []),
                'themes': item.get('themes', []),
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
        engagement_score = min(4.0, math.log10(max(1, upvotes)) / 2 + math.log10(max(1, comments)) / 4)
        structure_score = 3.0 if data_item.get('structure', {}).get('conflict') else 1.0
        originality_score = 2.0  # Would need NLP analysis
        recency_score = 1.0

        return min(10.0, engagement_score + structure_score + originality_score + recency_score)

    def get_analysis_prompt(self, data: List[Dict[str, Any]]) -> str:
        return f"""Analyze these {len(data)} story patterns for music video screenplays:

1. TRENDING STORY STRUCTURES (Top 10)
2. POPULAR CHARACTER ARCHETYPES
3. EMOTIONAL ARC TEMPLATES
4. DIALOGUE PATTERNS
5. STORY RECOMMENDATIONS for 3-5min music videos

Return structured JSON with patterns and examples."""

    def _harvest_reddit(self, subreddit_name: str) -> List[Dict[str, Any]]:
        if not self.reddit:
            return []
        try:
            subreddit = self.reddit.subreddit(subreddit_name.replace('r/', ''))
            items = []
            for post in subreddit.hot(limit=50):
                items.append({
                    'id': post.id,
                    'title': post.title,
                    'story_type': 'prompt' if 'prompt' in subreddit_name.lower() else 'screenplay',
                    'setup': post.selftext[:200] if post.selftext else '',
                    'upvotes': post.score,
                    'comments': post.num_comments,
                    'themes': [post.link_flair_text] if post.link_flair_text else [],
                    'url': f"https://reddit.com{post.permalink}"
                })
            self.logger.info(f"Harvested {len(items)} screenplay items from {subreddit_name}")
            return items
        except Exception as e:
            self.logger.error(f"Reddit harvest failed: {str(e)}")
            return []

    def _harvest_github(self) -> List[Dict[str, Any]]:
        self.logger.warning("GitHub screenplay harvest requires implementation")
        return []