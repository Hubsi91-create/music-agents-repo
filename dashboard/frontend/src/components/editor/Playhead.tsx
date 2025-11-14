import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { PlayheadProps } from '../../types';
import styles from './EditorStyles.module.css';

/**
 * Playhead Position Indicator Component
 *
 * Features:
 * - Vertical red line with glow
 * - Draggable to scrub timeline
 * - Shows current time on hover
 * - Smooth animation
 */
const Playhead = ({
  position,
  currentTime,
  onSeek
}: PlayheadProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const playheadRef = useRef<HTMLDivElement>(null);

  // Handle drag start
  const handleMouseDown = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsDragging(true);

    const handleMouseMove = (moveEvent: MouseEvent) => {
      const timeline = playheadRef.current?.parentElement;
      if (!timeline) return;

      const rect = timeline.getBoundingClientRect();
      const x = moveEvent.clientX - rect.left;
      const newPosition = Math.max(0, Math.min(1, x / rect.width));
      onSeek(newPosition);
    };

    const handleMouseUp = () => {
      setIsDragging(false);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  };

  // Format time
  const formatTime = (seconds: number): string => {
    if (!isFinite(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <motion.div
      ref={playheadRef}
      className={`${styles.playhead} ${isDragging ? styles.dragging : ''}`}
      style={{ left: `${position * 100}%` }}
      onMouseDown={handleMouseDown}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      animate={{
        boxShadow: isDragging
          ? '0 0 30px rgba(255, 23, 68, 1)'
          : '0 0 15px rgba(255, 23, 68, 0.6)'
      }}
      transition={{ duration: 0.2 }}
    >
      {/* Playhead Line */}
      <div className={styles.playheadLine}></div>

      {/* Playhead Handle */}
      <motion.div
        className={styles.playheadHandle}
        whileHover={{ scale: 1.3 }}
        whileTap={{ scale: 1.1 }}
      ></motion.div>

      {/* Time Display Tooltip */}
      {(isHovered || isDragging) && (
        <motion.div
          className={styles.playheadTooltip}
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -5 }}
        >
          {formatTime(currentTime)}
        </motion.div>
      )}
    </motion.div>
  );
};

export default Playhead;
