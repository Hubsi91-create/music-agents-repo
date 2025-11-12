'use client'

import React, { useState, useEffect } from 'react'
import Header from '../../components/layout/Header'
import LeftSidebar from '../../components/layout/LeftSidebar'
import RightPanel from '../../components/layout/RightPanel'
import SceneCard from '../../components/scene/SceneCard'

interface Agent {
  id: string
  name: string
  description: string
  icon: string
}

interface Scene {
  id: string
  name: string
}

export default function StoryboardPage() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null)
  const [scenes, setScenes] = useState<Scene[]>([{ id: 'scene-1', name: 'Scene 1' }])
  const [activeSceneId, setActiveSceneId] = useState('scene-1')
  const [metadata, setMetadata] = useState({
    projectName: 'Untitled Project',
    duration: '3:30',
    genre: 'Electronic',
  })
  const [isLoading, setIsLoading] = useState(true)

  // Fetch available agents on mount
  useEffect(() => {
    fetchAgents()
  }, [])

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents')
      const data = await response.json()
      setAgents(data.agents || [])
      if (data.agents && data.agents.length > 0) {
        setSelectedAgent(data.agents[0])
      }
    } catch (error) {
      console.error('Error fetching agents:', error)
      // Demo agents fallback
      const demoAgents = [
        {
          id: 'cinematic-director',
          name: 'Cinematic Director Agent',
          description: 'Specializes in shot composition, camera movements, and cinematic storytelling',
          icon: '🎬',
        },
        {
          id: 'scene-architect',
          name: 'Scene Architect Agent',
          description: 'Creates detailed scene breakdowns with locations, props, and lighting',
          icon: '🏗️',
        },
        {
          id: 'visual-effects',
          name: 'Visual Effects Agent',
          description: 'Enhances prompts with cutting-edge VFX and post-production ideas',
          icon: '✨',
        },
        {
          id: 'music-video-specialist',
          name: 'Music Video Specialist',
          description: 'Optimizes scenes for music video production with sync and rhythm',
          icon: '🎵',
        },
      ]
      setAgents(demoAgents)
      setSelectedAgent(demoAgents[0])
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddScene = () => {
    const newSceneNumber = scenes.length + 1
    const newScene = {
      id: `scene-${newSceneNumber}`,
      name: `Scene ${newSceneNumber}`,
    }
    setScenes([...scenes, newScene])
    setActiveSceneId(newScene.id)

    // Scroll to new scene
    setTimeout(() => {
      const element = document.getElementById(newScene.id)
      element?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 100)
  }

  const handleSceneSelect = (sceneId: string) => {
    setActiveSceneId(sceneId)
    const element = document.getElementById(sceneId)
    element?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-space-dark flex items-center justify-center">
        <div className="text-center">
          <div className="spinner-neon w-16 h-16 mx-auto mb-4" />
          <p className="text-text-secondary">Loading Storyboard App...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-space-dark">
      {/* Header */}
      <Header
        selectedAgent={selectedAgent}
        onAgentSelect={setSelectedAgent}
        agents={agents}
      />

      {/* Main Layout */}
      <div className="relative">
        {/* Left Sidebar */}
        <LeftSidebar
          scenes={scenes}
          activeSceneId={activeSceneId}
          onSceneSelect={handleSceneSelect}
          onAddScene={handleAddScene}
        />

        {/* Main Content */}
        <main className="ml-20 mr-80 min-h-[calc(100vh-70px)] p-8">
          <div className="max-w-5xl mx-auto">
            {/* Project Header */}
            <div className="mb-8">
              <h2 className="text-4xl font-bold text-glow-cyan text-neon-cyan mb-2">
                {metadata.projectName}
              </h2>
              <p className="text-text-secondary">
                {metadata.genre} • {metadata.duration} • {scenes.length} scene{scenes.length !== 1 ? 's' : ''}
              </p>
            </div>

            {/* Scene Cards */}
            {scenes.map((scene, index) => (
              <div
                key={scene.id}
                id={scene.id}
                className={`transition-opacity ${
                  activeSceneId === scene.id ? 'opacity-100' : 'opacity-75'
                }`}
              >
                <SceneCard
                  sceneId={scene.id}
                  sceneNumber={index + 1}
                  agents={agents}
                  selectedAgent={selectedAgent}
                  onAgentSelect={setSelectedAgent}
                />
              </div>
            ))}

            {/* Add Scene Prompt */}
            {scenes.length === 0 && (
              <div className="text-center py-20">
                <div className="text-6xl mb-4">🎬</div>
                <p className="text-text-secondary mb-6">No scenes yet</p>
                <button
                  onClick={handleAddScene}
                  className="btn-neon-cyan"
                >
                  + ADD FIRST SCENE
                </button>
              </div>
            )}
          </div>
        </main>

        {/* Right Panel */}
        <RightPanel metadata={metadata} onMetadataUpdate={setMetadata} />
      </div>
    </div>
  )
}
