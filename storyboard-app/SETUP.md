# 🛠️ Storyboard App - Detailed Setup Guide

Complete setup instructions for the Storyboard Video Production App.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Google Cloud Setup](#google-cloud-setup)
3. [Runway Setup](#runway-setup)
4. [Local Development](#local-development)
5. [Environment Configuration](#environment-configuration)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts

- ✅ **Google Cloud Account** (with billing enabled)
- ✅ **Runway Account** (runwayml.com)
- ✅ **Node.js 18+** installed
- ✅ **npm or yarn** package manager

### Estimated Costs

- Google Cloud Vertex AI: ~$0.002 per 1K characters
- Runway Gen-4: ~$0.05-0.10 per second of video
- Total for MVP testing: ~$10-20

---

## Google Cloud Setup

### Step 1: Create Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **Select a project** → **New Project**
3. Enter project name: `storyboard-app`
4. Click **Create**

### Step 2: Enable APIs

```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Enable Google Drive API
gcloud services enable drive.googleapis.com

# Enable OAuth 2.0
gcloud services enable oauth2.googleapis.com
```

Or via Console:
1. Navigate to **APIs & Services** → **Library**
2. Search and enable:
   - ✅ Vertex AI API
   - ✅ Google Drive API
   - ✅ Cloud Resource Manager API

### Step 3: Create OAuth 2.0 Credentials

1. Navigate to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Configure consent screen:
   - User Type: **External**
   - App name: `Storyboard App`
   - User support email: your-email@gmail.com
   - Scopes: Add these scopes:
     - `https://www.googleapis.com/auth/cloud-platform`
     - `https://www.googleapis.com/auth/drive.file`
     - `openid`, `profile`, `email`
4. Create OAuth 2.0 Client ID:
   - Application type: **Web application**
   - Name: `Storyboard App Client`
   - Authorized redirect URIs:
     - `http://localhost:3000/api/auth/callback`
     - `https://your-domain.com/api/auth/callback` (production)
5. Click **Create**
6. **Download JSON** or copy:
   - Client ID
   - Client Secret

### Step 4: Configure Gemini Agents

#### Option A: Use Pre-built Agents (Recommended for MVP)

The app works with Gemini models directly. No additional agent configuration required.

#### Option B: Create Custom Agents (Advanced)

1. Navigate to **Vertex AI** → **Agent Builder**
2. Click **Create Agent**
3. Configure each agent:

**Agent 1: Cinematic Director**
```
Name: Cinematic Director Agent
Model: gemini-2.0-flash-exp
System Instruction: You are an expert film director...
Tools: None (prompt-based)
```

**Agent 2: Scene Architect**
```
Name: Scene Architect Agent
Model: gemini-1.5-pro
System Instruction: You are a master storyboard artist...
Tools: None (prompt-based)
```

**Agent 3: Visual Effects**
```
Name: Visual Effects Agent
Model: gemini-1.5-pro
System Instruction: You are a VFX specialist...
Tools: None (prompt-based)
```

**Agent 4: Music Video Specialist**
```
Name: Music Video Specialist
Model: gemini-2.0-flash-exp
System Instruction: You are a music video producer...
Tools: None (prompt-based)
```

4. Note agent IDs (if using custom agents)

### Step 5: Set Up Service Account (Optional)

For production environments:

```bash
# Create service account
gcloud iam service-accounts create storyboard-app \
  --display-name="Storyboard App Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:storyboard-app@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=storyboard-app@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

---

## Runway Setup

### Step 1: Create Account

1. Go to [runwayml.com](https://runwayml.com)
2. Sign up / Log in
3. Navigate to **Settings** → **API Keys**

### Step 2: Generate API Key

1. Click **Generate New API Key**
2. Name: `Storyboard App`
3. Copy the API key
4. **Save it securely** (you won't see it again)

### Step 3: Add Credits

1. Navigate to **Billing**
2. Add credits (minimum $10 recommended for testing)
3. Gen-4 pricing: ~$0.05-0.10 per second

---

## Local Development

### Step 1: Install Dependencies

```bash
cd storyboard-app
npm install
```

### Step 2: Configure Environment

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
# Google Cloud Configuration
GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxx
GOOGLE_PROJECT_ID=storyboard-app-123456
GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/callback

# Vertex AI Configuration
VERTEX_AI_LOCATION=us-central1

# Runway API Configuration
RUNWAY_API_KEY=rw_xxxxxxxxxxxxx
RUNWAY_API_URL=https://api.runwayml.com/v1

# Application Configuration
NEXT_PUBLIC_API_URL=http://localhost:3001
JWT_SECRET=$(openssl rand -base64 32)
ENCRYPTION_KEY=$(openssl rand -base64 32)

# Server Configuration
PORT=3001
NODE_ENV=development
```

### Step 3: Generate Secrets

```bash
# Generate JWT secret
openssl rand -base64 32

# Generate encryption key
openssl rand -base64 32
```

Copy these into `.env.local`

### Step 4: Start Development Servers

**Terminal 1 - Backend:**
```bash
npm run server
```

Expected output:
```
🚀 Storyboard API Server running on http://localhost:3001
📍 Environment: development
🌐 CORS enabled for: http://localhost:3000
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

Expected output:
```
▲ Next.js 14.2.18
- Local:        http://localhost:3000
- ready started server on 0.0.0.0:3000
```

### Step 5: Verify Setup

1. Open `http://localhost:3000`
2. You should see the landing page
3. Click **Launch App**
4. Test agent selection and prompts

---

## Environment Configuration

### Development

```env
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:3001
```

### Production

```env
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.your-domain.com
GOOGLE_REDIRECT_URI=https://your-domain.com/api/auth/callback
```

### Security Notes

- ✅ Never commit `.env.local` to git
- ✅ Use different keys for dev/prod
- ✅ Rotate secrets every 90 days
- ✅ Use secret management in production (Google Secret Manager)

---

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Vertex AI API not enabled"

**Solution:**
```bash
gcloud services enable aiplatform.googleapis.com
```

### Issue: "OAuth redirect URI mismatch"

**Solution:**
1. Go to Google Cloud Console → Credentials
2. Edit OAuth 2.0 Client
3. Add exact redirect URI: `http://localhost:3000/api/auth/callback`
4. Wait 5 minutes for changes to propagate

### Issue: "Runway API 401 Unauthorized"

**Solution:**
- Verify `RUNWAY_API_KEY` is correct
- Check API key hasn't expired
- Ensure billing/credits are active

### Issue: "CORS error"

**Solution:**
- Check `NEXT_PUBLIC_API_URL` matches backend URL
- Ensure backend is running on correct port
- Clear browser cache

### Issue: "Agent response timeout"

**Solution:**
- Increase timeout in `server/routes/agents.js`
- Check Google Cloud quotas
- Verify internet connection

### Issue: Port already in use

**Solution:**
```bash
# Find process using port 3001
lsof -ti:3001 | xargs kill -9

# Or use different port
PORT=3002 npm run server
```

---

## Verification Checklist

Before building, verify:

- [ ] Node.js 18+ installed (`node --version`)
- [ ] Google Cloud project created
- [ ] Vertex AI API enabled
- [ ] OAuth 2.0 credentials configured
- [ ] Runway API key obtained
- [ ] `.env.local` configured with all values
- [ ] Dependencies installed (`npm install`)
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access `http://localhost:3000`
- [ ] Can select agents
- [ ] No console errors

---

## Next Steps

1. ✅ Complete setup above
2. 🎬 Test agent enhancement
3. 🎥 Test video generation
4. 📤 Test export functionality
5. 🚀 Deploy to production

---

## Support

If you encounter issues:

1. Check [README.md](./README.md) for common solutions
2. Review logs in terminal
3. Check Google Cloud Console for API errors
4. Verify all environment variables are set

**Happy building! 🎬✨**
