import { Badge, Card, EmptyState, PageHeader } from '@appgen/ui-kit'
import { Icon } from './Icon'
import { loadComponentPackages } from './studioApi'
import { useStudioData } from './useStudioData'

/**
 * The package panel reads the platform's own component suites.
 *
 * The suites are what the generator can install; the panel used to list a
 * TypeScript catalog of its own, so it could offer a package that did not
 * exist. Each suite is a card, its components are the evidence it is real.
 */
export function PackageManager() {
  const packages = useStudioData(loadComponentPackages)

  return (
    <section className="panel package-manager" aria-label="Design-time package manager">
      <PageHeader
        description="Third-party component suites the generator can install into a design."
        title="Component Installation"
      />

      {packages.state === 'loading' && (
        <EmptyState description="Reading the component suites from the backend." title="Loading packages" />
      )}

      {packages.state === 'error' && (
        <EmptyState
          description={packages.error.message}
          title="Could not load packages"
        />
      )}

      {packages.state === 'ready' && packages.data.packages.length === 0 && (
        <EmptyState title="No component suites are installed" />
      )}

      {packages.state === 'ready' && packages.data.packages.length > 0 && (
        <div className="package-grid">
          {packages.data.packages.map((item) => (
            <Card
              actions={<Badge tone={item.license === 'commercial' ? 'warning' : 'success'}>{item.license}</Badge>}
              as="article"
              key={item.id}
              subtitle={`${item.vendor} · ${item.frameworks.join(', ')}`}
              title={item.id}
            >
              <div className="package-components">
                {item.components.map((component) => (
                  <span key={`${item.id}-${component}`}>{component}</span>
                ))}
              </div>
              {item.use_cases && item.use_cases.length > 0 && (
                <p className="package-use-cases">
                  <Icon name="check" />
                  {item.use_cases.join(' · ')}
                </p>
              )}
            </Card>
          ))}
        </div>
      )}
    </section>
  )
}
