import { Badge, Card, EmptyState, PageHeader } from '@appgen/ui-kit'
import { loadTargetCapabilities } from './studioApi'
import { useStudioData } from './useStudioData'

/**
 * The device panel reads the platform's own target contracts.
 *
 * The platform states each target's capabilities and permissions; the panel
 * used to keep a TypeScript list of its own, so it could show a capability no
 * target declares. Each target is a card, its permissions are the evidence.
 */
export function DeviceApiWorkbench() {
  const capabilities = useStudioData(loadTargetCapabilities)

  return (
    <section className="panel device-api-workbench" aria-label="Device API workbench">
      <PageHeader
        description="Capabilities and permissions each generated target can use."
        title="Native Capability Coverage"
      />

      {capabilities.state === 'loading' && (
        <EmptyState description="Reading the target contracts from the backend." title="Loading capabilities" />
      )}

      {capabilities.state === 'error' && (
        <EmptyState description={capabilities.error.message} title="Could not load capabilities" />
      )}

      {capabilities.state === 'ready' && (
        <div className="device-api-grid">
          {(
            [
              ['mobile', capabilities.data.mobile],
              ['desktop', capabilities.data.desktop],
            ] as const
          ).map(([name, contract]) => (
            <Card
              actions={<Badge tone="info">{name}</Badge>}
              as="article"
              key={name}
              subtitle={String((contract.target as { runtime?: string }).runtime ?? '')}
              title={name}
            >
              <div className="device-api-list">
                {('permissions' in contract ? contract.permissions : []).map((permission) => (
                  <div className="device-api-card" key={permission}>
                    <strong>{permission}</strong>
                  </div>
                ))}
                {('capabilities' in (contract.target as object)
                  ? ((contract.target as { capabilities?: readonly string[] }).capabilities ?? [])
                  : []
                ).map((capability) => (
                  <span className="device-api-fallback" key={capability}>
                    {capability}
                  </span>
                ))}
              </div>
            </Card>
          ))}
        </div>
      )}
    </section>
  )
}
