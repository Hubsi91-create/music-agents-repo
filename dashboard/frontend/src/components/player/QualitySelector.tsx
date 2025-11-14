import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { QualitySelectorProps } from '../../types';
import styles from './PlayerStyles.module.css';

/**
 * Quality Selector Dropdown Component
 *
 * Allows users to select video quality (1080p, 2k, 4k)
 */
const QualitySelector = ({ selectedQuality, qualities, onSelect }: QualitySelectorProps) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleSelect = (quality: typeof selectedQuality) => {
    onSelect(quality);
    setIsOpen(false);
  };

  return (
    <div className={styles.qualitySelector}>
      <motion.button
        className={styles.qualityButton}
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        {selectedQuality} ▼
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className={styles.qualityDropdown}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            {qualities.map((quality) => (
              <button
                key={quality}
                className={`${styles.qualityOption} ${
                  quality === selectedQuality ? styles.selected : ''
                }`}
                onClick={() => handleSelect(quality)}
              >
                {quality}
                {quality === selectedQuality && ' ✓'}
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default QualitySelector;
