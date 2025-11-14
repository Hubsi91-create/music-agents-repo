# Holistic Training Pipeline

**Automatic training system for all Music Video Production Agents (1-11)**

Version: 1.0.0

---

## Overview

The Holistic Training Pipeline provides comprehensive, automated training for all agents in the Music Video Production System using data from Agent 12 (Universal Harvester).

### Key Features

- **6-Phase Training Workflow**
- **Sequential Agent Training** with dependency management
- **Quality Scoring** and data validation
- **Comprehensive Monitoring** and reporting
- **Error Handling** with graceful degradation
- **Automated Scheduling** support

---

## Architecture

```
training/
├── holistic_trainer.py      # Core training orchestrator
├── training_monitor.py       # Metrics tracking & reporting
├── agent_trainer.py          # Individual agent training helper
├── config.json               # Training configuration
└── __init__.py              # Package initialization
```

---

## 6-Phase Training Workflow

### Phase 1: Data Harvesting (30s)
- Harvests data from Agent 12 (Universal Harvester)
- Sources: Trends, Audio, Screenplay, Creator, Distribution, Sound
- Collects 100-500 records per category

### Phase 2: Data Validation (10s)
- Quality filtering (threshold: 6.5/10)
- Deduplication
- Ranking by quality score
- Format validation

### Phase 3: Agent Training (2-3 min)
Sequential training of all agents:
1. Agent 1 (Trend Detective) - 50 top trends
2. Agent 2 (Audio Curator) - 100 top tracks
3. Agent 3 (Video Concept) - Uses Agent 1 output
4. Agent 4 (Screenplay Generator) - 75 top stories
5. Agent 6 (Influencer Matcher) - 50 top creators
6. Agent 7 (Distribution Metadata) - 100 top strategies
7. Agent 8 (Prompt Refiner) - 200 top prompts
8. Agent 9 (Sound Designer) - 75 top techniques
9. Agent 10 (Master Distributor) - 100 top tactics
10. Agent 11 (Meta Trainer) - All outputs

### Phase 4: Production Run (5-10 min) - Optional
- Executes full production pipeline with trained agents
- Agent 1 → Agent 3 → Agent 4 → Agent 2 → Agent 9 →
  Agent 8 → Agent 5a/5b → Agent 6 → Agent 10 → Agent 7

### Phase 5: Monitoring & Logging (1 min)
- Generates daily training report
- Updates metrics database
- Calculates system health
- Tracks improvement trends

### Phase 6: Cleanup & Archiving (30s)
- Archives old logs (30 day retention)
- Cleans temporary files
- Optimizes database
- Schedules next run

---

## Usage

### CLI Commands

#### Run Holistic Training

```bash
# Run training with verbose output
python orchestrator/orchestrator.py train --verbose

# Run training (quiet mode)
python orchestrator/orchestrator.py train
```

#### Get Training Statistics

```bash
python orchestrator/orchestrator.py stats
```

Output:
```
[Training Statistics]
  Overall Quality: 8.2/10
  Trend: UP
  Improvement: +1.5%
  Agents Online: 11
  Agents Needing Attention: 0
  Next Training: 2025-01-15T03:00:00
```

### Python API

```python
from training.holistic_trainer import HolisticTrainer

# Initialize with agents
agents = {
    'agent_1': agent_1_instance,
    'agent_2': agent_2_instance,
    # ... etc
}

trainer = HolisticTrainer(agents)

# Run training
result = trainer.run_holistic_training(verbose=True)

print(f"Status: {result['status']}")
print(f"Duration: {result['total_time_minutes']:.2f} min")
print(f"Agents Trained: {result['agents_trained']}")
print(f"Improvement: {result['system_quality_delta']:+.2f}%")
```

---

## Configuration

Edit [config.json](config.json) to customize training:

```json
{
  "training": {
    "enabled": true,
    "schedule": "0 3 * * *",
    "timeout_per_agent_seconds": 300,
    "timeout_total_seconds": 1800,

    "harvester": {
      "data_quality_threshold": 6.5,
      "min_records_per_type": 20
    },

    "monitoring": {
      "track_metrics": true,
      "generate_reports": true,
      "save_logs": true,
      "log_retention_days": 30
    },

    "production_run": {
      "enabled": false
    }
  }
}
```

---

## Training Metrics

### Agent-Specific Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Quality Score | Overall quality rating (0-10) | 8.0+ |
| Processing Time | Training duration in ms | <2000ms |
| Improvement | Delta vs previous run (%) | +0.5%+ |
| Data Count | Training records used | 20-200 |

### System-Wide Metrics

- **Overall System Quality**: Weighted average of all agents
- **Success Rate**: % of successful training runs
- **Training Speed**: Average ms per agent
- **Trend**: UP / DOWN / STABLE

---

## Monitoring & Reports

### Daily Reports

Generated automatically after each training run:
- Location: `orchestrator/logs/daily_report_YYYY-MM-DD.txt`
- Format: Text table with ASCII box drawing
- Includes: All agent metrics, recommendations, trends

Example: [Sample Daily Report](../logs/sample_daily_report.txt)

### Metrics Database

- Location: `orchestrator/logs/training_metrics.json`
- Contains: Historical data for all metrics
- Retention: Unlimited (manual cleanup)
- Format: JSON

### System Health

```python
from training.training_monitor import TrainingMonitor

monitor = TrainingMonitor()
health = monitor.get_system_health()

# Returns:
{
  'overall_quality': 8.2,
  'trend': 'up',
  'improvement_percent': 1.5,
  'agents_online': 11,
  'agents_needing_attention': [],
  'next_training': '2025-01-15T03:00:00',
  'estimated_video_quality': 9.2
}
```

---

## Scheduling

### Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add daily training at 3 AM
0 3 * * * cd /path/to/repo && python orchestrator/orchestrator.py train

# Add weekly stats email at 9 AM Monday
0 9 * * 1 cd /path/to/repo && python orchestrator/orchestrator.py stats | mail -s "Training Stats" you@email.com
```

### Task Scheduler (Windows)

```powershell
# Create scheduled task for daily training
schtasks /create /tn "HolisticTraining" /tr "python C:\path\to\orchestrator\orchestrator.py train" /sc daily /st 03:00
```

### Python Scheduler

```python
import schedule
import time

def run_training():
    os.system('python orchestrator/orchestrator.py train')

# Schedule daily at 3 AM
schedule.every().day.at("03:00").do(run_training)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Error Handling

### Timeout Handling
- Per-agent timeout: 300 seconds (configurable)
- Total pipeline timeout: 1800 seconds
- Graceful degradation: Continues with next agent on failure

### Error Recovery
- Failed agents are logged but don't halt pipeline
- Automatic retry on transient errors
- Fallback to cached data if harvesting fails

### Logging
- All errors logged to `training_monitor.log`
- Detailed stack traces for debugging
- Error summary in daily report

---

## Integration

### With Agent 12 (Universal Harvester)

```python
# Automatic integration
# HolisticTrainer automatically imports and uses Agent 12

from agent_12_universal_harvester import UniversalHarvester

harvester = UniversalHarvester()
trend_data = harvester.harvest('trend')
```

### With Individual Agents

Each agent must implement a `train()` method:

```python
class MyAgent:
    def train(self, data):
        """
        Train agent with provided data.

        Args:
            data: List of training data items

        Returns:
            Training results dict
        """
        # Training logic here
        return {
            'status': 'success',
            'quality_improvement': 0.5,
            'model_updated': True
        }
```

---

## Performance

### Expected Timings

| Phase | Duration | Notes |
|-------|----------|-------|
| Harvesting | 30s | Depends on API response times |
| Validation | 10s | Fast local processing |
| Training | 2-3 min | Sequential agent training |
| Production | 5-10 min | Optional, disabled by default |
| Monitoring | 1 min | Report generation |
| Cleanup | 30s | File operations |
| **Total** | **4-5 min** | Full pipeline |

### Optimization

- Enable `parallel_training` for faster execution (experimental)
- Reduce `training_data_limits` for quicker runs
- Disable `production_run` to save time
- Use caching: `cache_training_data: true`

---

## Troubleshooting

### Problem: Training times out

**Solution:**
```bash
# Increase timeout in config.json
"timeout_per_agent_seconds": 600  # 10 minutes
```

### Problem: No data harvested

**Solution:**
```bash
# Check Agent 12 is running
cd agent-12-universal-harvester
python main.py status

# Force fresh harvest
python orchestrator/orchestrator.py train --force
```

### Problem: Agent training fails

**Solution:**
```bash
# Check agent has train() method
# Verify data format matches agent expectations
# Check logs for specific error:
cat orchestrator/logs/training_monitor.log
```

---

## Development

### Adding New Metrics

Edit `training_monitor.py`:

```python
def _initialize_metrics(self):
    return {
        # ... existing metrics
        'my_custom_metric': [],
    }
```

### Custom Training Logic

Extend `HolisticTrainer`:

```python
from training.holistic_trainer import HolisticTrainer

class CustomTrainer(HolisticTrainer):
    def _phase3_agent_training(self, verbose=True):
        # Custom training logic
        pass
```

---

## Testing

### Unit Tests

```bash
# Run tests
pytest orchestrator/training/

# Test individual components
python orchestrator/training/agent_trainer.py
python orchestrator/training/training_monitor.py
```

### Integration Test

```bash
# Full pipeline test
python orchestrator/orchestrator.py train --verbose

# Verify output
cat orchestrator/logs/daily_report_$(date +%Y-%m-%d).txt
cat orchestrator/holistic_training_result.json
```

---

## Best Practices

1. **Schedule Regularly**: Daily at 3 AM for fresh data
2. **Monitor Metrics**: Check daily reports for degradation
3. **Adjust Thresholds**: Increase quality threshold as system improves
4. **Review Recommendations**: Act on training suggestions
5. **Backup Metrics**: Keep `training_metrics.json` backed up

---

## Future Enhancements

- [ ] Parallel agent training
- [ ] A/B testing of training strategies
- [ ] Automatic hyperparameter tuning
- [ ] Real-time dashboard
- [ ] Email/Slack notifications
- [ ] Multi-region harvesting
- [ ] GPU acceleration support

---

## License

Proprietary - Music Video Production System

---

## Support

For issues or questions:
1. Check this README
2. Review logs in `orchestrator/logs/`
3. Run `python orchestrator/orchestrator.py stats`
4. Contact system administrator

---

**Built with Claude Code - Holistic Training Pipeline powers continuous improvement for all 11 Music Video Production Agents.**
