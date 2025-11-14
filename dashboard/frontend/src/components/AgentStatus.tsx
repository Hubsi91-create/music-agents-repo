import { useEffect, useState } from 'react'
import { useApi } from '../hooks/useApi'
import type { Agent } from '../types'

export const AgentStatus: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const { fetchData } = useApi()

  useEffect(() => {
    loadAgents()
  }, [])

  const loadAgents = async () => {
    try {
      setLoading(true)
      setError(null)
      const result = await fetchData('/api/agents/status')
      setAgents(result.agents || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load agents')
      console.error('Failed to load agents:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <h2>Loading Agents...</h2>
        <div className="spinner"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error">
        <h2>Error Loading Agents</h2>
        <p>{error}</p>
        <button onClick={loadAgents}>Retry</button>
      </div>
    )
  }

  return (
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
  )
}
