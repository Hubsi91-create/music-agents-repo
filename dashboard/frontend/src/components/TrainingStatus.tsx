import { useEffect, useState } from 'react'
import { useApi } from '../hooks/useApi'

interface TrainingData {
  status: string
  iterations: number
  last_run: string | null
  system_ready: boolean
}

export const TrainingStatus: React.FC = () => {
  const [training, setTraining] = useState<TrainingData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const { fetchData } = useApi()

  useEffect(() => {
    loadTrainingStatus()
  }, [])

  const loadTrainingStatus = async () => {
    try {
      setLoading(true)
      setError(null)
      const result = await fetchData('/api/training/status')
      setTraining(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load training status')
      console.error('Failed to load training status:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <h2>Loading Training Status...</h2>
        <div className="spinner"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error">
        <h2>Error Loading Training Status</h2>
        <p>{error}</p>
        <button onClick={loadTrainingStatus}>Retry</button>
      </div>
    )
  }

  if (!training) return null

  return (
    <div className="training">
      <h2>Training Status</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Status</h3>
          <div className="stat-value">{training.status}</div>
          <div className="stat-label">Current State</div>
        </div>

        <div className="stat-card">
          <h3>Iterations</h3>
          <div className="stat-value">{training.iterations}</div>
          <div className="stat-label">Completed</div>
        </div>

        <div className="stat-card">
          <h3>System Ready</h3>
          <div className="stat-value">{training.system_ready ? 'Yes' : 'No'}</div>
          <div className="stat-label">Ready to Train</div>
        </div>

        {training.last_run && (
          <div className="stat-card">
            <h3>Last Run</h3>
            <div className="stat-value">{new Date(training.last_run).toLocaleDateString()}</div>
            <div className="stat-label">{new Date(training.last_run).toLocaleTimeString()}</div>
          </div>
        )}
      </div>

      <div className="info-box">
        <p>Training pipeline monitoring for the 7-agent music video production system.</p>
        <p>Status: {training.system_ready ? 'Ready to start training' : 'System not ready'}</p>
      </div>
    </div>
  )
}
