import React, { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import type { Scene } from '@/lib/types'
import styles from '@/styles/components.module.css'

interface TimelineProps {
  scenes: Scene[]
  duration: number
  currentTime?: number
  onSceneClick?: (scene: Scene) => void
  onTimeChange?: (time: number) => void
}

export const Timeline: React.FC<TimelineProps> = ({
  scenes,
  duration,
  currentTime = 0,
  onSceneClick,
  onTimeChange,
}) => {
  const [isDragging, setIsDragging] = useState(false)
  const timelineRef = useRef<HTMLDivElement>(null)

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${String(secs).padStart(2, '0')}`
  }

  const handleTimelineClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!timelineRef.current || !onTimeChange) return

    const rect = timelineRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const percentage = x / rect.width
    const time = percentage * duration

    onTimeChange(Math.max(0, Math.min(time, duration)))
  }

  const handleMouseDown = () => {
    setIsDragging(true)
  }

  const handleMouseUp = () => {
    setIsDragging(false)
  }

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mouseup', handleMouseUp)
      return () => document.removeEventListener('mouseup', handleMouseUp)
    }
  }, [isDragging])

  // Generate time markers
  const timeMarkers = []
  const markerCount = Math.ceil(duration / 10) // Every 10 seconds
  for (let i = 0; i <= markerCount; i++) {
    const time = i * 10
    if (time <= duration) {
      timeMarkers.push(time)
    }
  }

  return (
    <div className="space-y-2">
      {/* Time Markers */}
      <div className="relative h-6 px-2">
        {timeMarkers.map((time) => (
          <div
            key={time}
            className="absolute top-0 text-xs text-text-secondary"
            style={{ left: `${(time / duration) * 100}%` }}
          >
            {formatTime(time)}
          </div>
        ))}
      </div>

      {/* Timeline Track */}
      <div
        ref={timelineRef}
        className={styles.timeline}
        onClick={handleTimelineClick}
      >
        <div className={styles.timelineTrack}>
          {/* Scenes */}
          {scenes.map((scene) => {
            const left = (scene.start_time / duration) * 100
            const width = ((scene.end_time - scene.start_time) / duration) * 100

            return (
              <motion.div
                key={scene.id}
                className={styles.timelineScene}
                style={{
                  left: `${left}%`,
                  width: `${width}%`,
                }}
                onClick={(e) => {
                  e.stopPropagation()
                  onSceneClick?.(scene)
                }}
                whileHover={{ scale: 1.05 }}
              >
                <div className="h-full flex flex-col items-center justify-center px-2">
                  <span className="text-xs font-bold text-neon-cyan truncate w-full text-center">
                    {scene.title}
                  </span>
                  <span className="text-[10px] text-text-secondary">
                    {formatTime(scene.duration)}
                  </span>
                </div>
              </motion.div>
            )
          })}

          {/* Playhead */}
          <motion.div
            className="absolute top-0 bottom-0 w-0.5 bg-neon-red z-10"
            style={{
              left: `${(currentTime / duration) * 100}%`,
              boxShadow: '0 0 10px rgba(255, 23, 68, 0.8)',
            }}
            animate={{ left: `${(currentTime / duration) * 100}%` }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          >
            {/* Playhead Handle */}
            <div
              className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3 h-3 bg-neon-red rounded-full cursor-pointer"
              onMouseDown={handleMouseDown}
              style={{
                boxShadow: '0 0 8px rgba(255, 23, 68, 1)',
              }}
            />
          </motion.div>
        </div>
      </div>

      {/* Current Time Display */}
      <div className="text-center text-xs text-neon-cyan font-semibold">
        {formatTime(currentTime)} / {formatTime(duration)}
      </div>
    </div>
  )
}
