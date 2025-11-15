import type { NavItem } from '../../types/storyboard';

interface SidebarProps {
  navItems: NavItem[];
  activeItem: string;
  onItemClick: (id: string) => void;
}

export function Sidebar({ navItems, activeItem, onItemClick }: SidebarProps) {
  // Defensive: Handle undefined navItems array
  const validNavItems = navItems ?? [];
  const sections = validNavItems.filter(item => item?.type === 'section');
  const projects = validNavItems.filter(item => item?.type === 'project');

  return (
    <aside className="storyboard-sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-logo">🎵 Music Agents</h2>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section">
          {sections.map((item, index) => (
            <button
              key={item?.id ?? `section-${index}`}
              className={`nav-item ${activeItem === item?.id ? 'active' : ''}`}
              onClick={() => onItemClick(item?.id ?? '')}
            >
              <span className="nav-icon">{item?.icon ?? '📁'}</span>
              <span className="nav-label">{item?.label ?? 'Unknown'}</span>
            </button>
          ))}
        </div>

        {projects.length > 0 && (
          <div className="nav-section">
            <h3 className="nav-section-title">Projects</h3>
            {projects.map((item, index) => (
              <button
                key={item?.id ?? `project-${index}`}
                className={`nav-item ${activeItem === item?.id ? 'active' : ''}`}
                onClick={() => onItemClick(item?.id ?? '')}
              >
                <span className="nav-icon">{item?.icon ?? '🎵'}</span>
                <span className="nav-label">{item?.label ?? 'Unknown Project'}</span>
              </button>
            ))}
          </div>
        )}
      </nav>
    </aside>
  );
}
