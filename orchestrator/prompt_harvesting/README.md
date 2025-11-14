# Prompt Harvesting Module

AI-powered prompt harvesting, analysis, and training system for video generation agents.

## Overview

This module automatically collects, analyzes, and manages prompts from Reddit, YouTube, and web sources to train video generation AI agents (Runway, Veo, Sora, Pika).

### Features

- **Multi-Source Harvesting**: Reddit, YouTube, Web scraping
- **AI Analysis**: Google Gemini-powered prompt quality assessment
- **Local Scoring**: Cost-effective quality scoring without API calls
- **SQLite Database**: Persistent storage with pattern library
- **Agent Training**: Automated training pipeline for agents 5a, 5b, 8, and 11

## Components

### 1. PromptHarvester (`harvester.py`)

Collects prompts from multiple sources.

**Sources:**
- Reddit (via PRAW): Subreddits like RunwayML, PromptEngineering, VideoGeneration
- YouTube: Video descriptions and transcripts
- Web: GitHub repositories, blogs, articles

**Usage:**
```python
from orchestrator.prompt_harvesting import PromptHarvester

harvester = PromptHarvester()

# Harvest from all sources
results = harvester.harvest_all()

# Or harvest individually
reddit_prompts = harvester.harvest_reddit(subreddits=['RunwayML'], limit=50)
youtube_prompts = harvester.harvest_youtube(search_queries=['Runway Gen-4 prompts'])
web_prompts = harvester.harvest_web(['https://github.com/topics/prompt-engineering'])
```

### 2. PromptAnalyzer (`analyzer.py`)

Uses Google Gemini AI for intelligent prompt analysis.

**Features:**
- Quality scoring (1-10)
- Pattern extraction
- Prompt improvement suggestions
- Categorization (genre, model, complexity)

**Usage:**
```python
from orchestrator.prompt_harvesting import PromptAnalyzer

analyzer = PromptAnalyzer(model_name="gemini-2.5-flash")

# Analyze prompt quality
analysis = analyzer.analyze_prompt_quality(
    "A cinematic 4K shot of a futuristic city at night"
)
print(f"Score: {analysis['overall_score']}/10")

# Extract patterns from multiple prompts
patterns = analyzer.extract_patterns(prompts_list)

# Get improvement suggestions
improvements = analyzer.suggest_improvements(prompt_text, current_score=6.5)

# Categorize prompt
category = analyzer.categorize_prompt(prompt_text)
```

### 3. QualityScorer (`quality_scorer.py`)

Local quality assessment without API costs.

**Scoring Factors:**
- Community engagement (upvotes, comments)
- Prompt text quality (keywords, structure)
- Recency (newer prompts scored higher)
- Video quality indicators (4K, cinematic, etc.)

**Usage:**
```python
from orchestrator.prompt_harvesting import QualityScorer

scorer = QualityScorer()

# Score a single prompt
prompt_data = {
    'text': 'Cinematic 4K shot...',
    'upvotes': 150,
    'comments': 25,
    'created_utc': '2025-01-01T00:00:00'
}

result = scorer.combined_quality_score(prompt_data)
print(f"Combined Score: {result['combined_score']}/10")

# Rank multiple prompts
ranked = scorer.rank_prompts(prompts_list, min_score=7.0)

# Get statistics
stats = scorer.get_quality_stats(prompts_list)
```

### 4. PromptDatabase (`prompt_database.py`)

SQLite database for persistent storage.

**Tables:**
- `prompts`: Main prompt storage
- `patterns`: Pattern library
- `training_history`: Training usage tracking

**Usage:**
```python
from orchestrator.prompt_harvesting import PromptDatabase

db = PromptDatabase()

# Save prompts
db.save_prompt(prompt_data)
db.save_prompts(prompts_list)

# Retrieve top prompts
top_prompts = db.get_top_prompts(n=100, min_score=7.5, model_type='runway')

# Get patterns
patterns = db.get_patterns_summary(model_type='veo')

# Mark as trained
db.mark_as_trained(
    prompt_id=123,
    agent_name='agent_5a_veo',
    iterations=10,
    success=True
)

# Get statistics
stats = db.get_statistics()

db.close()
```

## Setup

### 1. Install Dependencies

```bash
pip install praw google-generativeai beautifulsoup4 requests youtube-transcript-api
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```env
# Reddit API (get from https://www.reddit.com/prefs/apps)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=PromptHarvester/1.0

# Google Gemini API (get from https://ai.google.dev/)
GEMINI_API_KEY=your_gemini_api_key
# OR
GOOGLE_API_KEY=your_google_api_key
```

### 3. Configure Settings

Edit `config.json` to customize:
- Subreddits to harvest
- YouTube search queries
- Quality thresholds
- Training parameters

## Enhanced Training Pipeline

The main integration with the orchestrator system.

### Usage

```python
from orchestrator.orchestrator import enhanced_training_pipeline

# Run the full pipeline
report = enhanced_training_pipeline(
    iterations=100,
    min_score=7.0
)

print(f"Status: {report['status']}")
print(f"Harvested: {report['harvesting']['total_harvested']} prompts")
print(f"High Quality: {report['quality']['high_quality_count']}")
print(f"Trained: {report['training']['prompts_selected']} prompts")
```

### Pipeline Steps

1. **Harvest**: Collect prompts from Reddit, YouTube, and Web
2. **Analyze**: Use Gemini AI to analyze prompt quality
3. **Score**: Apply local quality scoring
4. **Extract**: Identify successful patterns
5. **Store**: Save to SQLite database
6. **Train**: Feed top prompts to agents 5a, 5b, 8, and 11

### Command Line

```bash
# Run from orchestrator directory
cd orchestrator
python -c "from orchestrator import enhanced_training_pipeline; enhanced_training_pipeline()"
```

## Configuration

### config.json Structure

```json
{
  "reddit": {
    "subreddits": ["RunwayML", "PromptEngineering"],
    "limit": 100,
    "sort": "hot"
  },
  "youtube": {
    "search_queries": ["Runway Gen-4 prompts"],
    "max_results": 50
  },
  "quality": {
    "threshold": 7.0,
    "weights": {
      "gemini": 0.40,
      "community": 0.30,
      "quality": 0.20,
      "recency": 0.10
    }
  },
  "training": {
    "min_score_for_training": 7.0,
    "batch_size": 100
  }
}
```

## Database Schema

### prompts Table

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| source | TEXT | reddit/youtube/web |
| prompt_text | TEXT | The actual prompt |
| model_type | TEXT | runway/veo/sora/pika |
| quality_score | REAL | Combined quality score (0-10) |
| upvotes | INTEGER | Community upvotes |
| comments | INTEGER | Number of comments |
| gemini_analysis | TEXT | JSON analysis from Gemini |
| patterns | TEXT | JSON extracted patterns |
| used_for_training | INTEGER | 0/1 flag |
| harvested_at | TEXT | ISO timestamp |

### patterns Table

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| pattern_type | TEXT | keyword/structure/style |
| pattern_value | TEXT | The pattern |
| occurrences | INTEGER | Frequency count |
| model_type | TEXT | Associated model |
| quality_score | REAL | Average quality |

## Examples

### Example 1: Quick Harvest

```python
from orchestrator.prompt_harvesting import PromptHarvester, QualityScorer

harvester = PromptHarvester()
scorer = QualityScorer()

# Harvest from Reddit only
prompts = harvester.harvest_reddit(subreddits=['RunwayML'], limit=20)

# Score them
ranked = scorer.rank_prompts(prompts, min_score=5.0)

# Print top 5
for i, p in enumerate(ranked[:5], 1):
    print(f"{i}. Score: {p['quality_score']:.2f} - {p['title']}")
```

### Example 2: Gemini Analysis

```python
from orchestrator.prompt_harvesting import PromptAnalyzer

analyzer = PromptAnalyzer()

prompt = "A cinematic 4K shot of a futuristic city at sunset, camera slowly panning right, neon lights reflecting on wet streets, cyberpunk aesthetic"

analysis = analyzer.analyze_prompt_quality(prompt)

print(f"Overall Score: {analysis['overall_score']}/10")
print(f"Clarity: {analysis['clarity_score']}/10")
print(f"Specificity: {analysis['specificity_score']}/10")
print(f"Strengths: {', '.join(analysis['strengths'])}")
print(f"Best Model: {max(analysis['model_suitability'], key=analysis['model_suitability'].get)}")
```

### Example 3: Database Operations

```python
from orchestrator.prompt_harvesting import PromptDatabase

db = PromptDatabase()

# Get top Runway prompts
runway_prompts = db.get_top_prompts(
    n=50,
    min_score=8.0,
    model_type='runway'
)

# Get pattern summary
patterns = db.get_patterns_summary(model_type='runway', min_occurrences=3)

print(f"Found {len(runway_prompts)} top Runway prompts")
print(f"Common keywords: {patterns['patterns_by_type'].get('keyword', [])[:5]}")

# Get database statistics
stats = db.get_statistics()
print(f"Total prompts: {stats['total_prompts']}")
print(f"Quality distribution: {stats['quality']}")

db.close()
```

## Testing

Each module includes a `__main__` section for testing:

```bash
# Test harvester
python orchestrator/prompt_harvesting/harvester.py

# Test analyzer
python orchestrator/prompt_harvesting/analyzer.py

# Test scorer
python orchestrator/prompt_harvesting/quality_scorer.py

# Test database
python orchestrator/prompt_harvesting/prompt_database.py
```

## Cost Management

### Free Tier Usage

- **Reddit API**: Free with rate limits (60 requests/minute)
- **YouTube**: Web scraping (no API key needed)
- **Web Scraping**: Free
- **SQLite**: Free, no limits

### Gemini API Costs

- **Model**: gemini-2.5-flash (recommended for cost-efficiency)
- **Free Tier**: 15 requests/minute, 1 million tokens/minute
- **Cost Control**: Limit analysis to top prompts only

**Tips:**
1. Set `max_prompts_per_run` in config.json
2. Use local scoring first, Gemini for top candidates only
3. Cache Gemini results in database
4. Use fallback mode when API unavailable

## Troubleshooting

### Reddit Authentication Failed

```bash
# Check credentials in .env
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...

# Test connection
python -c "import praw; reddit = praw.Reddit(client_id='...', client_secret='...', user_agent='test'); print(reddit.read_only)"
```

### Gemini API Error

```bash
# Check API key
echo $GEMINI_API_KEY

# Test connection
python -c "import google.generativeai as genai; genai.configure(api_key='...'); model = genai.GenerativeModel('gemini-2.5-flash'); print('OK')"
```

### Database Locked

```python
# Close connections properly
db = PromptDatabase()
try:
    # ... operations ...
finally:
    db.close()
```

## Roadmap

- [ ] Add Twitter/X scraping
- [ ] Implement prompt versioning
- [ ] Add A/B testing for prompts
- [ ] Create web UI for prompt management
- [ ] Add automatic quality feedback loop
- [ ] Implement collaborative filtering

## Contributing

This module is part of the Music Agents Repository. See main README for contribution guidelines.

## License

Part of Music Agents Repo - All rights reserved.

## Support

For issues or questions, create an issue in the main repository.

---

**Version**: 1.0.0
**Last Updated**: 2025-01-14
**Maintained by**: Music Agents Repo Team
