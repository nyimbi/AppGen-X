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
