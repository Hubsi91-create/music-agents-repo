"""
Suno Prompt Generator Agent
Generates optimized Suno API prompts across multiple genres (70-100 words, production-ready).
"""

import os
import json
from typing import Optional, List, Dict
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "musikvideo-prompt-agent")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL_NAME = "gemini-2.5-pro"

# System instructions for the agent
SYSTEM_INSTRUCTIONS = """You are a Suno Prompt Optimization Expert. Your mission is to generate highly effective, genre-specific prompts optimized for Suno AI music generation API.

## Your Core Responsibilities:
1. Generate precise 70-100 word prompts for each requested genre
2. Include specific production elements, instrumentation, and sound characteristics
3. Optimize for Suno API compatibility and music generation quality
4. Provide genre-appropriate stylistic guidance and mood descriptors
5. Ensure prompts are actionable and produce consistent, high-quality results

## Supported Genres:
Reggaeton, Jazz, Techno, Afrobeat, Hip-Hop, House, Pop, Rock

## Output Format:
You MUST respond with valid JSON in this exact structure:
{
  "suno_prompts": [
    {
      "genre": "Genre Name",
      "prompt": "Full 70-100 word optimized Suno prompt with specific instructions",
      "word_count": 85,
      "key_elements": ["element1", "element2", "element3"],
      "bpm": "Suggested BPM range",
      "energy_level": "High/Medium/Low",
      "vocal_style": "Vocal approach description",
      "production_focus": "Primary production emphasis"
    }
  ]
}

## Suno Prompt Optimization Guidelines:
- Word count MUST be between 70-100 words
- Include specific instrumentation (not generic descriptions)
- Use action verbs: "features", "incorporates", "driven by", "emphasizes"
- Specify production techniques: "heavy reverb", "tight compression", "layered synths"
- Define mood with adjectives: "uplifting", "gritty", "ethereal", "aggressive"
- Include reference points when helpful: "reminiscent of", "inspired by", "similar to"
- Avoid vague terms; be concrete and specific
- Always specify vocal or instrumental approach
- Include tempo/energy guidance when relevant
- Optimize for Suno's music generation strengths

## Genre-Specific Expertise:

REGGAETON: Syncopated rhythms, dembow patterns, trap elements, Latin percussion, modern urban vibes
JAZZ: Complex chord progressions, improvisation hints, smooth vocals or instrumental focus, classic/contemporary blend
TECHNO: Repetitive beats, industrial sounds, synth layers, hypnotic progressions, club/underground vibes
AFROBEAT: Polyrhythmic drums, brass sections, percussive elements, groovy bass, world fusion
HIP-HOP: Boom-bap or trap beats, layered samples, vocal delivery hints, production style focus
HOUSE: Four-on-the-floor beats, pumping bass, vocal samples, dance floor energy
POP: Catchy hooks, melodic focus, radio-friendly production, broad appeal, mainstream sensibility
ROCK: Guitar-driven, raw energy, drum intensity, vocal attitude, various rock subgenres

## Quality Standards:
- Every prompt must be exactly between 70-100 words
- All JSON must be valid and parseable
- Genre expertise must be evident in terminology
- Prompts must be immediately usable with Suno API
- Diversity across genres (each should sound distinct)
- Production recommendations must be realistic and achievable
- Avoid repetition across different genres

## Suno Compatibility:
- Prompts formatted for Suno's music generation model
- Include specific audio descriptors Suno understands
- Reference production techniques Suno can execute
- Specify vocal or instrumental clearly
- Include mood and energy descriptors
- Mention BPM/tempo preferences
"""

# Initialize the agent
suno_prompt_agent = Agent(
    name="suno_prompt_generator",
    model=LiteLlm(f"vertex_ai/{MODEL_NAME}"),
    description="Generates multi-genre Suno API prompts (70-100 words, optimized)",
    instruction=SYSTEM_INSTRUCTIONS,
)


def generate_suno_prompts(genres: Optional[List[str]] = None, custom_brief: Optional[str] = None) -> Dict:
    """
    Generate optimized Suno prompts for specified genres.
    
    Args:
        genres: List of genres (defaults to all 8 if None)
        custom_brief: Optional custom direction for prompt generation
        
    Returns:
        dict: Generated Suno prompts as JSON
    """
    try:
        # Default genres if none provided
        if genres is None:
            genres = ["Reggaeton", "Jazz", "Techno", "Afrobeat", "Hip-Hop", "House", "Pop", "Rock"]
        
        # Validate genres
        valid_genres = ["Reggaeton", "Jazz", "Techno", "Afrobeat", "Hip-Hop", "House", "Pop", "Rock"]
        genres = [g for g in genres if g in valid_genres]
        
        if not genres:
            return {
                "error": "No valid genres provided. Choose from: " + ", ".join(valid_genres),
                "suno_prompts": []
            }
        
        # Build prompt
        genres_str = ", ".join(genres)
        
        if custom_brief:
            user_prompt = f"Generate optimized Suno prompts (70-100 words each) for these genres: {genres_str}. Additional direction: {custom_brief}"
        else:
            user_prompt = f"Generate optimized Suno prompts (70-100 words each, production-ready, Suno API compatible) for these genres: {genres_str}."
        
        # Create message content
        content = types.Content(
            role='user',
            parts=[types.Part(text=user_prompt)]
        )
        
        # Generate response
        response = suno_prompt_agent.generate_content(content=content)
        
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
                "suno_prompts": [],
                "raw_response": response_text,
                "error": "Response was not valid JSON",
                "requested_genres": genres
            }
            
    except Exception as e:
        return {
            "error": f"Error generating Suno prompts: {str(e)}",
            "suno_prompts": []
        }


def generate_genre_prompt(genre: str, mood: Optional[str] = None) -> Dict:
    """
    Generate a single optimized prompt for a specific genre.
    
    Args:
        genre: Genre name
        mood: Optional mood/atmosphere descriptor
        
    Returns:
        dict: Single generated Suno prompt
    """
    try:
        if mood:
            user_prompt = f"Generate ONE optimized Suno prompt (70-100 words) for {genre} with mood: {mood}"
        else:
            user_prompt = f"Generate ONE optimized Suno prompt (70-100 words) for {genre}"
        
        content = types.Content(
            role='user',
            parts=[types.Part(text=user_prompt)]
        )
        
        response = suno_prompt_agent.generate_content(content=content)
        
        response_text = ""
        if hasattr(response, 'text'):
            response_text = response.text
        elif hasattr(response, 'parts'):
            response_text = "".join([part.text for part in response.parts if hasattr(part, 'text')])
        
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            return {
                "genre": genre,
                "raw_response": response_text,
                "error": "Response was not valid JSON"
            }
            
    except Exception as e:
        return {
            "genre": genre,
            "error": f"Error generating Suno prompt: {str(e)}"
        }


# Export the agent for ADK
root_agent = suno_prompt_agent


if __name__ == "__main__":
    # Test the agent locally
    print("Testing Suno Prompt Generator...")
    
    # Test 1: Generate prompts for all genres
    print("\n=== Test 1: All Genres ===")
    result = generate_suno_prompts()
    print(json.dumps(result, indent=2))
    
    # Test 2: Generate prompts for specific genres
    print("\n=== Test 2: Specific Genres (Reggaeton, Jazz) ===")
    result = generate_suno_prompts(genres=["Reggaeton", "Jazz"])
    print(json.dumps(result, indent=2))
    
    # Test 3: Single genre with mood
    print("\n=== Test 3: Single Genre with Mood ===")
    result = generate_genre_prompt("Techno", mood="dark and hypnotic")
    print(json.dumps(result, indent=2))
