import { encrypt, decrypt, isEncrypted } from './encryption'

export interface ApiKeys {
  googleProjectId?: string
  runwayApiKey?: string
  updatedAt?: string
}

const STORAGE_KEY = 'storyboard_api_keys'

/**
 * Save API keys to localStorage (encrypted)
 */
export function saveApiKeys(keys: ApiKeys): void {
  if (typeof window === 'undefined') {
    throw new Error('saveApiKeys can only be called in browser')
  }

  const encryptedKeys: Record<string, string> = {}

  if (keys.googleProjectId) {
    encryptedKeys.googleProjectId = encrypt(keys.googleProjectId)
  }
  if (keys.runwayApiKey) {
    encryptedKeys.runwayApiKey = encrypt(keys.runwayApiKey)
  }

  encryptedKeys.updatedAt = new Date().toISOString()

  localStorage.setItem(STORAGE_KEY, JSON.stringify(encryptedKeys))
}

/**
 * Load API keys from localStorage (decrypted)
 */
export function loadApiKeys(): ApiKeys | null {
  if (typeof window === 'undefined') {
    return null
  }

  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return null

    const encryptedKeys = JSON.parse(stored)
    const keys: ApiKeys = {}

    if (encryptedKeys.googleProjectId && isEncrypted(encryptedKeys.googleProjectId)) {
      keys.googleProjectId = decrypt(encryptedKeys.googleProjectId)
    }
    if (encryptedKeys.runwayApiKey && isEncrypted(encryptedKeys.runwayApiKey)) {
      keys.runwayApiKey = decrypt(encryptedKeys.runwayApiKey)
    }
    if (encryptedKeys.updatedAt) {
      keys.updatedAt = encryptedKeys.updatedAt
    }

    return keys
  } catch (error) {
    console.error('Error loading API keys:', error)
    return null
  }
}

/**
 * Remove API keys from localStorage
 */
export function removeApiKeys(): void {
  if (typeof window === 'undefined') {
    return
  }

  localStorage.removeItem(STORAGE_KEY)
}

/**
 * Check if API keys are configured
 */
export function hasApiKeys(): boolean {
  const keys = loadApiKeys()
  return !!(keys?.googleProjectId || keys?.runwayApiKey)
}

/**
 * Mask API key for display (show only first and last 4 characters)
 */
export function maskApiKey(key: string): string {
  if (!key || key.length < 8) return '***'
  return `${key.slice(0, 4)}***${key.slice(-4)}`
}
