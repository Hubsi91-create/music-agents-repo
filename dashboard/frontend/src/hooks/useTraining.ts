import { useState, useCallback, useEffect } from 'react'
import { getTrainingStatus, startTraining as apiStartTraining, stopTraining as apiStopTraining } from '@/lib/api/client'
import type { TrainingStatus } from '@/lib/types'

const POLL_INTERVAL = 2000 // Poll every 2 seconds during training

export const useTraining = () => {
  const [training, setTraining] = useState<TrainingStatus | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchStatus = useCallback(async () => {
    try {
      setError(null)
      const data = await getTrainingStatus()
      setTraining(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch training status'
      setError(message)
      console.error('Training status fetch error:', err)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const startTraining = useCallback(async () => {
    try {
      setError(null)
      await apiStartTraining()
      await fetchStatus()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to start training'
      setError(message)
      console.error('Start training error:', err)
    }
  }, [fetchStatus])

  const stopTraining = useCallback(async () => {
    try {
      setError(null)
      await apiStopTraining()
      await fetchStatus()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to stop training'
      setError(message)
      console.error('Stop training error:', err)
    }
  }, [fetchStatus])

  // Initial fetch
  useEffect(() => {
    fetchStatus()
  }, [fetchStatus])

  // Poll while training is active
  useEffect(() => {
    if (!training?.is_training) return

    const interval = setInterval(fetchStatus, POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [training?.is_training, fetchStatus])

  return {
    training,
    isLoading,
    error,
    startTraining,
    stopTraining,
    refresh: fetchStatus,
  }
}
