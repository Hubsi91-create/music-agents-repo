const express = require('express')
const { VertexAI } = require('@google-cloud/vertexai')
const { authMiddleware } = require('../middleware/auth')
const { retryWithBackoff } = require('../lib/retry')
const router = express.Router()

// Initialize Vertex AI
const vertexAI = new VertexAI({
  project: process.env.GOOGLE_PROJECT_ID,
  location: process.env.VERTEX_AI_LOCATION || 'us-central1',
})

// List available agents (demo agents for now)
router.get('/', (req, res) => {
  const agents = [
    {
      id: 'cinematic-director',
      name: 'Cinematic Director Agent',
      description: 'Specializes in shot composition, camera movements, and cinematic storytelling for music videos',
      icon: '🎬',
      model: 'gemini-2.0-flash-exp',
    },
    {
      id: 'scene-architect',
      name: 'Scene Architect Agent',
      description: 'Creates detailed scene breakdowns with locations, props, lighting setups, and composition',
      icon: '🏗️',
      model: 'gemini-1.5-pro',
    },
    {
      id: 'visual-effects',
      name: 'Visual Effects Agent',
      description: 'Enhances prompts with cutting-edge VFX, transitions, and post-production ideas',
      icon: '✨',
      model: 'gemini-1.5-pro',
    },
    {
      id: 'music-video-specialist',
      name: 'Music Video Specialist',
      description: 'Optimizes scenes for music video production with sync, rhythm, and genre-specific aesthetics',
      icon: '🎵',
      model: 'gemini-2.0-flash-exp',
    },
  ]

  res.json({ agents })
})

// Call agent to enhance prompt
router.post('/call', async (req, res) => {
  const { agentId, userPrompt, context } = req.body

  if (!agentId || !userPrompt) {
    return res.status(400).json({
      error: 'Missing required fields',
      message: 'agentId and userPrompt are required',
    })
  }

  try {
    // Get agent configuration
    const agentsResponse = await fetch(`http://localhost:${process.env.PORT || 3001}/api/agents`)
    const { agents } = await agentsResponse.json()
    const agent = agents.find(a => a.id === agentId)

    if (!agent) {
      return res.status(404).json({ error: 'Agent not found' })
    }

    // System prompts for each agent type
    const systemPrompts = {
      'cinematic-director': `You are an expert film director specializing in music videos.
Your role is to take user scene descriptions and enhance them with cinematic details, shot suggestions, and visual moods.

Respond with a JSON object containing:
{
  "enhancedPrompt": "detailed enhanced prompt suitable for AI video generation",
  "mood": "comma-separated moods",
  "suggestedStyle": "comma-separated styles",
  "shotSuggestions": ["array", "of", "shot", "types"],
  "reasoning": "brief explanation of your enhancements",
  "confidence": 0.0-1.0
}`,
      'scene-architect': `You are a master storyboard artist and scene architect.
Take scene descriptions and create detailed breakdowns including locations, props, lighting, and composition.

Respond with JSON matching the schema with enhanced prompts optimized for AI video generation.`,
      'visual-effects': `You are a VFX specialist for music videos.
Enhance prompts with cutting-edge visual effects, transitions, and post-production ideas.

Respond with JSON including VFX techniques, transitions, and effect chains.`,
      'music-video-specialist': `You are a music video production specialist.
Optimize scenes for music video production with sync, rhythm, and genre-specific aesthetics.

Respond with JSON including rhythm sync, genre aesthetics, and production techniques.`,
    }

    const systemPrompt = systemPrompts[agentId] || systemPrompts['cinematic-director']

    // Construct full prompt with context
    let fullPrompt = `User Prompt: "${userPrompt}"\n\n`
    if (context) {
      fullPrompt += `Context:\n`
      if (context.musicTrack) fullPrompt += `- Music: ${context.musicTrack}\n`
      if (context.duration) fullPrompt += `- Duration: ${context.duration}\n`
      if (context.mood) fullPrompt += `- Desired Mood: ${context.mood}\n`
      if (context.settings) fullPrompt += `- Settings: ${JSON.stringify(context.settings)}\n`
    }
    fullPrompt += `\nPlease enhance this prompt for AI video generation with your expertise.`

    // Call Gemini model with retry logic
    const response = await retryWithBackoff(async () => {
      const model = vertexAI.getGenerativeModel({
        model: agent.model,
        generationConfig: {
          temperature: 0.8,
          topP: 0.95,
          maxOutputTokens: 2048,
        },
      })

      const result = await model.generateContent([
        { text: systemPrompt },
        { text: fullPrompt },
      ])

      return result.response
    }, 3, 2000)

    const text = response.candidates[0].content.parts[0].text

    // Try to parse JSON response
    let agentResponse
    try {
      // Extract JSON from markdown code blocks if present
      const jsonMatch = text.match(/```json\n([\s\S]*?)\n```/) || text.match(/\{[\s\S]*\}/)
      const jsonText = jsonMatch ? (jsonMatch[1] || jsonMatch[0]) : text
      agentResponse = JSON.parse(jsonText)
    } catch (parseError) {
      // Fallback if JSON parsing fails
      console.warn('Failed to parse agent response as JSON:', parseError)
      agentResponse = {
        enhancedPrompt: text,
        mood: 'cinematic',
        suggestedStyle: 'professional',
        shotSuggestions: ['wide shot', 'close-up'],
        reasoning: 'Enhanced based on prompt analysis',
        confidence: 0.7,
      }
    }

    // Validate response structure
    if (!agentResponse.enhancedPrompt) {
      agentResponse.enhancedPrompt = userPrompt
    }

    res.json({
      success: true,
      agentId,
      agentName: agent.name,
      ...agentResponse,
    })
  } catch (error) {
    console.error('Agent call error:', error)
    res.status(500).json({
      error: 'Agent call failed',
      message: error.message,
      agentId,
    })
  }
})

module.exports = router
