import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { TimelineEditorProps } from '../../types';
import { useTimelineEditor } from '../../hooks/useTimelineEditor';
import TimelineTrack from './TimelineTrack';
import EditorControls from './EditorControls';
import styles from './EditorStyles.module.css';

/**
 * Interactive Storyboard Timeline Editor
 *
 * Features:
 * - Drag & drop scene repositioning
 * - Resize scene duration
 * - Playhead scrubbing
 * - Zoom in/out
 * - Undo/Redo (10 steps)
 * - Save/Export functionality
 * - Keyboard shortcuts
 * - Waveform visualization
 * - Snap-to-grid
 * - Multi-scene selection
 */
const TimelineEditor = ({
  projectId,
  initialScenes,
  musicDuration,
  onScenesChange,
  onSave,
  onExport
}: TimelineEditorProps) => {
  const {
    scenes,
    selectedSceneId,
    playheadPosition,
    isPlaying,
    zoomLevel,
    canUndo,
    canRedo,
    addScene,
    removeScene,
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
  } = useTimelineEditor(projectId, initialScenes, musicDuration);

  // Notify parent of scene changes
  useEffect(() => {
    if (onScenesChange) {
      onScenesChange(scenes);
    }
  }, [scenes, onScenesChange]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const targetTag = (e.target as HTMLElement).tagName;
      if (targetTag === 'INPUT' || targetTag === 'TEXTAREA') return;

      // Check for modifier keys
      const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
      const modifier = isMac ? e.metaKey : e.ctrlKey;

      if (e.key === ' ') {
        // Space: Play/Pause
        e.preventDefault();
        if (isPlaying) {
          stopPreview();
        } else {
          playPreview();
        }
      } else if (e.key === 'Delete' || e.key === 'Backspace') {
        // Delete selected scene
        e.preventDefault();
        if (selectedSceneId) {
          removeScene(selectedSceneId);
        }
      } else if (modifier && e.key === 'z') {
        // Ctrl/Cmd + Z: Undo
        e.preventDefault();
        if (e.shiftKey) {
          redo();
        } else {
          undo();
        }
      } else if (modifier && e.key === 'y') {
        // Ctrl/Cmd + Y: Redo
        e.preventDefault();
        redo();
      } else if (modifier && e.key === 's') {
        // Ctrl/Cmd + S: Save
        e.preventDefault();
        handleSave();
      } else if (e.key === 'd' || e.key === 'D') {
        // D: Duplicate selected scene
        e.preventDefault();
        if (selectedSceneId) {
          const scene = scenes.find(s => s.id === selectedSceneId);
          if (scene) {
            const newScene = {
              ...scene,
              id: `scene-${Date.now()}`,
              startTime: scene.startTime + scene.duration
            };
            addScene(newScene);
          }
        }
      } else if (e.key === '+' || e.key === '=') {
        // +: Zoom in
        e.preventDefault();
        zoomIn();
      } else if (e.key === '-' || e.key === '_') {
        // -: Zoom out
        e.preventDefault();
        zoomOut();
      } else if (e.key === 'ArrowLeft') {
        // ←: Move playhead left
        e.preventDefault();
        seek(Math.max(0, playheadPosition - 0.01));
      } else if (e.key === 'ArrowRight') {
        // →: Move playhead right
        e.preventDefault();
        seek(Math.min(1, playheadPosition + 0.01));
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [
    isPlaying,
    selectedSceneId,
    scenes,
    playheadPosition,
    playPreview,
    stopPreview,
    removeScene,
    undo,
    redo,
    addScene,
    zoomIn,
    zoomOut,
    seek
  ]);

  const handleSave = async () => {
    try {
      await saveProject();
      if (onSave) {
        await onSave();
      }
    } catch (error) {
      console.error('Failed to save project:', error);
      alert('Failed to save project. Please try again.');
    }
  };

  const handleExport = async (format: 'json' | 'runway' | 'veo') => {
    try {
      await exportProject(format);
      if (onExport) {
        onExport(format);
      }
    } catch (error) {
      console.error('Failed to export project:', error);
      alert('Failed to export project. Please try again.');
    }
  };

  const handleSceneSelect = (sceneId: string) => {
    selectScene(sceneId);
  };

  const handleSceneMove = (sceneId: string, startTime: number) => {
    moveScene(sceneId, startTime);
  };

  const handleSceneResize = (sceneId: string, duration: number) => {
    resizeScene(sceneId, duration);
  };

  const handleSeek = (position: number) => {
    seek(position);
  };

  const handleDeleteSelected = () => {
    if (selectedSceneId) {
      removeScene(selectedSceneId);
    }
  };

  return (
    <motion.div
      className={styles.editor}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Editor Header */}
      <div className={styles.header}>
        <h2 className={styles.title}>Storyboard Timeline Editor</h2>
        <div className={styles.info}>
          <span>Duration: {formatDuration(musicDuration)}</span>
          <span>Scenes: {scenes.length}</span>
          <span>Zoom: {(zoomLevel * 100).toFixed(0)}%</span>
        </div>
      </div>

      {/* Editor Controls */}
      <EditorControls
        isPlaying={isPlaying}
        zoomLevel={zoomLevel}
        canUndo={canUndo}
        canRedo={canRedo}
        onPlay={playPreview}
        onPause={stopPreview}
        onStop={stopPreview}
        onZoomIn={zoomIn}
        onZoomOut={zoomOut}
        onSave={handleSave}
        onExport={handleExport}
        onDownload={() => handleExport('json')}
        onUndo={undo}
        onRedo={redo}
        onDelete={handleDeleteSelected}
      />

      {/* Timeline Track */}
      <div className={styles.timelineContainer}>
        <TimelineTrack
          scenes={scenes}
          selectedSceneId={selectedSceneId}
          playheadPosition={playheadPosition}
          zoomLevel={zoomLevel}
          totalDuration={musicDuration}
          onSceneSelect={handleSceneSelect}
          onSceneMove={handleSceneMove}
          onSceneResize={handleSceneResize}
          onSeek={handleSeek}
        />
      </div>

      {/* Scene Details Panel (if scene selected) */}
      {selectedSceneId && (
        <div className={styles.detailsPanel}>
          {(() => {
            const scene = scenes.find(s => s.id === selectedSceneId);
            if (!scene) return null;

            return (
              <motion.div
                className={styles.sceneDetails}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h3>Scene {scene.sceneNumber}</h3>
                <div className={styles.detailRow}>
                  <span>Start:</span>
                  <span>{formatDuration(scene.startTime)}</span>
                </div>
                <div className={styles.detailRow}>
                  <span>Duration:</span>
                  <span>{formatDuration(scene.duration)}</span>
                </div>
                <div className={styles.detailRow}>
                  <span>End:</span>
                  <span>{formatDuration(scene.startTime + scene.duration)}</span>
                </div>
                <div className={styles.detailRow}>
                  <span>Agent:</span>
                  <span>{scene.agent}</span>
                </div>
                <div className={styles.detailRow}>
                  <span>Style:</span>
                  <span>{scene.style}</span>
                </div>
                <div className={styles.promptPreview}>
                  <strong>Prompt:</strong>
                  <p>{scene.prompt}</p>
                </div>
              </motion.div>
            );
          })()}
        </div>
      )}

      {/* Keyboard Shortcuts Help */}
      <div className={styles.shortcuts}>
        <span>Shortcuts:</span>
        <span>Space: Play/Pause</span>
        <span>Del: Delete</span>
        <span>Ctrl+Z: Undo</span>
        <span>Ctrl+Y: Redo</span>
        <span>Ctrl+S: Save</span>
        <span>D: Duplicate</span>
        <span>+/-: Zoom</span>
        <span>←/→: Scrub</span>
      </div>
    </motion.div>
  );
};

// Helper function to format duration in MM:SS
const formatDuration = (seconds: number): string => {
  if (!isFinite(seconds)) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

export default TimelineEditor;
