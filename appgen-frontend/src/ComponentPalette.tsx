import { Icon } from './Icon'
import type { ComponentCategory } from './componentCatalog'
import { paletteCategories, paletteComponents } from './componentCatalog'

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
          All
        </button>
        {paletteCategories.map((category) => (
          <button
            className={activeCategory === category ? 'selected' : ''}
            key={category}
            onClick={() => onCategoryChange(category)}
            type="button"
          >
            {category}
          </button>
        ))}
      </div>

      <div className="component-list">
        {visibleComponents.map((component) => (
          <button className="component-tile" draggable key={component.name} title={component.description} type="button">
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
      </div>
    </aside>
  )
}
