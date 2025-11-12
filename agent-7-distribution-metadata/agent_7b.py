# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime

def generate_metadata(title="Electronic Cinematic Mix", genre="Electronic", mood="cinematic, professional"):
    """Generiere YouTube + Social Media Metadata."""

    # YouTube Metadata
    youtube_meta = {
        "title": f"{title} | {genre} | {mood}",
        "description": f"""🎵 NEW: {title}

Genre: {genre}
Mood: {mood}

✨ Professional electronic music video featuring top influencers
🎬 Cinematic visuals
🎧 High-quality audio production

Subscribe for more: [Link]
Follow us on social: [Instagram] [TikTok] [Twitter]

#ElectronicMusic #{genre.replace(' ', '')} #MusicVideo #Cinematic #4K""",
        "tags": ["electronic", "music", "cinematic", genre.lower(), "official video", "hd", "4k", "new music"],
        "category": "Music",
        "language": "en"
    }

    # Social Media Posts
    social_posts = {
        "instagram": f"""🎵 NEW DROP ALERT 🎵

{title}
Now available on YouTube! 🔗

🎬 Cinematic visuals
🎧 Electronic perfection
⚡ Tag someone who needs to hear this

Link in bio ↗️

#{genre.replace(' ', '')} #MusicVideo #ElectronicMusic #NewMusic""",

        "tiktok": f"""POV: You just found the sickest electronic track 🎵
{title} OUT NOW
Link in bio 🔗
#foryou #electronic #musicvideo #newmusic""",

        "twitter": f"""🔥 NEW MUSIC 🔥

{title}
{genre} • {mood}

Streaming now on YouTube ▶️
[Link]

#MusicProduction #{genre.replace(' ', '')} #NewMusic""",

        "youtube_short": f"""🎵 {title}
Genre: {genre}
Full video on my channel! ▶️"""
    }

    # Email Templates
    email_templates = {
        "influencer_outreach": f"""Subject: Collaboration Opportunity - Your Channel Featured!

Hi [Influencer Name],

We loved your channel and featured it in our new music video:
"{title}"

🎵 Genre: {genre}
🎬 Mood: {mood}

Check it out: [YouTube Link]

We'd love to collaborate on future projects!

Best regards,
[Your Name]""",

        "media_pitch": f"""Subject: New Music Release - {title}

Hi [Media Contact],

We're excited to announce: {title}

Details:
- Genre: {genre}
- Mood: {mood}
- Release: Today
- YouTube: [Link]

Perfect for playlists: #NewMusic #Electronic #Cinematic

Regards"""
    }

    return {
        "timestamp": datetime.now().isoformat(),
        "content": {
            "title": title,
            "genre": genre,
            "mood": mood
        },
        "youtube": youtube_meta,
        "social_media": social_posts,
        "email_templates": email_templates,
        "seo": {
            "meta_keywords": f"{genre.lower()}, electronic music, music video, cinematic, new music",
            "og_title": f"{title} | {genre} Music Video",
            "og_description": f"New {genre} music video with cinematic visuals. {mood}."
        }
    }

def main():
    print("[Agent 7b] Metadata Generator")

    result = generate_metadata()

    with open('metadata.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Metadata für YouTube, Instagram, TikTok, Twitter generiert!")
    print(f"[EMAIL TEMPLATES] 2x Email Vorlagen erstellt!")
    print(f"[SEO] Optimiert für Google & YouTube!")
    print(f"[SAVED] Ergebnisse in: metadata.json")

if __name__ == '__main__':
    main()
