import { useEffect, useRef, useState } from 'react';
import { WaveformDisplayProps } from '../../types';
import styles from './EditorStyles.module.css';

/**
 * Waveform Display Component
 *
 * Displays audio waveform visualization as background
 * Uses Web Audio API to extract PCM data (if available)
 * Falls back to placeholder visualization
 */
const WaveformDisplay = ({
  audioUrl,
  duration,
  height = 100,
  opacity = 0.2
}: WaveformDisplayProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [waveformData, setWaveformData] = useState<number[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!audioUrl) {
      // Generate placeholder waveform
      generatePlaceholderWaveform();
      return;
    }

    // Try to load and analyze audio
    loadAudioWaveform(audioUrl);
  }, [audioUrl, duration]);

  // Draw waveform whenever data changes
  useEffect(() => {
    if (waveformData.length > 0) {
      drawWaveform();
    }
  }, [waveformData, height]);

  const generatePlaceholderWaveform = () => {
    // Generate a simple sine wave pattern
    const samples = 200;
    const data = [];

    for (let i = 0; i < samples; i++) {
      const t = i / samples;
      const value = Math.sin(t * Math.PI * 8) * 0.5 + 0.5;
      data.push(value);
    }

    setWaveformData(data);
    setIsLoading(false);
  };

  const loadAudioWaveform = async (url: string) => {
    try {
      // Fetch audio file
      const response = await fetch(url);
      const arrayBuffer = await response.arrayBuffer();

      // Create audio context
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

      // Extract channel data
      const channelData = audioBuffer.getChannelData(0);
      const samples = 200;
      const blockSize = Math.floor(channelData.length / samples);
      const data = [];

      // Downsample to 200 points
      for (let i = 0; i < samples; i++) {
        let sum = 0;
        for (let j = 0; j < blockSize; j++) {
          sum += Math.abs(channelData[i * blockSize + j]);
        }
        const average = sum / blockSize;
        data.push(average);
      }

      // Normalize to 0-1 range
      const max = Math.max(...data);
      const normalized = data.map(v => v / max);

      setWaveformData(normalized);
      setIsLoading(false);
    } catch (error) {
      console.error('Failed to load audio waveform:', error);
      generatePlaceholderWaveform();
    }
  };

  const drawWaveform = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const canvasHeight = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, canvasHeight);

    // Draw waveform
    ctx.beginPath();
    ctx.strokeStyle = `rgba(0, 240, 255, ${opacity})`;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    const barWidth = width / waveformData.length;
    const centerY = canvasHeight / 2;

    for (let i = 0; i < waveformData.length; i++) {
      const x = i * barWidth;
      const amplitude = waveformData[i] * (canvasHeight / 2);

      if (i === 0) {
        ctx.moveTo(x, centerY - amplitude);
      } else {
        ctx.lineTo(x, centerY - amplitude);
      }
    }

    ctx.stroke();

    // Draw mirror (bottom half)
    ctx.beginPath();
    for (let i = 0; i < waveformData.length; i++) {
      const x = i * barWidth;
      const amplitude = waveformData[i] * (canvasHeight / 2);

      if (i === 0) {
        ctx.moveTo(x, centerY + amplitude);
      } else {
        ctx.lineTo(x, centerY + amplitude);
      }
    }

    ctx.stroke();

    // Fill area
    ctx.globalAlpha = opacity * 0.3;
    ctx.fillStyle = '#00f0ff';

    ctx.beginPath();
    ctx.moveTo(0, centerY);

    for (let i = 0; i < waveformData.length; i++) {
      const x = i * barWidth;
      const amplitude = waveformData[i] * (canvasHeight / 2);
      ctx.lineTo(x, centerY - amplitude);
    }

    for (let i = waveformData.length - 1; i >= 0; i--) {
      const x = i * barWidth;
      const amplitude = waveformData[i] * (canvasHeight / 2);
      ctx.lineTo(x, centerY + amplitude);
    }

    ctx.closePath();
    ctx.fill();
  };

  return (
    <div className={styles.waveform} style={{ height: `${height}px` }}>
      {isLoading && (
        <div className={styles.waveformLoading}>
          Loading waveform...
        </div>
      )}
      <canvas
        ref={canvasRef}
        width={1000}
        height={height}
        className={styles.waveformCanvas}
      />
    </div>
  );
};

export default WaveformDisplay;
