import type { IconName } from './Icon'

/**
 * The Studio's sections, one entry per panel that actually exists.
 *
 * The nav used to list Forms, Database, Agents, Reports, Packages, and Targets,
 * two of which had no panel behind them. A nav item with nothing to route to is
 * the same defect as a declared-but-unmounted workbench route, so the list is
 * the panels.
 */
export type StudioSection = {
  id: string
  label: string
  icon: IconName
}

export const studioSections: readonly StudioSection[] = [
  { id: 'overview', label: 'Overview', icon: 'layout' },
  { id: 'forms', label: 'Forms', icon: 'form' },
  { id: 'database', label: 'Database', icon: 'database' },
  { id: 'packages', label: 'Packages', icon: 'package' },
  { id: 'targets', label: 'Targets', icon: 'mobile' },
]

/** Read the section from a hash like `#packages`, falling back to the first. */
export function readSection(hash = typeof window === 'undefined' ? '' : window.location.hash): string {
  const id = hash.replace(/^#/, '')
  return studioSections.some((section) => section.id === id) ? id : studioSections[0].id
}
