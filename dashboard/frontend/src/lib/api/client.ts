import axios, { AxiosInstance, AxiosError } from 'axios'
import type {
  Agent,
  DashboardOverview,
  TrainingStatus,
  SystemHealth,
  MetricsHistory,
  EventLogEntry,
  StoryboardProject,
  ApiResponse,
} from '../types'

// API Base URL from environment or default
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 30000

// Create Axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ error?: string }>) => {
    console.error('API Error:', error.message)
    return Promise.reject(error)
  }
)

// Helper function to handle API responses
const handleResponse = <T>(promise: Promise<any>): Promise<T> => {
  return promise
    .then((response) => response.data)
    .catch((error: AxiosError<{ error?: string }>) => {
      throw new Error(error.response?.data?.error || error.message || 'An error occurred')
    })
}

// ===========================
// Dashboard API Endpoints
// ===========================

/**
 * Get dashboard overview with system status and stats
 */
export const getDashboardOverview = (): Promise<DashboardOverview> => {
  return handleResponse(apiClient.get('/api/dashboard/overview'))
}

/**
 * Get all agents status
 */
export const getAgentsStatus = (): Promise<Agent[]> => {
  return handleResponse(apiClient.get('/api/agents/status'))
}

/**
 * Get specific agent details
 */
export const getAgentDetails = (agentId: string): Promise<Agent> => {
  return handleResponse(apiClient.get(`/api/agents/${agentId}`))
}

/**
 * Get training status
 */
export const getTrainingStatus = (): Promise<TrainingStatus> => {
  return handleResponse(apiClient.get('/api/training/status'))
}

/**
 * Start training process
 */
export const startTraining = (): Promise<ApiResponse<{ message: string }>> => {
  return handleResponse(apiClient.post('/api/training/start'))
}

/**
 * Stop training process
 */
export const stopTraining = (): Promise<ApiResponse<{ message: string }>> => {
  return handleResponse(apiClient.post('/api/training/stop'))
}

/**
 * Get system health metrics
 */
export const getSystemHealth = (): Promise<SystemHealth> => {
  return handleResponse(apiClient.get('/api/system/health'))
}

/**
 * Get metrics history
 */
export const getMetricsHistory = (days: number = 7): Promise<MetricsHistory> => {
  return handleResponse(apiClient.get(`/api/metrics/history?days=${days}`))
}

/**
 * Get recent event logs
 */
export const getRecentLogs = (limit: number = 20): Promise<EventLogEntry[]> => {
  return handleResponse(apiClient.get(`/api/logs/recent?limit=${limit}`))
}

// ===========================
// Storyboard API Endpoints
// ===========================

/**
 * Get all storyboard projects
 */
export const getStoryboardProjects = (): Promise<StoryboardProject[]> => {
  return handleResponse(apiClient.get('/api/storyboard/projects'))
}

/**
 * Get specific storyboard project
 */
export const getStoryboardProject = (projectId: string): Promise<StoryboardProject> => {
  return handleResponse(apiClient.get(`/api/storyboard/project/${projectId}`))
}

/**
 * Create new storyboard project
 */
export const createStoryboardProject = (
  data: Partial<StoryboardProject>
): Promise<StoryboardProject> => {
  return handleResponse(apiClient.post('/api/storyboard/project', data))
}

/**
 * Update storyboard project
 */
export const updateStoryboardProject = (
  projectId: string,
  data: Partial<StoryboardProject>
): Promise<StoryboardProject> => {
  return handleResponse(apiClient.put(`/api/storyboard/project/${projectId}`, data))
}

/**
 * Delete storyboard project
 */
export const deleteStoryboardProject = (
  projectId: string
): Promise<ApiResponse<{ message: string }>> => {
  return handleResponse(apiClient.delete(`/api/storyboard/project/${projectId}`))
}

/**
 * Export storyboard to video
 */
export const exportStoryboard = (
  projectId: string
): Promise<ApiResponse<{ video_url: string }>> => {
  return handleResponse(apiClient.post(`/api/storyboard/export/${projectId}`))
}

// ===========================
// Agent Management Endpoints
// ===========================

/**
 * Deploy specific agent
 */
export const deployAgent = (agentId: string): Promise<ApiResponse<{ message: string }>> => {
  return handleResponse(apiClient.post(`/api/agents/${agentId}/deploy`))
}

/**
 * Stop specific agent
 */
export const stopAgent = (agentId: string): Promise<ApiResponse<{ message: string }>> => {
  return handleResponse(apiClient.post(`/api/agents/${agentId}/stop`))
}

/**
 * Restart specific agent
 */
export const restartAgent = (agentId: string): Promise<ApiResponse<{ message: string }>> => {
  return handleResponse(apiClient.post(`/api/agents/${agentId}/restart`))
}

/**
 * Get agent logs
 */
export const getAgentLogs = (
  agentId: string,
  limit: number = 50
): Promise<EventLogEntry[]> => {
  return handleResponse(apiClient.get(`/api/agents/${agentId}/logs?limit=${limit}`))
}

// ===========================
// Settings & Configuration
// ===========================

/**
 * Get application settings
 */
export const getSettings = (): Promise<any> => {
  return handleResponse(apiClient.get('/api/settings'))
}

/**
 * Update application settings
 */
export const updateSettings = (settings: any): Promise<ApiResponse<{ message: string }>> => {
  return handleResponse(apiClient.put('/api/settings', settings))
}

// ===========================
// Upload & Share
// ===========================

/**
 * Upload video file
 */
export const uploadVideo = (
  file: File,
  onProgress?: (progress: number) => void
): Promise<ApiResponse<{ file_url: string }>> => {
  const formData = new FormData()
  formData.append('file', file)

  return handleResponse(
    apiClient.post('/api/upload/video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(percentCompleted)
        }
      },
    })
  )
}

/**
 * Share video to platforms
 */
export const shareVideo = (
  videoUrl: string,
  platforms: string[]
): Promise<ApiResponse<{ message: string }>> => {
  return handleResponse(
    apiClient.post('/api/share/video', {
      video_url: videoUrl,
      platforms,
    })
  )
}

// ===========================
// Utility Functions
// ===========================

/**
 * Ping API to check connectivity
 */
export const pingApi = (): Promise<{ status: string; timestamp: string }> => {
  return handleResponse(apiClient.get('/api/ping'))
}

/**
 * Get API version
 */
export const getApiVersion = (): Promise<{ version: string }> => {
  return handleResponse(apiClient.get('/api/version'))
}

// Export API client instance for custom requests
export { apiClient }
export default apiClient
