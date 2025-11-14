/**
 * Storyboard API Types
 * =====================
 * TypeScript type definitions for Storyboard API endpoints
 *
 * Corresponds to:
 * - dashboard/backend/routes/storyboard_routes.py
 * - dashboard/backend/services/*.py
 *
 * Author: Music Video Production System
 * Version: 1.0.0
 */

// ============================================================
// COMMON TYPES
// ============================================================

export interface ApiError {
  error: string;
  message: string;
  retryable: boolean;
  timestamp: string;
  details?: Record<string, any>;
}

export type ApiResponse<T> = T | ApiError;

export function isApiError(response: any): response is ApiError {
  return response && typeof response.error === 'string';
}

// ============================================================
// GOOGLE DRIVE TYPES
// ============================================================

export interface DriveFolder {
  id: string;
  name: string;
  created: string;
  modified?: string;
}

export interface DriveFoldersResponse {
  folders: DriveFolder[];
  count: number;
  parent_id: string;
}

export interface DriveFile {
  id: string;
  name: string;
  mimeType: string;
  size: number;
  extension?: string;
  created: string;
  modified?: string;
  duration?: number | null;
}

export interface DriveFilesResponse {
  files: DriveFile[];
  count: number;
  folder_id: string;
  file_type: string;
}

export interface DriveFileMetadata {
  id: string;
  name: string;
  mimeType: string;
  size: number;
  extension?: string;
  created: string;
  modified?: string;
  webContentLink?: string;
  webViewLink?: string;
  owners?: any[];
  properties?: Record<string, any>;
}

export type DriveFileType = 'audio' | 'video' | 'image' | 'all';

// ============================================================
// RUNWAY VIDEO GENERATION TYPES
// ============================================================

export type RunwayEngine =
  | 'veo31_standard'
  | 'veo31_fast'
  | 'runway_standard'
  | 'runway_turbo'
  | 'runway_unlimited';

export type GenerationStatus =
  | 'queued'
  | 'processing'
  | 'completed'
  | 'failed'
  | 'cancelled';

export interface VideoGenerationRequest {
  prompt: string;
  duration: number;
  style?: string;
  engine?: RunwayEngine;
  music_file?: string;
}

export interface VideoGenerationTask {
  task_id: string;
  status: GenerationStatus;
  prompt: string;
  duration: number;
  engine: string;
  style?: string;
  music_file?: string;
  video_url: string | null;
  estimated_time: number;
  cost: number;
  credits_required: number;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
  retry_count: number;
}

export interface EngineInfo {
  id: RunwayEngine;
  name: string;
  cost_per_10s: number;
  credits_per_10s: number;
  estimated_speed: number;
}

export interface EnginesResponse {
  engines: EngineInfo[];
  count: number;
  timestamp: string;
}

export interface CostCalculationRequest {
  duration: number;
  engine: RunwayEngine;
}

export interface CostCalculation {
  duration: number;
  engine: string;
  cost_per_10s: number;
  credits_per_10s: number;
  total_cost: number;
  total_credits: number;
  currency: string;
}

export interface VideoUrlResponse {
  task_id: string;
  video_url: string;
  duration: number;
  engine: string;
  cost: number;
}

export interface CreditBalance {
  credits: number;
  credits_usd: number;
  subscription: string;
  subscription_active: boolean;
}

// ============================================================
// DADAN METADATA GENERATION TYPES
// ============================================================

export interface MetadataGenerationRequest {
  song_title: string;
  genre: string;
  mood?: string;
}

export interface YouTubeMetadata {
  youtube_title: string;
  youtube_description: string;
  youtube_tags: string;
  youtube_hashtags: string;
  trending_score: number;
  genre: string;
  mood?: string;
  generated_at: string;
  from_cache: boolean;
}

export interface GenresResponse {
  genres: string[];
  count: number;
  timestamp: string;
}

export interface MoodsResponse {
  moods: string[];
  count: number;
  timestamp: string;
}

// ============================================================
// RECRAFT THUMBNAIL GENERATION TYPES
// ============================================================

export type ThumbnailVariant =
  | 'bold'
  | 'minimal'
  | 'vibrant'
  | 'dark_mode'
  | 'text_heavy';

export interface ThumbnailGenerationRequest {
  video_url: string;
  context?: {
    song_title?: string;
    genre?: string;
    mood?: string;
    artist?: string;
  };
  variants?: ThumbnailVariant[];
}

export interface Thumbnail {
  variant: ThumbnailVariant;
  image_url: string;
  click_prediction: number;
  description: string;
  best_for: string[];
  generated_at: string;
}

export interface ThumbnailsResponse {
  thumbnails: Thumbnail[];
  count: number;
  video_url: string;
  context?: Record<string, any>;
  generated_at: string;
}

export interface VariantInfo {
  variant: ThumbnailVariant;
  description: string;
  click_prediction_boost: number;
  best_for: string[];
}

export interface VariantsResponse {
  variants: VariantInfo[];
  count: number;
  timestamp: string;
}

export interface FrameExtractionRequest {
  video_url: string;
  timestamp?: number;
}

export interface FrameExtractionResponse {
  video_url: string;
  timestamp: number;
  frame_url: string;
  extracted_at: string;
}

export interface ThumbnailPerformance {
  thumbnail_url: string;
  impressions: number;
  clicks: number;
  views: number;
  ctr: number;
  conversion_rate: number;
  performance_rating: 'poor' | 'average' | 'good' | 'excellent';
  analyzed_at: string;
}

export interface VariantComparison {
  total_variants: number;
  best_variant: ThumbnailVariant;
  best_prediction: number;
  worst_variant: ThumbnailVariant;
  worst_prediction: number;
  average_prediction: number;
  improvement_potential: number;
  recommendation: ThumbnailVariant;
  compared_at: string;
}

// ============================================================
// DATABASE TYPES (for frontend state management)
// ============================================================

export interface StoryboardVideo {
  id: string;
  user_id: string;
  project_name: string;
  song_title: string;
  music_file: string;
  genre: string;
  bpm?: number;
  engine: string;
  prompt: string;
  video_url?: string;
  status: GenerationStatus;
  youtube_title?: string;
  youtube_description?: string;
  youtube_tags?: string;
  cost: number;
  credits_used: number;
  duration: number;
  created_at: string;
  completed_at?: string;
  error_message?: string;
}

export interface StoryboardThumbnail {
  id: string;
  video_id: string;
  variant: ThumbnailVariant;
  image_url: string;
  click_prediction: number;
  is_selected: boolean;
  created_at: string;
}

// ============================================================
// HEALTH CHECK
// ============================================================

export interface StoryboardHealthResponse {
  status: 'operational' | 'degraded' | 'down';
  service: string;
  version: string;
  timestamp: string;
  endpoints: {
    drive: number;
    video: number;
    metadata: number;
    thumbnails: number;
  };
}

// ============================================================
// API CLIENT HELPERS
// ============================================================

export const STORYBOARD_API_BASE = '/api/storyboard';

export const StoryboardEndpoints = {
  // Drive
  DRIVE_FOLDERS: `${STORYBOARD_API_BASE}/drive/folders`,
  DRIVE_FILES: (folderId: string) => `${STORYBOARD_API_BASE}/drive/files/${folderId}`,
  DRIVE_FILE_METADATA: (fileId: string) => `${STORYBOARD_API_BASE}/drive/file/${fileId}/metadata`,

  // Video
  VIDEO_GENERATE: `${STORYBOARD_API_BASE}/video/generate`,
  VIDEO_STATUS: (taskId: string) => `${STORYBOARD_API_BASE}/video/${taskId}/status`,
  VIDEO_ENGINES: `${STORYBOARD_API_BASE}/video/engines`,
  VIDEO_CALCULATE_COST: `${STORYBOARD_API_BASE}/video/calculate-cost`,

  // Metadata
  METADATA_GENERATE: `${STORYBOARD_API_BASE}/metadata/generate`,
  METADATA_GENRES: `${STORYBOARD_API_BASE}/metadata/genres`,
  METADATA_MOODS: `${STORYBOARD_API_BASE}/metadata/moods`,

  // Thumbnails
  THUMBNAILS_GENERATE: `${STORYBOARD_API_BASE}/thumbnails/generate`,
  THUMBNAILS_VARIANTS: `${STORYBOARD_API_BASE}/thumbnails/variants`,
  THUMBNAILS_EXTRACT_FRAME: `${STORYBOARD_API_BASE}/thumbnails/extract-frame`,

  // Health
  HEALTH: `${STORYBOARD_API_BASE}/health`,
} as const;

// ============================================================
// REQUEST HELPER FUNCTIONS
// ============================================================

export async function fetchStoryboardApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(endpoint, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      return data as ApiError;
    }

    return data as T;
  } catch (error) {
    return {
      error: 'FETCH_ERROR',
      message: error instanceof Error ? error.message : 'Unknown error',
      retryable: true,
      timestamp: new Date().toISOString(),
    };
  }
}
