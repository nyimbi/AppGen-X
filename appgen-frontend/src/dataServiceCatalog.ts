import { iconNames } from './Icon'
import type { IconName } from './Icon'

export type DataServiceLane = 'Source' | 'Query' | 'Publish' | 'Embedded DB' | 'Resilience' | 'Security'

export type DataServiceCapability = {
  name: string
  lane: DataServiceLane
  icon: IconName
  designSurface: string
  generationOutput: string
  runtimeContract: string
  evidence: string
}

export const dataServiceCapabilities: DataServiceCapability[] = [
  {
    name: 'Database Source Designer',
    lane: 'Source',
    icon: 'database',
    designSurface: 'Connection selector, schema browser, table picker, and relationship preview',
    generationOutput: 'Typed repository, migration seed, model binding source, and environment contract',
    runtimeContract: 'Connection pool, transaction scope, and read/write role separation',
    evidence: 'Covers database-backed form generation and model-bound controls',
  },
  {
    name: 'Query Designer',
    lane: 'Query',
    icon: 'query',
    designSurface: 'Filter builder, joins, parameters, sort order, and result shape preview',
    generationOutput: 'Parameterized query object, DTO projection, and validation rules',
    runtimeContract: 'Bound parameters, pagination, explain-plan hook, and timeout policy',
    evidence: 'Covers read models, lookups, reports, and dashboard feeds',
  },
  {
    name: 'Client Dataset Designer',
    lane: 'Embedded DB',
    icon: 'dataset',
    designSurface: 'Offline table shape, sync keys, conflict rules, and local index plan',
    generationOutput: 'Local store schema, change log, sync mapper, and merge policy',
    runtimeContract: 'Offline cache, dirty-state tracking, and resumable synchronization',
    evidence: 'Covers mobile, desktop, and interrupted-network workflows',
  },
  {
    name: 'Service Publisher',
    lane: 'Publish',
    icon: 'api',
    designSurface: 'Endpoint map, verbs, payload schema, auth policy, and versioning controls',
    generationOutput: 'REST endpoint, OpenAPI contract, service client, and route tests',
    runtimeContract: 'Auth guard, validation middleware, rate limits, and response envelopes',
    evidence: 'Covers generated API services and integration boundaries',
  },
  {
    name: 'Service Proxy Designer',
    lane: 'Publish',
    icon: 'service',
    designSurface: 'Remote endpoint import, retry policy, timeout budget, and mapping editor',
    generationOutput: 'Typed client, adapter facade, fixtures, and error translation table',
    runtimeContract: 'Circuit breaker, retry budget, and observable request lifecycle',
    evidence: 'Covers generated clients for hosted and local services',
  },
  {
    name: 'Failover Policy',
    lane: 'Resilience',
    icon: 'workflow',
    designSurface: 'Primary/secondary source graph, health checks, and promotion rules',
    generationOutput: 'Failover coordinator, health probe, and operational runbook stub',
    runtimeContract: 'Bounded switchover, consistency mode, and telemetry events',
    evidence: 'Covers resilient data access and service-publishing paths',
  },
  {
    name: 'Replay Queue',
    lane: 'Resilience',
    icon: 'scheduler',
    designSurface: 'Retry schedule, dead-letter handling, idempotency key, and replay inspector',
    generationOutput: 'Durable outbox, retry worker, replay endpoint, and audit log table',
    runtimeContract: 'At-least-once delivery with idempotent handler contract',
    evidence: 'Covers offline submit, failed service calls, and delayed processing',
  },
  {
    name: 'Data Access Policy',
    lane: 'Security',
    icon: 'lock',
    designSurface: 'Role matrix, field masking, row filters, and secret reference picker',
    generationOutput: 'Policy middleware, scoped query filters, and generated tests',
    runtimeContract: 'Least-privilege data access with audited policy decisions',
    evidence: 'Covers secure generated data screens and service endpoints',
  },
]

const requiredLanes: DataServiceLane[] = ['Source', 'Query', 'Publish', 'Embedded DB', 'Resilience', 'Security']

export function dataServiceAudit() {
  const registeredIcons = new Set(iconNames)
  const missingIcons = dataServiceCapabilities.filter((capability) => !registeredIcons.has(capability.icon))
  const missingLanes = requiredLanes.filter(
    (lane) => !dataServiceCapabilities.some((capability) => capability.lane === lane),
  )
  const incompleteCapabilities = dataServiceCapabilities.filter(
    (capability) =>
      capability.designSurface.trim() === '' ||
      capability.generationOutput.trim() === '' ||
      capability.runtimeContract.trim() === '' ||
      capability.evidence.trim() === '',
  )

  return {
    ok: missingIcons.length === 0 && missingLanes.length === 0 && incompleteCapabilities.length === 0,
    totalCapabilities: dataServiceCapabilities.length,
    missingIcons,
    missingLanes,
    incompleteCapabilities,
  }
}
