import { Icon } from './Icon'

const placedComponents = [
  { name: 'Main Menu', icon: 'menu' as const, x: 4, y: 4, w: 92, tone: 'navigation' },
  { name: 'Customer Name', icon: 'input' as const, x: 7, y: 16, w: 36, tone: 'inputs' },
  { name: 'Account Lookup', icon: 'lookup' as const, x: 48, y: 16, w: 26, tone: 'choice' },
  { name: 'Invoice Date', icon: 'calendar' as const, x: 77, y: 16, w: 19, tone: 'inputs' },
  { name: 'Line Items', icon: 'grid' as const, x: 7, y: 35, w: 67, tone: 'data' },
  { name: 'Popup Actions', icon: 'popup' as const, x: 78, y: 35, w: 18, tone: 'navigation' },
  { name: 'Approval Agent', icon: 'agent' as const, x: 78, y: 49, w: 18, tone: 'automation' },
  { name: 'Totals Chart', icon: 'chart' as const, x: 7, y: 73, w: 30, tone: 'data' },
  { name: 'Receipt Camera', icon: 'camera' as const, x: 41, y: 73, w: 24, tone: 'media' },
  { name: 'Mobile Target', icon: 'mobile' as const, x: 69, y: 73, w: 27, tone: 'targets' },
]

const timelineTracks = [
  { name: 'Fade totals panel', icon: 'floatAnimation' as const, duration: '180ms', target: 'Totals Chart' },
  { name: 'Accent color shift', icon: 'colorAnimation' as const, duration: '240ms', target: 'Line Items' },
  { name: 'Receipt path reveal', icon: 'pathAnimation' as const, duration: '420ms', target: 'Receipt Camera' },
]

const styleTokens = [
  { name: 'Field focus', icon: 'style' as const, value: '#246b61' },
  { name: 'Error state', icon: 'rule' as const, value: '#b42318' },
  { name: 'Panel fill', icon: 'rectangle' as const, value: '#f8fafc' },
]

const sceneNodes = [
  { name: 'Preview viewport', icon: 'viewport3d' as const, state: 'Active' },
  { name: 'Invoice camera', icon: 'camera3d' as const, state: '35mm' },
  { name: 'Key light', icon: 'light3d' as const, state: 'Soft' },
  { name: 'Product mesh', icon: 'mesh3d' as const, state: 'Bound' },
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
              className={`placed-component placed-${component.tone}`}
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

      <section className="surface-workbenches" aria-label="Advanced design surfaces">
        <div className="surface-lane">
          <div className="surface-lane-title">
            <Icon name="animation" />
            <span>Timeline</span>
          </div>
          <div className="timeline-stack">
            {timelineTracks.map((track) => (
              <button className="timeline-track" key={track.name} type="button" title={track.target}>
                <Icon name={track.icon} />
                <span>{track.name}</span>
                <strong>{track.duration}</strong>
              </button>
            ))}
          </div>
        </div>

        <div className="surface-lane">
          <div className="surface-lane-title">
            <Icon name="style" />
            <span>Style Tokens</span>
          </div>
          <div className="token-stack">
            {styleTokens.map((token) => (
              <button className="token-row" key={token.name} type="button">
                <span className="token-swatch" style={{ background: token.value }} />
                <Icon name={token.icon} />
                <span>{token.name}</span>
                <strong>{token.value}</strong>
              </button>
            ))}
          </div>
        </div>

        <div className="surface-lane">
          <div className="surface-lane-title">
            <Icon name="viewport3d" />
            <span>3D Scene</span>
          </div>
          <div className="scene-node-stack">
            {sceneNodes.map((node) => (
              <button className="scene-node" key={node.name} type="button">
                <Icon name={node.icon} />
                <span>{node.name}</span>
                <strong>{node.state}</strong>
              </button>
            ))}
          </div>
        </div>
      </section>
    </main>
  )
}
