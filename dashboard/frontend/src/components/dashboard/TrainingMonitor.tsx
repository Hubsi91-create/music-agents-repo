import React from 'react'
import { motion } from 'framer-motion'
import { Play, StopCircle } from 'lucide-react'
import type { TrainingStatus } from '@/lib/types'
import { NeonCard } from '@/components/ui/NeonCard'
import { NeonButton } from '@/components/ui/NeonButton'
import { Badge } from '@/components/ui/Badge'

interface TrainingMonitorProps {
  status: TrainingStatus
  onStart?: () => void
  onStop?: () => void
}

export const TrainingMonitor: React.FC<TrainingMonitorProps> = ({
  status,
  onStart,
  onStop,
}) => {
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${String(secs).padStart(2, '0')}`
  }

  return (
    <NeonCard hoverable={false}>
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h2 className="text-lg font-bold text-text-primary">
              Training Monitor
            </h2>
            <Badge variant={status.is_training ? 'warning' : 'info'}>
              {status.is_training ? 'Training' : 'Idle'}
            </Badge>
          </div>

          <div className="flex items-center gap-2">
            {!status.is_training ? (
              <NeonButton
                variant="green"
                size="sm"
                onClick={onStart}
                icon={<Play size={14} />}
              >
                Start
              </NeonButton>
            ) : (
              <NeonButton
                variant="red"
                size="sm"
                onClick={onStop}
                icon={<StopCircle size={14} />}
              >
                Stop
              </NeonButton>
            )}
          </div>
        </div>

        {status.is_training && (
          <>
            {/* Current Phase */}
            <div>
              <p className="text-xs text-text-secondary mb-1">Current Phase:</p>
              <p className="text-sm font-semibold text-neon-cyan">
                Phase {status.phase_details.phase_number}/
                {status.phase_details.total_phases}:{' '}
                {status.phase_details.phase_name}
              </p>
            </div>

            {/* Current Agent */}
            {status.current_agent && (
              <div>
                <p className="text-xs text-text-secondary mb-1">
                  Current Agent:
                </p>
                <p className="text-sm font-semibold text-neon-purple">
                  Training {status.current_agent}...
                </p>
              </div>
            )}

            {/* Progress Bar */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-text-secondary">Progress</span>
                <span className="text-xs font-bold text-neon-cyan">
                  {Math.round(status.progress)}%
                </span>
              </div>
              <div className="relative w-full h-3 bg-neon-cyan/10 rounded-full overflow-hidden">
                {/* Progress Fill */}
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${status.progress}%` }}
                  transition={{ duration: 0.5 }}
                  className="h-full bg-gradient-to-r from-neon-cyan via-neon-purple to-neon-cyan"
                  style={{
                    boxShadow: '0 0 10px rgba(0, 240, 255, 0.6)',
                  }}
                />
                {/* Shimmer Effect */}
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
                  animate={{
                    x: ['-100%', '200%'],
                  }}
                  transition={{
                    repeat: Infinity,
                    duration: 1.5,
                    ease: 'linear',
                  }}
                />
              </div>
            </div>

            {/* Time Remaining */}
            <div className="flex items-center justify-between pt-2 border-t border-neon-cyan/20">
              <span className="text-xs text-text-secondary">
                Time Remaining:
              </span>
              <span className="text-sm font-bold text-neon-yellow">
                {formatTime(status.time_remaining)}
              </span>
            </div>
          </>
        )}

        {!status.is_training && (
          <div className="text-center py-8">
            <p className="text-sm text-text-secondary italic">
              No active training session
            </p>
          </div>
        )}
      </div>
    </NeonCard>
  )
}
