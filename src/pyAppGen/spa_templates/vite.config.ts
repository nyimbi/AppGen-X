import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/** The generated app's frontend build.
 *
 * `ui_kit/` is emitted next to this file by the generator, so the alias is a
 * sibling path rather than a package dependency. The kit is the same source
 * the Studio consumes, so the two render identical markup.
 *
 * The dev server proxies the API to the Flask app, so `npm run dev` talks to a
 * live backend without a CORS relaxation.
 */
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      { find: '@appgen/ui-kit/components.css', replacement: '/app/ui_kit/components.css' },
      { find: '@appgen/ui-kit', replacement: '/app/ui_kit/index.ts' },
    ],
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:5000',
      '/static': 'http://127.0.0.1:5000',
    },
  },
})
