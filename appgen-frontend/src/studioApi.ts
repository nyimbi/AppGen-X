/**
 * The Studio's typed client for the Python backend.
 *
 * Every panel reads its catalog here rather than from a local module, so the
 * Studio and the platform cannot disagree about which components, packages, or
 * capabilities exist. The routes are the ones `studio_backend.studio_api_manifest`
 * serves, and a test asserts both halves name the same set.
 */

export const STUDIO_API_FORMAT = 'appgen.studio-api.v1'

export const STUDIO_ROUTES = {
  workspace: '/api/studio/workspace',
  components: '/api/studio/components',
  packages: '/api/studio/packages',
  targets: '/api/studio/targets',
  tokens: '/api/studio/tokens',
  semanticService: '/api/studio/semantic-service',
  manifest: '/api/studio/manifest',
} as const

export type StudioRoute = keyof typeof STUDIO_ROUTES

export class StudioApiError extends Error {
  constructor(route: string, public readonly status: number, message: string) {
    super(message)
    this.name = 'StudioApiError'
  }
}

export type PaletteComponent = {
  component: string
  /** Display name, e.g. "Secure Storage" for `SecureStore`. */
  label: string
  description: string
  icon: string
  category: string
  category_label: string
  /** Drag footprint, e.g. "4 x 1". */
  size: string
  field_types: readonly string[]
  properties?: readonly string[]
}

export type PaletteGroup = {
  category: string
  label: string
  icon: string
  /** Component names in this category, in listing order. */
  components: readonly string[]
}

export type ComponentPalettePayload = {
  format: string
  ok: boolean
  components: readonly PaletteComponent[]
  categories: readonly string[]
  groups: readonly PaletteGroup[]
}

export type ComponentPackage = {
  id: string
  vendor: string
  frameworks: readonly string[]
  license: string
  categories: readonly string[]
  components: readonly string[]
  use_cases?: readonly string[]
}

export type ComponentPackagesPayload = {
  format: string
  ok: boolean
  packages: readonly ComponentPackage[]
}

export type TargetCapabilityPayload = {
  format: string
  ok: boolean
  targets: readonly Record<string, unknown>[]
  mobile: { permissions: readonly string[]; target: Record<string, unknown> }
  desktop: { target: Record<string, unknown> }
}

export type SemanticServicePayload = {
  format: string
  ok: boolean
  semantic_service: {
    format: string
    ok: boolean
    services: Record<string, string>
    designer_surfaces: Record<string, { format?: string }>
    checks: readonly { id: string; ok: boolean }[]
    blocking_gaps: readonly unknown[]
  }
}

/** Fetch one Studio route. Throws on a non-2xx so a caller never renders `undefined`. */
export async function studioGet<T>(route: StudioRoute, init?: RequestInit): Promise<T> {
  const path = STUDIO_ROUTES[route]
  const response = await fetch(path, {
    headers: { Accept: 'application/json' },
    ...init,
  })
  if (!response.ok) {
    throw new StudioApiError(path, response.status, `Studio API ${path} returned ${response.status}`)
  }
  const payload = (await response.json()) as T & { format?: string; ok?: boolean }
  if (payload.format !== STUDIO_API_FORMAT) {
    throw new StudioApiError(path, response.status, `Studio API ${path} returned an unexpected format`)
  }
  return payload
}

export const loadComponentPalette = () => studioGet<ComponentPalettePayload>('components')
export const loadComponentPackages = () => studioGet<ComponentPackagesPayload>('packages')
export const loadTargetCapabilities = () => studioGet<TargetCapabilityPayload>('targets')
export const loadSemanticService = () => studioGet<SemanticServicePayload>('semanticService')
