import React, { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Play, Pause, Volume2, VolumeX } from 'lucide-react'
import { NeonCard } from '@/components/ui/NeonCard'

interface MusicPreviewProps {
  audioUrl?: string
  bpm?: number
  genre?: string
  duration?: number
}

export const MusicPreview: React.FC<MusicPreviewProps> = ({
  audioUrl,
  bpm,
  duration,
}) => {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [volume, setVolume] = useState(1)
  const [isMuted, setIsMuted] = useState(false)
  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const updateTime = () => setCurrentTime(audio.currentTime)
    const handleEnded = () => setIsPlaying(false)

    audio.addEventListener('timeupdate', updateTime)
    audio.addEventListener('ended', handleEnded)

    return () => {
      audio.removeEventListener('timeupdate', updateTime)
      audio.removeEventListener('ended', handleEnded)
    }
  }, [])

  const togglePlay = () => {
    const audio = audioRef.current
    if (!audio) return

    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
    setIsPlaying(!isPlaying)
  }

  const toggleMute = () => {
    const audio = audioRef.current
    if (!audio) return

    audio.muted = !isMuted
    setIsMuted(!isMuted)
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value)
    setVolume(newVolume)
    if (audioRef.current) {
      audioRef.current.volume = newVolume
    }
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = parseFloat(e.target.value)
    setCurrentTime(newTime)
    if (audioRef.current) {
      audioRef.current.currentTime = newTime
    }
  }

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${String(secs).padStart(2, '0')}`
  }

  // Simple waveform visualization (placeholder)
  const waveformBars = Array.from({ length: 50 }, (_, i) => {
    const height = Math.random() * 60 + 20
    const isActive = currentTime > 0 && i < (currentTime / (duration || 1)) * 50
    return { height, isActive }
  })

  return (
    <NeonCard hoverable={false}>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-text-primary">Music Preview</h3>
          {bpm && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-text-secondary">BPM:</span>
              <span className="text-sm font-bold text-neon-purple">{bpm}</span>
            </div>
          )}
        </div>

        {audioUrl ? (
          <>
            {/* Waveform Visualization */}
            <div className="h-24 bg-bg-primary rounded-lg p-2 flex items-end justify-between gap-0.5">
              {waveformBars.map((bar, index) => (
                <motion.div
                  key={index}
                  className="flex-1 rounded-t"
                  style={{
                    height: `${bar.height}%`,
                    backgroundColor: bar.isActive
                      ? '#00f0ff'
                      : 'rgba(0, 240, 255, 0.2)',
                  }}
                  initial={{ height: 0 }}
                  animate={{ height: `${bar.height}%` }}
                  transition={{ delay: index * 0.01 }}
                />
              ))}
            </div>

            {/* Progress Bar */}
            <div className="space-y-1">
              <input
                type="range"
                min="0"
                max={duration || 100}
                step="0.1"
                value={currentTime}
                onChange={handleSeek}
                className="w-full h-1 bg-neon-cyan/20 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:bg-neon-cyan [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:cursor-pointer"
              />
              <div className="flex items-center justify-between text-xs text-text-secondary">
                <span>{formatTime(currentTime)}</span>
                <span>{formatTime(duration || 0)}</span>
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center justify-between">
              {/* Play/Pause */}
              <button
                onClick={togglePlay}
                className="w-10 h-10 rounded-full bg-neon-cyan/20 border-2 border-neon-cyan flex items-center justify-center hover:bg-neon-cyan/30 transition-all"
              >
                {isPlaying ? (
                  <Pause size={18} className="text-neon-cyan" />
                ) : (
                  <Play size={18} className="text-neon-cyan ml-0.5" />
                )}
              </button>

              {/* Volume */}
              <div className="flex items-center gap-2 flex-1 ml-4">
                <button
                  onClick={toggleMute}
                  className="p-1.5 rounded hover:bg-neon-purple/10"
                >
                  {isMuted ? (
                    <VolumeX size={16} className="text-neon-purple" />
                  ) : (
                    <Volume2 size={16} className="text-neon-purple" />
                  )}
                </button>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={volume}
                  onChange={handleVolumeChange}
                  className="flex-1 h-1 bg-neon-purple/20 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-2.5 [&::-webkit-slider-thumb]:h-2.5 [&::-webkit-slider-thumb]:bg-neon-purple [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:cursor-pointer"
                />
              </div>
            </div>

            {/* Hidden Audio Element */}
            <audio ref={audioRef} src={audioUrl} preload="metadata" />
          </>
        ) : (
          <div className="text-center py-8">
            <p className="text-sm text-text-secondary italic">
              No audio available
            </p>
          </div>
        )}
      </div>
    </NeonCard>
  )
}
