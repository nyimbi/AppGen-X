import { Badge, EmptyState, PageHeader } from '@appgen/ui-kit'
import { Icon } from './Icon'
import type { IconName } from './Icon'
import { loadDataServices } from './studioApi'
import type { DataServiceLane } from './studioApi'
import { useStudioData } from './useStudioData'

/**
 * The workbench renders the platform's data tooling, not a description of it.
 *
 * The panel listed eight capabilities written in TypeScript, each with a prose
 * description of what it would do, so it could describe a designer that does
 * not exist and miss sixty contracts that do. Each lane now carries the
 * contracts it renders and each contract its own `format`, so a capability
 * without a real payload cannot appear.
 */

const LANE_ICONS: Record<string, IconName> = {
  Source: 'database',
  Query: 'query',
  Publish: 'api',
  'Embedded DB': 'dataset',
  Resilience: 'workflow',
  Security: 'lock',
}

/** A capability's evidence is a contract; its `format` is the one readable claim. */
function evidenceSummary(evidence: Record<string, unknown>): string {
  const lists = Object.entries(evidence).filter(
    ([key, value]) => key !== 'format' && Array.isArray(value) && value.length > 0,
  )
  const [first] = lists
  if (!first) return 'contract'
  const [key, value] = first
  return `${(value as unknown[]).length} ${key.replace(/_/g, ' ')}`
}

function Lane({ lane }: { lane: DataServiceLane }) {
  return (
    <article className="data-service-lane">
      <header>
        <Icon name={LANE_ICONS[lane.lane] ?? 'database'} />
        <strong>{lane.lane}</strong>
        <span>{lane.capabilities.length}</span>
      </header>
      <div className="data-service-list">
        {lane.capabilities.map((capability) => (
          <button
            className="data-service-card"
            key={capability.key}
            title={capability.format}
            type="button"
          >
            <span className="component-icon category-data">
              <Icon name={LANE_ICONS[lane.lane] ?? 'database'} />
            </span>
            <span>
              <strong>{capability.key.replace(/_/g, ' ')}</strong>
              <small>{capability.format}</small>
            </span>
            <em>{evidenceSummary(capability.evidence)}</em>
          </button>
        ))}
      </div>
    </article>
  )
}

export function DataServiceWorkbench() {
  const services = useStudioData(loadDataServices)

  if (services.state === 'loading') {
    return (
      <section className="panel data-service-workbench" aria-label="Data and service workbench">
        <EmptyState description="Reading the data tooling contracts from the backend." title="Loading data services" />
      </section>
    )
  }

  if (services.state === 'error') {
    return (
      <section className="panel data-service-workbench" aria-label="Data and service workbench">
        <EmptyState description={services.error.message} title="Could not load data services" />
      </section>
    )
  }

  const report = services.data

  return (
    <section className="panel data-service-workbench" aria-label="Data and service workbench">
      <PageHeader
        actions={
          <Badge tone={report.decision === 'approved' ? 'success' : 'warning'}>{report.decision}</Badge>
        }
        description={`${report.lanes.reduce((count, lane) => count + lane.capabilities.length, 0)} contracts across ${report.lanes.length} lanes`}
        title="Sources, Queries, Publishing"
      />

      <div className="data-service-grid">
        {report.lanes.map((lane) => (
          <Lane key={lane.lane} lane={lane} />
        ))}
      </div>

      <div className="readiness-strip" aria-label="Data tooling readiness">
        <p className="eyebrow">
          <Icon name={report.readiness.ok ? 'check' : 'rule'} />
          Readiness
        </p>
        {report.readiness.phases.map((phase) => (
          <span className={phase.ok ? 'readiness-phase' : 'readiness-phase readiness-phase-blocked'} key={phase.phase}>
            {phase.phase.replace(/_/g, ' ')}
            <small>{phase.steps.length} steps</small>
          </span>
        ))}
      </div>
    </section>
  )
}
