'use client'

import React from 'react'

interface Scene {
  id: string
  name: string
}

interface LeftSidebarProps {
  scenes: Scene[]
  activeSceneId: string
  onSceneSelect: (sceneId: string) => void
  onAddScene: () => void
}

export default function LeftSidebar({
  scenes,
  activeSceneId,
  onSceneSelect,
  onAddScene,
}: LeftSidebarProps) {
  return (
    <aside className="fixed left-0 top-[70px] bottom-0 w-20 bg-surface-dark border-r border-neon-cyan/20
                      shadow-neon-cyan overflow-y-auto">
      <div className="flex flex-col items-center gap-4 py-6">
        {/* Add Scene Button */}
        <button
          onClick={onAddScene}
          className="w-12 h-12 rounded-lg bg-neon-cyan/10 border-2 border-neon-cyan
                   text-neon-cyan hover:bg-neon-cyan hover:text-space-dark
                   transition-all shadow-neon-cyan hover:scale-110 active:scale-95
                   flex items-center justify-center text-2xl font-bold"
          title="Add Scene"
        >
          +
        </button>

        {/* Divider */}
        <div className="w-8 h-px bg-neon-cyan/20" />

        {/* Scene Buttons */}
        {scenes.map((scene, index) => (
          <button
            key={scene.id}
            onClick={() => onSceneSelect(scene.id)}
            className={`w-12 h-12 rounded-lg border-2 flex items-center justify-center
                       transition-all font-semibold text-sm
                       ${
                         activeSceneId === scene.id
                           ? 'bg-neon-cyan text-space-dark border-neon-cyan shadow-neon-cyan scale-110'
                           : 'bg-surface-light text-text-secondary border-neon-cyan/30 hover:border-neon-cyan hover:text-neon-cyan hover:scale-105'
                       }`}
            title={scene.name}
          >
            {index + 1}
          </button>
        ))}
      </div>
    </aside>
  )
}
