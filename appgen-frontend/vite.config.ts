import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const fromHere = (p: string) => fileURLToPath(new URL(p, import.meta.url))

// The kit is one source consumed twice: aliased here for the Studio, and
// copied into generated apps by pyAppGen.gen.write_ui_kit.
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      { find: '@appgen/ui-kit/components.css', replacement: fromHere('../src/pyAppGen/ui_kit/src/components.css') },
      { find: '@appgen/ui-kit', replacement: fromHere('../src/pyAppGen/ui_kit/src/index.ts') },
      { find: 'react', replacement: fromHere('./node_modules/react') },
      { find: 'react-dom', replacement: fromHere('./node_modules/react-dom') },
    ],
  },
})
