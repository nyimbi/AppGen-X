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
  form_designer.py       RAD-style form designer contracts
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
- RAD-style form designer workbench.
- Natural-language evolution workbench.
- Release and capability workbenches.
- Runtime assurance and diagnostics workbenches.

This workbench-first architecture lets a web IDE, desktop IDE, external plugin,
or automated agent consume the same structured contracts.
The React Studio prototype is also bound to `.github/workflows/studio-browser-smoke.yml`,
which runs `npm run test:browser` against `appgen-frontend/scripts/browser-smoke.mjs`
on a prepared CI host. `studio_browser_smoke_ci_contract()` is included in the
package Studio release audit so the browser smoke command, workflow, scenarios,
and prepared-host browser contract remain part of the required evidence.

## Visual Design Architecture

Visual design is split into two related capabilities:

- `form_designer.py` handles form components, component placement, property
  editing, responsive layouts, renderer metadata, design validation, per-component
  usability evidence, RAD parity contracts, and reviewed third-party component
  package import/install plans.
- `component_contracts/<component>.py` and `component_packages/<package>.py`
  are generated alongside the form designer so every component and package has a
  discrete, importable contract, renderer/loader surface, validation evidence,
  and test plan.
- `component_tests/test_<component>.py` and
  `component_package_tests/test_<package>.py` are generated beside those
  modules so each component and package has its own importable test surface that
  loads the generated module, asserts its contract, and runs its smoke test.
- `visual_runtime_assets.py` is generated beside the form designer so style
  bundles, animation timelines, effect fallback bundles, scene manifests, and
  visual asset manifests have a dedicated runtime validation surface.
- `data_tooling_runtime.py` is generated beside the form designer so connection
  probes, schema and lookup metadata, service publish plans, and failover replay
  contracts have a dedicated runtime validation surface.
- `component_analog_workbench()` and `component_analog_group_audit()` sit above
  the raw palette and prove requested native-style analog coverage across
  controls, layouts, data display, graphics, animation, theming, gestures,
  sensors, 3D primitives, and data access.
- `component_behavior_workbench()` proves each component is more than catalog
  metadata: it has render nodes, property validation, event dispatch metadata,
  target adapters, accessibility metadata, and side-effect-free preview behavior.
- `pascal_runtime_workbench()` validates deterministic form streaming, generated
  units, package manifests, compiler pipeline metadata, runtime type
  information, event binding lifecycle, resource streaming, form lifecycle
  hooks, incremental compile planning, diagnostic mapping, package dependency
  order, event stub evolution, resource fidelity, and runtime artifact parity.
- Its design-edit replay contract validates that property edits, preserved
  extension properties, event stub updates, resource hashes, cache
  invalidations, diagnostic routing, and runtime preview reloads happen in a
  deterministic order.
- `object_inspector_workbench()` validates the design-time metadata layer:
  property editors, event handler lifecycle, component verbs, custom designer
  hooks, editor registration, property validation, staged verb execution,
  custom designer activation, filtering/sorting modes, and persisted inspector
  state. Its editor lifecycle replay validates property value pipelines, event
  handler routing, component-editor transactions, custom designer lifecycle,
  dependency refresh, metadata round trip, design-surface replay, and custom
  designer registration in one release-ordered flow. Its design-surface
  transaction replay validates ordered selection, multi-select edit,
  component-editor, overlay, dependency refresh, diagnostic, undo/redo, and
  reference-sync behavior. Its custom designer registration replay validates
  registration, activation, overlay rendering, hit-target routing, lifecycle
  commit/cancel behavior, and metadata round trip.
- `component_analog_workbench()` validates requested component analog coverage
  across controls, layouts, data display, graphics, animation, theming,
  gestures, sensors, 3D scene primitives, and data access. It records the
  runtime adapter class for each analog before replaying behavior contracts;
  `component_analog_group_audit()` then groups that evidence by requested
  category so package and generated-app tests can prove the full list at once.
- `livebindings_workbench()` validates visual data-binding graphs, expression
  safety, converter/validator catalogs, designer interactions, and runtime
  update modes, plus link authoring operations, conflict checks, preview
  evaluation, generated runtime wiring, undo/redo history, and one ordered
  designer transaction from graph edits through diagnostics, accessibility,
  offline replay, runtime propagation, and rollback recovery. Its release
  lifecycle replay orders graph authoring, validation, staged transactions,
  diagnostics/conflicts, generated wiring, offline replay, accessibility routes,
  runtime propagation, and design/runtime replays before release approval.
- `rad_data_tooling_workbench()` validates native data tooling: connection
  profile catalogs, parameterized query design, server method and client proxy
  generation, secured resource metadata, embedded local database contracts,
  offline sync policies, conflict handling, and side-effect guards. Its publish
  transaction replay validates connection profiling, schema/query planning,
  dataset publishing, service artifacts, local/offline queues, conflict review,
  telemetry, runtime smoke, and no-write replay in one ordered flow. Its
  relationship lookup lifecycle replay validates multi-hop relationship chains,
  lookup editor generation, previewed joins, runtime lookup artifacts, and
  published lookup endpoints together.
- `mobile_native_api_workbench()` validates full listed-device-API coverage:
  permission manifests, design-time/runtime component adapters, simulator
  fixtures, platform targets, runtime permission guardrails, and an ordered
  designer transaction that carries device components through privacy review,
  revocation, lifecycle delivery, bridge recovery, and runtime dispatch. Its
  capability lifecycle replay checks each API through privacy metadata,
  permission transitions, simulator fixtures, target bridges, API-specific
  pipelines, recovery, runtime events, and designer replay.
- `cross_target_visual_depth_workbench()` validates style resources, style
  cascade authoring, animation timelines, effect-stack validation, 3D scene
  authoring, asset import budgets, preview/runtime parity, and runtime
  fallbacks. Its designer transaction replay ties style overrides, timeline
  authoring, effect fallback, scene editing, asset preview, hit testing,
  transform synchronization, and runtime delivery into one ordered contract.
  Its visual lifecycle replay ties style validation, timeline export, effect
  fallbacks, scene/material validation, asset preview diffs, hit-test routing,
  transform synchronization, runtime replay, and designer replay into one
  ordered contract.
- `design_time_package_manager_workbench()` validates package install sessions,
  compatibility matrices, palette/inspector/binding registration, isolated
  loading, rollback plans, package behavior contracts, dependency lockfile
  metadata, adapter smoke tests, isolated preview-load lifecycles, failure
  containment, uninstall cleanup, side-effect guards, and one ordered lifecycle
  transaction replay that proves install, preview, update, failure recovery,
  rollback, and unload behavior together.
- `platform_parity_lifecycle_replay_contract()` validates the whole IDE parity
  flow by replaying component coverage, form streaming, runtime replay,
  inspector and binding transactions, data-service publishing, package
  installation, device capability validation, and cross-target visual depth in
  one ordered contract.
- `platform_parity_requirement_audit_contract()` validates each explicit parity
  requirement against subsystem workbench evidence plus the ordered lifecycle
  replay, so release readiness can be traced by requirement instead of only by
  aggregate checks.
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

## Composable PBC Architecture

Packaged Business Capabilities are the platform's higher-level composition
unit for enterprise applications. `pbc.py` keeps the catalog executable instead
of prose-only: each PBC declares its mesh, owned datastore, approved
open-source datastore backend, command APIs, emitted events, consumed events,
generated tables, and optional ERP template bridge.

The composition path is:

1. Resolve a natural-language prompt, explicit selection, or starter stack to
   PBC keys.
2. Build a composition plan with one deployment unit, datastore, and approved
   datastore backend per PBC.
3. Resolve internal event dependencies and record external event obligations.
4. Select a Python-native stream processor profile for event-heavy PBCs.
   `faust_streaming` is the default for service/workflow meshes, and normal
   generated manifests omit the field so validation can normalize the platform
   decision. The generated implementation path is fixed: transactional
   outbox/inbox tables, the AppGen-X event adapter, the default service-runtime
   profile, and generated retry/idempotency/dead-letter/release audit
   contracts. Use `quix_streams` only for high-throughput event/time-series
   processing, and `bytewax` only for complex parallel dataflow transformations.
   Business logic depends on generated outbox/inbox and event-handler
   contracts; profile-specific adapters and broker choices stay behind the
   platform event layer. The Studio and natural-language generator present this
   as a generated decision, not as a free-form stream-engine picker. Exceptions
   require `stream_exception_evidence` in the PBC manifest.
   `acp_stream_processing_policy()` is the canonical policy surface and the
   release audit includes an `opinionated_stream_processing_policy` gate so
   generated apps do not drift into an uncontrolled processor matrix.
5. Render compact AppGen DSL for workbench views, outbox tables, and target
   selection.
6. Generate `pbc_runtime.py` into the produced application so the selected
   catalog entries, self-registration validator, composition workbench, and
   stream policy can be compiled and smoke-tested inside the app artifact.
7. Load package entrypoints from local source directories or importable modules,
   validate their manifests, and produce side-effect-free catalog patches.
8. Load package index files that point to local source packages or importable
   modules, then validate every entry before exposing generated catalog patches.
9. Generate and compile the application shell as part of the PBC release audit.

This keeps composable applications from collapsing into a shared database
module while still letting users select finance, supply-chain, people,
manufacturing, commerce, and customer-experience capabilities into one
application.

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
