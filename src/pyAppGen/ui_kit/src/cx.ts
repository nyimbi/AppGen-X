/** Join class names, keeping only non-empty strings.
 *
 * Accepts anything so a caller can write `condition && 'class'` without the
 * union of falsy ReactNode values tripping the type checker. Every kit
 * component takes a `className` and appends it last, so a caller's utility
 * class wins over the component's own rule without `!important`.
 */
export function cx(...parts: unknown[]): string {
  return parts.filter((part): part is string => typeof part === 'string' && part.length > 0).join(' ')
}
