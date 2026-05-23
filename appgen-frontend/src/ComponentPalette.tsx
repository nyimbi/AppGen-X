import { Icon } from './Icon'
import type { ComponentCategory } from './componentCatalog'
import { categoryIcons, paletteCategories, paletteComponents } from './componentCatalog'

type ComponentPaletteProps = {
  activeCategory: ComponentCategory | 'All'
  query: string
  onCategoryChange: (category: ComponentCategory | 'All') => void
  onQueryChange: (query: string) => void
}

export function ComponentPalette({
  activeCategory,
  query,
  onCategoryChange,
  onQueryChange,
}: ComponentPaletteProps) {
  const normalizedQuery = query.trim().toLowerCase()
  const visibleComponents = paletteComponents.filter((component) => {
    const matchesCategory = activeCategory === 'All' || component.category === activeCategory
    const matchesQuery =
      !normalizedQuery ||
      component.name.toLowerCase().includes(normalizedQuery) ||
      component.description.toLowerCase().includes(normalizedQuery)

    return matchesCategory && matchesQuery
  })
  const visibleGroups = paletteCategories
    .map((category) => ({
      category,
      components: visibleComponents.filter((component) => component.category === category),
    }))
    .filter((group) => group.components.length > 0)
  const categoryCounts = Object.fromEntries(
    paletteCategories.map((category) => [
      category,
      paletteComponents.filter((component) => component.category === category).length,
    ]),
  ) as Record<ComponentCategory, number>

  return (
    <aside className="panel component-palette" aria-label="Component palette">
      <div className="panel-title-row">
        <div>
          <p className="eyebrow">Components</p>
          <h2>Toolbox</h2>
        </div>
        <span className="count-pill">{visibleComponents.length}</span>
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

      <div className="category-tabs" aria-label="Component categories">
        <button className={activeCategory === 'All' ? 'selected' : ''} onClick={() => onCategoryChange('All')} type="button">
          <Icon name={categoryIcons.All} />
          <span>All</span>
        </button>
        {paletteCategories.map((category) => (
          <button
            className={activeCategory === category ? 'selected' : ''}
            key={category}
            onClick={() => onCategoryChange(category)}
            type="button"
            title={`${categoryCounts[category]} ${category.toLowerCase()} components`}
          >
            <Icon name={categoryIcons[category]} />
            <span>{category}</span>
            <strong>{categoryCounts[category]}</strong>
          </button>
        ))}
      </div>

      <div className="component-list">
        {visibleGroups.map((group) => (
          <section className="component-group" key={group.category}>
            <div className="component-group-title">
              <Icon name={categoryIcons[group.category]} />
              <span>{group.category}</span>
              <strong>{group.components.length}</strong>
            </div>
            {group.components.map((component) => (
              <button
                aria-label={`${component.name}: ${component.description}`}
                className="component-tile"
                data-component={component.name}
                data-component-icon={component.icon}
                draggable
                key={component.name}
                title={component.description}
                type="button"
              >
                <span className={`component-icon category-${component.category.toLowerCase()}`}>
                  <Icon name={component.icon} />
                </span>
                <span className="component-copy">
                  <span className="component-name">{component.name}</span>
                  <span className="component-description">{component.description}</span>
                </span>
                <span className="component-size">{component.size}</span>
              </button>
            ))}
          </section>
        ))}
        {visibleComponents.length === 0 ? (
          <div className="empty-palette" role="status">
            <Icon name="search" />
            <span>No matching components</span>
          </div>
        ) : null}
      </div>
    </aside>
  )
}
