import type { HTMLAttributes, ReactNode } from 'react'
import { cx } from './cx'

export type CardProps = HTMLAttributes<HTMLElement> & {
  title?: ReactNode
  /** Secondary line under the title, for a route or a count. */
  subtitle?: ReactNode
  /** Right-aligned slot in the header, usually actions or a badge. */
  actions?: ReactNode
  /** Remove the padding and the raised surface, for a plain grouping. */
  flush?: boolean
  as?: 'article' | 'section' | 'div'
}

export function Card({
  title,
  subtitle,
  actions,
  flush = false,
  as: Element = 'section',
  className,
  children,
  ...rest
}: CardProps) {
  const hasHeader = Boolean(title || subtitle || actions)
  return (
    <Element className={cx('appgen-card', flush && 'appgen-card--flush', className)} {...rest}>
      {hasHeader && (
        <header className="appgen-card__header">
          <div className="appgen-card__heading">
            {title && <h3 className="appgen-card__title">{title}</h3>}
            {subtitle && <p className="appgen-card__subtitle">{subtitle}</p>}
          </div>
          {actions && <div className="appgen-card__actions">{actions}</div>}
        </header>
      )}
      {children}
    </Element>
  )
}
