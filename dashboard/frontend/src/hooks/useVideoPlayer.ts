import { useState, useRef, useEffect } from 'react';
import { UseVideoPlayerReturn, PlaybackRate, Quality } from '../types';

/**
 * Custom Hook for Video Player Logic
 *
 * Manages all video player state and controls:
 * - Play/Pause/Seek
 * - Volume control
 * - Playback rate
 * - Quality selection
 * - Fullscreen
 * - Download
 */
export const useVideoPlayer = (): UseVideoPlayerReturn => {
  const videoRef = useRef<HTMLVideoElement>(null);

  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolumeState] = useState(1);
  const [playbackRate, setPlaybackRateState] = useState<PlaybackRate>(1);
  const [selectedQuality, setSelectedQuality] = useState<Quality>('1080p');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isBuffering, setIsBuffering] = useState(false);

  // Video event listeners
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      setCurrentTime(video.currentTime);
    };

    const handleDurationChange = () => {
      setDuration(video.duration);
    };

    const handlePlay = () => {
      setIsPlaying(true);
      setIsBuffering(false);
    };

    const handlePause = () => {
      setIsPlaying(false);
    };

    const handleEnded = () => {
      setIsPlaying(false);
    };

    const handleWaiting = () => {
      setIsBuffering(true);
    };

    const handleCanPlay = () => {
      setIsBuffering(false);
    };

    const handleVolumeChange = () => {
      setVolumeState(video.volume);
    };

    const handleRateChange = () => {
      setPlaybackRateState(video.playbackRate as PlaybackRate);
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('durationchange', handleDurationChange);
    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);
    video.addEventListener('ended', handleEnded);
    video.addEventListener('waiting', handleWaiting);
    video.addEventListener('canplay', handleCanPlay);
    video.addEventListener('volumechange', handleVolumeChange);
    video.addEventListener('ratechange', handleRateChange);

    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('durationchange', handleDurationChange);
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
      video.removeEventListener('ended', handleEnded);
      video.removeEventListener('waiting', handleWaiting);
      video.removeEventListener('canplay', handleCanPlay);
      video.removeEventListener('volumechange', handleVolumeChange);
      video.removeEventListener('ratechange', handleRateChange);
    };
  }, []);

  // Fullscreen change listener
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  // Control functions
  const play = () => {
    videoRef.current?.play();
  };

  const pause = () => {
    videoRef.current?.pause();
  };

  const togglePlay = () => {
    if (isPlaying) {
      pause();
    } else {
      play();
    }
  };

  const seek = (time: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  const setVolume = (level: number) => {
    if (videoRef.current) {
      const clampedVolume = Math.max(0, Math.min(1, level));
      videoRef.current.volume = clampedVolume;
      setVolumeState(clampedVolume);
    }
  };

  const toggleMute = () => {
    if (videoRef.current) {
      if (videoRef.current.volume > 0) {
        videoRef.current.volume = 0;
      } else {
        videoRef.current.volume = 1;
      }
    }
  };

  const setPlaybackRate = (rate: PlaybackRate) => {
    if (videoRef.current) {
      videoRef.current.playbackRate = rate;
      setPlaybackRateState(rate);
    }
  };

  const setQuality = (quality: Quality) => {
    // In a real implementation, this would switch video sources
    // For now, just update the selected quality
    setSelectedQuality(quality);

    // Preserve playback state
    const wasPlaying = isPlaying;
    const currentPosition = currentTime;

    // In real implementation:
    // 1. Pause video
    // 2. Switch source to quality-specific URL
    // 3. Seek to previous position
    // 4. Resume playback if it was playing

    if (videoRef.current) {
      videoRef.current.currentTime = currentPosition;
      if (wasPlaying) {
        videoRef.current.play();
      }
    }
  };

  const toggleFullscreen = async () => {
    const video = videoRef.current;
    if (!video) return;

    try {
      if (!document.fullscreenElement) {
        await video.requestFullscreen();
      } else {
        await document.exitFullscreen();
      }
    } catch (error) {
      console.error('Fullscreen error:', error);
    }
  };

  const download = () => {
    const video = videoRef.current;
    if (!video || !video.src) return;

    // Create a temporary link and trigger download
    const link = document.createElement('a');
    link.href = video.src;
    link.download = 'video.mp4';
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return {
    videoRef,
    isPlaying,
    currentTime,
    duration,
    volume,
    playbackRate,
    selectedQuality,
    isFullscreen,
    isBuffering,
    play,
    pause,
    togglePlay,
    seek,
    setVolume,
    toggleMute,
    setPlaybackRate,
    setQuality,
    toggleFullscreen,
    download
  };
};
