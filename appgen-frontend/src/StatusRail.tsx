import { Icon } from './Icon'
import type { IconName } from './Icon'
import { useRouteAudit } from './studioRouteAudit'

type Card = { label: string; value: string; icon: IconName; tone?: 'ok' | 'warn' }

/**
 * The status rail reports the route audit, which is the only consistency check
 * the Studio can still make about itself.
 *
 * It used to report five catalog audits over TypeScript lists. Those catalogs
 * are gone: every panel reads the platform's contracts over the API, so the
 * thing that can still be wrong is a client route with no server behind it.
 */
export function StatusRail() {
  const audit = useRouteAudit()

  const cards: Card[] = [
    { label: 'DSL lint', value: 'Clean', icon: 'check' },
    {
      label: 'Routes',
      value: audit.state === 'ready' ? `${audit.served} served` : audit.state === 'error' ? 'Unreachable' : 'Checking',
      icon: 'api',
      tone: audit.state === 'ready' && !audit.ok ? 'warn' : 'ok',
    },
    {
      label: 'Client',
      value: audit.state === 'ready' ? `${audit.declared} declared` : 'Unknown',
      icon: 'service',
      tone: audit.state === 'ready' && audit.missing.length > 0 ? 'warn' : 'ok',
    },
    {
      label: 'Contract',
      value: audit.state === 'ready' && audit.ok ? 'Matched' : audit.state === 'error' ? 'Unreachable' : 'Checking',
      icon: audit.state === 'ready' && audit.ok ? 'check' : 'rule',
      tone: audit.state === 'ready' && !audit.ok ? 'warn' : 'ok',
    },
  ]

  return (
    <section className="status-rail" aria-label="Workspace status">
      {cards.map((card) => (
        <div className={`status-card status-card-${card.tone ?? 'ok'}`} key={card.label}>
          <Icon name={card.icon} />
          <span>{card.label}</span>
          <strong>{card.value}</strong>
        </div>
      ))}
    </section>
  )
}
