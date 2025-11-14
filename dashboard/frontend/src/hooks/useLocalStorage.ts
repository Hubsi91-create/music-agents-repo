import { useState, useCallback } from 'react'

/**
 * Custom hook for managing state with localStorage persistence
 */
export const useLocalStorage = <T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void] => {
  // Get from localStorage or use initial value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error)
      return initialValue
    }
  })

  // Return a wrapped version of useState's setter function that persists to localStorage
  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      try {
        // Allow value to be a function so we have same API as useState
        const valueToStore = value instanceof Function ? value(storedValue) : value

        // Save state
        setStoredValue(valueToStore)

        // Save to localStorage
        window.localStorage.setItem(key, JSON.stringify(valueToStore))
      } catch (error) {
        console.error(`Error setting localStorage key "${key}":`, error)
      }
    },
    [key, storedValue]
  )

  return [storedValue, setValue]
}

/**
 * Hook to manage multiple localStorage keys at once
 */
export const useLocalStorageState = () => {
  const [selectedAgent, setSelectedAgent] = useLocalStorage<string | null>(
    'dashboard_selected_agent',
    null
  )

  const [activeTab, setActiveTab] = useLocalStorage<'dashboard' | 'storyboard' | 'settings'>(
    'dashboard_active_tab',
    'dashboard'
  )

  const [enableAnimations, setEnableAnimations] = useLocalStorage<boolean>(
    'dashboard_enable_animations',
    true
  )

  const [enableAutoRefresh, setEnableAutoRefresh] = useLocalStorage<boolean>(
    'dashboard_enable_auto_refresh',
    true
  )

  return {
    selectedAgent,
    setSelectedAgent,
    activeTab,
    setActiveTab,
    enableAnimations,
    setEnableAnimations,
    enableAutoRefresh,
    setEnableAutoRefresh,
  }
}
