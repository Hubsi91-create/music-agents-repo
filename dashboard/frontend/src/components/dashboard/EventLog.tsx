import React from 'react'
import { motion } from 'framer-motion'
import { CheckCircle, XCircle, AlertTriangle, Info } from 'lucide-react'
import type { EventLogEntry, EventType } from '@/lib/types'
import { NeonCard } from '@/components/ui/NeonCard'
import { Badge } from '@/components/ui/Badge'
import styles from '@/styles/components.module.css'

interface EventLogProps {
  events: EventLogEntry[]
  maxHeight?: number
}

const EVENT_ICON: Record<EventType, React.ReactNode> = {
  success: <CheckCircle size={16} className="text-neon-green" />,
  error: <XCircle size={16} className="text-neon-red" />,
  warning: <AlertTriangle size={16} className="text-neon-yellow" />,
  training: <Info size={16} className="text-neon-purple" />,
  info: <Info size={16} className="text-neon-cyan" />,
}

const EVENT_VARIANT: Record<EventType, 'success' | 'error' | 'warning' | 'info'> = {
  success: 'success',
  error: 'error',
  warning: 'warning',
  training: 'warning',
  info: 'info',
}

export const EventLog: React.FC<EventLogProps> = ({ events, maxHeight = 400 }) => {
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { hour12: false })
  }

  return (
    <NeonCard hoverable={false}>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-text-primary">Recent Events</h2>
          <span className="text-xs text-text-secondary">
            Last {events.length} events
          </span>
        </div>

        <div
          className="space-y-2 overflow-y-auto pr-2"
          style={{ maxHeight: `${maxHeight}px` }}
        >
          {events.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-sm text-text-secondary italic">No recent events</p>
            </div>
          ) : (
            events.map((event, index) => (
              <motion.div
                key={event.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.03 }}
                className={`
                  ${styles.eventLogItem}
                  ${event.type === 'training' ? styles.warning : styles[event.type] || ''}
                `}
              >
                {/* Icon */}
                <div className="flex-shrink-0 mt-0.5">
                  {EVENT_ICON[event.type]}
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <Badge variant={EVENT_VARIANT[event.type]}>
                        {event.type}
                      </Badge>
                      {event.agent_name && (
                        <span className="text-xs text-neon-purple font-semibold">
                          {event.agent_name}
                        </span>
                      )}
                    </div>
                    <span className="text-xs text-text-secondary whitespace-nowrap">
                      {formatTime(event.timestamp)}
                    </span>
                  </div>

                  <p className="text-sm text-text-primary">{event.message}</p>

                  {event.details && (
                    <p className="text-xs text-text-secondary mt-1 truncate">
                      {event.details}
                    </p>
                  )}
                </div>
              </motion.div>
            ))
          )}
        </div>
      </div>
    </NeonCard>
  )
}
