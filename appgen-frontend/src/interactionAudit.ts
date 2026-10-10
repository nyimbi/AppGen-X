import { visualBindingAudit } from './bindingCatalog'
import { dataServiceAudit, dataServiceCapabilities } from './dataServiceCatalog'
import type { DataServiceLane } from './dataServiceCatalog'
import { inspectorEditorAudit } from './inspectorCatalog'
import { packageInstallAudit } from './packageCatalog'

const requiredDataLanes: DataServiceLane[] = ['Source', 'Query', 'Publish', 'Embedded DB', 'Resilience', 'Security']

/**
 * The scenarios the Studio's own panels depend on.
 *
 * The palette, component-icon, device, and semantic-service scenarios used to
 * live here, asserted against local TypeScript catalogs. Those panels now read
 * the platform's contracts over the API, so the scenarios were checking a
 * fabricated list the app no longer rendered. Their real check is the backend
 * payload contract, tested in Python, plus the browser smoke's rendered-text
 * assertions. What remains here covers the panels that still render from a
 * local catalog.
 */
export function studioInteractionAudit() {
  const dataLanes = new Set(dataServiceCapabilities.map((capability) => capability.lane))
  const bindingAudit = visualBindingAudit()
  const dataAudit = dataServiceAudit()
  const inspectorAudit = inspectorEditorAudit()
  const packageAudit = packageInstallAudit()

  const scenarios = [
    {
      id: 'data_workbench_render_inputs',
      ok: requiredDataLanes.every((lane) => dataLanes.has(lane)) && dataAudit.ok,
      evidence: { lanes: Array.from(dataLanes), total: dataAudit.totalCapabilities },
    },
    {
      id: 'status_rail_audit_inputs',
      ok: bindingAudit.ok && dataAudit.ok && inspectorAudit.ok && packageAudit.ok,
      evidence: {
        bindings: bindingAudit.totalBindings,
        data: dataAudit.totalCapabilities,
        editors: inspectorAudit.totalEditors,
        packages: packageAudit.totalPackages,
      },
    },
  ]

  return {
    format: 'appgen.frontend-interaction-audit.v1',
    ok: scenarios.every((scenario) => scenario.ok),
    totalScenarios: scenarios.length,
    scenarios,
    blockingScenarios: scenarios.filter((scenario) => !scenario.ok),
  }
}
