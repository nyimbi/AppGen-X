import { Icon } from './Icon'

const statuses = [
  { label: 'DSL lint', value: 'Clean', icon: 'check' as const },
  { label: 'Bindings', value: '8 links', icon: 'database' as const },
  { label: 'Targets', value: '3 ready', icon: 'desktop' as const },
  { label: 'Agents', value: '2 staged', icon: 'agent' as const },
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
