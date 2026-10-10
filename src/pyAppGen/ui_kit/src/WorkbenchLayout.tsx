import type { CSSProperties, ReactNode } from 'react'
import { cx } from './cx'

export type WorkbenchLayoutProps = {
  /** The primary work area: a canvas, a table, a form. */
  children: ReactNode
  /** A fixed-width inspector on the right. */
  aside?: ReactNode
  /** Tabs or a toolbar pinned above both columns. */
  toolbar?: ReactNode
  asideWidth?: string
  className?: string
}

/** The two-column workbench: content plus an inspector, with an optional
 * toolbar across the top. Collapses to one column below the mobile breakpoint.
 */
export function WorkbenchLayout({ children, aside, toolbar, asideWidth = '320px', className }: WorkbenchLayoutProps) {
  return (
    <div
      className={cx('appgen-workbench', aside && 'appgen-workbench--split', className)}
      style={aside ? ({ '--appgen-aside-width': asideWidth } as CSSProperties) : undefined}
    >
      {toolbar && <div className="appgen-workbench__toolbar">{toolbar}</div>}
      <div className="appgen-workbench__main">{children}</div>
      {aside && (
        <aside aria-label="Inspector" className="appgen-workbench__aside">
          {aside}
        </aside>
      )}
    </div>
  )
}
