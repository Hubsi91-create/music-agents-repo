export interface Agent {
  id: string
  name: string
  status: string
  icon: string
  quality_score: number
  uptime_percent: number
  avg_response_time_ms: number
  tasks_completed: number
  error_rate: number
}

export interface Activity {
  type: string
  message: string
  timestamp: string
}

export interface DashboardOverview {
  status: string
  timestamp: string
  system_health: {
    overall_score: number
    agents_active: number
    agents_total: number
    uptime_seconds: number
    uptime_percent: number
  }
  quick_stats: {
    training_sessions_today: number
    videos_processed: number
    total_quality_score: number
    active_projects: number
    pending_exports: number
  }
  recent_activity?: Activity[]
}
