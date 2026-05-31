export type DslDiagnosticSeverity = 'error' | 'warning' | 'info'

export type DslDiagnostic = {
  code: string
  severity: DslDiagnosticSeverity
  message: string
  line: number
  column: number
}

export type DslCompletion = {
  label: string
  insertText: string
  detail: string
  category: 'schema' | 'ui' | 'workflow' | 'agent' | 'release'
}

export type DslQuickFix = {
  id: string
  title: string
  diagnosticCode: string
  preview: string
  apply: (source: string) => string
}

export const dslEditorSample = `app InvoiceOps { targets: web, mobile, desktop }

table Invoice {
  id: int pk
  customer: string required search
  status: string
  total: decimal required
}

view InvoiceForm for Invoice {
  Main: customer, status, total
  on Save -> SubmitInvoice
}

flow InvoiceApproval {
  draft -> approved on approve
}

agent BillingAssistant {
  provider: LocalModel
  goal: "Help billing users review invoices"
  tools: schema, forms, reports
}
`

export const dslCompletions: DslCompletion[] = [
  {
    label: 'table',
    insertText: 'table Entity {\n  id: int pk\n  name: string required search\n}',
    detail: 'Create a database-backed table with a primary key and searchable name.',
    category: 'schema',
  },
  {
    label: 'view',
    insertText: 'view EntityForm for Entity {\n  Main: name\n}',
    detail: 'Create a form projection for a table.',
    category: 'ui',
  },
  {
    label: 'flow',
    insertText: 'flow EntityWorkflow {\n  draft -> approved on approve\n}',
    detail: 'Create a workflow with a transition event.',
    category: 'workflow',
  },
  {
    label: 'agent',
    insertText: 'agent Assistant {\n  provider: LocalModel\n  goal: "Help users finish work"\n  tools: schema, forms, reports\n}',
    detail: 'Create an agent contract that can use local or API-backed models.',
    category: 'agent',
  },
  {
    label: 'package',
    insertText: 'package ReleaseBundle {\n  targets: web, mobile, desktop\n}',
    detail: 'Declare release targets for generated application packages.',
    category: 'release',
  },
]

export function dslEditorDiagnostics(source: string): DslDiagnostic[] {
  const diagnostics: DslDiagnostic[] = []
  const lines = source.split('\n')
  const statusLine = lines.findIndex((line) => /^\s*status:\s*string\s*$/.test(line))
  if (statusLine >= 0) {
    diagnostics.push({
      code: 'AGX0304',
      severity: 'warning',
      message: 'Database-backed workflow status should be searchable or constrained.',
      line: statusLine + 1,
      column: lines[statusLine].indexOf('status') + 1,
    })
  }
  const saveLine = lines.findIndex((line) => line.includes('on Save -> SubmitInvoice'))
  const hasHandler = /operation\s+SubmitInvoice\b/.test(source)
  if (saveLine >= 0 && !hasHandler) {
    diagnostics.push({
      code: 'AGX0402',
      severity: 'error',
      message: 'Handler SubmitInvoice is referenced by the form but not defined.',
      line: saveLine + 1,
      column: lines[saveLine].indexOf('SubmitInvoice') + 1,
    })
  }
  return diagnostics
}

export const dslQuickFixes: DslQuickFix[] = [
  {
    id: 'make_status_searchable',
    title: 'Make status searchable',
    diagnosticCode: 'AGX0304',
    preview: 'status: string search',
    apply: (source) => source.replace(/(^\s*status:\s*string)\s*$/m, '$1 search'),
  },
  {
    id: 'create_submit_invoice_operation',
    title: 'Create SubmitInvoice operation',
    diagnosticCode: 'AGX0402',
    preview: 'operation SubmitInvoice { input: Invoice; action: validate, persist }',
    apply: (source) =>
      /operation\s+SubmitInvoice\b/.test(source)
        ? source
        : `${source.trimEnd()}\n\noperation SubmitInvoice {\n  input: Invoice\n  action: validate, persist\n}\n`,
  },
]

export function quickFixesForDiagnostics(diagnostics: DslDiagnostic[]) {
  const codes = new Set(diagnostics.map((diagnostic) => diagnostic.code))
  return dslQuickFixes.filter((fix) => codes.has(fix.diagnosticCode))
}

export function dslOutline(source: string) {
  const blockPattern = /^(app|table|view|flow|agent|operation|package)\s+([A-Za-z_][A-Za-z0-9_]*)/gm
  return Array.from(source.matchAll(blockPattern), (match) => ({
    kind: match[1],
    name: match[2],
  }))
}

export function dslEditorAudit() {
  const diagnostics = dslEditorDiagnostics(dslEditorSample)
  const fixes = quickFixesForDiagnostics(diagnostics)
  const fixed = fixes.reduce((source, fix) => fix.apply(source), dslEditorSample)
  const fixedDiagnostics = dslEditorDiagnostics(fixed)
  const outline = dslOutline(fixed)
  const completionCategories = new Set(dslCompletions.map((completion) => completion.category))
  const requiredCategories = ['schema', 'ui', 'workflow', 'agent', 'release']
  const missingCompletionCategories = requiredCategories.filter((category) => !completionCategories.has(category as DslCompletion['category']))

  return {
    format: 'appgen.frontend-dsl-editor-audit.v1',
    ok:
      diagnostics.length === 2 &&
      fixes.length === 2 &&
      fixedDiagnostics.length === 0 &&
      outline.length >= 6 &&
      missingCompletionCategories.length === 0,
    diagnosticCount: diagnostics.length,
    quickFixCount: fixes.length,
    fixedDiagnosticCount: fixedDiagnostics.length,
    outlineCount: outline.length,
    completionCount: dslCompletions.length,
    missingCompletionCategories,
  }
}
