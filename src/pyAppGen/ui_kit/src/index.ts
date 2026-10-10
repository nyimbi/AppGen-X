/** AppGen-X component kit.
 *
 * One React kit, consumed two ways: the Studio aliases this directory through
 * `vite.config.ts`, and the generator emits the same source into a generated
 * app. Both therefore render the same markup and read the same
 * `--appgen-*` tokens, so a component cannot mean one thing in the Studio and
 * another in a generated app.
 *
 * Every component styles itself from `tokens.css` only. No component carries a
 * literal colour, so switching theme is a token change and nothing else.
 */

export { AppShell } from './AppShell'
export type { AppShellProps } from './AppShell'

export { Badge } from './Badge'
export type { BadgeProps, BadgeTone } from './Badge'

export { Button } from './Button'
export type { ButtonProps, ButtonSize, ButtonVariant } from './Button'

export { Card } from './Card'
export type { CardProps } from './Card'

export { Dialog } from './Dialog'
export type { DialogProps } from './Dialog'

export { EmptyState } from './EmptyState'
export type { EmptyStateProps } from './EmptyState'

export { Field } from './Field'
export type { FieldProps } from './Field'

export { Input } from './Input'
export type { InputProps } from './Input'

export { NavRail } from './NavRail'
export type { NavItem, NavRailProps } from './NavRail'

export { PageHeader } from './PageHeader'
export type { PageHeaderProps } from './PageHeader'

export { Select } from './Select'
export type { SelectOption, SelectProps } from './Select'

export { Table, tableEmptyState } from './Table'
export type { TableColumn, TableProps } from './Table'

export { Tabs } from './Tabs'
export type { TabItem, TabsProps } from './Tabs'

export { ToastProvider, useToast } from './Toast'
export type { Toast, ToastApi, ToastTone } from './Toast'

export { Tooltip } from './Tooltip'
export type { TooltipProps } from './Tooltip'

export { WorkbenchLayout } from './WorkbenchLayout'
export type { WorkbenchLayoutProps } from './WorkbenchLayout'

export { cx } from './cx'
