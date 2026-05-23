import { visualBindingAudit } from './bindingCatalog'
import { componentIconAudit } from './componentCatalog'
import { inspectorEditorAudit } from './inspectorCatalog'
import { packageInstallAudit } from './packageCatalog'

export function studioCatalogAudit() {
  const bindingAudit = visualBindingAudit()
  const componentAudit = componentIconAudit()
  const inspectorAudit = inspectorEditorAudit()
  const packageAudit = packageInstallAudit()

  return {
    ok: bindingAudit.ok && componentAudit.ok && inspectorAudit.ok && packageAudit.ok,
    bindingAudit,
    componentAudit,
    inspectorAudit,
    packageAudit,
  }
}

const audit = studioCatalogAudit()

if (!audit.ok) {
  throw new Error(`Studio catalog audit failed: ${JSON.stringify(audit)}`)
}
