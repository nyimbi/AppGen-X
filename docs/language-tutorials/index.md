# AppGen-X Language Tutorials

This is a guided one-hour tutorial path for learning the AppGen-X language. It is designed to take at least 60 minutes to read carefully because each lesson includes explanation, a DSL increment, validation guidance, generator expectations, gotchas, and exercises. The goal is not only to memorize syntax; the goal is to learn how AppGen-X turns a concise enterprise specification into database schema, forms, handlers, workflows, agents, PBC contracts, packages, and tests.

Use the language manual when you need exhaustive keyword detail. Use this tutorial when you want to build muscle memory. The tutorial is intentionally written as a continuous reading path rather than a terse quickstart.

## Before You Start

You need the source tree or an installed package that exposes the `appgen` command.

```console
appgen --help
appgen --lint-dsl finance.appgen
appgen --dsl finance.appgen --writedir generated/finance
```

The tutorial builds a small finance and operations application. It intentionally uses only a few tables, but every pattern scales to large ERP-style systems.

## One-Hour Reading Plan

- **Minute 00-05: Orient the project.** Create the application shell, choose targets, and run the linter before any domain detail is added.
- **Minute 05-10: Model master data.** Declare stable tables, primary keys, search fields, required fields, and uniqueness constraints.
- **Minute 10-15: Add relationships.** Connect tables with arrow references and check that lookup paths resolve through declared foreign keys.
- **Minute 15-20: Design a form.** Use sections and component placements to define a visual screen that remains database-backed and lintable.
- **Minute 20-25: Wire handlers.** Route buttons, commands, and context actions to named operations and flows.
- **Minute 25-30: Write rules.** Add validation and policy rules with comparisons, membership checks, null checks, and actions.
- **Minute 30-35: Build workflow.** Define state transitions, human tasks, timers, participants, and compensation.
- **Minute 35-40: Add security.** Declare roles and security policies for RBAC, tenancy, and sensitive data handling.
- **Minute 40-45: Add agents.** Declare local and hosted LLMs, agent permissions, and constrained skills.
- **Minute 45-50: Compose PBCs.** Model a PBC and assemble it into a composition through explicit API and event contracts.
- **Minute 50-55: Package targets.** Declare web, mobile, desktop, chatbot, service, and worker packaging intent.
- **Minute 55-65: Validate and evolve.** Lint, generate, inspect the DSL diff from natural language, and add tests for the generated capability.

Create `finance.appgen` and add each section as you go. Run the linter after each lesson. The repeated linting is part of the learning process: AppGen-X is meant to keep the DSL small, reviewable, and safe enough for small local models and external coding agents to evolve.

## Lesson 1. Orient the project (00-05 minutes)

Create the application shell, choose targets, and run the linter before any domain detail is added.

Start with the app declaration. The app block names the product boundary and declares generation targets. This is the point where you decide whether the product is a web app only, a multi-target application, a chatbot-enabled system, or a package that also includes mobile and desktop output.

```appgen
app FinanceOps {
  targets: web, mobile, desktop, chatbot
  database: postgresql
  theme: graphite
}
```

Run the linter now. A clean empty application is valuable because it proves your tooling works before domain complexity arrives.

```console
appgen --lint-dsl finance.appgen
```

What to look for: the linter should accept known targets, reject unknown targets, and report syntax errors with useful locations. If this first step fails, fix the environment before adding tables. Do not debug a large DSL file when a five-line application shell would have exposed the same setup problem.

Generator expectation: from the application declaration alone, generators can choose target families, default project layout, package directories, theme defaults, and runtime policies. Later declarations fill in the data, UI, workflow, and deployment details.

Exercise: add `pwa` to the target list, lint again, then remove it if your generated application does not need offline browser installation.

## Lesson 2. Model master data (05-10 minutes)

Declare stable tables, primary keys, search fields, required fields, and uniqueness constraints.

Model master data with tables. Use `required` for values that must exist, `search` for default lookup fields, and `unique` for business keys.

```appgen
table Customer {
  id: int pk
  code: string required unique search
  name: string required search
  email: email unique
}

table Product {
  id: int pk
  sku: string required unique search
  name: string required search
  unit_price: decimal default 0
}
```

A table is more than a database migration. It becomes a model, validation surface, API resource, default list screen, create/edit workflow, search index candidate, report source, and form binding target. Because it feeds so many generated surfaces, table clarity matters more than compactness.

Authoring guidance: put identity first, then business keys, then required display fields, then optional details, then calculated values, then directives. This order is not required by the grammar, but it makes reviews faster.

Validation guidance: duplicate field names should fail. Invalid modifiers should fail. A table without an explicit primary key may receive a generated `id`, but critical enterprise tables should usually declare their primary key intentionally so database and integration contracts remain stable.

Exercise: add a `Vendor` table with `code`, `name`, and `tax_id`. Mark `code` as required, unique, and searchable.

## Lesson 3. Add relationships (10-15 minutes)

Connect tables with arrow references and check that lookup paths resolve through declared foreign keys.

Relationships use arrow references. Add invoices and invoice lines.

```appgen
enum InvoiceStatus { draft reviewed approved paid void }

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

table InvoiceLine {
  id: int pk
  invoice_id: int required -> Invoice.id [many-to-one]
  product_id: int required -> Product.id [many-to-one]
  quantity: decimal default 1
  unit_price: decimal default 0
  line_total: decimal = quantity * unit_price
}
```

The important idea is that `customer.name` is not magic text. It is a lookup path derived from the `customer_id -> Customer.id` relationship. AppGen-X should reject paths that do not resolve. For multi-table chains such as invoice to customer to account manager to user, each hop must be backed by a relationship. The platform should not guess missing joins.

Generator expectation: relationship fields become foreign keys, generated lookup controls, API relationship metadata, join helpers, report dimensions, and navigation links. Searchable fields on the referenced table provide good default display labels.

Gotcha: if a table has two relationships to the same target, such as `billing_customer_id` and `shipping_customer_id`, lookup aliases must remain unambiguous. Prefer explicit lookup directives when default aliasing is not enough.

Exercise: add `product.name` to an invoice-line lookup directive and verify the linter accepts it only because `product_id` references `Product.id`.

## Lesson 4. Design a form (15-20 minutes)

Use sections and component placements to define a visual screen that remains database-backed and lintable.

A view binds UI to a table. Sections describe logical grouping; placements describe visual component positions.

```appgen
view InvoiceForm for Invoice {
  Header: invoice_number, customer.name, status
  Totals: subtotal, tax, total
  @ invoice_number TextBox 0 0 4 1
  @ customer.name Lookup 4 0 4 1
  @ status ComboBox 8 0 3 1
  @ subtotal CurrencyBox 0 2 3 1
  @ tax CurrencyBox 3 2 3 1
  @ total CurrencyBox 6 2 3 1
}
```

The form designer can render these placements as draggable components. The linter still enforces that every bound field is a real column, calculated field, or lookup path. This is the key design principle: the visual surface is flexible, but database-backed forms cannot silently point to invented columns.

Generator expectation: sections become layout groups or responsive regions. Component placements become design-surface coordinates. Component names such as `TextBox`, `Lookup`, `ComboBox`, and `CurrencyBox` select generated controls from the platform component catalog. The same view can inform web, mobile, and desktop generators, though each target may adapt layout density.

Gotcha: a calculated field such as `total` can be displayed, but it should not be editable unless an explicit generator feature supports reverse calculation. For ordinary forms, calculated values are read-only or recalculated through handlers.

Exercise: add a compact mobile form view with fewer fields and wider rows. Keep every binding valid.

## Lesson 5. Wire handlers (20-25 minutes)

Route buttons, commands, and context actions to named operations and flows.

Handlers route user actions to named application behavior.

```appgen
view InvoiceForm for Invoice {
  Header: invoice_number, customer.name, status
  @ invoice_number TextBox 0 0 4 1
  @ customer.name Lookup 4 0 4 1
  on Save -> SubmitInvoice
  on Cancel -> CloseInvoice
}

operation CloseInvoice {
  close -> InvoiceList
}
```

Prefer named operations as handler targets. This gives generated classes and components a stable architecture: a button handler can call a shared operation, and another button can call the same operation without copying logic. It also lets tests exercise business behavior without pretending to click every visual control.

Context actions belong in menu blocks.

```appgen
menu InvoiceContextMenu {
  context InvoiceRow -> OpenInvoice
  item VoidInvoice -> VoidInvoice
}
```

Generator expectation: the platform should generate component event bindings, handler stubs or concrete calls, operation classes/functions, and tests that prove event targets exist. Handlers may call other handlers indirectly through shared operations, but shared operations are the clean integration point.

Gotcha: avoid burying business rules inside visual event code. If a save button approves an invoice, write an operation and a flow. The view should only wire the event.

Exercise: add a toolbar command and a context menu command that both call the same `OpenInvoice` operation.

## Lesson 6. Write rules (25-30 minutes)

Add validation and policy rules with comparisons, membership checks, null checks, and actions.

Rules capture validation and policy close to the data they protect.

```appgen
rule InvoicePolicy for Invoice {
  invoice_number required "Invoice number is required"
  total > 0
  status in draft, reviewed, approved, paid
  customer_id is not null
}
```

Use `required` for field presence, `in` for allowed values, comparison operators for thresholds, and null checks for relationship completeness. Use `->` when a rule should trigger an operation or policy action.

```appgen
rule ApprovalPolicy for Invoice {
  status == approved and total > 0 -> SubmitInvoice
  status == approved and customer_id is null -> BlockApproval
}
```

Generator expectation: rules can become server-side validators, client-side validation hints, workflow guards, tests, and policy documentation. A rule is a contract; do not treat it as a comment.

Gotcha: single `=` is for calculated fields. Use `==` for equality in rule expressions. Another common mistake is checking display labels instead of stable enum values. Rules should compare stable values.

Exercise: add a rule that blocks approval when `total <= 0`, then add a positive test and a negative test declaration.

## Lesson 7. Build workflow (30-35 minutes)

Define state transitions, human tasks, timers, participants, and compensation.

Flows model lifecycle and process.

```appgen
flow SubmitInvoice {
  participant Accountant
  participant Controller
  draft -> reviewed
  human ControllerReview assigned Controller -> approved
  timer reviewed "P2D" -> escalated
  approved -> posted
  compensate posted -> ReverseInvoice
}
```

The DSL keeps workflow concise but expressive. Contextual directives such as `participant`, `human`, `timer`, and `compensate` are parsed as flow directives and interpreted by workflow-capable generators. This gives the language room to support human tasks, timers, compensation, escalation, rollout plans, and workflow-agent skills without a grammar change for every workflow engine.

Generator expectation: a flow may emit state-machine code, workflow definitions, task queues, audit events, notification hooks, and tests. Human tasks should produce assignable work items. Timers should produce scheduled checks or workflow-engine timers. Compensation should produce explicit reverse or repair operations.

Gotcha: do not model every UI click as a workflow state. Use flows for business lifecycle, not for tiny local interface details.

Exercise: add a payment collection flow with `issued -> partially_paid -> paid`, then add a timer that escalates overdue invoices.

## Lesson 8. Add security (35-40 minutes)

Declare roles and security policies for RBAC, tenancy, and sensitive data handling.

Roles and security policies keep generated applications from treating every screen as public.

```appgen
role Accountant {
  Customer: read, create, update
  Invoice: read, create, update
}

role Auditor {
  Customer: read
  Invoice: read
}

security TenantPolicy {
  rbac: enabled
  tenant: organization_id
  Invoice: read, create, update
}
```

A generator should use this information for API authorization, form visibility, menu visibility, report access, background job permissions, and test generation. Security should not be added as a separate handwritten layer that the DSL cannot see.

Generator expectation: roles become policy definitions, route guards, menu filters, test fixtures, and documentation. Security blocks become tenancy filters, secret references, data-classification hints, and platform policy checks.

Gotcha: do not put secret values in the DSL. Declare secret names or environment bindings in deployment blocks. The actual values belong in deployment infrastructure.

Exercise: add a `CollectionsAgent` role that can read invoices and update payment status, but cannot edit customer master data.

## Lesson 9. Add agents (40-45 minutes)

Declare local and hosted LLMs, agent permissions, and constrained skills.

LLM and agent declarations make agentic systems explicit and reviewable.

```appgen
llm LocalPlanner {
  provider: ollama
  model: qwen3.5-4b
  endpoint: "http://localhost:11434"
}

llm HostedPlanner {
  provider: openai_compatible
  model: frontier-coder
  api_key_env: APPGEN_LLM_API_KEY
}

agent FinanceAssistant {
  uses: LocalPlanner, HostedPlanner
  skill explain_invoice -> ExplainInvoice
  skill draft_collection_note -> DraftCollectionNote
  permission Invoice: read, update
}
```

Small local models work best when the DSL change is constrained: add a table, add a field, add a lookup, add a handler, add a rule, or connect a PBC event. Natural language should produce a lintable DSL diff, not opaque generated code.

Generator expectation: LLM declarations become provider configuration, environment-variable requirements, and model routing hints. Agent declarations become tool manifests, permissions, prompt contracts, test fixtures, and runtime wiring.

Gotcha: an agent without permissions is either useless or unsafe, depending on generator defaults. Declare permissions explicitly. An agent skill should point to a named operation, flow, or contract target.

Exercise: add an agent skill that creates a customer follow-up task and restrict it to reading customer records and creating tasks.

## Lesson 10. Compose PBCs (45-50 minutes)

Model a PBC and assemble it into a composition through explicit API and event contracts.

PBCs let you assemble applications from bounded business capabilities.

```appgen
pbc AccountsReceivable {
  domain: finance
  owns: Customer, Invoice, InvoiceLine
  exposes InvoiceApi -> public
  emits InvoiceIssued -> InvoiceIssuedEvent
  datastore: postgresql
}

event InvoiceIssuedEvent {
  payload: Invoice
  key: Invoice.id
  version: 1
}

api InvoiceApi {
  endpoint: "/api/invoices"
  method: GET, POST
}
```

A PBC owns its data and publishes contracts. Other PBCs integrate through APIs, events, and commands rather than private tables. This is what makes AppGen-X an application composition platform instead of only a CRUD generator.

Generator expectation: a PBC should self-register with the platform catalog, expose metadata, publish contracts, emit tests, and produce deployment descriptors. A composition should verify version compatibility and contract existence.

Gotcha: if a composition connects two PBCs but the event or command is not declared, the integration is not reviewable. Declare the contract first.

Exercise: add a `GeneralLedger` PBC that consumes `InvoiceIssuedEvent` and exposes a `PostJournal` command.

## Lesson 11. Package targets (50-55 minutes)

Declare web, mobile, desktop, chatbot, service, and worker packaging intent.

Composition records selected PBCs and their connections. Deployment and package blocks record runtime and distribution intent.

```appgen
composition FinanceSuite {
  include pbc AccountsReceivable version 1.0.0
  include pbc GeneralLedger version 1.0.0
  require database postgresql
  expose api InvoiceApi
  connect AccountsReceivable event InvoiceIssued -> GeneralLedger command PostJournal
}

deploy Production {
  unit ar as service
  unit ar_worker as worker
  unit finance_web as web
  unit finance_desktop as desktop
  scale ar min 2 max 8
  health ar "/health"
  env ar DATABASE_URL
}

package FinanceDesktop {
  target: desktop
  format: installer
  signing: required
}

package FinanceMobile {
  target: mobile
  format: store_archive
  signing: required
  offline: enabled
}
```

Generator expectation: deployment blocks produce service manifests, worker manifests, health checks, environment-variable documentation, resource hints, and smoke tests. Package blocks produce target-specific package descriptors and release checks.

Gotcha: declaring `targets: mobile` in the app block says the application should support mobile generation. It does not fully describe signing, offline policy, permissions, or distribution format. Use package blocks for that.

Exercise: add a chatbot package or target-specific package for field collections.

## Lesson 12. Validate and evolve (55-65 minutes)

Lint, generate, inspect the DSL diff from natural language, and add tests for the generated capability.

Finish by linting and generating.

```console
appgen --lint-dsl finance.appgen
appgen --dsl finance.appgen --writedir generated/finance
```

Then inspect the generated migrations, models, forms, handlers, workflow files, PBC contracts, package descriptors, and tests. When using natural language to evolve the application, insist on a DSL diff first. Review the diff, run the linter, and only then regenerate.

```appgen
test InvoiceAcceptance {
  scenario: issue_invoice
  expects: InvoiceIssuedEvent
}
```

Generator expectation: tests should cover database schema, view bindings, handler targets, workflow transitions, PBC contracts, deployment metadata, and package outputs. Even when you defer broad test automation for velocity, keep the DSL lint and a narrow release audit in place.

Gotcha: generated code should not become the only source of truth. If a natural-language request adds a field directly to generated code but not the DSL, regeneration can erase it. Always return to the DSL.

Exercise: ask an agent to add credit memos. The acceptable output is a small DSL patch that adds tables, rules, forms, operations, and events. Reject a response that jumps straight to unrelated handwritten application code.

## Extended One-Hour Reading Notes

The lessons above are the hands-on path. The notes below are the long-form reading path. Read them slowly before assigning work to another developer or agent; they explain the design pressure behind the syntax and help you review generated applications with more confidence.

### Reading Note 1. Application boundaries

This note focuses on app declarations, target selection, database policy, and generation scope. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 2. Data modeling discipline

This note focuses on tables, fields, identity, business keys, default values, calculated values, and table directives. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 3. Relationship-driven UI

This note focuses on foreign keys, lookup aliases, multi-hop paths, automatic lookup controls, and invalid binding prevention. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 4. Visual form design

This note focuses on sections, component placements, responsive target adaptation, and component catalog usage. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 5. Handler architecture

This note focuses on events, operations, shared behavior, class/component integration, and testable command routing. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 6. Policy and validation

This note focuses on required messages, boolean expressions, membership checks, null checks, and workflow guards. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 7. Workflow modeling

This note focuses on states, human tasks, timers, compensation, participants, rollout plans, and evidence. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 8. Security modeling

This note focuses on roles, RBAC, tenancy, secret references, row filters, and generated authorization tests. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 9. Agentic development

This note focuses on local LLMs, hosted LLMs, constrained agent skills, permissions, and token-efficient DSL diffs. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 10. PBC boundaries

This note focuses on owned data, published APIs, events, commands, self-registration, tests, and independent deployment. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 11. Composition and deployment

This note focuses on versioned inclusion, contract connections, service units, workers, jobs, packages, and health checks. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

### Reading Note 12. Review and regeneration

This note focuses on linting, generated artifacts, natural-language changes, diff review, commits, and release evidence. The practical discipline is to keep every important application decision visible in the DSL. If a decision affects generated code, runtime behavior, access control, deployment, packaging, or future regeneration, it belongs in a block that the linter and generator can inspect.

When authoring this part of an application, start with the smallest valid construct and add detail only when a generator, reviewer, or business rule needs it. A concise table is better than a speculative schema. A named operation is better than hidden button behavior. A PBC contract is better than a direct cross-module table dependency. This restraint is what makes the language useful for both humans and small local models.

During review, ask three questions. First, does every referenced name resolve to something declared? Second, does the generated artifact have a stable owner? Third, can a future natural-language change produce a small DSL diff rather than editing generated code directly? If the answer to any of these is no, improve the DSL before generating more files.

The common failure mode is treating the DSL as a quick scaffolding input and then moving all real work into generated code. AppGen-X is designed for the opposite workflow: the DSL remains the source of durable intent, while generated code is a repeatable projection. That is why tables, forms, workflows, rules, agents, packages, and deployment patterns all have language-level representation.

Practice exercise: write a five-line DSL change for this topic, lint it, and explain what generated files should change. Then write one invalid version and confirm the linter catches it. This invalid case is often more educational than the happy path because it reveals the semantic boundary the platform is protecting.

## Deep-Dive Reading Examples

These examples extend the one-hour tutorial with slower, review-oriented reading. They are intentionally prose-heavy so a reader can understand why each DSL construct exists before asking an agent to modify it.

### Deep Dive 1. From request to DSL

A user asks for a capability in natural language. The platform should convert that request into a precise DSL patch before generation. For example, "track customer credit limits" becomes a field, a validation rule, a form binding, and possibly an agent skill. The reviewable artifact is the DSL diff. Generated code is secondary evidence.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 2. From table to app surface

A single table can produce migrations, model classes, API routes, list screens, edit screens, search indexes, fixtures, and tests. That breadth is why table naming and field modifiers matter. A weak table definition creates weak generated output everywhere.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 3. From relationship to lookup

A relationship field should become a database constraint and a human-friendly lookup. The lookup label should come from search fields or explicit lookup directives. If a lookup path cannot resolve through declared relationships, the form should fail linting instead of generating a broken control.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 4. From view to component tree

A view is not a screenshot. It is a contract for a component tree. Sections express grouping, placements express design intent, and handlers express event wiring. Target generators adapt that contract to web, mobile, and desktop conventions.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 5. From handler to operation

A handler should be a short route to named behavior. This makes generated code easier to test and lets multiple controls share one operation. When a user asks for a button to do something, first ask what operation that button should invoke.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 6. From rule to generated tests

Every rule implies at least one positive and one negative test. If `total > 0` is required for approval, generated tests should prove zero or negative totals cannot approve. Rules are not comments; they are executable policy.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 7. From flow to work queue

Human tasks in flows should become assignable work. Timers should become scheduled checks or workflow-engine timers. Compensation should become explicit reversal or repair behavior. A flow without generated evidence is only a drawing.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 8. From role to access control

A role block should affect API policy, screen visibility, menu visibility, report access, agent permissions, and tests. The same permission model should apply across generated targets so mobile and desktop do not drift from web behavior.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 9. From LLM to constrained agent

An LLM declaration is infrastructure. An agent declaration is behavior. Keep them separate. The model endpoint says where reasoning happens; the agent skills and permissions say what the application allows that reasoning to do.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 10. From PBC to catalog entry

A PBC should self-register with enough metadata for the platform catalog: name, version, domain, owned tables, APIs, events, commands, roles, tests, deployment units, and documentation. Without registration, composition becomes manual assembly.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 11. From composition to runtime topology

A composition chooses capabilities and connects contracts. A deployment block chooses how those capabilities run. Keep those concerns separate so the same composition can be tested locally and deployed with a different topology later.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

### Deep Dive 12. From package to release

A package block records distribution intent. Desktop and mobile outputs need signing, identifiers, formats, splash/startup behavior, permissions, offline policy, and release checks. Treat packaging as part of application design, not as a post-generation afterthought.

Read the generated output through this lens: what contract did the DSL create, what files should be produced, what validation should fail for invalid references, and what tests prove the behavior? If you cannot answer those questions, the DSL needs more explicit intent before the next generation step.

A useful review habit is to write the inverse case. If the valid model adds a relationship-backed lookup, write the invalid model with a missing relationship and make sure linting fails. If the valid model adds a package, write the invalid model with an unsupported target and make sure the generator refuses it. This is how teams learn the edges of the language.

When using external agents, include this deep-dive framing in the prompt. Ask for the DSL patch first, ask for generated code second, and ask for verification evidence last. That sequence keeps the platform composable and prevents unreviewed handwritten code from becoming the hidden source of truth.

## Capstone: Build A Mini ERP Slice

Extend the tutorial app with these capabilities:

1. General ledger accounts and journals.
2. Accounts payable vendors and bills.
3. Inventory items and stock movements.
4. Employees and approval roles.
5. Reports for aging, trial balance, and inventory value.
6. A chatbot agent that explains invoice status and drafts collection messages.
7. Separate service units for finance APIs and background posting jobs.

A compact solution starts like this:

```appgen
table Account {
  id: int pk
  code: string required unique search
  name: string required search
  type: string required search
}

table JournalEntry {
  id: int pk
  entry_number: string required unique search
  posted_at: datetime
  source_event: string search
}

table JournalLine {
  id: int pk
  journal_entry_id: int required -> JournalEntry.id [many-to-one]
  account_id: int required -> Account.id [many-to-one]
  debit: decimal default 0
  credit: decimal default 0
}

rule JournalBalance for JournalLine {
  debit >= 0
  credit >= 0
}

report TrialBalance {
  source: JournalLine
  group: account.code, account.name
  measure: debit, credit
  export: pdf, xlsx
}
```

Read your generated app like a reviewer. Check that relationship fields have lookup controls, tables have migration files, handlers point at operations, operations point at workflows or contracts, PBCs do not cross private datastore boundaries, packages match app targets, and tests cover the acceptance paths.

## Tutorial Review Questions

- Which construct owns durable data?
- Which construct designs a database-backed form?
- Which construct routes a button click to behavior?
- Which construct describes a PBC boundary?
- Which construct assembles PBCs into an application?
- Which construct declares local or hosted LLM access?
- Which construct declares runtime topology?
- Which construct declares desktop or mobile packaging?
- Which operator compares equality in rules?
- Why should natural-language changes produce DSL diffs before code generation?

## Expected Reading Duration

A fast reader can skim examples quickly, but the intended tutorial path is at least one hour of careful reading: five minutes for setup, roughly five minutes per lesson, and ten minutes for capstone review. Teams should run the linter after every lesson and commit each meaningful DSL increment.
