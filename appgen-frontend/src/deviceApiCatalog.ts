import { iconNames } from './Icon'
import type { IconName } from './Icon'

export type DeviceApiGroup =
  | 'Sensors'
  | 'Media'
  | 'Permissions'
  | 'Connectivity'
  | 'Storage'
  | 'Notifications'
  | 'Background'
  | 'Security'

export type DeviceTargetAdapter = 'web' | 'mobile' | 'desktop'

export type DeviceApiCapability = {
  name: string
  group: DeviceApiGroup
  icon: IconName
  permission: string
  adapters: DeviceTargetAdapter[]
  privacy: string
  fallback: string
}

export const deviceApiCapabilities: DeviceApiCapability[] = [
  {
    name: 'Location',
    group: 'Sensors',
    icon: 'location',
    permission: 'Foreground and optional background location',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'Purpose text, retention policy, and precision controls',
    fallback: 'Manual address or coordinate entry',
  },
  {
    name: 'Motion',
    group: 'Sensors',
    icon: 'motion',
    permission: 'Device motion stream',
    adapters: ['web', 'mobile'],
    privacy: 'Sampling rate limits and explicit sensor enablement',
    fallback: 'Manual state update or last-known movement value',
  },
  {
    name: 'Orientation',
    group: 'Sensors',
    icon: 'orientation',
    permission: 'Device orientation stream',
    adapters: ['web', 'mobile'],
    privacy: 'Session-scoped access with live indicator',
    fallback: 'Static layout orientation setting',
  },
  {
    name: 'Camera',
    group: 'Media',
    icon: 'camera',
    permission: 'Camera capture',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'Capture-only access with preview confirmation',
    fallback: 'File upload from gallery or disk',
  },
  {
    name: 'Microphone',
    group: 'Media',
    icon: 'microphone',
    permission: 'Audio capture',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'Recording indicator, duration limit, and transcript opt-in',
    fallback: 'Typed note or uploaded audio file',
  },
  {
    name: 'Push Notifications',
    group: 'Notifications',
    icon: 'bell',
    permission: 'Notification opt-in and channel selection',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'User-visible categories and quiet-hours policy',
    fallback: 'In-app inbox notification',
  },
  {
    name: 'Biometrics',
    group: 'Security',
    icon: 'lock',
    permission: 'Platform authentication prompt',
    adapters: ['mobile', 'desktop'],
    privacy: 'No biometric material leaves the operating system',
    fallback: 'Password, PIN, or one-time code challenge',
  },
  {
    name: 'Bluetooth',
    group: 'Connectivity',
    icon: 'bluetooth',
    permission: 'Nearby device discovery and pairing',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'Scoped device selection and pairing history controls',
    fallback: 'USB import or manual device identifier entry',
  },
  {
    name: 'NFC',
    group: 'Connectivity',
    icon: 'nfc',
    permission: 'Near-field tag session',
    adapters: ['web', 'mobile'],
    privacy: 'One-shot scan sessions with visible confirmation',
    fallback: 'Barcode, QR code, or manual token entry',
  },
  {
    name: 'Network State',
    group: 'Connectivity',
    icon: 'api',
    permission: 'Connectivity observation',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'No packet payload inspection',
    fallback: 'Retry queue with user-controlled refresh',
  },
  {
    name: 'Secure Storage',
    group: 'Storage',
    icon: 'lock',
    permission: 'Keychain or encrypted vault access',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'Encrypted at rest with scoped secret names',
    fallback: 'Server-side session token refresh',
  },
  {
    name: 'File Storage',
    group: 'Storage',
    icon: 'storage',
    permission: 'Sandbox file and document access',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'User-selected files and retention controls',
    fallback: 'Remote object storage attachment',
  },
  {
    name: 'Background Sync',
    group: 'Background',
    icon: 'scheduler',
    permission: 'Background task and retry schedule',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'Bounded retries with visible sync history',
    fallback: 'Foreground sync on app open',
  },
  {
    name: 'Share Sheet',
    group: 'Permissions',
    icon: 'upload',
    permission: 'User-initiated share action',
    adapters: ['web', 'mobile', 'desktop'],
    privacy: 'No data leaves the app without explicit user action',
    fallback: 'Download, copy link, or export file',
  },
]

const requiredGroups: DeviceApiGroup[] = [
  'Sensors',
  'Media',
  'Permissions',
  'Connectivity',
  'Storage',
  'Notifications',
  'Background',
  'Security',
]

export function deviceApiAudit() {
  const registeredIcons = new Set(iconNames)
  const missingIcons = deviceApiCapabilities.filter((capability) => !registeredIcons.has(capability.icon))
  const missingGroups = requiredGroups.filter(
    (group) => !deviceApiCapabilities.some((capability) => capability.group === group),
  )
  const incompleteCapabilities = deviceApiCapabilities.filter(
    (capability) =>
      capability.permission.length === 0 ||
      capability.adapters.length === 0 ||
      capability.privacy.length === 0 ||
      capability.fallback.length === 0,
  )
  const targetCoverage = {
    web: deviceApiCapabilities.filter((capability) => capability.adapters.includes('web')).length,
    mobile: deviceApiCapabilities.filter((capability) => capability.adapters.includes('mobile')).length,
    desktop: deviceApiCapabilities.filter((capability) => capability.adapters.includes('desktop')).length,
  }

  return {
    ok:
      missingIcons.length === 0 &&
      missingGroups.length === 0 &&
      incompleteCapabilities.length === 0 &&
      targetCoverage.mobile > 0 &&
      targetCoverage.web > 0 &&
      targetCoverage.desktop > 0,
    totalCapabilities: deviceApiCapabilities.length,
    missingIcons,
    missingGroups,
    incompleteCapabilities,
    targetCoverage,
  }
}
