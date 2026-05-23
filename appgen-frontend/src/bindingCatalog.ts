import { iconNames } from './Icon'
import type { IconName } from './Icon'

export type BindingState = 'valid' | 'warning' | 'review'

export type VisualBinding = {
  source: string
  target: string
  expression: string
  icon: IconName
  state: BindingState
}

export const visualBindings: VisualBinding[] = [
  {
    source: 'Invoice.customer.name',
    target: 'Customer Name.Text',
    expression: 'formatCustomerName(customer)',
    icon: 'input',
    state: 'valid',
  },
  {
    source: 'Invoice.account.id',
    target: 'Account Lookup.Value',
    expression: 'lookup(accounts, account_id)',
    icon: 'lookup',
    state: 'valid',
  },
  {
    source: 'Invoice.lines',
    target: 'Line Items.Rows',
    expression: 'lineItems.withTotals()',
    icon: 'dataGrid',
    state: 'valid',
  },
  {
    source: 'Invoice.totals',
    target: 'Totals Chart.Series',
    expression: 'totals.toSeries(currency)',
    icon: 'chart',
    state: 'warning',
  },
  {
    source: 'Approval.status',
    target: 'Approval Agent.Context',
    expression: 'agentContext(status, route)',
    icon: 'agent',
    state: 'review',
  },
]

export function visualBindingAudit() {
  const registeredIcons = new Set(iconNames)
  const requiredStates: BindingState[] = ['valid', 'warning', 'review']
  const missingIcons = visualBindings.filter((binding) => !registeredIcons.has(binding.icon))
  const missingEndpoints = visualBindings.filter(
    (binding) => binding.source.trim() === '' || binding.target.trim() === '' || binding.expression.trim() === '',
  )
  const stateCoverage = requiredStates.map((state) => ({
    state,
    count: visualBindings.filter((binding) => binding.state === state).length,
  }))

  return {
    ok:
      missingIcons.length === 0 &&
      missingEndpoints.length === 0 &&
      stateCoverage.every((item) => item.count > 0),
    totalBindings: visualBindings.length,
    missingIcons,
    missingEndpoints,
    stateCoverage,
  }
}
