import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { EditorControlsProps } from '../../types';
import styles from './EditorStyles.module.css';

/**
 * Editor Control Buttons Component
 *
 * Features:
 * - Playback controls (Play/Pause/Stop)
 * - Zoom controls (In/Out)
 * - Save/Export buttons with dropdown
 * - Undo/Redo buttons
 * - Delete button
 * - All with Neon styling
 */
const EditorControls = ({
  isPlaying,
  zoomLevel,
  canUndo,
  canRedo,
  onPlay,
  onPause,
  onStop,
  onZoomIn,
  onZoomOut,
  onSave,
  onExport,
  onDownload,
  onUndo,
  onRedo,
  onDelete
}: EditorControlsProps) => {
  const [showExportMenu, setShowExportMenu] = useState(false);

  return (
    <div className={styles.controls}>
      {/* Playback Controls */}
      <div className={styles.controlGroup}>
        <span className={styles.groupLabel}>Playback</span>
        <div className={styles.buttonRow}>
          {!isPlaying ? (
            <motion.button
              className={`${styles.controlBtn} ${styles.playBtn}`}
              onClick={onPlay}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z" />
              </svg>
              Play
            </motion.button>
          ) : (
            <motion.button
              className={`${styles.controlBtn} ${styles.pauseBtn}`}
              onClick={onPause}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
              </svg>
              Pause
            </motion.button>
          )}

          <motion.button
            className={`${styles.controlBtn} ${styles.stopBtn}`}
            onClick={onStop}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <rect x="6" y="6" width="12" height="12" />
            </svg>
            Stop
          </motion.button>
        </div>
      </div>

      {/* Zoom Controls */}
      <div className={styles.controlGroup}>
        <span className={styles.groupLabel}>Zoom</span>
        <div className={styles.buttonRow}>
          <motion.button
            className={`${styles.controlBtn} ${styles.zoomBtn}`}
            onClick={onZoomOut}
            disabled={zoomLevel <= 0.5}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
              <path d="M7 9h5v1H7z" />
            </svg>
          </motion.button>

          <span className={styles.zoomDisplay}>
            {(zoomLevel * 100).toFixed(0)}%
          </span>

          <motion.button
            className={`${styles.controlBtn} ${styles.zoomBtn}`}
            onClick={onZoomIn}
            disabled={zoomLevel >= 2}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
              <path d="M12 10h-2v2H9v-2H7V9h2V7h1v2h2v1z" />
            </svg>
          </motion.button>
        </div>
      </div>

      {/* Project Controls */}
      <div className={styles.controlGroup}>
        <span className={styles.groupLabel}>Project</span>
        <div className={styles.buttonRow}>
          <motion.button
            className={`${styles.controlBtn} ${styles.saveBtn}`}
            onClick={onSave}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M17 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z" />
            </svg>
            Save
          </motion.button>

          {/* Export Dropdown */}
          <div className={styles.exportContainer}>
            <motion.button
              className={`${styles.controlBtn} ${styles.exportBtn}`}
              onClick={() => setShowExportMenu(!showExportMenu)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2z" />
              </svg>
              Export ▼
            </motion.button>

            <AnimatePresence>
              {showExportMenu && (
                <motion.div
                  className={styles.exportMenu}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  <button onClick={() => { onExport('json'); setShowExportMenu(false); }}>
                    JSON Format
                  </button>
                  <button onClick={() => { onExport('runway'); setShowExportMenu(false); }}>
                    Runway Format
                  </button>
                  <button onClick={() => { onExport('veo'); setShowExportMenu(false); }}>
                    Veo Format
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <motion.button
            className={`${styles.controlBtn} ${styles.downloadBtn}`}
            onClick={onDownload}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z" />
            </svg>
            Download
          </motion.button>
        </div>
      </div>

      {/* Edit Controls */}
      <div className={styles.controlGroup}>
        <span className={styles.groupLabel}>Edit</span>
        <div className={styles.buttonRow}>
          <motion.button
            className={`${styles.controlBtn} ${styles.undoBtn}`}
            onClick={onUndo}
            disabled={!canUndo}
            whileHover={{ scale: canUndo ? 1.05 : 1 }}
            whileTap={{ scale: canUndo ? 0.95 : 1 }}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12.5 8c-2.65 0-5.05.99-6.9 2.6L2 7v9h9l-3.62-3.62c1.39-1.16 3.16-1.88 5.12-1.88 3.54 0 6.55 2.31 7.6 5.5l2.37-.78C21.08 11.03 17.15 8 12.5 8z" />
            </svg>
            Undo
          </motion.button>

          <motion.button
            className={`${styles.controlBtn} ${styles.redoBtn}`}
            onClick={onRedo}
            disabled={!canRedo}
            whileHover={{ scale: canRedo ? 1.05 : 1 }}
            whileTap={{ scale: canRedo ? 0.95 : 1 }}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M18.4 10.6C16.55 8.99 14.15 8 11.5 8c-4.65 0-8.58 3.03-9.96 7.22L3.9 16c1.05-3.19 4.05-5.5 7.6-5.5 1.95 0 3.73.72 5.12 1.88L13 16h9V7l-3.6 3.6z" />
            </svg>
            Redo
          </motion.button>

          <motion.button
            className={`${styles.controlBtn} ${styles.deleteBtn}`}
            onClick={onDelete}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
            </svg>
            Delete
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default EditorControls;
