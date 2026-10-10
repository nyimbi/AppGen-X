import { createContext, useCallback, useContext, useMemo, useRef, useState, type ReactNode } from 'react'
import { cx } from './cx'

export type ToastTone = 'info' | 'success' | 'warning' | 'danger'

export type Toast = {
  id: string
  message: ReactNode
  tone?: ToastTone
  /** Milliseconds before auto-dismiss; 0 keeps it until dismissed. */
  duration?: number
}

export type ToastApi = {
  push: (toast: Omit<Toast, 'id'> & { id?: string }) => string
  dismiss: (id: string) => void
}

const ToastContext = createContext<ToastApi | null>(null)

/** Access the toast queue. Throws when used outside a `<ToastProvider>` so a
 * missing provider fails at the call site, not silently in a dead queue.
 */
export function useToast(): ToastApi {
  const api = useContext(ToastContext)
  if (!api) throw new Error('useToast must be used inside a <ToastProvider>')
  return api
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])
  const counter = useRef(0)

  const dismiss = useCallback((id: string) => {
    setToasts((current) => current.filter((toast) => toast.id !== id))
  }, [])

  const push = useCallback<ToastApi['push']>(
    (toast) => {
      const id = toast.id ?? `toast-${(counter.current += 1)}`
      const duration = toast.duration ?? 5000
      setToasts((current) => [...current, { ...toast, id }])
      if (duration > 0) window.setTimeout(() => dismiss(id), duration)
      return id
    },
    [dismiss],
  )

  const api = useMemo(() => ({ push, dismiss }), [push, dismiss])

  return (
    <ToastContext.Provider value={api}>
      {children}
      <div aria-live="polite" aria-relevant="additions" className="appgen-toast-region">
        {toasts.map((toast) => (
          <div className={cx('appgen-toast', `appgen-toast--${toast.tone ?? 'info'}`)} key={toast.id} role="status">
            <span className="appgen-toast__message">{toast.message}</span>
            <button aria-label="Dismiss notification" className="appgen-toast__close" onClick={() => dismiss(toast.id)} type="button">
              &times;
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}
