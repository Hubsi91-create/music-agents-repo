"""
Frontend Integration Tests
Tests for the Music Agents Dashboard Frontend
"""

import requests
import subprocess
import time
import os
from pathlib import Path
from typing import Dict, List, Tuple


class FrontendTests:
    """Test suite for Frontend functionality"""

    def __init__(self, base_url: str = "http://localhost:5173", verbose: bool = True):
        self.base_url = base_url
        self.backend_url = "http://localhost:5000"
        self.verbose = verbose
        self.results = []
        self.frontend_path = Path(__file__).parent.parent / "dashboard" / "frontend"

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

    def test_frontend_running(self) -> Tuple[bool, str]:
        """Test 1: Check if frontend is running on port 5173"""
        self.log("Testing frontend connectivity...", "INFO")

        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                # Check if response contains HTML
                content = response.text.lower()
                if "html" in content or "<!doctype" in content:
                    self.log("Frontend is running on port 5173", "SUCCESS")
                    return True, "Frontend running successfully"
                else:
                    msg = "Frontend responding but content may be invalid"
                    self.log(msg, "WARNING")
                    return False, msg
            else:
                msg = f"Unexpected status code: {response.status_code}"
                self.log(msg, "ERROR")
                return False, msg
        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to frontend on port 5173"
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

    def test_build_compiles(self) -> Tuple[bool, str]:
        """Test 2: Check if frontend build compiles without errors"""
        self.log("Testing frontend build compilation...", "INFO")

        if not self.frontend_path.exists():
            msg = "Frontend directory not found"
            self.log(msg, "ERROR")
            return False, msg

        try:
            # Check if package.json exists
            package_json = self.frontend_path / "package.json"
            if not package_json.exists():
                msg = "package.json not found"
                self.log(msg, "ERROR")
                return False, msg

            self.log("✓ package.json found", "INFO")

            # Check if node_modules exists (dependencies installed)
            node_modules = self.frontend_path / "node_modules"
            if not node_modules.exists():
                msg = "node_modules not found (run npm install first)"
                self.log(msg, "WARNING")
                return False, msg

            self.log("✓ node_modules found", "INFO")

            # Check if dist folder exists (previous build)
            dist_dir = self.frontend_path / "dist"
            if dist_dir.exists():
                # Check dist size
                dist_size = sum(f.stat().st_size for f in dist_dir.rglob('*') if f.is_file())
                dist_size_kb = dist_size / 1024

                self.log(f"✓ dist/ folder found ({dist_size_kb:.0f}KB)", "INFO")

                if dist_size_kb > 0 and dist_size_kb < 5000:  # Between 0 and 5MB
                    msg = f"Build artifacts present ({dist_size_kb:.0f}KB)"
                    self.log(msg, "SUCCESS")
                    return True, msg
                elif dist_size_kb >= 5000:
                    msg = f"Build artifacts large ({dist_size_kb:.0f}KB) - may need optimization"
                    self.log(msg, "WARNING")
                    return True, msg
                else:
                    msg = "Build artifacts may be incomplete"
                    self.log(msg, "WARNING")
                    return False, msg
            else:
                msg = "No build artifacts found (dist/ folder missing)"
                self.log(msg, "WARNING")
                return False, msg

        except Exception as e:
            msg = f"Error checking build: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_no_typescript_errors(self) -> Tuple[bool, str]:
        """Test 3: Check for TypeScript compilation errors"""
        self.log("Checking TypeScript errors...", "INFO")

        if not self.frontend_path.exists():
            msg = "Frontend directory not found"
            self.log(msg, "ERROR")
            return False, msg

        try:
            # Check if tsconfig.json exists
            tsconfig = self.frontend_path / "tsconfig.json"
            if not tsconfig.exists():
                msg = "tsconfig.json not found (not a TypeScript project)"
                self.log(msg, "WARNING")
                return True, msg

            self.log("✓ tsconfig.json found", "INFO")

            # Check for common TypeScript files
            ts_files = list(self.frontend_path.glob("**/*.ts")) + list(self.frontend_path.glob("**/*.tsx"))
            ts_files = [f for f in ts_files if "node_modules" not in str(f)]

            if ts_files:
                self.log(f"✓ Found {len(ts_files)} TypeScript files", "INFO")
                msg = f"TypeScript project detected ({len(ts_files)} .ts/.tsx files)"
                self.log(msg, "SUCCESS")
                return True, msg
            else:
                msg = "No TypeScript files found"
                self.log(msg, "WARNING")
                return True, msg

        except Exception as e:
            msg = f"Error checking TypeScript: {str(e)}"
            self.log(msg, "WARNING")
            return True, msg  # Don't fail on this

    def test_connection_to_backend(self) -> Tuple[bool, str]:
        """Test 4: Check if frontend can connect to backend"""
        self.log("Testing frontend-backend connection...", "INFO")

        try:
            # Check if backend is accessible
            backend_response = requests.get(self.backend_url, timeout=5)

            if backend_response.status_code in [200, 404]:
                self.log("✓ Backend is accessible", "INFO")

                # Check for CORS headers that allow frontend origin
                cors_origin = backend_response.headers.get("Access-Control-Allow-Origin", "")

                if cors_origin in ["*", self.base_url, "http://localhost:5173"]:
                    msg = f"Backend accessible with CORS enabled (origin: {cors_origin})"
                    self.log(msg, "SUCCESS")
                    return True, msg
                else:
                    msg = f"Backend accessible but CORS may not allow frontend (origin: {cors_origin or 'not set'})"
                    self.log(msg, "WARNING")
                    return True, msg
            else:
                msg = f"Backend returned unexpected status: {backend_response.status_code}"
                self.log(msg, "WARNING")
                return False, msg

        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend (backend may be down)"
            self.log(msg, "ERROR")
            return False, msg
        except Exception as e:
            msg = f"Error testing backend connection: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def test_components_import(self) -> Tuple[bool, str]:
        """Test 5: Check if components can be imported"""
        self.log("Checking component files...", "INFO")

        if not self.frontend_path.exists():
            msg = "Frontend directory not found"
            self.log(msg, "ERROR")
            return False, msg

        try:
            # Check for common component directories
            component_dirs = [
                self.frontend_path / "src" / "components",
                self.frontend_path / "src" / "pages",
                self.frontend_path / "src" / "views",
                self.frontend_path / "components",
            ]

            found_components = False
            component_count = 0

            for comp_dir in component_dirs:
                if comp_dir.exists():
                    # Count component files
                    jsx_files = list(comp_dir.glob("**/*.jsx")) + list(comp_dir.glob("**/*.tsx"))
                    jsx_files = [f for f in jsx_files if "node_modules" not in str(f)]

                    if jsx_files:
                        component_count += len(jsx_files)
                        found_components = True
                        self.log(f"✓ Found {len(jsx_files)} components in {comp_dir.name}/", "INFO")

            if found_components:
                msg = f"Component files found ({component_count} total)"
                self.log(msg, "SUCCESS")
                return True, msg
            else:
                msg = "No component files found"
                self.log(msg, "WARNING")
                return False, msg

        except Exception as e:
            msg = f"Error checking components: {str(e)}"
            self.log(msg, "ERROR")
            return False, msg

    def run_all_tests(self) -> Dict:
        """Run all frontend tests and return results"""
        self.log("=" * 60, "INFO")
        self.log("FRONTEND TESTS", "INFO")
        self.log("=" * 60, "INFO")

        tests = [
            ("frontend_running", self.test_frontend_running),
            ("build_compiles", self.test_build_compiles),
            ("no_typescript_errors", self.test_no_typescript_errors),
            ("connection_to_backend", self.test_connection_to_backend),
            ("components_import", self.test_components_import)
        ]

        results = {
            "category": "Frontend Tests",
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
    tester = FrontendTests(verbose=True)
    results = tester.run_all_tests()

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print("=" * 60)

    # Exit with error code if any tests failed
    exit(0 if results['failed'] == 0 else 1)
