# -*- coding: utf-8 -*-
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_authenticated_service(client_secret_file='client_secret.json'):
    """
    Authentifiziere mit OAuth 2.0 und hole YouTube Service.
    """
    creds = None
    token_file = 'token.json'
    
    # Wenn token.json existiert, verwende den gecachten token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # Wenn kein gültiger Token, starte OAuth Flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(client_secret_file):
                print(f"[ERROR] {client_secret_file} nicht gefunden!")
                print("[HINT] Speichere dein OAuth JSON von Google Cloud Console!")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Speichere Token für nächstes mal
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    youtube = build('youtube', 'v3', credentials=creds)
    return youtube

def search_youtube_channels(youtube, query, max_results=10):
    """
    Suche YouTube Kanäle basierend auf Query.
    """
    try:
        request = youtube.search().list(
            q=query,
            type='channel',
            part='snippet',
            maxResults=max_results,
            order='viewCount',
            relevanceLanguage='de'
        )
        response = request.execute()
        return response
    except HttpError as e:
        print(f"[ERROR] YouTube API Error: {e}")
        return None

def get_channel_stats(youtube, channel_id):
    """
    Hole Channel Statistiken (Subscribers, Views).
    """
    try:
        request = youtube.channels().list(
            id=channel_id,
            part='statistics,snippet'
        )
        response = request.execute()
        
        if response['items']:
            item = response['items'][0]
            stats = item.get('statistics', {})
            snippet = item.get('snippet', {})
            
            return {
                "channel_name": snippet.get('title', 'Unknown'),
                "channel_id": channel_id,
                "subscribers": stats.get('subscriberCount', 'Private'),
                "views": stats.get('viewCount', 'N/A'),
                "video_count": stats.get('videoCount', 'N/A'),
                "description": snippet.get('description', '')[:100],
                "url": f"https://www.youtube.com/channel/{channel_id}",
                "thumbnail": snippet.get('thumbnails', {}).get('default', {}).get('url', '')
            }
    except HttpError as e:
        print(f"[WARNING] Konnte Stats für {channel_id} nicht laden: {e}")
    
    return None

def main():
    if len(sys.argv) < 3:
        print("[Agent 6] Influencer Matcher mit YouTube OAuth 2.0")
        print("Usage: python agent_6.py <music_genre> <mood>")
        sys.exit(1)
    
    try:
        music_genre = sys.argv[1]
        mood = sys.argv[2]
        
        print(f"[Agent 6] Suche nach Influencern für: {music_genre} ({mood})")
        
        # Authentifiziere mit OAuth 2.0
        print(f"[INFO] Starte OAuth 2.0 Authentifizierung...")
        youtube = get_authenticated_service()
        print(f"[SUCCESS] Authentifizierung erfolgreich! ✓")
        
        # Erstelle Search Query
        search_query = f"{music_genre} music video {mood} professional"
        print(f"[INFO] Suche auf YouTube: '{search_query}'")
        
        # Suche Kanäle
        search_results = search_youtube_channels(youtube, search_query, max_results=10)
        
        if not search_results or 'items' not in search_results:
            print("[ERROR] Keine YouTube Ergebnisse!")
            sys.exit(1)
        
        influencers = []
        print(f"[INFO] {len(search_results['items'])} Kanäle gefunden, hole Statistiken...")
        
        # Hole Stats für jeden Kanal
        for i, item in enumerate(search_results['items'], 1):
            channel_id = item['snippet']['channelId']
            stats = get_channel_stats(youtube, channel_id)
            
            if stats:
                # Berechne Recommendation Score
                score = 95 - (i * 5)  # Top-to-Bottom scoring
                stats['rank'] = i
                stats['recommendation_score'] = score
                stats['mood_match'] = mood
                stats['genre_match'] = music_genre
                stats['platform'] = 'YouTube'
                
                influencers.append(stats)
        
        if not influencers:
            print("[ERROR] Keine Statistiken konnten geladen werden!")
            sys.exit(1)
        
        # Speichere Ergebnisse
        result = {
            "timestamp": datetime.now().isoformat(),
            "music_genre": music_genre,
            "mood": mood,
            "total_found": len(influencers),
            "recommendation_type": "Premium YouTube Influencers",
            "authentication": "OAuth 2.0",
            "influencers": influencers
        }
        
        with open('influencers.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"[SUCCESS] {len(influencers)} Influencer gefunden und analysiert!")
        print(f"[SAVED] Ergebnisse in: influencers.json")
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
