/** Typed client for the generated Flask API.
 *
 * The routes come from `appgen.generated.ts`, which the generator writes from
 * the same contract the Flask views are built from, so a client method and its
 * server route cannot drift apart without the type-check failing.
 */

import { API_BASE, WORKBENCHES } from './appgen.generated'
import type { TableSpec, WorkbenchSpec, WorkbenchRender } from './appgen.generated'

export class ApiError extends Error {
  readonly status: number
  readonly route: string

  constructor(route: string, status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.route = route
  }
}

async function request<T>(route: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${route}`, {
    credentials: 'same-origin',
    headers: { Accept: 'application/json', ...(init?.body ? { 'Content-Type': 'application/json' } : {}) },
    ...init,
  })
  const text = await response.text()
  let payload: unknown = null
  if (text) {
    try {
      payload = JSON.parse(text)
    } catch {
      payload = text
    }
  }
  if (!response.ok) {
    const detail =
      payload && typeof payload === 'object' && 'message' in payload
        ? String((payload as { message: unknown }).message)
        : `${response.status} ${response.statusText}`
    throw new ApiError(route, response.status, detail)
  }
  return payload as T
}

/** List rows from a table's collection route. */
export function listRows<T = Record<string, unknown>>(table: TableSpec): Promise<T[]> {
  return request<T[]>(table.route)
}

/** Read one row by primary key. */
export function readRow<T = Record<string, unknown>>(table: TableSpec, id: string): Promise<T> {
  return request<T>(`${table.route}${encodeURIComponent(id)}`)
}

/** Create a row. */
export function createRow<T = Record<string, unknown>>(
  table: TableSpec,
  body: Record<string, unknown>,
): Promise<T> {
  return request<T>(table.route, { method: 'POST', body: JSON.stringify(body) })
}

/** Load a PBC workbench render payload. */
export function loadWorkbench(workbench: WorkbenchSpec): Promise<WorkbenchRender> {
  return request<WorkbenchRender>(`${workbench.route}/workbench.json`)
}

/** Load every workbench in the composition. */
export function loadWorkbenches(): Promise<WorkbenchRender[]> {
  return Promise.all(WORKBENCHES.map(loadWorkbench))
}
