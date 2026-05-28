import { useState } from 'react'
import './App.css'
import { ComponentPalette } from './ComponentPalette'
import { DataServiceWorkbench } from './DataServiceWorkbench'
import { DesignerCanvas } from './DesignerCanvas'
import { DeviceApiWorkbench } from './DeviceApiWorkbench'
import { InspectorPanel } from './InspectorPanel'
import { PackageManager } from './PackageManager'
import { SemanticServicePanel } from './SemanticServicePanel'
import { StatusRail } from './StatusRail'
import { StudioChrome } from './StudioChrome'
import { paletteCategories } from './componentCatalog'
import type { ComponentCategory } from './componentCatalog'

type StudioInitialState = {
  category: ComponentCategory | 'All'
  query: string
}

export function readStudioInitialState(search = typeof window === 'undefined' ? '' : window.location.search): StudioInitialState {
  const params = new URLSearchParams(search)
  const requestedCategory = params.get('studioCategory')
  const category =
    requestedCategory && paletteCategories.includes(requestedCategory as ComponentCategory)
      ? (requestedCategory as ComponentCategory)
      : 'All'

  return {
    category,
    query: params.get('studioQuery') ?? '',
  }
}

function App() {
  const initialState = readStudioInitialState()
  const [activeCategory, setActiveCategory] = useState<ComponentCategory | 'All'>(initialState.category)
  const [query, setQuery] = useState(initialState.query)

  return (
    <div className="app-shell">
      <StudioChrome />
      <section className="workbench">
        <ComponentPalette
          activeCategory={activeCategory}
          onCategoryChange={setActiveCategory}
          onQueryChange={setQuery}
          query={query}
        />
        <DesignerCanvas />
        <InspectorPanel />
      </section>
      <SemanticServicePanel />
      <PackageManager />
      <DeviceApiWorkbench />
      <DataServiceWorkbench />
      <StatusRail />
    </div>
  )
}

export default App
