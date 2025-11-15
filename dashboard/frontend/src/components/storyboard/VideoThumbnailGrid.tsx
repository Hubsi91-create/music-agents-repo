import type { VideoThumbnail } from '../../types/storyboard';
import { ThumbnailCard } from './ThumbnailCard';

interface VideoThumbnailGridProps {
  thumbnails: VideoThumbnail[];
}

export function VideoThumbnailGrid({ thumbnails }: VideoThumbnailGridProps) {
  return (
    <div className="video-thumbnail-grid">
      <h2 className="grid-title">Video Previews</h2>
      <div className="thumbnail-grid">
        {thumbnails.map(thumbnail => (
          <ThumbnailCard key={thumbnail.id} thumbnail={thumbnail} />
        ))}
      </div>
    </div>
  );
}
