import type { ReactNode } from 'react'
import { cx } from './cx'

export type PageHeaderProps = {
  title: ReactNode
  /** One line under the title explaining what this page is for. */
  description?: ReactNode
  /** Right-aligned actions. */
  actions?: ReactNode
  /** A breadcrumb or back link above the title. */
  breadcrumb?: ReactNode
  className?: string
}

export function PageHeader({ title, description, actions, breadcrumb, className }: PageHeaderProps) {
  return (
    <header className={cx('appgen-page-header', className)}>
      <div className="appgen-page-header__main">
        {breadcrumb && <div className="appgen-page-header__breadcrumb">{breadcrumb}</div>}
        <h1 className="appgen-page-title">{title}</h1>
        {description && <p className="appgen-page-note">{description}</p>}
      </div>
      {actions && <div className="appgen-page-header__actions">{actions}</div>}
    </header>
  )
}
