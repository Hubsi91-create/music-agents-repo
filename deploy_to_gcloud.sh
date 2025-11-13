#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Agent 8 Google Cloud Deployment${NC}"
echo ""

# Step 1: Check if gcloud is installed
echo -e "${BLUE}Step 1: Checking gcloud CLI...${NC}"
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI not installed${NC}"
    echo "Download from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi
echo -e "${GREEN}✅ gcloud CLI found${NC}"
echo ""

# Step 2: Authenticate
echo -e "${BLUE}Step 2: Authenticating with Google Cloud...${NC}"
gcloud auth login
echo ""

# Step 3: Set project
echo -e "${BLUE}Step 3: Setting up project...${NC}"
read -p "Enter your Google Cloud Project ID: " PROJECT_ID
gcloud config set project $PROJECT_ID
echo ""

# Step 4: Deploy
echo -e "${BLUE}Step 4: Deploying Agent 8 to Google Cloud Functions...${NC}"
gcloud functions deploy agent-8-prompt-refiner \
  --gen2 \
  --runtime python311 \
  --region europe-west3 \
  --source . \
  --entry-point validate_prompt \
  --trigger-http \
  --allow-unauthenticated \
  --memory 512MB \
  --timeout 60s \
  --max-instances 10 \
  --set-env-vars ENVIRONMENT=production,LOG_LEVEL=INFO

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo ""
    echo -e "${BLUE}Getting function URL...${NC}"
    FUNCTION_URL=$(gcloud functions describe agent-8-prompt-refiner \
      --region europe-west3 \
      --format='value(serviceConfig.uri)')

    echo -e "${GREEN}✅ Function URL:${NC}"
    echo $FUNCTION_URL

    echo ""
    echo -e "${BLUE}📋 Next steps:${NC}"
    echo "1. Update Agent 5a/5b with this URL"
    echo "2. Test the endpoint"
    echo "3. Monitor in Google Cloud Console"
else
    echo -e "${RED}❌ Deployment failed${NC}"
    exit 1
fi
