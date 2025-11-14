"""
Backend API Integration Tests
Tests for the Music Agents Dashboard Backend API
"""

import requests
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any


class BackendTests:
    """Test suite for Backend API functionality"""

    def __init__(self, base_url: str = "http://localhost:5000", verbose: bool = True):
        self.base_url = base_url
        self.verbose = verbose
        self.results = []
        self.backend_path = Path(__file__).parent.parent / "dashboard" / "backend"

        # Define all 26 API endpoints
        self.endpoints = [
            ("GET", "/api/dashboard/overview", "Dashboard Overview"),
            ("GET", "/api/dashboard/quick-stats", "Quick Stats"),
            ("GET", "/api/agents/status", "Agents Status"),
            ("GET", "/api/agents/health", "Agents Health"),
            ("GET", "/api/agents/performance", "Agents Performance"),
            ("GET", "/api/training/status", "Training Status"),
            ("GET", "/api/training/history", "Training History"),
            ("GET", "/api/metrics/quality", "Quality Metrics"),
            ("GET", "/api/metrics/comparison", "Metrics Comparison"),
            ("GET", "/api/metrics/trends", "Metrics Trends"),
            ("GET", "/api/system/health", "System Health"),
            ("GET", "/api/system/logs/recent", "Recent Logs"),
            ("GET", "/api/system/errors", "System Errors"),
            ("GET", "/api/system/alerts", "System Alerts"),
            ("GET", "/api/storyboard/projects", "Storyboard Projects"),
            ("GET", "/api/storyboard/videos", "Available Videos"),
            ("GET", "/api/export/formats", "Export Formats"),
            ("GET", "/api/export/history", "Export History"),
            ("GET", "/api/prompts/library", "Prompt Library"),
            ("GET", "/api/prompts/categories", "Prompt Categories"),
            ("GET", "/api/harvest/recent", "Recent Harvests"),
            ("GET", "/api/harvest/stats", "Harvest Statistics"),
            ("GET", "/api/config/settings", "Configuration Settings"),
            ("GET", "/api/config/agents", "Agent Configuration"),
            ("GET", "/api/analytics/summary", "Analytics Summary"),
            ("GET", "/api/analytics/performance", "Performance Analytics"),
        ]

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

    def test_backend_running(self) -> Tuple[bool, str]:
        """Test 1: Check if backend is running on port 5000"""
        self.log("Testing backend connectivity...", "INFO")

        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code in [200, 404]:  # 404 is OK if no root endpoint
                self.log("Backend is running on port 5000", "SUCCESS")
                return True, "Backend running successfully"
            else:
                msg = f"Unexpected status code: {response.status_code}"
                self.log(msg, "ERROR")
                return False, msg
        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend on port 5000"
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

    def test_all_26_endpoints(self) -> Tuple[bool, str]:
        """Test 2: Test all 26 API endpoints"""
        self.log("Testing all 26 API endpoints...", "INFO")

        successful = 0
        failed = 0
        not_found = 0
        endpoint_results = []

        for method, endpoint, description in self.endpoints:
            url = f"{self.base_url}{endpoint}"

            try:
                if method == "GET":
                    response = requests.get(url, timeout=5)
                elif method == "POST":
                    response = requests.post(url, json={}, timeout=5)
                else:
                    continue

                # Check status code
                if response.status_code == 200:
                    # Validate JSON response
                    try:
                        data = response.json()
                        self.log(f"  ✓ {endpoint} - OK (200)", "INFO")
                        successful += 1
                        endpoint_results.append({
                            "endpoint": endpoint,
                            "status": "success",
                            "code": 200
                        })
                    except json.JSONDecodeError:
                        self.log(f"  ⚠ {endpoint} - Invalid JSON", "WARNING")
                        failed += 1
                        endpoint_results.append({
                            "endpoint": endpoint,
                            "status": "invalid_json",
                            "code": 200
                        })

                elif response.status_code == 404:
                    self.log(f"  ⚠ {endpoint} - Not Found (404)", "WARNING")
                    not_found += 1
                    endpoint_results.append({
                        "endpoint": endpoint,
                        "status": "not_found",
                        "code": 404
                    })

                elif response.status_code == 500:
                    self.log(f"  ✗ {endpoint} - Server Error (500)", "ERROR")
                    failed += 1
                    endpoint_results.append({
                        "endpoint": endpoint,
                        "status": "server_error",
                        "code": 500
                    })

                else:
                    self.log(f"  ? {endpoint} - Status {response.status_code}", "INFO")
                    endpoint_results.append({
                        "endpoint": endpoint,
                        "status": "other",
                        "code": response.status_code
                    })

            except requests.exceptions.Timeout:
                self.log(f"  ✗ {endpoint} - Timeout", "ERROR")
                failed += 1
                endpoint_results.append({
                    "endpoint": endpoint,
                    "status": "timeout",
                    "code": None
                })
            except requests.exceptions.ConnectionError:
                self.log(f"  ✗ {endpoint} - Connection Error", "ERROR")
                failed += 1
                endpoint_results.append({
                    "endpoint": endpoint,
                    "status": "connection_error",
                    "code": None
                })
            except Exception as e:
                self.log(f"  ✗ {endpoint} - Error: {str(e)}", "ERROR")
                failed += 1
                endpoint_results.append({
                    "endpoint": endpoint,
                    "status": "error",
                    "code": None,
                    "error": str(e)
                })

        total = len(self.endpoints)
        success_rate = (successful / total) * 100

        msg = f"{successful}/{total} endpoints successful ({success_rate:.1f}%), {not_found} not found, {failed} failed"

        if successful >= total * 0.7:  # 70% success rate is acceptable
            self.log(msg, "SUCCESS")
            return True, msg
        else:
            self.log(msg, "WARNING")
            return False, msg

    def test_database_connection(self) -> Tuple[bool, str]:
        """Test 3: Check database connection and availability"""
        self.log("Testing database connection...", "INFO")

        try:
            # Check if database file exists
            db_path = self.backend_path / "dashboard.db"

            if db_path.exists():
                db_size = db_path.stat().st_size
                self.log(f"✓ Database file found ({db_size} bytes)", "INFO")

                # Try to fetch data from an endpoint that requires database
                response = requests.get(f"{self.base_url}/api/dashboard/overview", timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    msg = "Database connection OK (data retrievable)"
                    self.log(msg, "SUCCESS")
                    return True, msg
                else:
                    msg = "Database file exists but cannot retrieve data"
                    self.log(msg, "WARNING")
                    return False, msg
            else:
                msg = "Database file not found (may use in-memory or not initialized)"
                self.log(msg, "WARNING")
                return False, msg

        except Exception as e:
            msg = f"Error checking database: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_cors_enabled(self) -> Tuple[bool, str]:
        """Test 4: Check if CORS is properly configured"""
        self.log("Testing CORS configuration...", "INFO")

        try:
            # Make a request and check for CORS headers
            response = requests.get(f"{self.base_url}/api/dashboard/overview", timeout=5)

            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
            }

            cors_enabled = any(value for value in cors_headers.values())

            if cors_enabled:
                origin = cors_headers.get("Access-Control-Allow-Origin", "not set")
                msg = f"CORS enabled (origin: {origin})"
                self.log(msg, "SUCCESS")
                return True, msg
            else:
                msg = "CORS headers not found (may need configuration)"
                self.log(msg, "WARNING")
                return False, msg

        except Exception as e:
            msg = f"Error checking CORS: {str(e)}"
            self.log(msg, "WARNING")
            return False, msg

    def test_response_times(self) -> Tuple[bool, str]:
        """Test 5: Measure API response times"""
        self.log("Testing API response times...", "INFO")

        test_endpoints = [
            "/api/dashboard/overview",
            "/api/agents/status",
            "/api/training/status"
        ]

        response_times = []

        for endpoint in test_endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                elapsed = (time.time() - start_time) * 1000  # Convert to ms

                response_times.append({
                    "endpoint": endpoint,
                    "time": elapsed,
                    "status": response.status_code
                })

                if elapsed < 500:
                    self.log(f"  ✓ {endpoint}: {elapsed:.0f}ms", "INFO")
                elif elapsed < 2000:
                    self.log(f"  ⚠ {endpoint}: {elapsed:.0f}ms (slow)", "WARNING")
                else:
                    self.log(f"  ✗ {endpoint}: {elapsed:.0f}ms (too slow)", "ERROR")

            except Exception as e:
                self.log(f"  ✗ {endpoint}: Error - {str(e)}", "ERROR")

        if response_times:
            avg_time = sum(rt["time"] for rt in response_times) / len(response_times)
            max_time = max(rt["time"] for rt in response_times)

            if max_time < 2000:  # All under 2 seconds
                msg = f"Response times OK (avg: {avg_time:.0f}ms, max: {max_time:.0f}ms)"
                self.log(msg, "SUCCESS")
                return True, msg
            elif max_time < 5000:  # Under 5 seconds
                msg = f"Response times acceptable (avg: {avg_time:.0f}ms, max: {max_time:.0f}ms)"
                self.log(msg, "WARNING")
                return True, msg
            else:
                msg = f"Response times too slow (avg: {avg_time:.0f}ms, max: {max_time:.0f}ms)"
                self.log(msg, "ERROR")
                return False, msg
        else:
            msg = "Could not measure response times"
            self.log(msg, "ERROR")
            return False, msg

    def test_data_consistency(self) -> Tuple[bool, str]:
        """Test 6: Check data consistency across multiple requests"""
        self.log("Testing data consistency...", "INFO")

        try:
            endpoint = "/api/agents/status"

            # Fetch data twice
            response1 = requests.get(f"{self.base_url}{endpoint}", timeout=5)
            time.sleep(0.5)
            response2 = requests.get(f"{self.base_url}{endpoint}", timeout=5)

            if response1.status_code == 200 and response2.status_code == 200:
                data1 = response1.json()
                data2 = response2.json()

                # Basic consistency check (structure should be the same)
                if type(data1) == type(data2):
                    if isinstance(data1, list):
                        consistent = len(data1) == len(data2)
                    elif isinstance(data1, dict):
                        consistent = set(data1.keys()) == set(data2.keys())
                    else:
                        consistent = True

                    if consistent:
                        msg = "Data consistency OK"
                        self.log(msg, "SUCCESS")
                        return True, msg
                    else:
                        msg = "Data inconsistency detected"
                        self.log(msg, "WARNING")
                        return False, msg
                else:
                    msg = "Data type inconsistency detected"
                    self.log(msg, "ERROR")
                    return False, msg
            else:
                msg = "Cannot verify consistency (API errors)"
                self.log(msg, "WARNING")
                return False, msg

        except Exception as e:
            msg = f"Error checking data consistency: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_error_handling(self) -> Tuple[bool, str]:
        """Test 7: Check API error handling"""
        self.log("Testing error handling...", "INFO")

        tests_passed = 0

        # Test 1: Invalid endpoint
        try:
            response = requests.get(f"{self.base_url}/api/invalid/endpoint/xyz", timeout=5)
            if response.status_code == 404:
                self.log("  ✓ Invalid endpoint returns 404", "INFO")
                tests_passed += 1
            else:
                self.log(f"  ✗ Invalid endpoint returned {response.status_code}", "WARNING")
        except Exception as e:
            self.log(f"  ✗ Error testing invalid endpoint: {str(e)}", "ERROR")

        # Test 2: Invalid agent ID
        try:
            response = requests.get(f"{self.base_url}/api/agents/invalid-id-999", timeout=5)
            if response.status_code in [404, 400]:
                self.log("  ✓ Invalid agent ID returns error code", "INFO")
                tests_passed += 1
            else:
                self.log(f"  ? Invalid agent ID returned {response.status_code}", "INFO")
                tests_passed += 0.5
        except Exception as e:
            self.log(f"  ✗ Error testing invalid agent ID: {str(e)}", "ERROR")

        if tests_passed >= 1.5:
            msg = f"Error handling OK ({tests_passed}/2 tests passed)"
            self.log(msg, "SUCCESS")
            return True, msg
        else:
            msg = f"Error handling needs improvement ({tests_passed}/2 tests passed)"
            self.log(msg, "WARNING")
            return False, msg

    def run_all_tests(self) -> Dict:
        """Run all backend tests and return results"""
        self.log("=" * 60, "INFO")
        self.log("BACKEND API TESTS", "INFO")
        self.log("=" * 60, "INFO")

        tests = [
            ("backend_running", self.test_backend_running),
            ("all_26_endpoints", self.test_all_26_endpoints),
            ("database_connection", self.test_database_connection),
            ("cors_enabled", self.test_cors_enabled),
            ("response_times", self.test_response_times),
            ("data_consistency", self.test_data_consistency),
            ("error_handling", self.test_error_handling)
        ]

        results = {
            "category": "Backend API Tests",
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
    tester = BackendTests(verbose=True)
    results = tester.run_all_tests()

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print("=" * 60)

    # Exit with error code if any tests failed
    exit(0 if results['failed'] == 0 else 1)
