# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime

def analyze_influencers(influencers_file="../agent-6-influencer-matcher/influencers.json"):
    """Analysiere Influencer für Distribution."""
    try:
        with open(influencers_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[ERROR] influencers.json nicht gefunden!")
        sys.exit(1)

    influencers = data.get('influencers', [])

    # Ranking & Scoring
    recommendations = []
    for inf in influencers:
        subs = int(inf.get('subscribers', '0').replace(',', '')) if isinstance(inf.get('subscribers'), str) else 0
        views = int(inf.get('views', '0').replace(',', '')) if isinstance(inf.get('views'), str) else 0

        # Berechne Collaboration Score (0-100)
        if subs > 0:
            engagement_ratio = (views / (subs * 10)) if subs > 0 else 0
            reach_score = min(100, subs / 10000) if subs > 0 else 0
            engagement_score = min(100, engagement_ratio * 100)
            collaboration_score = (reach_score * 0.6) + (engagement_score * 0.4)
        else:
            collaboration_score = 0

        rec = {
            "rank": inf.get('rank', 0),
            "channel_name": inf.get('channel_name', ''),
            "channel_id": inf.get('channel_id', ''),
            "subscribers": inf.get('subscribers', '0'),
            "views": inf.get('views', '0'),
            "collaboration_score": round(collaboration_score, 1),
            "estimated_reach": f"{subs * 0.1:.0f}-{subs * 0.3:.0f}",
            "engagement_probability": f"{min(8, max(1, engagement_ratio * 2)):.1f}%",
            "best_post_time": "14:00-16:00 UTC (Peak Hours)",
            "priority": "HIGH" if collaboration_score > 70 else "MEDIUM" if collaboration_score > 40 else "LOW",
            "email_template": f"Collaboration: Your Channel in New Electronic Music Video",
            "url": inf.get('url', '')
        }
        recommendations.append(rec)

    # Sortiere nach Collaboration Score
    recommendations = sorted(recommendations, key=lambda x: x['collaboration_score'], reverse=True)

    # Top 5
    top_5 = recommendations[:5]

    return {
        "timestamp": datetime.now().isoformat(),
        "total_influencers": len(influencers),
        "top_5_recommendations": top_5,
        "all_recommendations": recommendations,
        "distribution_strategy": {
            "phase_1": "Contact Top 5 (Week 1)",
            "phase_2": "Secondary Outreach (Week 2)",
            "phase_3": "Community Posts (Week 3)",
            "expected_total_reach": f"{sum([int(x['subscribers'].replace(',', '')) if ',' in str(x['subscribers']) else int(x['subscribers'] or 0) for x in influencers]) * 0.2:.0f}+"
        }
    }

def main():
    print("[Agent 7a] Analytics & Distribution Strategy")

    result = analyze_influencers()

    # Speichere Result
    with open('distribution_strategy.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] {result['total_influencers']} Influencer analysiert!")
    print(f"[TOP 5] Collaboration Partners identifiziert!")
    print(f"[SAVED] Ergebnisse in: distribution_strategy.json")

if __name__ == '__main__':
    main()
