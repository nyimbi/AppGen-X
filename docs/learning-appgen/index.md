# Learning AppGen-X

This textbook is a guided path for learning AppGen-X as an application
composition and generation platform. It starts with small DSL files and ends
with composable enterprise applications.

## Who This Is For

- Application developers who want to generate web, mobile, desktop, PWA, and
  chatbot targets from one source.
- Business analysts who want a readable application specification.
- Platform engineers who need PBC composition, release evidence, and deployment
  contracts.
- Coding agents that need token-efficient examples for generating complete
  applications.

## How To Use This Book

Read chapters 1 through 6 first. Then choose the enterprise chapters that match
your application.

Every chapter follows the same loop:

1. Write or generate a small DSL slice.
2. Lint it.
3. Review generated plans or release evidence.
4. Generate the application.
5. Commit the DSL and evidence.

## Chapter 1. The AppGen-X Mental Model

AppGen-X treats the DSL as the durable source of truth. Visual design, database
design, and natural-language changes should produce reviewable DSL updates.

The generation pipeline is:

1. Source intake from DSL, DBML, SQL, PonyORM, or live database.
2. Canonical `AppSchema`.
3. Lint, authoring, and release gates.
4. Generated app targets and package evidence.
5. Iteration through DSL, Studio, or natural language.

## Chapter 2. Your First Application

```appgen
app Library { targets: web, mobile, desktop }

table Book {
  id: int pk
  title: string required search
  isbn: string unique
}

view BookForm for Book {
  Main: title, isbn
}
```

Run:

```console
appgen --lint-dsl library.appgen
appgen --dsl library.appgen --writedir generated/library/app
```

Exercise: add `published_on: date` and rerun the linter.

## Chapter 3. Data Modeling

A useful application needs relationships, calculated fields, and lookup paths.

```appgen
table Author {
  id: int pk
  name: string required search
}

table Book {
  id: int pk
  author_id: int required -> Author.id [many-to-one]
  title: string required search
  slug: string = title + author_id
  lookup author_name (author.name)
}
```

Exercise: add a `Publisher` table and connect `Book.publisher_id` to it.

## Chapter 4. Form Design

AppGen-X can generate form sections and exact component placements.

```appgen
view BookForm for Book {
  Main: title, author.name
  @ title TextBox 0 0 6 1
  @ author.name Lookup 0 1 6 1
  on Save -> PublishBook
}
```

The linter rejects unknown form fields and invalid lookup paths. This prevents
database-backed forms from binding to columns that do not exist.

Exercise: intentionally write `author.full_name`, run the linter, then fix it.

## Chapter 5. Behavior

Use flows for lifecycle behavior and rules for validation or decision logic.

```appgen
flow PublishBook {
  draft -> reviewed
  human EditorialReview assigned Editor -> approved
  timer reviewed "P3D" -> escalated
  approved -> published
}

rule BookPolicy for Book {
  title required "Title is required"
  title is not null and exists(author) -> PublishBook
}
```

Exercise: add a compensation step that moves `published` back through a review
operation.

## Chapter 6. Security And Audit

```appgen
role Editor {
  Book: read, create, update
}

security LibraryPolicy {
  Book: read, create, update
  rbac: enabled
}

audit ReleaseAudit {
  evidence: migrations, tests, security
  gate: release
}
```

Exercise: add a `Reader` role that can only read books.

## Chapter 7. Agentic Applications

AppGen-X supports local and API-backed LLM providers.

```appgen
llm LocalModel {
  provider: ollama
  mode: local
  model: qwen3_4b
}

agent LibraryAssistant {
  provider: LocalModel
  goal: "Help editors prepare book records"
  tools: schema, forms, reports
  skill review BookSubmitted -> PublishBook
  Book: read, update
}
```

Token-efficient generation tip: ask coding agents to emit complete AppGen-X DSL
instead of verbose prose. The linter can then validate the result.

Exercise: add an API-backed provider that references an environment variable
for its key.

## Chapter 8. Enterprise Contracts

Generated applications need APIs, events, jobs, reports, menus, packages, and
tests.

```appgen
operation PublishBook {
  draft -> reviewed
  reviewed -> published
  owner: editorial_ops
}

api BookApi {
  GET "/books" -> PublishBook
  auth: Book.read
}

event BookPublished {
  publish BookPublished -> PublishBook
  topic: pbc.library.events
}

job NightlyCatalogCheck {
  daily -> PublishBook
  retry: 3
}

report CatalogReport {
  source: Book
  export: csv, pdf
}

package LibraryRelease {
  targets: web, mobile, desktop
  channel: stable
}
```

Exercise: add a menu item and a smoke test block.

## Chapter 9. Composable Applications

PBCs let users select and compose enterprise capabilities.

```appgen
pbc catalog {
  label: "Catalog"
  mesh: commerce
  owns: Book, Author
  emits: BookPublished
  consumes: AuthorUpdated
}

composition LibrarySuite {
  include pbc catalog version "1.x"
  require datastore owned_per_pbc
  require eventing appgen_x_outbox
  expose workbench all
}
```

Exercise: add a second PBC for subscriptions and connect one event between the
two capabilities.

## Chapter 10. Deployment And Packaging

```appgen
deploy Production {
  runtime: kubernetes
  unit catalog as microservice
  unit PublishBook as process
  unit NightlyCatalogCheck as worker
  scale catalog min 2 max 8
  health catalog "/healthz"
  check catalog readiness "/readyz"
  env catalog DATABASE_URL
  secret catalog OPENAI_API_KEY
}
```

Exercise: add a desktop/mobile/web package block and run the target release
audit.

## Chapter 11. Natural-Language Evolution

Natural language is treated as a proposal source, not an unchecked mutation.

```console
appgen --nl-plan "Add customer support tickets, a TicketForm, a SupportAgent, and targets web mobile desktop"
appgen --nl-dsl "Add customer support tickets, a TicketForm, a SupportAgent, and targets web mobile desktop"
```

Review the generated DSL, run the linter, then generate the app.

Exercise: ask for a change that adds a workflow and verify that the DSL contains
a `flow` block.

## Chapter 12. Release Evidence

Before claiming readiness, run focused gates.

```console
appgen --dsl-release-audit
appgen --source-intake-release-audit
appgen --studio-release-audit
appgen --target-release-audit
appgen --agentic-release-audit
appgen --pbc-release-audit
```

Exercise: run `appgen --dsl-antlr-report` and confirm the result is `ok: true`.

## Capstone Project

Build a service desk application:

- PBCs: `ticketing`, `customer_registry`, and `knowledge_base`.
- Tables: customers, tickets, comments, knowledge articles, assignments.
- Forms: ticket form with customer lookup and status component.
- Workflow: triage, human approval, escalation timer, compensation.
- Rules: required title, valid status, escalation conditions.
- Agent: local LLM support assistant with limited permissions.
- Contracts: API, event, job, report, menu, package, test, deployment.

Acceptance criteria:

- `appgen --lint-dsl service-desk.appgen` succeeds.
- `appgen --dsl-authoring-gate service-desk.appgen` succeeds.
- The generated app includes web, mobile, and desktop targets.
- The DSL remains readable enough for a small local coding model to regenerate.

## Reading Map

- Tutorials: `docs/language-tutorials/`
- Manual: `docs/language-manual/`
- Grammar: `docs/dsl-grammar.md`
- Linter: `docs/dsl-linter.md`
- Application generation: `docs/app-generation-guide.md`
- PBC composition: `docs/composable-pbc-apps.md`
