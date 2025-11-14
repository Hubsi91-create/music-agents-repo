/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_TIMEOUT: string
  readonly VITE_DASHBOARD_POLL_INTERVAL: string
  readonly VITE_METRICS_POLL_INTERVAL: string
  readonly VITE_ENABLE_ANIMATIONS: string
  readonly VITE_ENABLE_AUTO_REFRESH: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
