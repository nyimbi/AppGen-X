import type { SelectHTMLAttributes } from 'react'
import { cx } from './cx'

export type SelectOption = {
  value: string
  label: string
  disabled?: boolean
}

export type SelectProps = Omit<SelectHTMLAttributes<HTMLSelectElement>, 'size'> & {
  options: readonly SelectOption[]
  /** Rendered as a disabled first option when nothing is selected yet. */
  placeholder?: string
  invalid?: boolean
}

export function Select({ options, placeholder, invalid = false, className, value, ...rest }: SelectProps) {
  return (
    <select
      aria-invalid={invalid || undefined}
      className={cx('appgen-select', invalid && 'is-invalid', className)}
      value={value}
      {...rest}
    >
      {placeholder && (
        <option disabled value="">
          {placeholder}
        </option>
      )}
      {options.map((option) => (
        <option disabled={option.disabled} key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  )
}
