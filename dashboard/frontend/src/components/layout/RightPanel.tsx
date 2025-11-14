import React from 'react'
import { Settings, Upload, Database } from 'lucide-react'
import { NeonCard } from '@/components/ui/NeonCard'
import { Badge } from '@/components/ui/Badge'
import styles from '@/styles/layout.module.css'

interface RightPanelProps {
  metadata?: {
    title?: string
    artist?: string
    duration?: number
    genre?: string
  }
  uploadProgress?: {
    isUploading: boolean
    progress: number
    fileName?: string
  }
}

export const RightPanel: React.FC<RightPanelProps> = ({
  metadata,
  uploadProgress,
}) => {
  return (
    <aside className={styles.rightPanel}>
      <div className="p-4 space-y-4">
        {/* Metadata Section */}
        <NeonCard hoverable={false}>
          <div className="flex items-center gap-2 mb-4">
            <Database size={18} className="text-neon-cyan" />
            <h3 className="text-sm font-bold uppercase tracking-wide">
              Metadata & Cues
            </h3>
          </div>

          <div className="space-y-3">
            {metadata?.title ? (
              <>
                <div>
                  <p className="text-xs text-text-secondary mb-1">Title</p>
                  <p className="text-sm font-semibold text-text-primary">
                    {metadata.title}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-text-secondary mb-1">Artist</p>
                  <p className="text-sm font-semibold text-text-primary">
                    {metadata.artist || 'Unknown'}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-text-secondary mb-1">Duration</p>
                  <p className="text-sm font-semibold text-text-primary">
                    {metadata.duration
                      ? `${Math.floor(metadata.duration / 60)}:${String(metadata.duration % 60).padStart(2, '0')}`
                      : 'N/A'}
                  </p>
                </div>
                {metadata.genre && (
                  <div>
                    <p className="text-xs text-text-secondary mb-1">Genre</p>
                    <Badge variant="info">{metadata.genre}</Badge>
                  </div>
                )}
              </>
            ) : (
              <p className="text-xs text-text-secondary italic">
                No metadata available
              </p>
            )}
          </div>
        </NeonCard>

        {/* Upload & Share Section */}
        <NeonCard hoverable={false}>
          <div className="flex items-center gap-2 mb-4">
            <Upload size={18} className="text-neon-purple" />
            <h3 className="text-sm font-bold uppercase tracking-wide">
              Upload & Share
            </h3>
          </div>

          {uploadProgress?.isUploading ? (
            <div className="space-y-2">
              <p className="text-xs text-text-secondary">
                {uploadProgress.fileName || 'Uploading...'}
              </p>
              <div className="w-full h-2 bg-neon-purple/10 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-neon-purple to-neon-cyan transition-all duration-300"
                  style={{ width: `${uploadProgress.progress}%` }}
                />
              </div>
              <p className="text-xs text-neon-purple font-semibold">
                {uploadProgress.progress}%
              </p>
            </div>
          ) : (
            <p className="text-xs text-text-secondary italic">
              No active uploads
            </p>
          )}
        </NeonCard>

        {/* Settings Section */}
        <NeonCard hoverable={false}>
          <div className="flex items-center gap-2 mb-4">
            <Settings size={18} className="text-neon-yellow" />
            <h3 className="text-sm font-bold uppercase tracking-wide">
              Quick Settings
            </h3>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs text-text-secondary">Auto-refresh</span>
              <div className="w-10 h-5 bg-neon-cyan/20 rounded-full border border-neon-cyan/50 relative cursor-pointer">
                <div className="absolute right-0.5 top-0.5 w-4 h-4 bg-neon-cyan rounded-full" />
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-text-secondary">Animations</span>
              <div className="w-10 h-5 bg-neon-cyan/20 rounded-full border border-neon-cyan/50 relative cursor-pointer">
                <div className="absolute right-0.5 top-0.5 w-4 h-4 bg-neon-cyan rounded-full" />
              </div>
            </div>
          </div>
        </NeonCard>
      </div>
    </aside>
  )
}
