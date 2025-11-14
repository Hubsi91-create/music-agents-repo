"""
Training Module - Holistic Training Pipeline

Provides comprehensive training infrastructure for all agents
in the Music Video Production System.

Components:
- HolisticTrainer: Core training pipeline coordinator
- TrainingMonitor: Metrics tracking and reporting
- AgentTrainer: Individual agent training helper

Author: Music Video Production System
Version: 1.0.0
"""

from .holistic_trainer import HolisticTrainer
from .training_monitor import TrainingMonitor
from .agent_trainer import AgentTrainer

__version__ = "1.0.0"
__all__ = ['HolisticTrainer', 'TrainingMonitor', 'AgentTrainer']
