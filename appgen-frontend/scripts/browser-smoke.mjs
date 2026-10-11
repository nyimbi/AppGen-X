import { existsSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { spawn } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const root = resolve(here, '..')
const distDir = join(root, 'dist')
const reportPath = join(root, 'browser-smoke-report.json')
const domDumpScript = join(here, 'dom_dump.py')
const pythonCommand = process.env.APPGEN_PYTHON ?? 'python3'

// The Studio's panels read the Python backend over `/api/studio/*`, so the
// smoke needs both halves. `appgen studio-serve` serves the API and `dist/`
// from one process, which is how the Studio actually runs; the harness used to
// serve `dist/` from a static Node server, where every API call fell through to
// index.html and the panels rendered their error state.
const defaultPort = Number(process.env.APPGEN_STUDIO_PORT ?? 5199)
const backendCommand = process.env.APPGEN_STUDIO_COMMAND ?? 'appgen'
const backendArgs = ['studio-serve', '--host', '127.0.0.1', '--port', String(defaultPort)]

// The document is only complete once every `/api/studio/*` fetch has settled,
// and `/api/studio/workspace` alone walks the whole catalog. On a two-core
// runner that outruns a short budget, so the timeout has to cover the slowest
// route on the slowest machine rather than a local one.
const dumpTimeoutMs = Number(process.env.APPGEN_STUDIO_DUMP_TIMEOUT_MS ?? 60000)

function startBackend(port) {
  const backend = spawn(backendCommand, backendArgs, {
    cwd: root,
    stdio: ['ignore', 'pipe', 'pipe'],
    env: { ...process.env, PYTHONPATH: resolve(root, '..', 'src') },
  })
  backend.stdout.on('data', () => {})
  backend.stderr.on('data', () => {})
  return backend
}

async function waitForBackend(baseUrl, attempts = 60) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(`${baseUrl}/api/studio/manifest`)
      if (response.ok) return
    } catch {
      // The server is still binding; keep polling.
    }
    await new Promise((resolveWait) => setTimeout(resolveWait, 500))
  }
  throw new Error(`Studio backend did not answer on ${baseUrl}. Is the \`appgen\` CLI installed, or set APPGEN_STUDIO_COMMAND?`)
}

function dumpDom(url) {
  return new Promise((resolveDump, rejectDump) => {
    const child = spawn(pythonCommand, [domDumpScript, url], {
      cwd: root,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: process.env,
    })
    let stdout = ''
    let stderr = ''
    let settled = false
    const finish = (error) => {
      if (settled) return
      settled = true
      clearTimeout(timer)
      child.kill('SIGKILL')
      if (error) rejectDump(error)
      else resolveDump(stdout)
    }
    // The driver owns the page timeout; this is the backstop for a driver that
    // never exits at all, so it sits above the page timeout rather than at it.
    const timer = setTimeout(() => {
      finish(new Error(
        `Rendering ${url} produced no document within ${dumpTimeoutMs}ms `
        + `(${stdout.length} bytes received)\n`
        + `--- partial document ---\n${stdout.slice(-2000) || '(nothing on stdout)'}\n`
        + `--- driver stderr ---\n${stderr.slice(-2000) || '(nothing on stderr)'}`,
      ))
    }, dumpTimeoutMs + 15000)

    child.stdout.on('data', (chunk) => {
      stdout += chunk.toString()
    })
    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString()
    })
    child.once('error', (error) => {
      finish(error)
    })
    child.once('close', (code) => {
      if (code !== 0) {
        finish(new Error(`Rendering ${url} failed with ${code}\n${stderr}`))
        return
      }
      if (!stdout.includes('</html>')) {
        finish(new Error(
          `Rendering ${url} returned an incomplete document (${stdout.length} bytes)\n`
          + `--- partial document ---\n${stdout.slice(-2000) || '(nothing on stdout)'}`,
        ))
        return
      }
      finish()
    })
  })
}

function assertIncludes(dom, expected, scenario) {
  const missing = expected.filter((text) => !dom.includes(text))
  if (missing.length) {
    throw new Error(`${scenario} missing browser-rendered text: ${missing.join(', ')}`)
  }
}

async function main() {
  if (!existsSync(join(distDir, 'index.html'))) {
    throw new Error('Build the Studio first with `npm run build` before running browser smoke tests.')
  }

  const backend = startBackend(defaultPort)
  const baseUrl = `http://127.0.0.1:${defaultPort}`
  const scenarios = [
    {
      id: 'studio_shell',
      path: '/',
      includes: [
        'AppGen Studio',
        'Toolbox',
        'InvoiceForm',
        'Object Inspector',
        'Component Installation',
        'Native Capability Coverage',
        'Sources, Queries, Publishing',
        'Editor And Designer Bridge',
        'appgen.lsp-service.v1',
      ],
    },
    {
      id: 'semantic_service_bridge',
      path: '/#database',
      includes: ['Language service', 'Designer sync', 'Graph suite', 'Change planner'],
    },
    {
      id: 'designer_binding_graph',
      path: '/#forms',
      includes: ['Bindings', 'field:name', 'control:name', 'field_to_control'],
    },
    {
      id: 'data_service_lanes',
      path: '/#database',
      includes: ['Sources, Queries, Publishing', 'Embedded DB', 'Resilience', 'Readiness'],
    },
    {
      id: 'inspector_editors',
      path: '/#forms',
      includes: ['Object Inspector', 'Property', 'Event', 'Custom Designer'],
    },
    {
      // `mobile` is the platform's category key; its display heading is Device.
      id: 'device_palette_filter',
      path: '/?studioCategory=mobile',
      includes: ['Secure Storage', 'File Storage', 'Background Sync', 'Share Sheet'],
    },
    {
      id: 'storage_search_filter',
      path: '/?studioQuery=storage',
      includes: ['Secure Storage', 'File Storage'],
    },
    {
      id: 'empty_palette_state',
      path: '/?studioQuery=definitely-not-a-component',
      includes: ['No matching components'],
    },
  ]
  const results = []

  try {
    await waitForBackend(baseUrl)
    for (const scenario of scenarios) {
      const dom = await dumpDom(`${baseUrl}${scenario.path}`)
      assertIncludes(dom, scenario.includes, scenario.id)
      results.push({ id: scenario.id, ok: true, bytes: dom.length })
    }
  } finally {
    backend.kill('SIGTERM')
  }

  const report = {
    format: 'appgen.studio-browser-smoke.v1',
    ok: results.every((result) => result.ok),
    browser: process.env.APPGEN_CHROME_BIN ?? 'playwright-chromium',
    scenarios: results,
  }
  writeFileSync(reportPath, JSON.stringify(report, null, 2))
  console.log(JSON.stringify(report, null, 2))
}

main().catch((error) => {
  writeFileSync(reportPath, JSON.stringify({
    format: 'appgen.studio-browser-smoke.v1',
    ok: false,
    error: error.message,
  }, null, 2))
  console.error(error.message)
  process.exit(1)
})
