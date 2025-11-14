import { useRef, useState, useEffect } from 'react';
import { TimelineTrackProps } from '../../types';
import SceneBlock from './SceneBlock';
import Playhead from './Playhead';
import WaveformDisplay from './WaveformDisplay';
import styles from './EditorStyles.module.css';

/**
 * Timeline Track Component
 *
 * Renders the timeline canvas with:
 * - Time ruler with labels
 * - Grid lines (every 5s)
 * - Waveform background
 * - Scene blocks
 * - Playhead indicator
 */
const TimelineTrack = ({
  scenes,
  selectedSceneId,
  playheadPosition,
  zoomLevel,
  totalDuration,
  onSceneSelect,
  onSceneMove,
  onSceneResize,
  onSeek,
  waveformUrl
}: TimelineTrackProps) => {
  const trackRef = useRef<HTMLDivElement>(null);
  const [trackWidth, setTrackWidth] = useState(1000);
  const [isDraggingScene, setIsDraggingScene] = useState(false);

  // Update track width on resize
  useEffect(() => {
    const updateWidth = () => {
      if (trackRef.current) {
        setTrackWidth(trackRef.current.clientWidth);
      }
    };

    updateWidth();
    window.addEventListener('resize', updateWidth);
    return () => window.removeEventListener('resize', updateWidth);
  }, []);

  // Calculate effective width with zoom
  const effectiveWidth = trackWidth * zoomLevel;

  // Generate time ruler markers
  const generateRulerMarkers = () => {
    const markers = [];
    const interval = 5; // 5 second intervals
    const numMarkers = Math.ceil(totalDuration / interval);

    for (let i = 0; i <= numMarkers; i++) {
      const time = i * interval;
      if (time > totalDuration) break;

      const position = (time / totalDuration) * 100;

      markers.push(
        <div
          key={`marker-${i}`}
          className={styles.rulerMarker}
          style={{ left: `${position}%` }}
        >
          <div className={styles.rulerTick}></div>
          <div className={styles.rulerLabel}>{formatTime(time)}</div>
        </div>
      );
    }

    return markers;
  };

  // Generate grid lines
  const generateGridLines = () => {
    const lines = [];
    const interval = 5; // 5 second intervals
    const numLines = Math.ceil(totalDuration / interval);

    for (let i = 0; i <= numLines; i++) {
      const time = i * interval;
      if (time > totalDuration) break;

      const position = (time / totalDuration) * 100;

      lines.push(
        <div
          key={`line-${i}`}
          className={styles.gridLine}
          style={{ left: `${position}%` }}
        ></div>
      );
    }

    return lines;
  };

  // Handle track click for seeking
  const handleTrackClick = (e: React.MouseEvent<HTMLDivElement>) => {
    // Don't seek if clicking on a scene or playhead
    const target = e.target as HTMLElement;
    if (
      target.closest(`.${styles.sceneBlock}`) ||
      target.closest(`.${styles.playhead}`)
    ) {
      return;
    }

    if (trackRef.current) {
      const rect = trackRef.current.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const position = clickX / rect.width;
      onSeek(Math.max(0, Math.min(1, position)));
    }
  };

  // Scene drag handlers
  const handleSceneDragStart = (sceneId: string) => (e: React.DragEvent) => {
    setIsDraggingScene(true);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', sceneId);
  };

  const handleSceneDragEnd = (sceneId: string) => (e: React.DragEvent) => {
    setIsDraggingScene(false);

    if (trackRef.current) {
      const rect = trackRef.current.getBoundingClientRect();
      const dropX = e.clientX - rect.left;
      const position = dropX / rect.width;
      const newStartTime = position * totalDuration;

      // Snap to grid (0.5s intervals)
      const snappedTime = Math.round(newStartTime * 2) / 2;
      onSceneMove(sceneId, Math.max(0, Math.min(snappedTime, totalDuration)));
    }
  };

  // Scene resize handlers
  const handleSceneResizeStart = (sceneId: string, direction: 'left' | 'right') => (
    e: React.MouseEvent
  ) => {
    e.stopPropagation();
    const startX = e.clientX;
    const scene = scenes.find(s => s.id === sceneId);
    if (!scene) return;

    const startDuration = scene.duration;
    const startTime = scene.startTime;

    const handleMouseMove = (moveEvent: MouseEvent) => {
      const deltaX = moveEvent.clientX - startX;
      const deltaTime = (deltaX / effectiveWidth) * totalDuration;

      if (direction === 'right') {
        // Resize from right edge (change duration)
        const newDuration = Math.max(0.5, startDuration + deltaTime);
        onSceneResize(sceneId, newDuration);
      } else {
        // Resize from left edge (change start time and duration)
        const newStartTime = Math.max(0, startTime + deltaTime);
        const newDuration = Math.max(0.5, startDuration - deltaTime);
        onSceneMove(sceneId, newStartTime);
        onSceneResize(sceneId, newDuration);
      }
    };

    const handleMouseUp = () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  };

  // Scene delete handler
  const handleSceneDelete = (sceneId: string) => {
    const confirmed = window.confirm('Are you sure you want to delete this scene?');
    if (confirmed) {
      // The parent will handle deletion through onSceneSelect
      onSceneSelect(sceneId);
    }
  };

  return (
    <div
      ref={trackRef}
      className={styles.timeline}
      onClick={handleTrackClick}
      style={{ cursor: isDraggingScene ? 'grabbing' : 'default' }}
    >
      {/* Time Ruler */}
      <div className={styles.ruler}>
        {generateRulerMarkers()}
      </div>

      {/* Track Container */}
      <div className={styles.track}>
        {/* Waveform Background */}
        {waveformUrl && (
          <div className={styles.waveformContainer}>
            <WaveformDisplay
              audioUrl={waveformUrl}
              duration={totalDuration}
              height={100}
              opacity={0.2}
            />
          </div>
        )}

        {/* Grid Lines */}
        <div className={styles.grid}>
          {generateGridLines()}
        </div>

        {/* Scene Blocks */}
        <div className={styles.scenesContainer}>
          {scenes.map((scene) => (
            <SceneBlock
              key={scene.id}
              scene={scene}
              isSelected={scene.id === selectedSceneId}
              onSelect={() => onSceneSelect(scene.id)}
              onDragStart={handleSceneDragStart(scene.id)}
              onDragEnd={handleSceneDragEnd(scene.id)}
              onResizeStart={(direction) => handleSceneResizeStart(scene.id, direction)}
              onDelete={() => handleSceneDelete(scene.id)}
              timelineWidth={trackWidth}
              totalDuration={totalDuration}
            />
          ))}
        </div>

        {/* Playhead */}
        <Playhead
          position={playheadPosition}
          timelineWidth={trackWidth}
          currentTime={playheadPosition * totalDuration}
          duration={totalDuration}
          onSeek={onSeek}
        />
      </div>
    </div>
  );
};

// Format time as MM:SS
const formatTime = (seconds: number): string => {
  if (!isFinite(seconds)) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

export default TimelineTrack;
