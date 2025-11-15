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
  // Defensive: Provide defaults for all props
  const headerTitle = title ?? 'Music Video Workflow';
  const validEngines = engines ?? [];
  const currentEngine = selectedEngine ?? '';

  return (
    <header className="workflow-header">
      <div className="workflow-title">
        <h1>{headerTitle}</h1>
      </div>

      <div className="workflow-controls">
        <div className="engine-selector">
          <select
            value={currentEngine}
            onChange={(e) => onEngineChange(e.target.value)}
            className="engine-dropdown"
          >
            {validEngines.length > 0 ? (
              validEngines.map((engine, index) => (
                <option key={engine?.id ?? `engine-${index}`} value={engine?.id ?? ''}>
                  {engine?.name ?? 'Unknown Engine'}
                </option>
              ))
            ) : (
              <option value="">No engines available</option>
            )}
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
