"""
Main Integration Test Runner
Coordinates all integration tests and generates comprehensive reports
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import argparse

# Import test modules
from orchestrator_tests import OrchestratorTests
from backend_tests import BackendTests
from frontend_tests import FrontendTests
from workflow_tests import WorkflowTests
from performance_tests import PerformanceTests


class IntegrationTestRunner:
    """Main test runner that coordinates all integration tests"""

    def __init__(self, verbose: bool = True, generate_report: bool = True):
        self.verbose = verbose
        self.generate_report = generate_report
        self.start_time = None
        self.end_time = None
        self.all_results = []

        # Initialize output directories
        self.test_results_dir = Path(__file__).parent.parent / "test_results"
        self.test_results_dir.mkdir(exist_ok=True)

        # Color codes for terminal output
        self.colors = {
            "GREEN": "\033[92m",
            "RED": "\033[91m",
            "YELLOW": "\033[93m",
            "BLUE": "\033[94m",
            "MAGENTA": "\033[95m",
            "CYAN": "\033[96m",
            "RESET": "\033[0m",
            "BOLD": "\033[1m"
        }

    def print_colored(self, message: str, color: str = "RESET"):
        """Print colored message to console"""
        if self.verbose:
            color_code = self.colors.get(color, self.colors["RESET"])
            print(f"{color_code}{message}{self.colors['RESET']}")

    def print_header(self, title: str):
        """Print formatted header"""
        self.print_colored("\n" + "=" * 60, "CYAN")
        self.print_colored(f"  {title}", "BOLD")
        self.print_colored("=" * 60, "CYAN")

    def print_progress(self, phase: str, current: int, total: int):
        """Print progress bar"""
        percent = (current / total) * 100
        bar_length = 40
        filled = int(bar_length * current / total)
        bar = "█" * filled + "░" * (bar_length - filled)

        self.print_colored(f"\n[{bar}] {percent:.1f}% - {phase}", "BLUE")

    def run_all_tests(self) -> Dict:
        """Master test runner - executes all test phases"""
        self.start_time = time.time()

        self.print_header("🧪 FULL INTEGRATION TEST SUITE")
        self.print_colored(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", "CYAN")

        # Define all test phases
        test_phases = [
            ("Orchestrator Tests", OrchestratorTests),
            ("Backend API Tests", BackendTests),
            ("Frontend Tests", FrontendTests),
            ("Workflow Tests", WorkflowTests),
            ("Performance Tests", PerformanceTests)
        ]

        total_phases = len(test_phases)
        phase_results = []

        # Execute each phase
        for idx, (phase_name, TestClass) in enumerate(test_phases, 1):
            self.print_progress(phase_name, idx - 1, total_phases)

            try:
                # Initialize and run test phase
                tester = TestClass(verbose=False)  # Disable verbose in individual tests
                results = tester.run_all_tests()

                phase_results.append(results)

                # Print phase summary
                passed = results.get("passed", 0)
                failed = results.get("failed", 0)
                total = results.get("total", 0)

                if failed == 0:
                    self.print_colored(f"✅ {phase_name}: {passed}/{total} passed", "GREEN")
                elif passed > failed:
                    self.print_colored(f"⚠️  {phase_name}: {passed}/{total} passed, {failed} failed", "YELLOW")
                else:
                    self.print_colored(f"❌ {phase_name}: {passed}/{total} passed, {failed} failed", "RED")

            except Exception as e:
                self.print_colored(f"❌ {phase_name}: Exception - {str(e)}", "RED")
                phase_results.append({
                    "category": phase_name,
                    "total": 0,
                    "passed": 0,
                    "failed": 1,
                    "tests": [{
                        "name": "phase_execution",
                        "passed": False,
                        "message": f"Exception: {str(e)}"
                    }]
                })

        self.print_progress("Complete", total_phases, total_phases)

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        # Calculate overall statistics
        total_tests = sum(r.get("total", 0) for r in phase_results)
        total_passed = sum(r.get("passed", 0) for r in phase_results)
        total_failed = sum(r.get("failed", 0) for r in phase_results)

        overall_results = {
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "phase_results": phase_results
        }

        self.all_results = overall_results

        # Print summary
        self.print_summary()

        # Generate report if requested
        if self.generate_report:
            self.generate_markdown_report()

        return overall_results

    def print_summary(self):
        """Print colored summary to console"""
        self.print_header("📊 TEST SUMMARY")

        if not self.all_results:
            self.print_colored("No results available", "RED")
            return

        total_tests = self.all_results["total_tests"]
        total_passed = self.all_results["total_passed"]
        total_failed = self.all_results["total_failed"]
        duration = self.all_results["duration"]

        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

        # Overall status
        if total_failed == 0:
            self.print_colored(f"\n✅ ALL TESTS PASSED! ({total_passed}/{total_tests})", "GREEN")
        elif success_rate >= 80:
            self.print_colored(f"\n⚠️  MOSTLY PASSED ({total_passed}/{total_tests} - {success_rate:.1f}%)", "YELLOW")
        else:
            self.print_colored(f"\n❌ MANY FAILURES ({total_passed}/{total_tests} - {success_rate:.1f}%)", "RED")

        self.print_colored(f"\nTotal Tests: {total_tests}", "CYAN")
        self.print_colored(f"✅ Passed: {total_passed}", "GREEN")
        self.print_colored(f"❌ Failed: {total_failed}", "RED")
        self.print_colored(f"⏱️  Duration: {duration:.2f}s", "BLUE")

        # Phase breakdown
        self.print_colored("\n📋 Results by Phase:", "CYAN")
        for phase in self.all_results["phase_results"]:
            category = phase.get("category", "Unknown")
            passed = phase.get("passed", 0)
            failed = phase.get("failed", 0)
            total = phase.get("total", 0)

            status_icon = "✅" if failed == 0 else "⚠️" if passed > failed else "❌"
            color = "GREEN" if failed == 0 else "YELLOW" if passed > failed else "RED"

            self.print_colored(f"  {status_icon} {category}: {passed}/{total} passed", color)

        # Failed tests details
        if total_failed > 0:
            self.print_colored("\n❌ Failed Tests:", "RED")
            for phase in self.all_results["phase_results"]:
                for test in phase.get("tests", []):
                    if not test.get("passed", False):
                        test_name = test.get("name", "unknown")
                        message = test.get("message", "No message")
                        self.print_colored(f"  • {phase['category']}.{test_name}", "RED")
                        self.print_colored(f"    {message}", "YELLOW")

        self.print_colored("\n" + "=" * 60, "CYAN")

    def generate_markdown_report(self):
        """Generate detailed markdown report"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_path = self.test_results_dir / f"integration_report_{timestamp}.md"

        if not self.all_results:
            self.print_colored("No results to generate report", "RED")
            return

        total_tests = self.all_results["total_tests"]
        total_passed = self.all_results["total_passed"]
        total_failed = self.all_results["total_failed"]
        duration = self.all_results["duration"]
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

        # Generate markdown content
        report_content = f"""# Integration Test Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Duration:** {duration:.2f}s
**Test Suite Version:** 1.0.0

---

## 📊 Summary

{"✅ **ALL TESTS PASSED!**" if total_failed == 0 else f"⚠️ **{total_failed} TEST(S) FAILED**"}

- **Total Tests:** {total_tests}
- **✅ Passed:** {total_passed} ({success_rate:.1f}%)
- **❌ Failed:** {total_failed}
- **⏱️ Duration:** {duration:.2f}s

---

## 📋 Results by Category

"""

        # Add results for each phase
        for phase in self.all_results["phase_results"]:
            category = phase.get("category", "Unknown")
            passed = phase.get("passed", 0)
            failed = phase.get("failed", 0)
            total = phase.get("total", 0)

            status = "✅" if failed == 0 else "⚠️" if passed > failed else "❌"

            report_content += f"""
### {status} {category} ({passed}/{total})

"""

            # List all tests in this phase
            for test in phase.get("tests", []):
                test_name = test.get("name", "unknown")
                test_passed = test.get("passed", False)
                test_message = test.get("message", "")

                checkbox = "[x]" if test_passed else "[ ]"
                status_emoji = "✅" if test_passed else "❌"

                report_content += f"- {checkbox} **{test_name}** {status_emoji}\n"
                if not test_passed:
                    report_content += f"  - Error: `{test_message}`\n"

        # Add failed tests section
        if total_failed > 0:
            report_content += """
---

## ❌ Failed Tests Details

"""

            for phase in self.all_results["phase_results"]:
                phase_has_failures = False
                for test in phase.get("tests", []):
                    if not test.get("passed", False):
                        if not phase_has_failures:
                            report_content += f"\n### {phase['category']}\n\n"
                            phase_has_failures = True

                        test_name = test.get("name", "unknown")
                        test_message = test.get("message", "No message")

                        report_content += f"""
**Test:** `{test_name}`
**Error:** {test_message}
**Recommendation:** Investigate and fix this issue

"""

        # Add recommendations
        report_content += """
---

## 💡 Recommendations

"""

        if total_failed == 0:
            report_content += """
✅ All tests passed! System is healthy.

**Next Steps:**
- Monitor system in production
- Consider adding more edge case tests
- Setup CI/CD pipeline with these tests

"""
        else:
            report_content += f"""
⚠️ {total_failed} test(s) failed. Please review and fix.

**Priority Actions:**
1. Review failed tests above
2. Check service logs for errors
3. Verify all services are running
4. Re-run tests after fixes

**Common Issues:**
- Services not running (orchestrator, backend, frontend)
- Port conflicts
- Database not initialized
- CORS configuration issues

"""

        report_content += """
---

## 🔄 Next Steps

- [ ] Fix all failed tests
- [ ] Re-run integration tests
- [ ] Deploy to staging environment
- [ ] Setup continuous integration
- [ ] Configure monitoring and alerts

---

**Report generated by Music Agents Integration Test Suite v1.0.0**
"""

        # Write report to file
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_content)

            self.print_colored(f"\n📄 Report saved: {report_path}", "GREEN")

            # Also save JSON report
            json_path = self.test_results_dir / f"integration_report_{timestamp}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(self.all_results, f, indent=2)

            self.print_colored(f"📄 JSON report saved: {json_path}", "GREEN")

        except Exception as e:
            self.print_colored(f"❌ Error saving report: {str(e)}", "RED")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Music Agents Integration Test Suite")
    parser.add_argument("--no-report", action="store_true", help="Skip report generation")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    parser.add_argument("--generate-report", action="store_true", help="Only generate report from last run")

    args = parser.parse_args()

    # Create test runner
    runner = IntegrationTestRunner(
        verbose=not args.quiet,
        generate_report=not args.no_report
    )

    if args.generate_report:
        # Only generate report
        if runner.all_results:
            runner.generate_markdown_report()
        else:
            print("No test results available. Run tests first.")
            sys.exit(1)
    else:
        # Run all tests
        results = runner.run_all_tests()

        # Exit with error code if any tests failed
        if results["total_failed"] > 0:
            sys.exit(1)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
