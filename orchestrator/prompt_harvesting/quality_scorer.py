#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quality Scorer Module - Local Quality Assessment
Evaluates prompt quality without API calls for cost-effective scoring
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import math

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class QualityScorer:
    """
    Local quality scoring for prompts (no API costs)
    """

    # Quality keywords by category
    QUALITY_KEYWORDS = {
        'high': ['4k', '8k', 'ultra', 'professional', 'cinematic', 'premium', 'hd', 'uhd'],
        'technical': ['camera', 'lighting', 'color grading', 'shot', 'angle', 'focus', 'depth of field'],
        'motion': ['pan', 'zoom', 'tilt', 'dolly', 'tracking', 'smooth', 'slow motion', 'time-lapse'],
        'style': ['aesthetic', 'mood', 'atmosphere', 'tone', 'style', 'vibe'],
        'detail': ['detailed', 'intricate', 'complex', 'rich', 'vivid', 'sharp']
    }

    VIDEO_MODELS = {
        'runway': ['runway', 'gen-3', 'gen-4', 'gen3', 'gen4'],
        'veo': ['veo', 'veo-3', 'veo-2'],
        'sora': ['sora', 'openai'],
        'pika': ['pika', 'pikalabs']
    }

    def __init__(self):
        """Initialize the quality scorer"""
        logger.info("[QualityScorer] Initialized")

    def score_community_engagement(self, upvotes: int, comments: int) -> float:
        """
        Calculate community engagement score

        Args:
            upvotes: Number of upvotes/likes
            comments: Number of comments

        Returns:
            Engagement score (0-10)
        """
        try:
            # Formula: upvotes + (comments * 0.5)
            raw_score = upvotes + (comments * 0.5)

            # Normalize to 0-10 scale using logarithmic scaling
            if raw_score <= 0:
                return 0.0

            # Log scale for better distribution
            normalized = math.log10(raw_score + 1) * 3

            # Cap at 10
            score = min(normalized, 10.0)

            return round(score, 2)

        except Exception as e:
            logger.error(f"Error calculating engagement score: {e}")
            return 5.0

    def score_video_quality_estimated(self, text: str) -> float:
        """
        Estimate video quality from text description

        Args:
            text: Description text to analyze

        Returns:
            Quality score (0-10)
        """
        if not text:
            return 5.0

        text_lower = text.lower()
        score = 5.0  # Base score

        # Check for quality keywords
        keyword_bonus = 0
        for category, keywords in self.QUALITY_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > 0:
                if category == 'high':
                    keyword_bonus += matches * 0.5
                elif category == 'technical':
                    keyword_bonus += matches * 0.3
                elif category == 'motion':
                    keyword_bonus += matches * 0.2
                else:
                    keyword_bonus += matches * 0.1

        score += min(keyword_bonus, 4.0)

        # Bonus for length (detailed descriptions)
        word_count = len(text.split())
        if 30 <= word_count <= 150:
            score += 0.5
        elif 150 < word_count <= 300:
            score += 0.3

        # Penalty for too short or too long
        if word_count < 10:
            score -= 1.0
        elif word_count > 500:
            score -= 0.5

        # Bonus for technical specifications
        if re.search(r'\d+k', text_lower):  # 4k, 8k, etc.
            score += 0.5
        if 'fps' in text_lower or 'frame' in text_lower:
            score += 0.3
        if 'resolution' in text_lower or 'aspect ratio' in text_lower:
            score += 0.3

        # Cap at 10
        score = min(score, 10.0)
        score = max(score, 0.0)

        return round(score, 2)

    def score_recency(self, timestamp: str, max_age_days: int = 90) -> float:
        """
        Score based on how recent the prompt is

        Args:
            timestamp: ISO format timestamp
            max_age_days: Maximum age in days for full score

        Returns:
            Recency score (0-10)
        """
        try:
            if not timestamp:
                return 5.0

            # Parse timestamp
            if isinstance(timestamp, str):
                try:
                    post_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except:
                    post_date = datetime.now() - timedelta(days=30)
            else:
                post_date = timestamp

            now = datetime.now()
            if post_date.tzinfo:
                now = datetime.now(post_date.tzinfo)

            age_days = (now - post_date).days

            # Scoring curve
            if age_days <= 7:
                score = 10.0
            elif age_days <= 30:
                score = 9.0
            elif age_days <= 60:
                score = 7.5
            elif age_days <= max_age_days:
                score = 5.0
            elif age_days <= 180:
                score = 3.0
            else:
                score = 1.0

            return score

        except Exception as e:
            logger.error(f"Error calculating recency score: {e}")
            return 5.0

    def score_prompt_text(self, prompt: str) -> float:
        """
        Score a single prompt text based on local heuristics

        Args:
            prompt: Prompt text to score

        Returns:
            Quality score (0-10)
        """
        if not prompt or len(prompt) < 10:
            return 2.0

        score = 5.0  # Base score
        prompt_lower = prompt.lower()

        # Length check (good prompts are detailed but not too long)
        length = len(prompt)
        if 50 <= length <= 200:
            score += 1.0
        elif 200 < length <= 400:
            score += 0.5
        elif length < 20:
            score -= 2.0

        # Check for video generation keywords
        video_keywords = ['camera', 'shot', 'scene', 'video', 'motion', 'cinematic']
        keyword_matches = sum(1 for kw in video_keywords if kw in prompt_lower)
        score += min(keyword_matches * 0.4, 2.0)

        # Check for quality indicators
        quality_matches = sum(1 for kw in self.QUALITY_KEYWORDS['high'] if kw in prompt_lower)
        score += min(quality_matches * 0.5, 1.5)

        # Check for technical details
        technical_matches = sum(1 for kw in self.QUALITY_KEYWORDS['technical'] if kw in prompt_lower)
        score += min(technical_matches * 0.3, 1.5)

        # Bonus for specific model mentions
        has_model = any(any(m in prompt_lower for m in models) for models in self.VIDEO_MODELS.values())
        if has_model:
            score += 0.5

        # Check for style and mood descriptors
        style_words = ['aesthetic', 'mood', 'atmosphere', 'style', 'tone']
        if any(word in prompt_lower for word in style_words):
            score += 0.5

        # Penalty for vague language
        vague_words = ['something', 'maybe', 'kind of', 'sort of', 'like']
        vague_count = sum(1 for word in vague_words if word in prompt_lower)
        score -= vague_count * 0.3

        # Cap at 10
        score = min(score, 10.0)
        score = max(score, 0.0)

        return round(score, 2)

    def detect_model_type(self, text: str) -> Optional[str]:
        """
        Detect which video generation model the prompt is for

        Args:
            text: Text to analyze

        Returns:
            Model name or None
        """
        if not text:
            return None

        text_lower = text.lower()

        for model, keywords in self.VIDEO_MODELS.items():
            if any(kw in text_lower for kw in keywords):
                return model

        return None

    def combined_quality_score(self, prompt_obj: Dict) -> Dict:
        """
        Calculate combined quality score from all factors

        Args:
            prompt_obj: Dictionary containing prompt data with fields:
                - text or prompts: The prompt text
                - upvotes: Number of upvotes (optional)
                - comments: Number of comments (optional)
                - created_utc or harvested_at: Timestamp (optional)
                - gemini_score: Gemini analysis score (optional)

        Returns:
            Dictionary with detailed scoring breakdown
        """
        # Extract prompt text
        prompt_text = ""
        if 'prompts' in prompt_obj and prompt_obj['prompts']:
            prompt_text = prompt_obj['prompts'][0] if isinstance(prompt_obj['prompts'], list) else prompt_obj['prompts']
        elif 'text' in prompt_obj:
            prompt_text = prompt_obj['text']
        elif 'description' in prompt_obj:
            prompt_text = prompt_obj['description']

        # Calculate individual scores
        prompt_score = self.score_prompt_text(prompt_text) if prompt_text else 5.0

        community_score = self.score_community_engagement(
            prompt_obj.get('upvotes', 0),
            prompt_obj.get('comments', 0)
        )

        timestamp = prompt_obj.get('created_utc') or prompt_obj.get('harvested_at') or datetime.now().isoformat()
        recency_score = self.score_recency(timestamp)

        quality_estimate = self.score_video_quality_estimated(prompt_text)

        # Get Gemini score if available
        gemini_score = prompt_obj.get('gemini_score', 0)
        if isinstance(prompt_obj.get('analysis'), dict):
            gemini_score = prompt_obj['analysis'].get('overall_score', 0)

        # Combined score with weights
        if gemini_score > 0:
            # With Gemini: 40% Gemini + 30% Community + 20% Quality + 10% Recency
            combined = (
                gemini_score * 0.40 +
                community_score * 0.30 +
                quality_estimate * 0.20 +
                recency_score * 0.10
            )
        else:
            # Without Gemini: 40% Prompt + 30% Community + 20% Quality + 10% Recency
            combined = (
                prompt_score * 0.40 +
                community_score * 0.30 +
                quality_estimate * 0.20 +
                recency_score * 0.10
            )

        # Detect model type
        model_type = self.detect_model_type(prompt_text)

        result = {
            'combined_score': round(combined, 2),
            'breakdown': {
                'prompt_score': prompt_score,
                'community_score': community_score,
                'recency_score': recency_score,
                'quality_estimate': quality_estimate,
                'gemini_score': gemini_score if gemini_score > 0 else None
            },
            'weights': {
                'gemini': 0.40 if gemini_score > 0 else 0.0,
                'prompt': 0.40 if gemini_score == 0 else 0.0,
                'community': 0.30,
                'quality': 0.20,
                'recency': 0.10
            },
            'model_type': model_type,
            'scored_at': datetime.now().isoformat()
        }

        return result

    def rank_prompts(self, prompts: List[Dict], min_score: float = 0.0) -> List[Dict]:
        """
        Rank prompts by quality score

        Args:
            prompts: List of prompt dictionaries
            min_score: Minimum score threshold

        Returns:
            Sorted list of prompts with scores
        """
        scored_prompts = []

        for prompt in prompts:
            score_data = self.combined_quality_score(prompt)
            combined_score = score_data['combined_score']

            if combined_score >= min_score:
                prompt['quality_score'] = combined_score
                prompt['score_breakdown'] = score_data
                scored_prompts.append(prompt)

        # Sort by score (highest first)
        scored_prompts.sort(key=lambda x: x['quality_score'], reverse=True)

        logger.info(f"[QualityScorer] Ranked {len(scored_prompts)} prompts (min score: {min_score})")

        return scored_prompts

    def get_quality_stats(self, prompts: List[Dict]) -> Dict:
        """
        Get statistical summary of prompt quality

        Args:
            prompts: List of prompt dictionaries

        Returns:
            Statistics dictionary
        """
        if not prompts:
            return {
                'count': 0,
                'average': 0.0,
                'median': 0.0,
                'high_quality': 0,
                'medium_quality': 0,
                'low_quality': 0
            }

        scores = []
        for prompt in prompts:
            if 'quality_score' not in prompt:
                score_data = self.combined_quality_score(prompt)
                score = score_data['combined_score']
            else:
                score = prompt['quality_score']
            scores.append(score)

        scores.sort()
        count = len(scores)
        avg = sum(scores) / count if count > 0 else 0
        median = scores[count // 2] if count > 0 else 0

        # Quality tiers
        high_quality = sum(1 for s in scores if s >= 7.5)
        medium_quality = sum(1 for s in scores if 5.0 <= s < 7.5)
        low_quality = sum(1 for s in scores if s < 5.0)

        return {
            'count': count,
            'average': round(avg, 2),
            'median': round(median, 2),
            'min': round(min(scores), 2),
            'max': round(max(scores), 2),
            'high_quality': high_quality,
            'medium_quality': medium_quality,
            'low_quality': low_quality,
            'high_quality_pct': round(high_quality / count * 100, 1),
            'medium_quality_pct': round(medium_quality / count * 100, 1),
            'low_quality_pct': round(low_quality / count * 100, 1)
        }


if __name__ == '__main__':
    # Test quality scorer
    print("Quality Scorer - Test Mode")
    print("="*60)

    scorer = QualityScorer()

    # Test prompt
    test_prompt = {
        'text': 'A cinematic 4K shot of a futuristic city at night, camera slowly panning right',
        'prompts': ['Cinematic 4K shot, city at night, slow pan'],
        'upvotes': 150,
        'comments': 25,
        'created_utc': datetime.now().isoformat()
    }

    print("\nTesting combined quality score...")
    result = scorer.combined_quality_score(test_prompt)
    print(f"Combined Score: {result['combined_score']}/10")
    print(f"Breakdown: {result['breakdown']}")
    print(f"Model Type: {result['model_type']}")

    # Test multiple prompts
    test_prompts = [
        {'text': 'Amazing video', 'upvotes': 10, 'comments': 2},
        {'text': 'Professional 4K cinematic shot with detailed lighting and camera movement', 'upvotes': 200, 'comments': 50},
        {'text': 'x', 'upvotes': 1, 'comments': 0}
    ]

    print("\nTesting ranking...")
    ranked = scorer.rank_prompts(test_prompts, min_score=3.0)
    for i, p in enumerate(ranked, 1):
        print(f"{i}. Score: {p['quality_score']:.2f} - {p['text'][:50]}")

    print("\nTesting statistics...")
    stats = scorer.get_quality_stats(ranked)
    print(f"Average: {stats['average']}")
    print(f"High Quality: {stats['high_quality']} ({stats['high_quality_pct']}%)")

    print("\n" + "="*60)
