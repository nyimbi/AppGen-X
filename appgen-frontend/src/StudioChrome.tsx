import { Icon } from './Icon'

const navItems = [
  { label: 'Forms', icon: 'form' as const, active: true },
  { label: 'Database', icon: 'database' as const },
  { label: 'Agents', icon: 'agent' as const },
  { label: 'Reports', icon: 'report' as const },
  { label: 'Targets', icon: 'desktop' as const },
]

export function StudioChrome() {
  return (
    <header className="studio-chrome">
      <div className="brand-block">
        <div className="brand-mark">AG</div>
        <div>
          <strong>AppGen Studio</strong>
          <span>Visual application builder</span>
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
        <button className="primary-action" type="button">
          <Icon name="workflow" />
          Generate
        </button>
      </div>
    </header>
  )
}
