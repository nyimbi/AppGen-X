import { EmptyState } from '@appgen/ui-kit'
import { Icon } from './Icon'
import type { IconName } from './Icon'
import { loadSemanticService } from './studioApi'
import { useStudioData } from './useStudioData'

/**
 * The bridge panel reads the platform's shared-semantics report.
 *
 * The panel used to list the service names and designer surfaces from a
 * TypeScript module, so it could name a surface no designer implemented. The
 * ids and their contract formats now come from the workspace's own
 * `semantic_service` section; this module holds only the labels and icons to
 * render them with. A surface the backend does not report has no label, so the
 * panel cannot invent one.
 */
const SERVICE_LABELS: Record<string, { label: string; icon: IconName }> = {
  lsp: { label: 'Language service', icon: 'workflow' },
  designer_sync: { label: 'Designer sync', icon: 'layout' },
  graph_suite: { label: 'Graph suite', icon: 'flow' },
  natural_language_planner: { label: 'Change planner', icon: 'agent' },
}

const SURFACE_LABELS: Record<string, { label: string; icon: IconName }> = {
  dsl_editor: { label: 'DSL editor', icon: 'file' },
  component_palette: { label: 'Component palette', icon: 'drag' },
  form_designer: { label: 'Form designer', icon: 'form' },
  database_designer: { label: 'Database designer', icon: 'database' },
  workflow_designer: { label: 'Workflow designer', icon: 'workflow' },
  pbc_composition_designer: { label: 'PBC composition', icon: 'package' },
  package_deployment_designer: { label: 'Package deployment', icon: 'desktop' },
  diagnostics_panel: { label: 'Diagnostics', icon: 'rule' },
  graph_explain_panel: { label: 'Graphs and explain', icon: 'flow' },
  natural_language_planner: { label: 'Natural language planner', icon: 'bot' },
}

export function SemanticServicePanel() {
  const bridge = useStudioData(loadSemanticService)

  if (bridge.state === 'loading') {
    return (
      <section className="panel semantic-service-panel" aria-label="Semantic service bridge">
        <EmptyState description="Reading the shared-semantics report from the backend." title="Loading bridge" />
      </section>
    )
  }

  if (bridge.state === 'error') {
    return (
      <section className="panel semantic-service-panel" aria-label="Semantic service bridge">
        <EmptyState description={bridge.error.message} title="Could not load the bridge" />
      </section>
    )
  }

  const report = bridge.data.semantic_service
  const services = Object.entries(report.services)
  const surfaces = Object.entries(report.designer_surfaces)

  return (
    <section className="panel semantic-service-panel" aria-label="Semantic service bridge">
      <div className="semantic-service-header">
        <div>
          <p className="eyebrow">Shared Semantics</p>
          <h2>Editor And Designer Bridge</h2>
        </div>
        <span className={report.ok ? 'semantic-status semantic-status-ok' : 'semantic-status semantic-status-blocked'}>
          <Icon name={report.ok ? 'check' : 'rule'} />
          {report.ok ? 'Synced' : 'Blocked'}
        </span>
      </div>

      <div className="semantic-service-grid" aria-label="Semantic service contracts">
        {services.map(([id, format]) => (
          <button className="semantic-service-card" key={id} type="button" title={format}>
            <Icon name={SERVICE_LABELS[id]?.icon ?? 'service'} />
            <span>
              <strong>{SERVICE_LABELS[id]?.label ?? id}</strong>
              <small>{format}</small>
            </span>
          </button>
        ))}
      </div>

      <div className="semantic-surface-grid" aria-label="Designer surfaces using shared semantics">
        {surfaces.map(([id, surface]) => (
          <button
            className="semantic-surface-card"
            key={id}
            title={surface.format ?? id}
            type="button"
          >
            <Icon name={SURFACE_LABELS[id]?.icon ?? 'layout'} />
            <span>{SURFACE_LABELS[id]?.label ?? id}</span>
          </button>
        ))}
      </div>
    </section>
  )
}
