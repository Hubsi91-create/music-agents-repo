/**
 * Retry a function with exponential backoff
 * @param {Function} fn - Async function to retry
 * @param {number} maxRetries - Maximum number of retry attempts
 * @param {number} baseDelay - Base delay in milliseconds (will be doubled each retry)
 * @returns {Promise} - Result of the function
 */
async function retryWithBackoff(fn, maxRetries = 3, baseDelay = 1000) {
  let lastError

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error

      if (attempt === maxRetries) {
        break
      }

      // Calculate delay with exponential backoff
      const delay = baseDelay * Math.pow(2, attempt)

      console.log(`Retry attempt ${attempt + 1}/${maxRetries} after ${delay}ms delay`)
      console.log(`Error: ${error.message}`)

      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }

  throw lastError
}

/**
 * Retry specifically for network errors
 * @param {Function} fn - Async function to retry
 * @param {number} maxRetries - Maximum number of retry attempts
 * @returns {Promise} - Result of the function
 */
async function retryNetworkRequest(fn, maxRetries = 4) {
  return retryWithBackoff(fn, maxRetries, 2000)
}

module.exports = {
  retryWithBackoff,
  retryNetworkRequest,
}
