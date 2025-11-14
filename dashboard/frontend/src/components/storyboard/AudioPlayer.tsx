import { AudioTrack } from '../../types/storyboard';
import { useState } from 'react';

interface AudioPlayerProps {
  track: AudioTrack;
}

export function AudioPlayer({ track }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(track.isPlaying);
  const [currentTime, setCurrentTime] = useState(track.currentTime);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const progressPercentage = (currentTime / track.duration) * 100;

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = (parseFloat(e.target.value) / 100) * track.duration;
    setCurrentTime(newTime);
  };

  return (
    <div className="audio-player">
      <div className="audio-info">
        <h3 className="track-title">{track.title}</h3>
        <p className="track-artist">{track.artist}</p>
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
        <span className="time-display">{formatTime(track.duration)}</span>
      </div>
    </div>
  );
}
