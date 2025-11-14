# Integration Testing Suite

Comprehensive integration testing for the Music Agents System.

## 📋 Overview

This test suite provides **full integration testing** for:
- **Orchestrator** (Port 8000) - Agent management and coordination
- **Backend API** (Port 5000) - 26+ API endpoints
- **Frontend** (Port 5173) - React application
- **End-to-End Workflows** - Complete user scenarios
- **Performance Metrics** - Response times, memory usage, concurrency

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r tests/requirements.txt
```

### 2. Start All Services

**Terminal 1: Orchestrator**
```bash
cd orchestrator
python main.py
```

**Terminal 2: Backend**
```bash
cd dashboard/backend
python app.py
```

**Terminal 3: Frontend** (Optional)
```bash
cd dashboard/frontend
npm run dev
```

### 3. Run Tests

```bash
./run_integration_tests.sh
```

## 📁 Test Structure

```
tests/
├── __init__.py
├── integration_test.py           # Main test runner (300 lines)
├── orchestrator_tests.py         # Orchestrator health checks (150 lines)
├── backend_tests.py              # Backend API validation (250 lines)
├── frontend_tests.py             # Frontend connectivity (100 lines)
├── workflow_tests.py             # End-to-end workflows (200 lines)
├── performance_tests.py          # Performance benchmarks (150 lines)
├── requirements.txt              # Test dependencies
├── test_report_template.md       # Report template
└── README.md                     # This file

run_integration_tests.sh          # Bash runner script (root)
test_results/                     # Generated reports (auto-created)
```

## 🧪 Test Categories

### 1. Orchestrator Tests (6 tests)
- ✅ Orchestrator running on port 8000
- ✅ All 12 agents online
- ✅ Database initialized
- ✅ Training pipeline active
- ✅ Universal Harvester (Agent 12) running
- ✅ Port accessibility

### 2. Backend API Tests (7 tests)
- ✅ Backend running on port 5000
- ✅ All 26 endpoints responding
- ✅ Database connection
- ✅ CORS configuration
- ✅ Response times < 500ms
- ✅ Data consistency
- ✅ Error handling

### 3. Frontend Tests (5 tests)
- ✅ Frontend running on port 5173
- ✅ Build compiles without errors
- ✅ No TypeScript errors
- ✅ Backend connection established
- ✅ Components importable

### 4. Workflow Tests (7 tests)
- ✅ Create project
- ✅ Add scenes
- ✅ Save project
- ✅ Export project
- ✅ Fetch video list
- ✅ Data persistence
- ✅ Delete project

### 5. Performance Tests (5 tests)
- ✅ API response times
- ✅ Frontend load time
- ✅ Memory usage
- ✅ Concurrent request handling
- ✅ Database query speed

**Total: 30 comprehensive tests**

## 🎯 Usage Examples

### Run All Tests
```bash
./run_integration_tests.sh
```

### Skip Service Checks
```bash
./run_integration_tests.sh --skip-checks
```

### Install Dependencies and Run
```bash
./run_integration_tests.sh --install-deps
```

### Run Without Report Generation
```bash
./run_integration_tests.sh --no-report
```

### Quiet Mode (Minimal Output)
```bash
./run_integration_tests.sh --quiet
```

### Run Specific Test Module
```bash
python tests/orchestrator_tests.py
python tests/backend_tests.py
python tests/frontend_tests.py
python tests/workflow_tests.py
python tests/performance_tests.py
```

### Run with pytest
```bash
pytest tests/backend_tests.py -v
pytest tests/ -v
```

## 📊 Output & Reports

### Console Output

```
═══════════════════════════════════════════════════════════
   🧪 MUSIC AGENTS - FULL INTEGRATION TEST SUITE
═══════════════════════════════════════════════════════════

Phase 1: Service Availability Checks

✅ Orchestrator running on port 8000
✅ Backend API running on port 5000
✅ Frontend running on port 5173

Phase 2: Running Integration Tests

[████████████████████████████████████████] 100% - Complete

✅ Orchestrator Tests: 6/6 passed
✅ Backend API Tests: 7/7 passed
✅ Frontend Tests: 5/5 passed
✅ Workflow Tests: 7/7 passed
✅ Performance Tests: 5/5 passed

═══════════════════════════════════════════════════════════
📊 TEST SUMMARY
═══════════════════════════════════════════════════════════

✅ ALL TESTS PASSED! (30/30)

Total Tests: 30
✅ Passed: 30
❌ Failed: 0
⏱️  Duration: 23.45s
```

### Generated Reports

**Markdown Report** (`test_results/integration_report_YYYY-MM-DD_HH-MM-SS.md`)
- Detailed test results
- Failed test analysis
- Performance metrics
- Recommendations

**JSON Report** (`test_results/integration_report_YYYY-MM-DD_HH-MM-SS.json`)
- Machine-readable format
- CI/CD integration
- Historical tracking

## 🔧 Troubleshooting

### Services Not Running

```bash
# Check if ports are in use
netstat -tuln | grep -E '5000|5173|8000'

# Start services manually
cd orchestrator && python main.py &
cd dashboard/backend && python app.py &
cd dashboard/frontend && npm run dev &
```

### Import Errors

```bash
# Install missing dependencies
pip install -r tests/requirements.txt

# Verify Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Port Conflicts

```bash
# Kill processes on specific ports
kill $(lsof -t -i:8000)
kill $(lsof -t -i:5000)
kill $(lsof -t -i:5173)
```

### Tests Fail with Connection Errors

1. Verify all services are running
2. Check firewall settings
3. Ensure ports 5000, 5173, 8000 are open
4. Try running with `--skip-checks` to bypass pre-checks

## 📈 Performance Benchmarks

### Expected Response Times

| Endpoint | Target | Good | Acceptable |
|----------|--------|------|------------|
| Dashboard Overview | < 200ms | < 500ms | < 2000ms |
| Agent Status | < 100ms | < 300ms | < 1000ms |
| Training Status | < 150ms | < 400ms | < 1500ms |
| Frontend Load | < 1s | < 3s | < 5s |

### Memory Usage

- Backend: < 200MB
- Frontend: < 100MB
- System: < 90% total

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install -r tests/requirements.txt
      - name: Start services
        run: |
          cd orchestrator && python main.py &
          cd dashboard/backend && python app.py &
      - name: Run tests
        run: ./run_integration_tests.sh
```

## 📚 Documentation

- **Test Report Template**: `test_report_template.md`
- **Test Results**: `test_results/` (auto-generated)
- **Individual Tests**: Each test file is self-documenting

## 🤝 Contributing

When adding new tests:
1. Follow existing test structure
2. Use descriptive test names
3. Include error messages
4. Update this README
5. Add to `integration_test.py` if needed

## 📞 Support

If tests fail repeatedly:
1. Review test report in `test_results/`
2. Check service logs
3. Verify environment setup
4. Consult main project README

---

**Test Suite Version:** 1.0.0
**Last Updated:** 2025-11-14
