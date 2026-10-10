import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { cx } from './cx'

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger'
export type ButtonSize = 'md' | 'sm'

export type ButtonProps = Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'type'> & {
  variant?: ButtonVariant
  size?: ButtonSize
  /** Rendered before the label, usually an `<Icon>`. */
  leading?: ReactNode
  /** Rendered after the label, for a chevron or a count badge. */
  trailing?: ReactNode
  /** Shows a busy state and blocks activation without removing the button. */
  loading?: boolean
  type?: 'button' | 'submit' | 'reset'
}

export function Button({
  variant = 'primary',
  size = 'md',
  leading,
  trailing,
  loading = false,
  type = 'button',
  disabled,
  className,
  children,
  ...rest
}: ButtonProps) {
  return (
    <button
      aria-busy={loading || undefined}
      className={cx('appgen-button', `appgen-button--${variant}`, size === 'sm' && 'appgen-button--sm', className)}
      disabled={disabled || loading}
      type={type}
      {...rest}
    >
      {loading ? <span aria-hidden="true" className="appgen-button__spinner" /> : leading}
      <span className="appgen-button__label">{children}</span>
      {trailing}
    </button>
  )
}
