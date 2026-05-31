import type { IconName } from './Icon'
import type { PaletteComponent } from './componentCatalog'

export type PlacedComponentTone =
  | 'automation'
  | 'choice'
  | 'data'
  | 'graphics'
  | 'inputs'
  | 'layouts'
  | 'media'
  | 'navigation'
  | 'targets'

export type PlacedComponent = {
  id: string
  name: string
  icon: IconName
  x: number
  y: number
  w: number
  h: number
  tone: PlacedComponentTone
  binding: string
  source: 'initial' | 'component_palette'
  handler?: {
    event: string
    target: string
    signature: string
  }
}

export type ComponentDragPayload = {
  format: 'appgen.frontend-component-drag-payload.v1'
  component: string
  category: PaletteComponent['category']
  icon: IconName
  size: string
  draggable: true
  source: 'component_palette'
}

export type DropTarget = {
  x: number
  y: number
}

export type DesignerDropOperation = {
  format: 'appgen.frontend-component-drop-operation.v1'
  ok: boolean
  operation: 'bind_event_to_handler' | 'place_bound_component'
  payload: ComponentDragPayload
  preview: PlacedComponent
  handlerDefinition: {
    event: string
    target: string
    signature: string
  }
  dslPatch: string[]
  changedSurfaces: string[]
}

export const initialPlacedComponents: PlacedComponent[] = [
  { id: 'main-menu', name: 'Main Menu', icon: 'menu', x: 4, y: 4, w: 92, h: 7, tone: 'navigation', binding: 'MainMenu', source: 'initial', handler: { event: 'Open', target: 'ReverseInvoice', signature: 'sender, context' } },
  { id: 'customer-name', name: 'Customer Name', icon: 'input', x: 7, y: 16, w: 36, h: 8, tone: 'inputs', binding: 'Invoice.customer.name', source: 'initial' },
  { id: 'account-lookup', name: 'Account Lookup', icon: 'lookup', x: 48, y: 16, w: 26, h: 8, tone: 'choice', binding: 'Invoice.customer_id', source: 'initial' },
  { id: 'invoice-date', name: 'Invoice Date', icon: 'calendar', x: 77, y: 16, w: 19, h: 8, tone: 'inputs', binding: 'Invoice.date', source: 'initial' },
  { id: 'line-items', name: 'Line Items', icon: 'dataGrid', x: 7, y: 35, w: 67, h: 26, tone: 'data', binding: 'Invoice.lines', source: 'initial' },
  { id: 'popup-actions', name: 'Popup Actions', icon: 'popup', x: 78, y: 35, w: 18, h: 8, tone: 'navigation', binding: 'InvoiceForm.PopupActions', source: 'initial', handler: { event: 'Open', target: 'ShowInvoiceActions', signature: 'sender, context' } },
  { id: 'approval-agent', name: 'Approval Agent', icon: 'agent', x: 78, y: 49, w: 18, h: 8, tone: 'automation', binding: 'Approval.status', source: 'initial', handler: { event: 'Explain', target: 'InvoiceAssistant', signature: 'sender, context' } },
  { id: 'totals-chart', name: 'Totals Chart', icon: 'chart', x: 7, y: 73, w: 30, h: 10, tone: 'data', binding: 'Invoice.total', source: 'initial' },
  { id: 'receipt-camera', name: 'Receipt Camera', icon: 'camera', x: 41, y: 73, w: 24, h: 10, tone: 'media', binding: 'Receipt.image', source: 'initial' },
  { id: 'mobile-target', name: 'Mobile Target', icon: 'mobile', x: 69, y: 73, w: 27, h: 10, tone: 'targets', binding: 'ReleaseMobile', source: 'initial' },
]

const toneByCategory: Record<PaletteComponent['category'], PlacedComponentTone> = {
  Inputs: 'inputs',
  Choice: 'choice',
  Layouts: 'layouts',
  Data: 'data',
  Graphics: 'graphics',
  Media: 'media',
  Navigation: 'navigation',
  Automation: 'automation',
  Effects: 'automation',
  Sensors: 'automation',
  '3D': 'graphics',
  Device: 'media',
  Targets: 'targets',
}

export function createComponentDragPayload(component: PaletteComponent): ComponentDragPayload {
  return {
    format: 'appgen.frontend-component-drag-payload.v1',
    component: component.name,
    category: component.category,
    icon: component.icon,
    size: component.size,
    draggable: true,
    source: 'component_palette',
  }
}

export function previewComponentDropOperation(payload: ComponentDragPayload, target: DropTarget): DesignerDropOperation {
  const componentName = payload.component.replace(/\s+/g, '')
  const event = payload.component === 'Button' ? 'Click' : payload.category === 'Navigation' ? 'Open' : 'Change'
  const handlerTarget = `${componentName}${event}`
  const handlerDefinition = {
    event,
    target: handlerTarget,
    signature: 'sender, context',
  }
  const preview: PlacedComponent = {
    id: `dropped-${slug(payload.component)}-${Math.round(target.x)}-${Math.round(target.y)}`,
    name: payload.component,
    icon: payload.icon,
    x: clamp(target.x, 3, 88),
    y: clamp(target.y, 11, 86),
    w: payload.category === 'Layouts' ? 38 : payload.category === 'Data' ? 34 : 22,
    h: payload.category === 'Layouts' || payload.category === 'Data' ? 16 : 8,
    tone: toneByCategory[payload.category],
    binding: payload.category === 'Inputs' || payload.category === 'Choice' ? `Invoice.${slug(payload.component)}` : payload.component,
    source: 'component_palette',
    handler: handlerDefinition,
  }

  return {
    format: 'appgen.frontend-component-drop-operation.v1',
    ok: payload.draggable === true && payload.source === 'component_palette',
    operation: payload.component === 'Button' ? 'bind_event_to_handler' : 'place_bound_component',
    payload,
    preview,
    handlerDefinition,
    dslPatch: [
      `@ ${preview.binding} ${payload.component.replace(/\s+/g, '')} ${Math.round(preview.x)} ${Math.round(preview.y)} ${Math.round(preview.w)} ${Math.round(preview.h)}`,
      `on ${handlerDefinition.event} -> ${handlerDefinition.target}`,
    ],
    changedSurfaces: ['form_designer', 'component_palette', 'object_inspector'],
  }
}

export function commitComponentDropOperation(
  components: PlacedComponent[],
  payload: ComponentDragPayload,
  target: DropTarget,
) {
  const operation = previewComponentDropOperation(payload, target)
  const committed = {
    ...operation.preview,
    id: uniqueId(operation.preview.id, components),
  }

  return {
    ...operation,
    committed,
    components: [...components, committed],
    componentCountBefore: components.length,
    componentCountAfter: components.length + 1,
  }
}

export function designerRuntimeAudit() {
  const buttonPayload = createComponentDragPayload({
    name: 'Button',
    category: 'Inputs',
    icon: 'button',
    size: '2 x 1',
    description: 'Commands, workflow actions, and submits.',
  })
  const preview = previewComponentDropOperation(buttonPayload, { x: 62, y: 62 })
  const commit = commitComponentDropOperation(initialPlacedComponents, buttonPayload, { x: 62, y: 62 })
  const checks = [
    { id: 'palette_drag_source', ok: buttonPayload.source === 'component_palette' && buttonPayload.draggable },
    { id: 'canvas_drop_target', ok: preview.ok && preview.preview.x === 62 && preview.preview.y === 62 },
    { id: 'component_drop_preview', ok: preview.dslPatch.length === 2 && preview.changedSurfaces.includes('form_designer') },
    { id: 'component_drop_commit', ok: commit.componentCountAfter === commit.componentCountBefore + 1 },
    { id: 'handler_definition_flow', ok: commit.handlerDefinition.target === 'ButtonClick' && commit.handlerDefinition.signature === 'sender, context' },
  ]

  return {
    format: 'appgen.frontend-visual-designer-runtime-audit.v1',
    ok: checks.every((check) => check.ok),
    checks,
    dragPayload: buttonPayload,
    preview,
    commit: {
      operation: commit.operation,
      componentCountBefore: commit.componentCountBefore,
      componentCountAfter: commit.componentCountAfter,
      handlerDefinition: commit.handlerDefinition,
      dslPatch: commit.dslPatch,
    },
  }
}

function slug(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '')
}

function clamp(value: number, min: number, max: number) {
  return Math.max(min, Math.min(max, value))
}

function uniqueId(base: string, components: PlacedComponent[]) {
  const existing = new Set(components.map((component) => component.id))
  if (!existing.has(base)) {
    return base
  }
  let index = 2
  while (existing.has(`${base}-${index}`)) {
    index += 1
  }
  return `${base}-${index}`
}
