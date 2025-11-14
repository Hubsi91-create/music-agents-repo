import React from 'react'
import { Dashboard } from '@/components/dashboard/Dashboard'
import { useAppContext } from '@/context/AppContext'

export const DashboardPage: React.FC = () => {
  const { selectedAgent, setSelectedAgent } = useAppContext()

  return (
    <Dashboard
      selectedAgent={selectedAgent || undefined}
      onSelectAgent={setSelectedAgent}
    />
  )
}
