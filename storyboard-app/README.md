# 🎬 Storyboard App - AI Music Video Production

Professional storyboard video production application with **Google Gemini Agent Integration** and **Runway Gen-4** video generation.

## ✨ Features

- 🤖 **Google Gemini Agent Integration** - Custom AI agents enhance your scene prompts
- 🎥 **Runway Gen-4 Video Generation** - Professional AI video creation
- 🎨 **Galaxy/Universe Neon Theme** - Beautiful cyberpunk-inspired UI
- 📊 **Real-time Progress Tracking** - Monitor video generation progress
- 🔐 **Secure API Key Management** - Encrypted storage with AES-256-GCM
- 🔄 **Google OAuth 2.0** - Seamless authentication
- 📤 **Google Drive Integration** - Export and share your videos
- 🎭 **Multiple Scene Management** - Create complex storyboards

## 🏗️ Architecture

```
┌─────────────────────┐
│   Next.js Frontend  │
│   (React 18 + TS)   │
└──────────┬──────────┘
           │
           │ HTTP/REST
           ↓
┌──────────────────────────────┐
│   Express.js Backend         │
│   (Node.js 18+)              │
└──────┬───────────────────────┘
       │
       ├──→ Google Cloud Vertex AI
       │    └─ Custom Gemini Agents
       │
       ├──→ Google OAuth 2.0
       │    └─ Authentication
       │
       └──→ Runway Gen-4 API
            └─ Video Generation
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Google Cloud account with:
  - Vertex AI API enabled
  - Custom Gemini Agents configured
  - OAuth 2.0 credentials
- Runway API key (from runwayml.com)

### Installation

1. **Clone and navigate:**
```bash
cd storyboard-app
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment:**
```bash
cp .env.local.example .env.local
```

Edit `.env.local` with your credentials:
```env
# Google Cloud Configuration
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_PROJECT_ID=your_project_id
GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/callback

# Vertex AI Configuration
VERTEX_AI_LOCATION=us-central1

# Runway API Configuration
RUNWAY_API_KEY=your_runway_api_key

# Application Configuration
NEXT_PUBLIC_API_URL=http://localhost:3001
JWT_SECRET=your_very_secure_jwt_secret_change_this
ENCRYPTION_KEY=your_32_character_encryption_key
```

4. **Start development servers:**

Terminal 1 - Backend:
```bash
npm run server
```

Terminal 2 - Frontend:
```bash
npm run dev
```

5. **Open app:**
```
http://localhost:3000
```

## 🔧 Configuration

### Google Cloud Setup

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create new project or select existing

2. **Enable APIs:**
   - Vertex AI API
   - Google Drive API
   - OAuth 2.0

3. **Create OAuth 2.0 Credentials:**
   - Navigate to APIs & Services > Credentials
   - Create OAuth 2.0 Client ID
   - Add authorized redirect URI: `http://localhost:3000/api/auth/callback`

4. **Configure Gemini Agents:**
   - Go to Vertex AI > Agent Builder
   - Create custom agents for:
     - Cinematic Director
     - Scene Architect
     - Visual Effects
     - Music Video Specialist
   - Note agent IDs for configuration

### Runway Setup

1. Get API key from [runwayml.com](https://runwayml.com)
2. Add to `.env.local` as `RUNWAY_API_KEY`

## 📖 Usage

### Creating a Scene

1. Click **+ ADD SCENE** in left sidebar
2. Select a **Gemini Agent** from dropdown
3. Enter your **scene prompt**
4. Click **🤖 ENHANCE WITH AGENT** to improve prompt
5. Review enhanced prompt with suggestions
6. Click **🎬 GENERATE** to create video
7. Monitor progress in real-time
8. Click **⭐ SAVE** when complete

### Agent Types

| Agent | Purpose |
|-------|---------|
| 🎬 **Cinematic Director** | Shot composition, camera movements, storytelling |
| 🏗️ **Scene Architect** | Detailed scene breakdowns, locations, props |
| ✨ **Visual Effects** | VFX enhancements, transitions, post-production |
| 🎵 **Music Video Specialist** | Music sync, rhythm, genre-specific aesthetics |

### Keyboard Shortcuts

- `Cmd/Ctrl + N` - New scene
- `Cmd/Ctrl + S` - Save current scene
- `Cmd/Ctrl + E` - Export project
- `Space` - Play/pause video preview

## 🎨 Design System

### Color Palette

```css
Primary Background:   #0a0e27 (Deep Space Dark)
Surface Dark:         #1a1f3a (Cards, Containers)
Surface Light:        #252d4a (Hover States)

Neon Cyan (Primary):  #00f0ff (Main accent, glows)
Energy Red (Accent):  #ff1744 (Important actions)
Nebula Purple:        #b24bff (Secondary actions)
Success Green:        #00e676 (Status indicators)
Plasma Yellow:        #ffeb3b (Warnings)

Text Primary:         #e0e8ff (High contrast)
Text Secondary:       #a0aff0 (Muted text)
```

### Components

- **NeonButton** - Glowing pill-shaped buttons
- **NeonInput** - Futuristic input fields
- **ProgressRing** - Circular progress indicator
- **LoadingSpinner** - Animated neon spinner
- **SceneCard** - Complete scene management
- **AgentSelector** - AI agent selection
- **EnhancedPromptDisplay** - Agent-enhanced results

## 🔐 Security

- API keys encrypted with AES-256-GCM
- JWT sessions with httpOnly cookies
- OAuth 2.0 token management
- HTTPS required in production
- Rate limiting on all endpoints
- No API keys sent to frontend

## 📊 API Endpoints

### Authentication
- `GET /api/auth/google` - Get OAuth URL
- `POST /api/auth/google/callback` - Handle OAuth callback
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout user

### Agents
- `GET /api/agents` - List available agents
- `POST /api/agents/call` - Call agent to enhance prompt

### Runway
- `POST /api/runway/generate` - Start video generation
- `GET /api/runway/status/:taskId` - Get generation status
- `DELETE /api/runway/cancel/:taskId` - Cancel generation

## 🚀 Deployment

### Vercel (Frontend)

```bash
npm run build
vercel deploy
```

### Google Cloud Run (Backend)

```bash
# Build container
docker build -t gcr.io/[PROJECT-ID]/storyboard-api ./server

# Push to registry
docker push gcr.io/[PROJECT-ID]/storyboard-api

# Deploy to Cloud Run
gcloud run deploy storyboard-api \
  --image gcr.io/[PROJECT-ID]/storyboard-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📈 Performance

- Agent calls: < 10 seconds
- Video generation: 2-3 minutes average
- UI render: < 1 second
- API response: < 200ms (excluding external calls)

## 🔧 Troubleshooting

### "Agent call failed"
- Verify `GOOGLE_PROJECT_ID` is correct
- Check Vertex AI API is enabled
- Ensure agents are configured in Vertex AI

### "Runway API not configured"
- Add `RUNWAY_API_KEY` to `.env.local`
- Verify API key is valid

### "Authentication required"
- Clear cookies and re-authenticate
- Check OAuth credentials are correct

## 📚 Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- TailwindCSS

**Backend:**
- Express.js
- Node.js 18+
- Google Cloud Vertex AI
- Runway Gen-4 API

**Security:**
- JWT (jsonwebtoken)
- AES-256-GCM encryption
- Google OAuth 2.0

## 🎯 Roadmap

- [ ] Real-time collaboration
- [ ] Agent response streaming
- [ ] Custom agent creation
- [ ] Template library
- [ ] Batch video generation
- [ ] Advanced timeline editing

## 📝 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📞 Support

- Issues: [GitHub Issues](https://github.com/your-repo/issues)
- Docs: [Full Documentation](https://docs.your-domain.com)
- Email: support@your-domain.com

---

**Built with ❤️ using Claude Code**

*Powered by Google Gemini 2.0 + Runway Gen-4*
