import { useState, useCallback, useEffect } from 'react'
import { getMetricsHistory, getSystemHealth, getRecentLogs } from '@/lib/api/client'
import type { MetricsHistory, SystemHealth, EventLogEntry } from '@/lib/types'

const METRICS_POLL_INTERVAL = Number(import.meta.env.VITE_METRICS_POLL_INTERVAL) || 30000
const LOGS_LIMIT = 20

export const useMetrics = () => {
  const [metrics, setMetrics] = useState<MetricsHistory | null>(null)
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null)
  const [recentLogs, setRecentLogs] = useState<EventLogEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchMetrics = useCallback(async (days: number = 7) => {
    try {
      setError(null)
      const data = await getMetricsHistory(days)
      setMetrics(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch metrics'
      setError(message)
      console.error('Metrics fetch error:', err)
    }
  }, [])

  const fetchSystemHealth = useCallback(async () => {
    try {
      setError(null)
      const data = await getSystemHealth()
      setSystemHealth(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch system health'
      setError(message)
      console.error('System health fetch error:', err)
    }
  }, [])

  const fetchRecentLogs = useCallback(async () => {
    try {
      setError(null)
      const data = await getRecentLogs(LOGS_LIMIT)
      setRecentLogs(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch logs'
      setError(message)
      console.error('Logs fetch error:', err)
    }
  }, [])

  const fetchAll = useCallback(async () => {
    setIsLoading(true)
    await Promise.all([fetchMetrics(), fetchSystemHealth(), fetchRecentLogs()])
    setIsLoading(false)
  }, [fetchMetrics, fetchSystemHealth, fetchRecentLogs])

  // Initial fetch
  useEffect(() => {
    fetchAll()
  }, [fetchAll])

  // Auto-refresh metrics
  useEffect(() => {
    const enableAutoRefresh = import.meta.env.VITE_ENABLE_AUTO_REFRESH !== 'false'
    if (!enableAutoRefresh) return

    const interval = setInterval(fetchAll, METRICS_POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [fetchAll])

  return {
    metrics,
    systemHealth,
    recentLogs,
    isLoading,
    error,
    fetchMetrics,
    fetchSystemHealth,
    fetchRecentLogs,
    refresh: fetchAll,
  }
}
