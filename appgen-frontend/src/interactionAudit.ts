import {
  componentDragPayload,
  filterPaletteComponents,
  groupPaletteComponents,
  paletteCategoryCounts,
} from './ComponentPalette'
import { visualBindingAudit } from './bindingCatalog'
import { componentIconAudit, paletteComponents } from './componentCatalog'
import { dataServiceAudit, dataServiceCapabilities } from './dataServiceCatalog'
import type { DataServiceLane } from './dataServiceCatalog'
import { deviceApiAudit, deviceApiCapabilities } from './deviceApiCatalog'
import type { DeviceApiGroup } from './deviceApiCatalog'
import { inspectorEditorAudit } from './inspectorCatalog'
import { packageInstallAudit } from './packageCatalog'
import { semanticServiceAudit } from './semanticServiceContract'

const requiredDeviceGroups: DeviceApiGroup[] = [
  'Sensors',
  'Media',
  'Permissions',
  'Connectivity',
  'Storage',
  'Notifications',
  'Background',
  'Security',
]

const requiredDataLanes: DataServiceLane[] = ['Source', 'Query', 'Publish', 'Embedded DB', 'Resilience', 'Security']

export function studioInteractionAudit() {
  const categoryCounts = paletteCategoryCounts()
  const deviceComponents = filterPaletteComponents('Device', '')
  const storageSearch = filterPaletteComponents('All', 'storage')
  const emptySearch = filterPaletteComponents('All', 'definitely-not-a-component')
  const groupedStorage = groupPaletteComponents(storageSearch)
  const button = paletteComponents.find((component) => component.name === 'Button')
  const dragPayload = button ? componentDragPayload(button) : null
  const deviceGroups = new Set(deviceApiCapabilities.map((capability) => capability.group))
  const dataLanes = new Set(dataServiceCapabilities.map((capability) => capability.lane))
  const bindingAudit = visualBindingAudit()
  const componentAudit = componentIconAudit()
  const dataAudit = dataServiceAudit()
  const deviceAudit = deviceApiAudit()
  const inspectorAudit = inspectorEditorAudit()
  const packageAudit = packageInstallAudit()
  const semanticAudit = semanticServiceAudit()

  const scenarios = [
    {
      id: 'palette_category_filter',
      ok:
        deviceComponents.length === categoryCounts.Device &&
        deviceComponents.length > 0 &&
        deviceComponents.every((component) => component.category === 'Device'),
      evidence: { count: deviceComponents.length, expected: categoryCounts.Device },
    },
    {
      id: 'palette_search_filter',
      ok:
        storageSearch.some((component) => component.name === 'Secure Storage') &&
        storageSearch.some((component) => component.name === 'File Storage') &&
        groupedStorage.length > 0,
      evidence: { matches: storageSearch.map((component) => component.name), groups: groupedStorage.map((group) => group.category) },
    },
    {
      id: 'palette_empty_state',
      ok: emptySearch.length === 0,
      evidence: { count: emptySearch.length },
    },
    {
      id: 'component_drag_payload',
      ok:
        dragPayload !== null &&
        dragPayload.component === 'Button' &&
        dragPayload.category === 'Inputs' &&
        dragPayload.icon === 'button' &&
        dragPayload.draggable,
      evidence: dragPayload,
    },
    {
      id: 'device_workbench_render_inputs',
      ok: requiredDeviceGroups.every((group) => deviceGroups.has(group)) && deviceAudit.ok,
      evidence: { groups: Array.from(deviceGroups), total: deviceAudit.totalCapabilities },
    },
    {
      id: 'data_workbench_render_inputs',
      ok: requiredDataLanes.every((lane) => dataLanes.has(lane)) && dataAudit.ok,
      evidence: { lanes: Array.from(dataLanes), total: dataAudit.totalCapabilities },
    },
    {
      id: 'status_rail_audit_inputs',
      ok:
        bindingAudit.ok &&
        componentAudit.ok &&
        dataAudit.ok &&
        deviceAudit.ok &&
        inspectorAudit.ok &&
        packageAudit.ok &&
        semanticAudit.ok,
      evidence: {
        bindings: bindingAudit.totalBindings,
        components: componentAudit.totalComponents,
        data: dataAudit.totalCapabilities,
        devices: deviceAudit.totalCapabilities,
        editors: inspectorAudit.totalEditors,
        packages: packageAudit.totalPackages,
        semanticSurfaces: semanticAudit.surfaceCount,
      },
    },
    {
      id: 'semantic_service_bridge',
      ok: semanticAudit.ok,
      evidence: semanticAudit,
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
