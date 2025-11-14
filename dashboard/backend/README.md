# Production Dashboard Backend API v2.0

Complete REST API backend for Music Agents Production Dashboard with 25+ endpoints, real-time data from orchestrator, SQLite database integration, and comprehensive error handling.

## Features

- **25+ API Endpoints** - Complete REST API for dashboard functionality
- **Real-time Data** - Live data from orchestrator training pipeline
- **SQLite Database** - Persistent storage for metrics, events, and training sessions
- **System Health Monitoring** - CPU, memory, disk, uptime tracking with psutil
- **Comprehensive Logging** - Detailed logging with file and console output
- **Error Handling** - Graceful degradation and proper error responses
- **CORS Support** - Cross-origin requests enabled for frontend integration

## Architecture

```
dashboard/backend/
├── app.py                    # Main Flask application (400+ lines)
├── database.py               # SQLite database helpers
├── data_loader.py            # Load data from orchestrator
├── requirements.txt          # Python dependencies
├── .env.example             # Configuration template
├── templates/
│   └── index.html           # Dashboard frontend
└── static/
    ├── css/
    └── js/
```

## Quick Start

### 1. Install Dependencies

```bash
cd dashboard/backend
pip install -r requirements.txt
```

### 2. Configuration (Optional)

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run Server

```bash
python app.py
```

Server starts on: **http://localhost:5000**

## API Endpoints

### Dashboard Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard/overview` | GET | Complete dashboard overview with system state |
| `/api/dashboard/quick-stats` | GET | Quick statistics for dashboard header |

**Example Response - /api/dashboard/overview:**
```json
{
  "current_phase": "monitoring",
  "overall_quality": 8.2,
  "last_training": "2025-11-14T03:00:00Z",
  "next_training": "2025-11-15T03:00:00Z",
  "agents_trained": 11,
  "training_speed_ms": 142000,
  "improvements": {
    "agent_1": 2.3,
    "agent_2": 3.1,
    "agent_8": 5.2
  },
  "quality_trend": "improving"
}
```

### Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/agents/status` | GET | Status for all 12 agents |
| `/api/agents/<agent_id>` | GET | Detailed info for specific agent |
| `/api/agents/health` | GET | Aggregate health status for all agents |

**Example Response - /api/agents/status:**
```json
[
  {
    "id": "agent_1",
    "name": "Trend Detective",
    "status": "online",
    "quality_score": 8.0,
    "last_updated": "2025-11-14T09:15:00Z",
    "processing_time_ms": 1250,
    "improvement": 2.3,
    "errors": 0
  },
  ...
]
```

### Training Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/training/status` | GET | Current training phase and progress |
| `/api/training/history?days=7` | GET | Training history for last N days |
| `/api/training/start` | POST | Start training immediately |
| `/api/training/stop` | POST | Stop running training |
| `/api/training/schedule` | GET | Get training schedule info |

**Example Response - /api/training/status:**
```json
{
  "is_running": true,
  "current_phase": "agent_training",
  "progress_percent": 65,
  "current_agent": "agent_8",
  "estimated_time_remaining_sec": 145,
  "phase_durations": {
    "harvesting": 28,
    "validation": 9,
    "agent_training": 142,
    "production": 0,
    "monitoring": 60
  }
}
```

### Metrics Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/metrics/quality` | GET | Quality scores over time |
| `/api/metrics/history/<metric_name>` | GET | Detailed metric history |
| `/api/metrics/comparison` | GET | Agent vs agent comparison |
| `/api/metrics/trends` | GET | System trends (7-day moving average) |

**Example Response - /api/metrics/quality:**
```json
{
  "timestamps": ["2025-11-07", "2025-11-08", ..., "2025-11-14"],
  "system": [7.2, 7.4, 7.6, ..., 8.2],
  "agent_8": [7.8, 7.9, 8.2, ..., 9.3],
  "agent_5a": [8.5, 8.5, 8.7, ..., 9.0]
}
```

### System Health Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/system/health` | GET | Real-time system metrics (CPU, memory, disk) |
| `/api/system/logs/recent?limit=50` | GET | Recent log events |
| `/api/system/errors` | GET | Recent errors and warnings |
| `/api/system/alerts` | GET | Active alerts/notifications |

**Example Response - /api/system/health:**
```json
{
  "cpu_percent": 45.2,
  "memory_percent": 62.1,
  "disk_percent": 38.5,
  "uptime_seconds": 259200,
  "uptime_hours": 72.0,
  "active_connections": 3,
  "timestamp": "2025-11-14T09:15:00Z"
}
```

### Storyboard Endpoints (Foundation)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/storyboard/projects` | GET | List of storyboard projects |
| `/api/storyboard/project/<project_id>` | GET | Full project with scenes |
| `/api/storyboard/project/create` | POST | Create new project |

### Logs Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/logs/training` | GET | All training logs |
| `/api/logs/export?format=json&days=7` | GET | Export logs in format |

### Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | API status and version |
| `/api/endpoints` | GET | List all available endpoints |

## Database Schema

### Tables

**metrics**
- `id` - Primary key
- `timestamp` - ISO timestamp
- `agent_id` - Agent identifier (nullable)
- `metric_type` - Type of metric (quality, speed, errors)
- `value` - Metric value
- `notes` - Optional notes

**events**
- `id` - Primary key
- `timestamp` - ISO timestamp
- `event_type` - Type of event (training, error, alert)
- `agent_id` - Related agent (nullable)
- `message` - Event message
- `severity` - Severity level (info, warning, error, critical)
- `metadata` - JSON metadata

**training_sessions**
- `id` - Primary key
- `start_time` - Session start timestamp
- `end_time` - Session end timestamp (nullable)
- `agents_trained` - Number of agents trained
- `overall_improvement` - Overall improvement percentage
- `status` - Session status (running, completed, failed, stopped)
- `phase` - Current phase
- `error_message` - Error message if failed

**system_health**
- `id` - Primary key
- `timestamp` - ISO timestamp
- `cpu_percent` - CPU usage percentage
- `memory_percent` - Memory usage percentage
- `disk_percent` - Disk usage percentage
- `uptime_seconds` - System uptime in seconds
- `active_connections` - Active network connections

**agent_metrics**
- `id` - Primary key
- `timestamp` - ISO timestamp
- `agent_id` - Agent identifier
- `quality_score` - Quality score (0-10)
- `processing_time_ms` - Processing time in milliseconds
- `error_count` - Number of errors
- `status` - Agent status (online, offline)
- `improvement` - Improvement vs previous
- `metadata` - JSON metadata

## Data Sources

### 1. Training Configuration
**Source:** `orchestrator/training/config.json`
- Agent configurations
- Training schedule
- Quality targets
- Performance settings

### 2. Training Results
**Source:** `orchestrator/holistic_training_result.json`
- Latest training session results
- Agent improvements
- System quality metrics

### 3. Daily Reports
**Source:** `orchestrator/logs/daily_report_*.txt`
- Per-agent quality scores
- Processing times
- Daily improvements
- System trends

### 4. System Health
**Source:** `psutil` library (real-time)
- CPU usage
- Memory usage
- Disk usage
- Network connections
- System uptime

## Error Handling

All endpoints implement comprehensive error handling:

```python
try:
    # Endpoint logic
    return jsonify(result)
except Exception as e:
    logger.error(f"[API] Endpoint failed: {str(e)}")
    return jsonify({'error': str(e)}), 500
```

**Error Response Format:**
```json
{
  "error": "Error message",
  "status": 500
}
```

## Logging

Logging configuration in `app.py`:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard.log'),
        logging.StreamHandler()
    ]
)
```

**Log Levels:**
- `DEBUG` - Detailed diagnostic information
- `INFO` - General informational messages
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical errors

## Testing API Endpoints

### Using curl

```bash
# Dashboard overview
curl http://localhost:5000/api/dashboard/overview

# Agent status
curl http://localhost:5000/api/agents/status

# Specific agent
curl http://localhost:5000/api/agents/agent_8

# System health
curl http://localhost:5000/api/system/health

# Training status
curl http://localhost:5000/api/training/status

# Training history
curl http://localhost:5000/api/training/history?days=7

# Quality metrics
curl http://localhost:5000/api/metrics/quality

# Start training
curl -X POST http://localhost:5000/api/training/start \
  -H "Content-Type: application/json" \
  -d '{"force": true}'

# Recent logs
curl http://localhost:5000/api/system/logs/recent?limit=50
```

### Using Python

```python
import requests

# Get dashboard overview
response = requests.get('http://localhost:5000/api/dashboard/overview')
data = response.json()
print(f"Quality: {data['overall_quality']}")

# Get all agents
response = requests.get('http://localhost:5000/api/agents/status')
agents = response.json()
for agent in agents:
    print(f"{agent['name']}: {agent['quality_score']}")

# Start training
response = requests.post(
    'http://localhost:5000/api/training/start',
    json={'force': True}
)
print(response.json())
```

## Performance

- **Response Time:** < 100ms for most endpoints
- **Database Queries:** Indexed for performance
- **Data Caching:** Data loader uses singleton pattern
- **Error Recovery:** Graceful degradation when orchestrator data unavailable

## Configuration

Environment variables (`.env`):

```bash
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=5000
DATABASE_PATH=./dashboard.db
ORCHESTRATOR_PATH=../../orchestrator
LOG_LEVEL=INFO
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using systemd

Create `/etc/systemd/system/dashboard.service`:

```ini
[Unit]
Description=Music Agents Dashboard Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/dashboard/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl start dashboard
sudo systemctl enable dashboard
```

## Frontend Integration

This backend is designed to work with React/Next.js frontends:

```javascript
// Example React integration
const fetchDashboard = async () => {
  const response = await fetch('http://localhost:5000/api/dashboard/overview');
  const data = await response.json();
  console.log(data);
};

const fetchAgents = async () => {
  const response = await fetch('http://localhost:5000/api/agents/status');
  const agents = await response.json();
  return agents;
};

const startTraining = async () => {
  const response = await fetch('http://localhost:5000/api/training/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ force: true })
  });
  return await response.json();
};
```

## Troubleshooting

### Database Issues

```bash
# Check database file
ls -la dashboard.db

# Reset database
rm dashboard.db
python app.py  # Will recreate on startup
```

### Missing Orchestrator Data

The API gracefully handles missing orchestrator data:
- Returns empty/default values
- Logs warnings
- Continues to function

### High CPU/Memory Usage

Check system health:
```bash
curl http://localhost:5000/api/system/health
```

Adjust thresholds in `.env`

## Development

### Adding New Endpoints

1. Add endpoint function in `app.py`
2. Add proper error handling
3. Update this README
4. Test with curl

Example:
```python
@app.route('/api/my-endpoint')
def my_endpoint():
    """GET /api/my-endpoint - Description"""
    try:
        # Your logic here
        return jsonify(result)
    except Exception as e:
        logger.error(f"[API] My endpoint failed: {str(e)}")
        return jsonify({'error': str(e)}), 500
```

### Database Migrations

To add new tables/columns:

1. Update schema in `database.py`
2. Delete `dashboard.db`
3. Restart server (auto-recreates)

## Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Authentication & authorization
- [ ] Rate limiting
- [ ] Caching layer (Redis)
- [ ] Async endpoints for long-running operations
- [ ] GraphQL API
- [ ] API versioning
- [ ] Swagger/OpenAPI documentation
- [ ] Docker containerization
- [ ] Horizontal scaling support

## License

Part of Music Agents Production System

## Support

For issues or questions:
1. Check logs: `dashboard.log`
2. Test endpoints with curl
3. Check orchestrator data availability
4. Review database schema

---

**Built with Flask 3.0 | Python 3.8+ | SQLite**
