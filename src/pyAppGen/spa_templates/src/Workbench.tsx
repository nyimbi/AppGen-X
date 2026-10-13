/** Render one PBC workbench from its own contract.
 *
 * The payload is what the PBC package declares: its owned tables, its command
 * and query routes, its outbox and dead-letter tables. A workbench that shows
 * a placeholder instead is the defect this component exists to avoid, so every
 * section renders from the payload and an empty payload reads as empty.
 */

import { Badge } from '@appgen/ui-kit'
import { Card, EmptyState, PageHeader, Table, WorkbenchLayout } from '@appgen/ui-kit'
import type { TableColumn } from '@appgen/ui-kit'

import type { WorkbenchRender } from './appgen.generated'

type ApiRow = {
  method: string
  route: string
  handler: string
  permission?: string
}

type PanelRow = {
  key: string
  fragment: string
  binds_to: readonly string[]
  commands: readonly string[]
}

const apiColumns: readonly TableColumn<ApiRow>[] = [
  {
    key: 'method',
    header: 'Method',
    width: '88px',
    render: (row) => <Badge tone={row.method === 'GET' ? 'info' : 'neutral'}>{row.method}</Badge>,
  },
  { key: 'route', header: 'Route', render: (row) => <code>{row.route}</code> },
  { key: 'handler', header: 'Handler', render: (row) => row.handler },
]

const panelColumns: readonly TableColumn<PanelRow>[] = [
  { key: 'key', header: 'Panel', render: (row) => row.key },
  { key: 'fragment', header: 'Fragment', render: (row) => <code>{row.fragment}</code> },
  { key: 'binds_to', header: 'Binds to', render: (row) => row.binds_to.join(', ') },
  { key: 'commands', header: 'Commands', render: (row) => row.commands.join(', ') },
]

export function Workbench({ workbench }: { workbench: WorkbenchRender }) {
  if (!workbench.ok) {
    return (
      <EmptyState
        title={`No workbench for ${workbench.pbc}`}
        description="This PBC is not part of the composition this app was generated from."
      />
    )
  }

  const tableRows = workbench.owned_tables.map((name) => ({ name }))

  return (
    <WorkbenchLayout
      toolbar={<PageHeader title={workbench.label} description={`${workbench.pbc} · ${workbench.mesh}`} />}
      aside={
        <Card title="Bound artifacts" flush>
          <ul className="appgen-kpi-row">
            {workbench.cards.map((card) => (
              <li key={card.key}>
                <span>{card.label}</span>
                <strong>{card.value}</strong>
              </li>
            ))}
          </ul>
        </Card>
      }
    >
      <Card title="Owned tables" subtitle={`${workbench.owned_tables.length} tables`} flush>
        <Table
          caption={`Tables owned by ${workbench.pbc}`}
          columns={[{ key: 'name', header: 'Physical table', render: (row) => <code>{row.name}</code> }]}
          rows={tableRows}
          rowKey={(row) => row.name}
          empty={tableRows.length === 0 ? 'This PBC owns no tables.' : undefined}
        />
      </Card>

      <Card title="Command and query APIs" subtitle={`${workbench.apis.length} routes`} flush>
        <Table
          caption={`API routes exposed by ${workbench.pbc}`}
          columns={apiColumns}
          rows={workbench.apis as readonly ApiRow[]}
          rowKey={(row) => `${row.method} ${row.route}`}
        />
      </Card>

      {workbench.panels.length > 0 && (
        <Card title="Panels" subtitle={`${workbench.panels.length} panels`} flush>
          <Table
            caption={`Panels declared by ${workbench.pbc}`}
            columns={panelColumns}
            rows={workbench.panels as readonly PanelRow[]}
            rowKey={(row) => row.key}
          />
        </Card>
      )}

      {(workbench.configuration.required_fields?.length ?? 0) > 0 && (
        <Card
          title="Configuration"
          subtitle={`${workbench.configuration.required_fields?.length ?? 0} fields`}
        >
          <ul className="appgen-kpi-row">
            {workbench.configuration.required_fields?.map((field) => (
              <li key={field}>
                <code>{field}</code>
              </li>
            ))}
          </ul>
          {workbench.configuration.required_event_topic && (
            <p>
              Event topic: <code>{workbench.configuration.required_event_topic}</code>
            </p>
          )}
        </Card>
      )}

      {(workbench.rules.rule_types?.length ?? 0) > 0 && (
        <Card title="Rules" subtitle={`${workbench.rules.rule_types?.length ?? 0} types`}>
          <ul>
            {workbench.rules.rule_types?.map((rule) => (
              <li key={rule}>{rule}</li>
            ))}
          </ul>
        </Card>
      )}

      {(workbench.parameters?.numeric_parameters?.length ?? 0) > 0 && (
        <Card
          title="Parameters"
          subtitle={`${workbench.parameters?.numeric_parameters?.length ?? 0} tunable`}
        >
          <ul>
            {workbench.parameters?.numeric_parameters?.map((parameter) => (
              <li key={parameter}>{parameter}</li>
            ))}
          </ul>
        </Card>
      )}

      {(workbench.interactions?.forms?.length ?? 0) > 0 && (
        <Card
          title="Intake forms"
          subtitle={`${workbench.interactions?.forms?.length ?? 0} forms`}
        >
          <ul>
            {workbench.interactions?.forms?.map((form) => (
              <li key={form}>
                <code>{form}</code>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {(workbench.interactions?.wizards?.length ?? 0) > 0 && (
        <Card
          title="Wizards"
          subtitle={`${workbench.interactions?.wizards?.length ?? 0} wizards`}
        >
          <ul>
            {workbench.interactions?.wizards?.map((wizard) => (
              <li key={wizard}>
                <code>{wizard}</code>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {(workbench.interactions?.controls?.length ?? 0) > 0 && (
        <Card
          title="Controls"
          subtitle={`${workbench.interactions?.controls?.length ?? 0} controls`}
        >
          <ul>
            {workbench.interactions?.controls?.map((control) => (
              <li key={control}>
                <code>{control}</code>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {(workbench.events.emits?.length ?? 0) > 0 && (
        <Card
          title="Events"
          subtitle={`${workbench.events.emits?.length ?? 0} emitted · ${workbench.events.consumes?.length ?? 0} consumed`}
        >
          <ul>
            {workbench.events.emits?.map((event) => (
              <li key={event}>
                <Badge tone="info">{event}</Badge>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {workbench.fragments.length > 0 && (
        <Card title="Declared fragments">
          <ul>
            {workbench.fragments.map((fragment) => (
              <li key={fragment}>{fragment}</li>
            ))}
          </ul>
        </Card>
      )}
    </WorkbenchLayout>
  )
}
