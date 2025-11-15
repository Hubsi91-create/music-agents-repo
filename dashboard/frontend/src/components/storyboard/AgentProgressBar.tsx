import type { AgentProgress } from '../../types/storyboard';
import { useEffect, useState } from 'react';

interface AgentProgressBarProps {
  agent: AgentProgress;
}

export function AgentProgressBar({ agent }: AgentProgressBarProps) {
  const [animatedProgress, setAnimatedProgress] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedProgress(agent.progress);
    }, 100);

    return () => clearTimeout(timer);
  }, [agent.progress]);

  return (
    <div className="agent-progress-bar">
      <div className="agent-info">
        <span className="agent-name">Agent {agent.id}: {agent.name}</span>
        <span className="agent-percentage">{agent.progress}%</span>
      </div>
      <div className="progress-track">
        <div
          className="progress-fill"
          style={{
            width: `${animatedProgress}%`,
            backgroundColor: agent.color,
            transition: 'width 0.8s ease-out'
          }}
        />
      </div>
    </div>
  );
}
