import type { ReactNode } from 'react'
import { cx } from './cx'

export type EmptyStateProps = {
  title: ReactNode
  /** Explain what would fill this space and how to get there. */
  description?: ReactNode
  /** An `<Icon>`, an illustration, or any decorative element. */
  icon?: ReactNode
  /** The action that resolves the emptiness, usually a `<Button>`. */
  action?: ReactNode
  className?: string
}

export function EmptyState({ title, description, icon, action, className }: EmptyStateProps) {
  return (
    <div className={cx('appgen-empty', className)} role="status">
      {icon && (
        <div aria-hidden="true" className="appgen-empty__icon">
          {icon}
        </div>
      )}
      <p className="appgen-empty__title">{title}</p>
      {description && <p className="appgen-empty__description">{description}</p>}
      {action && <div className="appgen-empty__action">{action}</div>}
    </div>
  )
}
