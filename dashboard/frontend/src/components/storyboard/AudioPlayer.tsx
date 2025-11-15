import type { AudioTrack } from '../../types/storyboard';
import { useState } from 'react';

interface AudioPlayerProps {
  track: AudioTrack;
}

export function AudioPlayer({ track }: AudioPlayerProps) {
  // Defensive: Provide defaults for all track properties
  const trackTitle = track?.title ?? 'Untitled Track';
  const trackArtist = track?.artist ?? 'Unknown Artist';
  const trackDuration = track?.duration ?? 0;
  const trackIsPlaying = track?.isPlaying ?? false;
  const trackCurrentTime = track?.currentTime ?? 0;

  const [isPlaying, setIsPlaying] = useState(trackIsPlaying);
  const [currentTime, setCurrentTime] = useState(trackCurrentTime);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const progressPercentage = trackDuration > 0 ? (currentTime / trackDuration) * 100 : 0;

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = (parseFloat(e.target.value) / 100) * trackDuration;
    setCurrentTime(newTime);
  };

  return (
    <div className="audio-player">
      <div className="audio-info">
        <h3 className="track-title">{trackTitle}</h3>
        <p className="track-artist">{trackArtist}</p>
      </div>

      <div className="waveform-container">
        <div className="waveform">
          {Array.from({ length: 60 }).map((_, i) => (
            <div
              key={i}
              className="waveform-bar"
              style={{
                height: `${Math.random() * 60 + 20}%`,
                opacity: i < (progressPercentage / 100 * 60) ? 1 : 0.3,
              }}
            />
          ))}
        </div>
      </div>

      <div className="playback-controls">
        <button className="control-btn" aria-label="Shuffle">🔀</button>
        <button className="control-btn" aria-label="Previous">⏮</button>
        <button className="control-btn play-btn" onClick={handlePlayPause} aria-label={isPlaying ? 'Pause' : 'Play'}>
          {isPlaying ? '⏸' : '▶'}
        </button>
        <button className="control-btn" aria-label="Next">⏭</button>
        <button className="control-btn" aria-label="Repeat">🔁</button>
        <button className="control-btn" aria-label="Settings">⚙️</button>
      </div>

      <div className="progress-container">
        <span className="time-display">{formatTime(currentTime)}</span>
        <input
          type="range"
          min="0"
          max="100"
          value={progressPercentage}
          onChange={handleSeek}
          className="progress-slider"
        />
        <span className="time-display">{formatTime(trackDuration)}</span>
      </div>
    </div>
  );
}
