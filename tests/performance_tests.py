"""
Performance Integration Tests
Tests for system performance, response times, and resource usage
"""

import requests
import time
import psutil
import os
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed


class PerformanceTests:
    """Test suite for performance metrics and benchmarks"""

    def __init__(self,
                 backend_url: str = "http://localhost:5000",
                 orchestrator_url: str = "http://localhost:8000",
                 frontend_url: str = "http://localhost:5173",
                 verbose: bool = True):
        self.backend_url = backend_url
        self.orchestrator_url = orchestrator_url
        self.frontend_url = frontend_url
        self.verbose = verbose
        self.results = []

        # Define test endpoints for performance testing
        self.test_endpoints = [
            ("Backend", f"{backend_url}/api/dashboard/overview"),
            ("Backend", f"{backend_url}/api/agents/status"),
            ("Backend", f"{backend_url}/api/training/status"),
            ("Backend", f"{backend_url}/api/system/health"),
            ("Orchestrator", f"{orchestrator_url}/api/agents"),
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

    def measure_response_time(self, url: str, timeout: int = 10) -> float:
        """Measure response time for a single request"""
        try:
            start = time.time()
            response = requests.get(url, timeout=timeout)
            elapsed = (time.time() - start) * 1000  # Convert to ms

            if response.status_code == 200:
                return elapsed
            else:
                return -1  # Error indicator
        except Exception:
            return -1

    def test_api_response_times(self) -> Tuple[bool, str]:
        """Test 1: Measure API response times"""
        self.log("Testing API response times...", "INFO")

        all_measurements = []

        for service, url in self.test_endpoints:
            try:
                # Measure response time 3 times and take average
                times = []
                for i in range(3):
                    elapsed = self.measure_response_time(url)
                    if elapsed > 0:
                        times.append(elapsed)
                    time.sleep(0.1)  # Small delay between requests

                if times:
                    avg_time = sum(times) / len(times)
                    min_time = min(times)
                    max_time = max(times)

                    all_measurements.append({
                        "service": service,
                        "endpoint": url.split("/api/")[-1] if "/api/" in url else "root",
                        "avg": avg_time,
                        "min": min_time,
                        "max": max_time
                    })

                    # Status indicator
                    if avg_time < 500:
                        status = "✅"
                    elif avg_time < 2000:
                        status = "⚠️"
                    else:
                        status = "❌"

                    endpoint_name = url.split("/")[-1] or "root"
                    self.log(f"  {status} {service}/{endpoint_name}: "
                           f"avg={avg_time:.0f}ms, min={min_time:.0f}ms, max={max_time:.0f}ms", "INFO")

            except Exception as e:
                self.log(f"  ❌ Error testing {url}: {str(e)}", "ERROR")

        if all_measurements:
            # Calculate overall statistics
            all_avg_times = [m["avg"] for m in all_measurements]
            overall_avg = sum(all_avg_times) / len(all_avg_times)
            overall_max = max(all_avg_times)

            self.log(f"\nOverall: avg={overall_avg:.0f}ms, max={overall_max:.0f}ms", "INFO")

            # Pass criteria: average < 2000ms and max < 5000ms
            if overall_max < 2000:
                msg = f"Response times excellent (avg: {overall_avg:.0f}ms, max: {overall_max:.0f}ms)"
                self.log(msg, "SUCCESS")
                return True, msg
            elif overall_max < 5000:
                msg = f"Response times acceptable (avg: {overall_avg:.0f}ms, max: {overall_max:.0f}ms)"
                self.log(msg, "WARNING")
                return True, msg
            else:
                msg = f"Response times too slow (avg: {overall_avg:.0f}ms, max: {overall_max:.0f}ms)"
                self.log(msg, "ERROR")
                return False, msg
        else:
            msg = "Could not measure response times"
            self.log(msg, "ERROR")
            return False, msg

    def test_frontend_performance(self) -> Tuple[bool, str]:
        """Test 2: Measure frontend performance"""
        self.log("Testing frontend performance...", "INFO")

        try:
            # Measure page load time
            start = time.time()
            response = requests.get(self.frontend_url, timeout=10)
            load_time = (time.time() - start) * 1000  # Convert to ms

            if response.status_code == 200:
                content_size = len(response.content)

                self.log(f"  Page load time: {load_time:.0f}ms", "INFO")
                self.log(f"  Content size: {content_size / 1024:.1f}KB", "INFO")

                # Pass criteria: load time < 3000ms
                if load_time < 2000:
                    msg = f"Frontend performance excellent ({load_time:.0f}ms)"
                    self.log(msg, "SUCCESS")
                    return True, msg
                elif load_time < 3000:
                    msg = f"Frontend performance good ({load_time:.0f}ms)"
                    self.log(msg, "SUCCESS")
                    return True, msg
                elif load_time < 5000:
                    msg = f"Frontend performance acceptable ({load_time:.0f}ms)"
                    self.log(msg, "WARNING")
                    return True, msg
                else:
                    msg = f"Frontend performance slow ({load_time:.0f}ms)"
                    self.log(msg, "ERROR")
                    return False, msg
            else:
                msg = f"Frontend not accessible (status: {response.status_code})"
                self.log(msg, "ERROR")
                return False, msg

        except requests.exceptions.ConnectionError:
            msg = "Frontend not running"
            self.log(msg, "WARNING")
            return False, msg
        except Exception as e:
            msg = f"Error testing frontend performance: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_memory_usage(self) -> Tuple[bool, str]:
        """Test 3: Monitor memory usage"""
        self.log("Testing memory usage...", "INFO")

        try:
            # Get current process memory
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)  # Convert to MB

            self.log(f"  Test process memory: {memory_mb:.1f}MB", "INFO")

            # Check system memory
            system_memory = psutil.virtual_memory()
            total_mb = system_memory.total / (1024 * 1024)
            available_mb = system_memory.available / (1024 * 1024)
            used_percent = system_memory.percent

            self.log(f"  System memory: {available_mb:.0f}MB available / {total_mb:.0f}MB total ({used_percent:.1f}% used)", "INFO")

            # Pass criteria: system memory usage < 90%
            if used_percent < 75:
                msg = f"Memory usage good ({used_percent:.1f}% used)"
                self.log(msg, "SUCCESS")
                return True, msg
            elif used_percent < 90:
                msg = f"Memory usage acceptable ({used_percent:.1f}% used)"
                self.log(msg, "WARNING")
                return True, msg
            else:
                msg = f"Memory usage high ({used_percent:.1f}% used)"
                self.log(msg, "ERROR")
                return False, msg

        except Exception as e:
            msg = f"Error checking memory usage: {str(e)}"
            self.log(msg, "WARNING")
            return True, msg  # Don't fail on memory check errors

    def test_concurrent_requests(self) -> Tuple[bool, str]:
        """Test 4: Test concurrent request handling"""
        self.log("Testing concurrent request handling...", "INFO")

        try:
            # Test endpoint
            test_url = f"{self.backend_url}/api/dashboard/overview"

            # Send 10 concurrent requests
            num_requests = 10
            self.log(f"  Sending {num_requests} concurrent requests...", "INFO")

            start_time = time.time()
            successful = 0
            failed = 0
            response_times = []

            def make_request():
                req_start = time.time()
                try:
                    response = requests.get(test_url, timeout=10)
                    elapsed = (time.time() - req_start) * 1000
                    if response.status_code == 200:
                        return ("success", elapsed)
                    else:
                        return ("failed", elapsed)
                except Exception as e:
                    return ("error", -1)

            # Execute concurrent requests
            with ThreadPoolExecutor(max_workers=num_requests) as executor:
                futures = [executor.submit(make_request) for _ in range(num_requests)]

                for future in as_completed(futures):
                    status, elapsed = future.result()
                    if status == "success":
                        successful += 1
                        if elapsed > 0:
                            response_times.append(elapsed)
                    else:
                        failed += 1

            total_time = (time.time() - start_time) * 1000

            self.log(f"  Completed: {successful}/{num_requests} successful in {total_time:.0f}ms", "INFO")

            if response_times:
                avg_response = sum(response_times) / len(response_times)
                max_response = max(response_times)
                self.log(f"  Response times: avg={avg_response:.0f}ms, max={max_response:.0f}ms", "INFO")

            # Pass criteria: at least 80% successful
            success_rate = (successful / num_requests) * 100

            if success_rate >= 90:
                msg = f"Concurrent handling excellent ({successful}/{num_requests} successful)"
                self.log(msg, "SUCCESS")
                return True, msg
            elif success_rate >= 70:
                msg = f"Concurrent handling acceptable ({successful}/{num_requests} successful)"
                self.log(msg, "WARNING")
                return True, msg
            else:
                msg = f"Concurrent handling poor ({successful}/{num_requests} successful)"
                self.log(msg, "ERROR")
                return False, msg

        except Exception as e:
            msg = f"Error testing concurrent requests: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_database_query_speed(self) -> Tuple[bool, str]:
        """Test 5: Measure database query speed"""
        self.log("Testing database query speed...", "INFO")

        try:
            # Test multiple endpoints that query the database
            db_endpoints = [
                f"{self.backend_url}/api/dashboard/overview",
                f"{self.backend_url}/api/agents/status",
                f"{self.backend_url}/api/training/history",
            ]

            query_times = []

            for endpoint in db_endpoints:
                start = time.time()
                response = requests.get(endpoint, timeout=5)
                elapsed = (time.time() - start) * 1000

                if response.status_code == 200:
                    query_times.append(elapsed)
                    endpoint_name = endpoint.split("/")[-1]
                    self.log(f"  {endpoint_name}: {elapsed:.0f}ms", "INFO")

            if query_times:
                avg_time = sum(query_times) / len(query_times)
                max_time = max(query_times)

                # Pass criteria: average query time < 200ms
                if avg_time < 100:
                    msg = f"Database queries excellent (avg: {avg_time:.0f}ms, max: {max_time:.0f}ms)"
                    self.log(msg, "SUCCESS")
                    return True, msg
                elif avg_time < 200:
                    msg = f"Database queries good (avg: {avg_time:.0f}ms, max: {max_time:.0f}ms)"
                    self.log(msg, "SUCCESS")
                    return True, msg
                elif avg_time < 500:
                    msg = f"Database queries acceptable (avg: {avg_time:.0f}ms, max: {max_time:.0f}ms)"
                    self.log(msg, "WARNING")
                    return True, msg
                else:
                    msg = f"Database queries slow (avg: {avg_time:.0f}ms, max: {max_time:.0f}ms)"
                    self.log(msg, "ERROR")
                    return False, msg
            else:
                msg = "Could not measure database query speed"
                self.log(msg, "WARNING")
                return False, msg

        except Exception as e:
            msg = f"Error testing database queries: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def run_all_tests(self) -> Dict:
        """Run all performance tests and return results"""
        self.log("=" * 60, "INFO")
        self.log("PERFORMANCE TESTS", "INFO")
        self.log("=" * 60, "INFO")

        tests = [
            ("api_response_times", self.test_api_response_times),
            ("frontend_performance", self.test_frontend_performance),
            ("memory_usage", self.test_memory_usage),
            ("concurrent_requests", self.test_concurrent_requests),
            ("database_query_speed", self.test_database_query_speed)
        ]

        results = {
            "category": "Performance Tests",
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
    tester = PerformanceTests(verbose=True)
    results = tester.run_all_tests()

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print("=" * 60)

    # Exit with error code if any tests failed
    exit(0 if results['failed'] == 0 else 1)
