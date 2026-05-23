import { visualBindingAudit } from './bindingCatalog'
import { componentIconAudit } from './componentCatalog'
import { inspectorEditorAudit } from './inspectorCatalog'

export function studioCatalogAudit() {
  const bindingAudit = visualBindingAudit()
  const componentAudit = componentIconAudit()
  const inspectorAudit = inspectorEditorAudit()

  return {
    ok: bindingAudit.ok && componentAudit.ok && inspectorAudit.ok,
    bindingAudit,
    componentAudit,
    inspectorAudit,
  }
}

const audit = studioCatalogAudit()

if (!audit.ok) {
  throw new Error(`Studio catalog audit failed: ${JSON.stringify(audit)}`)
}
