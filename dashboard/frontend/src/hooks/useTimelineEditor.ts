import { useState, useEffect, useCallback, useRef } from 'react';
import { SceneData, UseTimelineEditorReturn } from '../types';
import axios from 'axios';

/**
 * Custom Hook for Timeline Editor Logic
 *
 * Manages all timeline editor state and controls:
 * - Scene management (add/remove/update/move/resize)
 * - Playhead position and playback
 * - Zoom level
 * - Undo/Redo (10 steps)
 * - Save/Export functionality
 */
export const useTimelineEditor = (
  projectId: string,
  initialScenes: SceneData[],
  totalDuration: number
): UseTimelineEditorReturn => {
  // State
  const [scenes, setScenes] = useState<SceneData[]>(initialScenes);
  const [selectedSceneId, setSelectedSceneId] = useState<string | null>(null);
  const [playheadPosition, setPlayheadPosition] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(1);

  // Undo/Redo stacks
  const [undoStack, setUndoStack] = useState<SceneData[][]>([]);
  const [redoStack, setRedoStack] = useState<SceneData[][]>([]);

  // Playback interval ref
  const playbackIntervalRef = useRef<number | null>(null);

  // Save current state to undo stack
  const saveToUndoStack = useCallback(() => {
    setUndoStack(prev => {
      const newStack = [...prev, scenes];
      // Keep only last 10 states
      return newStack.slice(-10);
    });
    // Clear redo stack when new action is performed
    setRedoStack([]);
  }, [scenes]);

  // Scene management
  const addScene = useCallback((scene: SceneData) => {
    saveToUndoStack();
    setScenes(prev => [...prev, scene]);
  }, [saveToUndoStack]);

  const removeScene = useCallback((id: string) => {
    saveToUndoStack();
    setScenes(prev => prev.filter(s => s.id !== id));
    if (selectedSceneId === id) {
      setSelectedSceneId(null);
    }
  }, [saveToUndoStack, selectedSceneId]);

  const updateScene = useCallback((id: string, updates: Partial<SceneData>) => {
    saveToUndoStack();
    setScenes(prev =>
      prev.map(scene => (scene.id === id ? { ...scene, ...updates } : scene))
    );
  }, [saveToUndoStack]);

  const moveScene = useCallback((id: string, startTime: number) => {
    saveToUndoStack();
    setScenes(prev =>
      prev.map(scene =>
        scene.id === id ? { ...scene, startTime: Math.max(0, startTime) } : scene
      )
    );
  }, [saveToUndoStack]);

  const resizeScene = useCallback((id: string, duration: number) => {
    saveToUndoStack();
    setScenes(prev =>
      prev.map(scene =>
        scene.id === id ? { ...scene, duration: Math.max(0.5, duration) } : scene
      )
    );
  }, [saveToUndoStack]);

  const selectScene = useCallback((id: string) => {
    setSelectedSceneId(id);
  }, []);

  // Playback controls
  const playPreview = useCallback(() => {
    setIsPlaying(true);

    // Start playback interval (60 FPS)
    playbackIntervalRef.current = window.setInterval(() => {
      setPlayheadPosition(prev => {
        const newPosition = prev + (1 / 60) / totalDuration;
        if (newPosition >= 1) {
          // Stop at end
          setIsPlaying(false);
          if (playbackIntervalRef.current) {
            clearInterval(playbackIntervalRef.current);
          }
          return 1;
        }
        return newPosition;
      });
    }, 1000 / 60); // 60 FPS
  }, [totalDuration]);

  const stopPreview = useCallback(() => {
    setIsPlaying(false);
    if (playbackIntervalRef.current) {
      clearInterval(playbackIntervalRef.current);
      playbackIntervalRef.current = null;
    }
  }, []);

  const seek = useCallback((position: number) => {
    setPlayheadPosition(Math.max(0, Math.min(1, position)));
  }, []);

  // Cleanup playback on unmount
  useEffect(() => {
    return () => {
      if (playbackIntervalRef.current) {
        clearInterval(playbackIntervalRef.current);
      }
    };
  }, []);

  // Undo/Redo
  const undo = useCallback(() => {
    if (undoStack.length === 0) return;

    const previousState = undoStack[undoStack.length - 1];
    setRedoStack(prev => [...prev, scenes]);
    setScenes(previousState);
    setUndoStack(prev => prev.slice(0, -1));
  }, [undoStack, scenes]);

  const redo = useCallback(() => {
    if (redoStack.length === 0) return;

    const nextState = redoStack[redoStack.length - 1];
    setUndoStack(prev => [...prev, scenes]);
    setScenes(nextState);
    setRedoStack(prev => prev.slice(0, -1));
  }, [redoStack, scenes]);

  // Save/Export
  const saveProject = useCallback(async () => {
    try {
      await axios.post(`/api/projects/${projectId}/save`, {
        scenes
      });
      console.log('Project saved successfully');
    } catch (error) {
      console.error('Failed to save project:', error);
      throw error;
    }
  }, [projectId, scenes]);

  const exportProject = useCallback(async (format: 'json' | 'runway' | 'veo') => {
    try {
      let exportData: any;

      switch (format) {
        case 'json':
          // Simple JSON export
          exportData = {
            projectId,
            duration: totalDuration,
            scenes: scenes.map(s => ({
              sceneNumber: s.sceneNumber,
              startTime: s.startTime,
              duration: s.duration,
              prompt: s.prompt,
              style: s.style,
              agent: s.agent
            }))
          };
          break;

        case 'runway':
          // Runway ML format
          exportData = {
            version: '1.0',
            scenes: scenes.map(s => ({
              id: s.id,
              start_frame: Math.floor(s.startTime * 30), // 30 FPS
              end_frame: Math.floor((s.startTime + s.duration) * 30),
              prompt: s.prompt,
              style_preset: s.style
            }))
          };
          break;

        case 'veo':
          // Veo format
          exportData = {
            metadata: {
              project_id: projectId,
              total_duration: totalDuration
            },
            clips: scenes.map(s => ({
              clip_id: s.id,
              start_time: s.startTime,
              end_time: s.startTime + s.duration,
              description: s.prompt,
              visual_style: s.style
            }))
          };
          break;
      }

      // Download as file
      const blob = new Blob([JSON.stringify(exportData, null, 2)], {
        type: 'application/json'
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `storyboard-${projectId}-${format}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      console.log(`Project exported as ${format}`);
    } catch (error) {
      console.error('Failed to export project:', error);
      throw error;
    }
  }, [projectId, scenes, totalDuration]);

  // Zoom controls
  const zoomIn = useCallback(() => {
    setZoomLevel(prev => Math.min(2, prev + 0.25));
  }, []);

  const zoomOut = useCallback(() => {
    setZoomLevel(prev => Math.max(0.5, prev - 0.25));
  }, []);

  return {
    scenes,
    selectedSceneId,
    playheadPosition,
    isPlaying,
    zoomLevel,
    canUndo: undoStack.length > 0,
    canRedo: redoStack.length > 0,
    addScene,
    removeScene,
    updateScene,
    moveScene,
    resizeScene,
    selectScene,
    playPreview,
    stopPreview,
    seek,
    undo,
    redo,
    saveProject,
    exportProject,
    zoomIn,
    zoomOut
  };
};
