import React from 'react'
import { motion } from 'framer-motion'
import { Settings, Zap, Palette, Database } from 'lucide-react'
import { NeonCard } from '@/components/ui/NeonCard'
import { NeonButton } from '@/components/ui/NeonButton'
import { useAppContext } from '@/context/AppContext'

export const SettingsPage: React.FC = () => {
  const { enableAnimations, setEnableAnimations, enableAutoRefresh, setEnableAutoRefresh } =
    useAppContext()

  return (
    <div className="max-w-4xl space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-gradient-cyan mb-2">Settings</h1>
        <p className="text-text-secondary">
          Configure your dashboard preferences and API settings
        </p>
      </motion.div>

      {/* General Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <NeonCard hoverable={false}>
          <div className="space-y-4">
            <div className="flex items-center gap-3 mb-4">
              <Settings size={20} className="text-neon-cyan" />
              <h2 className="text-lg font-bold text-text-primary">
                General Settings
              </h2>
            </div>

            <div className="space-y-4">
              {/* Auto-refresh Toggle */}
              <div className="flex items-center justify-between p-4 bg-bg-primary rounded-lg">
                <div>
                  <h3 className="text-sm font-semibold text-text-primary mb-1">
                    Auto-refresh Data
                  </h3>
                  <p className="text-xs text-text-secondary">
                    Automatically fetch new data every 5 seconds
                  </p>
                </div>
                <button
                  onClick={() => setEnableAutoRefresh(!enableAutoRefresh)}
                  className={`
                    relative w-14 h-7 rounded-full transition-colors duration-300
                    ${enableAutoRefresh ? 'bg-neon-cyan/30 border-neon-cyan' : 'bg-gray-600/30 border-gray-600'}
                    border-2
                  `}
                >
                  <motion.div
                    className={`
                      absolute top-0.5 w-6 h-6 rounded-full
                      ${enableAutoRefresh ? 'bg-neon-cyan' : 'bg-gray-600'}
                    `}
                    animate={{ left: enableAutoRefresh ? '26px' : '2px' }}
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                </button>
              </div>

              {/* Animations Toggle */}
              <div className="flex items-center justify-between p-4 bg-bg-primary rounded-lg">
                <div>
                  <h3 className="text-sm font-semibold text-text-primary mb-1">
                    Enable Animations
                  </h3>
                  <p className="text-xs text-text-secondary">
                    Toggle smooth animations and transitions
                  </p>
                </div>
                <button
                  onClick={() => setEnableAnimations(!enableAnimations)}
                  className={`
                    relative w-14 h-7 rounded-full transition-colors duration-300
                    ${enableAnimations ? 'bg-neon-purple/30 border-neon-purple' : 'bg-gray-600/30 border-gray-600'}
                    border-2
                  `}
                >
                  <motion.div
                    className={`
                      absolute top-0.5 w-6 h-6 rounded-full
                      ${enableAnimations ? 'bg-neon-purple' : 'bg-gray-600'}
                    `}
                    animate={{ left: enableAnimations ? '26px' : '2px' }}
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                </button>
              </div>
            </div>
          </div>
        </NeonCard>
      </motion.div>

      {/* API Configuration */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <NeonCard hoverable={false}>
          <div className="space-y-4">
            <div className="flex items-center gap-3 mb-4">
              <Database size={20} className="text-neon-purple" />
              <h2 className="text-lg font-bold text-text-primary">
                API Configuration
              </h2>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs text-text-secondary mb-1 block">
                  API Base URL
                </label>
                <input
                  type="text"
                  value={import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'}
                  readOnly
                  className="w-full px-4 py-2 bg-bg-primary border border-neon-purple/30 rounded-lg text-sm text-text-primary focus:border-neon-purple/60 focus:outline-none"
                />
              </div>

              <div>
                <label className="text-xs text-text-secondary mb-1 block">
                  Dashboard Poll Interval (ms)
                </label>
                <input
                  type="number"
                  value={import.meta.env.VITE_DASHBOARD_POLL_INTERVAL || 5000}
                  readOnly
                  className="w-full px-4 py-2 bg-bg-primary border border-neon-purple/30 rounded-lg text-sm text-text-primary focus:border-neon-purple/60 focus:outline-none"
                />
              </div>

              <p className="text-xs text-text-secondary italic">
                Note: API settings are configured via environment variables (.env file)
              </p>
            </div>
          </div>
        </NeonCard>
      </motion.div>

      {/* Appearance */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <NeonCard hoverable={false}>
          <div className="space-y-4">
            <div className="flex items-center gap-3 mb-4">
              <Palette size={20} className="text-neon-green" />
              <h2 className="text-lg font-bold text-text-primary">Appearance</h2>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="p-4 bg-bg-primary rounded-lg border border-neon-cyan/50">
                <div className="w-full h-20 bg-gradient-to-br from-neon-cyan to-neon-purple rounded mb-2" />
                <p className="text-xs font-semibold text-center text-neon-cyan">
                  Galaxy Theme (Active)
                </p>
              </div>
              <div className="p-4 bg-bg-primary rounded-lg border border-gray-600/50 opacity-50 cursor-not-allowed">
                <div className="w-full h-20 bg-gradient-to-br from-gray-700 to-gray-900 rounded mb-2" />
                <p className="text-xs font-semibold text-center text-gray-500">
                  Dark Theme (Coming Soon)
                </p>
              </div>
            </div>
          </div>
        </NeonCard>
      </motion.div>

      {/* Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="flex items-center gap-3"
      >
        <NeonButton variant="cyan" icon={<Zap size={16} />}>
          Save Settings
        </NeonButton>
        <NeonButton variant="red">Reset to Defaults</NeonButton>
      </motion.div>
    </div>
  )
}
