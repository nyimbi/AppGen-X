# AppGen-X Language Manual

This is the complete working manual for the AppGen-X language. It explains the syntax, semantic rules, keywords, authoring conventions, generator expectations, and common mistakes for enterprise application generation. The grammar source of truth is `lang/appgen.g4`; this manual explains how to use that grammar to describe data models, forms, workflows, PBC composition, APIs, events, operations, security, deployment, packaging, tests, and agentic systems.

The language is intentionally small at the parser layer and broad at the contract layer. A few structural keywords define stable shapes, while contextual directives inside blocks let teams model real enterprise domains without waiting for a new parser rule for every industry term.

## Command-Line Entry Points

The installed command is `appgen`.

```console
appgen --help
appgen --lint-dsl app.appgen
appgen --dsl app.appgen --writedir generated/app
```

The source-tree equivalent is useful during platform development:

```console
PYTHONPATH=src ./.venv/bin/python -m pyAppGen --help
```

The command-line lifecycle is usually: write a DSL file, lint it, generate into a clean output directory, run generated tests, then package the target application or capability.

## File Structure

An AppGen-X file has an optional application declaration followed by zero or more top-level elements.

```appgen
app FieldOps { targets: web, mobile, desktop }

table Customer { id: int pk; name: string required search }
view CustomerForm for Customer { Main: name }
```

Top-level elements may appear in any order. The semantic pass resolves references after parsing, so a view may reference a table declared later in the same file. Keep related elements close anyway; it improves review quality and reduces accidental name collisions.

## Comments, Whitespace, And Style

Line comments use `#` or `//`. Block comments use `/* ... */`. Whitespace is not significant. Semicolons are optional in most places, but the project style recommends one statement per line and semicolons only when a dense one-line block is clearer.

```appgen
# preferred for short notes
// also valid
/* valid for generated or migrated annotations */
```

Identifiers start with a letter or underscore and may contain letters, digits, and underscores. String literals may use single or double quotes. Booleans are `true` and `false`. Numbers are integer or decimal literals.

## Complete Keyword Index

The following sections describe every parser keyword and the rules around it.

### `app`

Declares the application boundary and top-level generation options such as targets, theme, tenancy, and product intent.

```appgen
app FieldOps { targets: web, mobile, desktop
  theme: sage
  rls: WorkOrder.tenant_id
}
```

Gotchas: `app` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `app_code`, `app_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `table`

Declares a durable database-backed entity. Tables become migrations, models, APIs, admin screens, form bindings, seed hooks, and generated tests.

```appgen
table Customer {
  id: int pk
  name: string required search
  email: email unique
}
```

Gotchas: `table` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `table_code`, `table_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `enum`

Declares a closed vocabulary that can be used as a field type, default value set, rule operand, or UI selector source.

```appgen
enum InvoiceStatus { draft reviewed approved paid void }
```

Gotchas: `enum` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `enum_code`, `enum_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `view`

Declares a database-backed screen, form, list, wizard page, dashboard panel, or component design surface for a table.

```appgen
view InvoiceForm for Invoice {
  Header: invoice_number, customer.name
  @ invoice_number TextBox 0 0 4 1
  on Save -> SubmitInvoice
}
```

Gotchas: `view` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `view_code`, `view_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `for`

Binds a construct to its subject. Views and rules use it to identify the table they validate or render.

```appgen
rule InvoicePolicy for Invoice {
  total > 0
}
```

Gotchas: `for` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `for_code`, `for_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `flow`

Declares a workflow, state machine, or process route. It can include state transitions, participants, timers, human work, and compensation.

```appgen
flow SubmitInvoice {
  draft -> reviewed
  human Review assigned FinanceOps -> approved
  timer reviewed "P2D" -> escalated
}
```

Gotchas: `flow` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `flow_code`, `flow_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `role`

Declares a role and its permissions. Roles feed generated access-control policies and default navigation visibility.

```appgen
role Accountant {
  Invoice: read, create, update
  Payment: read
}
```

Gotchas: `role` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `role_code`, `role_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `rule`

Declares validation, policy, routing, or automation rules for a table or domain subject.

```appgen
rule InvoicePolicy for Invoice {
  invoice_number required "Invoice number is required"
  status in draft, reviewed, approved, paid
}
```

Gotchas: `rule` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `rule_code`, `rule_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `pbc`

Declares a Packaged Business Capability: a bounded business capability with contracts, datastore ownership, events, operations, permissions, and metadata.

```appgen
pbc AccountsReceivable {
  domain: finance
  owns: Invoice, Payment
  emits InvoiceIssued -> InvoiceIssuedEvent
}
```

Gotchas: `pbc` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `pbc_code`, `pbc_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `composition`

Declares how PBCs are assembled into an application. It records included versions, required capabilities, exposed surfaces, and event/API connections.

```appgen
composition FinanceSuite {
  include pbc AccountsReceivable version 1.2.0
  require database postgresql
  connect AccountsReceivable event InvoiceIssued -> GeneralLedger command PostJournal
}
```

Gotchas: `composition` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `composition_code`, `composition_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `audit`

Declares audit, trace, retention, evidence, and compliance requirements.

```appgen
audit FinanceAudit {
  subject: Invoice, Payment
  retention: P7Y
  immutable: true
}
```

Gotchas: `audit` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `audit_code`, `audit_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `deploy`

Declares deployment topology, units, scaling, health checks, resources, environment bindings, and operational checks.

```appgen
deploy Production {
  unit ar as service
  scale ar min 2 max 10
  health ar "/health"
  resource ar cpu 500m
  env ar DATABASE_URL
}
```

Gotchas: `deploy` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `deploy_code`, `deploy_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `version`

Declares release identity, compatibility, migration policy, and evidence expected for generated packages.

```appgen
version Release_2026_05 {
  semver: 1.4.0
  compatibility: backward
  migration: online
}
```

Gotchas: `version` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `version_code`, `version_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `operation`

Declares an executable command, orchestration, use case, or handler target.

```appgen
operation SubmitInvoice {
  validate -> PostInvoice
  emits: InvoiceSubmitted
}
```

Gotchas: `operation` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `operation_code`, `operation_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `security`

Declares security posture: RBAC, tenancy, secrets, row filters, data classification, and policy hooks.

```appgen
security TenantPolicy {
  rbac: enabled
  tenant: organization_id
  Invoice: read, create, update
}
```

Gotchas: `security` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `security_code`, `security_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `api`

Declares an API contract that generated applications expose or consume.

```appgen
api InvoiceApi {
  endpoint: "/api/invoices"
  method: GET, POST
  read Invoice -> InvoiceDto
}
```

Gotchas: `api` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `api_code`, `api_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `event`

Declares an event contract for asynchronous integration and PBC composition.

```appgen
event InvoiceIssuedEvent {
  payload: Invoice
  key: Invoice.id
  version: 1
}
```

Gotchas: `event` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `event_code`, `event_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `job`

Declares scheduled or background work.

```appgen
job ClosePeriod {
  schedule: "0 2 1 * *"
  run CloseAccountingPeriod -> PeriodClosed
}
```

Gotchas: `job` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `job_code`, `job_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `report`

Declares a generated report, its data source, filters, grouping, and export surfaces.

```appgen
report AgingSummary {
  source: Invoice
  filter: status != paid
  export: pdf, xlsx
}
```

Gotchas: `report` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `report_code`, `report_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `menu`

Declares menus, commands, right-click actions, and navigation contributions.

```appgen
menu InvoiceMenu {
  item IssueInvoice -> SubmitInvoice
  context InvoiceRow -> OpenInvoice
}
```

Gotchas: `menu` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `menu_code`, `menu_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `component`

Declares a reusable UI component contract available to the visual design surface and generators.

```appgen
component MoneyInput {
  property: value decimal
  event Changed -> RecalculateTotals
}
```

Gotchas: `component` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `component_code`, `component_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `package`

Declares packaging outputs and distribution metadata for generated apps or PBCs.

```appgen
package DesktopBundle {
  target: desktop
  format: installer
  signing: required
}
```

Gotchas: `package` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `package_code`, `package_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `test`

Declares acceptance, contract, workflow, generator, or smoke tests to emit with the application.

```appgen
test InvoiceAcceptance {
  scenario: issue_invoice
  expects: InvoiceIssuedEvent
}
```

Gotchas: `test` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `test_code`, `test_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `llm`

Declares a local or hosted language model endpoint available to agents and natural-language application evolution.

```appgen
llm LocalPlanner {
  provider: ollama
  model: qwen3.5-4b
  endpoint: "http://localhost:11434"
}
```

Gotchas: `llm` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `llm_code`, `llm_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `agent`

Declares an agentic worker, chatbot, copilot, integration actor, or automation assistant.

```appgen
agent InvoiceAssistant {
  uses: LocalPlanner
  skill classify_invoice -> ClassifyInvoice
  permission Invoice: read, update
}
```

Gotchas: `agent` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `agent_code`, `agent_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `pk`

Marks a field as a primary key.

```appgen
id: int pk
```

Gotchas: `pk` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `pk_code`, `pk_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `required`

Marks a field as mandatory or a rule assertion as required.

```appgen
invoice_number: string required
```

Gotchas: `required` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `required_code`, `required_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `unique`

Marks a field or table directive as uniqueness constrained.

```appgen
email: email unique
```

Gotchas: `unique` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `unique_code`, `unique_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `hidden`

Marks a field as not shown by default in generated forms and lists.

```appgen
internal_notes: text hidden
```

Gotchas: `hidden` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `hidden_code`, `hidden_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `search`

Marks a field as included in generated search indexes and default list filters.

```appgen
name: string required search
```

Gotchas: `search` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `search_code`, `search_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `default`

Assigns a default literal value to a field.

```appgen
status: InvoiceStatus default draft
```

Gotchas: `default` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `default_code`, `default_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

### `in`

Checks membership in a rule expression.

```appgen
status in draft, approved, paid
```

Gotchas: `in` is reserved where the grammar expects a keyword. If the same word is needed as a business label, use a different identifier such as `in_code`, `in_type`, or a string literal in metadata. Keep keyword use structural; place domain-specific detail in named directives inside the relevant block.

## Grammar Map

This section summarizes the grammar in authoring terms.

```antlr
schema      : appDecl? element* EOF;
element     : tableDecl | groupDecl | enumDecl | relationDecl | viewDecl
            | flowDecl | roleDecl | ruleDecl | llmDecl | agentDecl
            | pbcDecl | compositionDecl | auditDecl | deploymentDecl
            | versionDecl | operationDecl | securityDecl | apiDecl
            | eventDecl | jobDecl | reportDecl | menuDecl | componentDecl
            | packageDecl | testDecl;
```

The broad `element` list is the reason the language can describe a whole enterprise platform rather than only database tables. Tables, views, flows, and roles define the core application. PBCs and composition define composable enterprise assembly. APIs, events, jobs, reports, menus, components, packages, and tests define generated surfaces around that core. Audit, version, operation, security, and deploy blocks provide governance and runtime intent.

## Application Declaration

```appgen
app EnterpriseOps {
  targets: web, pwa, mobile, desktop, chatbot
  theme: graphite
  rls: TenantScoped.tenant_id
  database: postgresql
}
```

`targets` controls generated application families. Supported target names are `web`, `pwa`, `mobile`, `desktop`, and `chatbot`. The backend database should be `postgresql`, `mysql`, or a compatible open-source alternative declared by platform policy. Use one backend family per generated application to avoid multiplying migration and query behavior.

Gotchas:

- Unknown targets are lint errors.
- App options are metadata until a generator consumes them; do not assume an option changes behavior unless the generator contract documents it.
- Keep secrets out of app options. Use deployment bindings for environment variables and secret names.

## Table Syntax

```appgen
table Invoice {
  id: int pk
  invoice_number: string(40) required unique search
  customer_id: int required -> Customer.id [many-to-one]
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
  lookup customer_name (customer.name)
  index invoice_search (customer_id, invoice_number)
  unique invoice_number_key (invoice_number)
  fk invoice_customer_fk (customer_id) -> Customer.id
}
```

A field is `name: type`, optionally followed by a derived expression and modifiers. Types are identifiers with optional length, such as `string(120)`, and optional array suffix, such as `string[]`. AppGen-X does not force all domain types into primitive parser tokens; generators map known types and can reject unknown types during semantic validation.

Derived expressions use `=` and may reference fields, literals, and arithmetic operators. A derived field is calculated and therefore valid for form binding, lookup display, reports, and rules, but should not be treated as user-editable unless a generator explicitly supports reverse calculation.

## Field Modifiers

```appgen
id: int pk
name: string required search
email: email unique
status: InvoiceStatus default draft
internal_hash: string hidden
customer_id: int -> Customer.id [many-to-one]
```

Modifiers are order-insensitive. The semantic pass enforces sensible combinations. For example, a primary key should be unique, a required field should have UI validation, and a relationship target must resolve to an existing `Table.field`.

## Relationships And Lookup Paths

A relationship can be inline on a field or external as a relation declaration.

```appgen
customer_id: int required -> Customer.id [many-to-one]
Invoice.customer_id -> Customer.id [many-to-one]
```

Lookup paths use lower-case relationship aliases inferred from foreign keys. A field named `customer_id` that points to `Customer.id` exposes `customer.name`, `customer.email`, and other fields on the target table. Multi-hop paths are allowed when every hop is declared and unambiguous.

```appgen
view PaymentForm for Payment {
  Main: invoice.customer.name, invoice.customer.account_manager.name
}
```

For a chain such as A -> B -> C -> D, every hop must be backed by a declared foreign key or calculated relationship. The linter should reject `a.b.c.d` if any intermediate segment cannot be resolved. Generated lookup controls should be produced automatically for database-backed relationship fields, with display labels based on search fields, configured lookup directives, or stable fallback fields such as `name` and `code`.

Gotchas:

- `customer.name` is valid only if the current table has a relationship alias named `customer`.
- Do not bind forms to raw columns that do not exist. Use calculated fields or lookup directives when the display value is derived.
- Avoid ambiguous duplicate foreign keys without explicit lookup directives.

## Table Directives

Table directives are contextual statements inside a table. They support indexes, unique keys, checks, foreign-key naming, display lookup contracts, and generator-specific database hints.

```appgen
table Account {
  id: int pk
  parent_id: int -> Account.id [many-to-one]
  code: string required unique search
  name: string required search
  lookup display (code, name)
  check valid_code (code != null)
  index account_parent_idx (parent_id)
}
```

Directive values may be rule expressions or agentic values. When a directive references fields, the linter should verify that each field exists on the table, is calculated on the table, or is reachable through a declared relationship path.

## Groups And Spreads

Bare named blocks define reusable field groups.

```appgen
AuditFields {
  created_at: datetime
  created_by: int -> User.id [many-to-one]
  updated_at: datetime
}

table Customer {
  id: int pk
  ...AuditFields
}
```

Groups are copied into the target table during normalization. Duplicate fields and cyclic spreads are errors.

## Views, Forms, Components, And Handlers

A view has a name, a table subject, and view items.

```appgen
view InvoiceEditor for Invoice {
  Header: invoice_number, customer.name, status
  Lines: subtotal, tax, total
  @ invoice_number TextBox 0 0 4 1
  @ customer.name Lookup 4 0 4 1
  @ status ComboBox 0 1 3 1
  @ total CurrencyBox 8 2 3 1
  on Save -> SubmitInvoice
  on Cancel -> CloseInvoice
}
```

Section lines group fields for generated layouts. `@` placements are explicit design-surface placements using `field component x y width height`. A component binding must resolve to an existing field, calculated field, or valid lookup path. Handler declarations connect visual events to operations, flows, agents, or contract targets.

Handler rules:

- `on Save -> SubmitInvoice` is the canonical event form.
- `ButtonName Click -> OperationName` is accepted for component-specific wiring.
- Handlers may call other operations if those operations are declared and accessible by generated class/component architecture.
- Cross-handler calls should go through named operations rather than directly coupling one visual control to another visual control.

Gotchas:

- Keep business behavior in `operation`, `flow`, or `agent` blocks. Keep views focused on binding, layout, and event wiring.
- Context menus belong in `menu` blocks and may target the same operations as buttons.
- Splash screens and startup behavior should be modeled through `component`, `menu`, `package`, and `operation` contracts rather than hidden generator flags.

## Rules

Rules can declare required fields and boolean expressions.

```appgen
rule InvoicePolicy for Invoice {
  invoice_number required "Invoice number is required"
  total > 0
  status in draft, reviewed, approved, paid
  not exists(invoice_number) or status != approved -> BlockApproval
  customer_id is not null
}
```

Supported logical operators are `and`, `or`, and `not`. Supported predicates include equality, inequality, greater/less comparisons, `in`, `exists(...)`, and `is null` / `is not null` checks. Parentheses group expressions.

Rule gotchas:

- Use `==` for equality in expressions, not `=`. The single equals sign is for calculated fields.
- Use `field required "message"` for required-message rules.
- Rule targets after `->` should be declared operations, flows, events, or policy actions.
- Keep long policy sets split by subject. A giant all-purpose rule block is difficult to test.

## Workflows And Operations

Flows express lifecycle transitions. Operations express executable use cases and handler targets.

```appgen
flow PurchaseOrderApproval {
  participant Requester
  participant Buyer
  draft -> submitted
  human BuyerReview assigned Buyer -> approved
  timer submitted "P3D" -> escalated
  compensate approved -> ReverseCommitment
}

operation ApprovePurchaseOrder {
  validate -> PostCommitment
  emits: PurchaseOrderApproved
  audit: required
}
```

The grammar allows contextual directives inside flows and operations so workflow engines can add timers, human tasks, retry policies, compensation, participants, and evidence requirements without grammar churn.

## PBCs And Composition

```appgen
pbc AccountsReceivable {
  domain: finance
  owns: Customer, Invoice, Payment
  exposes InvoiceApi -> public
  emits InvoiceIssued -> InvoiceIssuedEvent
  consumes OrderShipped -> GenerateInvoice
  datastore: postgresql
}

composition EnterpriseFinance {
  include pbc AccountsReceivable version 1.2.0
  include pbc GeneralLedger version 2.0.0
  require database postgresql
  expose api InvoiceApi
  connect AccountsReceivable event InvoiceIssued -> GeneralLedger command PostJournal
}
```

A PBC should be independently buildable, testable, deployable, and self-registering. A composition should not reach into another PBC's private tables. Use APIs, events, commands, and published read models.

Deployment patterns are expressed in `deploy` blocks. A PBC may be generated into the same process, a modular monolith, a separate service, a worker, a scheduled job, or an edge unit. The language supports these patterns through deployment units and directives; the platform policy decides which topologies are allowed for a given generator.

## APIs, Events, Jobs, Reports, Menus, Components, Packages, Tests

These blocks share the contract-item pattern: handlers, arrows, directives, options, and permissions.

```appgen
api CustomerApi {
  endpoint: "/api/customers"
  Customer read -> CustomerDto
}

event CustomerCreated {
  payload: Customer
  key: Customer.id
}

job SyncBankStatements {
  schedule: "0 */4 * * *"
  run FetchStatements -> StatementsImported
}

menu CustomerContext {
  context CustomerRow -> OpenCustomer
  item MergeCustomer -> MergeCustomerOperation
}

package MobileBundle {
  target: mobile
  format: signed_archive
}

test CustomerSmoke {
  scenario: create_customer
  expects: CustomerCreated
}
```

Use these blocks to make generated output explicit. If a generated app needs a right-click menu, put it in `menu`. If a generated app needs a mobile package, put it in `package`. If a PBC emits an event, put it in `event` and reference it from the PBC.

## LLMs And Agents

```appgen
llm LocalCoder {
  provider: ollama
  model: qwen3.5-4b
  endpoint: "http://localhost:11434"
}

llm HostedPlanner {
  provider: openai_compatible
  model: frontier-coder
  api_key_env: APPGEN_LLM_API_KEY
}

agent AppBuilder {
  uses: LocalCoder, HostedPlanner
  skill create_table -> CreateTableOperation
  skill design_form -> DesignFormOperation
  permission Customer: read, create, update
}
```

Agent blocks define what an agent can do. LLM blocks define where the reasoning or code-generation backend lives. Keep API keys in environment variables and deployment secret bindings. For token-efficient generation, prefer small, explicit DSL changes over large natural-language prompts. Natural language should compile into tables, fields, forms, workflows, chatbots, agents, rules, packages, and tests through a constrained planning pipeline.

## Audit, Version, Security, And Deployment

```appgen
audit ComplianceTrail {
  subject: Invoice, Payment
  actor: User.id
  retention: P7Y
  immutable: true
}

version FinanceRelease {
  semver: 1.4.0
  compatibility: backward
  migration: online
}

security FinanceSecurity {
  rbac: enabled
  tenant: organization_id
  secret: PAYMENT_PROVIDER_KEY
}

deploy Production {
  unit ar as service
  unit ar_worker as worker
  unit desktop_shell as desktop
  scale ar min 2 max 10
  health ar "/health"
  check ar http "/ready"
  resource ar cpu 500m
  resource ar memory 1Gi
  env ar DATABASE_URL
}
```

Audit blocks describe evidence. Version blocks describe release compatibility. Security blocks describe policy. Deploy blocks describe runtime topology. Together they let AppGen-X generate not just code, but a managed enterprise application with operational intent.

## Packaging Desktop And Mobile Applications

Packaging is declared, not implied.

```appgen
package FieldOpsDesktop {
  target: desktop
  format: installer
  signing: required
  splash: FieldOpsSplash
}

package FieldOpsMobile {
  target: mobile
  format: store_archive
  signing: required
  offline: enabled
}
```

Desktop packages should include installer metadata, signing posture, startup commands, splash-screen assets, menus, and update policy. Mobile packages should include bundle identifiers, signing profile names, offline data policy, permissions, and store metadata. The language records intent; platform generators implement the concrete packaging toolchain.

## Semantic Validation Checklist

A valid AppGen-X program should satisfy these checks:

- Every table, view, flow, role, rule, PBC, API, event, job, report, menu, component, package, test, LLM, agent, deployment, audit, version, operation, and security block has a unique name in its namespace.
- Every relationship target resolves to an existing table field.
- Every database-backed view field resolves to a column, calculated field, or valid lookup path.
- Every handler target resolves to an operation, flow, agent, API/event contract, or other allowed generator target.
- Every PBC included in a composition has a version.
- Every cross-PBC connection uses a published API, event, or command contract.
- Every deployment unit has a known pattern such as service, worker, job, desktop, mobile, web, pwa, edge, or embedded.
- Every package target is compatible with the app targets.
- Every secret is referenced by name, not embedded as a literal value.

## Formatting Guidelines

Prefer one construct per file for large applications, or one bounded context per file for small teams. Keep table fields in this order: identity, business keys, foreign keys, editable fields, calculated fields, audit fields, directives. Keep views close to their table when the screen is table-specific. Keep PBCs and composition near the application assembly layer.

## Common Gotchas

- Single `=` creates calculated fields; `==` compares values in rules.
- A view bound with `for Table` cannot display arbitrary names. It may display table fields, calculated fields, or resolvable lookup paths.
- A PBC should not directly modify another PBC's private datastore.
- A composition should describe integration contracts, not implementation shortcuts.
- Generated lookup controls require declared relationships or lookup directives.
- Deployment patterns are explicit. If a PBC runs as a separate service, declare a service unit.
- Natural-language evolution should result in a DSL diff that can be linted and reviewed.
- Use contextual directives for domain detail; do not ask for a new global keyword unless the concept changes platform structure.

## Complete Example

```appgen
app FinanceOps { targets: web, mobile, desktop, chatbot; database: postgresql }

enum InvoiceStatus { draft reviewed approved paid void }

table Customer {
  id: int pk
  code: string required unique search
  name: string required search
}

table Invoice {
  id: int pk
  customer_id: int required -> Customer.id [many-to-one]
  invoice_number: string required unique search
  status: InvoiceStatus default draft search
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
  lookup customer_name (customer.name)
}

view InvoiceForm for Invoice {
  Header: invoice_number, customer.name, status
  Totals: subtotal, tax, total
  @ invoice_number TextBox 0 0 4 1
  @ customer.name Lookup 4 0 4 1
  @ total CurrencyBox 8 2 3 1
  on Save -> SubmitInvoice
}

rule InvoicePolicy for Invoice {
  invoice_number required "Invoice number is required"
  total > 0
  status in draft, reviewed, approved, paid
}

flow SubmitInvoice {
  draft -> reviewed
  human FinanceReview assigned Accountant -> approved
  approved -> posted
  compensate posted -> ReverseInvoice
}

operation SubmitInvoice {
  validate -> SubmitInvoice
  emits: InvoiceIssuedEvent
}

pbc AccountsReceivable {
  domain: finance
  owns: Customer, Invoice
  exposes InvoiceApi -> public
  emits InvoiceIssued -> InvoiceIssuedEvent
}

composition FinanceSuite {
  include pbc AccountsReceivable version 1.0.0
  require database postgresql
  expose api InvoiceApi
}

llm LocalBuilder { provider: ollama; model: qwen3.5-4b }
agent FinanceAssistant { uses: LocalBuilder; permission Invoice: read, create, update }
```

## Appendix: Complete ANTLR Grammar

The parser grammar below is included so this manual is self-contained. The prose sections above explain how to author against it; this appendix is the exact syntax contract used by the parser.

```antlr
grammar appgen;

options {
  language = Python3;
}

schema
  : appDecl? element* EOF
  ;

appDecl
  : APP (IDENT | STRING)? appBlock?
  ;

appBlock
  : LBRACE appOption* RBRACE
  ;

appOption
  : IDENT COLON literal (COMMA literal)* SEMI?
  ;

element
  : tableDecl
  | groupDecl
  | enumDecl
  | relationDecl
  | viewDecl
  | flowDecl
  | roleDecl
  | ruleDecl
  | llmDecl
  | agentDecl
  | pbcDecl
  | compositionDecl
  | auditDecl
  | deploymentDecl
  | versionDecl
  | operationDecl
  | securityDecl
  | apiDecl
  | eventDecl
  | jobDecl
  | reportDecl
  | menuDecl
  | componentDecl
  | packageDecl
  | testDecl
  ;

tableDecl
  : TABLE IDENT tableBody
  ;

tableBody
  : LBRACE tableItem* RBRACE
  ;

tableItem
  : fieldDecl
  | spreadDecl
  | relationDecl
  | tableDirective
  ;

fieldDecl
  : IDENT COLON typeRef derivedExpr? modifier* SEMI?
  ;

spreadDecl
  : ELLIPSIS IDENT SEMI?
  ;

groupDecl
  : IDENT tableBody
  ;

derivedExpr
  : EQ expression
  ;

typeRef
  : IDENT (LPAREN INT RPAREN)? (LBRACK RBRACK)?
  ;

modifier
  : PK
  | REQUIRED
  | UNIQUE
  | HIDE
  | SEARCH
  | DEFAULT literal
  | REF target relationCardinality?
  | ARROW target relationCardinality?
  ;

relationDecl
  : REF? target ARROW target relationCardinality? SEMI?
  ;

tableDirective
  : (IDENT | UNIQUE) IDENT? LPAREN directiveValue (COMMA directiveValue)* RPAREN (ARROW directiveValue (COMMA directiveValue)*)? SEMI?
  ;

relationCardinality
  : LBRACK agenticValue RBRACK
  ;

target
  : IDENT DOT IDENT
  ;

enumDecl
  : ENUM IDENT LBRACE IDENT* RBRACE
  ;

viewDecl
  : VIEW IDENT FOR IDENT LBRACE viewItem* RBRACE
  ;

viewItem
  : handlerDecl
  | componentPlacement
  | IDENT COLON qualifiedName (COMMA qualifiedName)* SEMI?
  | qualifiedName (COMMA qualifiedName)* SEMI?
  ;

componentPlacement
  : AT qualifiedName IDENT INT INT INT INT SEMI?
  ;

flowDecl
  : FLOW IDENT LBRACE flowItem* RBRACE
  ;

flowItem
  : flowStep
  | flowDirective
  ;

flowStep
  : IDENT ARROW IDENT SEMI?
  ;

flowDirective
  : IDENT agenticValue* (ARROW IDENT)? SEMI?
  ;

roleDecl
  : ROLE IDENT LBRACE permission* RBRACE
  ;

permission
  : IDENT COLON IDENT (COMMA IDENT)* SEMI?
  ;

ruleDecl
  : RULE IDENT FOR IDENT LBRACE ruleItem* RBRACE
  ;

llmDecl
  : LLM IDENT LBRACE agenticOption* RBRACE
  ;

agentDecl
  : AGENT IDENT LBRACE agentItem* RBRACE
  ;

agentItem
  : handlerDecl
  | contractArrow
  | agenticOption
  | permission
  ;

pbcDecl
  : PBC IDENT LBRACE pbcItem* RBRACE
  ;

pbcItem
  : handlerDecl
  | contractArrow
  | agenticOption
  | permission
  ;

compositionDecl
  : COMPOSITION IDENT LBRACE compositionItem* RBRACE
  ;

compositionItem
  : INCLUDE PBC IDENT VERSION agenticValue SEMI?
  | REQUIRE IDENT agenticValue (COMMA agenticValue)* SEMI?
  | EXPOSE IDENT agenticValue (COMMA agenticValue)* SEMI?
  | CONNECT IDENT IDENT IDENT ARROW IDENT IDENT IDENT SEMI?
  | agenticOption
  ;

auditDecl
  : AUDIT IDENT LBRACE agenticOption* RBRACE
  ;

deploymentDecl
  : DEPLOY IDENT LBRACE deploymentItem* RBRACE
  ;

deploymentItem
  : deployUnit
  | deployScale
  | deployHealth
  | deployCheck
  | deployResource
  | deployBinding
  | deployDirective
  | agenticOption
  ;

deployUnit
  : UNIT IDENT AS IDENT SEMI?
  ;

deployScale
  : SCALE IDENT MIN INT MAX INT SEMI?
  ;

deployHealth
  : HEALTH IDENT STRING SEMI?
  ;

deployCheck
  : CHECK IDENT IDENT STRING SEMI?
  ;

deployResource
  : RESOURCE IDENT IDENT agenticValue SEMI?
  ;

deployBinding
  : (ENV | IDENT) IDENT agenticValue SEMI?
  ;

deployDirective
  : IDENT IDENT agenticValue* SEMI?
  ;

versionDecl
  : VERSION IDENT LBRACE agenticOption* RBRACE
  ;

operationDecl
  : OPERATION IDENT LBRACE operationItem* RBRACE
  ;

operationItem
  : flowStep
  | handlerDecl
  | contractArrow
  | agenticOption
  ;

securityDecl
  : SECURITY IDENT LBRACE securityItem* RBRACE
  ;

securityItem
  : permission
  | agenticOption
  ;

apiDecl
  : API IDENT LBRACE contractItem* RBRACE
  ;

eventDecl
  : EVENT IDENT LBRACE contractItem* RBRACE
  ;

jobDecl
  : JOB IDENT LBRACE contractItem* RBRACE
  ;

reportDecl
  : REPORT IDENT LBRACE contractItem* RBRACE
  ;

menuDecl
  : MENU IDENT LBRACE contractItem* RBRACE
  ;

componentDecl
  : COMPONENT IDENT LBRACE contractItem* RBRACE
  ;

packageDecl
  : PACKAGE IDENT LBRACE contractItem* RBRACE
  ;

testDecl
  : TEST IDENT LBRACE contractItem* RBRACE
  ;

contractItem
  : handlerDecl
  | contractArrow
  | contractDirective
  | agenticOption
  | permission
  ;

handlerDecl
  : ON IDENT ARROW IDENT SEMI?
  | IDENT IDENT ARROW IDENT SEMI?
  ;

contractArrow
  : IDENT agenticValue* ARROW IDENT SEMI?
  ;

contractDirective
  : IDENT agenticValue+ SEMI?
  ;

agenticOption
  : IDENT COLON agenticValue (COMMA agenticValue)* SEMI?
  ;

agenticValue
  : valueAtom ((DOT | MINUS) valueAtom)*
  ;

valueAtom
  : literal
  | APP
  | TABLE
  | ENUM
  | VIEW
  | FOR
  | FLOW
  | ROLE
  | RULE
  | PBC
  | COMPOSITION
  | AUDIT
  | DEPLOY
  | VERSION
  | OPERATION
  | SECURITY
  | API
  | EVENT
  | JOB
  | REPORT
  | MENU
  | COMPONENT
  | PACKAGE
  | TEST
  | LLM
  | AGENT
  | INCLUDE
  | REQUIRE
  | EXPOSE
  | CONNECT
  | ON
  | AND
  | OR
  | NOT
  | EXISTS
  | IS
  | NULL
  | UNIT
  | AS
  | SCALE
  | MIN
  | MAX
  | HEALTH
  | CHECK
  | RESOURCE
  | ENV
  ;

ruleItem
  : IDENT REQUIRED STRING? SEMI?
  | ruleExpression (ARROW IDENT)? SEMI?
  ;

ruleExpression
  : ruleOr
  ;

ruleOr
  : ruleAnd (OR ruleAnd)*
  ;

ruleAnd
  : ruleUnary (AND ruleUnary)*
  ;

ruleUnary
  : NOT ruleUnary
  | EXISTS LPAREN qualifiedName RPAREN
  | rulePredicate
  ;

rulePredicate
  : ruleTerm (ruleOperator ruleValueList | IS NOT? NULL)?
  ;

ruleValueList
  : ruleTerm (COMMA ruleTerm)*
  ;

ruleTerm
  : qualifiedName
  | literal
  | LPAREN ruleExpression RPAREN
  ;

directiveValue
  : ruleExpression
  | agenticValue
  ;

ruleOperator
  : EQEQ
  | NEQ
  | GTE
  | LTE
  | GT
  | LT
  | IN
  ;

literal
  : STRING
  | DECIMAL
  | INT
  | BOOL
  | IDENT
  ;

qualifiedName
  : IDENT (DOT IDENT)*
  ;

expression
  : expressionAtom (operator expressionAtom)*
  ;

expressionAtom
  : qualifiedName
  | literal
  | LPAREN expression RPAREN
  ;

operator
  : PLUS
  | MINUS
  | STAR
  | SLASH
  ;

APP      : 'app';
TABLE    : 'table';
REF      : 'ref';
ENUM     : 'enum';
VIEW     : 'view';
FOR      : 'for';
FLOW     : 'flow';
ROLE     : 'role';
RULE     : 'rule';
PBC      : 'pbc';
COMPOSITION : 'composition';
AUDIT    : 'audit';
DEPLOY   : 'deploy';
VERSION  : 'version';
OPERATION : 'operation';
SECURITY : 'security';
API      : 'api';
EVENT    : 'event';
JOB      : 'job';
REPORT   : 'report';
MENU     : 'menu';
COMPONENT : 'component';
PACKAGE  : 'package';
TEST     : 'test';
INCLUDE  : 'include';
REQUIRE  : 'require';
EXPOSE   : 'expose';
CONNECT  : 'connect';
LLM      : 'llm';
AGENT    : 'agent';
PK       : 'pk';
REQUIRED : 'required';
UNIQUE   : 'unique';
HIDE     : 'hidden';
SEARCH   : 'search';
DEFAULT  : 'default';
IN       : 'in';
ON       : 'on';
AND      : 'and';
OR       : 'or';
NOT      : 'not';
EXISTS   : 'exists';
IS       : 'is';
NULL     : 'null';
UNIT     : 'unit';
AS       : 'as';
SCALE    : 'scale';
MIN      : 'min';
MAX      : 'max';
HEALTH   : 'health';
CHECK    : 'check';
RESOURCE : 'resource';
ENV      : 'env';

ELLIPSIS : '...';
AT     : '@';
ARROW  : '->';
EQEQ   : '==';
NEQ    : '!=';
GTE    : '>=';
LTE    : '<=';
GT     : '>';
LT     : '<';
EQ     : '=';
PLUS   : '+';
MINUS  : '-';
STAR   : '*';
SLASH  : '/';
COLON  : ':';
COMMA  : ',';
DOT    : '.';
SEMI   : ';';
LPAREN : '(';
RPAREN : ')';
LBRACE : '{';
RBRACE : '}';
LBRACK : '[';
RBRACK : ']';

BOOL
  : 'true'
  | 'false'
  ;

DECIMAL
  : [0-9]+ '.' [0-9]+
  ;

INT
  : [0-9]+
  ;

IDENT
  : [A-Za-z_][A-Za-z0-9_]*
  ;

STRING
  : '"' ( '\\' . | ~["\\] )* '"'
  | '\'' ( '\\' . | ~['\\] )* '\''
  ;

LINE_COMMENT
  : ('//' | '#') ~[\r\n]* -> skip
  ;

BLOCK_COMMENT
  : '/*' .*? '*/' -> skip
  ;

WS
  : [ \t\r\n]+ -> skip
  ;

```
