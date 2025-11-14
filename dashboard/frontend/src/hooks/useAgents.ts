import { useState, useCallback, useEffect } from 'react'
import { getAgentsStatus, getAgentDetails } from '@/lib/api/client'
import type { Agent } from '@/lib/types'

export const useAgents = () => {
  const [agents, setAgents] = useState<Agent[]>([])
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchAgents = useCallback(async () => {
    try {
      setError(null)
      const data = await getAgentsStatus()
      setAgents(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch agents'
      setError(message)
      console.error('Agents fetch error:', err)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const fetchAgentDetails = useCallback(async (agentId: string) => {
    try {
      setError(null)
      const data = await getAgentDetails(agentId)
      // Update the specific agent in the list
      setAgents((prev) =>
        prev.map((agent) => (agent.id === agentId ? data : agent))
      )
      return data
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch agent details'
      setError(message)
      console.error('Agent details fetch error:', err)
      return null
    }
  }, [])

  const selectAgent = useCallback((agentId: string) => {
    setSelectedAgent(agentId)
    fetchAgentDetails(agentId)
  }, [fetchAgentDetails])

  // Initial fetch
  useEffect(() => {
    fetchAgents()
  }, [fetchAgents])

  return {
    agents,
    selectedAgent,
    isLoading,
    error,
    fetchAgents,
    selectAgent,
  }
}
