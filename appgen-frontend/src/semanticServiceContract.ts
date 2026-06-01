import type { IconName } from './Icon'

export type SemanticServiceSurface =
  | 'dsl_editor'
  | 'component_palette'
  | 'form_designer'
  | 'database_designer'
  | 'workflow_designer'
  | 'pbc_composition_designer'
  | 'package_deployment_designer'
  | 'diagnostics_panel'
  | 'graph_explain_panel'
  | 'natural_language_planner'

type SemanticService = {
  id: string
  label: string
  icon: IconName
  evidence: string
}

type SemanticSurface = {
  id: SemanticServiceSurface
  label: string
  icon: IconName
  contract: string
}

export const semanticServices: SemanticService[] = [
  { id: 'lsp', label: 'Language service', icon: 'workflow', evidence: 'appgen.lsp-service.v1' },
  { id: 'designer_sync', label: 'Designer sync', icon: 'layout', evidence: 'appgen.designer-sync-report.v1' },
  { id: 'graph_suite', label: 'Graph suite', icon: 'flow', evidence: 'appgen.graph-suite-report.v1' },
  { id: 'nl_plan', label: 'Change planner', icon: 'agent', evidence: 'appgen.nl-plan.v1' },
]

export const semanticSurfaces: SemanticSurface[] = [
  { id: 'dsl_editor', label: 'DSL editor', icon: 'file', contract: 'appgen.designer-dsl-editor.v1' },
  { id: 'component_palette', label: 'Component palette', icon: 'drag', contract: 'appgen.designer-component-palette.v1' },
  { id: 'form_designer', label: 'Form designer', icon: 'form', contract: 'appgen.designer-form-projection.v1' },
  { id: 'database_designer', label: 'Database designer', icon: 'database', contract: 'appgen.designer-database-projection.v1' },
  { id: 'workflow_designer', label: 'Workflow designer', icon: 'workflow', contract: 'appgen.designer-workflow-projection.v1' },
  {
    id: 'pbc_composition_designer',
    label: 'PBC composition',
    icon: 'package',
    contract: 'appgen.designer-pbc-composition-projection.v1',
  },
  {
    id: 'package_deployment_designer',
    label: 'Package deployment',
    icon: 'desktop',
    contract: 'appgen.designer-package-deployment-projection.v1',
  },
  { id: 'diagnostics_panel', label: 'Diagnostics', icon: 'rule', contract: 'appgen.lsp-diagnostics.v1' },
  { id: 'graph_explain_panel', label: 'Graphs and explain', icon: 'flow', contract: 'appgen.designer-graph-explain-panel.v1' },
  {
    id: 'natural_language_planner',
    label: 'Natural language planner',
    icon: 'bot',
    contract: 'appgen.designer-nl-planner-panel.v1',
  },
]

export function semanticServiceAudit() {
  const requiredSurfaces: SemanticServiceSurface[] = [
    'dsl_editor',
    'component_palette',
    'form_designer',
    'database_designer',
    'workflow_designer',
    'pbc_composition_designer',
    'package_deployment_designer',
    'diagnostics_panel',
    'graph_explain_panel',
    'natural_language_planner',
  ]
  const requiredServices = [
    'appgen.lsp-service.v1',
    'appgen.designer-sync-report.v1',
    'appgen.graph-suite-report.v1',
    'appgen.nl-plan.v1',
  ]
  const requiredSurfaceContracts = [
    'appgen.designer-dsl-editor.v1',
    'appgen.designer-component-palette.v1',
    'appgen.designer-form-projection.v1',
    'appgen.designer-database-projection.v1',
    'appgen.designer-workflow-projection.v1',
    'appgen.designer-pbc-composition-projection.v1',
    'appgen.designer-package-deployment-projection.v1',
    'appgen.lsp-diagnostics.v1',
    'appgen.designer-graph-explain-panel.v1',
    'appgen.designer-nl-planner-panel.v1',
  ]
  const surfaceIds = new Set(semanticSurfaces.map((surface) => surface.id))
  const services = semanticServices.map((service) => service.evidence)
  const evidence = new Set(services)
  const surfaceContracts = semanticSurfaces.map((surface) => surface.contract)
  const observedSurfaceContracts = new Set(surfaceContracts)
  const missingSurfaces = requiredSurfaces.filter((surface) => !surfaceIds.has(surface))
  const missingServices = requiredServices.filter((item) => !evidence.has(item))
  const missingSurfaceContracts = requiredSurfaceContracts.filter((item) => !observedSurfaceContracts.has(item))

  return {
    format: 'appgen.frontend-semantic-service-audit.v1',
    ok: missingSurfaces.length === 0 && missingServices.length === 0 && missingSurfaceContracts.length === 0,
    serviceCount: semanticServices.length,
    requiredServiceCount: requiredServices.length,
    services,
    requiredServices,
    missingServices,
    missingServiceCount: missingServices.length,
    surfaceCount: semanticSurfaces.length,
    requiredSurfaceCount: requiredSurfaces.length,
    surfaces: semanticSurfaces.map((surface) => surface.id),
    requiredSurfaces,
    missingSurfaces,
    missingSurfaceCount: missingSurfaces.length,
    surfaceContractCount: surfaceContracts.length,
    requiredSurfaceContractCount: requiredSurfaceContracts.length,
    surfaceContracts,
    requiredSurfaceContracts,
    missingSurfaceContracts,
    missingSurfaceContractCount: missingSurfaceContracts.length,
  }
}
