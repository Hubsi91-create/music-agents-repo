import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-space-dark">
      <div className="text-center space-y-8 p-8">
        <h1 className="text-6xl font-bold text-glow-cyan text-neon-cyan">
          🎬 Storyboard App
        </h1>
        <p className="text-2xl text-text-secondary max-w-2xl mx-auto">
          AI-Powered Music Video Production with Google Gemini Agent Integration
        </p>
        <div className="flex gap-4 justify-center pt-8">
          <Link href="/storyboard" className="btn-neon-cyan">
            Launch App
          </Link>
          <button className="btn-neon-purple">
            Documentation
          </button>
        </div>
        <div className="mt-12 text-text-secondary text-sm">
          <p>✨ Powered by Google Gemini 2.0 + Runway Gen-4</p>
        </div>
      </div>
    </div>
  )
}
