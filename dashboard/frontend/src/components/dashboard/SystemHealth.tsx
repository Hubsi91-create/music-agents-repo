import React from 'react'
import { motion } from 'framer-motion'
import type { SystemHealth as SystemHealthType } from '@/lib/types'
import { NeonCard } from '@/components/ui/NeonCard'
import { GaugeChart } from '@/components/ui/GaugeChart'

interface SystemHealthProps {
  health: SystemHealthType
}

export const SystemHealth: React.FC<SystemHealthProps> = ({ health }) => {
  return (
    <NeonCard hoverable={false}>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-text-primary">System Health</h2>
          <div className="text-xs text-text-secondary">
            {new Date(health.timestamp).toLocaleTimeString()}
          </div>
        </div>

        <div className="grid grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            <GaugeChart
              value={health.cpu_usage}
              label="CPU Usage"
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <GaugeChart
              value={health.memory_usage}
              label="Memory Usage"
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <GaugeChart
              value={health.disk_usage}
              label="Disk Usage"
            />
          </motion.div>
        </div>
      </div>
    </NeonCard>
  )
}
