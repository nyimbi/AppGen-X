import { useEffect, useState } from 'react'
import { STUDIO_ROUTES, studioGet } from './studioApi'

export type RouteAuditState =
  | { state: 'loading' }
  | { state: 'ready'; ok: boolean; served: number; declared: number; missing: string[] }
  | { state: 'error'; error: Error }

/**
 * Check that every route the client declares is one the backend serves.
 *
 * The Studio's panels each read one route, so a client route with no server
 * behind it renders an error state in a panel no one opened. This asks the
 * manifest what exists and compares it to the client's own table, which is the
 * only drift the frontend can still have: the catalogs are gone, the routes are
 * what is left.
 */
export function useRouteAudit(): RouteAuditState {
  const [state, setState] = useState<RouteAuditState>({ state: 'loading' })

  useEffect(() => {
    let live = true
    studioGet<{ paths: string[] }>('manifest').then(
      (manifest) => {
        if (!live) return
        const served = new Set(manifest.paths)
        const declared = Object.values(STUDIO_ROUTES).filter((route) => route !== STUDIO_ROUTES.manifest)
        const missing = declared.filter((route) => !served.has(route))
        setState({ state: 'ready', ok: missing.length === 0, served: served.size, declared: declared.length, missing })
      },
      (error: Error) => live && setState({ state: 'error', error }),
    )
    return () => {
      live = false
    }
  }, [])

  return state
}
