import { createServer } from 'node:http'
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { extname, join, resolve } from 'node:path'
import { spawn } from 'node:child_process'

const root = resolve(new URL('..', import.meta.url).pathname)
const distDir = join(root, 'dist')
const reportPath = join(root, 'browser-smoke-report.json')

const contentTypes = {
  '.css': 'text/css',
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
}

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

function createStaticServer() {
  return createServer((request, response) => {
    const requestUrl = new URL(request.url ?? '/', 'http://127.0.0.1')
    const normalizedPath = requestUrl.pathname === '/' ? '/index.html' : requestUrl.pathname
    const filePath = resolve(join(distDir, normalizedPath))
    const safePath = filePath.startsWith(distDir) && existsSync(filePath) ? filePath : join(distDir, 'index.html')
    const extension = extname(safePath)

    response.setHeader('Content-Type', contentTypes[extension] ?? 'application/octet-stream')
    response.end(Buffer.from(readFileSync(safePath)))
  })
}

function listen(server) {
  return new Promise((resolveListen, rejectListen) => {
    server.once('error', rejectListen)
    server.listen(0, '127.0.0.1', () => {
      const address = server.address()
      if (!address || typeof address === 'string') {
        rejectListen(new Error('Could not determine browser smoke server address.'))
        return
      }
      resolveListen(address.port)
    })
  })
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
      '--virtual-time-budget=3000',
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
    const timeout = setTimeout(() => {
      browser.kill('SIGKILL')
      rmSync(userDataDir, { force: true, recursive: true })
      rejectDump(new Error(`Timed out loading ${url}`))
    }, 15000)

    browser.stdout.on('data', (chunk) => {
      stdout += chunk.toString()
    })
    browser.stderr.on('data', (chunk) => {
      stderr += chunk.toString()
    })
    browser.once('error', (error) => {
      clearTimeout(timeout)
      rmSync(userDataDir, { force: true, recursive: true })
      rejectDump(error)
    })
    browser.once('close', (code) => {
      clearTimeout(timeout)
      rmSync(userDataDir, { force: true, recursive: true })
      if (code !== 0) {
        rejectDump(new Error(`Chrome exited with ${code} for ${url}\n${stderr}`))
        return
      }
      resolveDump(stdout)
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
  const server = createStaticServer()
  const port = await listen(server)
  const baseUrl = `http://127.0.0.1:${port}`
  const scenarios = [
    {
      id: 'studio_shell',
      path: '/',
      includes: [
        'AppGen Studio',
        'Toolbox',
        'Invoice Workspace',
        'Object Inspector',
        'Component Installation',
        'Native Capability Coverage',
        'Sources, Queries, Publishing',
      ],
    },
    {
      id: 'device_palette_filter',
      path: '/?studioCategory=Device',
      includes: ['Secure Storage', 'File Storage', 'Background Sync', 'Share Sheet'],
    },
    {
      id: 'storage_search_filter',
      path: '/?studioQuery=storage',
      includes: ['Secure Storage', 'File Storage', 'Client Dataset', 'Local files'],
    },
    {
      id: 'empty_palette_state',
      path: '/?studioQuery=definitely-not-a-component',
      includes: ['No matching components'],
    },
  ]
  const results = []

  try {
    for (const scenario of scenarios) {
      const dom = await dumpDom(chrome, `${baseUrl}${scenario.path}`)
      assertIncludes(dom, scenario.includes, scenario.id)
      results.push({ id: scenario.id, ok: true, bytes: dom.length })
    }
  } finally {
    server.close()
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
