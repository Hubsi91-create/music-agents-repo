const express = require('express')
const { google } = require('googleapis')
const jwt = require('jsonwebtoken')
const router = express.Router()

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URI
)

// Generate authentication URL
router.get('/google', (req, res) => {
  const scopes = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive.file',
    'openid',
    'profile',
    'email',
  ]

  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: scopes,
    prompt: 'consent',
  })

  res.json({ authUrl })
})

// Handle OAuth callback
router.post('/google/callback', async (req, res) => {
  const { code } = req.body

  if (!code) {
    return res.status(400).json({ error: 'Authorization code required' })
  }

  try {
    // Exchange code for tokens
    const { tokens } = await oauth2Client.getToken(code)
    oauth2Client.setCredentials(tokens)

    // Get user info
    const oauth2 = google.oauth2({ version: 'v2', auth: oauth2Client })
    const { data: userInfo } = await oauth2.userinfo.get()

    // Create JWT for session
    const sessionToken = jwt.sign(
      {
        userId: userInfo.id,
        email: userInfo.email,
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
      },
      process.env.JWT_SECRET,
      { expiresIn: '7d' }
    )

    // Set httpOnly cookie
    res.cookie('session', sessionToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
      sameSite: 'strict',
    })

    res.json({
      success: true,
      user: {
        id: userInfo.id,
        email: userInfo.email,
        name: userInfo.name,
        picture: userInfo.picture,
      },
      accessToken: tokens.access_token,
      expiresIn: tokens.expiry_date,
    })
  } catch (error) {
    console.error('OAuth error:', error)
    res.status(500).json({
      error: 'Authentication failed',
      message: error.message,
    })
  }
})

// Refresh access token
router.post('/refresh', async (req, res) => {
  try {
    const sessionToken = req.cookies.session
    if (!sessionToken) {
      return res.status(401).json({ error: 'Not authenticated' })
    }

    const decoded = jwt.verify(sessionToken, process.env.JWT_SECRET)

    oauth2Client.setCredentials({
      refresh_token: decoded.refreshToken,
    })

    const { credentials } = await oauth2Client.refreshAccessToken()

    // Update session token
    const newSessionToken = jwt.sign(
      {
        ...decoded,
        accessToken: credentials.access_token,
      },
      process.env.JWT_SECRET,
      { expiresIn: '7d' }
    )

    res.cookie('session', newSessionToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      maxAge: 7 * 24 * 60 * 60 * 1000,
      sameSite: 'strict',
    })

    res.json({
      success: true,
      accessToken: credentials.access_token,
      expiresIn: credentials.expiry_date,
    })
  } catch (error) {
    console.error('Token refresh error:', error)
    res.status(401).json({
      error: 'Token refresh failed',
      message: error.message,
    })
  }
})

// Logout
router.post('/logout', (req, res) => {
  res.clearCookie('session')
  res.json({ success: true, message: 'Logged out successfully' })
})

// Get current user
router.get('/user', async (req, res) => {
  try {
    const sessionToken = req.cookies.session
    if (!sessionToken) {
      return res.status(401).json({ error: 'Not authenticated' })
    }

    const decoded = jwt.verify(sessionToken, process.env.JWT_SECRET)

    res.json({
      user: {
        userId: decoded.userId,
        email: decoded.email,
      },
    })
  } catch (error) {
    res.status(401).json({ error: 'Invalid session' })
  }
})

module.exports = router
