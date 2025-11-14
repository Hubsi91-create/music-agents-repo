// Agent Types
export interface Agent {
  id: string
  name: string
  status: 'online' | 'idle' | 'training' | 'error' | 'offline'
  quality_score: number
  last_updated: string
  processing_time: number
  trend: number
  icon: string
  description?: string
}

// Dashboard Overview
export interface DashboardOverview {
  system_status: 'healthy' | 'warning' | 'error'
  total_agents: number
  active_agents: number
  training_agents: number
  system_quality: number
  last_updated: string
}

// Training Status
export interface TrainingStatus {
  is_training: boolean
  current_phase: string
  current_agent: string | null
  progress: number
  time_remaining: number
  phase_details: {
    phase_number: number
    total_phases: number
    phase_name: string
  }
}

// System Health
export interface SystemHealth {
  cpu_usage: number
  memory_usage: number
  disk_usage: number
  status: 'healthy' | 'warning' | 'critical'
  timestamp: string
}

// Metrics History
export interface MetricsDataPoint {
  timestamp: string
  system_quality: number
  agent_8_quality?: number
  agent_5a_quality?: number
  agent_5b_quality?: number
}

export interface MetricsHistory {
  data: MetricsDataPoint[]
  period: string
}

// Event Log
export type EventType = 'training' | 'error' | 'success' | 'warning' | 'info'

export interface EventLogEntry {
  id: string
  timestamp: string
  type: EventType
  agent_name?: string
  message: string
  details?: string
}

// Storyboard Types
export interface Scene {
  id: string
  title: string
  start_time: number
  end_time: number
  duration: number
  prompt: string
  style_tags: string[]
  thumbnail?: string
  video_url?: string
}

export interface StoryboardProject {
  id: string
  title: string
  artist: string
  duration: number
  total_scenes: number
  scenes: Scene[]
  music_url?: string
  bpm?: number
  genre?: string
  created_at: string
  updated_at: string
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
  error?: string
}

// Settings
export interface Settings {
  api_base_url: string
  dashboard_poll_interval: number
  metrics_poll_interval: number
  enable_animations: boolean
  enable_auto_refresh: boolean
}

// UI Component Props Types
export type NeonColor = 'cyan' | 'red' | 'purple' | 'green' | 'yellow'
export type ButtonSize = 'sm' | 'md' | 'lg'
export type BadgeVariant = 'success' | 'warning' | 'error' | 'info'

// Navigation
export type TabType = 'dashboard' | 'storyboard' | 'settings'

// Upload Progress
export interface UploadProgress {
  is_uploading: boolean
  progress: number
  file_name?: string
  status: 'idle' | 'uploading' | 'processing' | 'complete' | 'error'
  error_message?: string
}
