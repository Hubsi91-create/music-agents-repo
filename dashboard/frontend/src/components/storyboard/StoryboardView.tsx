import { useState } from 'react';
import { Sidebar } from './Sidebar';
import { WorkflowHeader } from './WorkflowHeader';
import { AgentProgressBar } from './AgentProgressBar';
import { AudioPlayer } from './AudioPlayer';
import { VideoThumbnailGrid } from './VideoThumbnailGrid';
import {
  useAgentProgress,
  useVideoThumbnails,
  useAudioTrack,
  useEngines,
  useNavItems,
} from '../../hooks/useStoryboardApi';
import './Storyboard.css';

interface StoryboardViewProps {
  onBack?: () => void;
}

export function StoryboardView({ onBack }: StoryboardViewProps = {}) {
  const [activeNavItem, setActiveNavItem] = useState('project1'); // Start mit erstem Projekt
  const [selectedEngine, setSelectedEngine] = useState('');

  // Determine if activeNavItem is a project (starts with 'project')
  const selectedProjectId = activeNavItem.startsWith('project') ? activeNavItem : 'project1';

  // API Data Fetching mit React Query (mit projectId)
  const { data: agentProgress, isLoading: isLoadingAgents, isError: isErrorAgents } = useAgentProgress(selectedProjectId, { refetchInterval: 5000 });
  const { data: videoThumbnails, isLoading: isLoadingThumbnails, isError: isErrorThumbnails } = useVideoThumbnails(selectedProjectId);
  const { data: audioTrack, isLoading: isLoadingAudio, isError: isErrorAudio } = useAudioTrack(selectedProjectId);
  const { data: enginesData, isLoading: isLoadingEngines, isError: isErrorEngines } = useEngines();
  const { data: navItems, isLoading: isLoadingNav, isError: isErrorNav } = useNavItems();

  // Engines aus API-Response extrahieren
  const engines = enginesData?.engines.map(engine => ({
    id: engine.id,
    name: engine.name,
    type: 'ai' as const, // Alle Runway-Engines sind AI-basiert
  })) || [];

  // Setze Default-Engine, wenn noch nicht gesetzt
  if (!selectedEngine && engines.length > 0) {
    setSelectedEngine(engines[0].id);
  }

  // Loading State
  if (isLoadingAgents || isLoadingThumbnails || isLoadingAudio || isLoadingEngines || isLoadingNav) {
    return (
      <div className="storyboard-container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading Storyboard...</p>
        </div>
      </div>
    );
  }

  // Error State
  if (isErrorAgents || isErrorThumbnails || isErrorAudio || isErrorEngines || isErrorNav) {
    return (
      <div className="storyboard-container">
        <div className="error-container">
          <h2>Error Loading Storyboard</h2>
          <p>Failed to load data from the backend. Please check if the backend is running.</p>
          {onBack && (
            <button onClick={onBack} className="error-back-button">
              Go Back
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="storyboard-container">
      <Sidebar
        navItems={navItems || []}
        activeItem={activeNavItem}
        onItemClick={setActiveNavItem}
      />

      <div className="storyboard-main">
        <WorkflowHeader
          title={`Music Video Workflow - ${navItems?.find(item => item.id === selectedProjectId)?.label || 'Project'}`}
          engines={engines}
          selectedEngine={selectedEngine}
          onEngineChange={setSelectedEngine}
          onClose={onBack}
        />

        <div className="storyboard-content">
          <div className="workflow-section">
            <div className="agents-section">
              <h2 className="section-title">Agent Progress</h2>
              <div className="agents-list">
                {agentProgress?.map(agent => (
                  <AgentProgressBar key={agent.id} agent={agent} />
                ))}
              </div>
            </div>

            <div className="bottom-section">
              <div className="audio-section">
                {audioTrack && <AudioPlayer track={audioTrack} />}
              </div>
            </div>
          </div>

          <div className="preview-section">
            <VideoThumbnailGrid thumbnails={videoThumbnails || []} />
          </div>
        </div>
      </div>
    </div>
  );
}
