"""
Agent Trainer - Individual Agent Training Helper

Provides helper methods for training individual agents with
timeout handling, error recovery, and performance measurement.

Author: Music Video Production System
Version: 1.0.0
"""

import logging
import time
import signal
from typing import Any, Dict, Tuple, Optional
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)


class TimeoutException(Exception):
    """Exception raised when training times out."""
    pass


class AgentTrainer:
    """
    Helper class for training individual agents.

    Provides:
    - Timeout handling
    - Error recovery
    - Performance measurement
    - Logging
    """

    def __init__(self):
        """Initialize Agent Trainer."""
        self.logger = logging.getLogger("AgentTrainer")
        self.logger.info("Agent Trainer initialized")

    @staticmethod
    def train_agent_individually(
        agent: Any,
        data: Any,
        timeout: int = 300
    ) -> Tuple[bool, Optional[Any], int, Optional[str]]:
        """
        Train a single agent with timeout and error handling.

        Args:
            agent: Agent instance to train
            data: Training data
            timeout: Maximum processing time in seconds

        Returns:
            Tuple of (success, results, time_ms, error):
            - success: True if training completed successfully
            - results: Training results (or None if failed)
            - time_ms: Processing time in milliseconds
            - error: Error message (or None if successful)
        """
        logger = logging.getLogger("AgentTrainer")
        start_time = time.time()

        try:
            logger.info(f"Training {agent.__class__.__name__}...")

            # Check if agent has train method
            if not hasattr(agent, 'train'):
                error_msg = f"Agent {agent.__class__.__name__} does not have 'train' method"
                logger.error(error_msg)
                return (False, None, 0, error_msg)

            # Execute training with timeout
            try:
                with timeout_context(timeout):
                    results = agent.train(data)

                # Calculate processing time
                time_ms = int((time.time() - start_time) * 1000)

                logger.info(f"{agent.__class__.__name__} training completed in {time_ms}ms")

                return (True, results, time_ms, None)

            except TimeoutException:
                error_msg = f"Training timed out after {timeout}s"
                logger.error(error_msg)
                time_ms = int((time.time() - start_time) * 1000)
                return (False, None, time_ms, error_msg)

        except AttributeError as e:
            error_msg = f"Agent training method error: {str(e)}"
            logger.error(error_msg)
            time_ms = int((time.time() - start_time) * 1000)
            return (False, None, time_ms, error_msg)

        except Exception as e:
            error_msg = f"Training failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            time_ms = int((time.time() - start_time) * 1000)
            return (False, None, time_ms, error_msg)

    @staticmethod
    def validate_training_data(data: Any, min_count: int = 1) -> Tuple[bool, str]:
        """
        Validate training data before training.

        Args:
            data: Training data to validate
            min_count: Minimum number of records required

        Returns:
            Tuple of (valid, message)
        """
        logger = logging.getLogger("AgentTrainer")

        # Check if data exists
        if data is None:
            return (False, "Training data is None")

        # Check if data is empty
        if isinstance(data, (list, tuple, dict)):
            if len(data) == 0:
                return (False, "Training data is empty")

            if len(data) < min_count:
                return (False, f"Training data has only {len(data)} items (minimum: {min_count})")

        logger.debug(f"Training data validated: {len(data) if isinstance(data, (list, tuple, dict)) else 'N/A'} items")

        return (True, "Data valid")

    @staticmethod
    def measure_performance(
        agent_name: str,
        before_metrics: Dict[str, Any],
        after_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Measure performance improvement after training.

        Args:
            agent_name: Name of the agent
            before_metrics: Metrics before training
            after_metrics: Metrics after training

        Returns:
            Dict with performance delta
        """
        logger = logging.getLogger("AgentTrainer")

        try:
            performance = {
                'agent_name': agent_name,
                'timestamp': time.time(),
                'improvements': {}
            }

            # Calculate deltas for common metrics
            common_metrics = ['accuracy', 'quality', 'speed', 'confidence']

            for metric in common_metrics:
                if metric in before_metrics and metric in after_metrics:
                    before_val = before_metrics[metric]
                    after_val = after_metrics[metric]

                    if isinstance(before_val, (int, float)) and isinstance(after_val, (int, float)):
                        delta = after_val - before_val
                        percent_change = (delta / before_val * 100) if before_val != 0 else 0

                        performance['improvements'][metric] = {
                            'before': before_val,
                            'after': after_val,
                            'delta': delta,
                            'percent_change': percent_change
                        }

            logger.info(f"Performance measured for {agent_name}")

            return performance

        except Exception as e:
            logger.error(f"Error measuring performance: {str(e)}")
            return {'error': str(e)}

    @staticmethod
    def create_training_summary(
        agent_name: str,
        success: bool,
        results: Optional[Any],
        time_ms: int,
        data_count: int
    ) -> Dict[str, Any]:
        """
        Create a summary of training session.

        Args:
            agent_name: Name of the agent
            success: Whether training succeeded
            results: Training results
            time_ms: Processing time
            data_count: Number of training data items

        Returns:
            Training summary dict
        """
        summary = {
            'agent_name': agent_name,
            'timestamp': time.time(),
            'success': success,
            'time_ms': time_ms,
            'time_seconds': round(time_ms / 1000, 2),
            'data_count': data_count,
            'status': 'completed' if success else 'failed'
        }

        if results:
            summary['results_available'] = True
            # Add result summary (avoid storing large objects)
            if isinstance(results, dict):
                summary['result_keys'] = list(results.keys())
            elif isinstance(results, list):
                summary['result_count'] = len(results)

        return summary


# ============================================================
# TIMEOUT CONTEXT MANAGER
# ============================================================

@contextmanager
def timeout_context(seconds: int):
    """
    Context manager for timeout handling.

    Args:
        seconds: Timeout in seconds

    Raises:
        TimeoutException: If operation times out
    """
    def timeout_handler(signum, frame):
        raise TimeoutException(f"Operation timed out after {seconds} seconds")

    # Note: signal.alarm only works on Unix systems
    # For Windows, we would need a different approach (threading.Timer)
    import platform

    if platform.system() == 'Windows':
        # Windows fallback - no actual timeout (would need threading.Timer)
        yield
    else:
        # Unix systems - use signal
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(seconds)

        try:
            yield
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)


# ============================================================
# MOCK AGENT FOR TESTING
# ============================================================

class MockAgent:
    """Mock agent for testing purposes."""

    def __init__(self, name: str, training_time_ms: int = 1000):
        """
        Initialize mock agent.

        Args:
            name: Agent name
            training_time_ms: Simulated training time
        """
        self.name = name
        self.training_time_ms = training_time_ms
        self.trained = False

    def train(self, data: Any) -> Dict[str, Any]:
        """
        Simulate training.

        Args:
            data: Training data

        Returns:
            Mock training results
        """
        # Simulate processing time
        time.sleep(self.training_time_ms / 1000)

        self.trained = True

        return {
            'status': 'success',
            'agent_name': self.name,
            'data_count': len(data) if isinstance(data, (list, tuple)) else 1,
            'quality_improvement': 0.5,  # Mock improvement
            'model_updated': True
        }


# ============================================================
# STANDALONE EXECUTION (TESTING)
# ============================================================

if __name__ == '__main__':
    print("Agent Trainer - Standalone Test\n")

    # Create trainer
    trainer = AgentTrainer()

    # Create mock agent
    mock_agent = MockAgent("TestAgent", training_time_ms=500)

    # Create mock training data
    training_data = [
        {'id': i, 'quality_score': 7.0 + i*0.1}
        for i in range(10)
    ]

    print(f"Training mock agent with {len(training_data)} data items...")

    # Train agent
    success, results, time_ms, error = trainer.train_agent_individually(
        agent=mock_agent,
        data=training_data,
        timeout=10
    )

    # Print results
    print(f"\nTraining Results:")
    print(f"  Success: {success}")
    print(f"  Time: {time_ms}ms ({time_ms/1000:.2f}s)")
    print(f"  Error: {error}")
    print(f"  Results: {results}")

    # Test validation
    print("\n" + "="*60)
    print("Testing data validation...")

    valid, message = trainer.validate_training_data(training_data, min_count=5)
    print(f"  Valid: {valid}")
    print(f"  Message: {message}")

    # Test with empty data
    valid, message = trainer.validate_training_data([], min_count=5)
    print(f"\n  Empty data - Valid: {valid}")
    print(f"  Message: {message}")

    # Test summary creation
    print("\n" + "="*60)
    print("Creating training summary...")

    summary = trainer.create_training_summary(
        agent_name="TestAgent",
        success=success,
        results=results,
        time_ms=time_ms,
        data_count=len(training_data)
    )

    print(f"  Summary: {json.dumps(summary, indent=2)}")

    print("\n✅ Agent Trainer test completed!")
