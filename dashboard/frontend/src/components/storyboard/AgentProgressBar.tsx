import type { AgentProgress } from '../../types/storyboard';
import { useEffect, useState } from 'react';

interface AgentProgressBarProps {
  agent: AgentProgress;
}

export function AgentProgressBar({ agent }: AgentProgressBarProps) {
  // Defensive: Provide defaults for all agent properties
  const agentId = agent?.id ?? 'unknown';
  const agentName = agent?.name ?? 'Unknown Agent';
  const agentProgress = agent?.progress ?? 0;
  const agentColor = agent?.color ?? '#3B82F6';

  const [animatedProgress, setAnimatedProgress] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedProgress(agentProgress);
    }, 100);

    return () => clearTimeout(timer);
  }, [agentProgress]);

  return (
    <div className="agent-progress-bar">
      <div className="agent-info">
        <span className="agent-name">Agent {agentId}: {agentName}</span>
        <span className="agent-percentage">{agentProgress}%</span>
      </div>
      <div className="progress-track">
        <div
          className="progress-fill"
          style={{
            width: `${animatedProgress}%`,
            backgroundColor: agentColor,
            transition: 'width 0.8s ease-out'
          }}
        />
      </div>
    </div>
  );
}
