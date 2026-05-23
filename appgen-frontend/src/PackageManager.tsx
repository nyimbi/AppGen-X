import { Icon } from './Icon'
import { designPackages } from './packageCatalog'

export function PackageManager() {
  return (
    <section className="panel package-manager" aria-label="Design-time package manager">
      <div className="panel-title-row">
        <div>
          <p className="eyebrow">Packages</p>
          <h2>Component Installation</h2>
        </div>
        <Icon name="package" className="panel-title-icon" />
      </div>

      <div className="package-grid">
        {designPackages.map((item) => (
          <article className={`package-card package-${item.state}`} key={item.name}>
            <div className="package-card-title">
              <span className="component-icon category-layouts">
                <Icon name={item.icon} />
              </span>
              <span>
                <strong>{item.name}</strong>
                <small>
                  {item.vendor} {item.version}
                </small>
              </span>
              <em>{item.state}</em>
            </div>
            <div className="package-components">
              {item.components.map((component) => (
                <span key={`${item.name}-${component}`}>{component}</span>
              ))}
            </div>
            <div className="package-footer">
              <span>
                <Icon name={item.trust === 'signed' ? 'lock' : 'check'} />
                {item.trust}
              </span>
              <button type="button">
                <Icon name={item.state === 'installed' ? 'check' : 'upload'} />
                {item.state === 'installed' ? 'Installed' : item.state === 'update' ? 'Update' : 'Install'}
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
