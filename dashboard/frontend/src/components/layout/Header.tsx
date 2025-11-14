import React from 'react'
import { motion } from 'framer-motion'
import { RefreshCw, User } from 'lucide-react'
import type { TabType } from '@/lib/types'
import styles from '@/styles/layout.module.css'

interface HeaderProps {
  activeTab: TabType
  onTabChange: (tab: TabType) => void
  onRefresh?: () => void
  isLoading?: boolean
}

const TABS: { id: TabType; label: string }[] = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'storyboard', label: 'Storyboard' },
  { id: 'settings', label: 'Settings' },
]

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  onTabChange,
  onRefresh,
  isLoading = false,
}) => {
  return (
    <header className={styles.header}>
      <div className="h-full px-6 flex items-center justify-between">
        {/* Logo & Brand */}
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-neon-cyan to-neon-purple flex items-center justify-center">
            <span className="text-2xl">🎵</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-gradient-cyan">
              Music Agents
            </h1>
            <p className="text-xs text-text-secondary">
              Production Dashboard
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex gap-2">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`
                relative
                px-6
                py-2
                text-sm
                font-semibold
                uppercase
                tracking-wider
                transition-all
                duration-300
                ${
                  activeTab === tab.id
                    ? 'text-neon-cyan'
                    : 'text-text-secondary hover:text-neon-cyan/70'
                }
              `}
            >
              {tab.label}
              {activeTab === tab.id && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-neon-cyan shadow-neon-cyan"
                  transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                />
              )}
            </button>
          ))}
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-4">
          {/* Refresh Button */}
          <motion.button
            onClick={onRefresh}
            disabled={isLoading}
            className="p-2 rounded-full border border-neon-cyan/30 hover:border-neon-cyan/60 hover:bg-neon-cyan/10 transition-all duration-300"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            <RefreshCw
              size={18}
              className={`text-neon-cyan ${isLoading ? 'animate-spin' : ''}`}
            />
          </motion.button>

          {/* User Icon */}
          <div className="w-8 h-8 rounded-full bg-neon-purple/20 border border-neon-purple/50 flex items-center justify-center">
            <User size={16} className="text-neon-purple" />
          </div>
        </div>
      </div>
    </header>
  )
}
