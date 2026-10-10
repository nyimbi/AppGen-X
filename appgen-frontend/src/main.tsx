import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './tokens.css'
import '@appgen/ui-kit/components.css'
import './index.css'
import { ToastProvider } from '@appgen/ui-kit'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ToastProvider>
      <App />
    </ToastProvider>
  </React.StrictMode>,
)
