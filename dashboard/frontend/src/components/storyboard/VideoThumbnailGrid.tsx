import type { VideoThumbnail } from '../../types/storyboard';
import { ThumbnailCard } from './ThumbnailCard';

interface VideoThumbnailGridProps {
  thumbnails: VideoThumbnail[];
}

export function VideoThumbnailGrid({ thumbnails }: VideoThumbnailGridProps) {
  // Defensive: Handle undefined or empty thumbnails array
  const validThumbnails = thumbnails ?? [];

  return (
    <div className="video-thumbnail-grid">
      <h2 className="grid-title">Video Previews</h2>
      <div className="thumbnail-grid">
        {validThumbnails.length > 0 ? (
          validThumbnails.map(thumbnail => (
            <ThumbnailCard key={thumbnail?.id ?? Math.random()} thumbnail={thumbnail} />
          ))
        ) : (
          <div className="no-thumbnails">
            <p>No video previews available</p>
          </div>
        )}
      </div>
    </div>
  );
}
