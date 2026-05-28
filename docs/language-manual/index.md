# AppGen-X Language Manual

This manual is the compact reference for the AppGen-X language. It describes
what each construct means, how the linter validates it, and how the generator
uses it.

Use the grammar reference for exact ANTLR productions and the tutorials for
step-by-step examples.

## Command-Line Entry Points

The installed console command is currently `appgen`.

```console
appgen --help
appgen --lint-dsl app.appgen
appgen --dsl app.appgen --writedir generated/app
```

The source-tree equivalent is:

```console
PYTHONPATH=src ./.venv/bin/python -m pyAppGen --help
```

## Source Structure

A source file has an optional `app` declaration followed by any number of
top-level elements.

```appgen
app Name { targets: web, mobile, desktop }

table Customer { id: int pk; name: string required }
view CustomerForm for Customer { Main: name }
```

Comments may use `#`, `//`, or `/* ... */`.

## Canonical Keywords

The language keeps a compact canonical keyword budget:

`app`, `table`, `enum`, `view`, `for`, `flow`, `role`, `rule`, `pbc`,
`composition`, `audit`, `deploy`, `version`, `operation`, `security`, `api`,
`event`, `job`, `report`, `menu`, `component`, `package`, `test`, `llm`,
`agent`, `pk`, `required`, `unique`, `hidden`, `search`, `default`, and `in`.

Other domain words are contextual inside blocks. This keeps the language
readable without turning every business term into a global reserved word.

## Application Options

```appgen
app FieldOps {
  targets: web, pwa, mobile, desktop, chatbot
  theme: sage
  rls: WorkOrder.tenant_id
}
```

Supported targets are `web`, `pwa`, `mobile`, `desktop`, and `chatbot`.
Unknown targets are errors.

## Tables

```appgen
table Invoice {
  id: int pk
  invoice_number: string required unique search
  customer_id: int -> Customer.id [many-to-one]
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
}
```

Fields support:

- scalar and custom type names;
- `type[]` arrays;
- optional length such as `string(120)`;
- `pk`, `required`, `unique`, `hidden`, `search`;
- `default literal`;
- arrow references;
- derived expressions with `=`.

If no primary key is declared, AppGen-X adds an `id: int pk` field in the
canonical schema.

## Table Directives

Table directives express indexes, keys, checks, and lookup contracts.

```appgen
table Invoice {
  id: int pk
  customer_id: int -> Customer.id
  lookup customer_name (customer.name)
  index invoice_search (customer_id, invoice_number)
  unique invoice_number_key (invoice_number)
  fk invoice_customer_fk (customer_id) -> Customer.id
}
```

Directive values must reference existing fields, calculated fields, or valid
lookup paths from the table. Directive targets must resolve to declared
`Table.field` references.

## Relationships

Use arrows for foreign keys.

```appgen
customer_id: int required -> Customer.id [many-to-one]
```

External relationship declarations are also valid:

```appgen
Invoice.customer_id -> Customer.id [many-to-one]
```

Supported cardinalities are `many-to-one`, `one-to-one`, `one-to-many`, and
`many-to-many`.

## Field Groups

Reusable field groups are bare named blocks.

```appgen
AuditFields {
  created_at: datetime
  updated_at: datetime
}

table Project {
  id: int pk
  ...AuditFields
}
```

Group cycles and duplicate fields are rejected.

## Enums

```appgen
enum InvoiceStatus { draft reviewed approved paid void }

table Invoice {
  status: InvoiceStatus default draft search
}
```

## Views And Components

Views are database-backed forms or screens.

```appgen
view InvoiceForm for Invoice {
  Header: invoice_number, customer.name
  Totals: subtotal, tax, total
  @ invoice_number TextBox 0 0 4 1
  @ customer.name Lookup 4 0 4 1
  on Save -> SubmitInvoice
}
```

View fields and component bindings must resolve to:

- fields on the view table;
- calculated fields on the view table;
- valid relationship lookup paths such as `customer.name`.

Handlers use:

```appgen
on EventName -> TargetName
```

Targets must resolve to a flow, operation, enterprise contract, or agent.

## Workflows

Simple workflows are state transitions.

```appgen
flow TicketLifecycle {
  open -> triaged
  triaged -> resolved
}
```

Richer workflows use directives:

```appgen
flow TicketLifecycle {
  participant SupportLead
  open -> triaged
  human Review assigned SupportLead -> approved
  timer triaged "P1D" -> escalated
  compensate approved -> ReopenTicket
}
```

Common directive verbs include `participant`, `human`, `timer`, `compensate`,
`rollout`, and `skill`. They remain contextual words.

## Roles, Security, And Audit

```appgen
role SupportUser {
  Ticket: read, create, update
}

security TenantPolicy {
  Ticket: read, create, update
  rbac: enabled
  tenant: organization_id
}

audit ReleaseAudit {
  evidence: migrations, tests, security
  gate: release
}
```

`role` blocks describe resource permissions. `security` blocks describe
application policy. `audit` blocks describe evidence and release gates.

## Rules

```appgen
rule TicketPolicy for Ticket {
  title required "Title is required"
  status in open, triaged, resolved
  status == resolved and exists(assigned_to) -> NotifyCustomer
  closed_at is null
}
```

Supported expression features:

- `==`, `!=`, `>=`, `<=`, `>`, `<`, and `in`;
- `and`, `or`, `not`;
- `exists(path)`;
- `is null` and `is not null`;
- parentheses.

Rule fields must resolve against the declared table.

## LLM Providers

```appgen
llm LocalModel {
  provider: ollama
  mode: local
  model: qwen3_4b
  endpoint: "http://localhost:11434"
}

llm CloudModel {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}
```

`api_key` values should be environment variable names. Literal secrets are
lint warnings.

## Agents

```appgen
agent SupportAgent {
  provider: LocalModel
  goal: "Triage support tickets"
  tools: schema, forms, reports
  memory: project
  max_steps: 6
  skill triage TicketCreated -> TicketLifecycle
  Ticket: read, update
  on Escalate -> NotifySupportLead
}
```

Agents can declare:

- provider and model behavior;
- goals, tools, memory, and step limits;
- skills through arrow statements;
- resource permissions;
- handlers.

## PBCs And Composition

```appgen
pbc ticketing {
  label: "Ticketing"
  mesh: customer_experience
  owns: Ticket, TicketComment
  emits: TicketCreated
  consumes: CustomerUpdated
}

composition ServiceDesk {
  include pbc ticketing version "1.x"
  require datastore owned_per_pbc
  require eventing appgen_x_outbox
  expose workbench all
  connect ticketing emits TicketCreated -> ticketing consumes CustomerUpdated
}
```

PBC blocks describe bounded business capabilities. Composition blocks select
and connect capabilities into applications.

## Operations And Enterprise Contracts

```appgen
operation ResolveTicket {
  open -> triaged
  triaged -> resolved
  owner: support_ops
}

api TicketApi {
  GET "/tickets" -> ResolveTicket
  auth: Ticket.read
}

event TicketResolved {
  publish TicketResolved -> ResolveTicket
  topic: pbc.ticketing.events
}

job TicketEscalation {
  hourly -> ResolveTicket
  retry: 3
}

report TicketAging {
  source: Ticket
  export: csv, pdf
}

menu MainMenu {
  on OpenTickets -> ResolveTicket
}

component StatusBadge {
  on Click -> ResolveTicket
  prop: status
}

package ServiceDeskRelease {
  targets: web, mobile, desktop
  channel: stable
}

test TicketSmoke {
  run happy_path -> ResolveTicket
  assert: ok
}
```

Enterprise contract blocks expose generated surfaces for APIs, events, jobs,
reports, menus, reusable components, packages, and tests.

## Deployment

```appgen
deploy Production {
  runtime: kubernetes
  mesh: mtls
  unit ticketing as microservice
  unit ResolveTicket as process
  unit TicketEscalation as worker
  scale ticketing min 2 max 10
  health ticketing "/healthz"
  check ticketing readiness "/readyz"
  resource ticketing cpu "500m"
  env ticketing DATABASE_URL
  secret ticketing OPENAI_API_KEY
}
```

Deployment targets must resolve to declared PBCs, flows, operations, enterprise
contracts, or agents. Scale ranges must be valid.

## Formatting, Linting, And Release Gates

```console
appgen --format-dsl app.appgen
appgen --lint-dsl app.appgen
appgen --dsl-authoring-gate app.appgen
appgen --dsl-antlr-report
appgen --dsl-release-audit
```

Use these commands before generation and before committing language changes.

## Compatibility And Aliases

Older `ref Customer.id` references are accepted but linted to arrow syntax.
Beginner aliases normalize before parsing:

- `entity` and `model` become `table`;
- `form` and `screen` become `view`;
- `workflow` becomes `flow`;
- `searchable` becomes `search`;
- `hide` becomes `hidden`.

Committed DSL should use the canonical forms.
