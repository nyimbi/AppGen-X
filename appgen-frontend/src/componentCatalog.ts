import { iconNames } from './Icon'
import type { IconName } from './Icon'

export type ComponentCategory =
  | 'Inputs'
  | 'Choice'
  | 'Layouts'
  | 'Data'
  | 'Graphics'
  | 'Media'
  | 'Navigation'
  | 'Automation'
  | 'Effects'
  | 'Sensors'
  | '3D'
  | 'Device'
  | 'Targets'

export type PaletteComponent = {
  name: string
  category: ComponentCategory
  icon: IconName
  size: string
  description: string
}

export const categoryIcons: Record<ComponentCategory | 'All', IconName> = {
  All: 'grid',
  Inputs: 'input',
  Choice: 'check',
  Layouts: 'layout',
  Data: 'database',
  Graphics: 'shape',
  Media: 'image',
  Navigation: 'menu',
  Automation: 'agent',
  Effects: 'animation',
  Sensors: 'gesture',
  '3D': 'viewport3d',
  Device: 'mobile',
  Targets: 'desktop',
}

export const paletteComponents: PaletteComponent[] = [
  { name: 'Text Box', category: 'Inputs', icon: 'input', size: '6 x 1', description: 'Single-line text and numeric entry.' },
  { name: 'Text Area', category: 'Inputs', icon: 'textarea', size: '6 x 3', description: 'Multi-line notes, comments, and rich descriptions.' },
  { name: 'Label', category: 'Inputs', icon: 'label', size: '3 x 1', description: 'Static captions, field labels, and headings.' },
  { name: 'Date Picker', category: 'Inputs', icon: 'calendar', size: '4 x 1', description: 'Date, time, and timestamp entry.' },
  { name: 'Number Field', category: 'Inputs', icon: 'hash', size: '3 x 1', description: 'Decimal, currency, quantity, and calculated entry.' },
  { name: 'Button', category: 'Inputs', icon: 'button', size: '2 x 1', description: 'Commands, workflow actions, and submits.' },
  { name: 'File Upload', category: 'Inputs', icon: 'file', size: '5 x 2', description: 'Documents, images, and attachment capture.' },
  { name: 'Check Box', category: 'Choice', icon: 'check', size: '2 x 1', description: 'Boolean fields and toggle options.' },
  { name: 'Radio Button', category: 'Choice', icon: 'radio', size: '3 x 1', description: 'Exclusive option selection.' },
  { name: 'Combo Box', category: 'Choice', icon: 'combo', size: '4 x 1', description: 'Lookup and enumerated value picker.' },
  { name: 'List Box', category: 'Choice', icon: 'list', size: '4 x 4', description: 'Single or multi-select list control.' },
  { name: 'Lookup', category: 'Choice', icon: 'lookup', size: '5 x 1', description: 'Foreign-key search picker with generated display fields.' },
  { name: 'Switch', category: 'Choice', icon: 'switch', size: '2 x 1', description: 'Compact on/off editor for mobile and desktop forms.' },
  { name: 'Layout', category: 'Layouts', icon: 'layout', size: '12 x 4', description: 'Responsive container with spacing rules.' },
  { name: 'Scroll Box', category: 'Layouts', icon: 'scroll', size: '12 x 6', description: 'Scrollable region for long forms and nested panels.' },
  { name: 'Flow Layout', category: 'Layouts', icon: 'flow', size: '12 x 4', description: 'Wrap-aware component flow for adaptive screens.' },
  { name: 'Grid Layout', category: 'Layouts', icon: 'grid', size: '12 x 6', description: 'Column and row layout with snap alignment.' },
  { name: 'Vertical Stack', category: 'Layouts', icon: 'vstack', size: '6 x 8', description: 'Top-to-bottom field group with shared spacing.' },
  { name: 'Horizontal Stack', category: 'Layouts', icon: 'hstack', size: '8 x 2', description: 'Left-to-right command or field grouping.' },
  { name: 'Panel', category: 'Layouts', icon: 'panel', size: '12 x 3', description: 'Grouped visual region for related fields.' },
  { name: 'Tab Control', category: 'Layouts', icon: 'tabs', size: '12 x 6', description: 'Tabbed pages for complex master records.' },
  { name: 'Data Grid', category: 'Data', icon: 'dataGrid', size: '12 x 6', description: 'Editable tabular data with sort and filter.' },
  { name: 'String Grid', category: 'Data', icon: 'table', size: '12 x 6', description: 'Spreadsheet-like matrix for structured values.' },
  { name: 'List View', category: 'Data', icon: 'listView', size: '6 x 6', description: 'Virtualized record list with icons and actions.' },
  { name: 'Tree View', category: 'Data', icon: 'treeView', size: '4 x 6', description: 'Hierarchical navigation and master records.' },
  { name: 'Chart', category: 'Data', icon: 'chart', size: '8 x 5', description: 'Operational metrics and dashboard visuals.' },
  { name: 'Database Source', category: 'Data', icon: 'database', size: '3 x 1', description: 'Dataset, query, and binding source.' },
  { name: 'Query', category: 'Data', icon: 'query', size: '4 x 1', description: 'Read model, filter, and parameterized SQL contract.' },
  { name: 'Client Dataset', category: 'Data', icon: 'dataset', size: '4 x 1', description: 'Offline-capable dataset with local change tracking.' },
  { name: 'Service Proxy', category: 'Data', icon: 'service', size: '4 x 1', description: 'Generated API client and retry policy surface.' },
  { name: 'Service Publisher', category: 'Data', icon: 'api', size: '4 x 1', description: 'Endpoint publishing surface with contract and version controls.' },
  { name: 'Failover Policy', category: 'Data', icon: 'workflow', size: '4 x 1', description: 'Primary and fallback source graph with health checks.' },
  { name: 'Replay Queue', category: 'Data', icon: 'scheduler', size: '4 x 1', description: 'Durable retry, outbox, and dead-letter replay surface.' },
  { name: 'Data Access Policy', category: 'Data', icon: 'lock', size: '4 x 1', description: 'Role, row, and field-level policy designer.' },
  { name: 'Shape', category: 'Graphics', icon: 'shape', size: '3 x 3', description: 'Generic vector primitive for diagrams and adorners.' },
  { name: 'Rectangle', category: 'Graphics', icon: 'rectangle', size: '4 x 2', description: 'Box, border, and filled visual block.' },
  { name: 'Ellipse', category: 'Graphics', icon: 'ellipse', size: '3 x 3', description: 'Circular and oval visual elements.' },
  { name: 'Line', category: 'Graphics', icon: 'line', size: '4 x 1', description: 'Connector, divider, and annotation line.' },
  { name: 'Path', category: 'Graphics', icon: 'path', size: '4 x 3', description: 'Freeform vector path with editable points.' },
  { name: 'Style Book', category: 'Graphics', icon: 'style', size: '3 x 1', description: 'Theme tokens, component states, and target styles.' },
  { name: 'Image', category: 'Media', icon: 'image', size: '4 x 3', description: 'Pictures, documents, and generated assets.' },
  { name: 'Bitmap', category: 'Media', icon: 'bitmap', size: '4 x 3', description: 'Pixel asset with density and target variants.' },
  { name: 'Camera View', category: 'Media', icon: 'camera', size: '6 x 4', description: 'Camera preview, capture, and permission workflow.' },
  { name: 'Audio Player', category: 'Media', icon: 'audio', size: '5 x 1', description: 'Audio playback with device controls.' },
  { name: 'Video Player', category: 'Media', icon: 'video', size: '8 x 5', description: 'Inline video playback for web, mobile, and desktop.' },
  { name: 'Main Menu', category: 'Navigation', icon: 'menu', size: '12 x 1', description: 'Application-level menus and shortcuts.' },
  { name: 'Popup Menu', category: 'Navigation', icon: 'popup', size: '3 x 2', description: 'Right-click and long-press contextual commands.' },
  { name: 'Toolbar', category: 'Navigation', icon: 'toolbar', size: '12 x 1', description: 'Icon command strip with overflow behavior.' },
  { name: 'Wizard', category: 'Navigation', icon: 'wizard', size: '12 x 8', description: 'Step-by-step flow generated from model state.' },
  { name: 'Breadcrumb', category: 'Navigation', icon: 'breadcrumb', size: '8 x 1', description: 'Hierarchy and drill-down location trail.' },
  { name: 'Report Viewer', category: 'Navigation', icon: 'report', size: '12 x 7', description: 'Invoices, statutory reports, and exports.' },
  { name: 'Agent', category: 'Automation', icon: 'agent', size: '3 x 2', description: 'LLM-backed task runner or assistant.' },
  { name: 'Chatbot', category: 'Automation', icon: 'bot', size: '5 x 4', description: 'Conversational UI backed by local or hosted models.' },
  { name: 'Workflow', category: 'Automation', icon: 'workflow', size: '6 x 4', description: 'Stateful approvals and process logic.' },
  { name: 'Rule Set', category: 'Automation', icon: 'rule', size: '5 x 3', description: 'Validations, routing conditions, and policy checks.' },
  { name: 'Scheduler', category: 'Automation', icon: 'scheduler', size: '4 x 2', description: 'Timed jobs, reminders, and background triggers.' },
  { name: 'Float Animation', category: 'Effects', icon: 'floatAnimation', size: '4 x 1', description: 'Numeric property tween with easing and preview scrubber.' },
  { name: 'Color Animation', category: 'Effects', icon: 'colorAnimation', size: '4 x 1', description: 'Theme and fill color transition with keyframes.' },
  { name: 'Path Animation', category: 'Effects', icon: 'pathAnimation', size: '4 x 2', description: 'Motion path animation for shapes and components.' },
  { name: 'Animation Timeline', category: 'Effects', icon: 'animation', size: '8 x 2', description: 'Reusable timeline for coordinated UI transitions.' },
  { name: 'Gesture Manager', category: 'Sensors', icon: 'gesture', size: '4 x 2', description: 'Gesture recognizer registry with conflict handling.' },
  { name: 'Tap Gesture', category: 'Sensors', icon: 'tap', size: '3 x 1', description: 'Tap, double-tap, and long-press recognizer.' },
  { name: 'Location Sensor', category: 'Sensors', icon: 'location', size: '3 x 1', description: 'GPS, geofence, and map coordinate capture.' },
  { name: 'Motion Sensor', category: 'Sensors', icon: 'motion', size: '3 x 1', description: 'Accelerometer and movement stream binding.' },
  { name: 'Orientation Sensor', category: 'Sensors', icon: 'orientation', size: '3 x 1', description: 'Device rotation and heading changes.' },
  { name: '3D Viewport', category: '3D', icon: 'viewport3d', size: '12 x 8', description: 'Scene viewport with camera, lighting, and transforms.' },
  { name: '3D Camera', category: '3D', icon: 'camera3d', size: '3 x 2', description: 'Perspective or orthographic camera control.' },
  { name: '3D Light', category: '3D', icon: 'light3d', size: '3 x 2', description: 'Directional, point, or ambient scene light.' },
  { name: '3D Mesh', category: '3D', icon: 'mesh3d', size: '4 x 4', description: 'Mesh primitive or imported model with material binding.' },
  { name: '3D Anchor', category: '3D', icon: 'cube3d', size: '3 x 3', description: 'Invisible transform node for grouping scene objects.' },
  { name: 'Biometrics', category: 'Device', icon: 'lock', size: '3 x 1', description: 'Face, fingerprint, and platform authentication.' },
  { name: 'Push Notification', category: 'Device', icon: 'bell', size: '4 x 1', description: 'User notification channel and permission contract.' },
  { name: 'Microphone', category: 'Device', icon: 'microphone', size: '3 x 1', description: 'Voice capture, recording, and consent-aware audio input.' },
  { name: 'Bluetooth', category: 'Device', icon: 'bluetooth', size: '3 x 1', description: 'Peripheral discovery, pairing, and device data exchange.' },
  { name: 'NFC', category: 'Device', icon: 'nfc', size: '3 x 1', description: 'Near-field tag reads, writes, and tap-to-identify workflows.' },
  { name: 'Secure Storage', category: 'Device', icon: 'lock', size: '4 x 1', description: 'Encrypted secrets, tokens, and offline credentials.' },
  { name: 'File Storage', category: 'Device', icon: 'storage', size: '4 x 1', description: 'Local files, sandbox documents, and sync-ready cache data.' },
  { name: 'Background Sync', category: 'Device', icon: 'scheduler', size: '4 x 1', description: 'Deferred uploads, retries, and offline replay tasks.' },
  { name: 'Network State', category: 'Device', icon: 'api', size: '3 x 1', description: 'Connectivity detection with online, offline, and metered states.' },
  { name: 'Share Sheet', category: 'Device', icon: 'upload', size: '3 x 1', description: 'Platform sharing and document handoff workflows.' },
  { name: 'API Service', category: 'Targets', icon: 'api', size: 'target', description: 'Generated service endpoint and integration boundary.' },
  { name: 'Web App', category: 'Targets', icon: 'web', size: 'target', description: 'Generated responsive browser application.' },
  { name: 'Mobile App', category: 'Targets', icon: 'mobile', size: 'target', description: 'Generated phone and tablet application.' },
  { name: 'Desktop App', category: 'Targets', icon: 'desktop', size: 'target', description: 'Generated installable desktop shell.' },
]

export const paletteCategories = Array.from(new Set(paletteComponents.map((component) => component.category)))

const specificIconExpectations: Record<string, IconName> = {
  'Data Grid': 'dataGrid',
  'File Upload': 'file',
  Bluetooth: 'bluetooth',
  'List View': 'listView',
  Microphone: 'microphone',
  NFC: 'nfc',
  'File Storage': 'storage',
  'Tree View': 'treeView',
}

export function componentIconAudit() {
  const registeredIcons = new Set(iconNames)
  const missingIcons = paletteComponents.filter((component) => !registeredIcons.has(component.icon))
  const genericIconMismatches = paletteComponents.filter((component) => {
    const expectedIcon = specificIconExpectations[component.name]
    return expectedIcon !== undefined && component.icon !== expectedIcon
  })
  const categoryCoverage = paletteCategories.map((category) => {
    const components = paletteComponents.filter((component) => component.category === category)
    return {
      category,
      count: components.length,
      icons: Array.from(new Set(components.map((component) => component.icon))),
    }
  })

  return {
    ok:
      missingIcons.length === 0 &&
      genericIconMismatches.length === 0 &&
      categoryCoverage.every((item) => item.count > 0 && item.icons.length > 0),
    totalComponents: paletteComponents.length,
    totalIcons: iconNames.length,
    missingIcons,
    genericIconMismatches,
    categoryCoverage,
  }
}
