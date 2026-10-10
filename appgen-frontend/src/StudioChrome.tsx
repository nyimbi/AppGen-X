import { Button } from '@appgen/ui-kit'
import { Icon } from './Icon'
import { studioSections } from './studioSections'

export type StudioChromeProps = {
  /** The section the nav should mark active. */
  activeSection: string
  /** Called with a section id when the user picks one. */
  onSectionChange: (id: string) => void
}

export function StudioChrome({ activeSection, onSectionChange }: StudioChromeProps) {
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
        {studioSections.map((item) => (
          <button
            aria-current={item.id === activeSection ? 'page' : undefined}
            className={item.id === activeSection ? 'active' : ''}
            key={item.id}
            onClick={() => onSectionChange(item.id)}
            type="button"
          >
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
        <Button leading={<Icon name="workflow" />}>Generate</Button>
      </div>
    </header>
  )
}
