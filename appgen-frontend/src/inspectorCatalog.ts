import { iconNames } from './Icon'
import type { IconName } from './Icon'

export type InspectorEditorKind = 'Property' | 'Event' | 'Component' | 'Custom Designer'

export type InspectorEditor = {
  kind: InspectorEditorKind
  name: string
  value: string
  icon: IconName
  action: string
}

export const inspectorEditors: InspectorEditor[] = [
  {
    kind: 'Property',
    name: 'Columns',
    value: 'Item, Qty, Price, Tax, Total',
    icon: 'dataGrid',
    action: 'Edit columns',
  },
  {
    kind: 'Property',
    name: 'Data source',
    value: 'Invoice.lines',
    icon: 'database',
    action: 'Bind source',
  },
  {
    kind: 'Property',
    name: 'Style',
    value: 'Dense finance grid',
    icon: 'style',
    action: 'Open style',
  },
  {
    kind: 'Event',
    name: 'OnRowValidate',
    value: 'validateLineItem',
    icon: 'workflow',
    action: 'Edit handler',
  },
  {
    kind: 'Event',
    name: 'OnContextAction',
    value: 'openLineActions',
    icon: 'popup',
    action: 'Route action',
  },
  {
    kind: 'Component',
    name: 'Column Builder',
    value: '5 editable columns',
    icon: 'table',
    action: 'Configure',
  },
  {
    kind: 'Component',
    name: 'Lookup Columns',
    value: 'Product, Tax Code',
    icon: 'lookup',
    action: 'Map lookups',
  },
  {
    kind: 'Custom Designer',
    name: 'Grid Layout Designer',
    value: 'Snap, resize, reorder',
    icon: 'layout',
    action: 'Open designer',
  },
  {
    kind: 'Custom Designer',
    name: 'Target Preview',
    value: 'Web, mobile, desktop',
    icon: 'desktop',
    action: 'Preview',
  },
]

export const inspectorKindIcons: Record<InspectorEditorKind, IconName> = {
  Property: 'style',
  Event: 'workflow',
  Component: 'panel',
  'Custom Designer': 'layout',
}

export function inspectorEditorAudit() {
  const registeredIcons = new Set(iconNames)
  const requiredKinds: InspectorEditorKind[] = ['Property', 'Event', 'Component', 'Custom Designer']
  const missingIcons = inspectorEditors.filter((editor) => !registeredIcons.has(editor.icon))
  const missingKindIcons = requiredKinds.filter((kind) => !registeredIcons.has(inspectorKindIcons[kind]))
  const kindCoverage = requiredKinds.map((kind) => {
    const editors = inspectorEditors.filter((editor) => editor.kind === kind)
    return {
      kind,
      count: editors.length,
      icons: Array.from(new Set(editors.map((editor) => editor.icon))),
    }
  })

  return {
    ok:
      missingIcons.length === 0 &&
      missingKindIcons.length === 0 &&
      kindCoverage.every((item) => item.count > 0 && item.icons.length > 0),
    totalEditors: inspectorEditors.length,
    missingIcons,
    missingKindIcons,
    kindCoverage,
  }
}
