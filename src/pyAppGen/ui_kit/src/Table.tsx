import type { ReactNode } from 'react'
import { cx } from './cx'
import { EmptyState } from './EmptyState'

export type TableColumn<Row> = {
  /** Stable key; also the React key for the cell. */
  key: string
  header: ReactNode
  /** Cell content for a row. Return a node, not a string, when it needs styling. */
  render: (row: Row) => ReactNode
  /** Right-align numeric columns so digits line up. */
  align?: 'start' | 'end'
  width?: string
}

export type TableProps<Row> = {
  columns: readonly TableColumn<Row>[]
  rows: readonly Row[]
  /** Must be stable per row; the row id, never the array index. */
  rowKey: (row: Row) => string
  /** Shown in place of the body when there are no rows. */
  empty?: ReactNode
  selectedKey?: string
  onRowClick?: (row: Row) => void
  /** Accessible name for the table; required, since a table without one is
   * announced as an unlabelled grid. */
  caption: string
  className?: string
}

export function Table<Row>({
  columns,
  rows,
  rowKey,
  empty,
  selectedKey,
  onRowClick,
  caption,
  className,
}: TableProps<Row>) {
  if (rows.length === 0 && empty) {
    return <div className={cx('appgen-table-empty', className)}>{empty}</div>
  }
  return (
    // The wrapper scrolls horizontally when a table is wider than its column,
    // and a scroll container with no focusable child cannot be scrolled from
    // the keyboard. It is therefore focusable and named, so the tab stop
    // announces the table it scrolls rather than appearing as an unnamed region.
    <div
      aria-label={caption}
      className={cx('appgen-table-wrap', className)}
      role="group"
      tabIndex={0}
    >
      <table className="appgen-table">
        <caption className="appgen-visually-hidden">{caption}</caption>
        <thead>
          <tr>
            {columns.map((column) => (
              <th
                className={cx('appgen-table__th', column.align === 'end' && 'is-end')}
                key={column.key}
                scope="col"
                style={column.width ? { width: column.width } : undefined}
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => {
            const key = rowKey(row)
            return (
              <tr
                className={cx('appgen-table__row', selectedKey === key && 'is-selected', onRowClick && 'is-clickable')}
                key={key}
                onClick={onRowClick ? () => onRowClick(row) : undefined}
              >
                {columns.map((column) => (
                  <td className={cx('appgen-table__td', column.align === 'end' && 'is-end')} key={column.key}>
                    {column.render(row)}
                  </td>
                ))}
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

/** Convenience for the common case: a table with no rows and no caller-supplied
 * empty node gets a legible default rather than a bare header.
 */
export function tableEmptyState(title: string, description?: string): ReactNode {
  return <EmptyState description={description} title={title} />
}
