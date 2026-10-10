import { useId, type ReactElement } from 'react'
import { cx } from './cx'

export type TooltipProps = {
  label: string
  /** A single element; the tooltip attaches its own ARIA attributes to it
   * rather than wrapping it in a span, which would break layout.
   */
  children: ReactElement<{ 'aria-describedby'?: string; className?: string }>
  side?: 'top' | 'bottom'
  className?: string
}

/** A CSS-only tooltip: shown on hover and on keyboard focus, described to
 * assistive technology through `aria-describedby`.
 */
export function Tooltip({ label, children, side = 'top', className }: TooltipProps) {
  const id = useId()
  const described = [children.props['aria-describedby'], id].filter(Boolean).join(' ')
  const child = {
    ...children,
    props: {
      ...children.props,
      'aria-describedby': described,
      className: cx(children.props.className, 'appgen-tooltip-trigger'),
    },
  }
  return (
    <span className={cx('appgen-tooltip', `appgen-tooltip--${side}`, className)}>
      {child}
      <span className="appgen-tooltip__label" id={id} role="tooltip">
        {label}
      </span>
    </span>
  )
}
