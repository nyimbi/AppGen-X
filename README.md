# AppGen-X

**AppGen-X is an open-source application composition platform for generating
business applications from models, databases, DSL, and natural language.**

It turns a compact source definition into a working application package with
web screens, APIs, data models, visual design metadata, mobile and desktop
starters, deployment assets, ERP templates, agentic systems, and release
audits. The current Python package and CLI are still named `appgen`.

[![PyPI](https://img.shields.io/pypi/v/appgen.svg)][pypi_]
[![Python Version](https://img.shields.io/pypi/pyversions/appgen)][python version]
[![License](https://img.shields.io/pypi/l/appgen)][license]
[![Tests](https://github.com/nyimbi/AppGen-X/actions/workflows/tests.yml/badge.svg)][tests]

## Why AppGen-X

Most generators stop at scaffolding. AppGen-X is designed to keep generating,
validating, evolving, and packaging the application.

- **Start from what you have:** DSL, DBML, SQL DDL, PonyORM entities, a live
  SQLAlchemy database URL, ERP templates, or a natural-language change request.
- **Generate real application surfaces:** Flask-AppBuilder models, views, APIs,
  GraphQL, templates, config, reports, dashboards, workflow surfaces, and
  security policies.
- **Design visually:** generated Studio workbenches cover DSL editing, database
  design, visual form layout, component drops, property inspectors, data
  bindings, package management, device APIs, and target packaging.
- **Target more than the browser:** web, PWA, mobile, desktop, and chatbot
  artifacts are generated from the same source model.
- **Build enterprise apps faster:** ERP starter modules cover ledgers, accounts,
  invoicing, AP, AR, inventory, purchasing, sales, HR, payroll, CRM, projects,
  assets, tax, reporting, and approvals.
- **Compose business capabilities:** select packaged business capabilities
  across finance, supply chain, people, manufacturing, commerce, and customer
  experience, then generate an application from the chosen bounded contexts.
- **Use agents deliberately:** model local or API-backed LLM providers, agents,
  tools, execution policy, and release checks in the same source language.
- **Prove readiness:** release audits verify source intake, DSL quality,
  Studio/IDE readiness, form design, data tooling, security, deployment,
  integrations, targets, packages, and generated-app excellence.

## Quick Start

Install the CLI:

```console
pip install appgen
```

Create `invoice.appgen`:

```appgen
app InvoiceDesk { theme: sage; targets: web, pwa, mobile, desktop, chatbot }

table Customer {
  id: int pk
  name: string required search
  email: email unique
}

table Invoice {
  id: int pk
  invoice_number: string required unique search
  customer_id: int required -> Customer.id [many-to-one]
  status: string default "draft" search
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
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
}

llm LocalAssistant {
  provider: ollama
  mode: local
  model: llama3
  endpoint: "http://localhost:11434"
}

agent InvoiceReviewer {
  provider: LocalAssistant
  goal: "Review invoices for missing customer, tax, and line totals"
  tools: schema, forms, reports
}
```

Lint and generate:

```console
appgen --lint-dsl invoice.appgen
appgen --dsl invoice.appgen --writedir generated/invoice/app
```

Run the aggregate readiness audit:

```console
appgen --package-goal-audit
```

## Generate From Existing Sources

```console
appgen --dbml schema.dbml --writedir generated/dbml-app/app
appgen --sql schema.sql --writedir generated/sql-app/app
appgen --pony entities.py --writedir generated/pony-app/app
appgen --database-url sqlite:///existing.db --writedir generated/db-app/app
```

Natural-language evolution produces reviewable plans and DSL patches:

```console
appgen --nl-plan "Add support tickets, a TicketForm, a SupportAgent, and targets web mobile desktop"
appgen --nl-dsl "Add support tickets, a TicketForm, a SupportAgent, and targets web mobile desktop"
```

Composable PBC helpers let the platform resolve enterprise requests to
bounded-context selections, composition plans, and generated DSL starters:

```python
from pyAppGen.pbc import pbc_selection_from_prompt

selection = pbc_selection_from_prompt(
    "Build an enterprise ERP back office with GL, AP, AR, inventory, people, and order management"
)
assert selection["composition"]["ok"]
```

PBC packages can also self-register through a manifest entrypoint. Start with
the [PBC Specification](docs/pbc-specification.md), validate the manifest, and
run the PBC release audit before publishing:

```console
appgen --pbc-catalog
appgen --pbc-topology
appgen --pbc-release-audit
appgen --pbc-dsl application_composition_platform > acp.appgen
```

Event processing is intentionally opinionated: generated PBCs use
the AppGen-X event contract, and the runtime profile is platform-owned
metadata. Developers should omit `stream_processor` in ordinary manifests and
let the platform normalize the profile, generate the outbox/inbox contracts,
and wire handlers through the generated event adapter.
The implementation path is fixed for normal work: generated transactional
outbox/inbox tables, the AppGen-X event adapter, the `faust_streaming`
service-runtime profile, and generated retry/idempotency/dead-letter/release
audit contracts. Broker or runtime details below that adapter are platform
infrastructure, not a user-facing design choice.
The Studio and natural-language generator should not ask users to compare stream
libraries; they should model events, handlers, retries, idempotency, and
dead-letter behavior while the platform owns the adapter choice. `quix_streams`
and `bytewax` are documented exception profiles only. See the
[Opinionated Event Processing Standard](docs/kafka-alternatives.md) before
adding a stream-heavy PBC. Exception profiles must carry
`stream_exception_evidence` in the manifest, so generated agents can reject
unsupported choices without asking the user to compare stream libraries.
The executable policy also exposes `developer_guidance`, which is the contract
for Studio controls, DSL linting, natural-language generation, and external
coding agents: ordinary apps get one generated adapter path; exceptions are
evidence-driven release-audit workflows.
For token-constrained tools and coding agents, consume
`acp_event_processing_developer_guidance()` and use its short answer directly:
`Use appgen_event_contract. Omit stream_processor.`
The same helper returns `developer_default_stack`, which is the full
developer-facing answer: PostgreSQL by default or MySQL/MariaDB when that is the
project standard, generated `appgen_outbox_event` and `appgen_inbox_event`
tables, typed command/event handlers, the AppGen-X event adapter, and generated
idempotency/retry/dead-letter/release evidence.
The returned `decision_brief` is the one-card contract for templates, DSL
linting, Studio controls, and small local models: show the event contract
designer, handler registry, retry/idempotency/dead-letter controls, and
read-only runtime profile badge; hide stream-engine pickers and per-PBC runtime
preferences for ordinary generated work.
The returned `implementation_playbook` is the contributor checklist: Studio,
DSL linting, natural-language generation, package templates, and coding-agent
prompts all build the same ordinary path and hide runtime matrices.
The policy also returns `developer_decision_record` with the stable id
`appgen.event-processing.standard.v1`. Treat it as the support-matrix cap:
ordinary generated applications have one public event contract, zero visible
stream-engine choices, zero visible runtime-profile choices, two audited
exception profiles, and one stream profile per PBC.
The policy also exposes a first-match `developer_choice_algorithm`: ordinary
business, ERP, workflow, chatbot, agent, integration, and PBC event handling
always generate the AppGen-X event contract with `stream_processor` omitted;
only telemetry/time-series and complex dataflow PBCs can request audited
exception profiles.
Generators should call `resolve_acp_event_processing_choice()` when they need
the actual action: it returns the ordinary contract for normal work, falls back
to the ordinary contract when an exception candidate lacks evidence, and opens a
split specialized PBC only when `stream_exception_evidence` is present.

ERP starters can be exported and generated immediately:

```console
appgen --erp-template-catalog
appgen --erp-template invoicing > invoicing.appgen
appgen --dsl invoicing.appgen --writedir generated/invoicing/app
```

## What Gets Generated

A generated AppGen-X package can include:

- `app/models.py`, `app/views.py`, `app/api.py`, `app/gql.py`, templates, and
  Flask-AppBuilder config.
- `app/studio.py` for generated IDE and application-management contracts.
- `app/dsl_reference.py` for generated language guidance and linter helpers.
- `app/form_designer.py` for visual form layout, component metadata,
  design-time streaming, property inspectors, event handlers, and designer
  release gates.
- `app/designer.py` for visual database modeling, ERD export, schema refactors,
  migration previews, and source regeneration.
- `app/data_access.py` and related modules for connection profiles, query
  design, service publishing, local storage, offline queues, and replay guards.
- `app/branding.py` for themes, splash screens, menus, context menus, layout
  tuning, accessibility, and visual release gates.
- `app/agents.py` for local/API LLM provider contracts, agents, tool policy,
  execution plans, and release checks.
- `app/component_contracts/` and `app/component_packages/` for generated
  component and package metadata.
- `native/mobile/`, `native/desktop/`, PWA assets, chatbot exports, front-end
  starter packages, SDKs, deployment assets, and generated tests.

## Platform Highlights

### Visual App Studio

AppGen-X is building toward a full generated IDE, not just a command line. The
Studio contracts cover:

- Application portfolio and version history.
- DSL editor state, diagnostics, code actions, snippets, and formatting.
- Visual database design, schema diffs, relationship lookups, and migration
  previews.
- Component palette, form canvas, property inspectors, event editors, custom
  designers, and safe handler invocation.
- Visual data-binding graphs, converters, validators, conflict checks, runtime
  wiring, undo/redo, offline replay, and rollback.
- Data service publishing, local embedded storage contracts, failover, retry,
  replay, and generated lookup editors.
- Device API permissions, privacy metadata, target bridges, simulator fixtures,
  lifecycle replay, and designer transactions.
- Style resources, animation timelines, effect stacks, 3D scene metadata, asset
  budgets, preview/runtime parity, and runtime fallbacks.
- Package installation, trust validation, signature checks, adapter smoke
  tests, lifecycle execution, failure isolation, and rollback.

### Multi-Target Output

AppGen-X can generate contracts and starter artifacts for:

- **Web:** Flask-AppBuilder screens, REST APIs, GraphQL, templates, and role
  policies.
- **PWA:** manifest, service worker, offline shell, app icons, and install
  contracts.
- **Mobile:** native starter package, permissions, offline queue contracts,
  device capability metadata, sync plans, and binary adapter transcript audits.
- **Desktop:** native starter package, local file/cache contracts, keyboard
  navigation, sync replay, and produced artifact manifest checks.
- **Chatbots:** provider exports, required-field prompts, guided creation, and
  handoff flows.

### Verification-First Generation

The project treats every major capability as something that must be provable.
Useful gates include:

```console
appgen --dsl-release-audit
appgen --source-intake-release-audit
appgen --studio-release-audit
appgen --form-designer-release-audit
appgen --target-release-audit
appgen --target-binary-adapter-audit
appgen --agentic-release-audit
appgen --distribution-release-audit
appgen --package-goal-audit
```

## Repository Development

Clone and set up a development environment:

```console
git clone https://github.com/nyimbi/AppGen-X.git
cd AppGen-X
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
```

Run the main test suite:

```console
pytest
```

Run focused checks while working on platform features:

```console
python -m py_compile src/pyAppGen/*.py
pytest tests/test_main.py::test_package_goal_audit_cli_aggregates_objective_evidence
appgen --package-goal-audit
```

Frontend Studio prototype:

```console
cd appgen-frontend
npm install
npm run build
npm run test:browser
npm run dev
```

## Contributor Guide

AppGen-X needs contributors across language design, code generation, frontend
Studio work, databases, ERP, security, deployment, and documentation.

Good first contribution areas:

- Add DSL examples and tutorials for real business domains.
- Improve generated templates and UI workbenches.
- Add source-intake fixtures for DBML, SQL, PonyORM, or live database schemas.
- Expand ERP starter modules and reports.
- Add focused release-gate tests for a missing generator contract.
- Improve generated mobile, desktop, PWA, and chatbot starter artifacts.
- Harden package lifecycle, trust, rollback, and signature validation evidence.
- Polish documentation for users who are new to model-driven generation.

Before opening a pull request:

1. Keep generated capability claims backed by tests or release audits.
2. Prefer existing generator patterns before adding new abstractions.
3. Keep handwritten extensions separate from generated files.
4. Run the focused tests for the area you changed.
5. Include the command output or audit result that proves the change.

Read the [Contributor Guide](docs/contributing.md) and [Architecture](docs/architecture.md)
before larger changes.

## Documentation

- [Platform Guide](docs/platform-guide.md)
- [Architecture](docs/architecture.md)
- [App Generation Guide](docs/app-generation-guide.md)
- [Language Tutorials](docs/language-tutorials.md)
- [Deployment Guide](docs/deployment-guide.md)
- [Composable PBC Applications](docs/composable-pbc-apps.md)
- [PBC Specification](docs/pbc-specification.md)
- [DSL Reference](docs/dsl.md)
- [DSL Grammar](docs/dsl-grammar.md)
- [DSL User Guide](docs/dsl-user-guide.md)
- [DSL Tutorial](docs/dsl-tutorial.md)
- [DSL Linter Guide](docs/dsl-linter.md)
- [ERP Features](docs/erp-features.md)
- [Low-Code Features](docs/Lo-code%20features.md)

## Current Status

AppGen-X is under active development. The repository already contains a large
Python generator, DSL parser, release-audit suite, documentation set, generated
target contracts, and a React-based Studio prototype. Some generated target
outputs are starter packages and proof contracts rather than production-ready
native applications. The direction is clear: keep replacing aspirational
metadata with executable generation, tests, release gates, and usable IDE
surfaces.

## License

Distributed under the terms of the [MIT license][license], AppGen-X is free and
open-source software.

## Issues

Please [file an issue] with:

- The source file, schema, prompt, or command you used.
- Expected output and actual output.
- The relevant generated files.
- Any release-audit or test result that failed.

[pypi_]: https://pypi.org/project/appgen/
[python version]: https://pypi.org/project/appgen
[tests]: https://github.com/nyimbi/AppGen-X/actions
[file an issue]: https://github.com/nyimbi/AppGen-X/issues
[license]: https://github.com/nyimbi/AppGen-X/blob/main/LICENSE
