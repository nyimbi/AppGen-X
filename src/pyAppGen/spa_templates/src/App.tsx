/** The generated app's shell.
 *
 * Navigation is derived from the composition plan the app was generated from,
 * so the shell cannot offer a screen the backend does not serve. Workbenches
 * come from the PBC contracts; table screens come from the schema.
 */

import { useCallback, useEffect, useMemo, useState } from 'react'

import { AppShell, Badge, EmptyState, NavRail, PageHeader, Table, WorkbenchLayout } from '@appgen/ui-kit'
import type { NavItem, TableColumn } from '@appgen/ui-kit'

import { ApiError, listRows, loadWorkbench } from './api'
import { APP_NAME, TABLES, WORKBENCHES } from './appgen.generated'
import type { TableSpec, WorkbenchRender } from './appgen.generated'
import { Workbench } from './Workbench'

type Selection = { kind: 'table'; table: TableSpec } | { kind: 'workbench'; index: number }

function TableScreen({ table }: { table: TableSpec }) {
  const [rows, setRows] = useState<Record<string, unknown>[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let live = true
    setRows(null)
    setError(null)
    listRows(table)
      .then((payload) => live && setRows(payload))
      .catch((cause: unknown) => {
        if (!live) return
        setError(cause instanceof ApiError ? `${cause.status}: ${cause.message}` : String(cause))
      })
    return () => {
      live = false
    }
  }, [table])

  const columns = useMemo<readonly TableColumn<Record<string, unknown>>[]>(
    () =>
      table.columns.map((column) => ({
        key: column,
        header: column,
        render: (row: Record<string, unknown>) => {
          const value = row[column]
          return value === null || value === undefined ? '—' : String(value)
        },
      })),
    [table],
  )

  if (error) {
    return <EmptyState title="Could not load rows" description={error} />
  }
  if (rows === null) {
    return <EmptyState title="Loading" description={`Reading ${table.label} from ${table.route}`} />
  }
  return (
    <Table
      caption={table.label}
      columns={columns}
      rows={rows}
      rowKey={(row: Record<string, unknown>) => String(row[table.primaryKey] ?? JSON.stringify(row))}
    />
  )
}

function WorkbenchScreen({ index }: { index: number }) {
  const [payload, setPayload] = useState<WorkbenchRender | null>(null)
  const [error, setError] = useState<string | null>(null)
  const workbench = WORKBENCHES[index]

  useEffect(() => {
    let live = true
    setPayload(null)
    setError(null)
    loadWorkbench(workbench)
      .then((value) => live && setPayload(value))
      .catch((cause: unknown) => live && setError(String(cause)))
    return () => {
      live = false
    }
  }, [workbench])

  if (error) return <EmptyState title="Could not load the workbench" description={error} />
  if (!payload) return <EmptyState title="Loading" description={workbench.label} />
  return <Workbench workbench={payload} />
}

export function App() {
  const initial = useMemo<Selection>(
    () => (WORKBENCHES.length > 0 ? { kind: 'workbench', index: 0 } : { kind: 'table', table: TABLES[0] }),
    [],
  )
  const [selection, setSelection] = useState<Selection>(initial)

  const items = useMemo<NavItem[]>(() => {
    const workbenchItems: NavItem[] = WORKBENCHES.map((workbench, index) => ({
      id: `workbench:${index}`,
      label: workbench.label,
      badge: <Badge tone="info">{workbench.pbc}</Badge>,
    }))
    const tableItems: NavItem[] = TABLES.map((table) => ({ id: `table:${table.name}`, label: table.label }))
    return [...workbenchItems, ...tableItems]
  }, [])

  const activeId =
    selection.kind === 'workbench' ? `workbench:${selection.index}` : `table:${selection.table.name}`

  const onSelect = useCallback(
    (id: string) => {
      const [kind, rest] = id.split(':', 2)
      if (kind === 'workbench') setSelection({ kind: 'workbench', index: Number(rest) })
      else {
        const table = TABLES.find((candidate) => candidate.name === rest)
        if (table) setSelection({ kind: 'table', table })
      }
    },
    [],
  )

  return (
    <AppShell
      rail={<NavRail label="Application" items={items} activeId={activeId} onSelect={onSelect} brand={APP_NAME} />}
    >
      {selection.kind === 'workbench' ? (
        <WorkbenchScreen index={selection.index} />
      ) : (
        <WorkbenchLayout
          toolbar={<PageHeader title={selection.table.label} description={selection.table.route} />}
        >
          <TableScreen table={selection.table} />
        </WorkbenchLayout>
      )}
    </AppShell>
  )
}
