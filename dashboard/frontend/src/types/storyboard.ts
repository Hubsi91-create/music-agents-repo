// Storyboard types for Music Video Workflow

export interface AgentProgress {
  id: number;
  name: string;
  progress: number;
  color: string;
}

export interface VideoThumbnail {
  id: number;
  duration: string;
  status: string;
  thumbnailUrl?: string;
  gradientColors: string[];
}

export interface AudioTrack {
  title: string;
  artist: string;
  duration: number;
  currentTime: number;
  isPlaying: boolean;
}

export interface Engine {
  id: string;
  name: string;
  type: string;
}

export interface NavItem {
  id: string;
  label: string;
  icon: string;
  type: 'section' | 'project';
}
