# Architecture

This document explains how AppGen is structured, how data flows through the
platform, and where major capabilities live.

## System Overview

AppGen is organized as a model-driven generation pipeline:

```text
Source inputs
  -> source adapters
  -> AppSchema
  -> generator
  -> generated application package
  -> generated Studio/IDE and release gates
  -> deployment/runtime targets
```

The central design choice is that every supported source is normalized into one
canonical application model before generation. That keeps DBML, SQL, PonyORM,
live database introspection, DSL, and natural-language evolution aligned with
the same downstream generator and audit contracts.

## Repository Structure

```text
src/pyAppGen/
  dsl.py                 DSL parser, linter, formatter, language service
  dsl_generated/         Generated ANTLR lexer/parser/listener/visitor files
  schema.py              Canonical schema data structures
  gen.py                 Main generator and CLI entrypoint
  source_intake.py       Source-family intake and release evidence
  roadmap.py             Package-level roadmap and goal audits
  studio.py              Package-level Studio/IDE contracts
  form_designer.py       Delphi-style form designer contracts
  visual_modeling.py     Visual database modeling contracts
  erp.py                 ERP template catalog and generation smoke tests
  nl.py                  Natural-language planning and DSL proposal contracts
  agentic.py             LLM provider and agent contracts
  targets.py             Web/PWA/mobile/desktop/chatbot target contracts
  security.py            Security and identity release evidence
  reporting.py           Reports, charts, dashboards
  integrations.py        Enterprise integration contracts
  ops.py                 Deployment, search, automation, backup operations
  distribution.py        Package/template publishing contracts
  config_admin.py        Generated config editor contracts
  capabilities.py        Capability taxonomy shared by audits
docs/
  DSL, platform, generation, deployment, and roadmap documentation
tests/
  Package-level and generated-artifact regression tests
```

## Core Domain Model

The canonical model is `AppSchema`. It represents:

- Application metadata and target selections.
- Tables, fields, field modifiers, defaults, derived expressions, and hidden or
  searchable fields.
- Enums.
- Relationships and cardinality metadata.
- Views and form layout sections.
- Workflows.
- Roles and permissions.
- Rules and validation/review policies.
- LLM providers and agents.
- Source-fidelity metadata.

All source adapters produce this model. All generators consume it.

## Source Adapters

AppGen supports multiple source families:

- **DSL:** parsed through the ANTLR-backed language surface in `dsl.py` and
  `dsl_generated/`.
- **DBML:** normalized into tables, fields, indexes, relations, enums, and
  grouping metadata.
- **SQL:** normalized from DDL, constraints, generated columns, enum-like
  checks, foreign keys, unique constraints, and defaults.
- **PonyORM:** parsed statically so entity declarations can be read without
  executing application code.
- **Live databases:** introspected through SQLAlchemy URLs.
- **Natural language:** converted into reviewable plans and DSL patches before
  generation.

Each adapter records source-fidelity evidence so generated apps can explain
what was preserved and what needs review.

## DSL Layer

The DSL layer has three responsibilities:

1. **Parse:** use ANTLR-generated lexer/parser artifacts to build the schema.
2. **Assist:** provide lint diagnostics, quick fixes, formatting, snippets,
   navigation, semantic summaries, and language-service payloads for IDEs.
3. **Prove:** run grammar synchronization and DSL release audits.

Important commands:

```console
appgen --lint-dsl app.appgen
appgen --format-dsl app.appgen
appgen --dsl-authoring-gate app.appgen
appgen --dsl-antlr-report
appgen --dsl-release-audit
```

The DSL intentionally keeps a compact keyword set while supporting tables,
views, workflows, roles, rules, local/API LLM providers, and agents.

## Generator Layer

`gen.py` is the main generation engine and CLI surface. It takes an `AppSchema`
and writes a generated application package. The generated package can include:

- Flask-AppBuilder models, views, API, GraphQL, templates, config, and metadata.
- Generated Studio/IDE contracts.
- DSL reference and linter helper contracts.
- Visual form designer and visual database designer contracts.
- Security, reporting, integration, ops, and deployment modules.
- Web, PWA, mobile, desktop, and chatbot target artifacts.
- ERP starter output.
- Agentic system workbenches.
- Release gates and capability evidence.

The generator favors explicit generated contracts over hidden magic. Many
capabilities are surfaced as JSON-returning functions or generated release
gates so they can be tested without a full browser session.

## Generated Application Structure

A typical generated app contains:

```text
generated/app/
  app/
    __init__.py
    models.py
    views.py
    api.py
    gql.py
    appgen.json
    studio.py
    dsl_reference.py
    form_designer.py
    designer.py
    agents.py
    platforms.py
    reports.py
    security.py
    integrations.py
    database_ops.py
    schema_import.py
    templates/
    static/
  native/
    mobile/
    desktop/
  chatbots/
  automation/
  deploy/
  Dockerfile
  docker-compose.yml
```

Not every source or target writes every file, but package audits verify the
expected contracts for each capability area.

## Studio/IDE Architecture

The generated Studio is a management and design surface layered over the
generated app. It is structured around workbench payloads:

- Application portfolio and lifecycle workbenches.
- DSL editor/language-service workbench.
- Database designer and schema-refactor workbench.
- Delphi-style form designer workbench.
- Natural-language evolution workbench.
- Release and capability workbenches.
- Runtime assurance and diagnostics workbenches.

This workbench-first architecture lets a web IDE, desktop IDE, external plugin,
or automated agent consume the same structured contracts.

## Visual Design Architecture

Visual design is split into two related capabilities:

- `form_designer.py` handles form components, component placement, property
  editing, responsive layouts, renderer metadata, and design validation.
- `visual_modeling.py` handles database graph nodes, relationships, ERD export,
  DBML/SQL/PonyORM export, schema proposals, and migration preview.
- `branding.py` handles brand/theme contracts, splash-screen configuration,
  editable navigation menus, guarded menu edit plans, right-click/context-menu
  contracts, accessibility, responsive layout evidence, and UI release gates.

The DSL remains the durable source of truth. Visual changes should produce
reviewable schema, form, or migration proposals that can flow back into DSL.

## Agentic Architecture

Agentic systems are declared in DSL with `llm` and `agent` blocks. AppGen
separates provider configuration from agent behavior:

- Providers define driver, mode, model, endpoint, and secret environment
  variable names.
- Agents define provider links, goals, allowed tools, memory scope, and step
  limits.
- Tool policy defines what each agent may inspect or propose.
- Execution matrices turn agent definitions into reviewable runtime plans.

Generated apps should treat agent output as proposals unless a human-reviewed
policy explicitly allows automatic changes.

## Target Architecture

Target generation is additive:

- `web` generates Flask-AppBuilder application surfaces.
- `pwa` adds manifest and service-worker assets.
- `mobile` adds Kivy starter files and mobile capability contracts.
- `desktop` adds BeeWare starter files and desktop capability contracts.
- `chatbot` adds Dialogflow/Bot Framework export contracts.

`targets.py` and generated `platforms.py` expose release gates that verify
target artifacts, JSON exports, runtime assets, and native readiness contracts.

## ERP Template Architecture

ERP templates are reusable starter models expressed as DSL. The template layer
provides:

- Catalog metadata.
- Exportable DSL for individual modules.
- Finance-core generation smoke tests.
- Release gates that verify ERP artifacts, reporting surfaces, native/PWA
  outputs, and generated Python compilation.

Templates should stay composable. A project can start with invoicing, inventory,
or HR and later add related modules through DSL or natural-language evolution.

## Deployment Architecture

Deployment support is generated as explicit files and workbench contracts:

- Docker and Compose for local/container releases.
- Kubernetes and autoscaling manifests for orchestration.
- Terraform stubs for cloud infrastructure.
- Caddy/HTTPS helpers for edge deployment.
- Node-RED automation exports for integration and operations flows.
- Backup, restore, search, and release evidence contracts.

Operations audits verify that deployment capabilities are present before
deployment-readiness claims are made.

## Audit Architecture

AppGen uses release audits as executable architecture documentation. Audits are
small JSON-producing contracts that answer:

- What capability is being claimed?
- What files or generated contracts prove it?
- What checks ran?
- What gaps block approval?
- What stop condition prevents premature claims?

The aggregate audit is:

```console
appgen --package-goal-audit
```

It collects roadmap traceability, source intake, DSL quality, Studio/IDE,
visual modeling, form design, ERP templates, natural-language evolution,
security, reporting, ops, integrations, agentic systems, targets, and
generated-app excellence.

## Extension Points

Common extension points:

- Add a source adapter that produces `AppSchema`.
- Add DSL syntax and update ANTLR grammar, parser artifacts, linter,
  formatter, docs, and tests together.
- Add generated files in `gen.py` and prove them with package and generated-app
  audits.
- Add Studio workbench payloads for new management features.
- Add ERP templates as DSL exports plus smoke tests.
- Add target runtimes by extending target catalogs and release gates.
- Add deployment providers by extending generated deployment assets and ops
  audits.

## Design Principles

- Keep source models authoritative and generated output reproducible.
- Normalize all source families before generation.
- Prefer reviewable proposals for natural-language and agentic changes.
- Keep DSL compact, readable, and backed by lint/format/quick-fix tooling.
- Expose generated capability evidence through structured contracts.
- Prove readiness with audits before claiming platform capability.
