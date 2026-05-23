import type { SVGProps } from 'react'

export type IconName =
  | 'agent'
  | 'animation'
  | 'api'
  | 'audio'
  | 'bell'
  | 'bitmap'
  | 'bot'
  | 'breadcrumb'
  | 'button'
  | 'calendar'
  | 'camera'
  | 'camera3d'
  | 'chart'
  | 'check'
  | 'colorAnimation'
  | 'combo'
  | 'cube3d'
  | 'dataset'
  | 'data'
  | 'database'
  | 'desktop'
  | 'drag'
  | 'ellipse'
  | 'form'
  | 'flow'
  | 'floatAnimation'
  | 'gesture'
  | 'grid'
  | 'hash'
  | 'hstack'
  | 'image'
  | 'input'
  | 'label'
  | 'layout'
  | 'line'
  | 'list'
  | 'light3d'
  | 'location'
  | 'lock'
  | 'lookup'
  | 'menu'
  | 'mesh3d'
  | 'mobile'
  | 'motion'
  | 'orientation'
  | 'panel'
  | 'path'
  | 'pathAnimation'
  | 'popup'
  | 'query'
  | 'radio'
  | 'rectangle'
  | 'report'
  | 'rule'
  | 'scheduler'
  | 'search'
  | 'service'
  | 'shape'
  | 'scroll'
  | 'style'
  | 'switch'
  | 'table'
  | 'tabs'
  | 'tap'
  | 'textarea'
  | 'toolbar'
  | 'tree'
  | 'upload'
  | 'video'
  | 'viewport3d'
  | 'vstack'
  | 'web'
  | 'workflow'
  | 'wizard'

const paths: Record<IconName, JSX.Element> = {
  agent: (
    <>
      <path d="M12 4v3" />
      <rect x="5" y="7" width="14" height="11" rx="3" />
      <path d="M8 12h.01M16 12h.01M9 16h6" />
    </>
  ),
  animation: (
    <>
      <path d="M5 16c2.5-8 6.5 8 9-2 1-4 3-5 5-5" />
      <path d="M5 20h14" />
      <circle cx="5" cy="16" r="2" />
      <circle cx="19" cy="9" r="2" />
    </>
  ),
  api: (
    <>
      <path d="M7 8 3 12l4 4" />
      <path d="m17 8 4 4-4 4" />
      <path d="m14 5-4 14" />
    </>
  ),
  audio: (
    <>
      <path d="M5 10v4h4l5 4V6l-5 4z" />
      <path d="M17 9c1.2 1.5 1.2 4.5 0 6" />
    </>
  ),
  bell: (
    <>
      <path d="M6 10a6 6 0 0 1 12 0v4l2 3H4l2-3z" />
      <path d="M10 20h4" />
    </>
  ),
  bitmap: (
    <>
      <rect x="5" y="5" width="14" height="14" rx="2" />
      <path d="M9 5v14M15 5v14M5 9h14M5 15h14" />
    </>
  ),
  bot: (
    <>
      <rect x="4" y="8" width="16" height="10" rx="3" />
      <path d="M12 4v4M8 13h.01M16 13h.01M9 18v2M15 18v2" />
    </>
  ),
  breadcrumb: (
    <>
      <path d="M4 12h5" />
      <path d="m9 8 4 4-4 4" />
      <path d="M14 12h6" />
    </>
  ),
  button: (
    <>
      <rect x="5" y="8" width="14" height="8" rx="4" />
      <path d="M9 12h6" />
    </>
  ),
  calendar: (
    <>
      <rect x="4" y="5" width="16" height="15" rx="2" />
      <path d="M8 3v4M16 3v4M4 10h16" />
    </>
  ),
  camera: (
    <>
      <path d="M5 8h3l2-3h4l2 3h3v11H5z" />
      <circle cx="12" cy="13" r="3" />
    </>
  ),
  camera3d: (
    <>
      <path d="M6 8h7l3 3v6H6z" />
      <path d="m16 12 4-3v10l-4-3" />
      <path d="M8 20h8M12 17v3" />
    </>
  ),
  chart: (
    <>
      <path d="M5 19V5" />
      <path d="M5 19h15" />
      <path d="M9 15v-4M13 15V8M17 15v-7" />
    </>
  ),
  check: (
    <>
      <rect x="5" y="5" width="14" height="14" rx="3" />
      <path d="m8.5 12 2.5 2.5 4.5-5" />
    </>
  ),
  colorAnimation: (
    <>
      <path d="M12 4s6 6.2 6 10a6 6 0 0 1-12 0c0-3.8 6-10 6-10z" />
      <path d="M6 17c3 1.5 9 1.5 12 0" />
      <circle cx="17" cy="6" r="2" />
    </>
  ),
  combo: (
    <>
      <rect x="5" y="6" width="14" height="12" rx="2" />
      <path d="M8 10h8M15 14l2 2 2-2" />
    </>
  ),
  dataset: (
    <>
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="M4 10h16M9 5v14M14 5v14" />
      <path d="M7 13h2M12 16h2" />
    </>
  ),
  data: (
    <>
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="M4 10h16M9 5v14" />
    </>
  ),
  database: (
    <>
      <ellipse cx="12" cy="6" rx="7" ry="3" />
      <path d="M5 6v8c0 1.7 3.1 3 7 3s7-1.3 7-3V6" />
      <path d="M5 10c0 1.7 3.1 3 7 3s7-1.3 7-3" />
    </>
  ),
  cube3d: (
    <>
      <path d="m12 3 8 4.5v9L12 21l-8-4.5v-9z" />
      <path d="M12 12 4 7.5M12 12l8-4.5M12 12v9" />
    </>
  ),
  desktop: (
    <>
      <rect x="4" y="5" width="16" height="12" rx="2" />
      <path d="M9 21h6M12 17v4" />
    </>
  ),
  drag: (
    <>
      <path d="M8 6h.01M12 6h.01M16 6h.01" />
      <path d="M8 12h.01M12 12h.01M16 12h.01" />
      <path d="M8 18h.01M12 18h.01M16 18h.01" />
    </>
  ),
  ellipse: (
    <>
      <ellipse cx="12" cy="12" rx="8" ry="5" />
    </>
  ),
  form: (
    <>
      <rect x="5" y="4" width="14" height="16" rx="2" />
      <path d="M8 8h8M8 12h8M8 16h5" />
    </>
  ),
  flow: (
    <>
      <rect x="4" y="5" width="6" height="4" rx="1" />
      <rect x="14" y="5" width="6" height="4" rx="1" />
      <rect x="9" y="15" width="6" height="4" rx="1" />
      <path d="M10 7h4M17 9v3l-5 3M7 9v3l5 3" />
    </>
  ),
  floatAnimation: (
    <>
      <path d="M6 18V6" />
      <path d="m3 9 3-3 3 3" />
      <path d="m3 15 3 3 3-3" />
      <path d="M13 7h6M13 12h4M13 17h6" />
    </>
  ),
  gesture: (
    <>
      <path d="M7 12V8a2 2 0 0 1 4 0v4" />
      <path d="M11 12V6a2 2 0 0 1 4 0v6" />
      <path d="M15 13v-3a2 2 0 0 1 4 0v5c0 4-3 6-6 6h-1c-3 0-6-3-6-6v-2" />
    </>
  ),
  grid: (
    <>
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <path d="M4 10h16M4 15h16M10 4v16M15 4v16" />
    </>
  ),
  hash: (
    <>
      <path d="M9 4 7 20M17 4l-2 16M4 9h16M3 15h16" />
    </>
  ),
  hstack: (
    <>
      <rect x="4" y="6" width="4" height="12" rx="1" />
      <rect x="10" y="6" width="4" height="12" rx="1" />
      <rect x="16" y="6" width="4" height="12" rx="1" />
    </>
  ),
  image: (
    <>
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="m7 16 4-4 3 3 2-2 3 3" />
      <circle cx="9" cy="9" r="1" />
    </>
  ),
  input: (
    <>
      <rect x="4" y="7" width="16" height="10" rx="2" />
      <path d="M8 12h8" />
    </>
  ),
  label: (
    <>
      <path d="M5 7h14" />
      <path d="M9 7v10" />
      <path d="M15 7v10" />
    </>
  ),
  layout: (
    <>
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <path d="M4 10h16M10 10v10" />
    </>
  ),
  line: (
    <>
      <path d="M5 19 19 5" />
      <circle cx="5" cy="19" r="1.5" />
      <circle cx="19" cy="5" r="1.5" />
    </>
  ),
  list: (
    <>
      <path d="M8 7h12M8 12h12M8 17h12" />
      <path d="M4 7h.01M4 12h.01M4 17h.01" />
    </>
  ),
  light3d: (
    <>
      <circle cx="12" cy="10" r="4" />
      <path d="M12 2v3M12 15v3M4 10H2M22 10h-2M6.3 4.3 8 6M16 14l1.7 1.7M17.7 4.3 16 6M8 14l-1.7 1.7" />
      <path d="M9 21h6" />
    </>
  ),
  location: (
    <>
      <path d="M12 21s7-6 7-12a7 7 0 0 0-14 0c0 6 7 12 7 12z" />
      <circle cx="12" cy="9" r="2" />
    </>
  ),
  lock: (
    <>
      <rect x="5" y="10" width="14" height="10" rx="2" />
      <path d="M8 10V7a4 4 0 0 1 8 0v3" />
    </>
  ),
  lookup: (
    <>
      <rect x="4" y="5" width="11" height="11" rx="2" />
      <path d="M7 9h5M7 12h3" />
      <circle cx="17" cy="17" r="3" />
      <path d="m19 19 2 2" />
    </>
  ),
  menu: (
    <>
      <path d="M5 7h14M5 12h14M5 17h14" />
    </>
  ),
  mesh3d: (
    <>
      <path d="M4 17 8 5h8l4 12-8 4z" />
      <path d="M8 5 12 21M16 5l-4 16M4 17h16M6 11h12" />
    </>
  ),
  mobile: (
    <>
      <rect x="7" y="3" width="10" height="18" rx="2" />
      <path d="M11 18h2" />
    </>
  ),
  motion: (
    <>
      <path d="M4 12h4l2-5 4 10 2-5h4" />
      <path d="M6 18c2 2 10 2 12 0" />
    </>
  ),
  orientation: (
    <>
      <rect x="8" y="3" width="8" height="14" rx="2" />
      <path d="M5 17c2 3 12 3 14 0M12 14h.01" />
    </>
  ),
  panel: (
    <>
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="M4 10h16" />
    </>
  ),
  path: (
    <>
      <path d="M5 18c5-13 9 13 14-1" />
      <circle cx="5" cy="18" r="2" />
      <circle cx="19" cy="17" r="2" />
    </>
  ),
  pathAnimation: (
    <>
      <path d="M5 18c5-13 9 13 14-1" />
      <path d="M8 8h8" />
      <path d="m13 5 3 3-3 3" />
      <circle cx="5" cy="18" r="2" />
      <circle cx="19" cy="17" r="2" />
    </>
  ),
  popup: (
    <>
      <rect x="5" y="5" width="10" height="8" rx="2" />
      <rect x="9" y="11" width="10" height="8" rx="2" />
      <path d="M12 15h4" />
    </>
  ),
  query: (
    <>
      <path d="M5 7h14M7 12h10M9 17h6" />
      <path d="M17 7l2 2-2 2" />
    </>
  ),
  radio: (
    <>
      <circle cx="12" cy="12" r="7" />
      <circle cx="12" cy="12" r="3" />
    </>
  ),
  rectangle: (
    <>
      <rect x="4" y="7" width="16" height="10" rx="1" />
    </>
  ),
  report: (
    <>
      <path d="M7 3h7l4 4v14H7z" />
      <path d="M14 3v5h4M10 13h5M10 17h5" />
    </>
  ),
  rule: (
    <>
      <path d="M5 6h14M5 12h9M5 18h14" />
      <path d="m16 10 2 2 3-4" />
    </>
  ),
  scheduler: (
    <>
      <rect x="4" y="5" width="16" height="15" rx="2" />
      <path d="M8 3v4M16 3v4M4 10h16" />
      <path d="M12 14v3l2 1" />
    </>
  ),
  search: (
    <>
      <circle cx="11" cy="11" r="6" />
      <path d="m16 16 4 4" />
    </>
  ),
  service: (
    <>
      <rect x="4" y="5" width="16" height="5" rx="1" />
      <rect x="4" y="14" width="16" height="5" rx="1" />
      <path d="M8 8h.01M8 17h.01M12 10v4" />
    </>
  ),
  shape: (
    <>
      <path d="M12 4 20 9v6l-8 5-8-5V9z" />
    </>
  ),
  scroll: (
    <>
      <rect x="5" y="4" width="14" height="16" rx="2" />
      <path d="M16 7v10M16 14l2 2 2-2" />
      <path d="M8 8h5M8 12h4M8 16h5" />
    </>
  ),
  style: (
    <>
      <path d="M5 19h14" />
      <path d="M7 15 12 4l5 11" />
      <path d="M9 11h6" />
    </>
  ),
  switch: (
    <>
      <rect x="4" y="8" width="16" height="8" rx="4" />
      <circle cx="9" cy="12" r="3" />
    </>
  ),
  table: (
    <>
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="M4 10h16M4 15h16M10 5v14" />
    </>
  ),
  tabs: (
    <>
      <path d="M5 8h5l2 3h7v8H5z" />
      <path d="M5 8V5h5l2 3" />
    </>
  ),
  tap: (
    <>
      <circle cx="12" cy="8" r="3" />
      <path d="M12 11v5" />
      <path d="M8 16h8l-1.5 5h-5z" />
      <path d="M4 8a8 8 0 0 1 16 0" />
    </>
  ),
  textarea: (
    <>
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="M8 9h8M8 13h8M8 17h5" />
    </>
  ),
  toolbar: (
    <>
      <rect x="4" y="6" width="16" height="12" rx="2" />
      <path d="M4 10h16M8 14h.01M12 14h.01M16 14h.01" />
    </>
  ),
  tree: (
    <>
      <path d="M12 5v14M12 9H7v4M12 13h5v4" />
      <circle cx="12" cy="5" r="2" />
      <circle cx="7" cy="15" r="2" />
      <circle cx="17" cy="19" r="2" />
    </>
  ),
  upload: (
    <>
      <path d="M12 16V4" />
      <path d="m8 8 4-4 4 4" />
      <path d="M5 16v4h14v-4" />
    </>
  ),
  video: (
    <>
      <rect x="4" y="6" width="11" height="12" rx="2" />
      <path d="m15 10 5-3v10l-5-3z" />
    </>
  ),
  viewport3d: (
    <>
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="m12 8 5 3v5l-5 3-5-3v-5z" />
      <path d="M12 8v5l5 3M12 13l-5 3" />
    </>
  ),
  vstack: (
    <>
      <rect x="6" y="4" width="12" height="4" rx="1" />
      <rect x="6" y="10" width="12" height="4" rx="1" />
      <rect x="6" y="16" width="12" height="4" rx="1" />
    </>
  ),
  web: (
    <>
      <circle cx="12" cy="12" r="8" />
      <path d="M4 12h16M12 4c2 2.2 3 4.9 3 8s-1 5.8-3 8M12 4c-2 2.2-3 4.9-3 8s1 5.8 3 8" />
    </>
  ),
  workflow: (
    <>
      <circle cx="6" cy="6" r="2" />
      <circle cx="18" cy="6" r="2" />
      <circle cx="12" cy="18" r="2" />
      <path d="M8 7h8M7 8l4 8M17 8l-4 8" />
    </>
  ),
  wizard: (
    <>
      <path d="M4 7h16M4 12h12M4 17h8" />
      <path d="m16 15 2 2 3-5" />
    </>
  ),
}

export const iconNames = Object.keys(paths) as IconName[]

type IconProps = SVGProps<SVGSVGElement> & {
  name: IconName
}

export function Icon({ name, ...props }: IconProps) {
  return (
    <svg
      aria-hidden="true"
      fill="none"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="1.8"
      viewBox="0 0 24 24"
      {...props}
    >
      {paths[name]}
    </svg>
  )
}
