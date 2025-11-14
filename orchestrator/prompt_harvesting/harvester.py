#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prompt Harvesting Module - Reddit, YouTube, and Web Scraper
Collects prompts from various sources for training AI agents
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

# Third-party imports
try:
    import praw
    PRAW_AVAILABLE = True
except ImportError:
    PRAW_AVAILABLE = False
    logging.warning("PRAW not installed. Reddit harvesting disabled.")

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False
    logging.warning("youtube-transcript-api not installed. YouTube harvesting disabled.")

try:
    import requests
    from bs4 import BeautifulSoup
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False
    logging.warning("requests/beautifulsoup4 not installed. Web scraping disabled.")

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class PromptHarvester:
    """
    Harvests prompts from Reddit, YouTube, and web sources
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the harvester with configuration

        Args:
            config_path: Path to config.json file
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')

        self.config = self._load_config(config_path)
        self.reddit_client = None

        # Initialize Reddit client if credentials available
        if PRAW_AVAILABLE:
            self._init_reddit_client()

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"Config file not found: {config_path}. Using defaults.")
                return self._default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._default_config()

    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "reddit": {
                "subreddits": ["RunwayML", "PromptEngineering", "VideoGeneration", "OpenAI"],
                "limit": 100,
                "sort": "hot"
            },
            "youtube": {
                "search_queries": ["Runway Gen-4 prompts", "Veo 3.1 tutorial"],
                "max_results": 50
            },
            "quality_threshold": 7.0,
            "auto_harvest_interval_hours": 24,
            "gemini_model": "gemini-2.5-flash"
        }

    def _init_reddit_client(self):
        """Initialize Reddit API client"""
        try:
            # Read credentials from environment
            client_id = os.getenv('REDDIT_CLIENT_ID')
            client_secret = os.getenv('REDDIT_CLIENT_SECRET')
            user_agent = os.getenv('REDDIT_USER_AGENT', 'PromptHarvester/1.0')

            if client_id and client_secret:
                self.reddit_client = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )
                logger.info("[Reddit] Client initialized successfully")
            else:
                logger.warning("[Reddit] No credentials found in environment variables")
                logger.info("[Reddit] Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to enable")
        except Exception as e:
            logger.error(f"[Reddit] Failed to initialize client: {e}")

    def harvest_reddit(self, subreddits: Optional[List[str]] = None,
                       limit: Optional[int] = None) -> List[Dict]:
        """
        Harvest prompts from Reddit

        Args:
            subreddits: List of subreddit names (defaults to config)
            limit: Maximum posts per subreddit (defaults to config)

        Returns:
            List of harvested prompt dictionaries
        """
        if not PRAW_AVAILABLE:
            logger.error("[Reddit] PRAW library not installed")
            return []

        if not self.reddit_client:
            logger.error("[Reddit] Client not initialized. Check credentials.")
            return []

        if subreddits is None:
            subreddits = self.config['reddit']['subreddits']
        if limit is None:
            limit = self.config['reddit']['limit']

        harvested = []
        sort_method = self.config['reddit'].get('sort', 'hot')

        logger.info(f"[Reddit] Harvesting from {len(subreddits)} subreddits...")

        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit_client.subreddit(subreddit_name)

                # Get posts based on sort method
                if sort_method == 'hot':
                    posts = subreddit.hot(limit=limit)
                elif sort_method == 'top':
                    posts = subreddit.top(limit=limit, time_filter='week')
                else:
                    posts = subreddit.new(limit=limit)

                for post in posts:
                    # Extract prompts from post
                    prompts = self._extract_prompts_from_text(post.selftext)

                    if prompts or self._is_prompt_related(post.title + " " + post.selftext):
                        data = {
                            'source': 'reddit',
                            'subreddit': subreddit_name,
                            'title': post.title,
                            'text': post.selftext,
                            'prompts': prompts,
                            'url': f"https://reddit.com{post.permalink}",
                            'upvotes': post.score,
                            'comments': post.num_comments,
                            'created_utc': datetime.fromtimestamp(post.created_utc).isoformat(),
                            'harvested_at': datetime.now().isoformat()
                        }
                        harvested.append(data)

                logger.info(f"[Reddit] r/{subreddit_name}: {len([h for h in harvested if h['subreddit'] == subreddit_name])} posts")
                time.sleep(1)  # Rate limiting

            except Exception as e:
                logger.error(f"[Reddit] Error harvesting r/{subreddit_name}: {e}")

        logger.info(f"[Reddit] Total harvested: {len(harvested)} posts")
        return harvested

    def harvest_youtube(self, search_queries: Optional[List[str]] = None,
                        max_results: Optional[int] = None) -> List[Dict]:
        """
        Harvest prompts from YouTube video descriptions and transcripts

        Args:
            search_queries: List of search terms (defaults to config)
            max_results: Maximum results per query (defaults to config)

        Returns:
            List of harvested prompt dictionaries
        """
        if not WEB_SCRAPING_AVAILABLE:
            logger.error("[YouTube] requests/beautifulsoup4 not installed")
            return []

        if search_queries is None:
            search_queries = self.config['youtube']['search_queries']
        if max_results is None:
            max_results = self.config['youtube']['max_results']

        harvested = []

        logger.info(f"[YouTube] Harvesting from {len(search_queries)} search queries...")

        for query in search_queries:
            try:
                # Use YouTube search (web scraping approach - no API key needed)
                videos = self._search_youtube(query, max_results)

                for video in videos:
                    video_id = video['id']

                    # Get video details
                    details = self._get_video_details(video_id)

                    if details:
                        # Extract prompts from description
                        prompts = self._extract_prompts_from_text(details['description'])

                        if prompts or self._is_prompt_related(details['title'] + " " + details['description']):
                            data = {
                                'source': 'youtube',
                                'video_id': video_id,
                                'title': details['title'],
                                'description': details['description'],
                                'prompts': prompts,
                                'url': f"https://youtube.com/watch?v={video_id}",
                                'views': details.get('views', 0),
                                'harvested_at': datetime.now().isoformat()
                            }
                            harvested.append(data)

                logger.info(f"[YouTube] Query '{query}': {len([h for h in harvested if query.lower() in h['title'].lower()])} videos")
                time.sleep(2)  # Rate limiting

            except Exception as e:
                logger.error(f"[YouTube] Error harvesting query '{query}': {e}")

        logger.info(f"[YouTube] Total harvested: {len(harvested)} videos")
        return harvested

    def harvest_web(self, urls: Optional[List[str]] = None) -> List[Dict]:
        """
        Harvest prompts from web pages (GitHub, blogs, etc.)

        Args:
            urls: List of URLs to scrape (optional)

        Returns:
            List of harvested prompt dictionaries
        """
        if not WEB_SCRAPING_AVAILABLE:
            logger.error("[Web] requests/beautifulsoup4 not installed")
            return []

        if urls is None:
            # Default sources
            urls = [
                'https://github.com/topics/prompt-engineering',
                'https://github.com/topics/runway-ml',
            ]

        harvested = []

        logger.info(f"[Web] Harvesting from {len(urls)} URLs...")

        for url in urls:
            try:
                response = requests.get(url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract text content
                    text_content = soup.get_text(separator=' ', strip=True)

                    # Extract prompts
                    prompts = self._extract_prompts_from_text(text_content)

                    if prompts:
                        data = {
                            'source': 'web',
                            'url': url,
                            'title': soup.title.string if soup.title else url,
                            'prompts': prompts,
                            'harvested_at': datetime.now().isoformat()
                        }
                        harvested.append(data)

                time.sleep(1)  # Rate limiting

            except Exception as e:
                logger.error(f"[Web] Error harvesting {url}: {e}")

        logger.info(f"[Web] Total harvested: {len(harvested)} pages")
        return harvested

    def _search_youtube(self, query: str, max_results: int) -> List[Dict]:
        """
        Search YouTube videos (web scraping approach)

        Args:
            query: Search query
            max_results: Maximum results

        Returns:
            List of video data
        """
        try:
            # Use YouTube search URL
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

            response = requests.get(search_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })

            # Extract video IDs from page (simplified)
            video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)

            # Remove duplicates and limit
            video_ids = list(dict.fromkeys(video_ids))[:max_results]

            return [{'id': vid} for vid in video_ids]

        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return []

    def _get_video_details(self, video_id: str) -> Optional[Dict]:
        """
        Get video details from YouTube

        Args:
            video_id: YouTube video ID

        Returns:
            Video details dictionary
        """
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })

            if response.status_code == 200:
                # Extract title and description (simplified regex approach)
                title_match = re.search(r'"title":"([^"]+)"', response.text)
                desc_match = re.search(r'"shortDescription":"([^"]+)"', response.text)

                return {
                    'title': title_match.group(1) if title_match else 'Unknown',
                    'description': desc_match.group(1) if desc_match else '',
                    'views': 0  # Could be extracted with more complex parsing
                }

            return None

        except Exception as e:
            logger.error(f"Error getting video details for {video_id}: {e}")
            return None

    def _extract_prompts_from_text(self, text: str) -> List[str]:
        """
        Extract potential prompts from text using pattern matching

        Args:
            text: Text to analyze

        Returns:
            List of extracted prompts
        """
        if not text:
            return []

        prompts = []

        # Pattern 1: Text in quotes that looks like prompts
        quote_patterns = re.findall(r'"([^"]{20,300})"', text)
        prompts.extend([p for p in quote_patterns if self._is_likely_prompt(p)])

        # Pattern 2: Lines starting with "Prompt:" or "prompt:"
        prompt_lines = re.findall(r'[Pp]rompt:\s*(.+?)(?:\n|$)', text)
        prompts.extend([p.strip() for p in prompt_lines if len(p.strip()) > 20])

        # Pattern 3: Code blocks (often contain prompts)
        code_blocks = re.findall(r'```(?:\w+)?\n(.+?)\n```', text, re.DOTALL)
        prompts.extend([p.strip() for p in code_blocks if self._is_likely_prompt(p)])

        # Remove duplicates and clean
        prompts = list(dict.fromkeys(prompts))
        prompts = [p.strip() for p in prompts if len(p.strip()) > 20]

        return prompts[:10]  # Limit to top 10 per source

    def _is_likely_prompt(self, text: str) -> bool:
        """
        Check if text is likely a video generation prompt

        Args:
            text: Text to check

        Returns:
            True if likely a prompt
        """
        if len(text) < 20 or len(text) > 500:
            return False

        # Keywords that indicate video generation prompts
        keywords = [
            'cinematic', 'camera', 'shot', 'scene', 'video', 'motion',
            '4k', 'hd', 'professional', 'lighting', 'color', 'style',
            'runway', 'veo', 'sora', 'pika', 'gen-', 'zoom', 'pan'
        ]

        text_lower = text.lower()
        keyword_count = sum(1 for kw in keywords if kw in text_lower)

        return keyword_count >= 2

    def _is_prompt_related(self, text: str) -> bool:
        """
        Check if text is related to prompt engineering or video generation

        Args:
            text: Text to check

        Returns:
            True if prompt-related
        """
        if not text:
            return False

        keywords = [
            'prompt', 'runway', 'veo', 'sora', 'pika', 'video generation',
            'ai video', 'text to video', 'gen-3', 'gen-4', 'prompt engineering'
        ]

        text_lower = text.lower()
        return any(kw in text_lower for kw in keywords)

    def harvest_all(self) -> Dict[str, List[Dict]]:
        """
        Harvest from all sources

        Returns:
            Dictionary with results from all sources
        """
        logger.info("="*60)
        logger.info("STARTING FULL HARVEST CYCLE")
        logger.info("="*60)

        results = {
            'reddit': [],
            'youtube': [],
            'web': [],
            'timestamp': datetime.now().isoformat()
        }

        # Harvest from Reddit
        try:
            results['reddit'] = self.harvest_reddit()
        except Exception as e:
            logger.error(f"Reddit harvesting failed: {e}")

        # Harvest from YouTube
        try:
            results['youtube'] = self.harvest_youtube()
        except Exception as e:
            logger.error(f"YouTube harvesting failed: {e}")

        # Harvest from Web
        try:
            results['web'] = self.harvest_web()
        except Exception as e:
            logger.error(f"Web harvesting failed: {e}")

        total = len(results['reddit']) + len(results['youtube']) + len(results['web'])

        logger.info("="*60)
        logger.info(f"HARVEST COMPLETE: {total} items collected")
        logger.info(f"  Reddit: {len(results['reddit'])}")
        logger.info(f"  YouTube: {len(results['youtube'])}")
        logger.info(f"  Web: {len(results['web'])}")
        logger.info("="*60)

        return results


if __name__ == '__main__':
    # Test harvester
    print("Prompt Harvester - Test Mode")
    print("="*60)

    harvester = PromptHarvester()

    # Test with small limits
    print("\nTesting Reddit harvesting...")
    reddit_results = harvester.harvest_reddit(subreddits=['PromptEngineering'], limit=5)
    print(f"Reddit: {len(reddit_results)} items")

    print("\nTesting YouTube harvesting...")
    youtube_results = harvester.harvest_youtube(search_queries=['Runway Gen-4'], max_results=5)
    print(f"YouTube: {len(youtube_results)} items")

    print("\nTesting Web harvesting...")
    web_results = harvester.harvest_web()
    print(f"Web: {len(web_results)} items")

    print("\n" + "="*60)
    print(f"Total collected: {len(reddit_results) + len(youtube_results) + len(web_results)}")
