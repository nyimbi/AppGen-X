import type { SVGProps } from 'react'

export type IconName =
  | 'agent'
  | 'button'
  | 'calendar'
  | 'chart'
  | 'check'
  | 'combo'
  | 'data'
  | 'database'
  | 'desktop'
  | 'form'
  | 'grid'
  | 'image'
  | 'input'
  | 'label'
  | 'layout'
  | 'list'
  | 'menu'
  | 'mobile'
  | 'panel'
  | 'radio'
  | 'report'
  | 'search'
  | 'tree'
  | 'web'
  | 'workflow'

const paths: Record<IconName, JSX.Element> = {
  agent: (
    <>
      <path d="M12 4v3" />
      <rect x="5" y="7" width="14" height="11" rx="3" />
      <path d="M8 12h.01M16 12h.01M9 16h6" />
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
  combo: (
    <>
      <rect x="5" y="6" width="14" height="12" rx="2" />
      <path d="M8 10h8M15 14l2 2 2-2" />
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
  desktop: (
    <>
      <rect x="4" y="5" width="16" height="12" rx="2" />
      <path d="M9 21h6M12 17v4" />
    </>
  ),
  form: (
    <>
      <rect x="5" y="4" width="14" height="16" rx="2" />
      <path d="M8 8h8M8 12h8M8 16h5" />
    </>
  ),
  grid: (
    <>
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <path d="M4 10h16M4 15h16M10 4v16M15 4v16" />
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
  list: (
    <>
      <path d="M8 7h12M8 12h12M8 17h12" />
      <path d="M4 7h.01M4 12h.01M4 17h.01" />
    </>
  ),
  menu: (
    <>
      <path d="M5 7h14M5 12h14M5 17h14" />
    </>
  ),
  mobile: (
    <>
      <rect x="7" y="3" width="10" height="18" rx="2" />
      <path d="M11 18h2" />
    </>
  ),
  panel: (
    <>
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="M4 10h16" />
    </>
  ),
  radio: (
    <>
      <circle cx="12" cy="12" r="7" />
      <circle cx="12" cy="12" r="3" />
    </>
  ),
  report: (
    <>
      <path d="M7 3h7l4 4v14H7z" />
      <path d="M14 3v5h4M10 13h5M10 17h5" />
    </>
  ),
  search: (
    <>
      <circle cx="11" cy="11" r="6" />
      <path d="m16 16 4 4" />
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
}

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
