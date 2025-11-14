# Production Dashboard API Endpoints

**Version:** 2.0
**Total Endpoints:** 26
**Last Updated:** 2025-11-14

## Quick Reference

| Category | Endpoints | Description |
|----------|-----------|-------------|
| Dashboard | 2 | Overview & Quick Stats |
| Agents | 3 | Agent Status & Health |
| Training | 5 | Training Management |
| Metrics | 4 | Quality & Performance Metrics |
| System | 4 | Health & Logs |
| Storyboard | 3 | Project Management (Foundation) |
| Logs | 2 | Training & Export |
| Utility | 3 | Status & Documentation |

## Complete Endpoint List

### 1. Dashboard Endpoints (2)

```
GET  /api/dashboard/overview       - Complete dashboard overview
GET  /api/dashboard/quick-stats    - Quick statistics
```

### 2. Agent Endpoints (3)

```
GET  /api/agents/status            - All agents status
GET  /api/agents/<agent_id>        - Specific agent details
GET  /api/agents/health            - Aggregate agent health
```

### 3. Training Endpoints (5)

```
GET  /api/training/status          - Current training status
GET  /api/training/history         - Training history (?days=7)
POST /api/training/start           - Start training
POST /api/training/stop            - Stop training
GET  /api/training/schedule        - Training schedule info
```

### 4. Metrics Endpoints (4)

```
GET  /api/metrics/quality          - Quality scores over time
GET  /api/metrics/history/<name>   - Detailed metric history
GET  /api/metrics/comparison       - Agent comparison
GET  /api/metrics/trends           - System trends
```

### 5. System Health Endpoints (4)

```
GET  /api/system/health            - Real-time system metrics
GET  /api/system/logs/recent       - Recent log events (?limit=50)
GET  /api/system/errors            - Recent errors/warnings
GET  /api/system/alerts            - Active alerts
```

### 6. Storyboard Endpoints (3)

```
GET  /api/storyboard/projects      - List projects
GET  /api/storyboard/project/<id>  - Project details
POST /api/storyboard/project/create - Create project
```

### 7. Logs Endpoints (2)

```
GET  /api/logs/training            - Training logs
GET  /api/logs/export              - Export logs (?format=json&days=7)
```

### 8. Utility Endpoints (3)

```
GET  /                             - Dashboard web interface
GET  /api/status                   - API status & version
GET  /api/endpoints                - List all endpoints
```

## Response Examples

### Dashboard Overview
```json
{
  "current_phase": "monitoring",
  "overall_quality": 8.2,
  "last_training": "2025-11-14T03:00:00Z",
  "next_training": "2025-11-15T03:00:00Z",
  "agents_trained": 11,
  "training_speed_ms": 142000,
  "improvements": {...},
  "quality_trend": "improving"
}
```

### Agent Status
```json
[
  {
    "id": "agent_1",
    "name": "Trend Detective",
    "status": "online",
    "quality_score": 8.0,
    "processing_time_ms": 1250,
    "improvement": 2.3,
    "errors": 0
  }
]
```

### System Health
```json
{
  "cpu_percent": 45.2,
  "memory_percent": 62.1,
  "disk_percent": 38.5,
  "uptime_hours": 72.0,
  "active_connections": 3
}
```

## Testing Commands

```bash
# Dashboard
curl http://localhost:5000/api/dashboard/overview
curl http://localhost:5000/api/dashboard/quick-stats

# Agents
curl http://localhost:5000/api/agents/status
curl http://localhost:5000/api/agents/agent_8
curl http://localhost:5000/api/agents/health

# Training
curl http://localhost:5000/api/training/status
curl http://localhost:5000/api/training/history?days=7
curl -X POST http://localhost:5000/api/training/start \
  -H "Content-Type: application/json" \
  -d '{"force": true}'

# Metrics
curl http://localhost:5000/api/metrics/quality
curl http://localhost:5000/api/metrics/comparison
curl http://localhost:5000/api/metrics/trends

# System
curl http://localhost:5000/api/system/health
curl http://localhost:5000/api/system/logs/recent?limit=50
curl http://localhost:5000/api/system/alerts

# Utility
curl http://localhost:5000/api/status
curl http://localhost:5000/api/endpoints
```

## Status Codes

- **200** - Success
- **400** - Bad Request
- **404** - Not Found
- **500** - Internal Server Error
- **501** - Not Implemented

## Rate Limiting

Currently: No rate limiting
Production: Consider 100 requests/minute per IP

## CORS

Enabled for all origins in development
Production: Configure specific origins in `.env`

---

**Total Lines of Code:** 2,480
**Python Code:** 1,897 lines
**Documentation:** 583 lines
