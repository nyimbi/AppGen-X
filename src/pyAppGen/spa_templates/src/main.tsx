import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import '@appgen/ui-kit/components.css'
import './appgen.css'

import { App } from './App'

const container = document.getElementById('root')
if (!container) {
  throw new Error('the generated app shell is missing its #root element')
}

createRoot(container).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
