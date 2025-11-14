import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PlaybackSpeedProps, PlaybackRate } from '../../types';
import styles from './PlayerStyles.module.css';

/**
 * Playback Speed Selector Component
 *
 * Allows users to adjust playback speed (0.5x - 2.0x)
 */
const PlaybackSpeed = ({ speed, onSpeedChange }: PlaybackSpeedProps) => {
  const [isOpen, setIsOpen] = useState(false);

  const speeds: PlaybackRate[] = [0.5, 0.75, 1, 1.25, 1.5, 2];

  const handleSelect = (newSpeed: PlaybackRate) => {
    onSpeedChange(newSpeed);
    setIsOpen(false);
  };

  return (
    <div className={styles.speedSelector}>
      <motion.button
        className={styles.speedButton}
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        {speed}x ▼
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className={styles.speedDropdown}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            {speeds.map((s) => (
              <button
                key={s}
                className={`${styles.speedOption} ${
                  s === speed ? styles.selected : ''
                }`}
                onClick={() => handleSelect(s)}
              >
                {s}x
                {s === speed && ' ✓'}
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default PlaybackSpeed;
