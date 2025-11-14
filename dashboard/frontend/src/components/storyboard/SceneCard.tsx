import React from 'react'
import { motion } from 'framer-motion'
import { Edit, Trash2, Play } from 'lucide-react'
import type { Scene } from '@/lib/types'
import { Badge } from '@/components/ui/Badge'
import { NeonButton } from '@/components/ui/NeonButton'

interface SceneCardProps {
  scene: Scene
  onEdit?: (scene: Scene) => void
  onDelete?: (sceneId: string) => void
  onPreview?: (scene: Scene) => void
}

export const SceneCard: React.FC<SceneCardProps> = ({
  scene,
  onEdit,
  onDelete,
  onPreview,
}) => {
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${String(secs).padStart(2, '0')}`
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ y: -4 }}
      className="bg-bg-surface/80 border border-neon-cyan/20 rounded-lg overflow-hidden hover:border-neon-cyan/50 hover:shadow-neon-cyan transition-all duration-300"
    >
      {/* Thumbnail */}
      <div className="relative aspect-video bg-bg-primary flex items-center justify-center group cursor-pointer">
        {scene.thumbnail ? (
          <img
            src={scene.thumbnail}
            alt={scene.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="text-4xl">🎬</div>
        )}
        {/* Overlay */}
        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
          <button
            onClick={() => onPreview?.(scene)}
            className="w-12 h-12 rounded-full bg-neon-cyan/20 border-2 border-neon-cyan flex items-center justify-center hover:bg-neon-cyan/30 transition-all"
          >
            <Play size={20} className="text-neon-cyan ml-1" />
          </button>
        </div>
        {/* Duration Badge */}
        <div className="absolute top-2 right-2 bg-black/80 px-2 py-1 rounded text-xs font-semibold text-neon-cyan">
          {formatTime(scene.duration)}
        </div>
      </div>

      {/* Content */}
      <div className="p-4 space-y-3">
        {/* Title & Time */}
        <div>
          <h3 className="text-sm font-bold text-text-primary mb-1">
            {scene.title}
          </h3>
          <p className="text-xs text-text-secondary">
            {formatTime(scene.start_time)} - {formatTime(scene.end_time)}
          </p>
        </div>

        {/* Prompt Preview */}
        <p className="text-xs text-text-secondary truncate-2-lines">
          {scene.prompt}
        </p>

        {/* Style Tags */}
        {scene.style_tags && scene.style_tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {scene.style_tags.slice(0, 3).map((tag, index) => (
              <Badge key={index} variant="info">
                {tag}
              </Badge>
            ))}
            {scene.style_tags.length > 3 && (
              <Badge variant="info">+{scene.style_tags.length - 3}</Badge>
            )}
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center gap-2 pt-2">
          <NeonButton
            variant="purple"
            size="sm"
            onClick={() => onEdit?.(scene)}
            icon={<Edit size={12} />}
            className="flex-1"
          >
            Edit
          </NeonButton>
          <button
            onClick={() => onDelete?.(scene.id)}
            className="p-2 rounded-full border border-neon-red/30 hover:border-neon-red/60 hover:bg-neon-red/10 transition-all"
          >
            <Trash2 size={14} className="text-neon-red" />
          </button>
        </div>
      </div>
    </motion.div>
  )
}
