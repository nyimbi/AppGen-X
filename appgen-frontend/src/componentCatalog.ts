import type { IconName } from './Icon'

export type ComponentCategory =
  | 'Inputs'
  | 'Choice'
  | 'Layouts'
  | 'Data'
  | 'Media'
  | 'Navigation'
  | 'Automation'
  | 'Targets'

export type PaletteComponent = {
  name: string
  category: ComponentCategory
  icon: IconName
  size: string
  description: string
}

export const paletteComponents: PaletteComponent[] = [
  { name: 'Text Box', category: 'Inputs', icon: 'input', size: '6 x 1', description: 'Single-line text and numeric entry.' },
  { name: 'Label', category: 'Inputs', icon: 'label', size: '3 x 1', description: 'Static captions, field labels, and headings.' },
  { name: 'Date Picker', category: 'Inputs', icon: 'calendar', size: '4 x 1', description: 'Date, time, and timestamp entry.' },
  { name: 'Button', category: 'Inputs', icon: 'button', size: '2 x 1', description: 'Commands, workflow actions, and submits.' },
  { name: 'Check Box', category: 'Choice', icon: 'check', size: '2 x 1', description: 'Boolean fields and toggle options.' },
  { name: 'Radio Button', category: 'Choice', icon: 'radio', size: '3 x 1', description: 'Exclusive option selection.' },
  { name: 'Combo Box', category: 'Choice', icon: 'combo', size: '4 x 1', description: 'Lookup and enumerated value picker.' },
  { name: 'List Box', category: 'Choice', icon: 'list', size: '4 x 4', description: 'Single or multi-select list control.' },
  { name: 'Layout', category: 'Layouts', icon: 'layout', size: '12 x 4', description: 'Responsive container with spacing rules.' },
  { name: 'Panel', category: 'Layouts', icon: 'panel', size: '12 x 3', description: 'Grouped visual region for related fields.' },
  { name: 'Data Grid', category: 'Data', icon: 'grid', size: '12 x 6', description: 'Editable tabular data with sort and filter.' },
  { name: 'Tree View', category: 'Data', icon: 'tree', size: '4 x 6', description: 'Hierarchical navigation and master records.' },
  { name: 'Chart', category: 'Data', icon: 'chart', size: '8 x 5', description: 'Operational metrics and dashboard visuals.' },
  { name: 'Database Source', category: 'Data', icon: 'database', size: '3 x 1', description: 'Dataset, query, and binding source.' },
  { name: 'Image', category: 'Media', icon: 'image', size: '4 x 3', description: 'Pictures, documents, and generated assets.' },
  { name: 'Main Menu', category: 'Navigation', icon: 'menu', size: '12 x 1', description: 'Application-level menus and shortcuts.' },
  { name: 'Report Viewer', category: 'Navigation', icon: 'report', size: '12 x 7', description: 'Invoices, statutory reports, and exports.' },
  { name: 'Agent', category: 'Automation', icon: 'agent', size: '3 x 2', description: 'LLM-backed task runner or assistant.' },
  { name: 'Workflow', category: 'Automation', icon: 'workflow', size: '6 x 4', description: 'Stateful approvals and process logic.' },
  { name: 'Web App', category: 'Targets', icon: 'web', size: 'target', description: 'Generated responsive browser application.' },
  { name: 'Mobile App', category: 'Targets', icon: 'mobile', size: 'target', description: 'Generated phone and tablet application.' },
  { name: 'Desktop App', category: 'Targets', icon: 'desktop', size: 'target', description: 'Generated installable desktop shell.' },
]

export const paletteCategories = Array.from(new Set(paletteComponents.map((component) => component.category)))
