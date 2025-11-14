import React, { createContext, useContext, ReactNode } from 'react'
import { useLocalStorageState } from '@/hooks/useLocalStorage'
import type { TabType } from '@/lib/types'

interface AppContextType {
  selectedAgent: string | null
  setSelectedAgent: (id: string | null) => void
  activeTab: TabType
  setActiveTab: (tab: TabType) => void
  enableAnimations: boolean
  setEnableAnimations: (enabled: boolean) => void
  enableAutoRefresh: boolean
  setEnableAutoRefresh: (enabled: boolean) => void
}

const AppContext = createContext<AppContextType | undefined>(undefined)

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const {
    selectedAgent,
    setSelectedAgent,
    activeTab,
    setActiveTab,
    enableAnimations,
    setEnableAnimations,
    enableAutoRefresh,
    setEnableAutoRefresh,
  } = useLocalStorageState()

  const value: AppContextType = {
    selectedAgent,
    setSelectedAgent,
    activeTab,
    setActiveTab,
    enableAnimations,
    setEnableAnimations,
    enableAutoRefresh,
    setEnableAutoRefresh,
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export const useAppContext = () => {
  const context = useContext(AppContext)
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider')
  }
  return context
}
