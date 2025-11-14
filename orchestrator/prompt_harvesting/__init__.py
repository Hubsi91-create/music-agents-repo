#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prompt Harvesting Module for Music Video AI Orchestrator

This module harvests, analyzes, and manages prompts from various sources
(Reddit, YouTube, Web) for training video generation AI agents.

Components:
- PromptHarvester: Collects prompts from multiple sources
- PromptAnalyzer: Uses Gemini AI for intelligent prompt analysis
- QualityScorer: Local quality scoring without API costs
- PromptDatabase: SQLite-based persistent storage

Usage:
    from orchestrator.prompt_harvesting import PromptHarvester, PromptAnalyzer

    harvester = PromptHarvester()
    results = harvester.harvest_all()

    analyzer = PromptAnalyzer()
    analysis = analyzer.analyze_prompt_quality(prompt_text)
"""

__version__ = "1.0.0"
__author__ = "Music Agents Repo"

from .harvester import PromptHarvester
from .analyzer import PromptAnalyzer
from .quality_scorer import QualityScorer
from .prompt_database import PromptDatabase

__all__ = [
    'PromptHarvester',
    'PromptAnalyzer',
    'QualityScorer',
    'PromptDatabase'
]
