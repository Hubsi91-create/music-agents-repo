import { useState } from 'react';
import { Sidebar } from './Sidebar';
import { WorkflowHeader } from './WorkflowHeader';
import { AgentProgressBar } from './AgentProgressBar';
import { AudioPlayer } from './AudioPlayer';
import { VideoThumbnailGrid } from './VideoThumbnailGrid';
import {
  mockAgentProgress,
  mockVideoThumbnails,
  mockAudioTrack,
  mockEngines,
  mockNavItems
} from '../../data/storyboardMockData';
import './Storyboard.css';

interface StoryboardViewProps {
  onBack?: () => void;
}

export function StoryboardView({ onBack }: StoryboardViewProps = {}) {
  const [activeNavItem, setActiveNavItem] = useState('home');
  const [selectedEngine, setSelectedEngine] = useState(mockEngines[0].id);

  return (
    <div className="storyboard-container">
      <Sidebar
        navItems={mockNavItems}
        activeItem={activeNavItem}
        onItemClick={setActiveNavItem}
      />

      <div className="storyboard-main">
        <WorkflowHeader
          title="Music Video Workflow"
          engines={mockEngines}
          selectedEngine={selectedEngine}
          onEngineChange={setSelectedEngine}
          onClose={onBack}
        />

        <div className="storyboard-content">
          <div className="workflow-section">
            <div className="agents-section">
              <h2 className="section-title">Agent Progress</h2>
              <div className="agents-list">
                {mockAgentProgress.map(agent => (
                  <AgentProgressBar key={agent.id} agent={agent} />
                ))}
              </div>
            </div>

            <div className="bottom-section">
              <div className="audio-section">
                <AudioPlayer track={mockAudioTrack} />
              </div>
            </div>
          </div>

          <div className="preview-section">
            <VideoThumbnailGrid thumbnails={mockVideoThumbnails} />
          </div>
        </div>
      </div>
    </div>
  );
}
