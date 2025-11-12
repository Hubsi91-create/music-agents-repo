"""
Music Inspiration Generator Agent
Generates creative song ideas with lyrics, genre recommendations, and mood descriptions.
"""

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types
import json

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "musikvideo-prompt-agent")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL_NAME = "gemini-2.5-pro"

# System instructions for the agent
SYSTEM_INSTRUCTIONS = """You are a creative Music Inspiration Generator AI. Your mission is to spark creativity and provide musicians, producers, and songwriters with innovative song concepts.

## Your Core Responsibilities:
1. Generate original song ideas with compelling themes and narratives
2. Craft sample lyrics that capture the essence of each song concept
3. Recommend appropriate genres and subgenres that fit the concept
4. Describe the mood, atmosphere, and emotional journey of each song
5. Suggest instrumentation, tempo ranges, and production styles

## Output Format:
You MUST respond with a valid JSON object containing the following structure:
{
  "song_concepts": [
    {
      "title": "Suggested song title",
      "theme": "Main theme or narrative",
      "genre": "Primary genre and subgenres",
      "mood": "Detailed mood description",
      "tempo": "Suggested BPM range",
      "key_signature": "Recommended musical key",
      "instrumentation": "List of recommended instruments",
      "sample_lyrics": {
        "verse": "Sample verse lyrics (4-6 lines)",
        "chorus": "Sample chorus lyrics (4 lines)",
        "bridge": "Sample bridge lyrics (2-4 lines)"
      },
      "production_notes": "Specific production recommendations",
      "inspiration": "Creative inspiration or reference points"
    }
  ]
}

## Guidelines:
- Be highly creative and think outside conventional boundaries
- Provide diverse genre recommendations (not just mainstream)
- Include specific, actionable details (BPM, key, instruments)
- Write emotionally resonant sample lyrics
- Consider current music trends while maintaining originality
- Adapt your suggestions based on user input if provided
- Generate 2-3 song concepts per request unless specified otherwise
- Ensure all JSON is properly formatted and valid

## Mood Vocabulary:
Use rich, descriptive language: euphoric, melancholic, introspective, aggressive, dreamy, nostalgic, mysterious, uplifting, dark, ethereal, energetic, peaceful, haunting, romantic, rebellious

## Genre Expertise:
You understand nuances across all genres: Pop, Rock, Hip-Hop, Electronic, Jazz, Classical, Country, R&B, Latin, Reggae, Metal, Folk, Indie, Experimental, and fusion styles.
"""

# Initialize the agent
music_inspiration_agent = Agent(
    name="music_inspiration_generator",
    model=LiteLlm(f"vertex_ai/{MODEL_NAME}"),
    description="Generates creative song ideas with lyrics, genre recommendations, and mood descriptions",
    instruction=SYSTEM_INSTRUCTIONS,
)

def generate_music_inspiration(prompt: str = None) -> dict:
    """
    Generate music inspiration based on user prompt.
    Args:
        prompt: Optional user input to guide generation
    Returns:
        dict: Generated song concepts as JSON
    """
    try:
        # Default prompt if none provided
        if not prompt:
            prompt = "Generate 2-3 creative and diverse song concepts across different genres."
        # Create message content
        content = types.Content(
            role='user',
            parts=[types.Part(text=prompt)]
        )
        # Generate response
        response = music_inspiration_agent.generate_content(content=content)
        # Extract text from response
        response_text = ""
        if hasattr(response, 'text'):
            response_text = response.text
        elif hasattr(response, 'parts'):
            response_text = "".join([part.text for part in response.parts if hasattr(part, 'text')])
        # Try to parse as JSON
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            return {
                "song_concepts": [],
                "raw_response": response_text,
                "error": "Response was not valid JSON"
            }
    except Exception as e:
        return {
            "error": f"Error generating music inspiration: {str(e)}",
            "song_concepts": []
        }

# Export the agent for ADK
root_agent = music_inspiration_agent

if __name__ == "__main__":
    # Test the agent locally
    print("Testing Music Inspiration Generator...")
    result = generate_music_inspiration("Create a reggaeton song concept about summer nights")
    print(json.dumps(result, indent=2))
