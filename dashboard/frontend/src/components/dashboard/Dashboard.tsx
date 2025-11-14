import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { Activity, Zap, TrendingUp } from 'lucide-react'
import { AgentStatus } from './AgentStatus'
import { TrainingMonitor } from './TrainingMonitor'
import { QualityChart } from './QualityChart'
import { SystemHealth } from './SystemHealth'
import { EventLog } from './EventLog'
import { NeonCard } from '@/components/ui/NeonCard'
import { LoadingSpinner } from '@/components/ui/Spinner'
import { useDashboard } from '@/hooks/useDashboard'
import { useAgents } from '@/hooks/useAgents'
import { useTraining } from '@/hooks/useTraining'
import { useMetrics } from '@/hooks/useMetrics'

interface DashboardProps {
  selectedAgent?: string
  onSelectAgent?: (id: string) => void
}

export const Dashboard: React.FC<DashboardProps> = ({
  selectedAgent,
  onSelectAgent,
}) => {
  const { overview, isLoading: overviewLoading, refresh } = useDashboard()
  const { agents, isLoading: agentsLoading } = useAgents()
  const { training, startTraining, stopTraining } = useTraining()
  const { metrics, systemHealth, recentLogs } = useMetrics()

  // Auto-refresh every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      refresh()
    }, 5000)
    return () => clearInterval(interval)
  }, [refresh])

  if (overviewLoading && !overview) {
    return <LoadingSpinner message="Loading dashboard..." />
  }

  return (
    <div className="space-y-6">
      {/* Quick Stats */}
      {overview && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <NeonCard hoverable={false}>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-neon-cyan/20 flex items-center justify-center">
                  <Activity size={24} className="text-neon-cyan" />
                </div>
                <div>
                  <p className="text-xs text-text-secondary mb-1">Active Agents</p>
                  <p className="text-2xl font-bold text-neon-cyan">
                    {overview.active_agents}/{overview.total_agents}
                  </p>
                </div>
              </div>
            </NeonCard>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <NeonCard hoverable={false}>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-neon-purple/20 flex items-center justify-center">
                  <Zap size={24} className="text-neon-purple" />
                </div>
                <div>
                  <p className="text-xs text-text-secondary mb-1">
                    Training Agents
                  </p>
                  <p className="text-2xl font-bold text-neon-purple">
                    {overview.training_agents}
                  </p>
                </div>
              </div>
            </NeonCard>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <NeonCard hoverable={false}>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-neon-green/20 flex items-center justify-center">
                  <TrendingUp size={24} className="text-neon-green" />
                </div>
                <div>
                  <p className="text-xs text-text-secondary mb-1">
                    System Quality
                  </p>
                  <p className="text-2xl font-bold text-neon-green">
                    {overview.system_quality.toFixed(1)}/10
                  </p>
                </div>
              </div>
            </NeonCard>
          </motion.div>
        </div>
      )}

      {/* Agent Grid */}
      {!agentsLoading && agents.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <AgentStatus
            agents={agents}
            selectedAgent={selectedAgent}
            onSelectAgent={onSelectAgent}
          />
        </motion.div>
      )}

      {/* Training Monitor */}
      {training && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <TrainingMonitor
            status={training}
            onStart={startTraining}
            onStop={stopTraining}
          />
        </motion.div>
      )}

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quality Chart */}
        {metrics && metrics.data.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <QualityChart data={metrics.data} />
          </motion.div>
        )}

        {/* System Health */}
        {systemHealth && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
          >
            <SystemHealth health={systemHealth} />
          </motion.div>
        )}
      </div>

      {/* Event Log */}
      {recentLogs && recentLogs.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <EventLog events={recentLogs} />
        </motion.div>
      )}
    </div>
  )
}
