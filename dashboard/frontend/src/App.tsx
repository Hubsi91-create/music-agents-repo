import { useEffect, useState } from 'react'
import './App.css'

interface Agent {
  id: string
  name: string
  status: string
  icon: string
  quality_score: number
  uptime_percent: number
  avg_response_time_ms: number
  tasks_completed: number
  error_rate: number
}

interface Activity {
  type: string
  message: string
  timestamp: string
}

interface DashboardOverview {
  status: string
  timestamp: string
  system_health: {
    overall_score: number
    agents_active: number
    agents_total: number
    uptime_seconds: number
    uptime_percent: number
  }
  quick_stats: {
    training_sessions_today: number
    videos_processed: number
    total_quality_score: number
    active_projects: number
    pending_exports: number
  }
  recent_activity?: Activity[]
}

const API_BASE_URL = 'http://localhost:5000'

function App() {
  const [overview, setOverview] = useState<DashboardOverview | null>(null)
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'overview' | 'agents' | 'training'>('overview')

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch overview
      const overviewRes = await fetch(`${API_BASE_URL}/api/dashboard/overview`)
      if (!overviewRes.ok) throw new Error('Failed to fetch overview')
      const overviewData = await overviewRes.json()
      setOverview(overviewData)

      // Fetch agents
      const agentsRes = await fetch(`${API_BASE_URL}/api/agents/status`)
      if (!agentsRes.ok) throw new Error('Failed to fetch agents')
      const agentsData = await agentsRes.json()
      setAgents(agentsData.agents || [])

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
      console.error('Error fetching dashboard data:', err)
    } finally {
      setLoading(false)
    }
  }

  const formatUptime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours}h ${minutes}m`
  }

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <h2>Loading Music Agents Dashboard...</h2>
          <div className="spinner"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>Error Loading Dashboard</h2>
          <p>{error}</p>
          <button onClick={fetchDashboardData}>Retry</button>
        </div>
      </div>
    )
  }

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
      </nav>

      <main className="content">
        {activeTab === 'overview' && overview && (
          <div className="overview">
            <div className="stats-grid">
              <div className="stat-card">
                <h3>System Health</h3>
                <div className="stat-value">{(overview.system_health.overall_score * 100).toFixed(1)}%</div>
                <div className="stat-label">Overall Score</div>
              </div>

              <div className="stat-card">
                <h3>Agents Active</h3>
                <div className="stat-value">
                  {overview.system_health.agents_active}/{overview.system_health.agents_total}
                </div>
                <div className="stat-label">All Systems Operational</div>
              </div>

              <div className="stat-card">
                <h3>Training Sessions</h3>
                <div className="stat-value">{overview.quick_stats.training_sessions_today}</div>
                <div className="stat-label">Today</div>
              </div>

              <div className="stat-card">
                <h3>Videos Processed</h3>
                <div className="stat-value">{overview.quick_stats.videos_processed}</div>
                <div className="stat-label">Total</div>
              </div>

              <div className="stat-card">
                <h3>Quality Score</h3>
                <div className="stat-value">{(overview.quick_stats.total_quality_score * 100).toFixed(1)}%</div>
                <div className="stat-label">Average Quality</div>
              </div>

              <div className="stat-card">
                <h3>Uptime</h3>
                <div className="stat-value">{formatUptime(overview.system_health.uptime_seconds)}</div>
                <div className="stat-label">{overview.system_health.uptime_percent.toFixed(2)}%</div>
              </div>
            </div>

            <div className="section">
              <h2>Recent Activity</h2>
              <div className="activity-list">
                {overview.recent_activity?.map((activity, idx) => (
                  <div key={idx} className="activity-item">
                    <span className="activity-type">{activity.type}</span>
                    <span className="activity-message">{activity.message}</span>
                    <span className="activity-time">
                      {new Date(activity.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'agents' && (
          <div className="agents">
            <h2>Agent Status</h2>
            <div className="agents-grid">
              {agents.map((agent) => (
                <div key={agent.id} className="agent-card">
                  <div className="agent-header">
                    <span className="agent-icon">{agent.icon}</span>
                    <h3>{agent.name}</h3>
                  </div>
                  <div className="agent-stats">
                    <div className="agent-stat">
                      <span className="label">Status:</span>
                      <span className={`status ${agent.status}`}>{agent.status}</span>
                    </div>
                    <div className="agent-stat">
                      <span className="label">Quality:</span>
                      <span className="value">{(agent.quality_score * 100).toFixed(1)}%</span>
                    </div>
                    <div className="agent-stat">
                      <span className="label">Uptime:</span>
                      <span className="value">{agent.uptime_percent.toFixed(1)}%</span>
                    </div>
                    <div className="agent-stat">
                      <span className="label">Response:</span>
                      <span className="value">{agent.avg_response_time_ms}ms</span>
                    </div>
                    <div className="agent-stat">
                      <span className="label">Tasks:</span>
                      <span className="value">{agent.tasks_completed}</span>
                    </div>
                    <div className="agent-stat">
                      <span className="label">Error Rate:</span>
                      <span className="value">{(agent.error_rate * 100).toFixed(2)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'training' && (
          <div className="training">
            <h2>Training Status</h2>
            <div className="info-box">
              <p>Training pipeline monitoring coming soon...</p>
              <p>Current Status: Ready</p>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <button onClick={fetchDashboardData} className="refresh-btn">
          🔄 Refresh Data
        </button>
        <span className="timestamp">
          Last updated: {overview ? new Date(overview.timestamp).toLocaleString() : 'N/A'}
        </span>
      </footer>
    </div>
  )
}

export default App
