import { visualBindingAudit } from './bindingCatalog'
import { componentIconAudit } from './componentCatalog'
import { dataServiceAudit } from './dataServiceCatalog'
import { deviceApiAudit } from './deviceApiCatalog'
import { studioInteractionAudit } from './interactionAudit'
import { inspectorEditorAudit } from './inspectorCatalog'
import { packageInstallAudit } from './packageCatalog'

export function studioCatalogAudit() {
  const bindingAudit = visualBindingAudit()
  const componentAudit = componentIconAudit()
  const dataAudit = dataServiceAudit()
  const deviceAudit = deviceApiAudit()
  const inspectorAudit = inspectorEditorAudit()
  const interactionAudit = studioInteractionAudit()
  const packageAudit = packageInstallAudit()

  return {
    ok:
      bindingAudit.ok &&
      componentAudit.ok &&
      dataAudit.ok &&
      deviceAudit.ok &&
      inspectorAudit.ok &&
      interactionAudit.ok &&
      packageAudit.ok,
    bindingAudit,
    componentAudit,
    dataAudit,
    deviceAudit,
    inspectorAudit,
    interactionAudit,
    packageAudit,
  }
}

const audit = studioCatalogAudit()

if (!audit.ok) {
  throw new Error(`Studio catalog audit failed: ${JSON.stringify(audit)}`)
}
