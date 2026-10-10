import type { InputHTMLAttributes, ReactNode } from 'react'
import { cx } from './cx'

export type InputProps = Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> & {
  /** Rendered inside the control, before the text. */
  leading?: ReactNode
  /** Rendered inside the control, after the text. */
  trailing?: ReactNode
  invalid?: boolean
}

export function Input({ leading, trailing, invalid = false, className, ...rest }: InputProps) {
  const control = (
    <input
      aria-invalid={invalid || undefined}
      className={cx('appgen-input', invalid && 'is-invalid', (leading || trailing) && 'appgen-input--grouped', className)}
      {...rest}
    />
  )
  if (!leading && !trailing) return control
  return (
    <span className={cx('appgen-input-group', invalid && 'is-invalid')}>
      {leading && <span className="appgen-input-group__addon">{leading}</span>}
      {control}
      {trailing && <span className="appgen-input-group__addon">{trailing}</span>}
    </span>
  )
}
