import { useState, useCallback, useEffect } from 'react'
import { getDashboardOverview } from '@/lib/api/client'
import type { DashboardOverview } from '@/lib/types'

const POLL_INTERVAL = Number(import.meta.env.VITE_DASHBOARD_POLL_INTERVAL) || 5000

export const useDashboard = () => {
  const [overview, setOverview] = useState<DashboardOverview | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    try {
      setError(null)
      const data = await getDashboardOverview()
      setOverview(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch dashboard data'
      setError(message)
      console.error('Dashboard fetch error:', err)
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Initial fetch
  useEffect(() => {
    refresh()
  }, [refresh])

  // Auto-refresh (only if enabled)
  useEffect(() => {
    const enableAutoRefresh = import.meta.env.VITE_ENABLE_AUTO_REFRESH !== 'false'
    if (!enableAutoRefresh) return

    const interval = setInterval(refresh, POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [refresh])

  return {
    overview,
    isLoading,
    error,
    refresh,
  }
}
