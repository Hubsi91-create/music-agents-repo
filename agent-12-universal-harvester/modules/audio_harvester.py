"""
Audio Harvester - Agent 2 AudioCurator Integration

Harvests audio data from Spotify, YouTube Music, Reddit, and SoundCloud
to identify high-quality tracks for video production.

Author: Universal Harvester System
Version: 1.0.0
"""

from typing import List, Dict, Any
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import praw
from datetime import datetime
import logging
from .base_harvester import BaseHarvester

logging.basicConfig(level=logging.INFO)


class AudioHarvester(BaseHarvester):
    """
    Harvests audio/music data from multiple platforms.

    Data Sources:
    - Spotify Charts API
    - YouTube Music Trending
    - Reddit Music Communities
    - SoundCloud Trending
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__("audio_harvester", config)

        # API credentials
        import os
        self.spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')

        # Initialize Spotify
        if self.spotify_client_id and self.spotify_client_secret:
            auth_manager = SpotifyClientCredentials(
                client_id=self.spotify_client_id,
                client_secret=self.spotify_client_secret
            )
            self.spotify = spotipy.Spotify(auth_manager=auth_manager)
        else:
            self.spotify = None
            self.logger.warning("Spotify credentials not found")

        # Initialize Reddit
        if self.reddit_client_id and self.reddit_client_secret:
            self.reddit = praw.Reddit(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent='AudioHarvester/1.0'
            )
        else:
            self.reddit = None

    def get_data_sources(self) -> List[Dict[str, str]]:
        """Get audio data sources."""
        sources = []

        if 'spotify' in self.enabled_sources and self.spotify:
            sources.append({
                'name': 'Spotify Charts',
                'url': 'https://api.spotify.com/v1/playlists',
                'type': 'api'
            })

        if 'youtube_music' in self.enabled_sources:
            sources.append({
                'name': 'YouTube Music',
                'url': 'https://music.youtube.com',
                'type': 'api'
            })

        if 'reddit' in self.enabled_sources and self.reddit:
            sources.extend([
                {'name': 'Reddit Music', 'url': 'r/Music', 'type': 'scrape'},
                {'name': 'Reddit IndieMusic', 'url': 'r/indiemusic', 'type': 'scrape'},
                {'name': 'Reddit HipHop', 'url': 'r/hiphopheads', 'type': 'scrape'},
                {'name': 'Reddit Electronic', 'url': 'r/electronicmusic', 'type': 'scrape'}
            ])

        if 'soundcloud' in self.enabled_sources:
            sources.append({
                'name': 'SoundCloud Trending',
                'url': 'https://soundcloud.com/charts',
                'type': 'scrape'
            })

        return sources

    def extract_raw_data(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract audio data from source."""
        source_name = source['name']

        try:
            if 'Spotify' in source_name:
                return self._harvest_spotify()
            elif 'YouTube Music' in source_name:
                return self._harvest_youtube_music()
            elif 'Reddit' in source_name:
                return self._harvest_reddit(source['url'])
            elif 'SoundCloud' in source_name:
                return self._harvest_soundcloud()
            else:
                return []

        except Exception as e:
            self.logger.error(f"Failed to extract from {source_name}: {str(e)}")
            return []

    def parse_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse and structure audio data."""
        parsed_data = []

        for item in raw_data:
            try:
                parsed_item = {
                    'id': item.get('id', ''),
                    'title': item.get('title', ''),
                    'artist': item.get('artist', ''),
                    'platform': item.get('platform', 'unknown'),
                    'audio_features': {
                        'bpm': item.get('bpm', 0),
                        'key': item.get('key', ''),
                        'energy': item.get('energy', 0.0),
                        'danceability': item.get('danceability', 0.0),
                        'duration_ms': item.get('duration_ms', 0)
                    },
                    'popularity': {
                        'streams': item.get('streams', 0),
                        'plays': item.get('plays', 0),
                        'likes': item.get('likes', 0)
                    },
                    'metadata': {
                        'genre': item.get('genre', 'unknown'),
                        'mood': item.get('mood', 'neutral'),
                        'release_date': item.get('release_date', '')
                    },
                    'source_url': item.get('url', ''),
                    'harvested_at': datetime.now().isoformat()
                }
                parsed_data.append(parsed_item)

            except Exception as e:
                self.logger.error(f"Failed to parse audio item: {str(e)}")
                continue

        return parsed_data

    def score_data_quality(self, data_item: Dict[str, Any]) -> float:
        """
        Score audio quality for video production.

        Scoring:
        - 40% = Stream Count / Popularity
        - 30% = Technical Quality (BPM consistency, energy)
        - 20% = Community Rating
        - 10% = Recency
        """
        try:
            # Popularity score (0-4.0)
            popularity = data_item.get('popularity', {})
            streams = popularity.get('streams', 0) + popularity.get('plays', 0)
            likes = popularity.get('likes', 0)

            import math
            popularity_score = 0
            if streams > 0:
                popularity_score += min(3.0, math.log10(streams) / 2)
            if likes > 0:
                popularity_score += min(1.0, math.log10(likes) / 2)

            # Technical quality score (0-3.0)
            audio_features = data_item.get('audio_features', {})
            bpm = audio_features.get('bpm', 0)
            energy = audio_features.get('energy', 0.0)
            danceability = audio_features.get('danceability', 0.0)

            tech_score = 0
            # BPM in good range for videos (80-140)
            if 80 <= bpm <= 140:
                tech_score += 1.0
            # High energy is good for videos
            tech_score += energy * 1.0
            # Danceability adds appeal
            tech_score += danceability * 1.0

            # Community rating (0-2.0)
            # Based on likes relative to streams
            if streams > 0:
                engagement_ratio = likes / streams
                community_score = min(2.0, engagement_ratio * 100)
            else:
                community_score = 0.5

            # Recency score (0-1.0)
            release_date = data_item.get('metadata', {}).get('release_date', '')
            if release_date:
                try:
                    rel_date = datetime.fromisoformat(release_date.replace('Z', '+00:00'))
                    age_days = (datetime.now() - rel_date.replace(tzinfo=None)).days
                    if age_days <= 30:
                        recency_score = 1.0
                    elif age_days <= 90:
                        recency_score = 0.7
                    else:
                        recency_score = 0.3
                except:
                    recency_score = 0.5
            else:
                recency_score = 0.5

            total_score = popularity_score + tech_score + community_score + recency_score
            return min(10.0, max(0.0, total_score))

        except Exception as e:
            self.logger.error(f"Failed to score audio: {str(e)}")
            return 0.0

    def get_analysis_prompt(self, data: List[Dict[str, Any]]) -> str:
        """Generate Gemini analysis prompt for audio."""
        return f"""Analyze these {len(data)} audio tracks for video production and provide:

1. BEST TRACKS FOR VIDEO (Top 20 with scores)
   - Perfect BPM range for video editing
   - High energy and danceability
   - Viral potential assessment

2. BPM/MOOD RECOMMENDATIONS BY GENRE
   - Optimal BPM ranges per genre
   - Mood pairings (energetic, chill, dramatic)
   - Video style recommendations

3. PRODUCTION QUALITY TRENDS
   - Audio characteristics of popular tracks
   - Technical quality patterns
   - Production style trends

4. AUDIO PAIRING RECOMMENDATIONS
   - Best tracks for different video types
   - Music-visual style matching
   - Audience appeal predictions

5. CREATOR ACTIONABLE INSIGHTS
   - Track selection strategy
   - Genre recommendations
   - Licensing/usage considerations

Return results as structured JSON with track IDs and scores."""

    # ============================================================
    # PLATFORM-SPECIFIC HARVESTERS
    # ============================================================

    def _harvest_spotify(self) -> List[Dict[str, Any]]:
        """Harvest Spotify trending tracks."""
        if not self.spotify:
            return []

        try:
            # Get Top 50 Global playlist
            playlist_id = '37i9dQZEVXbMDoHDwVN2tF'  # Global Top 50
            results = self.spotify.playlist_tracks(playlist_id, limit=50)

            items = []
            for track_data in results['items']:
                track = track_data['track']

                # Get audio features
                try:
                    features = self.spotify.audio_features(track['id'])[0]
                    bpm = features.get('tempo', 0)
                    energy = features.get('energy', 0.0)
                    danceability = features.get('danceability', 0.0)
                    key = features.get('key', 0)
                except:
                    bpm = 0
                    energy = 0.0
                    danceability = 0.0
                    key = 0

                items.append({
                    'id': track['id'],
                    'title': track['name'],
                    'artist': ', '.join([a['name'] for a in track['artists']]),
                    'platform': 'spotify',
                    'bpm': int(bpm),
                    'key': str(key),
                    'energy': energy,
                    'danceability': danceability,
                    'duration_ms': track['duration_ms'],
                    'streams': track['popularity'] * 1000,  # Estimate
                    'likes': track['popularity'] * 100,
                    'genre': 'pop',  # Spotify doesn't always provide genre
                    'url': track['external_urls']['spotify'],
                    'release_date': track['album']['release_date']
                })

            self.logger.info(f"Harvested {len(items)} Spotify tracks")
            return items

        except Exception as e:
            self.logger.error(f"Spotify harvest failed: {str(e)}")
            return []

    def _harvest_youtube_music(self) -> List[Dict[str, Any]]:
        """Harvest YouTube Music trending (placeholder)."""
        self.logger.warning("YouTube Music harvesting requires ytmusicapi")
        # Would require ytmusicapi library
        return []

    def _harvest_reddit(self, subreddit_name: str) -> List[Dict[str, Any]]:
        """Harvest music recommendations from Reddit."""
        if not self.reddit:
            return []

        try:
            subreddit = self.reddit.subreddit(subreddit_name.replace('r/', ''))
            items = []

            for post in subreddit.hot(limit=50):
                # Extract track info from title (basic parsing)
                title = post.title

                items.append({
                    'id': f"reddit_{post.id}",
                    'title': title,
                    'artist': 'Unknown',
                    'platform': 'reddit',
                    'bpm': 0,
                    'key': '',
                    'energy': 0.5,
                    'danceability': 0.5,
                    'duration_ms': 0,
                    'streams': 0,
                    'likes': post.score,
                    'genre': subreddit_name.split('/')[-1],
                    'url': f"https://reddit.com{post.permalink}",
                    'release_date': datetime.fromtimestamp(post.created_utc).isoformat()
                })

            self.logger.info(f"Harvested {len(items)} Reddit music posts")
            return items

        except Exception as e:
            self.logger.error(f"Reddit harvest failed: {str(e)}")
            return []

    def _harvest_soundcloud(self) -> List[Dict[str, Any]]:
        """Harvest SoundCloud trending (placeholder)."""
        self.logger.warning("SoundCloud harvesting requires API access")
        return []

    def __repr__(self) -> str:
        return f"<AudioHarvester sources={len(self.enabled_sources)}>"