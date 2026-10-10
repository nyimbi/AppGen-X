import type { IconName } from './Icon'

/**
 * The palette's icons arrive from the Python contract as Font Awesome classes,
 * because the generator's other consumers (the desktop IDE palettes, the
 * generated cockpit templates) render FA. The Studio draws inline SVG, so each
 * class maps to the nearest name in `Icon.tsx`.
 *
 * The map is explicit rather than derived: `fa-table` and `fa-th` are both
 * grid-like, and which SVG stands in for which is a design decision, not a
 * string transform. `iconForClass` falls back to `puzzle` so a component the
 * generator adds before the map catches up still renders a tile.
 */
const ICON_BY_CLASS: Record<string, IconName> = {
  'fa-address-book-o': 'lookup',
  'fa-align-left': 'textarea',
  'fa-arrows-h': 'floatAnimation',
  'fa-arrows-v': 'scroll',
  'fa-bar-chart': 'chart',
  'fa-bars': 'menu',
  'fa-bell': 'bell',
  'fa-bluetooth-b': 'bluetooth',
  'fa-bolt': 'rule',
  'fa-book': 'style',
  'fa-calendar': 'calendar',
  'fa-calendar-check-o': 'calendar',
  'fa-camera': 'camera',
  'fa-check-square-o': 'check',
  'fa-circle-o': 'ellipse',
  'fa-clock-o': 'scheduler',
  'fa-cloud': 'api',
  'fa-code-fork': 'path',
  'fa-columns': 'tabs',
  'fa-compass': 'motion',
  'fa-crosshairs': 'cube3d',
  'fa-cube': 'viewport3d',
  'fa-cubes': 'mesh3d',
  'fa-database': 'database',
  'fa-desktop': 'desktop',
  'fa-dot-circle-o': 'radio',
  'fa-ellipsis-h': 'hstack',
  'fa-envelope-o': 'input',
  'fa-exchange': 'flow',
  'fa-file-text-o': 'report',
  'fa-folder-open': 'storage',
  'fa-font': 'label',
  'fa-globe': 'web',
  'fa-hand-paper-o': 'gesture',
  'fa-hand-pointer-o': 'button',
  'fa-image': 'image',
  'fa-keyboard-o': 'input',
  'fa-lightbulb-o': 'light3d',
  'fa-link': 'lookup',
  'fa-list': 'combo',
  'fa-list-alt': 'listView',
  'fa-location-arrow': 'location',
  'fa-lock': 'lock',
  'fa-magic': 'animation',
  'fa-minus': 'line',
  'fa-mobile': 'mobile',
  'fa-mouse-pointer': 'popup',
  'fa-object-group': 'panel',
  'fa-paint-brush': 'style',
  'fa-paper-plane': 'bell',
  'fa-picture-o': 'bitmap',
  'fa-play': 'animation',
  'fa-plug': 'service',
  'fa-puzzle-piece': 'shape',
  'fa-random': 'workflow',
  'fa-refresh': 'scheduler',
  'fa-road': 'pathAnimation',
  'fa-search': 'lookup',
  'fa-share-alt': 'upload',
  'fa-shield': 'lock',
  'fa-sitemap': 'treeView',
  'fa-sliders': 'style',
  'fa-square': 'rectangle',
  'fa-square-o': 'shape',
  'fa-table': 'table',
  'fa-th': 'grid',
  'fa-th-list': 'list',
  'fa-upload': 'upload',
  'fa-video-camera': 'video',
  'fa-wifi': 'nfc',
  'fa-window-maximize': 'panel',
  'fa-wrench': 'toolbar',
}

export function iconForClass(className: string): IconName {
  return ICON_BY_CLASS[className] ?? 'shape'
}
