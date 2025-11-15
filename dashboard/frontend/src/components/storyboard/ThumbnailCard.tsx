import type { VideoThumbnail } from '../../types/storyboard';

interface ThumbnailCardProps {
  thumbnail: VideoThumbnail;
}

export function ThumbnailCard({ thumbnail }: ThumbnailCardProps) {
  return (
    <div className="thumbnail-card">
      <div
        className="thumbnail-image"
        style={{
          background: `linear-gradient(135deg, ${thumbnail.gradientColors[0]} 0%, ${thumbnail.gradientColors[1]} 100%)`,
        }}
      >
        {thumbnail.status === 'rendering' && (
          <div className="rendering-overlay">
            <span className="rendering-icon">💧</span>
          </div>
        )}
      </div>
      <div className="thumbnail-info">
        <span className="duration-badge">{thumbnail.duration}</span>
      </div>
    </div>
  );
}
