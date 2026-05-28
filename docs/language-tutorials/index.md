# AppGen-X Language Tutorials

These tutorials teach the AppGen-X language by building small, valid
applications. Use them when you want examples before reading the full manual.
For exact syntax, see the language manual and grammar reference.

The command-line tool is currently `appgen`:

```console
appgen --lint-dsl app.appgen
appgen --dsl app.appgen --writedir generated/app
```

## 1. Model Tables

Start with an application and one table.

```appgen
app Contacts { targets: web, mobile, desktop }

table Contact {
  id: int pk
  name: string required search
  email: email unique
  birthday: date
  notes: text
}
```

Run:

```console
appgen --lint-dsl contacts.appgen
```

The linter checks syntax, unknown targets, duplicate names, invalid references,
and authoring style.

## 2. Add Relationships And Lookups

Use arrow references for foreign keys.

```appgen
table Customer {
  id: int pk
  name: string required search
}

table Invoice {
  id: int pk
  customer_id: int required -> Customer.id [many-to-one]
  invoice_number: string required unique search
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
  lookup customer_name (customer.name)
}
```

The lookup path `customer.name` is valid because `customer_id` references
`Customer.id`. The linter rejects paths that do not resolve through declared
columns or calculated fields.

## 3. Design Forms With Components

Sections describe readable form groups. `@` placements describe component,
field, x, y, width, and height for a visual design surface.

```appgen
view InvoiceForm for Invoice {
  Header: invoice_number, customer.name
  Totals: subtotal, tax, total
  @ invoice_number TextBox 0 0 4 1
  @ customer.name Lookup 4 0 4 1
  @ total CurrencyBox 8 2 3 1
  on Save -> SubmitInvoice
}
```

Handlers use `on Event -> OperationOrFlow`. Targets must resolve to a declared
flow, operation, enterprise contract, or agent.

## 4. Add Workflow And Rules

Flows can be simple state machines or richer workflow descriptions.

```appgen
flow SubmitInvoice {
  participant FinanceOps
  draft -> reviewed
  human Review assigned FinanceOps -> approved
  timer reviewed "P2D" -> escalated
  compensate approved -> ReverseInvoice
}

rule InvoicePolicy for Invoice {
  invoice_number required "Invoice number is required"
  status in draft, reviewed, approved, paid
  status == approved and total > 0 -> SubmitInvoice
}
```

Rules support `and`, `or`, `not`, `exists(...)`, comparisons, `in`, and null
checks.

## 5. Add Roles And Security

```appgen
role Accountant {
  Customer: read, create, update
  Invoice: read, create, update
}

security TenantPolicy {
  Invoice: read, create, update
  rbac: enabled
  tenant: organization_id
}
```

Use `role` for user-facing permissions and `security` for application-wide
policy contracts.

## 6. Add Local And API LLMs

```appgen
llm LocalModel {
  provider: ollama
  mode: local
  model: qwen3_4b
  endpoint: "http://localhost:11434"
}

llm ApiModel {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}
```

API keys should be environment variable names, not literal secrets.

## 7. Add Agents

```appgen
agent FinanceAssistant {
  provider: LocalModel
  goal: "Help finance users review invoices and close exceptions"
  tools: schema, forms, reports
  memory: project
  max_steps: 6
  skill reconcile InvoiceApproved -> SubmitInvoice
  Invoice: read, update
  on Alert -> SubmitInvoice
}
```

Agents can declare providers, goals, tools, memory, skills, permissions, and
handler wiring.

## 8. Compose PBCs

Packaged Business Capabilities are selectable bounded contexts.

```appgen
pbc invoicing {
  label: "Invoicing"
  mesh: finops
  owns: Invoice, InvoiceLine
  emits: InvoiceApproved
  consumes: CustomerUpdated
}

composition FinanceSuite {
  include pbc invoicing version "1.x"
  require datastore owned_per_pbc
  require eventing appgen_x_outbox
  expose workbench all
  connect invoicing emits InvoiceApproved -> invoicing consumes CustomerUpdated
}
```

Generate starter DSL from the package catalog:

```console
appgen --pbc-catalog
appgen --pbc-dsl gl_core --pbc-dsl ap_automation
```

## 9. Add APIs, Events, Jobs, Reports, Menus, And Packages

```appgen
operation SubmitInvoice {
  draft -> reviewed
  reviewed -> approved
  owner: finance_ops
}

api InvoiceApi {
  GET "/invoices" -> SubmitInvoice
  auth: Invoice.read
}

event InvoiceApproved {
  publish InvoiceApproved -> SubmitInvoice
  topic: pbc.invoicing.events
}

job NightlyInvoiceClose {
  daily -> SubmitInvoice
  retry: 3
}

report InvoiceAging {
  source: Invoice
  export: csv, pdf
}

menu MainMenu {
  on OpenInvoices -> SubmitInvoice
}

package FinanceRelease {
  targets: web, mobile, desktop
  channel: stable
}
```

Enterprise contract targets are validated so broken handler and operation
references are caught before generation.

## 10. Model Deployment

```appgen
deploy Production {
  runtime: kubernetes
  mesh: mtls
  unit invoicing as microservice
  unit SubmitInvoice as process
  unit NightlyInvoiceClose as worker
  scale invoicing min 2 max 10
  health invoicing "/healthz"
  check invoicing readiness "/readyz"
  resource invoicing cpu "500m"
  env invoicing DATABASE_URL
  secret invoicing OPENAI_API_KEY
}
```

Supported deployment patterns include `microservice`, `process`, `worker`,
`job`, `function`, `module`, `sidecar`, `embedded`, and `monolith`.

## 11. Validate And Generate

```console
appgen --format-dsl finance.appgen
appgen --lint-dsl finance.appgen
appgen --dsl-authoring-gate finance.appgen
appgen --dsl finance.appgen --writedir generated/finance/app
```

For package-level language readiness:

```console
appgen --dsl-antlr-report
appgen --dsl-release-audit
```

## 12. Practice Project

Build a small service desk application with:

- `Customer`, `Ticket`, and `TicketComment` tables.
- A `TicketForm` with a customer lookup path.
- A `TicketLifecycle` workflow with human review and escalation timer.
- A `SupportAgent` using a local LLM.
- An `api`, `event`, `job`, `report`, `menu`, and `package` block.
- A `deploy` block with web, worker, health, and secret bindings.

Run the linter after each section. Treat every natural-language or visual edit
as a proposal that must regenerate valid AppGen-X DSL.
