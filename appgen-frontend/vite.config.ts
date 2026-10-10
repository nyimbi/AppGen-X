import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const fromHere = (p: string) => fileURLToPath(new URL(p, import.meta.url))

// The kit is one source consumed twice: aliased here for the Studio, and
// copied into generated apps by pyAppGen.gen.write_ui_kit.
export default defineConfig({
  plugins: [react()],
  server: {
    // The Studio reads its panels from the Python backend. In dev that is a
    // separate process (`appgen studio-serve`), so its routes are proxied here
    // and the client's relative paths work in both dev and a served build.
    proxy: {
      '/api/studio': {
        target: process.env.APPGEN_STUDIO_BACKEND ?? 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
  },
  resolve: {
    alias: [
      { find: '@appgen/ui-kit/components.css', replacement: fromHere('../src/pyAppGen/ui_kit/src/components.css') },
      { find: '@appgen/ui-kit', replacement: fromHere('../src/pyAppGen/ui_kit/src/index.ts') },
      { find: 'react', replacement: fromHere('./node_modules/react') },
      { find: 'react-dom', replacement: fromHere('./node_modules/react-dom') },
    ],
  },
})
