import { useEffect, useState } from 'react'

export type StudioData<T> =
  | { state: 'loading' }
  | { state: 'ready'; data: T }
  | { state: 'error'; error: Error }

/**
 * Load one Studio route and track its three states.
 *
 * A panel that renders `undefined` while a fetch is in flight looks identical to
 * one whose catalog is empty, so the state is explicit and the caller decides
 * what each one looks like.
 */
export function useStudioData<T>(load: () => Promise<T>, deps: readonly unknown[] = []): StudioData<T> {
  const [state, setState] = useState<StudioData<T>>({ state: 'loading' })

  useEffect(() => {
    let live = true
    setState({ state: 'loading' })
    load().then(
      (data) => live && setState({ state: 'ready', data }),
      (error: Error) => live && setState({ state: 'error', error }),
    )
    return () => {
      live = false
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  return state
}
