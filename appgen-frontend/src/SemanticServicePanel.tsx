import { Icon } from './Icon'
import { semanticServiceAudit, semanticServices, semanticSurfaces } from './semanticServiceContract'

export function SemanticServicePanel() {
  const audit = semanticServiceAudit()

  return (
    <section className="panel semantic-service-panel" aria-label="Semantic service bridge">
      <div className="semantic-service-header">
        <div>
          <p className="eyebrow">Shared Semantics</p>
          <h2>Editor And Designer Bridge</h2>
        </div>
        <span className={audit.ok ? 'semantic-status semantic-status-ok' : 'semantic-status semantic-status-blocked'}>
          <Icon name={audit.ok ? 'check' : 'rule'} />
          {audit.ok ? 'Synced' : 'Blocked'}
        </span>
      </div>

      <div className="semantic-service-grid" aria-label="Semantic service contracts">
        {semanticServices.map((service) => (
          <button className="semantic-service-card" key={service.id} type="button" title={service.evidence}>
            <Icon name={service.icon} />
            <span>
              <strong>{service.label}</strong>
              <small>{service.evidence}</small>
            </span>
          </button>
        ))}
      </div>

      <div className="semantic-surface-grid" aria-label="Designer surfaces using shared semantics">
        {semanticSurfaces.map((surface) => (
          <button className="semantic-surface-card" key={surface.id} type="button" title={surface.contract}>
            <Icon name={surface.icon} />
            <span>{surface.label}</span>
          </button>
        ))}
      </div>
    </section>
  )
}
