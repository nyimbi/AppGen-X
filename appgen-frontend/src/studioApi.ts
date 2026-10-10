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
  designer: '/api/studio/designer',
  dataServices: '/api/studio/data-services',
  inspector: '/api/studio/inspector',
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

/** One binding graph node, e.g. `field:name` or `control:name`. */
export type BindingNode = {
  id: string
  kind: string
  table?: string
  field?: string
  field_type?: string
  mode?: string
}

export type BindingEdge = {
  from: string
  to: string
  kind: string
  mode?: string
}

export type BindingGraph = {
  format: string
  table: string
  nodes: readonly BindingNode[]
  edges: readonly BindingEdge[]
  converters: readonly string[]
  validators: readonly string[]
}

/** One visual lane. `format` is the contract the lane renders. */
export type DesignerLane = {
  lane: string
  label: string
  icon: string
  format: string
  items: readonly { name: string; value: string; detail: string }[]
  operations: readonly string[]
  tokens?: readonly string[]
  states?: readonly string[]
  targets?: readonly string[]
  import_formats?: readonly string[]
  effects?: readonly string[]
  effects_format?: string
}

export type DesignerPayload = {
  format: string
  ok: boolean
  form: {
    format: string
    views: readonly {
      view: string
      table: string
      sections: readonly { name: string; fields: readonly string[] }[]
      components: readonly { binding: string; component: string; x: number; y: number; w: number; h: number }[]
      handlers: readonly string[]
      valid_bindings: readonly string[]
    }[]
  }
  binding_graph: BindingGraph
  binding_families: {
    format: string
    ok: boolean
    families: readonly { family: string; surfaces: readonly string[]; guards: readonly string[] }[]
    guards: readonly string[]
  }
  lanes: readonly DesignerLane[]
}

/** A data tooling lane and the contracts it renders. */
export type DataServiceLane = {
  lane: string
  icon: string
  capabilities: readonly { key: string; format: string; evidence: Record<string, unknown> }[]
}

export type DataServicesPayload = {
  format: string
  ok: boolean
  decision: string
  blocking_gaps: readonly unknown[]
  readiness: {
    format: string
    ok: boolean
    phases: readonly { phase: string; ok: boolean; steps: readonly string[] }[]
    blocking_gaps: readonly unknown[]
  }
  lanes: readonly DataServiceLane[]
}

/** One component's registered property, event, component, and custom editors. */
export type InspectorRegistry = {
  component: string
  property_editors: readonly { property: string; editor: string; factory: string }[]
  event_editors: readonly { event: string; factory: string; lifecycle: readonly string[] }[]
  component_editors: readonly { verb: string; scope: string; requires_selection: boolean }[]
  custom_designers: readonly { hook: string; surface: string; supports_multi_select: boolean }[]
}

export type InspectorPayload = {
  format: string
  ok: boolean
  decision: string
  blocking_gaps: readonly unknown[]
  registries: readonly InspectorRegistry[]
  grouping: readonly {
    component: string
    groups: Record<string, readonly string[]>
    filters: readonly string[]
  }[]
  diagnostics: readonly {
    format: string
    ok: boolean
    component: string
    diagnostics: readonly {
      code: string
      property?: string
      target?: string
      severity: string
      surface: string
      quick_fix: string
    }[]
  }[]
  action_registry: {
    component: string
    actions: readonly { action: string; handler: string; signature: string; callers: readonly string[] }[]
  }
  readiness: {
    format: string
    ok: boolean
    components: readonly string[]
    final_state: Record<string, number>
    phases: readonly { phase: string; ok: boolean; steps: number }[]
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
export const loadDesigner = () => studioGet<DesignerPayload>('designer')
export const loadDataServices = () => studioGet<DataServicesPayload>('dataServices')
export const loadInspector = () => studioGet<InspectorPayload>('inspector')
