# AppGen

AppGen is a Python low-code/no-code application generator and DSL toolchain for
building secure, capable business applications from existing schemas, a compact
ANTLR-backed language, or natural-language evolution prompts.

It can generate Flask-AppBuilder web applications, PWA assets, mobile and
desktop starters, chatbot exports, ERP starter modules, Studio/IDE workbenches,
database design tools, reporting surfaces, deployment assets, and agentic
systems backed by local or API-key LLM providers.

[![PyPI](https://img.shields.io/pypi/v/appgen.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/appgen.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/appgen)][python version]
[![License](https://img.shields.io/pypi/l/appgen)][license]

[![Read the documentation at https://appgen.readthedocs.io/](https://img.shields.io/readthedocs/appgen/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/nyimbi/appgen/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/nyimbi/appgen/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

## What AppGen Builds

AppGen turns a source model into a generated application package. The source can
be:

- AppGen DSL files.
- DBML files.
- SQL DDL files.
- PonyORM entity scripts.
- Live SQLAlchemy database URLs.
- Natural-language prompts that produce reviewable DSL changes.

Generated packages include:

- Flask-AppBuilder models, views, forms, APIs, GraphQL, templates, and config.
- A generated Studio/IDE for managing applications, DSL, database designs,
  form layouts, natural-language evolution, releases, and audits.
- RAD-style visual form designer contracts with drop zones, components,
  property inspectors, layout validation, and renderer metadata.
- Native data tooling contracts for connection profiles, query design, server
  methods, generated client proxies, secured resources, embedded local storage,
  offline sync, conflict handling, and side-effect guards.
- Splash-screen, editable-menu, right-click/context-menu, and UI fine-tuning
  contracts in the generated branding workbench.
- Visual database modeling exports for Mermaid ERD, DBML, SQL DDL, PonyORM, and
  migration previews.
- Web, PWA, mobile, desktop, and chatbot target artifacts.
- Agentic-system contracts with local LLM providers, API-key LLM providers,
  agents, tool policy, execution plans, and release gates.
- ERP starter modules for ledgers, accounts, invoicing, AP, AR, inventory,
  purchasing, sales, HR, payroll, CRM, projects, assets, tax, reporting, and
  approval workflows.
- Deployment and operations assets for Docker, Compose, Kubernetes, Terraform,
  HTTPS, search, Node-RED automation, backups, and release validation.

## Quick Start

Install AppGen:

```console
pip install appgen
```

Generate from a DSL file:

```console
appgen --dsl invoice.appgen --writedir generated/invoice/app
```

Generate from an existing schema:

```console
appgen --dbml schema.dbml --writedir generated/dbml-app/app
appgen --sql schema.sql --writedir generated/sql-app/app
appgen --pony entities.py --writedir generated/pony-app/app
appgen --database-url sqlite:///existing.db --writedir generated/db-app/app
```

Lint and format DSL before generation:

```console
appgen --lint-dsl invoice.appgen
appgen --format-dsl invoice.appgen
appgen --dsl-authoring-gate invoice.appgen
```

Run the aggregate readiness audit:

```console
appgen --package-goal-audit
```

The package goal audit aggregates roadmap traceability, DSL quality, source
intake, ERP templates, Studio/IDE readiness, RAD-style form design, visual
modeling, security, reporting, deployment, integrations, agentic systems,
multi-target generation, and generated-app excellence.

## Minimal DSL Example

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

Generate it:

```console
appgen --dsl invoice.appgen --writedir generated/invoice/app
```

## Command Guide

Generation commands:

```console
appgen --dsl app.appgen --writedir generated/app/app
appgen --dbml schema.dbml --writedir generated/app/app
appgen --sql schema.sql --writedir generated/app/app
appgen --pony entities.py --writedir generated/app/app
appgen --database-url postgresql+psycopg2://user@host/db --writedir generated/app/app
```

DSL authoring commands:

```console
appgen --lint-dsl app.appgen
appgen --fix-dsl app.appgen
appgen --format-dsl app.appgen
appgen --dsl-authoring-gate app.appgen
appgen --dsl-antlr-report
appgen --dsl-release-audit
```

Natural-language evolution commands:

```console
appgen --nl-plan "Add customer support tickets, a TicketForm, and a SupportAgent"
appgen --nl-dsl "Add customer support tickets, a TicketForm, and a SupportAgent"
appgen --nl-release-audit
```

ERP template commands:

```console
appgen --erp-template-catalog
appgen --erp-template invoicing
appgen --erp-template inventory
```

Release/audit commands:

```console
appgen --schema-source-audit
appgen --source-intake-release-audit
appgen --roadmap-release-audit
appgen --ideas-release-audit
appgen --base-features-release-audit
appgen --generated-app-excellence-audit
appgen --jhipster-superiority-audit
appgen --studio-release-audit
appgen --form-designer-release-audit
appgen --visual-modeling-release-audit
appgen --security-release-audit
appgen --config-release-audit
appgen --distribution-release-audit
appgen --reporting-release-audit
appgen --ops-release-audit
appgen --integration-release-audit
appgen --agentic-release-audit
appgen --target-release-audit
appgen --package-goal-audit
```

## Documentation

Core documentation:

- [Platform Guide](docs/platform-guide.md)
- [Architecture](docs/architecture.md)
- [App Generation Guide](docs/app-generation-guide.md)
- [Language Tutorials](docs/language-tutorials.md)
- [Deployment Guide](docs/deployment-guide.md)
- [DSL Reference](docs/dsl.md)
- [DSL Grammar](docs/dsl-grammar.md)
- [DSL User Guide](docs/dsl-user-guide.md)
- [DSL Tutorial](docs/dsl-tutorial.md)
- [DSL Linter Guide](docs/dsl-linter.md)

Roadmap/source documents:

- [Original Ideas Roadmap](docs/ideas.md)
- [Base Features](docs/base_features.md)
- [Low-Code Features](docs/Lo-code%20features.md)
- [ERP Features](docs/erp-features.md)

## Platform Concepts

AppGen has four major layers:

1. Source adapters normalize DSL, DBML, SQL, PonyORM, and live databases into a
   common schema model.
2. The generator writes application code, metadata, workbenches, native target
   starters, automation, deployment files, and release gates.
3. The generated Studio/IDE exposes DSL authoring, visual form design,
   database design, generation queues, natural-language change proposals,
   release management, and runtime audits.
4. Package and generated-app audits prove readiness before capability claims
   are treated as complete.

This means AppGen is not only a scaffolder. It is a model-driven application
composition platform with generated proof surfaces for the language, generated
apps, deployment artifacts, and enterprise capabilities.

## DSL Design Goals

The DSL is designed to be compact, learnable, and powerful. Its canonical
keyword vocabulary covers application declarations, tables, views, workflows,
roles, rules, LLM providers, and agents without forcing users into verbose
boilerplate.

The language supports:

- Tables, fields, enums, defaults, uniqueness, hidden/search fields, arrays,
  derived fields, and relationships.
- View sections and RAD-style component placement with coordinates.
- Workflows and transition graphs.
- Roles and rule policies.
- Local/API LLM providers and agent definitions.
- App-level target selection for web, PWA, mobile, desktop, and chatbot output.
- Beginner-friendly aliases that the linter can normalize to canonical syntax.

The grammar is ANTLR-backed, and the generated parser is checked by
`appgen --dsl-antlr-report`.

## Generated Studio/IDE

Generated apps include Studio contracts for:

- Application portfolio management.
- DSL editor state, syntax diagnostics, code actions, snippets, and formatting.
- Visual database catalog, ERD export, schema refactors, and migration preview.
- RAD-style form design with component palette and property inspector.
- native desktop and cross-target UI RAD parity contracts: DFM-style streaming, Object
  Inspector metadata, LiveBindings-style binding graphs, native data-service
  tooling, mobile device APIs, animation/effects, and 3D surface descriptors.
- A component usability gate that requires every built-in component to carry
  renderer targets, default properties, property editors, events, validation
  rules, drop defaults, binding metadata, and preview contracts.
- Generated component modules under `app/component_contracts/<component>.py`
  export `contract()`, `render()`, `validate_props()`, `preview()`, and
  `test_plan()` for each built-in component.
- A component analog workbench covers requested cross-target controls, layouts,
  data display, graphics, animation, theming, gestures, sensors, 3D surfaces,
  and data-access components with usable generated contracts.
- An Object Inspector workbench proves property editor types, event-handler
  lifecycle actions, component editor verbs, custom designer hooks, and
  persisted inspector state.
- A visual data-binding workbench proves binding graph nodes/edges, expression
  validation, converter and validator catalogs, designer gestures, and runtime
  binding modes.
- A native data tooling workbench proves connection catalogs, query designer
  metadata, server method/client proxy generation, secured resource tooling,
  embedded local database support, offline sync policies, and conflict guards.
- A mobile/native API workbench proves device API breadth, permission manifests,
  design-time component adapters, simulator profiles, and side-effect guards.
- A cross-target visual depth workbench proves style resources, animation state
  graphs, effect pipelines, 3D scene designer tools, and runtime fallbacks.
- Curated third-party component registry for useful commercial and open-source
  suites, plus reviewed package import/install plans for additional vendors.
- Generated package modules under `app/component_packages/<package>.py` export
  `package_contract()`, `install_plan()`, `load_policy()`, and `test_plan()`.
- Natural-language evolution review queues.
- Generation plans for web, PWA, mobile, desktop, and chatbot targets.
- Release gates, app history, snapshots, restore points, and capability matrix.

The package-level Studio readiness check is:

```console
appgen --studio-release-audit
```

## Agentic Systems

AppGen DSL supports `llm` and `agent` blocks. A provider can be local, such as
Ollama, or API-backed, such as OpenAI, with secrets referenced through
environment variable names rather than literal keys.

Generated agent contracts include:

- Provider readiness.
- Missing-secret checks.
- Agent/provider links.
- Tool policy.
- Execution plans.
- Release gates and workbench payloads.

The package-level check is:

```console
appgen --agentic-release-audit
```

## Deployment

Generated apps include deployment and operations assets such as Dockerfile,
Compose, Kubernetes, autoscaling, Terraform stubs, HTTPS helpers, search,
Node-RED automation, backup contracts, and release checks.

Review generated deployment readiness with:

```console
appgen --ops-release-audit
appgen --distribution-release-audit
```

See [Deployment Guide](docs/deployment-guide.md) for the deployment workflow.

## Development

Install the project in a local environment:

```console
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
```

Run tests:

```console
pytest
```

Run focused proof commands during platform work:

```console
python -m py_compile src/pyAppGen/*.py
pytest tests/test_main.py
python -m pyAppGen.gen --package-goal-audit
```

## Contributing

Contributions are welcome. Read the [Contributor Guide] and keep changes
aligned with the existing generator patterns, tests, and audit contracts.

## License

Distributed under the terms of the [MIT license][license], AppGen is free and
open source software.

## Issues

If you encounter a problem, [file an issue] with the source file or prompt,
generation command, expected output, actual output, and relevant audit result.

[pypi_]: https://pypi.org/project/appgen/
[status]: https://pypi.org/project/appgen/
[python version]: https://pypi.org/project/appgen
[read the docs]: https://appgen.readthedocs.io/
[tests]: https://github.com/nyimbi/appgen/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/nyimbi/appgen
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black
[file an issue]: https://github.com/nyimbi/appgen/issues
[license]: https://github.com/nyimbi/appgen/blob/main/LICENSE
[contributor guide]: https://github.com/nyimbi/appgen/blob/main/CONTRIBUTING.md
