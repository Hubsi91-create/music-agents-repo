const express = require('express')
const axios = require('axios')
const { retryWithBackoff } = require('../lib/retry')
const router = express.Router()

const RUNWAY_API_URL = process.env.RUNWAY_API_URL || 'https://api.runwayml.com/v1'
const RUNWAY_API_KEY = process.env.RUNWAY_API_KEY

// In-memory task storage (use Redis/DB in production)
const tasks = new Map()

// Generate video
router.post('/generate', async (req, res) => {
  const { sceneId, prompt, format, quality, duration, style } = req.body

  if (!prompt) {
    return res.status(400).json({
      error: 'Missing required field',
      message: 'prompt is required',
    })
  }

  if (!RUNWAY_API_KEY) {
    return res.status(503).json({
      error: 'Runway API not configured',
      message: 'RUNWAY_API_KEY environment variable is not set',
    })
  }

  try {
    // Generate unique task ID
    const taskId = `task-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`

    // Initialize task
    tasks.set(taskId, {
      taskId,
      sceneId,
      status: 'queued',
      progress: 0,
      estimatedTime: 120, // seconds
      createdAt: new Date().toISOString(),
      prompt,
      settings: { format, quality, duration, style },
    })

    // Start generation (async)
    generateVideo(taskId, prompt, { format, quality, duration, style })
      .catch(error => {
        console.error(`Task ${taskId} failed:`, error)
        const task = tasks.get(taskId)
        if (task) {
          task.status = 'failed'
          task.error = error.message
        }
      })

    res.json({
      success: true,
      taskId,
      status: 'queued',
      estimatedTime: 120,
    })
  } catch (error) {
    console.error('Generate video error:', error)
    res.status(500).json({
      error: 'Video generation failed',
      message: error.message,
    })
  }
})

// Get generation status
router.get('/status/:taskId', (req, res) => {
  const { taskId } = req.params
  const task = tasks.get(taskId)

  if (!task) {
    return res.status(404).json({
      error: 'Task not found',
      message: `Task ${taskId} does not exist`,
    })
  }

  res.json({
    taskId: task.taskId,
    status: task.status,
    progress: task.progress,
    estimatedTimeRemaining: Math.max(0, task.estimatedTime - Math.floor((Date.now() - new Date(task.createdAt)) / 1000)),
    videoUrl: task.videoUrl || null,
    error: task.error || null,
  })
})

// Cancel generation
router.delete('/cancel/:taskId', (req, res) => {
  const { taskId } = req.params
  const task = tasks.get(taskId)

  if (!task) {
    return res.status(404).json({ error: 'Task not found' })
  }

  if (task.status === 'completed') {
    return res.status(400).json({ error: 'Cannot cancel completed task' })
  }

  task.status = 'cancelled'
  res.json({ success: true, message: 'Task cancelled' })
})

// Helper: Generate video with Runway API
async function generateVideo(taskId, prompt, settings) {
  const task = tasks.get(taskId)
  if (!task) return

  try {
    task.status = 'generating'
    task.progress = 10

    // Call Runway Gen-4 API with retry logic
    const response = await retryWithBackoff(async () => {
      return await axios.post(
        `${RUNWAY_API_URL}/generations`,
        {
          prompt,
          model: 'gen4',
          duration: parseInt(settings.duration) || 30,
          resolution: settings.quality === '4k' ? '2160p' : settings.quality === '1080p' ? '1080p' : '720p',
          format: settings.format || 'mp4',
          style: settings.style || 'cinematic',
        },
        {
          headers: {
            'Authorization': `Bearer ${RUNWAY_API_KEY}`,
            'Content-Type': 'application/json',
          },
          timeout: 30000,
        }
      )
    }, 4, 2000)

    const generationId = response.data.id
    task.runwayGenerationId = generationId
    task.progress = 30

    // Poll for completion
    let attempts = 0
    const maxAttempts = 90 // 3 minutes (2s intervals)

    while (attempts < maxAttempts) {
      await new Promise(resolve => setTimeout(resolve, 2000))
      attempts++

      try {
        const statusResponse = await axios.get(
          `${RUNWAY_API_URL}/generations/${generationId}`,
          {
            headers: {
              'Authorization': `Bearer ${RUNWAY_API_KEY}`,
            },
            timeout: 10000,
          }
        )

        const status = statusResponse.data
        task.progress = Math.min(95, 30 + (status.progress || 0) * 0.65)

        if (status.status === 'succeeded') {
          task.status = 'completed'
          task.progress = 100
          task.videoUrl = status.output?.url || status.url
          task.completedAt = new Date().toISOString()
          console.log(`✅ Task ${taskId} completed successfully`)
          return
        } else if (status.status === 'failed') {
          throw new Error(status.error || 'Generation failed')
        }
      } catch (pollError) {
        console.warn(`Poll attempt ${attempts} failed:`, pollError.message)
      }
    }

    throw new Error('Generation timed out')
  } catch (error) {
    console.error(`❌ Task ${taskId} failed:`, error)
    task.status = 'failed'
    task.error = error.message
    task.progress = 0
  }
}

module.exports = router
