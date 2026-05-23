import { Icon } from './Icon'

const placedComponents = [
  { name: 'Main Menu', icon: 'menu' as const, x: 4, y: 4, w: 92 },
  { name: 'Customer Name', icon: 'input' as const, x: 7, y: 16, w: 36 },
  { name: 'Account Lookup', icon: 'lookup' as const, x: 48, y: 16, w: 26 },
  { name: 'Invoice Date', icon: 'calendar' as const, x: 77, y: 16, w: 19 },
  { name: 'Line Items', icon: 'grid' as const, x: 7, y: 35, w: 67 },
  { name: 'Popup Actions', icon: 'popup' as const, x: 78, y: 35, w: 18 },
  { name: 'Approval Agent', icon: 'agent' as const, x: 78, y: 49, w: 18 },
  { name: 'Totals Chart', icon: 'chart' as const, x: 7, y: 73, w: 30 },
  { name: 'Receipt Camera', icon: 'camera' as const, x: 41, y: 73, w: 24 },
  { name: 'Mobile Target', icon: 'mobile' as const, x: 69, y: 73, w: 27 },
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
          <button type="button" title="Edit menu">
            <Icon name="menu" />
          </button>
          <button type="button" title="Edit context menu">
            <Icon name="popup" />
          </button>
          <button type="button" title="Bind data">
            <Icon name="database" />
          </button>
          <button type="button" title="Preview target">
            <Icon name="mobile" />
          </button>
        </div>
      </div>

      <section className="canvas-grid" aria-label="Form canvas">
        <div className="form-frame">
          <div className="form-titlebar">
            <span>InvoiceForm</span>
            <span>
              <Icon name="grid" />
              12 columns
            </span>
          </div>
          <div className="canvas-rulers" aria-hidden="true">
            <span>0</span>
            <span>320</span>
            <span>640</span>
            <span>960</span>
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
