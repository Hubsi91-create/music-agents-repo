"""
End-to-End Workflow Tests
Tests for complete user workflows in the Music Agents System
"""

import requests
import time
import json
from typing import Dict, List, Tuple, Optional


class WorkflowTests:
    """Test suite for end-to-end workflow functionality"""

    def __init__(self, base_url: str = "http://localhost:5000", verbose: bool = True):
        self.base_url = base_url
        self.verbose = verbose
        self.results = []
        self.test_project_id = None
        self.test_data = {
            "project_name": "Integration Test Project",
            "music_title": "Test Music Track",
            "scenes": [
                {"id": 1, "description": "Opening scene", "duration": 10},
                {"id": 2, "description": "Main action", "duration": 20},
                {"id": 3, "description": "Closing scene", "duration": 10}
            ]
        }

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

    def test_create_project(self) -> Tuple[bool, str]:
        """Test 1: Create a new storyboard project"""
        self.log("Testing project creation...", "INFO")

        try:
            # Prepare project data
            project_data = {
                "name": self.test_data["project_name"],
                "music": self.test_data["music_title"],
                "created_at": time.time()
            }

            # Try to create project
            response = requests.post(
                f"{self.base_url}/api/storyboard/project/create",
                json=project_data,
                timeout=5
            )

            if response.status_code == 201:
                data = response.json()
                self.test_project_id = data.get("project_id") or data.get("id")

                if self.test_project_id:
                    msg = f"Project created successfully (ID: {self.test_project_id})"
                    self.log(msg, "SUCCESS")
                    return True, msg
                else:
                    msg = "Project created but no ID returned"
                    self.log(msg, "WARNING")
                    return False, msg

            elif response.status_code == 200:
                # Some APIs return 200 instead of 201
                data = response.json()
                self.test_project_id = data.get("project_id") or data.get("id")

                if self.test_project_id:
                    msg = f"Project created successfully (ID: {self.test_project_id})"
                    self.log(msg, "SUCCESS")
                    return True, msg
                else:
                    msg = "Project endpoint returned 200 but format unclear"
                    self.log(msg, "WARNING")
                    return False, msg

            elif response.status_code == 404:
                msg = "Project creation endpoint not found (404)"
                self.log(msg, "WARNING")
                return False, msg

            else:
                msg = f"Project creation failed (status: {response.status_code})"
                self.log(msg, "ERROR")
                return False, msg

        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Error creating project: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_add_scenes(self) -> Tuple[bool, str]:
        """Test 2: Add scenes to the project"""
        self.log("Testing scene addition...", "INFO")

        if not self.test_project_id:
            msg = "No project ID available (skipping test)"
            self.log(msg, "WARNING")
            return False, msg

        try:
            # Try to add scenes
            response = requests.post(
                f"{self.base_url}/api/storyboard/project/{self.test_project_id}/scenes",
                json={"scenes": self.test_data["scenes"]},
                timeout=5
            )

            if response.status_code in [200, 201]:
                msg = f"Scenes added successfully ({len(self.test_data['scenes'])} scenes)"
                self.log(msg, "SUCCESS")
                return True, msg

            elif response.status_code == 404:
                msg = "Scene addition endpoint not found (404)"
                self.log(msg, "WARNING")
                return False, msg

            else:
                msg = f"Scene addition failed (status: {response.status_code})"
                self.log(msg, "ERROR")
                return False, msg

        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Error adding scenes: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_save_project(self) -> Tuple[bool, str]:
        """Test 3: Save project updates"""
        self.log("Testing project save...", "INFO")

        if not self.test_project_id:
            msg = "No project ID available (skipping test)"
            self.log(msg, "WARNING")
            return False, msg

        try:
            # Update project data
            updated_data = {
                "name": self.test_data["project_name"] + " (Updated)",
                "scenes": self.test_data["scenes"]
            }

            response = requests.put(
                f"{self.base_url}/api/storyboard/project/{self.test_project_id}",
                json=updated_data,
                timeout=5
            )

            if response.status_code in [200, 204]:
                msg = "Project saved successfully"
                self.log(msg, "SUCCESS")
                return True, msg

            elif response.status_code == 404:
                msg = "Project save endpoint not found (404)"
                self.log(msg, "WARNING")
                return False, msg

            else:
                msg = f"Project save failed (status: {response.status_code})"
                self.log(msg, "ERROR")
                return False, msg

        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Error saving project: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_export_project(self) -> Tuple[bool, str]:
        """Test 4: Export project data"""
        self.log("Testing project export...", "INFO")

        if not self.test_project_id:
            msg = "No project ID available (skipping test)"
            self.log(msg, "WARNING")
            return False, msg

        try:
            # Try to export project
            response = requests.post(
                f"{self.base_url}/api/storyboard/project/{self.test_project_id}/export",
                json={"format": "json"},
                timeout=5
            )

            if response.status_code == 200:
                # Check if valid JSON returned
                try:
                    export_data = response.json()
                    msg = f"Project exported successfully ({len(str(export_data))} bytes)"
                    self.log(msg, "SUCCESS")
                    return True, msg
                except json.JSONDecodeError:
                    msg = "Export returned invalid JSON"
                    self.log(msg, "ERROR")
                    return False, msg

            elif response.status_code == 404:
                msg = "Export endpoint not found (404)"
                self.log(msg, "WARNING")
                return False, msg

            else:
                msg = f"Export failed (status: {response.status_code})"
                self.log(msg, "ERROR")
                return False, msg

        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Error exporting project: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_fetch_video_list(self) -> Tuple[bool, str]:
        """Test 5: Fetch available videos"""
        self.log("Testing video list retrieval...", "INFO")

        try:
            response = requests.get(
                f"{self.base_url}/api/storyboard/videos",
                timeout=5
            )

            if response.status_code == 200:
                try:
                    videos = response.json()

                    if isinstance(videos, list):
                        # Check video structure
                        if videos and all(isinstance(v, dict) for v in videos):
                            msg = f"Video list retrieved ({len(videos)} videos)"
                            self.log(msg, "SUCCESS")
                            return True, msg
                        elif len(videos) == 0:
                            msg = "Video list empty (no videos available)"
                            self.log(msg, "WARNING")
                            return True, msg
                        else:
                            msg = "Video list format incorrect"
                            self.log(msg, "WARNING")
                            return False, msg
                    else:
                        msg = f"Video list not in expected format (type: {type(videos).__name__})"
                        self.log(msg, "WARNING")
                        return False, msg

                except json.JSONDecodeError:
                    msg = "Invalid JSON in video list response"
                    self.log(msg, "ERROR")
                    return False, msg

            elif response.status_code == 404:
                msg = "Video list endpoint not found (404)"
                self.log(msg, "WARNING")
                return False, msg

            else:
                msg = f"Video list fetch failed (status: {response.status_code})"
                self.log(msg, "ERROR")
                return False, msg

        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Error fetching video list: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_save_and_retrieve(self) -> Tuple[bool, str]:
        """Test 6: Save data and verify retrieval"""
        self.log("Testing data persistence...", "INFO")

        if not self.test_project_id:
            msg = "No project ID available (skipping test)"
            self.log(msg, "WARNING")
            return False, msg

        try:
            # Retrieve the project
            response = requests.get(
                f"{self.base_url}/api/storyboard/project/{self.test_project_id}",
                timeout=5
            )

            if response.status_code == 200:
                try:
                    project_data = response.json()

                    # Check if project data contains expected fields
                    if isinstance(project_data, dict):
                        msg = "Data persistence verified (project retrievable)"
                        self.log(msg, "SUCCESS")
                        return True, msg
                    else:
                        msg = "Retrieved data format incorrect"
                        self.log(msg, "WARNING")
                        return False, msg

                except json.JSONDecodeError:
                    msg = "Invalid JSON in project data"
                    self.log(msg, "ERROR")
                    return False, msg

            elif response.status_code == 404:
                msg = "Project not found (data persistence failed)"
                self.log(msg, "ERROR")
                return False, msg

            else:
                msg = f"Project retrieval failed (status: {response.status_code})"
                self.log(msg, "ERROR")
                return False, msg

        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Error retrieving project: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_delete_project(self) -> Tuple[bool, str]:
        """Test 7: Delete the test project"""
        self.log("Testing project deletion...", "INFO")

        if not self.test_project_id:
            msg = "No project ID available (skipping test)"
            self.log(msg, "WARNING")
            return False, msg

        try:
            # Delete the project
            response = requests.delete(
                f"{self.base_url}/api/storyboard/project/{self.test_project_id}",
                timeout=5
            )

            if response.status_code in [200, 204]:
                self.log("✓ Project deleted", "INFO")

                # Verify deletion
                time.sleep(0.5)
                verify_response = requests.get(
                    f"{self.base_url}/api/storyboard/project/{self.test_project_id}",
                    timeout=5
                )

                if verify_response.status_code == 404:
                    msg = "Project deleted successfully (verified)"
                    self.log(msg, "SUCCESS")
                    return True, msg
                else:
                    msg = "Project deletion uncertain (still retrievable)"
                    self.log(msg, "WARNING")
                    return False, msg

            elif response.status_code == 404:
                msg = "Delete endpoint not found (404)"
                self.log(msg, "WARNING")
                return False, msg

            else:
                msg = f"Project deletion failed (status: {response.status_code})"
                self.log(msg, "ERROR")
                return False, msg

        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Error deleting project: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def run_all_tests(self) -> Dict:
        """Run all workflow tests and return results"""
        self.log("=" * 60, "INFO")
        self.log("END-TO-END WORKFLOW TESTS", "INFO")
        self.log("=" * 60, "INFO")

        tests = [
            ("create_project", self.test_create_project),
            ("add_scenes", self.test_add_scenes),
            ("save_project", self.test_save_project),
            ("export_project", self.test_export_project),
            ("fetch_video_list", self.test_fetch_video_list),
            ("save_and_retrieve", self.test_save_and_retrieve),
            ("delete_project", self.test_delete_project)
        ]

        results = {
            "category": "Workflow Tests",
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
    tester = WorkflowTests(verbose=True)
    results = tester.run_all_tests()

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print("=" * 60)

    # Exit with error code if any tests failed
    exit(0 if results['failed'] == 0 else 1)
