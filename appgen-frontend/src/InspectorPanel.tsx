import { Icon } from './Icon'

const properties = [
  ['Name', 'LineItemsGrid'],
  ['Data source', 'Invoice.lines'],
  ['Lookup mode', 'Auto generated'],
  ['Context menu', 'PopupActions'],
  ['Validation', 'Required rows'],
  ['Target', 'Web, mobile, desktop'],
]

export function InspectorPanel() {
  return (
    <aside className="panel inspector-panel" aria-label="Object inspector">
      <div className="panel-title-row">
        <div>
          <p className="eyebrow">Selection</p>
          <h2>Inspector</h2>
        </div>
        <Icon name="grid" className="panel-title-icon" />
      </div>

      <div className="selected-card">
        <span className="component-icon category-data">
          <Icon name="grid" />
        </span>
        <div>
          <strong>Line Items</strong>
          <span>Data Grid</span>
        </div>
      </div>

      <div className="property-table">
        {properties.map(([name, value]) => (
          <div className="property-row" key={name}>
            <span>{name}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>

      <div className="inspector-actions">
        <button type="button">
          <Icon name="database" />
          Bind Field
        </button>
        <button type="button">
          <Icon name="popup" />
          Menu
        </button>
        <button type="button">
          <Icon name="workflow" />
          Add Event
        </button>
      </div>
    </aside>
  )
}
