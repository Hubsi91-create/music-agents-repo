'use client'

import React, { useState } from 'react'
import NeonButton from '../ui/NeonButton'
import NeonInput from '../ui/NeonInput'

interface RightPanelProps {
  metadata?: {
    projectName: string
    duration: string
    genre: string
  }
  onMetadataUpdate?: (metadata: any) => void
}

export default function RightPanel({ metadata, onMetadataUpdate }: RightPanelProps) {
  const [showApiKeys, setShowApiKeys] = useState(false)
  const [googleProjectId, setGoogleProjectId] = useState('')
  const [runwayApiKey, setRunwayApiKey] = useState('')
  const [showKeys, setShowKeys] = useState(false)

  return (
    <aside className="fixed right-0 top-[70px] bottom-0 w-80 bg-surface-dark border-l
                      border-neon-cyan/20 shadow-neon-cyan overflow-y-auto">
      <div className="p-6 space-y-6">
        {/* Metadata Section */}
        <section className="card-neon">
          <h3 className="text-lg font-bold text-neon-cyan mb-4 flex items-center gap-2">
            <span>📊</span> Project Metadata
          </h3>
          <div className="space-y-3">
            <div>
              <label className="text-xs text-text-secondary uppercase tracking-wide mb-1 block">
                Project Name
              </label>
              <NeonInput
                value={metadata?.projectName || ''}
                onChange={(value) => onMetadataUpdate?.({ ...metadata, projectName: value })}
                placeholder="Untitled Project"
              />
            </div>
            <div>
              <label className="text-xs text-text-secondary uppercase tracking-wide mb-1 block">
                Duration
              </label>
              <NeonInput
                value={metadata?.duration || ''}
                onChange={(value) => onMetadataUpdate?.({ ...metadata, duration: value })}
                placeholder="3:30"
              />
            </div>
            <div>
              <label className="text-xs text-text-secondary uppercase tracking-wide mb-1 block">
                Genre
              </label>
              <NeonInput
                value={metadata?.genre || ''}
                onChange={(value) => onMetadataUpdate?.({ ...metadata, genre: value })}
                placeholder="Electronic"
              />
            </div>
          </div>
        </section>

        {/* Export & Share */}
        <section className="card-neon">
          <h3 className="text-lg font-bold text-nebula-purple mb-4 flex items-center gap-2">
            <span>📤</span> Export & Share
          </h3>
          <div className="space-y-3">
            <NeonButton variant="purple" size="sm" className="w-full">
              Export to Drive
            </NeonButton>
            <NeonButton variant="cyan" size="sm" className="w-full">
              Generate Preview
            </NeonButton>
            <NeonButton variant="red" size="sm" className="w-full">
              Share Link
            </NeonButton>
          </div>
        </section>

        {/* API Keys Section */}
        <section className="card-neon">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-plasma-yellow flex items-center gap-2">
              <span>🔐</span> API Settings
            </h3>
            <button
              onClick={() => setShowApiKeys(!showApiKeys)}
              className="text-text-secondary hover:text-neon-cyan transition-colors"
            >
              {showApiKeys ? '−' : '+'}
            </button>
          </div>

          {showApiKeys && (
            <div className="space-y-4 animate-[fadeIn_0.3s_ease-in-out]">
              {/* Google Cloud Project ID */}
              <div>
                <label className="text-xs text-text-secondary uppercase tracking-wide mb-2 block">
                  Google Cloud Project ID
                </label>
                <div className="flex gap-2">
                  <NeonInput
                    type={showKeys ? 'text' : 'password'}
                    value={googleProjectId}
                    onChange={setGoogleProjectId}
                    placeholder="project-id-xyz"
                  />
                  <button
                    onClick={() => setShowKeys(!showKeys)}
                    className="px-3 text-text-secondary hover:text-neon-cyan transition-colors"
                    title={showKeys ? 'Hide' : 'Show'}
                  >
                    {showKeys ? '🙈' : '👁️'}
                  </button>
                </div>
              </div>

              {/* Runway API Key */}
              <div>
                <label className="text-xs text-text-secondary uppercase tracking-wide mb-2 block">
                  Runway API Key
                </label>
                <div className="flex gap-2">
                  <NeonInput
                    type={showKeys ? 'text' : 'password'}
                    value={runwayApiKey}
                    onChange={setRunwayApiKey}
                    placeholder="runway-***-***-***"
                  />
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-2 pt-2">
                <NeonButton variant="cyan" size="sm" className="flex-1">
                  Save
                </NeonButton>
                <NeonButton variant="red" size="sm" className="flex-1">
                  Remove
                </NeonButton>
              </div>

              {/* Info */}
              <div className="text-xs text-text-secondary mt-3 p-3 bg-surface-light rounded-lg border border-neon-cyan/10">
                <p className="flex items-start gap-2">
                  <span>ℹ️</span>
                  <span>Keys are encrypted in local storage and never sent to the frontend.</span>
                </p>
              </div>
            </div>
          )}
        </section>

        {/* Quick Tips */}
        <section className="p-4 bg-surface-light rounded-lg border border-nebula-purple/30">
          <h4 className="text-sm font-semibold text-nebula-purple mb-2 flex items-center gap-2">
            <span>💡</span> Quick Tips
          </h4>
          <ul className="text-xs text-text-secondary space-y-2">
            <li className="flex items-start gap-2">
              <span className="text-neon-cyan">•</span>
              <span>Use agents to enhance your prompts before generating</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-neon-cyan">•</span>
              <span>Video generation takes 2-3 minutes on average</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-neon-cyan">•</span>
              <span>Save scenes frequently to avoid losing work</span>
            </li>
          </ul>
        </section>
      </div>
    </aside>
  )
}
