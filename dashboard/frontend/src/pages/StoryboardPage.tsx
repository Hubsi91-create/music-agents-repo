import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import VideoPlayer from '../components/player/VideoPlayer';
import TimelineEditor from '../components/editor/TimelineEditor';
import { SceneData } from '../types';
import axios from 'axios';

/**
 * Storyboard Page Component
 *
 * Integrates both:
 * - Timeline Editor (for editing scenes)
 * - Video Player (for previewing rendered video)
 *
 * Features tabs to switch between views
 */
const StoryboardPage = () => {
  const [activeTab, setActiveTab] = useState<'timeline' | 'preview'>('timeline');
  const [projectId] = useState('project-1');
  const [scenes, setScenes] = useState<SceneData[]>([]);
  const [musicDuration, setMusicDuration] = useState(120);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load project data
  useEffect(() => {
    loadProjectData();
  }, []);

  const loadProjectData = async () => {
    try {
      setIsLoading(true);

      // Load scenes from backend
      const response = await axios.get(`/api/projects/${projectId}`);

      if (response.data.success) {
        const projectData = response.data.data;
        setScenes(projectData.scenes || generateMockScenes());
        setMusicDuration(projectData.musicDuration || 120);
        setVideoUrl(projectData.videoUrl || null);
      } else {
        // Use mock data if API fails
        setScenes(generateMockScenes());
        setMusicDuration(120);
      }
    } catch (error) {
      console.error('Failed to load project data:', error);
      // Use mock data as fallback
      setScenes(generateMockScenes());
      setMusicDuration(120);
    } finally {
      setIsLoading(false);
    }
  };

  const generateMockScenes = (): SceneData[] => {
    return [
      {
        id: 'scene-1',
        sceneNumber: 1,
        startTime: 0,
        duration: 10,
        prompt: 'A futuristic cityscape with neon lights and flying cars at night',
        style: 'Cyberpunk',
        agent: 'Agent 1',
        color: 'rgba(255, 107, 107, 0.8)'
      },
      {
        id: 'scene-2',
        sceneNumber: 2,
        startTime: 10,
        duration: 15,
        prompt: 'Close-up of a musician playing an electric guitar with dramatic lighting',
        style: 'Cinematic',
        agent: 'Agent 2',
        color: 'rgba(78, 205, 196, 0.8)'
      },
      {
        id: 'scene-3',
        sceneNumber: 3,
        startTime: 25,
        duration: 12,
        prompt: 'Abstract visualization of sound waves morphing into colorful patterns',
        style: 'Abstract',
        agent: 'Agent 3',
        color: 'rgba(255, 195, 113, 0.8)'
      },
      {
        id: 'scene-4',
        sceneNumber: 4,
        startTime: 37,
        duration: 18,
        prompt: 'Crowd at a concert dancing and singing, aerial drone shot',
        style: 'Documentary',
        agent: 'Agent 4',
        color: 'rgba(162, 155, 254, 0.8)'
      },
      {
        id: 'scene-5',
        sceneNumber: 5,
        startTime: 55,
        duration: 20,
        prompt: 'Transition through different music eras: 70s, 80s, 90s, modern',
        style: 'Retro Montage',
        agent: 'Agent 5',
        color: 'rgba(255, 159, 243, 0.8)'
      }
    ];
  };

  const handleScenesChange = (updatedScenes: SceneData[]) => {
    setScenes(updatedScenes);
  };

  const handleSave = async () => {
    try {
      await axios.post(`/api/projects/${projectId}/save`, {
        scenes,
        musicDuration
      });
      alert('Project saved successfully!');
    } catch (error) {
      console.error('Failed to save:', error);
      alert('Failed to save project. See console for details.');
    }
  };

  const handleExport = (format: 'json' | 'runway' | 'veo') => {
    console.log(`Exporting as ${format}...`);
  };

  if (isLoading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        background: '#0a0e27',
        color: '#e0e8ff'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '60px',
            height: '60px',
            border: '4px solid rgba(0, 240, 255, 0.2)',
            borderTopColor: '#00f0ff',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem'
          }}></div>
          <p>Loading project...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: '#0a0e27',
      padding: '2rem'
    }}>
      {/* Page Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          marginBottom: '2rem',
          textAlign: 'center'
        }}
      >
        <h1 style={{
          margin: 0,
          fontSize: '2.5rem',
          fontWeight: 700,
          color: '#e0e8ff',
          textShadow: '0 0 20px rgba(0, 240, 255, 0.5)'
        }}>
          🎬 Storyboard Studio
        </h1>
        <p style={{
          margin: '0.5rem 0 0',
          color: 'rgba(224, 232, 255, 0.7)',
          fontSize: '1.1rem'
        }}>
          Professional Video Timeline Editor + Preview Player
        </p>
      </motion.div>

      {/* Tab Navigation */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          display: 'flex',
          gap: '1rem',
          justifyContent: 'center',
          marginBottom: '2rem'
        }}
      >
        <TabButton
          active={activeTab === 'timeline'}
          onClick={() => setActiveTab('timeline')}
          icon="📊"
          label="Timeline Editor"
        />
        <TabButton
          active={activeTab === 'preview'}
          onClick={() => setActiveTab('preview')}
          icon="▶️"
          label="Video Preview"
          disabled={!videoUrl}
        />
      </motion.div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        {activeTab === 'timeline' && (
          <motion.div
            key="timeline"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.3 }}
          >
            <TimelineEditor
              projectId={projectId}
              initialScenes={scenes}
              musicDuration={musicDuration}
              onScenesChange={handleScenesChange}
              onSave={handleSave}
              onExport={handleExport}
            />
          </motion.div>
        )}

        {activeTab === 'preview' && (
          <motion.div
            key="preview"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {videoUrl ? (
              <VideoPlayer
                videoUrl={videoUrl}
                title="Storyboard Preview"
                duration={musicDuration}
                autoPlay={false}
              />
            ) : (
              <div style={{
                padding: '4rem 2rem',
                textAlign: 'center',
                background: '#1a1f3a',
                borderRadius: '12px',
                border: '1px solid rgba(0, 240, 255, 0.2)'
              }}>
                <h2 style={{
                  color: '#e0e8ff',
                  marginBottom: '1rem'
                }}>
                  No Video Available
                </h2>
                <p style={{
                  color: 'rgba(224, 232, 255, 0.7)',
                  marginBottom: '2rem'
                }}>
                  Render your timeline to generate a preview video.
                </p>
                <button style={{
                  padding: '1rem 2rem',
                  background: 'rgba(0, 240, 255, 0.2)',
                  border: '1px solid #00f0ff',
                  borderRadius: '8px',
                  color: '#00f0ff',
                  fontSize: '1rem',
                  cursor: 'pointer',
                  transition: 'all 300ms ease'
                }}>
                  Render Video
                </button>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// Tab Button Component
interface TabButtonProps {
  active: boolean;
  onClick: () => void;
  icon: string;
  label: string;
  disabled?: boolean;
}

const TabButton = ({ active, onClick, icon, label, disabled }: TabButtonProps) => (
  <motion.button
    onClick={onClick}
    disabled={disabled}
    whileHover={!disabled ? { scale: 1.05 } : {}}
    whileTap={!disabled ? { scale: 0.95 } : {}}
    style={{
      display: 'flex',
      alignItems: 'center',
      gap: '0.75rem',
      padding: '1rem 2rem',
      background: active
        ? 'rgba(0, 240, 255, 0.2)'
        : disabled
        ? 'rgba(26, 31, 58, 0.5)'
        : 'rgba(26, 31, 58, 0.8)',
      border: active
        ? '2px solid #00f0ff'
        : '1px solid rgba(0, 240, 255, 0.2)',
      borderRadius: '8px',
      color: active ? '#00f0ff' : disabled ? 'rgba(224, 232, 255, 0.3)' : '#e0e8ff',
      fontSize: '1rem',
      fontWeight: active ? 600 : 400,
      cursor: disabled ? 'not-allowed' : 'pointer',
      transition: 'all 300ms ease',
      boxShadow: active ? '0 0 20px rgba(0, 240, 255, 0.3)' : 'none',
      opacity: disabled ? 0.5 : 1
    }}
  >
    <span style={{ fontSize: '1.5rem' }}>{icon}</span>
    <span>{label}</span>
  </motion.button>
);

export default StoryboardPage;
