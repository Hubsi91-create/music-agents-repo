import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AGENT_ICONS, AGENT_NAMES } from '@/lib/constants/colors'
import styles from '@/styles/layout.module.css'

interface SidebarProps {
  selectedAgent?: string
  onSelectAgent?: (agentId: string) => void
}

const AGENT_IDS = [
  '1',
  '2',
  '3',
  '4',
  '5a',
  '5b',
  '6',
  '7',
  '8',
  '9',
  '10',
  '11',
  '12',
] as const

export const Sidebar: React.FC<SidebarProps> = ({
  selectedAgent,
  onSelectAgent,
}) => {
  const [hoveredAgent, setHoveredAgent] = useState<string | null>(null)

  return (
    <aside className={styles.sidebar}>
      <div className="py-4 space-y-1">
        {AGENT_IDS.map((agentId) => (
          <div
            key={agentId}
            className="relative"
            onMouseEnter={() => setHoveredAgent(agentId)}
            onMouseLeave={() => setHoveredAgent(null)}
          >
            <button
              onClick={() => onSelectAgent?.(agentId)}
              className={`
                ${styles.sidebarButton}
                ${selectedAgent === agentId ? styles.active : ''}
              `}
            >
              <span className="text-2xl">{AGENT_ICONS[agentId]}</span>
              <span className="text-[10px] font-semibold">
                {agentId.toUpperCase()}
              </span>
            </button>

            {/* Tooltip */}
            <AnimatePresence>
              {hoveredAgent === agentId && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="absolute left-full top-1/2 -translate-y-1/2 ml-4 z-10"
                >
                  <div className="bg-bg-surface border border-neon-cyan/50 rounded-lg px-3 py-2 shadow-neon-cyan whitespace-nowrap">
                    <p className="text-sm font-semibold text-neon-cyan">
                      Agent {agentId}
                    </p>
                    <p className="text-xs text-text-secondary">
                      {AGENT_NAMES[agentId]}
                    </p>
                  </div>
                  {/* Arrow */}
                  <div className="absolute right-full top-1/2 -translate-y-1/2 w-0 h-0 border-t-4 border-t-transparent border-b-4 border-b-transparent border-r-4 border-r-neon-cyan/50" />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </aside>
  )
}
