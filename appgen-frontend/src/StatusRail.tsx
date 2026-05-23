import { Icon } from './Icon'
import { studioCatalogAudit } from './catalogAudit'

const catalogAudit = studioCatalogAudit()
const iconAudit = catalogAudit.componentAudit
const inspectorAudit = catalogAudit.inspectorAudit

const statuses = [
  { label: 'DSL lint', value: 'Clean', icon: 'check' as const },
  { label: 'Bindings', value: '8 links', icon: 'database' as const },
  { label: 'Targets', value: '3 ready', icon: 'desktop' as const },
  { label: 'Agents', value: '2 staged', icon: 'agent' as const },
  {
    label: 'Editors',
    value: inspectorAudit.ok ? `${inspectorAudit.totalEditors} mapped` : 'Review',
    icon: 'style' as const,
  },
  { label: 'Icons', value: iconAudit.ok ? `${iconAudit.totalComponents} mapped` : 'Review', icon: 'shape' as const },
]

export function StatusRail() {
  return (
    <section className="status-rail" aria-label="Workspace status">
      {statuses.map((status) => (
        <div className="status-card" key={status.label}>
          <Icon name={status.icon} />
          <span>{status.label}</span>
          <strong>{status.value}</strong>
        </div>
      ))}
    </section>
  )
}
