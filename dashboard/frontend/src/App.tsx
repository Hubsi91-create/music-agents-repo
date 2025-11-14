import { useState } from 'react'
import './App.css'
import { Dashboard } from './components/Dashboard'
import { AgentStatus } from './components/AgentStatus'
import { TrainingStatus } from './components/TrainingStatus'
import { Metrics } from './components/Metrics'

function App() {
  const [activeTab, setActiveTab] = useState<'overview' | 'agents' | 'training' | 'metrics'>('overview')

  return (
    <div className="app">
      <header className="header">
        <h1>🎵 Music Agents Dashboard</h1>
        <p className="subtitle">7-Agent Music Video Production System</p>
      </header>

      <nav className="tabs">
        <button
          className={activeTab === 'overview' ? 'active' : ''}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={activeTab === 'agents' ? 'active' : ''}
          onClick={() => setActiveTab('agents')}
        >
          Agents
        </button>
        <button
          className={activeTab === 'training' ? 'active' : ''}
          onClick={() => setActiveTab('training')}
        >
          Training
        </button>
        <button
          className={activeTab === 'metrics' ? 'active' : ''}
          onClick={() => setActiveTab('metrics')}
        >
          Metrics
        </button>
      </nav>

      <main className="content">
        {activeTab === 'overview' && <Dashboard />}
        {activeTab === 'agents' && <AgentStatus />}
        {activeTab === 'training' && <TrainingStatus />}
        {activeTab === 'metrics' && <Metrics />}
      </main>

      <footer className="footer">
        <span className="timestamp">
          Music Agents Dashboard - 7-Agent Production System
        </span>
      </footer>
    </div>
  )
}

export default App
