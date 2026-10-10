import { visualBindingAudit } from './bindingCatalog'
import { dataServiceAudit } from './dataServiceCatalog'
import { inspectorEditorAudit } from './inspectorCatalog'
import { studioInteractionAudit } from './interactionAudit'
import { packageInstallAudit } from './packageCatalog'

/**
 * The Studio's own catalog consistency check.
 *
 * The component-icon and device-API audits used to be members. Both panels now
 * read the platform's contracts over the API, so the local catalogs they
 * checked are gone; a payload the backend cannot produce is the failure that
 * matters now, and Python tests it there.
 */
export function studioCatalogAudit() {
  const bindingAudit = visualBindingAudit()
  const dataAudit = dataServiceAudit()
  const inspectorAudit = inspectorEditorAudit()
  const interactionAudit = studioInteractionAudit()
  const packageAudit = packageInstallAudit()

  return {
    ok: bindingAudit.ok && dataAudit.ok && inspectorAudit.ok && interactionAudit.ok && packageAudit.ok,
    bindingAudit,
    dataAudit,
    inspectorAudit,
    interactionAudit,
    packageAudit,
  }
}

const audit = studioCatalogAudit()

if (!audit.ok) {
  throw new Error(`Studio catalog audit failed: ${JSON.stringify(audit)}`)
}
