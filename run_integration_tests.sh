#!/bin/bash

# ═══════════════════════════════════════════════════════════
# Music Agents - Full Integration Test Suite Runner
# ═══════════════════════════════════════════════════════════

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# ASCII Art Header
print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "═══════════════════════════════════════════════════════════"
    echo "   🧪 MUSIC AGENTS - FULL INTEGRATION TEST SUITE"
    echo "═══════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo -e "${BLUE}Started: $(date '+%Y-%m-%d %H:%M:%S')${NC}\n"
}

# Check if a service is running
check_service() {
    local service_name=$1
    local port=$2
    local url=$3

    echo -e "${YELLOW}Checking ${service_name}...${NC}"

    if curl -s --connect-timeout 3 "${url}" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ ${service_name} running on port ${port}${NC}"
        return 0
    else
        echo -e "${RED}❌ ${service_name} NOT running on port ${port}!${NC}"
        return 1
    fi
}

# Print usage information
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --skip-checks       Skip service availability checks"
    echo "  --no-report         Skip report generation"
    echo "  --quiet             Minimal output"
    echo "  --install-deps      Install test dependencies"
    echo "  --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                  Run all tests with checks"
    echo "  $0 --skip-checks    Run tests without pre-checks"
    echo "  $0 --install-deps   Install dependencies and run tests"
}

# Install dependencies
install_dependencies() {
    echo -e "${YELLOW}Installing test dependencies...${NC}"

    if [ ! -f "tests/requirements.txt" ]; then
        echo -e "${RED}❌ requirements.txt not found!${NC}"
        exit 1
    fi

    pip install -r tests/requirements.txt

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependencies installed successfully${NC}\n"
    else
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        exit 1
    fi
}

# Parse command line arguments
SKIP_CHECKS=false
NO_REPORT=false
QUIET=false
INSTALL_DEPS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-checks)
            SKIP_CHECKS=true
            shift
            ;;
        --no-report)
            NO_REPORT=true
            shift
            ;;
        --quiet)
            QUIET=true
            shift
            ;;
        --install-deps)
            INSTALL_DEPS=true
            shift
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            print_usage
            exit 1
            ;;
    esac
done

# Print header
print_header

# Install dependencies if requested
if [ "$INSTALL_DEPS" = true ]; then
    install_dependencies
fi

# Service availability checks (unless skipped)
if [ "$SKIP_CHECKS" = false ]; then
    echo -e "${CYAN}${BOLD}Phase 1: Service Availability Checks${NC}\n"

    SERVICES_OK=true

    # Check Orchestrator
    if ! check_service "Orchestrator" "8000" "http://localhost:8000"; then
        echo -e "${YELLOW}   Start with: cd orchestrator && python main.py${NC}"
        SERVICES_OK=false
    fi
    echo ""

    # Check Backend
    if ! check_service "Backend API" "5000" "http://localhost:5000"; then
        echo -e "${YELLOW}   Start with: cd dashboard/backend && python app.py${NC}"
        SERVICES_OK=false
    fi
    echo ""

    # Check Frontend (optional)
    if ! check_service "Frontend" "5173" "http://localhost:5173"; then
        echo -e "${YELLOW}⚠️  Frontend NOT running (optional for API tests)${NC}"
        echo -e "${YELLOW}   Start with: cd dashboard/frontend && npm run dev${NC}"
    fi
    echo ""

    # Exit if critical services are down
    if [ "$SERVICES_OK" = false ]; then
        echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${RED}❌ Critical services are not running!${NC}"
        echo -e "${RED}   Please start the required services and try again.${NC}"
        echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
        exit 1
    fi
fi

# Run integration tests
echo -e "${CYAN}${BOLD}Phase 2: Running Integration Tests${NC}\n"

# Build Python command
PYTHON_CMD="python tests/integration_test.py"

if [ "$NO_REPORT" = true ]; then
    PYTHON_CMD="$PYTHON_CMD --no-report"
fi

if [ "$QUIET" = true ]; then
    PYTHON_CMD="$PYTHON_CMD --quiet"
fi

# Execute tests
$PYTHON_CMD

TEST_EXIT_CODE=$?

# Print final summary
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✅ ALL TESTS PASSED!${NC}"
    echo -e "${GREEN}   System is healthy and ready for deployment.${NC}"
else
    echo -e "${YELLOW}${BOLD}⚠️  SOME TESTS FAILED${NC}"
    echo -e "${YELLOW}   Review the test report for details.${NC}"
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"

# Show report location
if [ "$NO_REPORT" = false ]; then
    LATEST_REPORT=$(ls -t test_results/integration_report_*.md 2>/dev/null | head -1)
    if [ -n "$LATEST_REPORT" ]; then
        echo -e "${BLUE}📄 Test Report: ${LATEST_REPORT}${NC}"
    fi
fi

echo -e "${BLUE}Finished: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""

# Exit with same code as tests
exit $TEST_EXIT_CODE
