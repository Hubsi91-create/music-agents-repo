import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './index.css'
import App from './App.tsx'

// React Query Client Konfiguration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false, // Verhindert unnötige Requests beim Tab-Wechsel
      retry: 1, // Versucht fehlgeschlagene Requests einmal erneut
      staleTime: 5000, // Daten werden 5 Sekunden als "frisch" betrachtet
    },
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
)
