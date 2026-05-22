# Language Tutorials

This guide teaches AppGen DSL through small examples. For the full grammar, see
`docs/dsl-grammar.md`. For linter behavior, see `docs/dsl-linter.md`.

## Tutorial 1: Tables And Fields

```appgen
app Contacts { theme: sage; targets: web }

table Contact {
  id: int pk
  name: string required search
  email: email unique
  birthday: date
  notes: text
}
```

Key ideas:

- `app` declares application-level options.
- `table` declares a data model.
- `pk`, `required`, `unique`, `search`, and `hidden` are field modifiers.
- Field types include common scalar types such as `string`, `text`, `int`,
  `decimal`, `date`, `datetime`, `email`, `file`, and `image`.

## Tutorial 2: Relationships

```appgen
table Customer {
  id: int pk
  name: string required search
}

table Order {
  id: int pk
  customer_id: int required -> Customer.id [many-to-one]
  order_date: date required
}
```

Use the arrow form for references:

```appgen
customer_id: int -> Customer.id [many-to-one]
```

The linter can rewrite the older `ref Customer.id` style to the canonical arrow
syntax.

## Tutorial 3: Enums, Defaults, Arrays, And Derived Fields

```appgen
enum InvoiceStatus { draft approved sent paid void }

table Invoice {
  id: int pk
  status: InvoiceStatus default draft search
  tags: string[]
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
}
```

Derived fields use `= expression` and do not require a new keyword.

## Tutorial 4: Reusable Field Groups

```appgen
AuditFields {
  created_at: datetime
  updated_at: datetime
  tenant_id: int search
}

table Project {
  id: int pk
  ...AuditFields
  name: string required search
}
```

Bare field groups keep the language compact while avoiding repetition.

## Tutorial 5: Views And RAD-Style Form Design

```appgen
view InvoiceForm for Invoice {
  Header: invoice_number, customer_id, status
  Totals: subtotal, tax, total
  @ invoice_number TextBox 0 0 4 1
  @ customer_id Lookup 4 0 4 1
  @ status Select 8 0 3 1
  @ total CurrencyBox 8 2 3 1
}
```

Sections describe grouping. `@` placements describe component, x, y, width, and
height for visual design surfaces. Generated form-designer contracts expose
component palettes, drop validation, property inspectors, responsive layouts,
and renderer metadata.

## Tutorial 6: Workflows

```appgen
flow InvoiceLifecycle {
  draft -> approved
  approved -> sent
  sent -> paid
  sent -> void
}
```

Flows define named state transitions. Generated workbenches can use them for
workflow visualization, validation, and transition review.

## Tutorial 7: Roles And Rules

```appgen
role Accountant {
  Customer: read, create, update
  Invoice: read, create, update
}

rule InvoicePolicy for Invoice {
  invoice_number required "Invoice number is required"
  status in draft, approved, sent, paid, void
  status == sent -> review
}
```

Roles express resource permissions. Rules express field requirements,
membership constraints, and review transitions.

## Tutorial 8: App Targets

```appgen
app FieldOps { targets: web, pwa, mobile, desktop, chatbot }
```

Targets control generated output:

- `web` writes Flask-AppBuilder surfaces.
- `pwa` writes manifest and service-worker assets.
- `mobile` writes a Kivy starter and mobile contracts.
- `desktop` writes a BeeWare starter and desktop contracts.
- `chatbot` writes chatbot provider exports.

Run:

```console
appgen --target-release-audit
```

## Tutorial 9: LLM Providers And Agents

```appgen
llm LocalModel {
  provider: ollama
  mode: local
  model: llama3
  endpoint: "http://localhost:11434"
}

llm ApiModel {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}

agent SupportAgent {
  provider: LocalModel
  goal: "Triage support tickets and prepare reviewed updates"
  tools: schema, forms, chatbots, reports
  memory: project
  max_steps: 6
}
```

API providers reference environment variable names. Do not put literal secrets
in DSL files.

Run:

```console
appgen --agentic-release-audit
```

## Tutorial 10: Full Invoicing App

```appgen
app InvoiceDesk { theme: sage; targets: web, pwa, mobile, desktop, chatbot }

enum InvoiceStatus { draft approved sent paid void }

table Customer {
  id: int pk
  name: string required search
  email: email unique
}

table Invoice {
  id: int pk
  invoice_number: string required unique search
  customer_id: int required -> Customer.id [many-to-one]
  status: InvoiceStatus default draft search
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
}

table InvoiceLine {
  id: int pk
  invoice_id: int required -> Invoice.id [many-to-one]
  description: string required
  quantity: decimal default 1
  unit_price: decimal default 0
  line_total: decimal = quantity * unit_price
}

view InvoiceForm for Invoice {
  Header: invoice_number, customer_id, status
  Totals: subtotal, tax, total
  @ invoice_number TextBox 0 0 4 1
  @ customer_id Lookup 4 0 4 1
  @ status Select 8 0 3 1
}

flow InvoiceLifecycle {
  draft -> approved
  approved -> sent
  sent -> paid
}

role Accountant {
  Customer: read, create, update
  Invoice: read, create, update
  InvoiceLine: read, create, update
}
```

Validate and generate:

```console
appgen --lint-dsl invoice.appgen
appgen --dsl-authoring-gate invoice.appgen
appgen --dsl invoice.appgen --writedir generated/invoice/app
```

## Linter Workflow

Use the linter before generation:

```console
appgen --lint-dsl app.appgen
```

Apply safe fixes:

```console
appgen --fix-dsl app.appgen
```

Format source:

```console
appgen --format-dsl app.appgen
```

Run the full language release checks:

```console
appgen --dsl-antlr-report
appgen --dsl-release-audit
```
