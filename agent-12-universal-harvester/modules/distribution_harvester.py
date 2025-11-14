"""
Distribution Harvester - Agent 10 MasterDistributor Integration

Harvests distribution data including title patterns, hashtags, posting times,
and viral hooks from YouTube, TikTok, Twitter, and Reddit.

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


class DistributionHarvester(BaseHarvester):
    """Harvests distribution strategy data for optimal content delivery."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__("distribution_harvester", config)
        import os
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')

        if self.reddit_client_id and self.reddit_client_secret:
            self.reddit = praw.Reddit(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent='DistributionHarvester/1.0'
            )
        else:
            self.reddit = None

    def get_data_sources(self) -> List[Dict[str, str]]:
        sources = []
        if 'youtube_analytics' in self.enabled_sources and self.youtube_api_key:
            sources.append({'name': 'YouTube Analytics', 'url': 'https://www.googleapis.com/youtube/v3/videos', 'type': 'api'})
        if 'reddit' in self.enabled_sources and self.reddit:
            sources.extend([
                {'name': 'Reddit Marketing', 'url': 'r/marketing', 'type': 'scrape'},
                {'name': 'Reddit ContentCreators', 'url': 'r/NewTubers', 'type': 'scrape'}
            ])
        return sources

    def extract_raw_data(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        if 'YouTube' in source['name']:
            return self._harvest_youtube_analytics()
        elif 'Reddit' in source['name']:
            return self._harvest_reddit(source['url'])
        return []

    def parse_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_data = []
        for item in raw_data:
            parsed_item = {
                'id': item.get('id', ''),
                'title': item.get('title', ''),
                'title_pattern': item.get('title_pattern', ''),
                'hashtags': item.get('hashtags', []),
                'post_time': item.get('post_time', ''),
                'platform': item.get('platform', 'unknown'),
                'performance': {
                    'views': item.get('views', 0),
                    'ctr': item.get('ctr', 0.0),
                    'shares': item.get('shares', 0)
                },
                'viral_hooks': item.get('viral_hooks', []),
                'source_url': item.get('url', ''),
                'harvested_at': datetime.now().isoformat()
            }
            parsed_data.append(parsed_item)
        return parsed_data

    def score_data_quality(self, data_item: Dict[str, Any]) -> float:
        performance = data_item.get('performance', {})
        views = performance.get('views', 0)
        ctr = performance.get('ctr', 0.0)
        shares = performance.get('shares', 0)

        import math
        engagement_score = min(4.0, math.log10(max(1, views)) / 2)
        shareability_score = min(3.0, math.log10(max(1, shares)) / 1.5)
        ctr_score = min(2.0, ctr * 20)
        timing_score = 1.0

        return min(10.0, engagement_score + shareability_score + ctr_score + timing_score)

    def get_analysis_prompt(self, data: List[Dict[str, Any]]) -> str:
        return f"""Analyze these {len(data)} distribution patterns:

1. OPTIMAL TITLE PATTERNS for maximum CTR
2. BEST HASHTAG COMBINATIONS by platform
3. OPTIMAL POSTING TIMES for each platform
4. VIRAL HOOK STRUCTURES
5. PLATFORM-SPECIFIC TACTICS

Return structured JSON with actionable strategies."""

    def _harvest_youtube_analytics(self) -> List[Dict[str, Any]]:
        if not self.youtube_api_key:
            return []
        try:
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet,statistics',
                'chart': 'mostPopular',
                'regionCode': 'US',
                'maxResults': 50,
                'key': self.youtube_api_key
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            items = []
            for video in data.get('items', []):
                snippet = video.get('snippet', {})
                stats = video.get('statistics', {})
                items.append({
                    'id': video.get('id', ''),
                    'title': snippet.get('title', ''),
                    'title_pattern': self._extract_title_pattern(snippet.get('title', '')),
                    'hashtags': snippet.get('tags', []),
                    'post_time': snippet.get('publishedAt', ''),
                    'platform': 'youtube',
                    'views': int(stats.get('viewCount', 0)),
                    'ctr': 0.05,  # Estimate
                    'shares': int(stats.get('commentCount', 0)),
                    'url': f"https://youtube.com/watch?v={video.get('id', '')}"
                })
            self.logger.info(f"Harvested {len(items)} YouTube analytics data")
            return items
        except Exception as e:
            self.logger.error(f"YouTube analytics harvest failed: {str(e)}")
            return []

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
                    'platform': 'reddit',
                    'views': 0,
                    'shares': post.score,
                    'url': f"https://reddit.com{post.permalink}"
                })
            return items
        except Exception as e:
            self.logger.error(f"Reddit harvest failed: {str(e)}")
            return []

    def _extract_title_pattern(self, title: str) -> str:
        """Extract title pattern (e.g., '[CAPS] description | keyword')"""
        # Basic pattern extraction
        if '[' in title and ']' in title:
            return 'bracketed_prefix'
        elif '|' in title:
            return 'pipe_separated'
        elif ':' in title:
            return 'colon_separated'
        else:
            return 'simple'