import type { ReactNode } from 'react'
import { cx } from './cx'

export type AppShellProps = {
  /** A `<NavRail>` or any fixed side region. */
  rail?: ReactNode
  /** Sticky top bar spanning the content column. */
  topbar?: ReactNode
  children: ReactNode
  /** Cap the content width; off for a full-bleed canvas or a data grid. */
  contained?: boolean
  className?: string
}

/** The page frame every screen sits in: an optional rail, an optional sticky
 * top bar, and a main region that owns the scroll. Kept deliberately thin so a
 * generated app and the Studio share one layout without sharing a router.
 */
export function AppShell({ rail, topbar, children, contained = true, className }: AppShellProps) {
  return (
    <div className={cx('appgen-shell', rail && 'appgen-shell--railed', className)}>
      {rail}
      <div className="appgen-shell__body">
        {topbar && <div className="appgen-shell__topbar">{topbar}</div>}
        <main className={cx('appgen-main', contained && 'appgen-page')} id="appgen-main">
          {children}
        </main>
      </div>
    </div>
  )
}
