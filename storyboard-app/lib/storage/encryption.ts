import crypto from 'crypto'

const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || 'your-32-character-encryption-key-change-this-to-32-chars'
const ALGORITHM = 'aes-256-gcm'
const IV_LENGTH = 16
const SALT_LENGTH = 64
const TAG_LENGTH = 16
const ITERATIONS = 100000

/**
 * Encrypt a value using AES-256-GCM
 */
export function encrypt(text: string): string {
  try {
    // Generate random IV
    const iv = crypto.randomBytes(IV_LENGTH)

    // Derive key from password
    const salt = crypto.randomBytes(SALT_LENGTH)
    const key = crypto.pbkdf2Sync(ENCRYPTION_KEY, salt, ITERATIONS, 32, 'sha512')

    // Create cipher
    const cipher = crypto.createCipheriv(ALGORITHM, key, iv)

    // Encrypt
    let encrypted = cipher.update(text, 'utf8', 'hex')
    encrypted += cipher.final('hex')

    // Get auth tag
    const tag = cipher.getAuthTag()

    // Combine salt + iv + tag + encrypted
    const result = Buffer.concat([salt, iv, tag, Buffer.from(encrypted, 'hex')]).toString('base64')

    return result
  } catch (error) {
    console.error('Encryption error:', error)
    throw new Error('Encryption failed')
  }
}

/**
 * Decrypt a value using AES-256-GCM
 */
export function decrypt(encryptedData: string): string {
  try {
    // Decode base64
    const buffer = Buffer.from(encryptedData, 'base64')

    // Extract components
    const salt = buffer.slice(0, SALT_LENGTH)
    const iv = buffer.slice(SALT_LENGTH, SALT_LENGTH + IV_LENGTH)
    const tag = buffer.slice(SALT_LENGTH + IV_LENGTH, SALT_LENGTH + IV_LENGTH + TAG_LENGTH)
    const encrypted = buffer.slice(SALT_LENGTH + IV_LENGTH + TAG_LENGTH).toString('hex')

    // Derive key from password
    const key = crypto.pbkdf2Sync(ENCRYPTION_KEY, salt, ITERATIONS, 32, 'sha512')

    // Create decipher
    const decipher = crypto.createDecipheriv(ALGORITHM, key, iv)
    decipher.setAuthTag(tag)

    // Decrypt
    let decrypted = decipher.update(encrypted, 'hex', 'utf8')
    decrypted += decipher.final('utf8')

    return decrypted
  } catch (error) {
    console.error('Decryption error:', error)
    throw new Error('Decryption failed')
  }
}

/**
 * Hash a value using SHA-256
 */
export function hash(text: string): string {
  return crypto.createHash('sha256').update(text).digest('hex')
}

/**
 * Validate if a string is properly encrypted
 */
export function isEncrypted(data: string): boolean {
  try {
    const buffer = Buffer.from(data, 'base64')
    return buffer.length > SALT_LENGTH + IV_LENGTH + TAG_LENGTH
  } catch {
    return false
  }
}
