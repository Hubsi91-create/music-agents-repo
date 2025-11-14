# Training Logs Directory

This directory contains logs from holistic training runs.

## Files

- `training_metrics.json` - Historical training metrics database
- `daily_report_YYYY-MM-DD.txt` - Daily training reports
- `holistic_training_result.json` - Latest training run results

## Log Retention

- Logs are retained for 30 days by default
- Configure retention in [training/config.json](../training/config.json)

## Viewing Logs

```bash
# View latest daily report
cat orchestrator/logs/daily_report_$(date +%Y-%m-%d).txt

# View training metrics
cat orchestrator/logs/training_metrics.json | jq '.system_overall_quality[-5:]'
```
