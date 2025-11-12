'use client'

import React from 'react'

export interface Agent {
  id: string
  name: string
  description: string
  icon: string
}

interface AgentSelectorProps {
  agents: Agent[]
  selectedAgent: Agent | null
  onAgentSelect: (agent: Agent) => void
}

export default function AgentSelector({
  agents,
  selectedAgent,
  onAgentSelect,
}: AgentSelectorProps) {
  return (
    <div>
      <label className="text-sm font-medium text-text-secondary mb-2 block">
        🤖 Select Gemini Agent
      </label>
      <select
        value={selectedAgent?.id || ''}
        onChange={(e) => {
          const agent = agents.find((a) => a.id === e.target.value)
          if (agent) onAgentSelect(agent)
        }}
        className="input-neon w-full cursor-pointer"
      >
        <option value="" disabled>
          Choose an agent...
        </option>
        {agents.map((agent) => (
          <option key={agent.id} value={agent.id}>
            {agent.icon} {agent.name}
          </option>
        ))}
      </select>
      {selectedAgent && (
        <p className="text-xs text-text-secondary mt-2 flex items-start gap-2">
          <span>ℹ️</span>
          <span>{selectedAgent.description}</span>
        </p>
      )}
    </div>
  )
}
