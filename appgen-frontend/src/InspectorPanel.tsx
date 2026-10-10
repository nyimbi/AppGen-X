import { EmptyState } from '@appgen/ui-kit'
import { Icon } from './Icon'
import type { IconName } from './Icon'
import { loadInspector } from './studioApi'
import type { InspectorRegistry } from './studioApi'
import { useStudioData } from './useStudioData'

/**
 * The inspector renders the editors the platform registers per component.
 *
 * The panel listed nine editors written in TypeScript against a hardcoded grid
 * named `LineItemsGrid`, so it showed editors for a component the platform had
 * not registered and could not show the ones it had. The registries, their
 * property groups, the diagnostics they raise, and the actions they route now
 * come from the object-inspector workbench.
 */

type EditorKind = 'Property' | 'Event' | 'Component' | 'Custom Designer'

const KIND_ICONS: Record<EditorKind, IconName> = {
  Property: 'style',
  Event: 'workflow',
  Component: 'panel',
  'Custom Designer': 'layout',
}

const KIND_SOURCE: Record<EditorKind, keyof InspectorRegistry> = {
  Property: 'property_editors',
  Event: 'event_editors',
  Component: 'component_editors',
  'Custom Designer': 'custom_designers',
}

const KINDS: EditorKind[] = ['Property', 'Event', 'Component', 'Custom Designer']

/** The name an editor row shows, whatever kind of registration it came from. */
function editorName(editor: Record<string, unknown>): string {
  return String(editor.property ?? editor.event ?? editor.verb ?? editor.hook ?? 'editor')
}

/** The one-line detail under an editor's name. */
function editorDetail(editor: Record<string, unknown>): string {
  if (typeof editor.editor === 'string') return editor.editor
  if (typeof editor.factory === 'string') return editor.factory
  if (typeof editor.surface === 'string') return editor.surface
  if (typeof editor.scope === 'string') return editor.scope
  return ''
}

export function InspectorPanel() {
  const inspector = useStudioData(loadInspector)

  if (inspector.state === 'loading') {
    return (
      <aside className="panel inspector-panel" aria-label="Object inspector">
        <EmptyState description="Reading the editor registries from the backend." title="Loading inspector" />
      </aside>
    )
  }

  if (inspector.state === 'error') {
    return (
      <aside className="panel inspector-panel" aria-label="Object inspector">
        <EmptyState description={inspector.error.message} title="Could not load the inspector" />
      </aside>
    )
  }

  const report = inspector.data
  const registry = report.registries[0]
  const grouping = report.grouping.find((entry) => entry.component === registry?.component)
  const groups = grouping ? Object.entries(grouping.groups).filter(([, names]) => names.length > 0) : []
  const diagnostics = report.diagnostics.find((entry) => entry.component === registry?.component)

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
        <span className="component-icon category-data">
          <Icon name="dataGrid" />
        </span>
        <div>
          <strong>{registry ? registry.component : 'No component'}</strong>
          <span>{report.registries.length} components registered</span>
        </div>
      </div>

      <div className="property-table">
        {groups.map(([name, properties]) => (
          <div className="property-row" key={name}>
            <span>{name}</span>
            <strong>{properties.join(', ')}</strong>
          </div>
        ))}
      </div>

      <div className="inspector-editor-stack" aria-label="Inspector editors">
        {registry &&
          KINDS.map((kind) => {
            const editors = registry[KIND_SOURCE[kind]] as readonly Record<string, unknown>[]

            return (
              <section className="inspector-editor-group" key={kind}>
                <div className="inspector-editor-title">
                  <Icon name={KIND_ICONS[kind]} />
                  <span>{kind}</span>
                  <strong>{editors.length}</strong>
                </div>
                {editors.map((editor) => (
                  <button
                    className="inspector-editor-row"
                    key={`${kind}-${editorName(editor)}`}
                    type="button"
                  >
                    <Icon name={KIND_ICONS[kind]} />
                    <span>
                      <strong>{editorName(editor)}</strong>
                      <small>{editorDetail(editor)}</small>
                    </span>
                  </button>
                ))}
              </section>
            )
          })}
      </div>

      <div className="inspector-diagnostics" aria-label="Inspector diagnostics">
        <p className="eyebrow">
          <Icon name={report.readiness.ok ? 'check' : 'rule'} />
          {diagnostics ? diagnostics.diagnostics.length : 0} diagnostics
        </p>
        {(diagnostics?.diagnostics ?? []).map((diagnostic) => (
          <button
            className={`diagnostic-row diagnostic-${diagnostic.severity}`}
            key={`${diagnostic.code}-${diagnostic.property ?? diagnostic.target ?? ''}`}
            title={diagnostic.quick_fix}
            type="button"
          >
            <Icon name={diagnostic.severity === 'error' ? 'rule' : 'bell'} />
            <span>
              <strong>{diagnostic.code.replace(/_/g, ' ')}</strong>
              <small>{diagnostic.property ?? diagnostic.target ?? ''}</small>
            </span>
            <em>{diagnostic.surface.replace(/_/g, ' ')}</em>
          </button>
        ))}
      </div>
    </aside>
  )
}
