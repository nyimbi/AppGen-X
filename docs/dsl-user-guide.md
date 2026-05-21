# AppGen DSL User Guide

Use the AppGen DSL when you want a readable source of truth for generated
applications. The same DSL can drive database schema, forms, generated REST and
GraphQL APIs, PWA assets, mobile and desktop starters, chatbots, agents,
reports, ERP templates, deployment files, and quality checks.

## Minimal App

```appgen
app Library { theme: sage; targets: web, mobile, desktop }

table Author {
  id: int pk
  name: string required search
  email: string unique
}

table Book {
  id: int pk
  title: string required search
  author_id: int required -> Author.id [many-to-one]
}
```

Generate from the DSL:

```bash
appgen --dsl library.appgen --writedir generated/app
```

Lint without generating:

```bash
appgen --lint-dsl library.appgen
```

Format in place before review:

```bash
appgen --format-dsl library.appgen
```

Format DSL text through `pyAppGen.dsl.format_dsl` or the generated
`dsl_reference.format_dsl` helper when builders need stable indentation and
spacing before review. Formatting returns before/after lint reports and does not
add keywords or apply semantic quick fixes.

IDE integrations can use `pyAppGen.dsl.dsl_language_service(source)` for a
single authoring payload: ANTLR-backed lint, parser-backed outline,
schema-aware completions, deterministic formatting preview, and language-quality
evidence. The outline falls back to a partial regex outline for incomplete
drafts, so editors can keep navigation and completions active while a builder is
still typing.

## Modeling Guidance

Use one table per business object. Use explicit `id: int pk` fields when you
want stable identifiers, or let AppGen add one when omitted.

If you are sketching quickly, you may write `entity` or `model` for `table`,
`form` or `screen` for `view`, and `workflow` for `flow`. AppGen accepts these
as authoring aliases before parsing, then the linter can rewrite them to the
canonical DSL so the committed language stays small.
You may also write `searchable` for `search` and `hide` for `hidden` on fields;
the parser receives the canonical modifiers, and the linter offers
`normalize_modifier_aliases`.

Use `dsl_language_quality_contract()` or the generated
`/dsl-reference/language-quality.json` endpoint when reviewing language changes.
The contract proves that the ANTLR grammar, generated parser, keyword budget,
keyword-free syntax, aliases, and learning path still fit the compact DSL goal.

Use `required` for fields that must be entered. Use `search` on fields that
should appear in generated search contracts. Use `hidden` for generated or
internal fields. Use `unique` for natural keys like invoice numbers and email
addresses.

Prefer arrow references:

```appgen
customer_id: int required -> Customer.id [many-to-one]
```

Existing DSL that uses `ref Customer.id` still parses so old projects can be
migrated, but `ref` is treated as a legacy contextual token rather than a
canonical keyword. Run the linter or quick-fix command to rewrite it to arrow
syntax before committing new source.

### Schema Design Checklist

Before generating, check that the DSL answers these questions:

- Which table is the source of truth for each business object?
- Which fields are identifiers, natural keys, required inputs, or searchable
  text?
- Which foreign keys need explicit cardinality metadata?
- Which fields are generated or internal and should be marked `hidden`?
- Which repeated field sets belong in a reusable group?
- Which derived fields should be calculated instead of stored?
- Which app targets are needed now: `web`, `pwa`, `mobile`, `desktop`, or
  `chatbot`?

### Reusable Groups And Derived Fields

Use groups when multiple tables share audit, tenancy, status, or import fields.

```appgen
AuditFields {
  created_at: datetime required
  updated_at: datetime
  tenant_id: int hidden
}

table Invoice {
  id: int pk
  ...AuditFields
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
}
```

The linter validates that derived-field expressions refer to fields available
on the same table.

## Designing Forms

Basic form sections:

```appgen
view BookForm for Book {
  Main: title, author_id;
}
```

Delphi-style component placement:

```appgen
view BookForm for Book {
  @ title TextBox 0 0 8 1;
  @ author_id Lookup 0 1 8 1;
}
```

The generated form designer can use these placements for drag/drop previews,
snap-to-grid placement, overlap detection, and property sheets.

Use section rows for readable forms and component placements when the exact
canvas layout matters. Component coordinates are grid values, not pixels, so
the same DSL can be adapted to web, mobile, and desktop renderers.

## Choosing Targets

Supported targets are `web`, `pwa`, `mobile`, `desktop`, and `chatbot`.

```appgen
app FieldOps { targets: web, pwa, mobile, desktop, chatbot }
```

`mobile` generates a Kivy starter. `desktop` generates a BeeWare starter.
`web` and `pwa` generate Flask-AppBuilder and PWA assets. `chatbot` generates
bot contracts and provider exports.

## Adding Behavior

Use `flow` for state transitions:

```appgen
flow Publish {
  draft -> published
  published -> archived
}
```

Generated workflow artifacts include transition helpers, Mermaid state diagrams,
provider-neutral FSM JSON, SCXML export for state-chart tools, graph diagnostics,
and reviewed transition proposals that can be turned back into DSL.

Use `rule` for validation and decisions:

```appgen
rule PublishPolicy for Book {
  title required "Title is required"
  status in draft, published -> review
}
```

Use `role` for generated access policies:

```appgen
role Editor {
  Book: read, create, update
}
```

Use the app option `rls` when row-level security should scope a table by a
domain-specific field name:

```appgen
app FieldOps { rls: Project.org_id; targets: web, mobile, desktop }

table Project {
  id: int pk
  org_id: string required search
  name: string required
}
```

AppGen still detects conventional tenant fields such as `tenant_id`,
`account_id`, `workspace_id`, and `organization_id`, but explicit `rls`
targets make the generated tenancy helpers and PostgreSQL policy SQL
reviewable in the DSL.

## Agentic Systems

Declare LLM providers separately from agents. This makes local and API-backed
providers explicit and keeps API keys out of source.

```appgen
llm LocalOps {
  provider: ollama
  mode: local
  endpoint: http://localhost:11434
  model: llama3
}

llm CloudOps {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}

agent InvoiceAssistant {
  provider: CloudOps
  goal: "Help users create and review invoices"
  tools: schema, forms, reports
}
```

## Natural Language Evolution

Generated apps include natural-language evolution contracts. A builder can ask
for changes such as:

```text
Create table Ticket with fields title and status, add TicketForm, add SupportBot,
and target web mobile desktop.
```

The generated change set must still be reviewed. AppGen treats natural language
as an authoring assistant, not as an unreviewed mutation path.

## Database Design Workbench

Generated apps include a Studio database workbench derived from the same DSL.
It exposes:

- table and field metadata for visual database design;
- Mermaid ERD output for diagrams;
- DBML export for external schema tools;
- SQL DDL preview for migration review;
- PonyORM entity preview for Python model comparison;
- a parameterized SQL SELECT builder with generated table/field completions and
  read-only guards;
- migration previews for proposed schema changes.

Use this workbench to round-trip between visual design and source-controlled
DSL. The DSL remains the durable source of truth.

For imported sources, check `appgen.json.source_fidelity` or
`/schema-import/fidelity.json` before regenerating. The report proves which
DBML, SQL, PonyORM, or live database source was normalized, lists the command
that generated the app, records the canonical fingerprint, and calls out
source-specific review areas before generated files are overwritten.
Use `/schema-import/release-gate.json` for the stricter proof that every source
family has validation, round-trip diff, import command, reviewed apply-plan,
fidelity, and database URL dialect evidence.

The generated Studio also manages a portfolio of generated applications through
`/studio/applications.json`. Use its create/import/open/export plans to build
new apps from DSL, DBML, SQL, PonyORM, or existing database URLs while keeping
source fidelity, linting, schema diffs, generation jobs, and quality gates in
one review flow.
Use `/studio/release-gate.json` before treating the Studio as release-ready;
it combines diagnostics, DSL linting, database workbench exports, safe SQL
guards, the parameterized query builder, generation jobs, app portfolio
management, reviewed edits, debug redaction, dependency review, and component
sharing.

## Design-System QA

Generated apps include `branding.py`, `appgen_branding.html`, and
`static/appgen-theme.css` for design-system review. The contract exposes:

- CSS custom properties for palette, spacing, density, focus, and UI states;
- viewport contracts for mobile, tablet, desktop, and wide layouts;
- component state matrices for hover, focus, disabled, invalid, selected,
  empty, and error states;
- a visual experience quality report with palette balance, WCAG contrast ratios,
  touch readiness, viewport coverage, component-state coverage, and no-overlap
  review evidence;
- a visual regression plan that lists screenshot targets and state coverage;
- accessibility audit plans for focus order, landmarks, touch targets, and
  WCAG-oriented checks.

Use the generated `/branding/visual-quality.json` endpoint as the machine gate
and `/branding/visual-regression.json` as the screenshot checklist when
validating that generated applications are polished across web, mobile, and
desktop-sized viewports.

## JHipster-Plus Readiness

Generated apps keep JHipster JDL interoperability while exposing a stricter
low-code capability scorecard in `low_code_features.py`. The scorecard requires
at least ten AppGen-only gates: visual builders, schema import, native targets,
agentic systems, natural-language evolution, ERP templates, runtime Studio
tooling, runtime assurance, application composition, and the database
IDE/workbench. Use `/low-code-features/jhipster-superset.json` to check whether
a generated app is still more capable than the JHipster baseline.
Use `/low-code-features/jhipster-superset-certification.json` for the release
gate that combines preserved JHipster overlap, AppGen-only advantage thresholds,
roadmap traceability, composition readiness, and generated artifact evidence.
Use `/low-code-features/jhipster-superiority-tiers.json` when you need the
stricter product-positioning gate: it separates preserved JHipster parity,
AppGen-only outperformance, and generated workbench routes, and it blocks
claims of superiority unless all three tiers pass.

The same module also exposes `/low-code-features/roadmap-sources.json`, which
maps `docs/ideas.md`, `docs/base_features.md`, and `docs/Lo-code features.md`
to generated capabilities and artifacts. Treat that endpoint as the source
traceability gate before claiming roadmap coverage.

## Linting Workflow

Run the linter before code generation and before committing DSL changes:

```bash
appgen --lint-dsl library.appgen
```

Treat errors as blockers. Warnings identify risky authoring patterns such as
literal API keys or legacy `ref` syntax. Suggestions identify missing design
surfaces such as views or agent declarations.

## CI Workflow

A simple CI gate can fail builds when the DSL is not valid:

```bash
appgen --lint-dsl appgen.appgen
appgen --dsl appgen.appgen --writedir build/generated-app
python -m py_compile build/generated-app/app/models.py
```

For larger projects, add generated quality checks after compilation so schema,
API, PWA, documentation, and generated test surfaces stay aligned.
