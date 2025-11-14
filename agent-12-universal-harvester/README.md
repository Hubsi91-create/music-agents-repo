# Agent 12 - Universal Harvester

**Central Data Harvesting System for Music Video Production Agents**

Version: 1.0.0
Author: Universal Harvester System

---

## Overview

The Universal Harvester is a centralized data collection and analysis system that provides harvested data to Agents 1-11 for continuous self-improvement. It scrapes, analyzes, and stores data from multiple platforms to enhance the capabilities of the entire Music Video Production System.

### Key Features

- **6 Specialized Harvesters** for different data types
- **Google Gemini AI Integration** for intelligent analysis
- **Centralized SQLite Database** for data persistence
- **REST API Server** for orchestrator integration
- **CLI Interface** for manual operations
- **Quality Scoring System** to filter high-value data
- **Automatic Caching** to reduce API calls

---

## Architecture

```
agent-12-universal-harvester/
├── modules/                      # Harvester implementations
│   ├── base_harvester.py        # Abstract base class
│   ├── trend_harvester.py       # Agent 1 - Trends
│   ├── audio_harvester.py       # Agent 2 - Audio
│   ├── screenplay_harvester.py  # Agent 4 - Stories
│   ├── creator_harvester.py     # Agent 6 - Creators
│   ├── distribution_harvester.py # Agent 10 - Distribution
│   └── sound_harvester.py       # Agent 9 - Sound Design
├── analyzers/
│   └── gemini_analyzer.py       # Shared Gemini AI analysis
├── database/
│   └── harvested_data.py        # SQLite database layer
├── main.py                       # CLI + Server entry point
├── config.json                   # Configuration
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

---

## Harvesters

### 1. Trend Harvester (Agent 1 - TrendDetective)

**Purpose:** Identify viral trends and emerging patterns

**Data Sources:**
- YouTube Trending API
- Reddit (r/TrendingMusic, r/Music, r/PopMusic)
- TikTok Trending Sounds
- Twitter/X Trends

**Quality Scoring:**
- 50% Engagement (Likes, Views, Comments)
- 30% Recency (Last 7 days = full score)
- 20% Community Validation

**Output:**
- Top 10 trends with viral potential scores
- Emerging trends in early growth phase
- Genre dominance patterns

---

### 2. Audio Harvester (Agent 2 - AudioCurator)

**Purpose:** Find high-quality audio tracks for video production

**Data Sources:**
- Spotify Charts API
- YouTube Music Trending
- Reddit Music Communities
- SoundCloud Trending

**Quality Scoring:**
- 40% Stream Count / Popularity
- 30% Technical Quality (BPM, Energy)
- 20% Community Rating
- 10% Recency

**Output:**
- Best tracks for video with scores
- BPM/Mood recommendations by genre
- Production quality trends

---

### 3. Screenplay Harvester (Agent 4 - ScreenplayGenerator)

**Purpose:** Discover story patterns and narrative structures

**Data Sources:**
- Reddit (r/WritingPrompts, r/Screenwriting)
- GitHub Screenplay Collections
- Story Platforms
- YouTube Script Analysis

**Quality Scoring:**
- 40% Story Quality (upvotes, stars)
- 30% Audience Engagement
- 20% Originality
- 10% Recency

**Output:**
- Trending story structures
- Character archetypes
- Emotional arc templates

---

### 4. Creator Harvester (Agent 6 - InfluencerMatcher)

**Purpose:** Identify creators for collaboration

**Data Sources:**
- YouTube Creator Metadata
- TikTok Creator Data
- Instagram Creator Info
- Reddit Creator Profiles

**Quality Scoring:**
- 40% Follower Count
- 30% Engagement Rate
- 20% Audience Alignment
- 10% Growth Trajectory

**Output:**
- Best creator matches with fit scores
- Audience overlap analysis
- Collaboration potential scores

---

### 5. Distribution Harvester (Agent 10 - MasterDistributor)

**Purpose:** Optimize distribution strategies

**Data Sources:**
- YouTube Analytics Trends
- TikTok Algorithm Insights
- Twitter/X Viral Analysis
- Reddit Marketing Communities

**Quality Scoring:**
- 40% Engagement Metrics
- 30% Shareability Score
- 20% Community Feedback
- 10% Time-to-Viral

**Output:**
- Optimal title patterns for CTR
- Best hashtag combinations
- Optimal posting times
- Viral hook structures

---

### 6. Sound Harvester (Agent 9 - SoundDesigner)

**Purpose:** Collect sound design techniques

**Data Sources:**
- Reddit (r/MusicProduction, r/AudioEngineering)
- Beatport Charts
- Sound Design Resources
- YouTube Production Tutorials

**Quality Scoring:**
- 40% Production Quality
- 30% Community Rating
- 20% Innovation
- 10% Recency

**Output:**
- Trending production techniques
- Effect chain patterns
- VST/Tool recommendations

---

## Installation

### 1. Clone Repository

```bash
cd agent-12-universal-harvester
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
nano .env
```

Required API Keys:
- `GOOGLE_AI_API_KEY` - Google Gemini AI (REQUIRED)
- `YOUTUBE_API_KEY` - YouTube Data API v3
- `REDDIT_CLIENT_ID` & `REDDIT_CLIENT_SECRET` - Reddit API
- `SPOTIFY_CLIENT_ID` & `SPOTIFY_CLIENT_SECRET` - Spotify API
- `TWITTER_BEARER_TOKEN` - Twitter API (optional)

### 4. Configure Harvesters

Edit `config.json` to enable/disable harvesters and adjust settings.

---

## Usage

### CLI Interface

#### Harvest Data

```bash
# Harvest from all enabled harvesters
python main.py harvest --type=all

# Harvest specific type
python main.py harvest --type=trend
python main.py harvest --type=audio
python main.py harvest --type=screenplay

# Force fresh harvest (bypass cache)
python main.py harvest --type=trend --force
```

#### Check Status

```bash
# Show status and statistics
python main.py status
```

#### Analyze Data

```bash
# Analyze harvested data
python main.py analyze --type=trend
python main.py analyze --type=audio
```

#### Cleanup Old Data

```bash
# Delete data older than 30 days
python main.py cleanup --days=30
```

### HTTP Server

#### Start Server

```bash
# Start on default port 5003
python main.py serve

# Start on custom port
python main.py serve --port=8000
```

#### API Endpoints

**Health Check**
```bash
GET /health
```

**Harvest Data**
```bash
POST /harvest
Content-Type: application/json

{
  "type": "trend",  # or "all"
  "force": false
}
```

**Get Harvested Data**
```bash
GET /data/{source_type}?limit=100&max_age_hours=24&min_score=7.0
```

**Get Statistics**
```bash
GET /stats
```

**Cleanup Data**
```bash
POST /cleanup
Content-Type: application/json

{
  "days": 30
}
```

---

## Integration with Orchestrator

The Universal Harvester integrates with the main orchestrator to provide data to agents.

### Example Integration

```python
from agent_12_universal_harvester import UniversalHarvester

class MusicAgentOrchestrator:
    def __init__(self):
        self.harvester = UniversalHarvester()

    def enhanced_pipeline(self):
        # Harvest data
        trend_data = self.harvester.harvest('trend')
        audio_data = self.harvester.harvest('audio')
        screenplay_data = self.harvester.harvest('screenplay')
        creator_data = self.harvester.harvest('creator')
        distribution_data = self.harvester.harvest('distribution')
        sound_data = self.harvester.harvest('sound')

        # Train agents with harvested data
        self.agents['trend_detective'].train(trend_data)
        self.agents['audio_curator'].train(audio_data)
        self.agents['screenplay_generator'].train(screenplay_data)
        self.agents['influencer_matcher'].train(creator_data)
        self.agents['distributor'].train(distribution_data)
        self.agents['sound_designer'].train(sound_data)

        return self.run_full_pipeline()
```

### HTTP Integration

```python
import requests

# Harvest trends
response = requests.post('http://localhost:5003/harvest', json={
    'type': 'trend',
    'force': False
})
result = response.json()

# Get harvested data
response = requests.get('http://localhost:5003/data/trend', params={
    'limit': 100,
    'min_score': 7.0
})
data = response.json()
```

---

## Database Schema

### Table: harvested_data

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| source_type | TEXT | Harvester name |
| harvester_name | TEXT | Full harvester name |
| raw_data | TEXT | Raw JSON data |
| analyzed_data | TEXT | Gemini analysis JSON |
| quality_score | REAL | Quality score 0-10 |
| source_url | TEXT | Original source URL |
| harvested_at | TIMESTAMP | Harvest timestamp |
| expires_at | TIMESTAMP | Expiry timestamp |

### Table: harvest_log

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| harvester_name | TEXT | Harvester name |
| status | TEXT | success/error/warning |
| record_count | INTEGER | Records harvested |
| execution_time | INTEGER | Time in milliseconds |
| error_message | TEXT | Error if failed |
| timestamp | TIMESTAMP | Log timestamp |

---

## Configuration

### config.json Structure

```json
{
  "harvesters": {
    "trend": {
      "enabled": true,
      "schedule": "daily",
      "sources": ["youtube", "reddit", "tiktok", "twitter"],
      "quality_threshold": 7.0
    },
    ...
  },
  "gemini": {
    "model": "gemini-2.0-flash-exp",
    "temperature": 0.7,
    "max_output_tokens": 2000
  },
  "database": {
    "path": "./database/harvested_data.db",
    "cleanup_after_days": 30
  }
}
```

---

## Development

### Adding a New Harvester

1. Create new file in `modules/` inheriting from `BaseHarvester`
2. Implement abstract methods:
   - `get_data_sources()`
   - `extract_raw_data()`
   - `parse_data()`
   - `score_data_quality()`
   - `get_analysis_prompt()`
3. Add to `config.json`
4. Import in `main.py`

### Example Template

```python
from .base_harvester import BaseHarvester

class MyHarvester(BaseHarvester):
    def __init__(self, config):
        super().__init__("my_harvester", config)

    def get_data_sources(self):
        return [{'name': 'Source', 'url': '...', 'type': 'api'}]

    def extract_raw_data(self, source):
        # Implement data extraction
        pass

    def parse_data(self, raw_data):
        # Implement data parsing
        pass

    def score_data_quality(self, data_item):
        # Implement quality scoring
        return 8.0

    def get_analysis_prompt(self, data):
        return "Analyze this data..."
```

---

## Security & Best Practices

### API Keys
- NEVER commit `.env` file to Git
- Use environment variables for all secrets
- Rotate API keys regularly

### Rate Limiting
- Respect API rate limits (configured in `config.json`)
- Use caching to minimize API calls
- Implement exponential backoff for failed requests

### Data Privacy
- Only harvest PUBLIC data
- Respect Terms of Service for each platform
- Do not store personally identifiable information (PII)

### Database
- Regular backups of `harvested_data.db`
- Use `cleanup` command to manage database size
- Run `VACUUM` periodically for optimization

---

## Troubleshooting

### No Data Harvested

1. Check API keys in `.env`
2. Verify sources are enabled in `config.json`
3. Check rate limits haven't been exceeded
4. Review logs for errors

### Gemini Analysis Fails

1. Verify `GOOGLE_AI_API_KEY` is valid
2. Check API quota hasn't been exceeded
3. Data may be too large (reduced automatically)

### Database Errors

1. Check database file permissions
2. Run cleanup to remove corrupted data
3. Delete database file to recreate (loses data)

---

## Performance Optimization

### Caching Strategy
- Default cache: 24 hours
- Use `force=true` to bypass cache
- Adjust `max_age_hours` in config

### Parallel Harvesting
- Run multiple harvesters in parallel (planned)
- Use async/await for API calls (planned)

### Database Optimization
- Run `cleanup` regularly
- Use indexes for frequent queries
- VACUUM database monthly

---

## Future Enhancements

- [ ] Async harvesting for parallel execution
- [ ] Real-time streaming data support
- [ ] Machine learning for quality prediction
- [ ] Advanced NLP for content analysis
- [ ] WebSocket support for live updates
- [ ] Docker containerization
- [ ] Kubernetes deployment configs
- [ ] GraphQL API support

---

## License

Proprietary - Music Video Production System

---

## Support

For issues or questions:
1. Check this README
2. Review logs in `logs/`
3. Check database with `python main.py status`
4. Contact system administrator

---

## Version History

**1.0.0** (2025-01-14)
- Initial release
- 6 specialized harvesters
- Gemini AI integration
- SQLite database
- CLI + HTTP server
- Orchestrator integration ready

---

**Built with Claude Code - The Universal Harvester powers continuous improvement for all Music Video Production Agents.**