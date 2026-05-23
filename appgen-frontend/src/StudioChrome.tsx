import { Icon } from './Icon'

const navItems = [
  { label: 'Forms', icon: 'form' as const, active: true },
  { label: 'Database', icon: 'database' as const },
  { label: 'Agents', icon: 'agent' as const },
  { label: 'Reports', icon: 'report' as const },
  { label: 'Packages', icon: 'package' as const },
  { label: 'Targets', icon: 'mobile' as const },
]

export function StudioChrome() {
  return (
    <header className="studio-chrome">
      <div className="brand-block">
        <div className="brand-mark" aria-hidden="true">
          <Icon name="layout" />
        </div>
        <div>
          <strong>AppGen Studio</strong>
          <span>Low-code application workbench</span>
        </div>
      </div>

      <nav className="workspace-nav" aria-label="Workspace navigation">
        {navItems.map((item) => (
          <button className={item.active ? 'active' : ''} key={item.label} type="button">
            <Icon name={item.icon} />
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="command-strip">
        <label className="command-input">
          <Icon name="search" />
          <input aria-label="Command search" placeholder="Command or natural language change" />
        </label>
        <div className="command-modes" aria-label="Generation modes">
          <span>
            <Icon name="database" />
            Schema
          </span>
          <span>
            <Icon name="form" />
            UI
          </span>
          <span>
            <Icon name="agent" />
            Agents
          </span>
        </div>
        <button className="primary-action" type="button">
          <Icon name="workflow" />
          Generate
        </button>
      </div>
    </header>
  )
}
