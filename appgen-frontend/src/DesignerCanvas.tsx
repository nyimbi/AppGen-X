import { Icon } from './Icon'
import { visualBindings } from './bindingCatalog'
import { designerRuntimeAudit } from './designerRuntime'
import type { ComponentDragPayload, DesignerDropOperation, PlacedComponent } from './designerRuntime'

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

type DesignerCanvasProps = {
  components: PlacedComponent[]
  selectedId: string
  lastOperation: DesignerDropOperation | null
  onDropComponent: (payload: ComponentDragPayload, target: { x: number; y: number }) => void
  onSelectComponent: (id: string) => void
}

export function DesignerCanvas({
  components,
  selectedId,
  lastOperation,
  onDropComponent,
  onSelectComponent,
}: DesignerCanvasProps) {
  const runtimeAudit = designerRuntimeAudit()

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
        <div
          className="form-frame"
          onDragOver={(event) => {
            event.preventDefault()
            event.dataTransfer.dropEffect = 'copy'
          }}
          onDrop={(event) => {
            event.preventDefault()
            const payloadText = event.dataTransfer.getData('application/appgen-component')
            if (!payloadText) {
              return
            }
            const bounds = event.currentTarget.getBoundingClientRect()
            const payload = JSON.parse(payloadText) as ComponentDragPayload
            onDropComponent(payload, {
              x: ((event.clientX - bounds.left) / bounds.width) * 100,
              y: ((event.clientY - bounds.top) / bounds.height) * 100,
            })
          }}
        >
          <div className="form-titlebar">
            <span>InvoiceForm</span>
            <span>
              <Icon name="grid" />
              12 columns
            </span>
          </div>
          <div className="drop-target-banner">
            <Icon name="drag" />
            <span>Drop Target Ready</span>
            <strong>{runtimeAudit.ok ? 'Runtime wired' : 'Runtime blocked'}</strong>
          </div>
          <div className="canvas-rulers" aria-hidden="true">
            <span>0</span>
            <span>320</span>
            <span>640</span>
            <span>960</span>
          </div>
          {components.map((component) => (
            <button
              className={`placed-component placed-${component.tone} ${component.id === selectedId ? 'selected' : ''}`}
              key={component.id}
              onClick={() => onSelectComponent(component.id)}
              style={{ left: `${component.x}%`, top: `${component.y}%`, width: `${component.w}%`, height: `${component.h}%` }}
              type="button"
            >
              <Icon name={component.icon} />
              <span>{component.name}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="drop-operation-panel" aria-label="Designer drag and drop runtime">
        <div>
          <Icon name="workflow" />
          <span>Drag/drop wiring</span>
          <strong>{lastOperation ? 'Committed' : 'Ready'}</strong>
        </div>
        <p>
          {lastOperation
            ? `Last drop: ${lastOperation.preview.name} -> handler ${lastOperation.handlerDefinition.target}`
            : `Actionable operation: ${runtimeAudit.commit.operation} -> handler ${runtimeAudit.commit.handlerDefinition.target}`}
        </p>
        <code>{lastOperation?.dslPatch[0] ?? runtimeAudit.commit.dslPatch[0]}</code>
      </section>

      <section className="surface-workbenches" aria-label="Advanced design surfaces">
        <div className="surface-lane binding-lane">
          <div className="surface-lane-title">
            <Icon name="database" />
            <span>Bindings</span>
          </div>
          <div className="binding-stack">
            {visualBindings.map((binding) => (
              <button
                className={`binding-row binding-${binding.state}`}
                key={`${binding.source}-${binding.target}`}
                type="button"
                title={binding.expression}
              >
                <Icon name={binding.icon} />
                <span>
                  <strong>{binding.source}</strong>
                  <small>{binding.target}</small>
                </span>
                <em>{binding.state}</em>
              </button>
            ))}
          </div>
        </div>

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
