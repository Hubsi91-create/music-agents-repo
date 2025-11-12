'use client'

import React, { useState } from 'react'

interface Agent {
  id: string
  name: string
  description: string
  icon: string
}

interface HeaderProps {
  selectedAgent: Agent | null
  onAgentSelect: (agent: Agent) => void
  agents: Agent[]
}

export default function Header({ selectedAgent, onAgentSelect, agents }: HeaderProps) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 h-[70px] bg-surface-dark border-b border-neon-cyan/20 shadow-neon-cyan">
      <div className="h-full px-6 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold text-neon-cyan text-glow-cyan">
            🎬 Storyboard
          </h1>
          <span className="text-text-secondary text-sm">AI Music Video Production</span>
        </div>

        {/* Navigation */}
        <nav className="flex items-center gap-6">
          <button className="text-text-secondary hover:text-neon-cyan transition-colors">
            Scenes
          </button>
          <button className="text-text-secondary hover:text-neon-cyan transition-colors">
            Library
          </button>
          <button className="text-text-secondary hover:text-neon-cyan transition-colors">
            Export
          </button>
        </nav>

        {/* Agent Selector + Settings */}
        <div className="flex items-center gap-4">
          {/* Agent Selector Dropdown */}
          <div className="relative">
            <button
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="flex items-center gap-2 px-4 py-2 bg-surface-light border border-neon-cyan/30
                       rounded-lg text-text-primary hover:border-neon-cyan transition-all"
            >
              <span className="text-lg">{selectedAgent?.icon || '🤖'}</span>
              <span className="text-sm font-medium">
                {selectedAgent?.name || 'Select Agent'}
              </span>
              <span className="text-neon-cyan">▼</span>
            </button>

            {/* Dropdown Menu */}
            {isDropdownOpen && (
              <div className="absolute top-full right-0 mt-2 w-80 bg-surface-dark border border-neon-cyan/30
                            rounded-lg shadow-neon-cyan overflow-hidden backdrop-neon z-50">
                <div className="p-3 border-b border-neon-cyan/20">
                  <p className="text-xs uppercase tracking-wider text-text-secondary">
                    Select Gemini Agent
                  </p>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  {agents.map((agent) => (
                    <button
                      key={agent.id}
                      onClick={() => {
                        onAgentSelect(agent)
                        setIsDropdownOpen(false)
                      }}
                      className={`w-full px-4 py-3 text-left hover:bg-surface-light transition-colors
                                border-l-2 ${
                                  selectedAgent?.id === agent.id
                                    ? 'border-neon-cyan bg-surface-light'
                                    : 'border-transparent'
                                }`}
                    >
                      <div className="flex items-start gap-3">
                        <span className="text-2xl">{agent.icon}</span>
                        <div className="flex-1">
                          <p className="font-medium text-text-primary">{agent.name}</p>
                          <p className="text-xs text-text-secondary mt-1">
                            {agent.description}
                          </p>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Settings Icon */}
          <button className="p-2 text-text-secondary hover:text-neon-cyan transition-colors">
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
          </button>
        </div>
      </div>
    </header>
  )
}
