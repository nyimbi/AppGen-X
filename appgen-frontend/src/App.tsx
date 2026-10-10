import { useEffect, useState } from 'react'
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
import { readSection } from './studioSections'

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
  const [section, setSection] = useState(() => readSection())

  useEffect(() => {
    const onHashChange = () => setSection(readSection())
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const goToSection = (id: string) => {
    window.location.hash = id
    setSection(id)
  }

  const palette = (
    <ComponentPalette
      activeCategory={activeCategory}
      onCategoryChange={setActiveCategory}
      onQueryChange={setQuery}
      query={query}
    />
  )

  // `overview` renders every panel, so the workbench is fully visible on first
  // load and the browser smoke's single-page scenarios keep seeing all of them.
  // A named section narrows to the panels it owns.
  const panels =
    section === 'forms' ? (
      <section className="workbench">
        {palette}
        <DesignerCanvas />
        <InspectorPanel />
      </section>
    ) : section === 'database' ? (
      <>
        <SemanticServicePanel />
        <DataServiceWorkbench />
      </>
    ) : section === 'packages' ? (
      <PackageManager />
    ) : section === 'targets' ? (
      <DeviceApiWorkbench />
    ) : (
      <>
        <section className="workbench">
          {palette}
          <DesignerCanvas />
          <InspectorPanel />
        </section>
        <SemanticServicePanel />
        <PackageManager />
        <DeviceApiWorkbench />
        <DataServiceWorkbench />
      </>
    )

  return (
    <div className="app-shell">
      <StudioChrome activeSection={section} onSectionChange={goToSection} />
      {panels}
      <StatusRail />
    </div>
  )
}

export default App
