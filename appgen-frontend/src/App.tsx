import { useState } from 'react'
import './App.css'
import { ComponentPalette } from './ComponentPalette'
import { DesignerCanvas } from './DesignerCanvas'
import { InspectorPanel } from './InspectorPanel'
import { PackageManager } from './PackageManager'
import { StatusRail } from './StatusRail'
import { StudioChrome } from './StudioChrome'
import type { ComponentCategory } from './componentCatalog'

function App() {
  const [activeCategory, setActiveCategory] = useState<ComponentCategory | 'All'>('All')
  const [query, setQuery] = useState('')

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
      <PackageManager />
      <StatusRail />
    </div>
  )
}

export default App
