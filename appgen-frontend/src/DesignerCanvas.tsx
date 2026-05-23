import { Icon } from './Icon'

const placedComponents = [
  { name: 'Customer Name', icon: 'input' as const, x: 7, y: 9, w: 36 },
  { name: 'Invoice Date', icon: 'calendar' as const, x: 48, y: 9, w: 26 },
  { name: 'Line Items', icon: 'grid' as const, x: 7, y: 29, w: 67 },
  { name: 'Approval Agent', icon: 'agent' as const, x: 78, y: 29, w: 18 },
  { name: 'Totals Chart', icon: 'chart' as const, x: 7, y: 68, w: 30 },
]

export function DesignerCanvas() {
  return (
    <main className="panel designer-canvas" aria-label="Application designer">
      <div className="canvas-toolbar">
        <div>
          <p className="eyebrow">Design Surface</p>
          <h2>Invoice Workspace</h2>
        </div>
        <div className="toolbar-actions" aria-label="Canvas actions">
          <button type="button" title="Align selection">
            <Icon name="layout" />
          </button>
          <button type="button" title="Bind data">
            <Icon name="database" />
          </button>
          <button type="button" title="Preview target">
            <Icon name="desktop" />
          </button>
        </div>
      </div>

      <section className="canvas-grid" aria-label="Form canvas">
        <div className="form-frame">
          <div className="form-titlebar">
            <span>InvoiceForm</span>
            <span>12 columns</span>
          </div>
          {placedComponents.map((component) => (
            <button
              className="placed-component"
              key={component.name}
              style={{ left: `${component.x}%`, top: `${component.y}%`, width: `${component.w}%` }}
              type="button"
            >
              <Icon name={component.icon} />
              <span>{component.name}</span>
            </button>
          ))}
        </div>
      </section>
    </main>
  )
}
