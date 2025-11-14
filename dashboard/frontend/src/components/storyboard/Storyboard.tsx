import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Plus, Download, Share2 } from 'lucide-react'
import type { StoryboardProject, Scene } from '@/lib/types'
import { Timeline } from './Timeline'
import { SceneCard } from './SceneCard'
import { MusicPreview } from './MusicPreview'
import { NeonCard } from '@/components/ui/NeonCard'
import { NeonButton } from '@/components/ui/NeonButton'
import { Badge } from '@/components/ui/Badge'
import { LoadingSpinner } from '@/components/ui/Spinner'

interface StoryboardProps {
  project?: StoryboardProject | null
  isLoading?: boolean
  onExport?: () => void
  onShare?: () => void
  onAddScene?: () => void
  onEditScene?: (scene: Scene) => void
  onDeleteScene?: (sceneId: string) => void
}

export const Storyboard: React.FC<StoryboardProps> = ({
  project,
  isLoading = false,
  onExport,
  onShare,
  onAddScene,
  onEditScene,
  onDeleteScene,
}) => {
  const [selectedScene, setSelectedScene] = useState<Scene | null>(null)
  const [currentTime, setCurrentTime] = useState(0)

  if (isLoading) {
    return <LoadingSpinner message="Loading storyboard..." />
  }

  if (!project) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="text-6xl mb-4">🎬</div>
        <h2 className="text-2xl font-bold text-text-primary mb-2">
          No Project Loaded
        </h2>
        <p className="text-text-secondary mb-6">
          Create a new storyboard project to get started
        </p>
        <NeonButton variant="cyan" onClick={onAddScene} icon={<Plus size={18} />}>
          Create Project
        </NeonButton>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Project Header */}
      <NeonCard hoverable={false}>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-2xl font-bold text-gradient-cyan">
                {project.title}
              </h1>
              <Badge variant="success">{project.total_scenes} Scenes</Badge>
            </div>
            <p className="text-sm text-text-secondary mb-3">{project.artist}</p>
            <div className="flex items-center gap-4 text-xs text-text-secondary">
              <span>Duration: {Math.floor(project.duration / 60)}:{String(project.duration % 60).padStart(2, '0')}</span>
              {project.genre && <span>Genre: {project.genre}</span>}
              <span>Updated: {new Date(project.updated_at).toLocaleDateString()}</span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <NeonButton
              variant="purple"
              size="sm"
              onClick={onExport}
              icon={<Download size={14} />}
            >
              Export
            </NeonButton>
            <NeonButton
              variant="cyan"
              size="sm"
              onClick={onShare}
              icon={<Share2 size={14} />}
            >
              Share
            </NeonButton>
          </div>
        </div>
      </NeonCard>

      {/* Timeline */}
      <NeonCard hoverable={false}>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-text-primary">Timeline</h2>
            <NeonButton
              variant="cyan"
              size="sm"
              onClick={onAddScene}
              icon={<Plus size={14} />}
            >
              Add Scene
            </NeonButton>
          </div>
          <Timeline
            scenes={project.scenes}
            duration={project.duration}
            currentTime={currentTime}
            onSceneClick={setSelectedScene}
            onTimeChange={setCurrentTime}
          />
        </div>
      </NeonCard>

      {/* Music Preview */}
      {project.music_url && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <MusicPreview
            audioUrl={project.music_url}
            bpm={project.bpm}
            genre={project.genre}
            duration={project.duration}
          />
        </motion.div>
      )}

      {/* Scene Cards Grid */}
      <div>
        <h2 className="text-lg font-bold text-text-primary mb-4">
          All Scenes ({project.scenes.length})
        </h2>
        {project.scenes.length === 0 ? (
          <NeonCard hoverable={false}>
            <div className="text-center py-12">
              <div className="text-5xl mb-4">🎞️</div>
              <p className="text-text-secondary mb-4">No scenes yet</p>
              <NeonButton variant="cyan" onClick={onAddScene} icon={<Plus size={18} />}>
                Add First Scene
              </NeonButton>
            </div>
          </NeonCard>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {project.scenes.map((scene, index) => (
              <motion.div
                key={scene.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <SceneCard
                  scene={scene}
                  onEdit={onEditScene}
                  onDelete={onDeleteScene}
                  onPreview={setSelectedScene}
                />
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Selected Scene Details (Optional) */}
      {selectedScene && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <NeonCard hoverable={false}>
            <div className="flex items-start justify-between mb-4">
              <h2 className="text-lg font-bold text-text-primary">
                Scene Details: {selectedScene.title}
              </h2>
              <button
                onClick={() => setSelectedScene(null)}
                className="text-text-secondary hover:text-neon-cyan"
              >
                ✕
              </button>
            </div>
            <div className="space-y-3">
              <div>
                <p className="text-xs text-text-secondary mb-1">Prompt:</p>
                <p className="text-sm text-text-primary">{selectedScene.prompt}</p>
              </div>
              {selectedScene.style_tags && selectedScene.style_tags.length > 0 && (
                <div>
                  <p className="text-xs text-text-secondary mb-2">Style Tags:</p>
                  <div className="flex flex-wrap gap-1">
                    {selectedScene.style_tags.map((tag, index) => (
                      <Badge key={index} variant="info">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </NeonCard>
        </motion.div>
      )}
    </div>
  )
}
