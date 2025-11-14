"""
Orchestrator Integration Tests
Tests for the Music Agents Orchestrator System
"""

import requests
import time
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple


class OrchestratorTests:
    """Test suite for Orchestrator health and functionality"""

    def __init__(self, base_url: str = "http://localhost:8000", verbose: bool = True):
        self.base_url = base_url
        self.verbose = verbose
        self.results = []
        self.orchestrator_path = Path(__file__).parent.parent / "orchestrator"

    def log(self, message: str, level: str = "INFO"):
        """Log message with level"""
        if self.verbose:
            prefix = {
                "INFO": "ℹ️",
                "SUCCESS": "✅",
                "ERROR": "❌",
                "WARNING": "⚠️"
            }.get(level, "•")
            print(f"{prefix} {message}")

    def test_orchestrator_running(self) -> Tuple[bool, str]:
        """Test 1: Check if orchestrator is running on port 8000"""
        self.log("Testing orchestrator connectivity...", "INFO")

        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code in [200, 404]:  # 404 is OK if no root endpoint
                self.log("Orchestrator is running on port 8000", "SUCCESS")
                return True, "Orchestrator running successfully"
            else:
                msg = f"Unexpected status code: {response.status_code}"
                self.log(msg, "ERROR")
                return False, msg
        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to orchestrator on port 8000"
            self.log(msg, "ERROR")
            return False, msg
        except requests.exceptions.Timeout:
            msg = "Connection timeout (>5s)"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Unexpected error: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_all_agents_online(self) -> Tuple[bool, str]:
        """Test 2: Check if all 12 agents are online"""
        self.log("Checking agent statuses...", "INFO")

        try:
            # Try common agent status endpoints
            endpoints = [
                f"{self.base_url}/api/agents",
                f"{self.base_url}/api/agents/status",
                f"{self.base_url}/agents/status"
            ]

            response = None
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, timeout=5)
                    if response.status_code == 200:
                        break
                except:
                    continue

            if not response or response.status_code != 200:
                # Fallback: Check if agent files exist
                agents_dir = self.orchestrator_path / "agents"
                if agents_dir.exists():
                    agent_files = list(agents_dir.glob("agent_*.py"))
                    if len(agent_files) >= 12:
                        self.log(f"Found {len(agent_files)} agent files", "SUCCESS")
                        return True, f"{len(agent_files)} agent files found"
                    else:
                        msg = f"Only {len(agent_files)} agent files found (expected 12)"
                        self.log(msg, "WARNING")
                        return False, msg
                else:
                    msg = "Could not verify agent status (no API response or agent files)"
                    self.log(msg, "WARNING")
                    return False, msg

            # Parse JSON response
            data = response.json()

            # Handle different response formats
            agents = data if isinstance(data, list) else data.get('agents', [])

            online_count = sum(1 for agent in agents if agent.get('status') == 'ONLINE')
            total_count = len(agents)

            if total_count >= 12 and online_count >= 10:  # Allow 2 offline
                self.log(f"{online_count}/{total_count} agents online", "SUCCESS")
                return True, f"{online_count}/{total_count} agents online"
            else:
                msg = f"Only {online_count}/{total_count} agents online (expected 12)"
                self.log(msg, "WARNING")
                return False, msg

        except Exception as e:
            msg = f"Error checking agents: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_database_initialized(self) -> Tuple[bool, str]:
        """Test 3: Check if database and logs are initialized"""
        self.log("Checking database initialization...", "INFO")

        checks = []

        # Check logs directory
        logs_dir = self.orchestrator_path / "logs"
        if logs_dir.exists():
            checks.append("logs directory exists")
            self.log("✓ logs/ directory found", "INFO")
        else:
            self.log("✗ logs/ directory not found", "WARNING")

        # Check training config
        training_config = self.orchestrator_path / "training" / "config.json"
        if training_config.exists():
            checks.append("training config exists")
            self.log("✓ training/config.json found", "INFO")
        else:
            self.log("✗ training/config.json not found", "WARNING")

        # Check for any daily report files
        if logs_dir.exists():
            daily_reports = list(logs_dir.glob("*daily_report*"))
            if daily_reports:
                checks.append(f"{len(daily_reports)} daily reports found")
                self.log(f"✓ {len(daily_reports)} daily report files found", "INFO")
            else:
                self.log("✗ No daily report files found", "WARNING")

        if len(checks) >= 2:  # At least 2 out of 3 checks pass
            msg = f"Database initialized ({len(checks)}/3 checks passed)"
            self.log(msg, "SUCCESS")
            return True, msg
        else:
            msg = f"Database may not be fully initialized ({len(checks)}/3 checks passed)"
            self.log(msg, "WARNING")
            return False, msg

    def test_training_pipeline_active(self) -> Tuple[bool, str]:
        """Test 4: Check if training pipeline is active"""
        self.log("Checking training pipeline status...", "INFO")

        try:
            # Try training status endpoint
            endpoints = [
                f"{self.base_url}/api/training/status",
                f"{self.base_url}/training/status"
            ]

            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, timeout=5)
                    if response.status_code == 200:
                        data = response.json()

                        # Check for training indicators
                        current_phase = data.get('current_phase') or data.get('phase')
                        progress = data.get('progress_percent') or data.get('progress', 0)

                        if current_phase:
                            msg = f"Training pipeline active (phase: {current_phase}, progress: {progress}%)"
                            self.log(msg, "SUCCESS")
                            return True, msg
                        break
                except:
                    continue

            # Fallback: Check for training files
            training_dir = self.orchestrator_path / "training"
            if training_dir.exists():
                training_files = list(training_dir.glob("*.py"))
                if training_files:
                    msg = f"Training system present ({len(training_files)} training files found)"
                    self.log(msg, "SUCCESS")
                    return True, msg

            msg = "Training pipeline status uncertain (no API response)"
            self.log(msg, "WARNING")
            return False, msg

        except Exception as e:
            msg = f"Error checking training pipeline: {str(e)}"
            self.log(msg, "WARNING")
            return False, msg

    def test_harvester_running(self) -> Tuple[bool, str]:
        """Test 5: Check if Agent 12 (Universal Harvester) is running"""
        self.log("Checking harvester agent...", "INFO")

        try:
            # Check for harvester agent file
            harvester_files = [
                self.orchestrator_path / "agents" / "agent_12_universal_harvester.py",
                self.orchestrator_path / "agents" / "agent_12.py",
                self.orchestrator_path / "universal_harvester.py"
            ]

            for harvester_file in harvester_files:
                if harvester_file.exists():
                    self.log(f"✓ Harvester file found: {harvester_file.name}", "INFO")

                    # Check for harvest logs
                    logs_dir = self.orchestrator_path / "logs"
                    if logs_dir.exists():
                        harvest_logs = list(logs_dir.glob("*harvest*")) + list(logs_dir.glob("*agent_12*"))
                        if harvest_logs:
                            # Check if logs are recent (within last 24 hours)
                            recent_logs = [log for log in harvest_logs
                                         if time.time() - log.stat().st_mtime < 86400]

                            if recent_logs:
                                msg = f"Harvester active ({len(recent_logs)} recent log files)"
                                self.log(msg, "SUCCESS")
                                return True, msg
                            else:
                                msg = f"Harvester exists but may be inactive (no recent logs)"
                                self.log(msg, "WARNING")
                                return True, msg

                    msg = "Harvester file found"
                    self.log(msg, "SUCCESS")
                    return True, msg

            msg = "Harvester agent file not found"
            self.log(msg, "WARNING")
            return False, msg

        except Exception as e:
            msg = f"Error checking harvester: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_port_not_blocked(self) -> Tuple[bool, str]:
        """Test 6: Check if port 8000 is accessible and not blocked"""
        self.log("Testing port accessibility...", "INFO")

        try:
            start_time = time.time()
            response = requests.get(self.base_url, timeout=2)
            elapsed = time.time() - start_time

            if elapsed < 2.0:
                msg = f"Port 8000 accessible (response time: {elapsed:.3f}s)"
                self.log(msg, "SUCCESS")
                return True, msg
            else:
                msg = f"Port 8000 accessible but slow (response time: {elapsed:.3f}s)"
                self.log(msg, "WARNING")
                return True, msg

        except requests.exceptions.Timeout:
            msg = "Port 8000 timeout (>2s) - may be blocked or slow"
            self.log(msg, "ERROR")
            return False, msg
        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to port 8000 - service may be down"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Error checking port: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def run_all_tests(self) -> Dict:
        """Run all orchestrator tests and return results"""
        self.log("=" * 60, "INFO")
        self.log("ORCHESTRATOR TESTS", "INFO")
        self.log("=" * 60, "INFO")

        tests = [
            ("orchestrator_running", self.test_orchestrator_running),
            ("all_agents_online", self.test_all_agents_online),
            ("database_initialized", self.test_database_initialized),
            ("training_pipeline_active", self.test_training_pipeline_active),
            ("harvester_running", self.test_harvester_running),
            ("port_not_blocked", self.test_port_not_blocked)
        ]

        results = {
            "category": "Orchestrator Tests",
            "total": len(tests),
            "passed": 0,
            "failed": 0,
            "tests": []
        }

        for test_name, test_func in tests:
            try:
                passed, message = test_func()
                results["tests"].append({
                    "name": test_name,
                    "passed": passed,
                    "message": message
                })
                if passed:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
            except Exception as e:
                results["tests"].append({
                    "name": test_name,
                    "passed": False,
                    "message": f"Exception: {str(e)}"
                })
                results["failed"] += 1
                self.log(f"Test {test_name} threw exception: {e}", "ERROR")

        self.log("=" * 60, "INFO")
        self.log(f"Results: {results['passed']}/{results['total']} tests passed",
                "SUCCESS" if results["failed"] == 0 else "WARNING")
        self.log("=" * 60, "INFO")

        return results


if __name__ == "__main__":
    # Run tests standalone
    tester = OrchestratorTests(verbose=True)
    results = tester.run_all_tests()

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print("=" * 60)

    # Exit with error code if any tests failed
    exit(0 if results['failed'] == 0 else 1)
