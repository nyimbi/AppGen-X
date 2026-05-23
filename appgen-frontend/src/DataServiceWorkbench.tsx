import { Icon } from './Icon'
import { dataServiceCapabilities } from './dataServiceCatalog'
import type { DataServiceLane } from './dataServiceCatalog'

const laneOrder: DataServiceLane[] = ['Source', 'Query', 'Publish', 'Embedded DB', 'Resilience', 'Security']

export function DataServiceWorkbench() {
  return (
    <section className="panel data-service-workbench" aria-label="Data and service workbench">
      <div className="panel-title-row">
        <div>
          <p className="eyebrow">Data Services</p>
          <h2>Sources, Queries, Publishing</h2>
        </div>
        <Icon name="database" className="panel-title-icon" />
      </div>

      <div className="data-service-grid">
        {laneOrder.map((lane) => {
          const capabilities = dataServiceCapabilities.filter((capability) => capability.lane === lane)

          return (
            <article className="data-service-lane" key={lane}>
              <header>
                <strong>{lane}</strong>
                <span>{capabilities.length}</span>
              </header>
              <div className="data-service-list">
                {capabilities.map((capability) => (
                  <button className="data-service-card" key={capability.name} type="button">
                    <span className="component-icon category-data">
                      <Icon name={capability.icon} />
                    </span>
                    <span>
                      <strong>{capability.name}</strong>
                      <small>{capability.designSurface}</small>
                    </span>
                    <em>{capability.runtimeContract}</em>
                    <small>{capability.generationOutput}</small>
                  </button>
                ))}
              </div>
            </article>
          )
        })}
      </div>
    </section>
  )
}
