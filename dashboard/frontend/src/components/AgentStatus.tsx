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

      // Defensive check: Ensure result and agents array exist
      if (!result || !Array.isArray(result.agents)) {
        console.warn('Invalid response format:', result)
        setAgents([])
        return
      }

      // Transform backend data to match frontend expectations
      const transformedAgents = result.agents.map((agent: any, index: number) => ({
        id: agent.id || agent.name || `agent-${index}`,
        name: agent.name || 'Unknown Agent',
        status: agent.status || 'unknown',
        icon: agent.icon || '🤖',
        quality_score: agent.quality_score ?? agent.health ?? 0.85,
        uptime_percent: agent.uptime_percent ?? 95,
        avg_response_time_ms: agent.avg_response_time_ms ?? 150,
        tasks_completed: agent.tasks_completed ?? 0,
        error_rate: agent.error_rate ?? 0.01
      }))

      setAgents(transformedAgents)
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
        {agents && agents.length > 0 ? (
          agents.map((agent) => (
            <div key={agent.id} className="agent-card">
              <div className="agent-header">
                <span className="agent-icon">{agent.icon || '🤖'}</span>
                <h3>{agent.name || 'Unknown Agent'}</h3>
              </div>
              <div className="agent-stats">
                <div className="agent-stat">
                  <span className="label">Status:</span>
                  <span className={`status ${agent.status || 'unknown'}`}>{agent.status || 'Unknown'}</span>
                </div>
                <div className="agent-stat">
                  <span className="label">Quality:</span>
                  <span className="value">{((agent.quality_score ?? 0) * 100).toFixed(1)}%</span>
                </div>
                <div className="agent-stat">
                  <span className="label">Uptime:</span>
                  <span className="value">{(agent.uptime_percent ?? 0).toFixed(1)}%</span>
                </div>
                <div className="agent-stat">
                  <span className="label">Response:</span>
                  <span className="value">{agent.avg_response_time_ms ?? 0}ms</span>
                </div>
                <div className="agent-stat">
                  <span className="label">Tasks:</span>
                  <span className="value">{agent.tasks_completed ?? 0}</span>
                </div>
                <div className="agent-stat">
                  <span className="label">Error Rate:</span>
                  <span className="value">{((agent.error_rate ?? 0) * 100).toFixed(2)}%</span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="no-agents">
            <p>No agents available</p>
          </div>
        )}
      </div>
    </div>
  )
}
