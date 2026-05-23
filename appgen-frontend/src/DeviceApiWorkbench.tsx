import { Icon } from './Icon'
import { deviceApiCapabilities } from './deviceApiCatalog'
import type { DeviceApiGroup } from './deviceApiCatalog'

const groupOrder: DeviceApiGroup[] = [
  'Sensors',
  'Media',
  'Connectivity',
  'Storage',
  'Security',
  'Notifications',
  'Background',
  'Permissions',
]

export function DeviceApiWorkbench() {
  return (
    <section className="panel device-api-workbench" aria-label="Device API workbench">
      <div className="panel-title-row">
        <div>
          <p className="eyebrow">Device APIs</p>
          <h2>Native Capability Coverage</h2>
        </div>
        <Icon name="mobile" className="panel-title-icon" />
      </div>

      <div className="device-api-grid">
        {groupOrder.map((group) => {
          const capabilities = deviceApiCapabilities.filter((capability) => capability.group === group)

          return (
            <article className="device-api-group" key={group}>
              <header>
                <strong>{group}</strong>
                <span>{capabilities.length}</span>
              </header>
              <div className="device-api-list">
                {capabilities.map((capability) => (
                  <div className="device-api-card" key={capability.name}>
                    <span className="component-icon category-device">
                      <Icon name={capability.icon} />
                    </span>
                    <div>
                      <strong>{capability.name}</strong>
                      <small>{capability.permission}</small>
                    </div>
                    <em>{capability.adapters.join(' + ')}</em>
                    <p>{capability.privacy}</p>
                    <span className="device-api-fallback">{capability.fallback}</span>
                  </div>
                ))}
              </div>
            </article>
          )
        })}
      </div>
    </section>
  )
}
