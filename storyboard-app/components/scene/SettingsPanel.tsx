'use client'

import React from 'react'

export interface SceneSettings {
  format: string
  quality: string
  duration: string
  style: string
}

interface SettingsPanelProps {
  settings: SceneSettings
  onSettingsChange: (settings: SceneSettings) => void
}

export default function SettingsPanel({ settings, onSettingsChange }: SettingsPanelProps) {
  const updateSetting = (key: keyof SceneSettings, value: string) => {
    onSettingsChange({ ...settings, [key]: value })
  }

  return (
    <div className="grid grid-cols-2 gap-4 p-4 bg-surface-light rounded-lg border border-neon-cyan/20">
      {/* Format */}
      <div>
        <label className="text-xs text-text-secondary uppercase tracking-wide mb-2 block">
          Format
        </label>
        <select
          value={settings.format}
          onChange={(e) => updateSetting('format', e.target.value)}
          className="input-neon w-full text-sm"
        >
          <option value="mp4">MP4</option>
          <option value="mov">MOV</option>
          <option value="webm">WebM</option>
        </select>
      </div>

      {/* Quality */}
      <div>
        <label className="text-xs text-text-secondary uppercase tracking-wide mb-2 block">
          Quality
        </label>
        <select
          value={settings.quality}
          onChange={(e) => updateSetting('quality', e.target.value)}
          className="input-neon w-full text-sm"
        >
          <option value="720p">720p</option>
          <option value="1080p">1080p</option>
          <option value="4k">4K</option>
          <option value="8k">8K</option>
        </select>
      </div>

      {/* Duration */}
      <div>
        <label className="text-xs text-text-secondary uppercase tracking-wide mb-2 block">
          Duration
        </label>
        <select
          value={settings.duration}
          onChange={(e) => updateSetting('duration', e.target.value)}
          className="input-neon w-full text-sm"
        >
          <option value="10s">10 seconds</option>
          <option value="15s">15 seconds</option>
          <option value="30s">30 seconds</option>
          <option value="60s">60 seconds</option>
        </select>
      </div>

      {/* Style */}
      <div>
        <label className="text-xs text-text-secondary uppercase tracking-wide mb-2 block">
          Style
        </label>
        <select
          value={settings.style}
          onChange={(e) => updateSetting('style', e.target.value)}
          className="input-neon w-full text-sm"
        >
          <option value="cinematic">Cinematic</option>
          <option value="cyberpunk">Cyberpunk</option>
          <option value="realistic">Realistic</option>
          <option value="animated">Animated</option>
          <option value="abstract">Abstract</option>
          <option value="vintage">Vintage</option>
        </select>
      </div>
    </div>
  )
}
