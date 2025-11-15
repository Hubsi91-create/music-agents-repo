import type { VideoThumbnail } from '../../types/storyboard';

interface ThumbnailCardProps {
  thumbnail: VideoThumbnail;
}

export function ThumbnailCard({ thumbnail }: ThumbnailCardProps) {
  // Defensive: Provide defaults for all thumbnail properties
  const gradientColors = thumbnail?.gradientColors ?? ['#3B82F6', '#8B5CF6'];
  const status = thumbnail?.status ?? 'ready';
  const duration = thumbnail?.duration ?? '0:00';

  return (
    <div className="thumbnail-card">
      <div
        className="thumbnail-image"
        style={{
          background: `linear-gradient(135deg, ${gradientColors[0] ?? '#3B82F6'} 0%, ${gradientColors[1] ?? '#8B5CF6'} 100%)`,
        }}
      >
        {status === 'rendering' && (
          <div className="rendering-overlay">
            <span className="rendering-icon">💧</span>
          </div>
        )}
      </div>
      <div className="thumbnail-info">
        <span className="duration-badge">{duration}</span>
      </div>
    </div>
  );
}
