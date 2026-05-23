import { componentIconAudit } from './componentCatalog'
import { inspectorEditorAudit } from './inspectorCatalog'

export function studioCatalogAudit() {
  const componentAudit = componentIconAudit()
  const inspectorAudit = inspectorEditorAudit()

  return {
    ok: componentAudit.ok && inspectorAudit.ok,
    componentAudit,
    inspectorAudit,
  }
}

const audit = studioCatalogAudit()

if (!audit.ok) {
  throw new Error(`Studio catalog audit failed: ${JSON.stringify(audit)}`)
}
