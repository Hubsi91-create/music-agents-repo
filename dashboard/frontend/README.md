# 🎵 Music Agents Dashboard - Production Frontend

Professional React dashboard for monitoring the Music Agents AI system with real-time tracking, quality metrics, and storyboard visualization.

## ✨ Features

- **🎨 Galaxy/Neon Theme** - Stunning visual design with cyan (#00f0ff) and red (#ff1744) neon effects
- **📊 Real-time Dashboard** - Live monitoring of 12 agents with auto-refresh
- **🎬 Storyboard Visualizer** - Timeline-based scene management and preview
- **📈 Quality Charts** - 7-day metrics history with interactive graphs
- **🖥️ System Health** - CPU, Memory, and Disk usage gauges
- **⚡ Training Monitor** - Live training progress with phase tracking
- **📝 Event Logs** - Real-time system events and notifications
- **🔄 Auto-refresh** - Configurable polling intervals
- **🎯 TypeScript** - Full type safety and IntelliSense support

## 🚀 Tech Stack

- **React 18** - Modern hooks and functional components
- **TypeScript 5** - Strict type checking
- **Vite** - Lightning-fast development and build
- **TailwindCSS 3** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Recharts** - Interactive charts and graphs
- **Axios** - API client with interceptors
- **Lucide React** - Beautiful icons

## 📁 Project Structure

```
dashboard/frontend/
├── src/
│   ├── components/
│   │   ├── layout/          # Header, Sidebar, RightPanel, MainContent
│   │   ├── dashboard/       # Dashboard, AgentStatus, TrainingMonitor, etc.
│   │   ├── storyboard/      # Timeline, SceneCard, MusicPreview
│   │   ├── ui/              # NeonButton, NeonCard, ProgressRing, etc.
│   │   └── modals/          # Modal components
│   │
│   ├── hooks/               # Custom React hooks
│   │   ├── useDashboard.ts
│   │   ├── useAgents.ts
│   │   ├── useTraining.ts
│   │   ├── useMetrics.ts
│   │   └── useLocalStorage.ts
│   │
│   ├── lib/
│   │   ├── api/             # API client and endpoints
│   │   ├── constants/       # Theme colors and constants
│   │   └── types/           # TypeScript interfaces
│   │
│   ├── styles/              # Global styles and CSS modules
│   │   ├── globals.css
│   │   ├── neon-effects.css
│   │   ├── layout.module.css
│   │   └── components.module.css
│   │
│   ├── pages/               # Page components
│   │   ├── DashboardPage.tsx
│   │   ├── StoryboardPage.tsx
│   │   └── SettingsPage.tsx
│   │
│   ├── context/             # React Context API
│   │   └── AppContext.tsx
│   │
│   ├── App.tsx              # Main application component
│   └── main.tsx             # React entry point
│
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── vite.config.ts           # Vite configuration
└── .env                     # Environment variables
```

## 🛠️ Setup & Installation

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on `http://localhost:5000` (or configure in `.env`)

### Installation

```bash
# Navigate to frontend directory
cd dashboard/frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

The dashboard will be available at `http://localhost:5173`

## 📝 Available Scripts

```bash
# Development
npm run dev          # Start Vite dev server with hot reload

# Production
npm run build        # Build for production (TypeScript + Vite)
npm run preview      # Preview production build locally

# Code Quality
npm run lint         # Run ESLint for code quality checks
```

## 🔌 API Integration

The dashboard connects to **26 API endpoints**:

### Dashboard Endpoints
- `GET /api/dashboard/overview` - System overview and stats
- `GET /api/agents/status` - All agents status
- `GET /api/agents/:id` - Specific agent details
- `GET /api/training/status` - Training progress
- `POST /api/training/start` - Start training
- `POST /api/training/stop` - Stop training
- `GET /api/system/health` - CPU/Memory/Disk metrics
- `GET /api/metrics/history` - Quality metrics (7 days)
- `GET /api/logs/recent` - Recent event logs

### Storyboard Endpoints
- `GET /api/storyboard/projects` - All projects
- `GET /api/storyboard/project/:id` - Specific project
- `POST /api/storyboard/project` - Create project
- `PUT /api/storyboard/project/:id` - Update project
- `DELETE /api/storyboard/project/:id` - Delete project
- `POST /api/storyboard/export/:id` - Export to video

### Agent Management
- `POST /api/agents/:id/deploy` - Deploy agent
- `POST /api/agents/:id/stop` - Stop agent
- `POST /api/agents/:id/restart` - Restart agent
- `GET /api/agents/:id/logs` - Agent logs

### Upload & Share
- `POST /api/upload/video` - Upload video file
- `POST /api/share/video` - Share to platforms

### Utilities
- `GET /api/ping` - Check API connectivity
- `GET /api/version` - API version
- `GET /api/settings` - App settings
- `PUT /api/settings` - Update settings

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=30000

# Polling Intervals (milliseconds)
VITE_DASHBOARD_POLL_INTERVAL=5000
VITE_METRICS_POLL_INTERVAL=30000

# Feature Flags
VITE_ENABLE_ANIMATIONS=true
VITE_ENABLE_AUTO_REFRESH=true
```

### Tailwind Theme Colors

```js
colors: {
  'bg-primary': '#0a0e27',       // Deep space blue
  'bg-surface': '#1a1f3a',       // Surface dark
  'text-primary': '#e0e8ff',     // Light text
  'text-secondary': '#a0aff0',   // Muted text
  'neon-cyan': '#00f0ff',        // Primary neon
  'neon-red': '#ff1744',         // Accent neon
  'neon-purple': '#b24bf3',      // Secondary
  'neon-green': '#00e676',       // Success
  'neon-yellow': '#ffeb3b',      // Warning
}
```

## 🎨 Component Showcase

### Layout Components
- **Header** - Sticky navigation with tabs and refresh button
- **Sidebar** - 12 agent icons with tooltips
- **RightPanel** - Metadata, upload progress, settings
- **MainContent** - Scrollable main area

### Dashboard Components
- **AgentStatus** - 3x4 grid of agent cards with metrics
- **TrainingMonitor** - Real-time training progress
- **QualityChart** - 7-day line chart (Recharts)
- **SystemHealth** - CPU/Memory/Disk gauges
- **EventLog** - Scrollable event timeline

### Storyboard Components
- **Timeline** - Interactive scene timeline
- **SceneCard** - Scene preview with actions
- **MusicPreview** - Audio player with waveform

### UI Components
- **NeonButton** - 5 variants (cyan, red, purple, green, yellow)
- **NeonCard** - Glowing card container
- **ProgressRing** - Circular progress indicator
- **GaugeChart** - Semicircle gauge
- **Badge** - Status badges
- **Spinner** - Loading indicators

## 🎯 Key Features Explained

### Auto-refresh System
- Dashboard polls every 5 seconds
- Metrics poll every 30 seconds
- Training status polls every 2 seconds (when active)
- Configurable via environment variables

### Local Storage Persistence
- Selected agent persists across sessions
- Active tab remembered
- User preferences saved

### Responsive Design
- Optimized for 1920px desktops
- Sticky header, sidebar, and right panel
- Smooth scrolling in main content area

### Neon Effects
- Custom glow animations
- Border and shadow effects
- Smooth transitions and hover states

## 🐛 Troubleshooting

### API Connection Issues
```bash
# Check if backend is running
curl http://localhost:5000/api/ping

# Update API URL in .env
VITE_API_BASE_URL=http://your-api-url:port
```

### Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf .vite
```

### TypeScript Errors
```bash
# Rebuild TypeScript definitions
npm run build -- --force
```

## 📊 Performance

- **First Load**: < 3s
- **Component Render**: < 100ms
- **Animations**: 60fps
- **Bundle Size**: ~500KB (gzipped)

## 🔒 Security

- No sensitive data in frontend code
- CORS enabled in backend
- Environment variables for configuration
- XSS protection via React
- Input sanitization

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates optimized production files in `dist/` directory.

### Deploy to Static Hosting

```bash
# Vercel
vercel --prod

# Netlify
netlify deploy --prod --dir=dist

# AWS S3
aws s3 sync dist/ s3://your-bucket-name
```

### Docker Deployment

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 📖 Documentation

- **Component Docs**: See inline JSDoc comments
- **API Docs**: Check `src/lib/api/client.ts`
- **Types**: All types defined in `src/lib/types/index.ts`

## 🤝 Contributing

1. Follow TypeScript strict mode
2. Use Prettier for code formatting
3. Write meaningful commit messages
4. Test all components before committing

## 📄 License

Part of the Music Agents production system.

---

**Built with ❤️ and React**

For questions or issues, check the backend API documentation or contact the development team.
