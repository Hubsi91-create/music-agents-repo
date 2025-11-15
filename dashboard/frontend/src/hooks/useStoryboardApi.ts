import { useQuery, useMutation } from '@tanstack/react-query';
import type { UseQueryOptions } from '@tanstack/react-query';
import apiClient from '../services/apiClient';
import type {
  EnginesResponse,
  VideoGenerationTask,
  DriveFoldersResponse,
  DriveFilesResponse,
  StoryboardHealthResponse,
  VideoGenerationRequest,
} from '../types/storyboard-api';

// ============================================================
// VIDEO ENGINE HOOKS
// ============================================================

/**
 * Fetch available video generation engines
 */
export function useEngines() {
  return useQuery<EnginesResponse>({
    queryKey: ['storyboard', 'engines'],
    queryFn: async () => {
      const response = await apiClient.get<EnginesResponse>('/video/engines');
      return response.data;
    },
    staleTime: 60000, // Engines ändern sich selten, 1 Minute Cache
  });
}

// ============================================================
// VIDEO GENERATION HOOKS
// ============================================================

/**
 * Fetch video generation task status
 * @param taskId - Task ID to check status for
 * @param options - Additional query options (e.g., refetchInterval for polling)
 */
export function useVideoStatus(
  taskId: string | null,
  options?: Omit<UseQueryOptions<VideoGenerationTask>, 'queryKey' | 'queryFn'>
) {
  return useQuery<VideoGenerationTask>({
    queryKey: ['storyboard', 'video', 'status', taskId],
    queryFn: async () => {
      if (!taskId) throw new Error('Task ID is required');
      const response = await apiClient.get<VideoGenerationTask>(`/video/${taskId}/status`);
      return response.data;
    },
    enabled: !!taskId, // Nur ausführen, wenn taskId vorhanden ist
    ...options,
  });
}

/**
 * Generate a new video
 */
export function useGenerateVideo() {
  return useMutation({
    mutationFn: async (request: VideoGenerationRequest) => {
      const response = await apiClient.post<VideoGenerationTask>('/video/generate', request);
      return response.data;
    },
  });
}

// ============================================================
// GOOGLE DRIVE HOOKS
// ============================================================

/**
 * List folders in Google Drive
 * @param parentId - Parent folder ID (default: 'root')
 * @param accessToken - OAuth2 access token
 */
export function useDriveFolders(parentId: string = 'root', accessToken?: string) {
  return useQuery<DriveFoldersResponse>({
    queryKey: ['storyboard', 'drive', 'folders', parentId],
    queryFn: async () => {
      const params = new URLSearchParams({ parent_id: parentId });
      if (accessToken) params.append('access_token', accessToken);

      const response = await apiClient.get<DriveFoldersResponse>(
        `/drive/folders?${params.toString()}`
      );
      return response.data;
    },
    enabled: !!accessToken, // Nur ausführen, wenn accessToken vorhanden ist
  });
}

/**
 * List files in a Google Drive folder
 * @param folderId - Folder ID to list files from
 * @param fileType - Type of files to list ('audio', 'video', 'image', 'all')
 * @param accessToken - OAuth2 access token
 */
export function useDriveFiles(
  folderId: string,
  fileType: 'audio' | 'video' | 'image' | 'all' = 'all',
  accessToken?: string
) {
  return useQuery<DriveFilesResponse>({
    queryKey: ['storyboard', 'drive', 'files', folderId, fileType],
    queryFn: async () => {
      const params = new URLSearchParams({ file_type: fileType });
      if (accessToken) params.append('access_token', accessToken);

      const response = await apiClient.get<DriveFilesResponse>(
        `/drive/files/${folderId}?${params.toString()}`
      );
      return response.data;
    },
    enabled: !!folderId && !!accessToken,
  });
}

// ============================================================
// HEALTH CHECK HOOKS
// ============================================================

/**
 * Check storyboard API health status
 */
export function useStoryboardHealth() {
  return useQuery<StoryboardHealthResponse>({
    queryKey: ['storyboard', 'health'],
    queryFn: async () => {
      const response = await apiClient.get<StoryboardHealthResponse>('/health');
      return response.data;
    },
    refetchInterval: 30000, // Check health every 30 seconds
  });
}

// ============================================================
// MOCK DATA HOOKS (für die Übergangsphase)
// ============================================================

/**
 * Simuliert Agent Progress Daten
 * TODO: Durch echten API-Endpoint ersetzen, wenn Backend verfügbar
 * @param projectId - The project ID to fetch progress for
 * @param options - Query options including refetchInterval
 */
export function useAgentProgress(projectId?: string, options?: { refetchInterval?: number }) {
  return useQuery({
    queryKey: ['storyboard', 'agent-progress', projectId],
    queryFn: async () => {
      // Temporär: Mock-Daten (variiert basierend auf projectId)
      // TODO: Durch echten API-Call ersetzen: `/projects/${projectId}/progress`

      // Simuliere unterschiedliche Progress-Werte für verschiedene Projekte
      const baseProgress = [
        { id: 1, name: 'FanFor Studio', progress: 100, color: '#3B82F6' },
        { id: 2, name: 'Audio Analysis', progress: 85, color: '#3B82F6' },
        { id: 3, name: 'Scene Generation', progress: 80, color: '#3B82F6' },
        { id: 4, name: 'Effect Layering', progress: 60, color: '#3B82F6' },
        { id: 5, name: 'Sync & Timing', progress: 30, color: '#3B82F6' },
        { id: 6, name: 'Final Render', progress: 10, color: '#3B82F6' },
      ];

      // Variiere Progress basierend auf projectId
      if (projectId === 'project2') {
        return baseProgress.map(agent => ({
          ...agent,
          progress: Math.min(100, agent.progress + 10)
        }));
      } else if (projectId === 'project3') {
        return baseProgress.map(agent => ({
          ...agent,
          progress: Math.max(0, agent.progress - 20)
        }));
      }

      return baseProgress;
    },
    refetchInterval: options?.refetchInterval || 5000, // Poll every 5 seconds
  });
}

/**
 * Simuliert Video Thumbnail Daten
 * TODO: Durch echten API-Endpoint ersetzen, wenn Backend verfügbar
 * @param projectId - The project ID to fetch thumbnails for
 */
export function useVideoThumbnails(projectId?: string) {
  return useQuery({
    queryKey: ['storyboard', 'video-thumbnails', projectId],
    queryFn: async () => {
      // Temporär: Mock-Daten (variiert basierend auf projectId)
      // TODO: Durch echten API-Call ersetzen: `/projects/${projectId}/thumbnails`

      const baseThumbnails = [
        { id: 1, duration: '1:0', status: 'rendering', gradientColors: ['#667eea', '#764ba2'] },
        { id: 2, duration: '0:8', status: 'rendering', gradientColors: ['#f093fb', '#f5576c'] },
        { id: 3, duration: '1:0', status: 'rendering', gradientColors: ['#4facfe', '#00f2fe'] },
        { id: 4, duration: '0:8', status: 'rendering', gradientColors: ['#43e97b', '#38f9d7'] },
        { id: 5, duration: '1:0', status: 'rendering', gradientColors: ['#fa709a', '#fee140'] },
        { id: 6, duration: '0:8', status: 'rendering', gradientColors: ['#30cfd0', '#330867'] },
      ];

      // Variiere Thumbnails basierend auf projectId
      if (projectId === 'project2') {
        return baseThumbnails.slice(0, 4); // Weniger Thumbnails für Project 2
      } else if (projectId === 'project3') {
        return baseThumbnails.slice(0, 3); // Noch weniger für Project 3
      }

      return baseThumbnails;
    },
  });
}

/**
 * Simuliert Audio Track Daten
 * TODO: Durch echten API-Endpoint ersetzen, wenn Backend verfügbar
 * @param projectId - The project ID to fetch audio track for
 */
export function useAudioTrack(projectId?: string) {
  return useQuery({
    queryKey: ['storyboard', 'audio-track', projectId],
    queryFn: async () => {
      // Temporär: Mock-Daten (variiert basierend auf projectId)
      // TODO: Durch echten API-Call ersetzen: `/projects/${projectId}/audio`

      const audioTracks: Record<string, any> = {
        project1: {
          title: 'Midnight Serenade',
          artist: 'CosmoSonic',
          duration: 240,
          currentTime: 45,
          isPlaying: false,
        },
        project2: {
          title: 'Electric Dreams',
          artist: 'Neon Pulse',
          duration: 195,
          currentTime: 30,
          isPlaying: false,
        },
        project3: {
          title: 'Selene Gtulls',
          artist: 'Lunar Waves',
          duration: 270,
          currentTime: 60,
          isPlaying: false,
        },
      };

      return audioTracks[projectId || 'project1'] || audioTracks.project1;
    },
  });
}

/**
 * Simuliert Navigation Items
 * TODO: Durch echten API-Endpoint ersetzen, wenn Backend verfügbar
 */
export function useNavItems() {
  return useQuery({
    queryKey: ['storyboard', 'nav-items'],
    queryFn: async () => {
      // Temporär: Mock-Daten
      // TODO: Durch echten API-Call ersetzen
      return [
        { id: 'home', label: 'Home', icon: '🏠', type: 'section' as const },
        { id: 'projects', label: 'Projects', icon: '📁', type: 'section' as const },
        { id: 'libraries', label: 'Libraris', icon: '📚', type: 'section' as const },
        { id: 'settings', label: 'Settings', icon: '⚙️', type: 'section' as const },
        { id: 'account', label: 'Account', icon: '👤', type: 'section' as const },
        { id: 'project1', label: 'Midnight Serenade', icon: '🎵', type: 'project' as const },
        { id: 'project2', label: 'Electric Dreams', icon: '⚡', type: 'project' as const },
        { id: 'project3', label: 'Selene Gtulls', icon: '🌙', type: 'project' as const },
      ];
    },
  });
}
