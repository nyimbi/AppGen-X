import { useMemo, useState } from 'react'
import { Icon } from './Icon'
import {
  dslCompletions,
  dslEditorAudit,
  dslEditorDiagnostics,
  dslEditorSample,
  dslOutline,
  quickFixesForDiagnostics,
} from './dslEditorCatalog'

export function DslEditorWorkbench() {
  const [source, setSource] = useState(dslEditorSample)
  const diagnostics = useMemo(() => dslEditorDiagnostics(source), [source])
  const fixes = useMemo(() => quickFixesForDiagnostics(diagnostics), [diagnostics])
  const outline = useMemo(() => dslOutline(source), [source])
  const audit = dslEditorAudit()

  return (
    <section className="panel dsl-editor-workbench" aria-label="DSL editor workbench">
      <div className="panel-title-row">
        <div>
          <p className="eyebrow">Language Studio</p>
          <h2>DSL Editor</h2>
        </div>
        <span className={audit.ok ? 'semantic-status semantic-status-ok' : 'semantic-status-blocked semantic-status'}>
          <Icon name={audit.ok ? 'check' : 'rule'} />
          {audit.ok ? 'Ready' : 'Needs review'}
        </span>
      </div>

      <div className="dsl-editor-grid">
        <label className="dsl-source-pane">
          <span>Source</span>
          <textarea
            aria-label="AppGen-X DSL source"
            spellCheck={false}
            value={source}
            onChange={(event) => setSource(event.target.value)}
          />
        </label>

        <aside className="dsl-assist-pane" aria-label="DSL authoring assistance">
          <div className="dsl-assist-section">
            <h3>Diagnostics</h3>
            <ul>
              {diagnostics.length === 0 ? (
                <li className="dsl-empty-state">
                  <Icon name="check" />
                  No diagnostics
                </li>
              ) : (
                diagnostics.map((diagnostic) => (
                  <li key={`${diagnostic.code}-${diagnostic.line}-${diagnostic.column}`}>
                    <strong>{diagnostic.code}</strong>
                    <span>{diagnostic.message}</span>
                    <small>
                      {diagnostic.line}:{diagnostic.column}
                    </small>
                  </li>
                ))
              )}
            </ul>
          </div>

          <div className="dsl-assist-section">
            <h3>Quick Fixes</h3>
            <div className="quick-fix-list">
              {fixes.map((fix) => (
                <button key={fix.id} type="button" onClick={() => setSource(fix.apply(source))} title={fix.preview}>
                  <Icon name="rule" />
                  <span>{fix.title}</span>
                </button>
              ))}
              {fixes.length === 0 ? <span className="dsl-empty-state">No quick fixes</span> : null}
            </div>
          </div>
        </aside>
      </div>

      <div className="dsl-intelligence-grid">
        <section aria-label="DSL completions">
          <h3>Completions</h3>
          <div className="completion-strip">
            {dslCompletions.map((completion) => (
              <button key={completion.label} type="button" onClick={() => setSource(`${source.trimEnd()}\n\n${completion.insertText}\n`)}>
                <span>{completion.label}</span>
                <small>{completion.category}</small>
              </button>
            ))}
          </div>
        </section>

        <section aria-label="Semantic outline">
          <h3>Outline</h3>
          <ul className="outline-list">
            {outline.map((item) => (
              <li key={`${item.kind}-${item.name}`}>
                <Icon name={item.kind === 'table' ? 'database' : item.kind === 'agent' ? 'agent' : 'file'} />
                <span>{item.kind}</span>
                <strong>{item.name}</strong>
              </li>
            ))}
          </ul>
        </section>

        <section aria-label="Agent handoff cues">
          <h3>Agent Handoff</h3>
          <p className="agent-handoff-copy">
            Compact change plans stay tied to diagnostics, quick fixes, generated handlers, and semantic outline symbols.
          </p>
        </section>
      </div>
    </section>
  )
}
