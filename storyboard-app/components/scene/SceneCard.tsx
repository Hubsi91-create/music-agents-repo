'use client'

import React, { useState } from 'react'
import NeonButton from '../ui/NeonButton'
import LoadingSpinner from '../ui/LoadingSpinner'
import ProgressRing from '../ui/ProgressRing'
import AgentSelector from './AgentSelector'
import EnhancedPromptDisplay from './EnhancedPromptDisplay'
import SettingsPanel from './SettingsPanel'

export interface Agent {
  id: string
  name: string
  description: string
  icon: string
}

export interface EnhancedPrompt {
  original: string
  enhanced: string
  mood: string
  suggestedStyle: string
  shotSuggestions: string[]
  confidence: number
  reasoning?: string
}

export interface SceneSettings {
  format: string
  quality: string
  duration: string
  style: string
}

interface SceneCardProps {
  sceneId: string
  sceneNumber: number
  agents: Agent[]
  selectedAgent: Agent | null
  onAgentSelect: (agent: Agent) => void
}

export default function SceneCard({
  sceneId,
  sceneNumber,
  agents,
  selectedAgent,
  onAgentSelect,
}: SceneCardProps) {
  const [prompt, setPrompt] = useState('')
  const [enhancedPrompt, setEnhancedPrompt] = useState<EnhancedPrompt | null>(null)
  const [settings, setSettings] = useState<SceneSettings>({
    format: 'mp4',
    quality: '4k',
    duration: '30s',
    style: 'cinematic',
  })
  const [isEnhancing, setIsEnhancing] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationProgress, setGenerationProgress] = useState(0)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [showSettings, setShowSettings] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)

  const handleEnhanceWithAgent = async () => {
    if (!selectedAgent || !prompt.trim()) {
      alert('Please select an agent and enter a prompt')
      return
    }

    setIsEnhancing(true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/agents/call', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agentId: selectedAgent.id,
          userPrompt: prompt,
          context: { sceneId, settings },
        }),
      })

      const data = await response.json()
      setEnhancedPrompt({
        original: prompt,
        enhanced: data.enhancedPrompt,
        mood: data.mood,
        suggestedStyle: data.suggestedStyle,
        shotSuggestions: data.shotSuggestions,
        confidence: data.confidence,
        reasoning: data.reasoning,
      })
    } catch (error) {
      console.error('Error enhancing prompt:', error)
      // Demo fallback
      setEnhancedPrompt({
        original: prompt,
        enhanced: `A cinematic ${prompt} with dynamic camera movements and professional lighting`,
        mood: 'intense, dramatic',
        suggestedStyle: 'cinematic',
        shotSuggestions: ['wide establishing shot', 'close-up', 'tracking shot'],
        confidence: 0.85,
      })
    } finally {
      setIsEnhancing(false)
    }
  }

  const handleGenerate = async () => {
    const finalPrompt = enhancedPrompt?.enhanced || prompt
    if (!finalPrompt.trim()) {
      alert('Please enter a prompt')
      return
    }

    setIsGenerating(true)
    setGenerationProgress(0)

    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/runway/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sceneId,
          prompt: finalPrompt,
          ...settings,
        }),
      })

      const { taskId } = await response.json()

      // Poll for progress
      const pollInterval = setInterval(async () => {
        const statusResponse = await fetch(`/api/runway/status/${taskId}`)
        const statusData = await statusResponse.json()

        setGenerationProgress(statusData.progress)

        if (statusData.status === 'completed') {
          clearInterval(pollInterval)
          setVideoUrl(statusData.videoUrl)
          setIsGenerating(false)
          setGenerationProgress(100)
        } else if (statusData.status === 'failed') {
          clearInterval(pollInterval)
          setIsGenerating(false)
          alert('Video generation failed')
        }
      }, 2000)
    } catch (error) {
      console.error('Error generating video:', error)
      setIsGenerating(false)
      // Demo mode: fake progress
      let progress = 0
      const interval = setInterval(() => {
        progress += 10
        setGenerationProgress(progress)
        if (progress >= 100) {
          clearInterval(interval)
          setIsGenerating(false)
          // Demo video URL
          setVideoUrl('https://storage.googleapis.com/demo-video.mp4')
        }
      }, 300)
    }
  }

  return (
    <div className="card-neon mb-6">
      {/* Scene Header */}
      <div className="flex items-center justify-between mb-4 pb-4 border-b divider-neon">
        <h3 className="text-xl font-bold text-neon-cyan flex items-center gap-2">
          <span>🎬</span> Scene {sceneNumber}
        </h3>
        <div className="flex items-center gap-2">
          <button className="text-text-secondary hover:text-neon-cyan transition-colors p-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

      {/* Video Preview */}
      <div className="relative aspect-video bg-space-dark rounded-lg overflow-hidden mb-4 video-container">
        {videoUrl ? (
          <>
            <video
              src={videoUrl}
              className="w-full h-full object-cover"
              controls
              onPlay={() => setIsPlaying(true)}
              onPause={() => setIsPlaying(false)}
            />
            <div className="video-overlay flex items-center justify-center">
              {!isPlaying && (
                <button className="w-16 h-16 rounded-full bg-neon-cyan/20 border-2 border-neon-cyan
                                 flex items-center justify-center text-neon-cyan shadow-neon-cyan
                                 hover:scale-110 transition-transform">
                  <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </button>
              )}
            </div>
          </>
        ) : isGenerating ? (
          <div className="w-full h-full flex items-center justify-center">
            <ProgressRing progress={generationProgress} />
          </div>
        ) : (
          <div className="w-full h-full flex items-center justify-center text-text-secondary">
            <div className="text-center">
              <div className="text-6xl mb-4">🎥</div>
              <p>No video generated yet</p>
              <p className="text-sm mt-2">Enter a prompt and generate</p>
            </div>
          </div>
        )}
      </div>

      {/* Agent Selection */}
      <div className="mb-4">
        <AgentSelector
          agents={agents}
          selectedAgent={selectedAgent}
          onAgentSelect={onAgentSelect}
        />
      </div>

      {/* Prompt Input */}
      <div className="mb-4">
        <label className="text-sm font-medium text-text-secondary mb-2 block">
          📝 Scene Prompt
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe your scene... (Agent will enhance this)"
          className="textarea-neon w-full h-24 resize-none"
          disabled={isEnhancing || isGenerating}
        />
      </div>

      {/* Enhanced Prompt Display */}
      {enhancedPrompt && (
        <EnhancedPromptDisplay
          enhancedPrompt={enhancedPrompt}
          onEdit={() => setPrompt(enhancedPrompt.enhanced)}
          onRevert={() => setEnhancedPrompt(null)}
        />
      )}

      {/* Settings Panel */}
      <div className="mb-4">
        <button
          onClick={() => setShowSettings(!showSettings)}
          className="flex items-center gap-2 text-text-secondary hover:text-neon-cyan transition-colors"
        >
          <span>⚙️</span>
          <span className="text-sm font-medium">Settings</span>
          <span className="text-xs">{showSettings ? '▲' : '▼'}</span>
        </button>
        {showSettings && (
          <div className="mt-3">
            <SettingsPanel settings={settings} onSettingsChange={setSettings} />
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <NeonButton
          variant="purple"
          onClick={handleEnhanceWithAgent}
          disabled={!selectedAgent || !prompt.trim() || isEnhancing || isGenerating}
          className="flex-1"
        >
          {isEnhancing ? (
            <span className="flex items-center justify-center gap-2">
              <LoadingSpinner size="sm" />
              Enhancing...
            </span>
          ) : (
            '🤖 ENHANCE WITH AGENT'
          )}
        </NeonButton>
        <NeonButton
          variant="cyan"
          onClick={handleGenerate}
          disabled={!prompt.trim() || isGenerating}
          className="flex-1"
        >
          {isGenerating ? 'GENERATING...' : '🎬 GENERATE'}
        </NeonButton>
        <NeonButton
          variant="green"
          disabled={!videoUrl}
          className="px-6"
        >
          ⭐ SAVE
        </NeonButton>
      </div>
    </div>
  )
}
