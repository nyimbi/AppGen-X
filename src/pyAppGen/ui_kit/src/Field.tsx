import type { ReactNode } from 'react'
import { cx } from './cx'

export type FieldProps = {
  id: string
  label: ReactNode
  /** Guidance shown under the control; hidden once an error is present. */
  hint?: ReactNode
  error?: ReactNode
  required?: boolean
  className?: string
  children: ReactNode
}

/** A labelled form row. Wires `aria-describedby` and the invalid state so a
 * control inside it needs no knowledge of its own validation.
 */
export function Field({ id, label, hint, error, required = false, className, children }: FieldProps) {
  const hintId = hint && !error ? `${id}-hint` : undefined
  const errorId = error ? `${id}-error` : undefined
  return (
    <div className={cx('appgen-field', error && 'is-invalid', className)}>
      <label className="appgen-field__label" htmlFor={id}>
        {label}
        {required && (
          <span aria-hidden="true" className="appgen-field__required">
            *
          </span>
        )}
      </label>
      <div aria-describedby={cx(hintId, errorId) || undefined} className="appgen-field__control">
        {children}
      </div>
      {hint && !error && (
        <p className="appgen-field__hint" id={hintId}>
          {hint}
        </p>
      )}
      {error && (
        <p className="appgen-field__error" id={errorId} role="alert">
          {error}
        </p>
      )}
    </div>
  )
}
