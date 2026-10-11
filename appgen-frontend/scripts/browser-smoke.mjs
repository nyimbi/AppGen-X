import { existsSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import { spawn } from 'node:child_process'

const root = resolve(new URL('..', import.meta.url).pathname)
const distDir = join(root, 'dist')
const reportPath = join(root, 'browser-smoke-report.json')

// The Studio's panels read the Python backend over `/api/studio/*`, so the
// smoke needs both halves. `appgen studio-serve` serves the API and `dist/`
// from one process, which is how the Studio actually runs; the harness used to
// serve `dist/` from a static Node server, where every API call fell through to
// index.html and the panels rendered their error state.
const defaultPort = Number(process.env.APPGEN_STUDIO_PORT ?? 5199)
const backendCommand = process.env.APPGEN_STUDIO_COMMAND ?? 'appgen'
const backendArgs = ['studio-serve', '--host', '127.0.0.1', '--port', String(defaultPort)]

// `--virtual-time-budget` pauses virtual time while a network fetch is pending,
// so the dump only completes once every request the SPA fires has settled. The
// budget therefore has to cover the slowest route (`/api/studio/workspace`
// walks the whole catalog) on the slowest runner, not just a local machine.
const virtualTimeBudgetMs = Number(process.env.APPGEN_STUDIO_VIRTUAL_TIME_MS ?? 15000)
const dumpTimeoutMs = Number(process.env.APPGEN_STUDIO_DUMP_TIMEOUT_MS ?? 60000)

const chromeCandidates = [
  process.env.APPGEN_CHROME_BIN,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
].filter(Boolean)

function findChrome() {
  const chrome = chromeCandidates.find((candidate) => existsSync(candidate))
  if (!chrome) {
    throw new Error('No Chrome-compatible browser found. Set APPGEN_CHROME_BIN to run the Studio browser smoke test.')
  }
  return chrome
}

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

function dumpDomWithHeadlessMode(chrome, url, headlessMode) {
  return new Promise((resolveDump, rejectDump) => {
    const userDataDir = mkdtempSync(join(tmpdir(), 'appgen-studio-chrome-'))
    const browser = spawn(chrome, [
      headlessMode,
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-gpu',
      '--disable-dev-shm-usage',
      '--disable-crash-reporter',
      '--disable-breakpad',
      '--disable-extensions',
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-background-networking',
      '--disable-component-update',
      '--disable-features=Crashpad',
      '--password-store=basic',
      '--use-mock-keychain',
      `--crash-dumps-dir=${userDataDir}`,
      `--user-data-dir=${userDataDir}`,
      `--virtual-time-budget=${virtualTimeBudgetMs}`,
      '--dump-dom',
      url,
    ], {
      env: {
        ...process.env,
        HOME: userDataDir,
        TMPDIR: userDataDir,
        XDG_CACHE_HOME: userDataDir,
        XDG_CONFIG_HOME: userDataDir,
      },
    })
    let stdout = ''
    let stderr = ''
    let settled = false
    const finish = (error) => {
      if (settled) return
      settled = true
      clearTimeout(timeout)
      browser.kill('SIGKILL')
      rmSync(userDataDir, { force: true, recursive: true })
      if (error) rejectDump(error)
      else resolveDump(stdout)
    }
    const timeout = setTimeout(() => {
      // `--dump-dom` writes the document and then hangs instead of exiting on
      // some Chrome builds. A complete document is the evidence the caller
      // wants, so it is accepted; a truncated one is still a failure.
      if (stdout.includes('</html>')) finish()
      else finish(new Error(
        `Timed out loading ${url} with an incomplete document `
        + `(${stdout.length} bytes received)\n`
        + `--- partial document ---\n${stdout.slice(-2000) || '(nothing on stdout)'}\n`
        + `--- chrome stderr ---\n${stderr.slice(-2000) || '(nothing on stderr)'}`,
      ))
    }, dumpTimeoutMs)

    browser.stdout.on('data', (chunk) => {
      stdout += chunk.toString()
      if (stdout.includes('</html>')) finish()
    })
    browser.stderr.on('data', (chunk) => {
      stderr += chunk.toString()
    })
    browser.once('error', (error) => {
      finish(error)
    })
    browser.once('close', (code) => {
      if (code !== 0) {
        finish(new Error(`Chrome exited with ${code} for ${url}\n${stderr}`))
        return
      }
      finish()
    })
  })
}

async function dumpDom(chrome, url) {
  const errors = []
  for (const headlessMode of ['--headless=new', '--headless']) {
    try {
      return await dumpDomWithHeadlessMode(chrome, url, headlessMode)
    } catch (error) {
      errors.push(`${headlessMode}: ${error.message}`)
    }
  }
  throw new Error(`Chrome dump failed for ${url}\n${errors.join('\n')}`)
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

  const chrome = findChrome()
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
      const dom = await dumpDom(chrome, `${baseUrl}${scenario.path}`)
      assertIncludes(dom, scenario.includes, scenario.id)
      results.push({ id: scenario.id, ok: true, bytes: dom.length })
    }
  } finally {
    backend.kill('SIGTERM')
  }

  const report = {
    format: 'appgen.studio-browser-smoke.v1',
    ok: results.every((result) => result.ok),
    browser: chrome,
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
