import { Icon } from './Icon'
import { inspectorEditors, inspectorKindIcons } from './inspectorCatalog'
import type { InspectorEditorKind } from './inspectorCatalog'
import type { PlacedComponent } from './designerRuntime'

const editorKinds: InspectorEditorKind[] = ['Property', 'Event', 'Component', 'Custom Designer']

type InspectorPanelProps = {
  selectedComponent: PlacedComponent
}

export function InspectorPanel({ selectedComponent }: InspectorPanelProps) {
  const properties = [
    ['Name', selectedComponent.id],
    ['Component', selectedComponent.name],
    ['Data source', selectedComponent.binding],
    ['Source', selectedComponent.source],
    ['Bounds', `${selectedComponent.x.toFixed(0)}, ${selectedComponent.y.toFixed(0)}, ${selectedComponent.w.toFixed(0)}, ${selectedComponent.h.toFixed(0)}`],
    ['Handler', selectedComponent.handler ? `${selectedComponent.handler.event} -> ${selectedComponent.handler.target}` : 'None'],
  ]

  return (
    <aside className="panel inspector-panel" aria-label="Object inspector">
      <div className="panel-title-row">
        <div>
          <p className="eyebrow">Selection</p>
          <h2>Object Inspector</h2>
        </div>
        <Icon name="dataGrid" className="panel-title-icon" />
      </div>

      <div className="selected-card">
        <span className={`component-icon category-${selectedComponent.tone}`}>
          <Icon name={selectedComponent.icon} />
        </span>
        <div>
          <strong>{selectedComponent.name}</strong>
          <span>{selectedComponent.binding}</span>
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

      <div className="inspector-editor-stack" aria-label="Inspector editors">
        {editorKinds.map((kind) => {
          const editors = inspectorEditors.filter((editor) => editor.kind === kind)

          return (
            <section className="inspector-editor-group" key={kind}>
              <div className="inspector-editor-title">
                <Icon name={inspectorKindIcons[kind]} />
                <span>{kind}</span>
                <strong>{editors.length}</strong>
              </div>
              {editors.map((editor) => (
                <button className="inspector-editor-row" key={`${editor.kind}-${editor.name}`} type="button">
                  <Icon name={editor.icon} />
                  <span>
                    <strong>{editor.name}</strong>
                    <small>{editor.value}</small>
                  </span>
                  <em>{editor.action}</em>
                </button>
              ))}
            </section>
          )
        })}
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
          {selectedComponent.handler ? selectedComponent.handler.target : 'Add Event'}
        </button>
      </div>
    </aside>
  )
}
