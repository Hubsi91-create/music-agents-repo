import React from 'react'
import type { NeonColor, ButtonSize } from '@/lib/types'

interface SpinnerProps {
  size?: ButtonSize
  color?: NeonColor
  className?: string
}

const SIZE_MAP: Record<ButtonSize, string> = {
  sm: 'w-4 h-4 border-2',
  md: 'w-8 h-8 border-3',
  lg: 'w-12 h-12 border-4',
}

const COLOR_MAP: Record<NeonColor, string> = {
  cyan: 'border-neon-cyan/20 border-t-neon-cyan',
  red: 'border-neon-red/20 border-t-neon-red',
  purple: 'border-neon-purple/20 border-t-neon-purple',
  green: 'border-neon-green/20 border-t-neon-green',
  yellow: 'border-neon-yellow/20 border-t-neon-yellow',
}

export const Spinner: React.FC<SpinnerProps> = ({
  size = 'md',
  color = 'cyan',
  className = '',
}) => {
  return (
    <div
      className={`
        rounded-full
        animate-spin
        ${SIZE_MAP[size]}
        ${COLOR_MAP[color]}
        ${className}
      `}
      role="status"
      aria-label="Loading"
    />
  )
}

// Centered spinner with message
interface LoadingSpinnerProps {
  message?: string
  size?: ButtonSize
  color?: NeonColor
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Loading...',
  size = 'lg',
  color = 'cyan',
}) => {
  return (
    <div className="flex flex-col items-center justify-center gap-4 p-8">
      <Spinner size={size} color={color} />
      {message && (
        <p className="text-text-secondary text-sm animate-pulse">{message}</p>
      )}
    </div>
  )
}
