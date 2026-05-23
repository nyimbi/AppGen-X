import { iconNames } from './Icon'
import type { IconName } from './Icon'

export type PackageState = 'installed' | 'available' | 'update'

export type DesignPackage = {
  name: string
  version: string
  vendor: string
  state: PackageState
  icon: IconName
  trust: 'signed' | 'verified'
  components: string[]
}

export const designPackages: DesignPackage[] = [
  {
    name: 'Core Controls',
    version: '1.8.0',
    vendor: 'AppGen',
    state: 'installed',
    icon: 'button',
    trust: 'signed',
    components: ['Button', 'Text Box', 'Label', 'Combo Box', 'Lookup'],
  },
  {
    name: 'Data Access Pack',
    version: '2.1.4',
    vendor: 'AppGen',
    state: 'installed',
    icon: 'database',
    trust: 'verified',
    components: ['Database Source', 'Query', 'Client Dataset', 'Service Proxy'],
  },
  {
    name: 'Device API Pack',
    version: '1.3.2',
    vendor: 'AppGen',
    state: 'available',
    icon: 'mobile',
    trust: 'signed',
    components: ['Location Sensor', 'Motion Sensor', 'Orientation Sensor', 'Camera View'],
  },
  {
    name: 'Visual Effects Pack',
    version: '1.5.1',
    vendor: 'AppGen',
    state: 'update',
    icon: 'animation',
    trust: 'verified',
    components: ['Float Animation', 'Color Animation', 'Path Animation', '3D Viewport'],
  },
]

export function packageInstallAudit() {
  const registeredIcons = new Set(iconNames)
  const requiredStates: PackageState[] = ['installed', 'available', 'update']
  const missingIcons = designPackages.filter((item) => !registeredIcons.has(item.icon))
  const emptyPackages = designPackages.filter((item) => item.components.length === 0)
  const unsignedPackages = designPackages.filter((item) => item.trust !== 'signed' && item.trust !== 'verified')
  const stateCoverage = requiredStates.map((state) => ({
    state,
    count: designPackages.filter((item) => item.state === state).length,
  }))
  const totalComponents = designPackages.reduce((count, item) => count + item.components.length, 0)

  return {
    ok:
      missingIcons.length === 0 &&
      emptyPackages.length === 0 &&
      unsignedPackages.length === 0 &&
      stateCoverage.every((item) => item.count > 0),
    totalPackages: designPackages.length,
    totalComponents,
    missingIcons,
    emptyPackages,
    unsignedPackages,
    stateCoverage,
  }
}
