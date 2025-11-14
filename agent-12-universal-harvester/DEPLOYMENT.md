# Agent 12 - Universal Harvester Deployment Guide

## Quick Start

### 1. Installation

```bash
cd agent-12-universal-harvester
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

Required keys:
```bash
GOOGLE_AI_API_KEY=your_key_here          # REQUIRED
YOUTUBE_API_KEY=your_key_here
REDDIT_CLIENT_ID=your_key_here
REDDIT_CLIENT_SECRET=your_key_here
SPOTIFY_CLIENT_ID=your_key_here
SPOTIFY_CLIENT_SECRET=your_key_here
```

### 3. Test Run

```bash
# Check status
python main.py status

# Harvest trends
python main.py harvest --type=trend
```

---

## CLI Commands

### Harvest Data

```bash
# All harvesters
python main.py harvest --type=all

# Specific harvester
python main.py harvest --type=trend
python main.py harvest --type=audio
python main.py harvest --type=screenplay
python main.py harvest --type=creator
python main.py harvest --type=distribution
python main.py harvest --type=sound

# Force fresh (bypass cache)
python main.py harvest --type=trend --force
```

### Check Status

```bash
python main.py status
```

Example output:
```json
{
  "harvesters": ["trend", "audio", "screenplay", "creator", "distribution", "sound"],
  "database": {
    "path": "./database/harvested_data.db",
    "data_counts": {
      "trend": 150,
      "audio": 200,
      "screenplay": 80
    }
  },
  "statistics": {
    "trend_harvester": {
      "total_runs": 10,
      "successful_runs": 9,
      "success_rate": 90.0,
      "total_records": 150
    }
  }
}
```

### Analyze Data

```bash
python main.py analyze --type=trend
```

### Cleanup

```bash
# Delete data older than 30 days
python main.py cleanup --days=30
```

---

## HTTP Server

### Start Server

```bash
# Default port 5003
python main.py serve

# Custom port
python main.py serve --port=8000
```

### API Endpoints

#### Health Check

```bash
curl http://localhost:5003/health
```

Response:
```json
{
  "status": "healthy",
  "service": "universal-harvester"
}
```

#### Harvest Data

```bash
curl -X POST http://localhost:5003/harvest \
  -H "Content-Type: application/json" \
  -d '{"type": "trend", "force": false}'
```

Response:
```json
{
  "status": "success",
  "source": "fresh",
  "count": 50,
  "timestamp": "2025-01-14T10:30:00",
  "execution_time_ms": 15234
}
```

#### Get Data

```bash
curl "http://localhost:5003/data/trend?limit=10&min_score=7.0"
```

Response:
```json
{
  "source_type": "trend",
  "count": 10,
  "data": [...]
}
```

#### Get Statistics

```bash
curl http://localhost:5003/stats
```

#### Cleanup

```bash
curl -X POST http://localhost:5003/cleanup \
  -H "Content-Type: application/json" \
  -d '{"days": 30}'
```

---

## Integration with Orchestrator

### Method 1: Direct Import

```python
# In orchestrator/main.py
from agent_12_universal_harvester import UniversalHarvester

class MusicAgentOrchestrator:
    def __init__(self):
        self.harvester = UniversalHarvester()

    def run_pipeline(self):
        # Harvest data
        trend_data = self.harvester.harvest('trend')
        audio_data = self.harvester.harvest('audio')

        # Train agents
        self.agents['trend_detective'].train(trend_data)
        self.agents['audio_curator'].train(audio_data)
```

### Method 2: HTTP API

```python
import requests

class MusicAgentOrchestrator:
    def __init__(self):
        self.harvester_url = "http://localhost:5003"

    def get_trend_data(self):
        response = requests.post(
            f"{self.harvester_url}/harvest",
            json={"type": "trend", "force": False}
        )
        return response.json()

    def get_data(self, source_type, min_score=7.0):
        response = requests.get(
            f"{self.harvester_url}/data/{source_type}",
            params={"min_score": min_score}
        )
        return response.json()['data']
```

---

## Production Deployment

### Option 1: Systemd Service

Create `/etc/systemd/system/harvester.service`:

```ini
[Unit]
Description=Universal Harvester Service
After=network.target

[Service]
Type=simple
User=harvester
WorkingDirectory=/opt/agent-12-universal-harvester
Environment="PATH=/opt/agent-12-universal-harvester/venv/bin"
ExecStart=/opt/agent-12-universal-harvester/venv/bin/python main.py serve --port=5003
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable harvester
sudo systemctl start harvester
sudo systemctl status harvester
```

### Option 2: Docker Container

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5003

CMD ["python", "main.py", "serve", "--port=5003"]
```

Build and run:
```bash
docker build -t universal-harvester .
docker run -d -p 5003:5003 \
  --env-file .env \
  -v ./database:/app/database \
  --name harvester \
  universal-harvester
```

### Option 3: Gunicorn + Nginx

Install Gunicorn:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5003 main:app
```

Nginx config:
```nginx
server {
    listen 80;
    server_name harvester.example.com;

    location / {
        proxy_pass http://localhost:5003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Scheduled Harvesting

### Option 1: Cron Jobs

```bash
# Edit crontab
crontab -e

# Add jobs
# Daily at 3 AM: Harvest trends
0 3 * * * cd /path/to/agent-12-universal-harvester && /path/to/python main.py harvest --type=trend

# Daily at 4 AM: Harvest audio
0 4 * * * cd /path/to/agent-12-universal-harvester && /path/to/python main.py harvest --type=audio

# Weekly on Monday: Harvest screenplay
0 5 * * 1 cd /path/to/agent-12-universal-harvester && /path/to/python main.py harvest --type=screenplay

# Monthly cleanup
0 2 1 * * cd /path/to/agent-12-universal-harvester && /path/to/python main.py cleanup --days=30
```

### Option 2: Python Scheduler

Create `scheduler.py`:

```python
import schedule
import time
from main import UniversalHarvester

harvester = UniversalHarvester()

# Schedule jobs
schedule.every().day.at("03:00").do(lambda: harvester.harvest('trend'))
schedule.every().day.at("04:00").do(lambda: harvester.harvest('audio'))
schedule.every().monday.at("05:00").do(lambda: harvester.harvest('screenplay'))

while True:
    schedule.run_pending()
    time.sleep(60)
```

Run:
```bash
python scheduler.py &
```

---

## Monitoring

### Logs

```bash
# View logs
tail -f logs/harvester.log

# Filter errors
grep "ERROR" logs/harvester.log

# Count by harvester
grep "trend_harvester" logs/harvester.log | wc -l
```

### Database Monitoring

```bash
# Database size
ls -lh database/harvested_data.db

# Record counts
python main.py status | jq '.database.data_counts'

# Statistics
python main.py status | jq '.statistics'
```

### Health Checks

```bash
# Check service health
curl http://localhost:5003/health

# Check with timeout
timeout 5 curl http://localhost:5003/health || echo "Service down"
```

---

## Backup & Recovery

### Database Backup

```bash
# Manual backup
cp database/harvested_data.db database/backup_$(date +%Y%m%d).db

# Automated daily backup
echo "0 2 * * * cp /path/to/database/harvested_data.db /path/to/backups/backup_\$(date +\%Y\%m\%d).db" | crontab -
```

### Restore from Backup

```bash
# Stop service
sudo systemctl stop harvester

# Restore database
cp database/backup_20250114.db database/harvested_data.db

# Start service
sudo systemctl start harvester
```

---

## Troubleshooting

### Problem: No data harvested

**Solution:**
```bash
# Check API keys
cat .env | grep API_KEY

# Test individual harvester
python main.py harvest --type=trend --force

# Check logs
tail -f logs/harvester.log
```

### Problem: Gemini analysis fails

**Solution:**
```bash
# Test Gemini connection
python -c "from analyzers.gemini_analyzer import GeminiAnalyzer; g = GeminiAnalyzer(); print(g.test_connection())"

# Check API key
echo $GOOGLE_AI_API_KEY
```

### Problem: Database locked

**Solution:**
```bash
# Stop all processes
sudo systemctl stop harvester

# Remove lock
rm database/harvested_data.db-journal

# Restart
sudo systemctl start harvester
```

### Problem: Rate limit exceeded

**Solution:**
```bash
# Wait for rate limit reset (typically 1 hour)

# Use force=false to use cache
python main.py harvest --type=trend

# Adjust rate limits in config.json
```

---

## Performance Tuning

### Optimize Database

```bash
# Vacuum database
python main.py cleanup --days=30

# Or manually
sqlite3 database/harvested_data.db "VACUUM;"
```

### Adjust Cache TTL

Edit `config.json`:
```json
{
  "cache": {
    "trend": 24,      // hours
    "audio": 12,
    "screenplay": 168  // 7 days
  }
}
```

### Reduce Data Size

```bash
# Lower quality threshold
# Edit config.json
{
  "harvesters": {
    "trend": {
      "quality_threshold": 8.0  // Higher = fewer results
    }
  }
}
```

---

## Security Checklist

- [ ] `.env` file is gitignored
- [ ] API keys are not hardcoded
- [ ] Database file has proper permissions (600)
- [ ] Server runs as non-root user
- [ ] Rate limits are configured
- [ ] HTTPS is enabled (production)
- [ ] Firewall rules are set
- [ ] Regular backups are scheduled
- [ ] Logs are rotated
- [ ] Dependencies are updated

---

## Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Cleanup old data | Weekly | `python main.py cleanup --days=30` |
| Database vacuum | Monthly | `sqlite3 db "VACUUM;"` |
| Update dependencies | Monthly | `pip install -U -r requirements.txt` |
| Backup database | Daily | `cp db backup/` |
| Review logs | Weekly | `tail logs/harvester.log` |
| Check disk space | Weekly | `df -h` |

---

## API Rate Limits

| Platform | Limit | Reset |
|----------|-------|-------|
| YouTube | 10,000/day | Daily |
| Reddit | 60/minute | Per minute |
| Spotify | 10/second | Per second |
| Twitter | 450/15min | 15 minutes |
| Gemini | 60/minute | Per minute |

---

## Support

### Getting Help

1. Check [README.md](README.md) for usage
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for design
3. Check logs: `logs/harvester.log`
4. Run status: `python main.py status`
5. Test connection: `curl http://localhost:5003/health`

### Reporting Issues

Include:
- System info: `python --version`, `pip list`
- Error logs: `tail -50 logs/harvester.log`
- Status output: `python main.py status`
- Steps to reproduce

---

**Deployment Guide Version:** 1.0.0
**Last Updated:** 2025-01-14