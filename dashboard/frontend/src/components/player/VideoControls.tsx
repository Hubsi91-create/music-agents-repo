import { useState } from 'react';
import { motion } from 'framer-motion';
import { VideoControlsProps } from '../../types';
import QualitySelector from './QualitySelector';
import PlaybackSpeed from './PlaybackSpeed';
import styles from './PlayerStyles.module.css';

/**
 * Video Controls Component
 *
 * Full control bar with:
 * - Progress bar (seekable)
 * - Play/Pause button
 * - Time display
 * - Volume slider
 * - Quality selector
 * - Playback speed selector
 * - Download button
 * - Share menu
 * - Fullscreen button
 */
const VideoControls = ({
  isPlaying,
  currentTime,
  duration,
  volume,
  playbackRate,
  selectedQuality,
  onPlayPause,
  onSeek,
  onVolumeChange,
  onPlaybackRateChange,
  onQualityChange,
  onFullscreen,
  onDownload,
  onShare
}: VideoControlsProps) => {
  const [showShareMenu, setShowShareMenu] = useState(false);
  const [isDraggingProgress, setIsDraggingProgress] = useState(false);
  const [isDraggingVolume, setIsDraggingVolume] = useState(false);

  // Format time as MM:SS
  const formatTime = (seconds: number): string => {
    if (!isFinite(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Progress bar handlers
  const handleProgressClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    onSeek(percent * duration);
  };

  const handleProgressMouseDown = () => {
    setIsDraggingProgress(true);
  };

  const handleProgressMouseMove = (e: MouseEvent) => {
    if (!isDraggingProgress) return;
    const progressBar = document.querySelector(`.${styles.progressBar}`) as HTMLDivElement;
    if (!progressBar) return;
    const rect = progressBar.getBoundingClientRect();
    const percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    onSeek(percent * duration);
  };

  const handleProgressMouseUp = () => {
    setIsDraggingProgress(false);
  };

  // Volume slider handlers
  const handleVolumeClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    onVolumeChange(Math.max(0, Math.min(1, percent)));
  };

  const handleVolumeMouseDown = () => {
    setIsDraggingVolume(true);
  };

  const handleVolumeMouseMove = (e: MouseEvent) => {
    if (!isDraggingVolume) return;
    const volumeSlider = document.querySelector(`.${styles.volumeSlider}`) as HTMLDivElement;
    if (!volumeSlider) return;
    const rect = volumeSlider.getBoundingClientRect();
    const percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    onVolumeChange(percent);
  };

  const handleVolumeMouseUp = () => {
    setIsDraggingVolume(false);
  };

  // Mouse event listeners
  useState(() => {
    window.addEventListener('mousemove', handleProgressMouseMove as any);
    window.addEventListener('mouseup', handleProgressMouseUp);
    window.addEventListener('mousemove', handleVolumeMouseMove as any);
    window.addEventListener('mouseup', handleVolumeMouseUp);

    return () => {
      window.removeEventListener('mousemove', handleProgressMouseMove as any);
      window.removeEventListener('mouseup', handleProgressMouseUp);
      window.removeEventListener('mousemove', handleVolumeMouseMove as any);
      window.removeEventListener('mouseup', handleVolumeMouseUp);
    };
  });

  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

  return (
    <div className={styles.controls}>
      {/* Progress Bar */}
      <div
        className={styles.progressBar}
        onClick={handleProgressClick}
        onMouseDown={handleProgressMouseDown}
      >
        <div className={styles.progressTrack}>
          <motion.div
            className={styles.progressFill}
            style={{ width: `${progress}%` }}
            initial={false}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.1 }}
          />
          <motion.div
            className={styles.progressHandle}
            style={{ left: `${progress}%` }}
            whileHover={{ scale: 1.2 }}
            whileTap={{ scale: 1.1 }}
          />
        </div>
      </div>

      {/* Control Buttons Row */}
      <div className={styles.controlsRow}>
        {/* Play/Pause Button */}
        <motion.button
          className={`${styles.button} ${styles.playPauseBtn}`}
          onClick={onPlayPause}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isPlaying ? (
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z" />
            </svg>
          )}
        </motion.button>

        {/* Time Display */}
        <div className={styles.timeDisplay}>
          {formatTime(currentTime)} / {formatTime(duration)}
        </div>

        {/* Quality Selector */}
        <QualitySelector
          selectedQuality={selectedQuality}
          qualities={['1080p', '2k', '4k']}
          onSelect={onQualityChange}
        />

        {/* Playback Speed */}
        <PlaybackSpeed
          speed={playbackRate}
          onSpeedChange={onPlaybackRateChange}
        />

        {/* Volume Control */}
        <div className={styles.volumeControl}>
          <button
            className={styles.button}
            onClick={() => onVolumeChange(volume > 0 ? 0 : 1)}
          >
            {volume === 0 ? (
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z" />
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z" />
              </svg>
            )}
          </button>
          <div
            className={styles.volumeSlider}
            onClick={handleVolumeClick}
            onMouseDown={handleVolumeMouseDown}
          >
            <div className={styles.volumeTrack}>
              <div
                className={styles.volumeFill}
                style={{ width: `${volume * 100}%` }}
              />
            </div>
          </div>
        </div>

        {/* Download Button */}
        <motion.button
          className={`${styles.button} ${styles.downloadBtn}`}
          onClick={onDownload}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z" />
          </svg>
        </motion.button>

        {/* Share Menu */}
        <div className={styles.shareContainer}>
          <motion.button
            className={`${styles.button} ${styles.shareBtn}`}
            onClick={() => setShowShareMenu(!showShareMenu)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z" />
            </svg>
            <span>▼</span>
          </motion.button>

          {showShareMenu && (
            <motion.div
              className={styles.shareMenu}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <button onClick={() => { onShare('twitter'); setShowShareMenu(false); }}>
                Twitter
              </button>
              <button onClick={() => { onShare('facebook'); setShowShareMenu(false); }}>
                Facebook
              </button>
              <button onClick={() => { onShare('linkedin'); setShowShareMenu(false); }}>
                LinkedIn
              </button>
              <button onClick={() => { onShare('email'); setShowShareMenu(false); }}>
                Email
              </button>
              <button onClick={() => { onShare('copy'); setShowShareMenu(false); }}>
                Copy Link
              </button>
            </motion.div>
          )}
        </div>

        {/* Fullscreen Button */}
        <motion.button
          className={`${styles.button} ${styles.fullscreenBtn}`}
          onClick={onFullscreen}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z" />
          </svg>
        </motion.button>
      </div>
    </div>
  );
};

export default VideoControls;
