import React from 'react'
import type { NeonColor, ButtonSize } from '@/lib/types'

interface ProgressRingProps {
  progress: number // 0-100
  size?: ButtonSize
  color?: NeonColor
  showPercentage?: boolean
  strokeWidth?: number
}

const SIZE_MAP: Record<ButtonSize, number> = {
  sm: 60,
  md: 100,
  lg: 140,
}

const COLOR_MAP: Record<NeonColor, string> = {
  cyan: '#00f0ff',
  red: '#ff1744',
  purple: '#b24bf3',
  green: '#00e676',
  yellow: '#ffeb3b',
}

export const ProgressRing: React.FC<ProgressRingProps> = ({
  progress,
  size = 'md',
  color = 'cyan',
  showPercentage = true,
  strokeWidth = 8,
}) => {
  const dimension = SIZE_MAP[size]
  const radius = (dimension - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (progress / 100) * circumference

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={dimension} height={dimension} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={dimension / 2}
          cy={dimension / 2}
          r={radius}
          stroke="rgba(0, 240, 255, 0.1)"
          strokeWidth={strokeWidth}
          fill="none"
        />
        {/* Progress circle */}
        <circle
          cx={dimension / 2}
          cy={dimension / 2}
          r={radius}
          stroke={COLOR_MAP[color]}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-500 ease-out"
          style={{
            filter: `drop-shadow(0 0 8px ${COLOR_MAP[color]})`,
          }}
        />
      </svg>
      {showPercentage && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span
            className="text-2xl font-bold"
            style={{ color: COLOR_MAP[color] }}
          >
            {Math.round(progress)}%
          </span>
        </div>
      )}
    </div>
  )
}
