const jwt = require('jsonwebtoken')

// Middleware to verify JWT token from cookie
function authMiddleware(req, res, next) {
  try {
    const sessionToken = req.cookies.session

    if (!sessionToken) {
      return res.status(401).json({
        error: 'Authentication required',
        message: 'No session token found',
      })
    }

    const decoded = jwt.verify(sessionToken, process.env.JWT_SECRET)
    req.user = decoded
    next()
  } catch (error) {
    return res.status(401).json({
      error: 'Invalid session',
      message: error.message,
    })
  }
}

// Optional auth middleware (doesn't fail if no token)
function optionalAuthMiddleware(req, res, next) {
  try {
    const sessionToken = req.cookies.session
    if (sessionToken) {
      const decoded = jwt.verify(sessionToken, process.env.JWT_SECRET)
      req.user = decoded
    }
  } catch (error) {
    // Ignore errors, continue without user
  }
  next()
}

module.exports = {
  authMiddleware,
  optionalAuthMiddleware,
}
