import { useEffect, useState } from 'react'
import { useApi } from '../hooks/useApi'
import type { DashboardOverview } from '../types'

export const Dashboard: React.FC = () => {
  const [overview, setOverview] = useState<DashboardOverview | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const { fetchData } = useApi()

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      setLoading(true)
      setError(null)
      const result = await fetchData('/api/dashboard/overview')
      setOverview(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dashboard')
      console.error('Failed to load dashboard:', err)
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
      <div className="loading">
        <h2>Loading Dashboard...</h2>
        <div className="spinner"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error">
        <h2>Error Loading Dashboard</h2>
        <p>{error}</p>
        <button onClick={loadDashboard}>Retry</button>
      </div>
    )
  }

  if (!overview) return null

  return (
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
  )
}
