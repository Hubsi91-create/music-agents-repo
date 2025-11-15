import type { AgentProgress, VideoThumbnail, AudioTrack, Engine, NavItem } from '../types/storyboard';

export const mockAgentProgress: AgentProgress[] = [
  { id: 1, name: 'FanFor Studio', progress: 100, color: '#3B82F6' },
  { id: 2, name: 'Audio Analysis', progress: 85, color: '#3B82F6' },
  { id: 3, name: 'Scene Generation', progress: 80, color: '#3B82F6' },
  { id: 4, name: 'Effect Layering', progress: 60, color: '#3B82F6' },
  { id: 5, name: 'Sync & Timing', progress: 30, color: '#3B82F6' },
  { id: 6, name: 'Final Render', progress: 10, color: '#3B82F6' },
];

export const mockVideoThumbnails: VideoThumbnail[] = [
  { id: 1, duration: '1:0', status: 'rendering', gradientColors: ['#667eea', '#764ba2'] },
  { id: 2, duration: '0:8', status: 'rendering', gradientColors: ['#f093fb', '#f5576c'] },
  { id: 3, duration: '1:0', status: 'rendering', gradientColors: ['#4facfe', '#00f2fe'] },
  { id: 4, duration: '0:8', status: 'rendering', gradientColors: ['#43e97b', '#38f9d7'] },
  { id: 5, duration: '1:0', status: 'rendering', gradientColors: ['#fa709a', '#fee140'] },
  { id: 6, duration: '0:8', status: 'rendering', gradientColors: ['#30cfd0', '#330867'] },
];

export const mockAudioTrack: AudioTrack = {
  title: 'Siwal Syanjolisity',
  artist: 'CosmoSonic',
  duration: 240,
  currentTime: 45,
  isPlaying: false,
};

export const mockEngines: Engine[] = [
  { id: '1', name: 'VisualForge Pro (AI)', type: 'ai' },
  { id: '2', name: 'RenderMax Studio', type: 'traditional' },
  { id: '3', name: 'CreativeSuite AI', type: 'ai' },
  { id: '4', name: 'VideoGen Pro', type: 'ai' },
];

export const mockNavItems: NavItem[] = [
  { id: 'home', label: 'Home', icon: '🏠', type: 'section' },
  { id: 'projects', label: 'Projects', icon: '📁', type: 'section' },
  { id: 'libraries', label: 'Libraris', icon: '📚', type: 'section' }, // Typo intentional
  { id: 'settings', label: 'Settings', icon: '⚙️', type: 'section' },
  { id: 'account', label: 'Account', icon: '👤', type: 'section' },
  { id: 'project1', label: 'Midnight Serenade', icon: '🎵', type: 'project' },
  { id: 'project2', label: 'Electric Dreams', icon: '⚡', type: 'project' },
  { id: 'project3', label: 'Selene Gtulls', icon: '🌙', type: 'project' }, // Typo intentional
];
