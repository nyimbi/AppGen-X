import type { ReactNode } from 'react'
import { cx } from './cx'

export type NavItem = {
  id: string
  label: string
  href?: string
  icon?: ReactNode
  /** Optional trailing count or status. */
  badge?: ReactNode
  disabled?: boolean
}

export type NavRailProps = {
  items: readonly NavItem[]
  activeId?: string
  onSelect?: (id: string) => void
  /** Rendered at the top of the rail, above the items. */
  brand?: ReactNode
  /** Rendered at the bottom, for settings or an account block. */
  footer?: ReactNode
  label: string
  className?: string
}

/** The primary vertical navigation. Renders anchors when an item has an href
 * and buttons otherwise, so a client-routed app and a plain page both work.
 */
export function NavRail({ items, activeId, onSelect, brand, footer, label, className }: NavRailProps) {
  return (
    <nav aria-label={label} className={cx('appgen-nav-rail', className)}>
      {brand && <div className="appgen-nav-rail__brand">{brand}</div>}
      <ul className="appgen-nav-rail__list">
        {items.map((item) => {
          const active = item.id === activeId
          const inner = (
            <>
              {item.icon && (
                <span aria-hidden="true" className="appgen-nav-rail__icon">
                  {item.icon}
                </span>
              )}
              <span className="appgen-nav-rail__label">{item.label}</span>
              {item.badge != null && <span className="appgen-nav-rail__badge">{item.badge}</span>}
            </>
          )
          return (
            <li key={item.id}>
              {item.href ? (
                <a
                  aria-current={active ? 'page' : undefined}
                  className={cx('appgen-nav-item', active && 'is-active', item.disabled && 'is-disabled')}
                  href={item.href}
                >
                  {inner}
                </a>
              ) : (
                <button
                  aria-current={active ? 'page' : undefined}
                  className={cx('appgen-nav-item', active && 'is-active')}
                  disabled={item.disabled}
                  onClick={() => onSelect?.(item.id)}
                  type="button"
                >
                  {inner}
                </button>
              )}
            </li>
          )
        })}
      </ul>
      {footer && <div className="appgen-nav-rail__footer">{footer}</div>}
    </nav>
  )
}
