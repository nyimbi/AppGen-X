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

## Modeling Guidance

Use one table per business object. Use explicit `id: int pk` fields when you
want stable identifiers, or let AppGen add one when omitted.

Use `required` for fields that must be entered. Use `search` on fields that
should appear in generated search contracts. Use `hidden` for generated or
internal fields. Use `unique` for natural keys like invoice numbers and email
addresses.

Prefer arrow references:

```appgen
customer_id: int required -> Customer.id [many-to-one]
```

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
- migration previews for proposed schema changes.

Use this workbench to round-trip between visual design and source-controlled
DSL. The DSL remains the durable source of truth.

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
