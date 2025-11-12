'use client'

import React from 'react'
import NeonButton from '../ui/NeonButton'

export interface EnhancedPrompt {
  original: string
  enhanced: string
  mood: string
  suggestedStyle: string
  shotSuggestions: string[]
  confidence: number
  reasoning?: string
}

interface EnhancedPromptDisplayProps {
  enhancedPrompt: EnhancedPrompt
  onEdit: () => void
  onRevert: () => void
}

export default function EnhancedPromptDisplay({
  enhancedPrompt,
  onEdit,
  onRevert,
}: EnhancedPromptDisplayProps) {
  return (
    <div className="mb-4 p-4 bg-surface-light rounded-lg border-2 border-success-green/50
                    shadow-[0_0_15px_rgba(0,230,118,0.3)]">
      {/* Header */}
      <div className="flex items-center gap-2 mb-3">
        <span className="text-success-green text-2xl">✅</span>
        <h4 className="text-lg font-bold text-success-green">Agent Enhanced Prompt</h4>
        <span className="ml-auto text-xs text-text-secondary">
          Confidence: {Math.round(enhancedPrompt.confidence * 100)}%
        </span>
      </div>

      {/* Original vs Enhanced */}
      <div className="space-y-3 mb-4">
        <div>
          <p className="text-xs text-text-secondary uppercase tracking-wide mb-1">
            Original Prompt
          </p>
          <p className="text-sm text-text-secondary bg-space-dark p-2 rounded">
            {enhancedPrompt.original}
          </p>
        </div>
        <div>
          <p className="text-xs text-success-green uppercase tracking-wide mb-1 flex items-center gap-1">
            <span>✨</span> Enhanced Prompt
          </p>
          <p className="text-sm text-text-primary bg-space-dark p-3 rounded border border-success-green/30">
            {enhancedPrompt.enhanced}
          </p>
        </div>
      </div>

      {/* Suggestions */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div>
          <p className="text-xs text-text-secondary uppercase tracking-wide mb-1">
            Suggested Style
          </p>
          <div className="flex flex-wrap gap-2">
            {enhancedPrompt.suggestedStyle.split(',').map((style, i) => (
              <span
                key={i}
                className="px-2 py-1 text-xs bg-nebula-purple/20 border border-nebula-purple/40
                         rounded-full text-nebula-purple"
              >
                {style.trim()}
              </span>
            ))}
          </div>
        </div>
        <div>
          <p className="text-xs text-text-secondary uppercase tracking-wide mb-1">
            Mood
          </p>
          <div className="flex flex-wrap gap-2">
            {enhancedPrompt.mood.split(',').map((mood, i) => (
              <span
                key={i}
                className="px-2 py-1 text-xs bg-neon-cyan/20 border border-neon-cyan/40
                         rounded-full text-neon-cyan"
              >
                {mood.trim()}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Shot Suggestions */}
      {enhancedPrompt.shotSuggestions.length > 0 && (
        <div className="mb-4">
          <p className="text-xs text-text-secondary uppercase tracking-wide mb-2">
            Suggested Shots
          </p>
          <div className="flex flex-wrap gap-2">
            {enhancedPrompt.shotSuggestions.map((shot, i) => (
              <span
                key={i}
                className="px-3 py-1 text-xs bg-surface-dark border border-neon-cyan/30
                         rounded-lg text-text-primary"
              >
                {shot}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Reasoning */}
      {enhancedPrompt.reasoning && (
        <div className="mb-4 p-3 bg-space-dark rounded border border-nebula-purple/30">
          <p className="text-xs text-nebula-purple font-medium mb-1">Agent Reasoning</p>
          <p className="text-xs text-text-secondary">{enhancedPrompt.reasoning}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-2">
        <NeonButton variant="green" size="sm" className="flex-1">
          ✅ USE THIS
        </NeonButton>
        <NeonButton variant="cyan" size="sm" onClick={onEdit} className="flex-1">
          ✏️ EDIT
        </NeonButton>
        <NeonButton variant="red" size="sm" onClick={onRevert} className="flex-1">
          ❌ REVERT
        </NeonButton>
      </div>
    </div>
  )
}
