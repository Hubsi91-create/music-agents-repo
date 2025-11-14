import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { VideoPlayerProps } from '../../types';
import { useVideoPlayer } from '../../hooks/useVideoPlayer';
import VideoControls from './VideoControls';
import styles from './PlayerStyles.module.css';

/**
 * Professional Video Preview Player Component
 *
 * Features:
 * - HTML5 video playback with full controls
 * - Play/Pause, Seek, Volume, Playback Speed
 * - Quality selector (1080p, 2k, 4k)
 * - Fullscreen support
 * - Download and Share functionality
 * - Keyboard shortcuts
 * - Neon-themed UI with smooth animations
 */
const VideoPlayer = ({
  videoUrl,
  title,
  thumbnail,
  duration: initialDuration,
  onTimeUpdate,
  onPlay,
  onPause,
  autoPlay = false
}: VideoPlayerProps) => {
  const {
    videoRef,
    isPlaying,
    currentTime,
    duration,
    volume,
    playbackRate,
    selectedQuality,
    isBuffering,
    play,
    togglePlay,
    seek,
    setVolume,
    toggleMute,
    setPlaybackRate,
    setQuality,
    toggleFullscreen,
    download
  } = useVideoPlayer();

  // Auto-play if requested
  useEffect(() => {
    if (autoPlay && videoRef.current) {
      play();
    }
  }, [autoPlay, videoRef, play]);

  // Notify parent of time updates
  useEffect(() => {
    if (onTimeUpdate) {
      onTimeUpdate(currentTime);
    }
  }, [currentTime, onTimeUpdate]);

  // Notify parent of play/pause events
  useEffect(() => {
    if (isPlaying && onPlay) {
      onPlay();
    } else if (!isPlaying && onPause) {
      onPause();
    }
  }, [isPlaying, onPlay, onPause]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Prevent default only for our shortcuts
      const targetTag = (e.target as HTMLElement).tagName;
      if (targetTag === 'INPUT' || targetTag === 'TEXTAREA') return;

      switch (e.key) {
        case ' ':
          e.preventDefault();
          togglePlay();
          break;
        case 'f':
        case 'F':
          e.preventDefault();
          toggleFullscreen();
          break;
        case 'm':
        case 'M':
          e.preventDefault();
          toggleMute();
          break;
        case 'ArrowRight':
          e.preventDefault();
          seek(Math.min(currentTime + 5, duration));
          break;
        case 'ArrowLeft':
          e.preventDefault();
          seek(Math.max(currentTime - 5, 0));
          break;
        case 'ArrowUp':
          e.preventDefault();
          setVolume(Math.min(volume + 0.1, 1));
          break;
        case 'ArrowDown':
          e.preventDefault();
          setVolume(Math.max(volume - 0.1, 0));
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentTime, duration, volume, togglePlay, seek, setVolume, toggleMute, toggleFullscreen]);

  const handleShare = (platform: string) => {
    const url = window.location.href;
    const text = `Check out this video: ${title}`;

    switch (platform) {
      case 'twitter':
        window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`, '_blank');
        break;
      case 'facebook':
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`, '_blank');
        break;
      case 'linkedin':
        window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`, '_blank');
        break;
      case 'email':
        window.location.href = `mailto:?subject=${encodeURIComponent(title)}&body=${encodeURIComponent(text + ' ' + url)}`;
        break;
      case 'copy':
        navigator.clipboard.writeText(url);
        alert('Link copied to clipboard!');
        break;
    }
  };

  return (
    <motion.div
      className={styles.player}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Video Title */}
      <div className={styles.header}>
        <h2 className={styles.title}>{title}</h2>
      </div>

      {/* Video Container */}
      <div className={styles.videoContainer}>
        <video
          ref={videoRef}
          className={styles.video}
          src={videoUrl}
          poster={thumbnail}
          onClick={togglePlay}
        >
          Your browser does not support the video tag.
        </video>

        {/* Buffering Indicator */}
        {isBuffering && (
          <div className={styles.bufferingOverlay}>
            <div className={styles.spinner}></div>
          </div>
        )}

        {/* Play/Pause Overlay (when paused) */}
        {!isPlaying && !isBuffering && (
          <motion.div
            className={styles.playOverlay}
            onClick={togglePlay}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className={styles.playButton}>
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z" />
              </svg>
            </div>
          </motion.div>
        )}
      </div>

      {/* Video Controls */}
      <VideoControls
        isPlaying={isPlaying}
        currentTime={currentTime}
        duration={duration || initialDuration || 0}
        volume={volume}
        playbackRate={playbackRate}
        selectedQuality={selectedQuality}
        onPlayPause={togglePlay}
        onSeek={seek}
        onVolumeChange={setVolume}
        onPlaybackRateChange={setPlaybackRate}
        onQualityChange={setQuality}
        onFullscreen={toggleFullscreen}
        onDownload={download}
        onShare={handleShare}
      />

      {/* Keyboard Shortcuts Help */}
      <div className={styles.shortcuts}>
        <span>Shortcuts:</span>
        <span>Space: Play/Pause</span>
        <span>F: Fullscreen</span>
        <span>M: Mute</span>
        <span>←/→: Seek ±5s</span>
        <span>↑/↓: Volume</span>
      </div>
    </motion.div>
  );
};

export default VideoPlayer;
