import React, { useState } from 'react'
import { Header } from './components/layout/Header'
import { Sidebar } from './components/layout/Sidebar'
import { RightPanel } from './components/layout/RightPanel'
import { MainContent } from './components/layout/MainContent'
import { DashboardPage } from './pages/DashboardPage'
import { StoryboardPage } from './pages/StoryboardPage'
import { SettingsPage } from './pages/SettingsPage'
import { AppProvider, useAppContext } from './context/AppContext'
import './styles/globals.css'
import './styles/neon-effects.css'

const AppContent: React.FC = () => {
  const { activeTab, setActiveTab, selectedAgent, setSelectedAgent } = useAppContext()
  const [isRefreshing, setIsRefreshing] = useState(false)

  const handleRefresh = async () => {
    setIsRefreshing(true)
    // Refresh is handled by individual hooks with auto-refresh
    setTimeout(() => setIsRefreshing(false), 1000)
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardPage />
      case 'storyboard':
        return <StoryboardPage />
      case 'settings':
        return <SettingsPage />
      default:
        return <DashboardPage />
    }
  }

  return (
    <div className="w-full h-full bg-bg-primary">
      <Header
        activeTab={activeTab}
        onTabChange={setActiveTab}
        onRefresh={handleRefresh}
        isLoading={isRefreshing}
      />

      <Sidebar selectedAgent={selectedAgent || undefined} onSelectAgent={setSelectedAgent} />

      <RightPanel
        metadata={{
          title: 'Sample Track',
          artist: 'AI Generated',
          duration: 180,
          genre: 'Electronic',
        }}
        uploadProgress={{
          isUploading: false,
          progress: 0,
        }}
      />

      <MainContent>{renderContent()}</MainContent>
    </div>
  )
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  )
}

export default App
