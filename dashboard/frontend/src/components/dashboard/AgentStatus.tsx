import React from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import type { Agent } from '@/lib/types'
import { Badge } from '@/components/ui/Badge'
import { AGENT_ICONS } from '@/lib/constants/colors'
import styles from '@/styles/components.module.css'

interface AgentStatusProps {
  agents: Agent[]
  selectedAgent?: string
  onSelectAgent?: (id: string) => void
}

const STATUS_VARIANT = {
  online: 'success' as const,
  idle: 'info' as const,
  training: 'warning' as const,
  error: 'error' as const,
  offline: 'error' as const,
}

export const AgentStatus: React.FC<AgentStatusProps> = ({
  agents,
  selectedAgent,
  onSelectAgent,
}) => {
  const getTrendIcon = (trend: number) => {
    if (trend > 0) return <TrendingUp size={14} className="text-neon-green" />
    if (trend < 0) return <TrendingDown size={14} className="text-neon-red" />
    return <Minus size={14} className="text-text-secondary" />
  }

  const getTimeAgo = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = Math.floor((now.getTime() - date.getTime()) / 1000 / 60)

    if (diff < 1) return 'Just now'
    if (diff < 60) return `${diff}m ago`
    if (diff < 1440) return `${Math.floor(diff / 60)}h ago`
    return `${Math.floor(diff / 1440)}d ago`
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {agents.map((agent, index) => (
        <motion.div
          key={agent.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
          onClick={() => onSelectAgent?.(agent.id)}
          className={`
            ${styles.agentCard}
            ${selectedAgent === agent.id ? styles.active : ''}
          `}
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <span className="text-3xl">
                {AGENT_ICONS[agent.id as keyof typeof AGENT_ICONS] || '🤖'}
              </span>
              <div>
                <h3 className="text-sm font-bold text-text-primary">
                  {agent.name}
                </h3>
                <p className="text-xs text-text-secondary">Agent {agent.id}</p>
              </div>
            </div>
            <Badge variant={STATUS_VARIANT[agent.status]}>
              {agent.status}
            </Badge>
          </div>

          {/* Metrics */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs text-text-secondary">Quality:</span>
              <span className="text-sm font-bold text-neon-cyan">
                {agent.quality_score.toFixed(1)}/10
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-text-secondary">Updated:</span>
              <span className="text-xs text-text-primary">
                {getTimeAgo(agent.last_updated)}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-text-secondary">Processing:</span>
              <span className="text-xs text-text-primary">
                {agent.processing_time.toFixed(1)}s
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-text-secondary">Trend:</span>
              <div className="flex items-center gap-1">
                {getTrendIcon(agent.trend)}
                <span
                  className={`text-xs font-semibold ${
                    agent.trend > 0
                      ? 'text-neon-green'
                      : agent.trend < 0
                        ? 'text-neon-red'
                        : 'text-text-secondary'
                  }`}
                >
                  {agent.trend > 0 ? '+' : ''}
                  {agent.trend.toFixed(1)}%
                </span>
              </div>
            </div>
          </div>

          {/* Quality Bar */}
          <div className="mt-4 w-full h-1.5 bg-neon-cyan/10 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${(agent.quality_score / 10) * 100}%` }}
              transition={{ delay: index * 0.05 + 0.2, duration: 0.5 }}
              className="h-full bg-gradient-to-r from-neon-cyan to-neon-purple"
              style={{
                boxShadow: '0 0 8px rgba(0, 240, 255, 0.6)',
              }}
            />
          </div>
        </motion.div>
      ))}
    </div>
  )
}
