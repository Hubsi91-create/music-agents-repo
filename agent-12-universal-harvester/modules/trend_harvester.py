"""
Trend Harvester - Agent 1 TrendDetective Integration

Harvests trending data from YouTube, Reddit, TikTok, and Twitter
to identify viral trends, emerging patterns, and popular content.

Author: Universal Harvester System
Version: 1.0.0
"""

from typing import List, Dict, Any
import requests
import praw
from datetime import datetime, timedelta
import logging
from .base_harvester import BaseHarvester

logging.basicConfig(level=logging.INFO)


class TrendHarvester(BaseHarvester):
    """
    Harvests trending music/video data from multiple platforms.

    Data Sources:
    - YouTube Trending API
    - Reddit (r/TrendingMusic, r/Music, r/PopMusic)
    - TikTok Web Scraping
    - Twitter/X Trends API
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__("trend_harvester", config)

        # API credentials (from env)
        import os
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

        # Initialize Reddit client
        if self.reddit_client_id and self.reddit_client_secret:
            self.reddit = praw.Reddit(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent='MusicTrendHarvester/1.0'
            )
        else:
            self.reddit = None
            self.logger.warning("Reddit credentials not found")

    # ============================================================
    # ABSTRACT METHOD IMPLEMENTATIONS
    # ============================================================

    def get_data_sources(self) -> List[Dict[str, str]]:
        """Get list of trend data sources."""
        sources = []

        if 'youtube' in self.enabled_sources and self.youtube_api_key:
            sources.append({
                'name': 'YouTube Trending',
                'url': 'https://www.googleapis.com/youtube/v3/videos',
                'type': 'api'
            })

        if 'reddit' in self.enabled_sources and self.reddit:
            sources.extend([
                {'name': 'Reddit TrendingMusic', 'url': 'r/TrendingMusic', 'type': 'scrape'},
                {'name': 'Reddit Music', 'url': 'r/Music', 'type': 'scrape'},
                {'name': 'Reddit PopMusic', 'url': 'r/popmusic', 'type': 'scrape'}
            ])

        if 'tiktok' in self.enabled_sources:
            sources.append({
                'name': 'TikTok Trending',
                'url': 'https://www.tiktok.com/discover',
                'type': 'scrape'
            })

        if 'twitter' in self.enabled_sources and self.twitter_bearer_token:
            sources.append({
                'name': 'Twitter Trends',
                'url': 'https://api.twitter.com/2/trends/place',
                'type': 'api'
            })

        return sources

    def extract_raw_data(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract raw data from a specific source."""
        source_name = source['name']

        try:
            if 'YouTube' in source_name:
                return self._harvest_youtube_trending()
            elif 'Reddit' in source_name:
                return self._harvest_reddit(source['url'])
            elif 'TikTok' in source_name:
                return self._harvest_tiktok()
            elif 'Twitter' in source_name:
                return self._harvest_twitter()
            else:
                return []

        except Exception as e:
            self.logger.error(f"Failed to extract from {source_name}: {str(e)}")
            return []

    def parse_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse and structure raw trend data."""
        parsed_data = []

        for item in raw_data:
            try:
                parsed_item = {
                    'id': item.get('id', ''),
                    'title': item.get('title', ''),
                    'platform': item.get('platform', 'unknown'),
                    'engagement': {
                        'views': item.get('views', 0),
                        'likes': item.get('likes', 0),
                        'comments': item.get('comments', 0),
                        'shares': item.get('shares', 0)
                    },
                    'metadata': {
                        'category': item.get('category', 'music'),
                        'genre': item.get('genre', 'unknown'),
                        'tags': item.get('tags', [])
                    },
                    'source_url': item.get('url', ''),
                    'published_at': item.get('published_at', datetime.now().isoformat()),
                    'harvested_at': datetime.now().isoformat()
                }
                parsed_data.append(parsed_item)

            except Exception as e:
                self.logger.error(f"Failed to parse item: {str(e)}")
                continue

        return parsed_data

    def score_data_quality(self, data_item: Dict[str, Any]) -> float:
        """
        Calculate quality score for trend data.

        Scoring:
        - 50% = Engagement (Likes, Views, Comments)
        - 30% = Recency (Last 7 days = full score)
        - 20% = Community Validation (Multi-source confirmation)
        """
        try:
            # Engagement score (0-5.0)
            engagement = data_item.get('engagement', {})
            views = engagement.get('views', 0)
            likes = engagement.get('likes', 0)
            comments = engagement.get('comments', 0)

            # Normalize engagement (logarithmic scale)
            import math
            engagement_score = 0
            if views > 0:
                engagement_score += min(2.0, math.log10(views) / 2)
            if likes > 0:
                engagement_score += min(2.0, math.log10(likes) / 2)
            if comments > 0:
                engagement_score += min(1.0, math.log10(comments) / 2)

            # Recency score (0-3.0)
            published_at = data_item.get('published_at', '')
            if published_at:
                try:
                    pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    age_days = (datetime.now() - pub_date.replace(tzinfo=None)).days
                    if age_days <= 7:
                        recency_score = 3.0
                    elif age_days <= 14:
                        recency_score = 2.0
                    elif age_days <= 30:
                        recency_score = 1.0
                    else:
                        recency_score = 0.5
                except:
                    recency_score = 1.0
            else:
                recency_score = 1.0

            # Community validation score (0-2.0)
            # Higher if from multiple platforms or high engagement
            platform = data_item.get('platform', '')
            validation_score = 1.0  # Base score

            if likes > 1000 or views > 100000:
                validation_score = 2.0

            # Total score (0-10)
            total_score = engagement_score + recency_score + validation_score

            return min(10.0, max(0.0, total_score))

        except Exception as e:
            self.logger.error(f"Failed to score item: {str(e)}")
            return 0.0

    def get_analysis_prompt(self, data: List[Dict[str, Any]]) -> str:
        """Generate Gemini analysis prompt for trends."""
        return f"""Analyze these {len(data)} trending items and provide:

1. TOP 10 TRENDS with viral potential scores (1-10)
   - Rank by engagement and growth trajectory
   - Identify why each trend is performing well

2. EMERGING TRENDS (early growth phase)
   - Trends showing rapid growth in last 7 days
   - Under-the-radar opportunities

3. DOMINANT GENRES/STYLES
   - Which music genres are trending
   - Visual style patterns
   - Content format trends

4. VIRAL CHARACTERISTICS
   - Common elements in viral content
   - Audience engagement patterns
   - Optimal content length/format

5. CREATOR RECOMMENDATIONS
   - Best trend opportunities for new creators
   - Trends with low competition
   - High-ROI trend selection

Return results as structured JSON."""

    # ============================================================
    # PLATFORM-SPECIFIC HARVESTERS
    # ============================================================

    def _harvest_youtube_trending(self) -> List[Dict[str, Any]]:
        """Harvest YouTube trending videos."""
        if not self.youtube_api_key:
            self.logger.warning("YouTube API key not configured")
            return []

        try:
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet,statistics,contentDetails',
                'chart': 'mostPopular',
                'regionCode': 'US',
                'videoCategoryId': '10',  # Music category
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
                    'platform': 'youtube',
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                    'category': 'music',
                    'tags': snippet.get('tags', []),
                    'url': f"https://youtube.com/watch?v={video.get('id', '')}",
                    'published_at': snippet.get('publishedAt', '')
                })

            self.logger.info(f"Harvested {len(items)} YouTube trending videos")
            return items

        except Exception as e:
            self.logger.error(f"YouTube harvest failed: {str(e)}")
            return []

    def _harvest_reddit(self, subreddit_name: str) -> List[Dict[str, Any]]:
        """Harvest Reddit posts from music subreddits."""
        if not self.reddit:
            return []

        try:
            subreddit = self.reddit.subreddit(subreddit_name.replace('r/', ''))
            items = []

            # Get hot posts
            for post in subreddit.hot(limit=50):
                # Filter for music-related content
                if any(word in post.title.lower() for word in ['music', 'song', 'artist', 'video', 'track']):
                    items.append({
                        'id': post.id,
                        'title': post.title,
                        'platform': 'reddit',
                        'views': 0,  # Reddit doesn't provide view count
                        'likes': post.score,
                        'comments': post.num_comments,
                        'category': 'music',
                        'tags': [post.link_flair_text] if post.link_flair_text else [],
                        'url': f"https://reddit.com{post.permalink}",
                        'published_at': datetime.fromtimestamp(post.created_utc).isoformat()
                    })

            self.logger.info(f"Harvested {len(items)} Reddit posts from {subreddit_name}")
            return items

        except Exception as e:
            self.logger.error(f"Reddit harvest failed for {subreddit_name}: {str(e)}")
            return []

    def _harvest_tiktok(self) -> List[Dict[str, Any]]:
        """
        Harvest TikTok trending sounds (web scraping).

        Note: This is a placeholder - real implementation would require
        TikTok API access or sophisticated web scraping.
        """
        self.logger.warning("TikTok harvesting not fully implemented (requires API access)")

        # Mock data for testing
        return [
            {
                'id': 'tiktok_trend_1',
                'title': 'Viral Dance Challenge',
                'platform': 'tiktok',
                'views': 5000000,
                'likes': 500000,
                'comments': 10000,
                'shares': 50000,
                'category': 'music',
                'tags': ['dance', 'viral', 'trending'],
                'url': 'https://tiktok.com/trending',
                'published_at': datetime.now().isoformat()
            }
        ]

    def _harvest_twitter(self) -> List[Dict[str, Any]]:
        """
        Harvest Twitter trending topics.

        Note: Requires Twitter API v2 access.
        """
        if not self.twitter_bearer_token:
            self.logger.warning("Twitter API token not configured")
            return []

        try:
            # Twitter API v2 trending topics
            url = "https://api.twitter.com/2/trends/by/woeid/1"  # Worldwide trends
            headers = {
                'Authorization': f'Bearer {self.twitter_bearer_token}'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            items = []
            for trend in data.get('data', []):
                # Filter music-related trends
                name = trend.get('name', '')
                if any(word in name.lower() for word in ['music', 'song', 'artist', 'video']):
                    items.append({
                        'id': f"twitter_{trend.get('id', '')}",
                        'title': name,
                        'platform': 'twitter',
                        'views': 0,
                        'likes': 0,
                        'comments': 0,
                        'category': 'music',
                        'tags': [name],
                        'url': f"https://twitter.com/search?q={name}",
                        'published_at': datetime.now().isoformat()
                    })

            self.logger.info(f"Harvested {len(items)} Twitter trends")
            return items

        except Exception as e:
            self.logger.error(f"Twitter harvest failed: {str(e)}")
            return []

    def __repr__(self) -> str:
        return f"<TrendHarvester sources={len(self.enabled_sources)}>"