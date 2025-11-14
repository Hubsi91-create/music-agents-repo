// Theme Colors
export const COLORS = {
  // Background
  BG_PRIMARY: '#0a0e27',
  BG_SURFACE: '#1a1f3a',
  BG_SURFACE_HOVER: '#252b47',

  // Text
  TEXT_PRIMARY: '#e0e8ff',
  TEXT_SECONDARY: '#a0aff0',

  // Neon Colors
  NEON_CYAN: '#00f0ff',
  NEON_RED: '#ff1744',
  NEON_PURPLE: '#b24bf3',
  NEON_GREEN: '#00e676',
  NEON_YELLOW: '#ffeb3b',

  // Status Colors
  SUCCESS: '#00e676',
  WARNING: '#ffeb3b',
  ERROR: '#ff1744',
  INFO: '#00f0ff',
} as const

// Agent Icons (Emoji mapping)
export const AGENT_ICONS = {
  '1': '🔥', // Trend Detective
  '2': '🎚️', // Audio Curator
  '3': '🎬', // Video Concept
  '4': '📝', // Screenplay Generator
  '5a': '🎞️', // Veo Adapter
  '5b': '🎞️', // Runway Adapter
  '6': '👤', // Influencer Matcher
  '7': '📊', // Distribution Metadata
  '8': '✨', // Prompt Refiner
  '9': '🎵', // Sound Designer
  '10': '🚀', // Master Distributor
  '11': '🤖', // Trainer
  '12': '🌐', // Universal Harvester
} as const

// Agent Names
export const AGENT_NAMES = {
  '1': 'Trend Detective',
  '2': 'Audio Curator',
  '3': 'Video Concept',
  '4': 'Screenplay Generator',
  '5a': 'Veo Adapter',
  '5b': 'Runway Adapter',
  '6': 'Influencer Matcher',
  '7': 'Distribution Metadata',
  '8': 'Prompt Refiner',
  '9': 'Sound Designer',
  '10': 'Master Distributor',
  '11': 'Trainer',
  '12': 'Universal Harvester',
} as const

// Chart Colors
export const CHART_COLORS = {
  SYSTEM_QUALITY: '#00f0ff',
  AGENT_8: '#b24bf3',
  AGENT_5A: '#ff1744',
  AGENT_5B: '#ff5252',
} as const

// Layout Dimensions
export const LAYOUT = {
  HEADER_HEIGHT: 70,
  SIDEBAR_WIDTH: 80,
  RIGHT_PANEL_WIDTH: 320,
} as const
