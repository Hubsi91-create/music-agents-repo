// ═══════════════════════════════════════════════════════════
// TYPE DEFINITIONS - Music Agents Dashboard
// ═══════════════════════════════════════════════════════════

// Video Player Types
export type Quality = '1080p' | '2k' | '4k';
export type PlaybackRate = 0.5 | 0.75 | 1 | 1.25 | 1.5 | 2;
export type SharePlatform = 'twitter' | 'facebook' | 'linkedin' | 'email' | 'copy';

export interface VideoPlayerProps {
  videoUrl: string;
  title: string;
  thumbnail?: string;
  duration?: number;
  onTimeUpdate?: (currentTime: number) => void;
  onPlay?: () => void;
  onPause?: () => void;
  autoPlay?: boolean;
}

export interface VideoControlsProps {
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  volume: number;
  playbackRate: PlaybackRate;
  selectedQuality: Quality;
  onPlayPause: () => void;
  onSeek: (time: number) => void;
  onVolumeChange: (volume: number) => void;
  onPlaybackRateChange: (rate: PlaybackRate) => void;
  onQualityChange: (quality: Quality) => void;
  onFullscreen: () => void;
  onDownload: () => void;
  onShare: (platform: SharePlatform) => void;
}

export interface QualitySelectorProps {
  selectedQuality: Quality;
  qualities: Quality[];
  onSelect: (quality: Quality) => void;
}

export interface PlaybackSpeedProps {
  speed: PlaybackRate;
  onSpeedChange: (speed: PlaybackRate) => void;
}

// Timeline Editor Types
export interface SceneData {
  id: string;
  sceneNumber: number;
  startTime: number;
  duration: number;
  prompt: string;
  style: string;
  agent: string;
  color?: string;
}

export interface TimelineEditorProps {
  projectId: string;
  initialScenes: SceneData[];
  musicDuration: number;
  onScenesChange: (scenes: SceneData[]) => void;
  onSave?: () => Promise<void>;
  onExport?: (format: 'json' | 'runway' | 'veo') => void;
}

export interface TimelineTrackProps {
  scenes: SceneData[];
  selectedSceneId: string | null;
  playheadPosition: number;
  zoomLevel: number;
  totalDuration: number;
  onSceneSelect: (sceneId: string) => void;
  onSceneMove: (sceneId: string, startTime: number) => void;
  onSceneResize: (sceneId: string, duration: number) => void;
  onSeek: (position: number) => void;
  waveformUrl?: string;
}

export interface SceneBlockProps {
  scene: SceneData;
  isSelected: boolean;
  onSelect: () => void;
  onDragStart: (e: React.DragEvent) => void;
  onDragEnd: (e: React.DragEvent) => void;
  onResizeStart: (direction: 'left' | 'right') => (e: React.MouseEvent) => void;
  onDelete: () => void;
  timelineWidth: number;
  totalDuration: number;
}

export interface PlayheadProps {
  position: number;
  timelineWidth: number;
  currentTime: number;
  duration: number;
  onSeek: (position: number) => void;
}

export interface EditorControlsProps {
  isPlaying: boolean;
  zoomLevel: number;
  canUndo: boolean;
  canRedo: boolean;
  onPlay: () => void;
  onPause: () => void;
  onStop: () => void;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onSave: () => void;
  onExport: (format: 'json' | 'runway' | 'veo') => void;
  onDownload: () => void;
  onUndo: () => void;
  onRedo: () => void;
  onDelete: () => void;
}

export interface WaveformDisplayProps {
  audioUrl?: string;
  duration: number;
  height?: number;
  opacity?: number;
}

// Hook Return Types
export interface UseVideoPlayerReturn {
  videoRef: React.RefObject<HTMLVideoElement>;
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  volume: number;
  playbackRate: PlaybackRate;
  selectedQuality: Quality;
  isFullscreen: boolean;
  isBuffering: boolean;
  play: () => void;
  pause: () => void;
  togglePlay: () => void;
  seek: (time: number) => void;
  setVolume: (level: number) => void;
  toggleMute: () => void;
  setPlaybackRate: (rate: PlaybackRate) => void;
  setQuality: (quality: Quality) => void;
  toggleFullscreen: () => void;
  download: () => void;
}

export interface UseTimelineEditorReturn {
  scenes: SceneData[];
  selectedSceneId: string | null;
  playheadPosition: number;
  isPlaying: boolean;
  zoomLevel: number;
  canUndo: boolean;
  canRedo: boolean;
  addScene: (scene: SceneData) => void;
  removeScene: (id: string) => void;
  updateScene: (id: string, updates: Partial<SceneData>) => void;
  moveScene: (id: string, startTime: number) => void;
  resizeScene: (id: string, duration: number) => void;
  selectScene: (id: string) => void;
  playPreview: () => void;
  stopPreview: () => void;
  seek: (position: number) => void;
  undo: () => void;
  redo: () => void;
  saveProject: () => Promise<void>;
  exportProject: (format: 'json' | 'runway' | 'veo') => Promise<void>;
  zoomIn: () => void;
  zoomOut: () => void;
}

// API Types
export interface ProjectData {
  id: string;
  name: string;
  scenes: SceneData[];
  musicUrl?: string;
  musicDuration: number;
  videoUrl?: string;
  createdAt: string;
  updatedAt: string;
}

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}
