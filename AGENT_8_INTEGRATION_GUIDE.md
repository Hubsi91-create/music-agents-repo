# AGENT 8 TRAINING SYSTEM - STORYBOARD INTEGRATION GUIDE

**Stand:** 12. November 2025
**Version:** 1.0
**Status:** Production Ready

---

## 📋 OVERVIEW

This guide explains how to integrate Agent 8's training system into your existing Storyboard App.

**3 New Modules:**
1. **agent_8_metrics.py** - Metrics Collection System
2. **agent_8_storyboard_bridge.py** - Integration Bridge (4 APIs)
3. **agent_8_dashboard.py** - Training Dashboard (HTML)

---

## 🎯 ARCHITECTURE

```
Storyboard App (Your Existing Code)
    ↓
Agent8StoryboardBridge (4 APIs)
    ├─→ Agent8PromptRefiner (Validation)
    └─→ Agent8MetricsCollector (Training Data)
        ↓
    agent_8_metrics.json (Database)
        ↓
Agent8TrainingDashboard (Visualization)
```

---

## 📁 FILE STRUCTURE

```
music-agents-repo/
├── agent_8_prompt_refiner.py        # Existing - Validator
├── config_agent8.json               # Existing - Config
│
├── agent_8_metrics.py               # NEW - Metrics System
├── agent_8_storyboard_bridge.py    # NEW - Integration Bridge
├── agent_8_dashboard.py             # NEW - Dashboard
│
└── data/
    └── agent_8_metrics.json         # Auto-created - Database
```

---

## 🚀 QUICK START - 5 STEPS

### STEP 1: Import the Bridge

In your Storyboard App main file:

```python
from agent_8_storyboard_bridge import Agent8StoryboardBridge

class StoryboardApp:
    def __init__(self):
        # Initialize Agent 8 Bridge
        self.agent8_bridge = Agent8StoryboardBridge()
        print("✅ Agent 8 Training System initialized")
```

### STEP 2: Validate Prompts

When user clicks "Validate" button:

```python
def on_validate_button_clicked(self, prompt, prompt_type, genre, scene_id):
    """User clicks 'Validate' in Storyboard UI"""

    # Call Agent 8
    result = self.agent8_bridge.validate_prompt_from_storyboard(
        prompt=prompt,
        prompt_type=prompt_type,       # "veo_3.1" or "runway_gen4"
        genre=genre,                    # "reggaeton", "edm", etc.
        storyboard_scene_id=scene_id   # Your scene ID
    )

    # Show results in UI
    if result["status"] == "success":
        quality_score = result["validation"]["quality_score"]
        ready = result["validation"]["ready_for_generation"]
        refined_prompt = result["refined_prompt"]

        # Update your UI
        self.show_validation_result(quality_score, ready, refined_prompt)

        # Store validation_id for later feedback
        self.current_validation_id = result["validation_id"]
    else:
        self.show_error(result["error"])
```

### STEP 3: Send Generation Feedback

After Agent 5c/5d generates video:

```python
def on_video_generated(self, validation_id, success, quality_score):
    """Called after Agent 5c/5d finishes video generation"""

    # Send feedback to Agent 8
    result = self.agent8_bridge.send_generation_feedback(
        validation_id=validation_id,
        generation_success=success,      # True/False
        generation_quality_score=quality_score  # 0.0-1.0
    )

    # Optionally update dashboard
    self.refresh_agent8_dashboard()
```

### STEP 4: Display Training Dashboard

Add a "Training" tab in your Storyboard UI:

```python
def show_agent8_training_dashboard(self):
    """Show Agent 8 training metrics in UI"""

    # Get dashboard data
    dashboard = self.agent8_bridge.get_dashboard_data()

    if dashboard["status"] == "success":
        # Display in your UI
        overview = dashboard["overview"]

        print(f"System Status: {overview['status_message']}")
        print(f"Total Validations: {overview['total_validations']}")
        print(f"Average Quality: {overview['avg_quality_score']:.2f}")
        print(f"Success Rate: {overview['success_rate']*100:.1f}%")

        # Show per-genre stats
        for genre, stats in dashboard["by_genre"].items():
            print(f"\n{genre}:")
            print(f"  Count: {stats['count']}")
            print(f"  Avg Score: {stats['avg_score']:.2f}")
            print(f"  Success: {stats['success_rate']*100:.1f}%")

        # Show recommendations
        for genre, rec in dashboard["recommendations"].items():
            print(f"\n{rec['recommendation']}")
```

### STEP 5: Save HTML Dashboard (Optional)

Generate beautiful HTML dashboard:

```python
from agent_8_dashboard import Agent8TrainingDashboard

def export_training_dashboard(self):
    """Export training dashboard as HTML"""

    dashboard = Agent8TrainingDashboard()
    dashboard.save_dashboard_html("agent_8_dashboard.html")

    print("✅ Dashboard saved! Open agent_8_dashboard.html in browser")
```

---

## 🔌 4 APIS - DETAILED REFERENCE

### API 1: `validate_prompt_from_storyboard()`

**Purpose:** Validate a prompt and record metrics

**Call from:** Storyboard UI when user clicks "Validate"

**Parameters:**
- `prompt` (str): The prompt text
- `prompt_type` (str): "veo_3.1" or "runway_gen4"
- `genre` (str): "reggaeton", "edm", "hiphop", "pop", "rb_soul"
- `storyboard_scene_id` (str): Your scene identifier

**Returns:**
```python
{
    "status": "success",
    "validation_id": "val_1699876543210",
    "validation": {
        "quality_score": 0.85,
        "quality_rating": 4.25,
        "ready_for_generation": True,
        "scores": {
            "structural": 0.90,
            "genre_compliance": 0.80,
            "artifact_risk": 0.75,
            "consistency": 0.95,
            "performance": 0.90
        },
        "issues": [...],
        "recommendations": [...]
    },
    "refined_prompt": "...",
    "original_prompt": "...",
    "auto_fixes": [...],
    "generation_mode": "veo_standard",
    "genre_detected": "reggaeton",
    "metrics": {...}
}
```

### API 2: `send_generation_feedback()`

**Purpose:** Send real-world generation results back to Agent 8

**Call from:** Agent 5c/5d after video generation completes

**Parameters:**
- `validation_id` (str): ID from validation response
- `generation_success` (bool): True if generation succeeded
- `generation_quality_score` (float): Quality score 0.0-1.0
- `error_message` (str, optional): Error if generation failed

**Returns:**
```python
{
    "status": "success",
    "message": "Feedback recorded for validation val_xxx",
    "updated_metrics": {...},
    "recommendations": {...}
}
```

### API 3: `get_dashboard_data()`

**Purpose:** Get all training metrics for display

**Call from:** Storyboard UI dashboard tab

**Parameters:** None

**Returns:**
```python
{
    "status": "success",
    "overview": {
        "total_validations": 150,
        "avg_quality_score": 0.82,
        "success_count": 120,
        "success_rate": 0.80,
        "system_status": "good",
        "status_message": "🟢 System performing well"
    },
    "by_genre": {...},
    "by_prompt_type": {...},
    "recommendations": {...},
    "recent_validations": [...]
}
```

### API 4: `send_manual_feedback()`

**Purpose:** Record manual user feedback

**Call from:** Storyboard UI when user rates a validation

**Parameters:**
- `validation_id` (str): ID from validation response
- `user_satisfaction` (int): Rating 1-5 stars
- `notes` (str): User's comments

**Returns:**
```python
{
    "status": "success",
    "message": "User feedback recorded successfully"
}
```

---

## 📊 TRAINING WORKFLOW

### Week 1: Initial Data Collection
```
User creates prompts → Validates with Agent 8 → Metrics recorded
- 100 validations collected
- Baseline quality score: 0.75
- Dashboard shows initial stats
```

### Week 2: Feedback Loop Active
```
Agent 5c/5d generates videos → Sends feedback → Metrics updated
- 50% of validations now have real feedback
- Quality score improves: 0.78 (+4%)
- Recommendations become more accurate
```

### Week 3: Analysis & Optimization
```
Dashboard shows genre-specific patterns
- Reggaeton: 0.85 avg (excellent)
- EDM: 0.72 avg (needs work)
- Adjust config for EDM based on recommendations
```

### Week 4: Production Ready
```
- 500+ prompts validated
- Strong feedback loop established
- Quality score: 0.85 avg (+13% from baseline)
- System optimized per genre
```

---

## 🎨 DASHBOARD EXAMPLE

The HTML dashboard (`agent_8_dashboard.html`) shows:

**📊 System Overview**
- Total validations
- Average quality score
- Success rate
- System health status

**🎵 Genre Performance**
- Per-genre statistics
- Average scores
- Ready rates
- Success rates

**💡 Recommendations**
- Genre-specific optimization tips
- Automatic suggestions based on data
- Action items for improvement

**📋 Recent Validations**
- Last 10 validations
- Timestamps, genres, scores
- Generation success status

---

## 🧪 TESTING THE INTEGRATION

### Test 1: Basic Validation

```python
from agent_8_storyboard_bridge import Agent8StoryboardBridge

bridge = Agent8StoryboardBridge()

result = bridge.validate_prompt_from_storyboard(
    prompt="Woman, 30s, walks to window...",
    prompt_type="veo_3.1",
    genre="reggaeton",
    storyboard_scene_id="test_scene_001"
)

print(f"Quality Score: {result['validation']['quality_score']:.2f}")
print(f"Ready: {result['validation']['ready_for_generation']}")
```

### Test 2: Generation Feedback

```python
bridge.send_generation_feedback(
    validation_id="val_1699876543210",
    generation_success=True,
    generation_quality_score=0.88
)
```

### Test 3: Dashboard Export

```python
from agent_8_dashboard import Agent8TrainingDashboard

dashboard = Agent8TrainingDashboard()
dashboard.save_dashboard_html("test_dashboard.html")
# Open test_dashboard.html in browser
```

---

## 🔧 CONFIGURATION

### Metrics Database Location

Default: `data/agent_8_metrics.json`

To change:
```python
bridge = Agent8StoryboardBridge(
    config_path="config_agent8.json",
    metrics_db_path="custom/path/metrics.json"
)
```

### Genre Configuration

Edit `config_agent8.json` to add/modify genres:
```json
{
  "genres": [
    {
      "id": "new_genre",
      "display_name": "New Genre",
      "color_temp": 6000,
      "saturation_boost": 20,
      "dialog_max_words": 7,
      "auto_negatives": ["..."]
    }
  ]
}
```

---

## 📈 METRICS COLLECTED

For each validation:
- Input prompt (truncated)
- Prompt type & genre
- Quality scores (5 layers)
- Issues found
- Auto-fixes applied
- Ready-for-generation flag
- Generation success (when available)
- Generation quality (when available)
- User feedback (when provided)

Aggregated metrics:
- Total validations
- Average quality score
- Success rate
- Per-genre stats
- Per-prompt-type stats
- Recommendations

---

## 🐛 TROUBLESHOOTING

### Issue: "Module not found"

**Solution:**
```bash
# Ensure all files are in the same directory
ls -la agent_8_*.py
```

### Issue: "Metrics database not found"

**Solution:**
```bash
# Create data directory
mkdir -p data

# The database will be auto-created on first run
python agent_8_metrics.py
```

### Issue: "Config file not found"

**Solution:**
```python
# Specify correct path
bridge = Agent8StoryboardBridge(
    config_path="path/to/config_agent8.json"
)
```

---

## 🎯 NEXT STEPS

1. **Integrate into Storyboard App** - Follow Quick Start above
2. **Run initial validations** - Collect baseline data
3. **Enable feedback loop** - Connect Agent 5c/5d
4. **Monitor dashboard** - Track training progress
5. **Optimize based on recommendations** - Improve over time

---

## 📚 API REFERENCE SUMMARY

| API | Purpose | Called By | Returns |
|-----|---------|-----------|---------|
| `validate_prompt_from_storyboard()` | Validate & record | Storyboard UI | Validation results + metrics |
| `send_generation_feedback()` | Real-world feedback | Agent 5c/5d | Updated metrics |
| `get_dashboard_data()` | Training metrics | Storyboard UI | Dashboard data |
| `send_manual_feedback()` | User feedback | Storyboard UI | Confirmation |

---

## ✅ CHECKLIST

Before integration:
- [ ] All 3 modules in repository
- [ ] config_agent8.json exists
- [ ] data/ directory created
- [ ] Tested basic validation
- [ ] Tested dashboard generation

After integration:
- [ ] Storyboard App imports bridge
- [ ] Validation button calls API 1
- [ ] Agent 5c/5d calls API 2
- [ ] Dashboard tab shows API 3 data
- [ ] Manual feedback uses API 4

---

**AGENT 8 TRAINING SYSTEM - READY FOR PRODUCTION**

Stand: 12. November 2025
Version: 1.0
Status: ✅ Production Ready
