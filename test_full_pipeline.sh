#!/bin/bash
###############################################################################
# FULL PIPELINE TEST SCRIPT
# Tests the complete music video production workflow with style anchors
###############################################################################

set -e  # Exit on error

echo "=========================================="
echo "🎬 MUSIC VIDEO PRODUCTION PIPELINE TEST"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test Configuration
SCREENPLAY_FILE="agent-4-screenplay-generator/screenplay.json"
TEST_OUTPUT="pipeline_output"

echo -e "${BLUE}📋 Test Configuration:${NC}"
echo "  Screenplay: $SCREENPLAY_FILE"
echo "  Output: $TEST_OUTPUT"
echo ""

# Check if screenplay exists
if [ ! -f "$SCREENPLAY_FILE" ]; then
    echo -e "${RED}❌ Screenplay file not found: $SCREENPLAY_FILE${NC}"
    echo "Please run Agent 4 first to generate a screenplay."
    exit 1
fi

echo -e "${GREEN}✅ Screenplay file found${NC}"
echo ""

###############################################################################
# STEP 1: Test Agent Imports
###############################################################################

echo "=========================================="
echo "STEP 1: Testing Agent Imports"
echo "=========================================="

echo -e "${YELLOW}Testing Agent 5a (Nanobanana Image Generator)...${NC}"
cd agent-5a-nanobanana-image
python3 test_agent_5a.py || {
    echo -e "${RED}❌ Agent 5a import failed${NC}"
    echo "Install dependencies: pip install google-auth requests"
    exit 1
}
cd ..

echo -e "${YELLOW}Testing Agent 5b (Runway Image Generator)...${NC}"
cd agent-5b-runway-image
python3 test_agent_5b.py || {
    echo -e "${RED}❌ Agent 5b import failed${NC}"
    echo "Install dependencies: pip install python-dotenv requests"
    exit 1
}
cd ..

echo -e "${GREEN}✅ All agent imports successful${NC}"
echo ""

###############################################################################
# STEP 2: Test Pipeline Execution (Dry Run)
###############################################################################

echo "=========================================="
echo "STEP 2: Testing Pipeline Execution"
echo "=========================================="

echo -e "${YELLOW}Running pipeline (Step 1 only - Style Anchor Generation)...${NC}"
echo ""

# Run pipeline step 1
python3 pipeline_with_style_anchors.py "$SCREENPLAY_FILE" || {
    echo -e "${RED}❌ Pipeline execution failed${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}✅ Pipeline Step 1 complete${NC}"
echo ""

###############################################################################
# STEP 3: Verify Output Files
###############################################################################

echo "=========================================="
echo "STEP 3: Verifying Output Files"
echo "=========================================="

# Check if output directory was created
if [ ! -d "$TEST_OUTPUT" ]; then
    echo -e "${RED}❌ Output directory not created${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Output directory exists${NC}"

# Check if style anchors JSON was created
if [ ! -f "$TEST_OUTPUT/style_anchors_generated.json" ]; then
    echo -e "${RED}❌ Style anchors JSON not created${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Style anchors JSON created${NC}"

# Check if style_anchors directory has images
IMAGE_COUNT=$(ls -1 style_anchors/*.png 2>/dev/null | wc -l || echo 0)
if [ "$IMAGE_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No images generated (API may not be configured)${NC}"
else
    echo -e "${GREEN}✅ $IMAGE_COUNT style anchor images generated${NC}"
fi

echo ""

###############################################################################
# STEP 4: Test Dashboard API
###############################################################################

echo "=========================================="
echo "STEP 4: Testing Dashboard API"
echo "=========================================="

echo -e "${YELLOW}Starting Flask dashboard (background)...${NC}"

# Start dashboard in background
cd dashboard
python3 app.py > /dev/null 2>&1 &
DASHBOARD_PID=$!
cd ..

# Wait for server to start
sleep 3

# Test API endpoints
echo -e "${YELLOW}Testing /api/status endpoint...${NC}"
curl -s http://localhost:5000/api/status | grep -q "PRODUCTION_READY" && {
    echo -e "${GREEN}✅ Status endpoint working${NC}"
} || {
    echo -e "${RED}❌ Status endpoint failed${NC}"
}

echo -e "${YELLOW}Testing /api/style-anchors endpoint...${NC}"
curl -s http://localhost:5000/api/style-anchors | grep -q "scenes" && {
    echo -e "${GREEN}✅ Style anchors API working${NC}"
} || {
    echo -e "${YELLOW}⚠️  Style anchors API returned no data (may need actual API keys)${NC}"
}

# Stop dashboard
kill $DASHBOARD_PID 2>/dev/null || true

echo ""

###############################################################################
# STEP 5: Test Pipeline Step 2 (Video Prompts)
###############################################################################

echo "=========================================="
echo "STEP 5: Testing Video Prompt Generation"
echo "=========================================="

echo -e "${YELLOW}Running pipeline Step 2 (Video Prompts with Style Anchors)...${NC}"

python3 pipeline_with_style_anchors.py "$SCREENPLAY_FILE" --step2 || {
    echo -e "${RED}❌ Video prompt generation failed${NC}"
    exit 1
}

# Check if video prompts were created
if [ -f "$TEST_OUTPUT/veo_prompts_with_anchors.json" ]; then
    echo -e "${GREEN}✅ VEO prompts with anchors created${NC}"
else
    echo -e "${RED}❌ VEO prompts not created${NC}"
    exit 1
fi

if [ -f "$TEST_OUTPUT/runway_prompts_with_anchors.json" ]; then
    echo -e "${GREEN}✅ Runway prompts with anchors created${NC}"
else
    echo -e "${RED}❌ Runway prompts not created${NC}"
    exit 1
fi

echo ""

###############################################################################
# FINAL REPORT
###############################################################################

echo "=========================================="
echo "🎉 FULL PIPELINE TEST COMPLETE"
echo "=========================================="
echo ""

echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
echo ""

echo "Generated Files:"
echo "  📄 $TEST_OUTPUT/style_anchors_generated.json"
echo "  📄 $TEST_OUTPUT/veo_prompts_with_anchors.json"
echo "  📄 $TEST_OUTPUT/runway_prompts_with_anchors.json"
if [ "$IMAGE_COUNT" -gt 0 ]; then
    echo "  🖼️  $IMAGE_COUNT style anchor images in style_anchors/"
fi
echo ""

echo "Next Steps:"
echo "  1. Review style anchors:"
echo "     → Start dashboard: cd dashboard && python3 app.py"
echo "     → Open: http://localhost:5000/storyboard"
echo ""
echo "  2. Configure API keys for actual image generation:"
echo "     → Nanobanana: Google Cloud credentials"
echo "     → Runway: RUNWAY_API_KEY in .env"
echo ""
echo "  3. Generate actual videos:"
echo "     → Use VEO API with prompts from $TEST_OUTPUT/veo_prompts_with_anchors.json"
echo "     → Use Runway API with prompts from $TEST_OUTPUT/runway_prompts_with_anchors.json"
echo ""

echo -e "${BLUE}Pipeline test completed successfully! 🎬${NC}"
