import { useEffect, useState } from 'react'
import { useApi } from '../hooks/useApi'

interface QualityMetrics {
  overall_quality: number
  audio_quality: number
  video_quality: number
  concept_quality: number
  total_videos: number
  avg_processing_time: number
}

export const Metrics: React.FC = () => {
  const [metrics, setMetrics] = useState<QualityMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const { fetchData } = useApi()

  useEffect(() => {
    loadMetrics()
  }, [])

  const loadMetrics = async () => {
    try {
      setLoading(true)
      setError(null)
      const result = await fetchData('/api/metrics/quality')
      setMetrics(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load metrics')
      console.error('Failed to load metrics:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <h2>Loading Metrics...</h2>
        <div className="spinner"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error">
        <h2>Error Loading Metrics</h2>
        <p>{error}</p>
        <button onClick={loadMetrics}>Retry</button>
      </div>
    )
  }

  if (!metrics) return null

  return (
    <div className="metrics">
      <h2>Quality Metrics</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Overall Quality</h3>
          <div className="stat-value">{(metrics.overall_quality * 100).toFixed(1)}%</div>
          <div className="stat-label">System Average</div>
        </div>

        <div className="stat-card">
          <h3>Audio Quality</h3>
          <div className="stat-value">{(metrics.audio_quality * 100).toFixed(1)}%</div>
          <div className="stat-label">Music Production</div>
        </div>

        <div className="stat-card">
          <h3>Video Quality</h3>
          <div className="stat-value">{(metrics.video_quality * 100).toFixed(1)}%</div>
          <div className="stat-label">Visual Content</div>
        </div>

        <div className="stat-card">
          <h3>Concept Quality</h3>
          <div className="stat-value">{(metrics.concept_quality * 100).toFixed(1)}%</div>
          <div className="stat-label">Creative Concept</div>
        </div>

        <div className="stat-card">
          <h3>Total Videos</h3>
          <div className="stat-value">{metrics.total_videos}</div>
          <div className="stat-label">Processed</div>
        </div>

        <div className="stat-card">
          <h3>Processing Time</h3>
          <div className="stat-value">{metrics.avg_processing_time.toFixed(0)}s</div>
          <div className="stat-label">Average</div>
        </div>
      </div>
    </div>
  )
}
