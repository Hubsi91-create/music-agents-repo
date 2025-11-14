# Agent 12 - Universal Harvester Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNIVERSAL HARVESTER                          │
│                     (Agent 12)                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
        ┌───────▼────────┐         ┌───────▼────────┐
        │  CLI Interface │         │  HTTP Server   │
        │   (main.py)    │         │   (Flask)      │
        └───────┬────────┘         └───────┬────────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                    ┌─────────▼─────────┐
                    │ UniversalHarvester │
                    │   (Orchestrator)   │
                    └─────────┬──────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼───────┐   ┌────────▼────────┐   ┌───────▼───────┐
│ 6 Specialized │   │ Gemini Analyzer │   │ SQLite Database│
│  Harvesters   │◄──┤  (Shared AI)    │   │  (Persistence) │
└───────┬───────┘   └─────────────────┘   └───────▲───────┘
        │                                          │
        └──────────────────────────────────────────┘
```

---

## Class Hierarchy

```
BaseHarvester (Abstract)
├── TrendHarvester (Agent 1)
├── AudioHarvester (Agent 2)
├── ScreenplayHarvester (Agent 4)
├── CreatorHarvester (Agent 6)
├── DistributionHarvester (Agent 10)
└── SoundHarvester (Agent 9)
```

### BaseHarvester Template Pattern

All harvesters inherit from `BaseHarvester` and implement:

```python
class BaseHarvester(ABC):
    # Abstract methods (must implement)
    @abstractmethod
    def get_data_sources() -> List[Dict]

    @abstractmethod
    def extract_raw_data(source) -> List[Dict]

    @abstractmethod
    def parse_data(raw_data) -> List[Dict]

    @abstractmethod
    def score_data_quality(data_item) -> float

    @abstractmethod
    def get_analysis_prompt(data) -> str

    # Shared methods (provided by base class)
    def harvest(force=False) -> Dict
    def analyze_with_gemini(data) -> List[Dict]
    def save_to_database(data) -> None
    def get_cached_data(hours=24) -> Optional[List[Dict]]
    def log_harvest_event(...) -> None
```

---

## Data Flow

```
1. Data Sources (External APIs)
        │
        ▼
2. Extract Raw Data
   (extract_raw_data)
        │
        ▼
3. Parse & Structure
   (parse_data)
        │
        ▼
4. Quality Scoring
   (score_data_quality)
        │
        ▼
5. Filter by Threshold
   (quality_threshold)
        │
        ▼
6. Gemini AI Analysis
   (analyze_with_gemini)
        │
        ▼
7. Save to Database
   (save_to_database)
        │
        ▼
8. Return Results
   (JSON response)
```

---

## Database Schema

### Table: harvested_data

```sql
CREATE TABLE harvested_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT NOT NULL,           -- "trend_harvester", "audio_harvester"
    harvester_name TEXT NOT NULL,        -- Full harvester name
    raw_data TEXT NOT NULL,              -- JSON: Original data
    analyzed_data TEXT,                  -- JSON: Gemini analysis
    quality_score REAL,                  -- 0.0 - 10.0
    source_url TEXT,                     -- Original source URL
    harvested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,                -- Auto-cleanup timestamp
    UNIQUE(source_type, source_url, harvested_at)
);

CREATE INDEX idx_source_type ON harvested_data(source_type, harvested_at DESC);
CREATE INDEX idx_quality ON harvested_data(quality_score DESC);
```

### Table: harvest_log

```sql
CREATE TABLE harvest_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    harvester_name TEXT NOT NULL,
    status TEXT NOT NULL,                -- "success", "error", "warning"
    record_count INTEGER DEFAULT 0,
    execution_time INTEGER,              -- Milliseconds
    error_message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_harvester_log ON harvest_log(harvester_name, timestamp DESC);
```

---

## Quality Scoring Algorithms

### Trend Harvester (Agent 1)

```python
total_score = (
    engagement_score * 0.50 +    # 0-5.0 based on views/likes/comments
    recency_score * 0.30 +       # 0-3.0 based on publish date
    validation_score * 0.20      # 0-2.0 based on multi-platform presence
)
```

### Audio Harvester (Agent 2)

```python
total_score = (
    popularity_score * 0.40 +    # 0-4.0 based on streams
    tech_quality_score * 0.30 +  # 0-3.0 based on BPM/energy/danceability
    community_score * 0.20 +     # 0-2.0 based on engagement ratio
    recency_score * 0.10         # 0-1.0 based on release date
)
```

### Screenplay Harvester (Agent 4)

```python
total_score = (
    story_quality_score * 0.40 + # 0-4.0 based on upvotes/stars
    engagement_score * 0.30 +    # 0-3.0 based on comments/shares
    originality_score * 0.20 +   # 0-2.0 based on uniqueness
    recency_score * 0.10         # 0-1.0 based on post date
)
```

### Creator Harvester (Agent 6)

```python
total_score = (
    follower_score * 0.40 +      # 0-4.0 based on follower count
    engagement_score * 0.30 +    # 0-3.0 based on engagement rate
    audience_score * 0.20 +      # 0-2.0 based on audience alignment
    growth_score * 0.10          # 0-1.0 based on growth trajectory
)
```

### Distribution Harvester (Agent 10)

```python
total_score = (
    engagement_score * 0.40 +    # 0-4.0 based on views/shares
    shareability_score * 0.30 +  # 0-3.0 based on viral potential
    ctr_score * 0.20 +           # 0-2.0 based on click-through rate
    timing_score * 0.10          # 0-1.0 based on optimal timing
)
```

### Sound Harvester (Agent 9)

```python
total_score = (
    quality_score * 0.40 +       # 0-4.0 based on production quality
    community_score * 0.30 +     # 0-3.0 based on ratings
    innovation_score * 0.20 +    # 0-2.0 based on uniqueness
    recency_score * 0.10         # 0-1.0 based on post date
)
```

---

## API Integration Points

### External APIs Used

1. **YouTube Data API v3**
   - Trending videos
   - Video metadata
   - Statistics

2. **Reddit API (PRAW)**
   - Subreddit posts
   - Comments
   - Engagement metrics

3. **Spotify Web API**
   - Top charts
   - Audio features
   - Track metadata

4. **Google Gemini AI**
   - Data analysis
   - Insight extraction
   - Pattern recognition

5. **Twitter API v2** (Optional)
   - Trending topics
   - Tweet analytics

---

## Gemini AI Analysis

### System Prompts by Harvester Type

Each harvester has a specialized system prompt:

```python
SYSTEM_PROMPTS = {
    'trend_harvester': """
        Analyze trending data and identify:
        1. TOP 10 trends with viral potential
        2. EMERGING trends gaining momentum
        3. Dominant genres/styles
        4. Viral characteristics
        5. Creator recommendations
    """,

    'audio_harvester': """
        Analyze audio data and identify:
        1. Best tracks for video production
        2. BPM/Mood recommendations by genre
        3. Production quality trends
        4. Audio pairing recommendations
    """,

    # ... etc for each harvester
}
```

### Analysis Pipeline

```
Raw Data → Prepare (limit size) → Generate Prompt → Gemini API → Parse JSON → Return Insights
```

---

## Caching Strategy

### Cache Levels

1. **Database Cache**
   - Default TTL: 24 hours
   - Configurable per harvester
   - Automatic expiry

2. **Memory Cache** (Future)
   - Hot data in memory
   - LRU eviction
   - Shared across requests

### Cache Keys

```python
cache_key = f"{harvester_name}:{timestamp_hour}"
```

---

## Error Handling

### Retry Strategy

```python
@retry(max_attempts=3, backoff=exponential)
def extract_raw_data(source):
    # API call with automatic retry
    pass
```

### Error Logging

All errors logged to:
1. Console (stdout)
2. Database (harvest_log table)
3. Log file (logs/harvester.log)

---

## Performance Considerations

### Optimization Techniques

1. **Lazy Loading**
   - Gemini analyzer loaded on demand
   - Database connection pooling

2. **Batch Processing**
   - Process multiple items together
   - Reduce database round-trips

3. **Async Operations** (Future)
   - Parallel harvesting
   - Non-blocking API calls

### Expected Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Single Harvest | 5-30s | Depends on source |
| Gemini Analysis | 2-10s | Depends on data size |
| Database Save | <1s | Per 100 items |
| Full Harvest (All) | 2-5min | All 6 harvesters |

---

## Security Model

### API Key Management

```
.env file (gitignored)
    ↓
Environment Variables
    ↓
Application Config
    ↓
API Clients
```

### Data Privacy

- Only PUBLIC data harvested
- No PII stored
- Respect platform ToS
- Rate limiting enforced

---

## Deployment Architecture

### Development

```
Local Machine
├── Python 3.9+
├── SQLite Database
├── CLI Interface
└── Flask Dev Server
```

### Production

```
Server/Container
├── Python 3.9+
├── SQLite Database (persistent volume)
├── Gunicorn WSGI Server
├── Nginx Reverse Proxy
└── Systemd Service
```

### Orchestrator Integration

```
Orchestrator (main.py)
    │
    ├── Import UniversalHarvester
    │
    ├── Call harvest() methods
    │
    └── Pass data to Agents 1-11
```

---

## Extension Points

### Adding New Harvesters

1. Create `modules/my_harvester.py`
2. Inherit from `BaseHarvester`
3. Implement 5 abstract methods
4. Add to `config.json`
5. Import in `main.py`

### Adding New Data Sources

1. Add source to harvester's `get_data_sources()`
2. Implement extraction in `extract_raw_data()`
3. Update parsing in `parse_data()`
4. Enable in `config.json`

### Custom Analysis

1. Add prompt to `GeminiAnalyzer.SYSTEM_PROMPTS`
2. Create specialized method
3. Call from harvester

---

## Monitoring & Observability

### Metrics Available

- Harvest success rate
- Execution time per harvester
- Data quality distribution
- API rate limit usage
- Database size

### Accessing Metrics

```bash
# CLI
python main.py status

# API
GET /stats
```

---

## Future Architecture Enhancements

1. **Microservices Split**
   - Each harvester as separate service
   - Message queue (RabbitMQ/Kafka)
   - Centralized coordinator

2. **Real-time Streaming**
   - WebSocket connections
   - Live data updates
   - Event-driven architecture

3. **Distributed Caching**
   - Redis cluster
   - Cache invalidation
   - Shared across instances

4. **Advanced Analytics**
   - Time-series analysis
   - Trend prediction
   - Anomaly detection

---

**Architecture Version:** 1.0.0
**Last Updated:** 2025-01-14