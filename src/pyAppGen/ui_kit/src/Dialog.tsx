import { useEffect, useRef, type ReactNode } from 'react'
import { cx } from './cx'

export type DialogProps = {
  open: boolean
  onClose: () => void
  title: ReactNode
  /** Body content. */
  children: ReactNode
  /** Footer slot, usually a cancel and a confirm button. */
  footer?: ReactNode
  /** Widen the panel for a form or a table. */
  size?: 'md' | 'lg'
  className?: string
}

const FOCUSABLE =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'

/** A modal dialog built on the native `<dialog>` element, which supplies the
 * top layer, the backdrop, and Escape-to-close without a focus-trap library.
 * Focus moves in on open, is kept inside while open, and returns to the
 * opener on close.
 */
export function Dialog({ open, onClose, title, children, footer, size = 'md', className }: DialogProps) {
  const ref = useRef<HTMLDialogElement>(null)
  const opener = useRef<Element | null>(null)

  useEffect(() => {
    const node = ref.current
    if (!node) return
    if (open && !node.open) {
      opener.current = document.activeElement
      node.showModal()
      const first = node.querySelector<HTMLElement>(FOCUSABLE)
      first?.focus()
    } else if (!open && node.open) {
      node.close()
      if (opener.current instanceof HTMLElement) opener.current.focus()
    }
  }, [open])

  return (
    <dialog
      aria-label={typeof title === 'string' ? title : undefined}
      className={cx('appgen-dialog', size === 'lg' && 'appgen-dialog--lg', className)}
      onCancel={(event) => {
        event.preventDefault()
        onClose()
      }}
      onClick={(event) => {
        // The backdrop is the dialog element itself; a click landing on it
        // rather than on the inner panel is a dismiss.
        if (event.target === ref.current) onClose()
      }}
      onKeyDown={(event) => {
        if (event.key !== 'Tab') return
        const node = ref.current
        if (!node) return
        const focusable = Array.from(node.querySelectorAll<HTMLElement>(FOCUSABLE))
        if (focusable.length === 0) return
        const first = focusable[0]
        const last = focusable[focusable.length - 1]
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault()
          last.focus()
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault()
          first.focus()
        }
      }}
      ref={ref}
    >
      <div className="appgen-dialog__panel">
        <header className="appgen-dialog__header">
          <h2 className="appgen-dialog__title">{title}</h2>
          <button aria-label="Close dialog" className="appgen-dialog__close" onClick={onClose} type="button">
            &times;
          </button>
        </header>
        <div className="appgen-dialog__body">{children}</div>
        {footer && <footer className="appgen-dialog__footer">{footer}</footer>}
      </div>
    </dialog>
  )
}
