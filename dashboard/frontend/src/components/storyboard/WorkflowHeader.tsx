import type { Engine } from '../../types/storyboard';

interface WorkflowHeaderProps {
  title: string;
  engines: Engine[];
  selectedEngine: string;
  onEngineChange: (engineId: string) => void;
  onClose?: () => void;
}

export function WorkflowHeader({
  title,
  engines,
  selectedEngine,
  onEngineChange,
  onClose
}: WorkflowHeaderProps) {
  return (
    <header className="workflow-header">
      <div className="workflow-title">
        <h1>{title}</h1>
      </div>

      <div className="workflow-controls">
        <div className="engine-selector">
          <select
            value={selectedEngine}
            onChange={(e) => onEngineChange(e.target.value)}
            className="engine-dropdown"
          >
            {engines.map(engine => (
              <option key={engine.id} value={engine.id}>
                {engine.name}
              </option>
            ))}
          </select>
          <button className="search-btn" aria-label="Search">
            🔍
          </button>
        </div>

        {onClose && (
          <button className="close-btn" onClick={onClose} aria-label="Close">
            ✕
          </button>
        )}
      </div>
    </header>
  );
}
