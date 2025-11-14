import { useState } from 'react';
import { motion } from 'framer-motion';
import { SceneBlockProps } from '../../types';
import styles from './EditorStyles.module.css';

/**
 * Draggable Scene Block Component
 *
 * Features:
 * - Displays scene information
 * - Draggable to reposition
 * - Resizable handles (left/right)
 * - Click to select
 * - Hover to preview details
 * - Delete button
 * - Neon border when selected
 */
const SceneBlock = ({
  scene,
  isSelected,
  onSelect,
  onDragStart,
  onDragEnd,
  onResizeStart,
  onDelete,
  totalDuration
}: SceneBlockProps) => {
  const [isHovered, setIsHovered] = useState(false);
  const [showContextMenu, setShowContextMenu] = useState(false);

  // Calculate position and width
  const left = (scene.startTime / totalDuration) * 100;
  const width = (scene.duration / totalDuration) * 100;

  // Get color based on agent or use default
  const sceneColor = scene.color || getAgentColor(scene.agent);

  // Handle right-click context menu
  const handleContextMenu = (e: React.MouseEvent) => {
    e.preventDefault();
    setShowContextMenu(true);
    onSelect();

    // Close menu on click outside
    const closeMenu = () => {
      setShowContextMenu(false);
      window.removeEventListener('click', closeMenu);
    };
    setTimeout(() => window.addEventListener('click', closeMenu), 10);
  };

  return (
    <>
      <div
        className={`${styles.sceneBlock} ${isSelected ? styles.selected : ''}`}
        style={{
          left: `${left}%`,
          width: `${width}%`,
          backgroundColor: sceneColor,
          borderColor: isSelected ? '#00f0ff' : 'transparent',
          transform: isHovered ? 'scale(1.02)' : 'scale(1)',
          transition: 'all 200ms ease'
        }}
        draggable
        onDragStart={onDragStart}
        onDragEnd={onDragEnd}
        onClick={(e) => {
          e.stopPropagation();
          onSelect();
        }}
        onContextMenu={handleContextMenu}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Scene Number */}
        <div className={styles.sceneNumber}>
          {scene.sceneNumber}
        </div>

        {/* Duration Display */}
        <div className={styles.sceneDuration}>
          {formatDuration(scene.duration)}
        </div>

        {/* Hover Details */}
        {isHovered && (
          <motion.div
            className={styles.sceneTooltip}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
          >
            <div><strong>Scene {scene.sceneNumber}</strong></div>
            <div>{scene.agent}</div>
            <div className={styles.tooltipPrompt}>
              {scene.prompt.substring(0, 100)}
              {scene.prompt.length > 100 ? '...' : ''}
            </div>
            <div className={styles.tooltipStyle}>{scene.style}</div>
          </motion.div>
        )}

        {/* Resize Handles */}
        {(isHovered || isSelected) && (
          <>
            <div
              className={`${styles.resizeHandle} ${styles.resizeLeft}`}
              onMouseDown={onResizeStart('left')}
              onClick={(e) => e.stopPropagation()}
            >
              <div className={styles.resizeIndicator}></div>
            </div>
            <div
              className={`${styles.resizeHandle} ${styles.resizeRight}`}
              onMouseDown={onResizeStart('right')}
              onClick={(e) => e.stopPropagation()}
            >
              <div className={styles.resizeIndicator}></div>
            </div>
          </>
        )}

        {/* Delete Button (on hover) */}
        {isHovered && (
          <motion.button
            className={styles.deleteButton}
            onClick={(e) => {
              e.stopPropagation();
              onDelete();
            }}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            ✕
          </motion.button>
        )}
      </div>

      {/* Context Menu */}
      {showContextMenu && (
        <div
          className={styles.contextMenu}
          style={{
            left: `${left}%`,
            top: '50px'
          }}
        >
          <button onClick={() => { onDelete(); setShowContextMenu(false); }}>
            Delete Scene
          </button>
          <button onClick={() => { /* Duplicate logic */ setShowContextMenu(false); }}>
            Duplicate Scene
          </button>
        </div>
      )}
    </>
  );
};

// Helper: Format duration
const formatDuration = (seconds: number): string => {
  if (!isFinite(seconds)) return '0s';
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

// Helper: Get agent color
const getAgentColor = (agent: string): string => {
  const colors: Record<string, string> = {
    'Agent 1': 'rgba(255, 107, 107, 0.8)',
    'Agent 2': 'rgba(78, 205, 196, 0.8)',
    'Agent 3': 'rgba(255, 195, 113, 0.8)',
    'Agent 4': 'rgba(162, 155, 254, 0.8)',
    'Agent 5': 'rgba(255, 159, 243, 0.8)',
    'Agent 6': 'rgba(99, 205, 218, 0.8)',
    'Agent 7': 'rgba(178, 75, 255, 0.8)',
    'default': 'rgba(0, 240, 255, 0.6)'
  };

  return colors[agent] || colors['default'];
};

export default SceneBlock;
