import { EmptyState } from '@appgen/ui-kit'
import { Icon } from './Icon'
import type { IconName } from './Icon'
import { loadDesigner } from './studioApi'
import type { DesignerLane } from './studioApi'
import { useStudioData } from './useStudioData'

/**
 * The design surface renders the platform's projected form and binding graph.
 *
 * The canvas used to draw a hardcoded invoice form and a hardcoded binding
 * list, so it showed a form the platform had not projected and links the
 * binding designer had not validated. The form now comes from the designer-sync
 * projection, the links from the livebindings graph, and each lane from the
 * contract it names, so a lane cannot display evidence the platform does not
 * publish.
 */

const LANE_ICONS: Record<string, IconName> = {
  timeline: 'animation',
  style: 'style',
  scene: 'viewport3d',
}

const COMPONENT_ICONS: Record<string, IconName> = {
  TextBox: 'input',
  NumberInput: 'hash',
  CheckBox: 'check',
  DatePicker: 'calendar',
  Lookup: 'lookup',
  Button: 'button',
  ComboBox: 'combo',
  DataGrid: 'dataGrid',
}

/** Which icon stands for a node kind in the binding graph. */
function nodeIcon(kind: string): IconName {
  if (kind === 'dataset') return 'database'
  if (kind === 'expression') return 'rule'
  if (kind === 'control') return 'button'
  if (kind === 'converter') return 'switch'
  if (kind === 'validator') return 'check'
  return 'input'
}

/** The 12-column footprint of a placed component, as a CSS percentage. */
function placement(component: { x: number; y: number; w: number; h: number }) {
  const columns = 12
  const rows = 6
  return {
    left: `${(component.x / columns) * 100}%`,
    top: `${(component.y / rows) * 100}%`,
    width: `${(component.w / columns) * 100}%`,
    height: `${(component.h / rows) * 100}%`,
  }
}

function Lane({ lane }: { lane: DesignerLane }) {
  return (
    <div className="surface-lane">
      <div className="surface-lane-title">
        <Icon name={LANE_ICONS[lane.lane] ?? 'layout'} />
        <span>{lane.label}</span>
      </div>
      <div className="lane-stack">
        {lane.items.map((item) => (
          <button className="lane-row" key={item.name} title={item.detail} type="button">
            <Icon name={LANE_ICONS[lane.lane] ?? 'layout'} />
            <span>
              <strong>{item.name}</strong>
              <small>{item.detail}</small>
            </span>
            <em>{item.value}</em>
          </button>
        ))}
      </div>
      <p className="lane-contract" title={lane.format}>
        <Icon name="check" />
        {lane.format}
      </p>
    </div>
  )
}

export function DesignerCanvas() {
  const designer = useStudioData(loadDesigner)

  if (designer.state === 'loading') {
    return (
      <main className="panel designer-canvas" aria-label="Application designer">
        <EmptyState description="Reading the form projection from the backend." title="Loading design surface" />
      </main>
    )
  }

  if (designer.state === 'error') {
    return (
      <main className="panel designer-canvas" aria-label="Application designer">
        <EmptyState description={designer.error.message} title="Could not load the design surface" />
      </main>
    )
  }

  const { binding_graph: graph, binding_families: families, form, lanes } = designer.data
  const view = form.views[0]
  const placed = view?.components ?? []
  const fields = view?.sections.flatMap((section) => section.fields) ?? []

  return (
    <main className="panel designer-canvas" aria-label="Application designer">
      <div className="canvas-toolbar">
        <div>
          <p className="eyebrow">Design Surface</p>
          <h2>{view ? view.view : 'No view projected'}</h2>
        </div>
        <div className="toolbar-actions" aria-label="Canvas actions">
          <button type="button" title="Align selection">
            <Icon name="layout" />
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
            <span>{view ? `${view.table} form` : 'No form'}</span>
            <span>
              <Icon name="grid" />
              12 columns
            </span>
          </div>
          {placed.map((component) => (
            <button
              className="placed-component"
              key={`${component.binding}-${component.component}`}
              style={placement(component)}
              title={`${component.component} bound to ${component.binding}`}
              type="button"
            >
              <Icon name={COMPONENT_ICONS[component.component] ?? 'shape'} />
              <span>{component.binding}</span>
            </button>
          ))}
        </div>
        <p className="canvas-note">
          <Icon name="check" />
          {fields.length} fields projected from {view?.table ?? 'no table'}
        </p>
      </section>

      <section className="surface-workbenches" aria-label="Advanced design surfaces">
        <div className="surface-lane binding-lane">
          <div className="surface-lane-title">
            <Icon name="database" />
            <span>Bindings</span>
            <strong>{graph.edges.length}</strong>
          </div>
          <div className="binding-stack">
            {graph.edges.map((edge) => (
              <button
                className="binding-row"
                key={`${edge.from}-${edge.to}-${edge.kind}`}
                title={`${edge.kind}${edge.mode ? ` (${edge.mode})` : ''}`}
                type="button"
              >
                <Icon name={nodeIcon(edge.from.split(':')[0])} />
                <span>
                  <strong>{edge.from}</strong>
                  <small>{edge.to}</small>
                </span>
                <em>{edge.kind}</em>
              </button>
            ))}
          </div>
          <p className="lane-contract" title={graph.format}>
            <Icon name="check" />
            {families.families.length} families, {families.guards.length} guards
          </p>
        </div>

        {lanes.map((lane) => (
          <Lane key={lane.lane} lane={lane} />
        ))}
      </section>
    </main>
  )
}
