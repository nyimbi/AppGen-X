import type { ReactNode } from 'react'
import { cx } from './cx'

export type TabItem = {
  id: string
  label: ReactNode
  /** Optional count or status shown after the label. */
  badge?: ReactNode
  disabled?: boolean
}

export type TabsProps = {
  items: readonly TabItem[]
  activeId: string
  onChange: (id: string) => void
  /** Accessible name for the tab list. */
  label: string
  className?: string
}

/** A tab strip following the ARIA tabs pattern: roving focus, arrow keys move
 * between tabs, and the selected tab owns the panel below it.
 */
export function Tabs({ items, activeId, onChange, label, className }: TabsProps) {
  const move = (delta: number) => {
    const enabled = items.filter((item) => !item.disabled)
    if (enabled.length === 0) return
    const index = enabled.findIndex((item) => item.id === activeId)
    const next = enabled[(index + delta + enabled.length) % enabled.length]
    onChange(next.id)
  }

  return (
    <div aria-label={label} className={cx('appgen-tabs', className)} role="tablist">
      {items.map((item) => {
        const selected = item.id === activeId
        return (
          <button
            aria-selected={selected}
            className={cx('appgen-tab', selected && 'is-active')}
            disabled={item.disabled}
            key={item.id}
            onClick={() => onChange(item.id)}
            onKeyDown={(event) => {
              if (event.key === 'ArrowRight') {
                event.preventDefault()
                move(1)
              } else if (event.key === 'ArrowLeft') {
                event.preventDefault()
                move(-1)
              }
            }}
            role="tab"
            tabIndex={selected ? 0 : -1}
            type="button"
          >
            <span className="appgen-tab__label">{item.label}</span>
            {item.badge != null && <span className="appgen-tab__badge">{item.badge}</span>}
          </button>
        )
      })}
    </div>
  )
}
