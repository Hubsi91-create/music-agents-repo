#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prompt Analyzer Module - Gemini-based Analysis
Uses Google Gemini API for intelligent prompt analysis and improvement
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("google-generativeai not installed. Gemini analysis disabled.")

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class PromptAnalyzer:
    """
    Analyzes prompts using Google Gemini API
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """
        Initialize the analyzer with Gemini API

        Args:
            model_name: Gemini model to use
        """
        self.model_name = model_name
        self.model = None

        if GEMINI_AVAILABLE:
            self._init_gemini()
        else:
            logger.error("[Gemini] google-generativeai library not installed")

    def _init_gemini(self):
        """Initialize Gemini API client"""
        try:
            api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(self.model_name)
                logger.info(f"[Gemini] Initialized with model: {self.model_name}")
            else:
                logger.warning("[Gemini] No API key found in environment variables")
                logger.info("[Gemini] Set GEMINI_API_KEY or GOOGLE_API_KEY to enable")
        except Exception as e:
            logger.error(f"[Gemini] Failed to initialize: {e}")

    def analyze_prompt_quality(self, prompt_text: str) -> Dict:
        """
        Analyze prompt quality using Gemini

        Args:
            prompt_text: The prompt to analyze

        Returns:
            Dictionary with quality metrics and analysis
        """
        if not self.model:
            logger.warning("[Gemini] Model not initialized. Returning fallback analysis.")
            return self._fallback_analysis(prompt_text)

        try:
            analysis_prompt = f"""
You are an expert in video generation prompt engineering for AI models like Runway Gen-4, Veo 3.1, Sora, and Pika.

Analyze the following prompt and provide a structured evaluation:

PROMPT TO ANALYZE:
"{prompt_text}"

Provide your analysis in the following JSON format:
{{
  "clarity_score": <1-10>,
  "specificity_score": <1-10>,
  "technical_accuracy_score": <1-10>,
  "overall_score": <1-10>,
  "strengths": ["list", "of", "strengths"],
  "weaknesses": ["list", "of", "weaknesses"],
  "keywords": ["important", "keywords", "found"],
  "style_detected": "<cinematic/abstract/realistic/etc>",
  "model_suitability": {{"runway": <1-10>, "veo": <1-10>, "sora": <1-10>}},
  "recommendation": "<brief recommendation>"
}}

Scoring criteria:
- Clarity (1-10): How clear and understandable is the prompt?
- Specificity (1-10): How detailed and specific is the description?
- Technical Accuracy (1-10): Are technical terms used correctly?
- Overall (1-10): Combined quality assessment

Respond ONLY with the JSON object, no additional text.
"""

            response = self.model.generate_content(analysis_prompt)
            result_text = response.text.strip()

            # Clean markdown code blocks if present
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.startswith('```'):
                result_text = result_text[3:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]

            result_text = result_text.strip()

            # Parse JSON response
            analysis = json.loads(result_text)

            # Add metadata
            analysis['analyzed_at'] = datetime.now().isoformat()
            analysis['model_used'] = self.model_name
            analysis['prompt_length'] = len(prompt_text)

            logger.info(f"[Gemini] Analysis complete - Score: {analysis.get('overall_score', 0)}/10")

            return analysis

        except json.JSONDecodeError as e:
            logger.error(f"[Gemini] Failed to parse response as JSON: {e}")
            logger.debug(f"Response text: {result_text[:200]}")
            return self._fallback_analysis(prompt_text)

        except Exception as e:
            logger.error(f"[Gemini] Analysis error: {e}")
            return self._fallback_analysis(prompt_text)

    def extract_patterns(self, prompts: List[Dict]) -> Dict:
        """
        Extract common patterns from a collection of prompts

        Args:
            prompts: List of prompt dictionaries with 'text' or 'prompts' field

        Returns:
            Dictionary with pattern analysis
        """
        if not self.model:
            logger.warning("[Gemini] Model not initialized. Returning fallback patterns.")
            return self._fallback_patterns(prompts)

        try:
            # Collect all prompt texts
            all_prompts = []
            for item in prompts[:50]:  # Limit to avoid token limits
                if 'prompts' in item and item['prompts']:
                    all_prompts.extend(item['prompts'][:3])
                elif 'text' in item:
                    all_prompts.append(item['text'])

            if not all_prompts:
                return {'error': 'No prompts to analyze'}

            prompts_text = '\n\n'.join([f"{i+1}. {p[:200]}" for i, p in enumerate(all_prompts[:20])])

            pattern_prompt = f"""
You are an expert in prompt engineering pattern analysis for AI video generation.

Analyze these prompts and identify common successful patterns:

PROMPTS:
{prompts_text}

Provide your analysis in JSON format:
{{
  "common_keywords": ["list", "of", "frequent", "keywords"],
  "structure_patterns": ["pattern1: description", "pattern2: description"],
  "style_trends": ["trend1", "trend2"],
  "technical_terms": ["term1", "term2"],
  "best_practices": ["practice1", "practice2"],
  "model_specific_patterns": {{
    "runway": ["pattern1", "pattern2"],
    "veo": ["pattern1", "pattern2"]
  }}
}}

Focus on patterns that appear in multiple prompts.
Respond ONLY with the JSON object.
"""

            response = self.model.generate_content(pattern_prompt)
            result_text = response.text.strip()

            # Clean markdown
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.startswith('```'):
                result_text = result_text[3:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]

            patterns = json.loads(result_text.strip())
            patterns['analyzed_prompts_count'] = len(all_prompts)
            patterns['extracted_at'] = datetime.now().isoformat()

            logger.info(f"[Gemini] Pattern extraction complete - {len(patterns.get('common_keywords', []))} keywords found")

            return patterns

        except Exception as e:
            logger.error(f"[Gemini] Pattern extraction error: {e}")
            return self._fallback_patterns(prompts)

    def suggest_improvements(self, prompt: str, score: float) -> Dict:
        """
        Suggest improvements for a prompt

        Args:
            prompt: The prompt to improve
            score: Current quality score

        Returns:
            Dictionary with improved prompt and suggestions
        """
        if not self.model:
            logger.warning("[Gemini] Model not initialized. Returning fallback suggestions.")
            return self._fallback_improvements(prompt, score)

        if score >= 8.0:
            return {
                'improved_prompt': prompt,
                'reason': 'Prompt already high quality',
                'confidence': 1.0,
                'suggestions': []
            }

        try:
            improvement_prompt = f"""
You are an expert in video generation prompt engineering.

Current prompt (score {score}/10):
"{prompt}"

Improve this prompt to make it more effective for AI video generation (Runway, Veo, Sora).

Respond in JSON format:
{{
  "improved_prompt": "<your improved version>",
  "reason": "<why your version is better>",
  "confidence": <0.0-1.0>,
  "suggestions": ["specific suggestion 1", "specific suggestion 2"],
  "changes_made": ["change1", "change2"]
}}

Focus on:
1. Adding technical details (camera angles, lighting, motion)
2. Improving clarity and specificity
3. Using effective video generation keywords
4. Maintaining the original intent

Respond ONLY with the JSON object.
"""

            response = self.model.generate_content(improvement_prompt)
            result_text = response.text.strip()

            # Clean markdown
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.startswith('```'):
                result_text = result_text[3:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]

            improvements = json.loads(result_text.strip())
            improvements['original_prompt'] = prompt
            improvements['original_score'] = score
            improvements['suggested_at'] = datetime.now().isoformat()

            logger.info(f"[Gemini] Improvements generated - Confidence: {improvements.get('confidence', 0)}")

            return improvements

        except Exception as e:
            logger.error(f"[Gemini] Improvement generation error: {e}")
            return self._fallback_improvements(prompt, score)

    def categorize_prompt(self, prompt: str) -> Dict:
        """
        Categorize a prompt by genre, model, and quality level

        Args:
            prompt: The prompt to categorize

        Returns:
            Dictionary with categorization results
        """
        if not self.model:
            logger.warning("[Gemini] Model not initialized. Returning fallback categorization.")
            return self._fallback_categorization(prompt)

        try:
            categorization_prompt = f"""
Categorize this video generation prompt:

PROMPT: "{prompt}"

Respond in JSON format:
{{
  "genre": "<action/drama/music/documentary/abstract/nature/etc>",
  "sub_genre": "<more specific genre>",
  "best_model": "<runway/veo/sora/pika>",
  "quality_level": "<low/mid/high/premium>",
  "complexity": "<simple/moderate/complex>",
  "estimated_duration": "<short/medium/long>",
  "primary_elements": ["element1", "element2"],
  "mood": ["mood1", "mood2"],
  "confidence": <0.0-1.0>
}}

Base your assessment on:
- Genre: The content type and subject matter
- Best Model: Which AI model would handle this best
- Quality Level: The production quality implied
- Complexity: How complex the scene is

Respond ONLY with the JSON object.
"""

            response = self.model.generate_content(categorization_prompt)
            result_text = response.text.strip()

            # Clean markdown
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.startswith('```'):
                result_text = result_text[3:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]

            categorization = json.loads(result_text.strip())
            categorization['categorized_at'] = datetime.now().isoformat()

            logger.info(f"[Gemini] Categorization complete - Genre: {categorization.get('genre', 'unknown')}")

            return categorization

        except Exception as e:
            logger.error(f"[Gemini] Categorization error: {e}")
            return self._fallback_categorization(prompt)

    def _fallback_analysis(self, prompt_text: str) -> Dict:
        """Fallback analysis when Gemini is unavailable"""
        words = prompt_text.split()
        has_technical = any(term in prompt_text.lower() for term in ['4k', 'cinematic', 'camera', 'lighting'])

        return {
            'clarity_score': 5,
            'specificity_score': 5,
            'technical_accuracy_score': 7 if has_technical else 4,
            'overall_score': 5,
            'strengths': ['Contains text'],
            'weaknesses': ['Analysis unavailable - Gemini not configured'],
            'keywords': [],
            'style_detected': 'unknown',
            'model_suitability': {'runway': 5, 'veo': 5, 'sora': 5},
            'recommendation': 'Configure Gemini API for detailed analysis',
            'analyzed_at': datetime.now().isoformat(),
            'model_used': 'fallback',
            'prompt_length': len(prompt_text)
        }

    def _fallback_patterns(self, prompts: List[Dict]) -> Dict:
        """Fallback pattern extraction"""
        return {
            'common_keywords': [],
            'structure_patterns': [],
            'style_trends': [],
            'technical_terms': [],
            'best_practices': [],
            'model_specific_patterns': {'runway': [], 'veo': []},
            'analyzed_prompts_count': len(prompts),
            'extracted_at': datetime.now().isoformat(),
            'note': 'Fallback mode - Configure Gemini API for pattern extraction'
        }

    def _fallback_improvements(self, prompt: str, score: float) -> Dict:
        """Fallback improvements"""
        return {
            'improved_prompt': prompt,
            'reason': 'Gemini API not configured',
            'confidence': 0.0,
            'suggestions': ['Configure Gemini API for AI-powered improvements'],
            'changes_made': [],
            'original_prompt': prompt,
            'original_score': score,
            'suggested_at': datetime.now().isoformat()
        }

    def _fallback_categorization(self, prompt: str) -> Dict:
        """Fallback categorization"""
        return {
            'genre': 'unknown',
            'sub_genre': 'unknown',
            'best_model': 'unknown',
            'quality_level': 'mid',
            'complexity': 'moderate',
            'estimated_duration': 'medium',
            'primary_elements': [],
            'mood': [],
            'confidence': 0.0,
            'categorized_at': datetime.now().isoformat(),
            'note': 'Fallback mode - Configure Gemini API for categorization'
        }


if __name__ == '__main__':
    # Test analyzer
    print("Prompt Analyzer - Test Mode")
    print("="*60)

    analyzer = PromptAnalyzer()

    # Test prompt
    test_prompt = """
    A cinematic shot of a futuristic city at night, neon lights reflecting
    on wet streets, camera slowly panning right, 4K professional quality,
    cyberpunk aesthetic with purple and blue color grading.
    """

    print("\nTesting prompt analysis...")
    analysis = analyzer.analyze_prompt_quality(test_prompt)
    print(f"Overall Score: {analysis.get('overall_score', 'N/A')}/10")
    print(f"Strengths: {analysis.get('strengths', [])}")

    print("\nTesting improvements...")
    improvements = analyzer.suggest_improvements(test_prompt, 6.5)
    print(f"Improved: {improvements.get('improved_prompt', 'N/A')[:100]}...")

    print("\nTesting categorization...")
    category = analyzer.categorize_prompt(test_prompt)
    print(f"Genre: {category.get('genre', 'N/A')}")
    print(f"Best Model: {category.get('best_model', 'N/A')}")

    print("\n" + "="*60)
