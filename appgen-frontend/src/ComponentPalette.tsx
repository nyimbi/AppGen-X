import { EmptyState } from '@appgen/ui-kit'
import { Icon } from './Icon'
import { iconForClass } from './paletteIcon'
import { loadComponentPalette } from './studioApi'
import type { PaletteComponent, PaletteGroup } from './studioApi'
import { useStudioData } from './useStudioData'

type ComponentPaletteProps = {
  activeCategory: string | 'All'
  query: string
  onCategoryChange: (category: string | 'All') => void
  onQueryChange: (query: string) => void
}

/**
 * The toolbox reads the platform's own palette.
 *
 * The generator binds against `form_designer.COMPONENTS`; the panel used to
 * render a TypeScript catalog of 87 invented names, so it could offer a
 * component the generator did not have and hide one it did. The panel now
 * fetches the palette, and the groups arrive in the platform's order with the
 * platform's headings, so there is nothing left to disagree about.
 */
export function ComponentPalette({ activeCategory, query, onCategoryChange, onQueryChange }: ComponentPaletteProps) {
  const palette = useStudioData(loadComponentPalette)

  const components = palette.state === 'ready' ? palette.data.components : []
  const groups = palette.state === 'ready' ? palette.data.groups : []
  const visible = filterPaletteComponents(components, activeCategory, query)
  const visibleGroups = groupPaletteComponents(groups, visible)
  const counts = categoryCounts(components)

  return (
    <aside className="panel component-palette" aria-label="Component palette">
      <div className="panel-title-row">
        <div>
          <p className="eyebrow">Components</p>
          <h2>Toolbox</h2>
        </div>
        {palette.state === 'ready' && <span className="count-pill">{visible.length}</span>}
      </div>

      <label className="search-box">
        <Icon name="search" />
        <input
          aria-label="Search components"
          onChange={(event) => onQueryChange(event.target.value)}
          placeholder="Search controls"
          type="search"
          value={query}
        />
      </label>

      {palette.state === 'loading' && (
        <EmptyState description="Reading the palette from the backend." title="Loading components" />
      )}

      {palette.state === 'error' && (
        <EmptyState description={palette.error.message} title="Could not load the palette" />
      )}

      {palette.state === 'ready' && (
        <>
          <div className="category-tabs" aria-label="Component categories">
            <button className={activeCategory === 'All' ? 'selected' : ''} onClick={() => onCategoryChange('All')} type="button">
              <Icon name="grid" />
              <span>All</span>
            </button>
            {groups.map((group) => (
              <button
                className={activeCategory === group.category ? 'selected' : ''}
                key={group.category}
                onClick={() => onCategoryChange(group.category)}
                title={`${counts[group.category] ?? 0} ${group.label.toLowerCase()} components`}
                type="button"
              >
                <Icon name={iconForClass(group.icon)} />
                <span>{group.label}</span>
                <strong>{counts[group.category] ?? 0}</strong>
              </button>
            ))}
          </div>

          <div className="component-list">
            {visibleGroups.map((group) => (
              <section className="component-group" key={group.category}>
                <div className="component-group-title">
                  <Icon name={iconForClass(group.icon)} />
                  <span>{group.label}</span>
                  <strong>{group.components.length}</strong>
                </div>
                {group.components.map((component) => (
                  <button
                    aria-label={`${component.label}: ${component.description}`}
                    className={`component-tile category-${component.category.replace(/[^a-z0-9]+/g, '-')}-tile`}
                    data-component={component.component}
                    data-component-category={component.category}
                    data-component-icon={component.icon}
                    draggable
                    key={component.component}
                    title={component.description}
                    type="button"
                  >
                    <span className={`component-icon category-${component.category.replace(/[^a-z0-9]+/g, '-')}`}>
                      <Icon name={iconForClass(component.icon)} />
                    </span>
                    <span className="component-copy">
                      <span className="component-name-row">
                        <span className="component-name">{component.label}</span>
                        <Icon name="drag" className="component-drag-icon" />
                      </span>
                      <span className="component-description">{component.description}</span>
                      <span className="component-meta">
                        <Icon name={iconForClass(group.icon)} />
                        <span>{group.label}</span>
                      </span>
                    </span>
                    <span className="component-size">{component.size}</span>
                  </button>
                ))}
              </section>
            ))}
            {visible.length === 0 ? (
              <div className="empty-palette" role="status">
                <Icon name="search" />
                <span>No matching components</span>
              </div>
            ) : null}
          </div>
        </>
      )}
    </aside>
  )
}

export function filterPaletteComponents(
  components: readonly PaletteComponent[],
  activeCategory: string | 'All',
  query: string,
) {
  const normalizedQuery = query.trim().toLowerCase()

  return components.filter((component) => {
    const matchesCategory = activeCategory === 'All' || component.category === activeCategory
    const matchesQuery =
      !normalizedQuery ||
      component.label.toLowerCase().includes(normalizedQuery) ||
      component.description.toLowerCase().includes(normalizedQuery) ||
      component.component.toLowerCase().includes(normalizedQuery)

    return matchesCategory && matchesQuery
  })
}

export function groupPaletteComponents(
  groups: readonly PaletteGroup[],
  components: readonly PaletteComponent[],
) {
  const byName = new Map(components.map((component) => [component.component, component]))

  return groups
    .map((group) => ({
      category: group.category,
      label: group.label,
      icon: group.icon,
      components: group.components
        .map((name) => byName.get(name))
        .filter((component): component is PaletteComponent => component !== undefined),
    }))
    .filter((group) => group.components.length > 0)
}

export function categoryCounts(components: readonly PaletteComponent[]) {
  const counts: Record<string, number> = {}
  for (const component of components) {
    counts[component.category] = (counts[component.category] ?? 0) + 1
  }
  return counts
}

export function componentDragPayload(component: PaletteComponent) {
  return {
    component: component.component,
    category: component.category,
    icon: component.icon,
    size: component.size,
    draggable: true,
  }
}
