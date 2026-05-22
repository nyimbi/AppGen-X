# Platform Guide

AppGen is a Python application composition platform. It combines source
intake, a compact DSL, generated application packages, generated Studio/IDE
workbenches, release gates, and deployment assets into one workflow.

## Architecture

AppGen has four layers:

1. **Source intake** normalizes DBML, SQL DDL, PonyORM scripts, live databases,
   and AppGen DSL files into one `AppSchema`.
2. **Generation** writes Flask-AppBuilder code, metadata, templates, APIs,
   GraphQL, workbenches, native target starters, chatbot exports, deployment
   files, and release gates.
3. **Studio/IDE** exposes application management, DSL authoring, database
   design, visual form design, generation queues, natural-language evolution,
   snapshots, releases, and capability evidence.
4. **Audits** prove that package-level and generated-app claims are backed by
   executable contracts.

## Core Workflows

Use AppGen in five common modes:

- **Generate from a schema:** start from DBML, SQL, PonyORM, or a live database.
- **Generate from DSL:** describe the application explicitly in AppGen DSL.
- **Design visually:** use generated Studio contracts for database modeling and
  RAD-style form design.
- **Evolve with natural language:** turn a prompt into a reviewable plan and DSL
  patch.
- **Release with evidence:** run targeted audits before claiming a capability is
  ready.

## Generated Application Contents

A generated app can include:

- `app/models.py`, `app/views.py`, `app/api.py`, `app/gql.py`, and templates.
- `app/appgen.json` with source fingerprint and generation metadata.
- `app/studio.py` and `app/templates/appgen_studio.html`.
- `app/dsl_reference.py`, linter workbench payloads, snippets, and code actions.
- `app/form_designer.py` for RAD-style drag/drop form contracts.
- `app/form_designer.py` also exposes `component_usability_workbench()` so every
  built-in palette item is proven usable before release: renderer targets,
  default properties, property editors, events, validation rules, drop defaults,
  binding metadata, and preview contracts must exist for every component.
- `app/component_contracts/<component>.py` gives every built-in component its
  own implementation contract with `contract()`, `render()`, `validate_props()`,
  `preview()`, and `test_plan()` exports.
- `component_analog_workbench()` proves analog coverage for cross-target
  controls, layout containers, data display, graphics, animations, theming,
  gestures, sensors, 3D scene primitives, and data-access components.
- `pascal_runtime_workbench()` proves deterministic form streaming, generated
  units, package manifests, compiler pipeline metadata, runtime type
  information, event binding lifecycle, resource streaming, and form lifecycle
  hooks.
- `object_inspector_workbench()` proves property editors, event editors,
  component editor verbs, custom designer hooks, filtering, sorting, and
  inspector state persistence.
- `livebindings_workbench()` proves visual data-binding graph nodes and edges,
  expression validation, converters, validators, designer gestures, and runtime
  update modes, plus link authoring operations, conflict checks, preview
  evaluation, generated runtime wiring, and undo/redo history.
- `rad_data_tooling_workbench()` proves connection catalogs, query designer
  metadata, server method and client proxy tooling, secured resource tooling,
  embedded local database support, offline sync policies, conflict handling, and
  side-effect guards.
- `mobile_native_api_workbench()` proves device API breadth, generated
  permission manifests, component adapters, simulator profiles, and permission
  guardrails.
- `cross_target_visual_depth_workbench()` proves style resources, animation
  state graphs, effect pipelines, 3D scene designer tools, and runtime
  fallbacks.
- `app/component_packages/<package>.py` gives every curated component package
  its own reviewed package contract with `package_contract()`, `install_plan()`,
  `load_policy()`, and `test_plan()` exports.
- `design_time_package_manager_workbench()` proves install session phases,
  compatibility matrices, palette/inspector/binding registration, isolated
  loading, rollback plans, and side-effect guards.
- `app/designer.py` for visual database design and ERD exports.
- `app/agents.py` for LLM providers and agent plans.
- `app/platforms.py`, `native/mobile`, `native/desktop`, PWA assets, and
  chatbot provider exports.
- `deploy/`, `Dockerfile`, `docker-compose.yml`, Kubernetes, Terraform, and
  automation files.

## Studio/IDE Capabilities

The generated Studio is the management surface for AppGen applications. It
provides contracts for:

- Creating, importing, opening, exporting, cloning, and restoring applications.
- Editing DSL with diagnostics, snippets, quick fixes, formatting, navigation,
  and authoring scores.
- Designing databases through visual catalogs, Mermaid ERD, DBML, SQL, PonyORM,
  schema refactors, and migration previews.
- Designing forms with component palettes, drop zones, coordinates, property
  inspectors, layout validation, and renderer metadata.
- Fine-tuning UI shells with splash-screen contracts, editable navigation
  menus, guarded menu edit plans, right-click/context menus, responsive design
  tokens, and visual QA workbenches.
- Managing generation queues and target outputs for web, PWA, mobile, desktop,
  and chatbot applications.
- Reviewing natural-language proposals before schema, form, workflow, report,
  chatbot, agent, or ERP changes are applied.
- Inspecting release gates, runtime assurance, app history, snapshots, and
  capability matrices.

Run the package-level Studio proof:

```console
appgen --studio-release-audit
```

## Enterprise Capabilities

AppGen includes contracts and generated surfaces for:

- Authentication, authorization, role policies, row-level security, audit logs,
  encryption metadata, and security release gates.
- Reports, chart views, dashboards, export metadata, and scheduled report
  contracts.
- Integration contracts for APIs, webhooks, CRM/ERP connectors, message
  providers, and generated integration release gates.
- ERP starter modules for finance, inventory, HR, purchasing, sales, CRM,
  projects, assets, tax, reporting, and approval workflows.
- Deployment operations including Docker, Compose, Kubernetes, Terraform, HTTPS,
  search, Node-RED, backup, and restore contracts.

## Readiness Audits

Use targeted audits while building:

```console
appgen --schema-source-audit
appgen --dsl-release-audit
appgen --studio-release-audit
appgen --form-designer-release-audit
appgen --visual-modeling-release-audit
appgen --agentic-release-audit
appgen --target-release-audit
```

Use the aggregate audit before claiming platform readiness:

```console
appgen --package-goal-audit
```

The aggregate audit should return `ok: true` and `decision: approved`.

## Recommended Project Layout

```text
my-product/
  appgen/
    app.appgen
    schema.dbml
    prompts/
  generated/
    app/
  deployment/
  docs/
```

Keep the source DSL or schema files under version control. Treat generated
output as reproducible build artifacts unless your team intentionally maintains
custom extensions in the generated app.

## Operating Model

1. Start from an existing schema or AppGen DSL.
2. Lint and run authoring gates.
3. Generate into a clean output directory.
4. Review generated metadata, Studio contracts, release gates, and target
   artifacts.
5. Run focused audits for touched capability areas.
6. Commit the source model, generated output policy, and deployment decision.
