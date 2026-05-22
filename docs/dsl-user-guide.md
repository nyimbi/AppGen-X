# AppGen DSL User Guide

Use the AppGen DSL when you want a readable source of truth for generated
applications. The same DSL can drive database schema, forms, generated REST and
GraphQL APIs, PWA assets, mobile and desktop starters, chatbots, agents,
reports, ERP templates, deployment files, and quality checks.

## Minimal App

```appgen
app Library { theme: sage; targets: web, mobile, desktop }

table Author {
  id: int pk
  name: string required search
  email: string unique
}

table Book {
  id: int pk
  title: string required search
  author_id: int required -> Author.id [many-to-one]
}
```

Generate from the DSL:

```bash
appgen --dsl library.appgen --writedir generated/app
```

Lint without generating:

```bash
appgen --lint-dsl library.appgen
```

Format in place before review:

```bash
appgen --format-dsl library.appgen
```

Format DSL text through `pyAppGen.dsl.format_dsl` or the generated
`dsl_reference.format_dsl` helper when builders need stable indentation and
spacing before review. Formatting returns before/after lint reports and does not
add keywords or apply semantic quick fixes.

IDE integrations can use `pyAppGen.dsl.dsl_language_service(source)` for a
single authoring payload: ANTLR-backed lint, parser-backed outline,
schema-aware completions, deterministic formatting preview, and language-quality
evidence. It also returns `authoring_score`, an IDE-friendly readiness score
with weighted checks and next actions for naming the app, adding data models,
designing forms, selecting targets, keeping canonical style, and formatting the
source. The outline falls back to a partial regex outline for incomplete drafts,
so editors can keep navigation and completions active while a builder is still
typing.

## Modeling Guidance

Use one table per business object. Use explicit `id: int pk` fields when you
want stable identifiers, or let AppGen add one when omitted.

If you are sketching quickly, you may write `entity` or `model` for `table`,
`form` or `screen` for `view`, and `workflow` for `flow`. AppGen accepts these
as authoring aliases before parsing, then the linter can rewrite them to the
canonical DSL so the committed language stays small.
You may also write `searchable` for `search` and `hide` for `hidden` on fields;
the parser receives the canonical modifiers, and the linter offers
`normalize_modifier_aliases`.

Use `dsl_language_quality_contract()` or the generated
`/dsl-reference/language-quality.json` endpoint when reviewing language changes.
The contract proves that the ANTLR grammar, generated parser, keyword budget,
keyword-free syntax, aliases, and learning path still fit the compact DSL goal.
Use `dsl_authoring_release_gate()` or `/dsl-reference/authoring-gate.json` when
reviewing release readiness for the whole authoring loop. The gate combines
language quality, syntax/semantic linting, formatter stability, IDE navigation,
code actions, authoring guidance, and source-family coverage for DBML, SQL,
PonyORM, live databases, and DSL files.
Use `dsl_antlr_integrity_report()` when changing the grammar: it proves the
canonical grammar, generated lexer, generated parser, token names, parser rules,
and compact keyword literals are synchronized before the language-service
contract is considered healthy.

Use `required` for fields that must be entered. Use `search` on fields that
should appear in generated search contracts. Use `hidden` for generated or
internal fields. Use `unique` for natural keys like invoice numbers and email
addresses.

Prefer arrow references:

```appgen
customer_id: int required -> Customer.id [many-to-one]
```

Existing DSL that uses `ref Customer.id` still parses so old projects can be
migrated, but `ref` is treated as a legacy contextual token rather than a
canonical keyword. Run the linter or quick-fix command to rewrite it to arrow
syntax before committing new source.

### Schema Design Checklist

Before generating, check that the DSL answers these questions:

- Which table is the source of truth for each business object?
- Which fields are identifiers, natural keys, required inputs, or searchable
  text?
- Which foreign keys need explicit cardinality metadata?
- Which fields are generated or internal and should be marked `hidden`?
- Which repeated field sets belong in a reusable group?
- Which derived fields should be calculated instead of stored?
- Which app targets are needed now: `web`, `pwa`, `mobile`, `desktop`, or
  `chatbot`?

### Reusable Groups And Derived Fields

Use groups when multiple tables share audit, tenancy, status, or import fields.

```appgen
AuditFields {
  created_at: datetime required
  updated_at: datetime
  tenant_id: int hidden
}

table Invoice {
  id: int pk
  ...AuditFields
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
}
```

The linter validates that derived-field expressions refer to fields available
on the same table.

## Designing Forms

Basic form sections:

```appgen
view BookForm for Book {
  Main: title, author_id;
}
```

Delphi-style component placement:

```appgen
view BookForm for Book {
  @ title TextBox 0 0 8 1;
  @ author_id Lookup 0 1 8 1;
}
```

The generated form designer can use these placements for drag/drop previews,
snap-to-grid placement, overlap detection, and property sheets.

Use section rows for readable forms and component placements when the exact
canvas layout matters. Component coordinates are grid values, not pixels, so
the same DSL can be adapted to web, mobile, and desktop renderers.

## Choosing Targets

Supported targets are `web`, `pwa`, `mobile`, `desktop`, and `chatbot`.

```appgen
app FieldOps { targets: web, pwa, mobile, desktop, chatbot }
```

`mobile` generates a Kivy starter. `desktop` generates a BeeWare starter.
`web` and `pwa` generate Flask-AppBuilder and PWA assets. `chatbot` generates
bot contracts and provider exports. Use `/platforms/generation-matrix.json`
and `/platforms/release-gate.json` to verify selected target packages,
capabilities, artifacts, and web/mobile/desktop readiness.
For generated Python-native targets, `native/appgen_native.py` also exposes
`native_release_gate()` to prove mobile permissions, offline sync/replay,
desktop cache replay, shared API routes, and required native package files.
When `web` is selected, AppGen also emits React, Vue, Angular, Svelte, HTMX,
and Express starter contracts under `frontends/`; use
`frontends/appgen_frontends.py` to inspect route bindings, shared API
environment variables, dev/build commands, quality checks, and the generated
front-end release gate.

## Adding Behavior

Use `flow` for state transitions:

```appgen
flow Publish {
  draft -> published
  published -> archived
}
```

Generated workflow artifacts include transition helpers, Mermaid state diagrams,
provider-neutral FSM JSON, SCXML export for state-chart tools, graph diagnostics,
and reviewed transition proposals that can be turned back into DSL.
Use `workflow_release_gate()` or `/workflows/release-gate.json` to prove
workflow artifacts, FSM/Mermaid/SCXML exports, graph diagnostics,
authorization flows, approval routes, SLA metadata, and transition runbooks
before treating generated workflow automation as release-ready.

Generated table and workflow wizards expose `wizard_release_gate()` and
`/wizards/release-gate.json`. Use this gate to prove field prompts, required
step validation, sequential progress behavior, table wizard coverage, workflow
wizard coverage, and required wizard artifacts before release.

Use `rule` for validation and decisions:

```appgen
rule PublishPolicy for Book {
  title required "Title is required"
  status in draft, published -> review
}
```

Use `role` for generated access policies:

```appgen
role Editor {
  Book: read, create, update
}
```

Use the app option `rls` when row-level security should scope a table by a
domain-specific field name:

```appgen
app FieldOps { rls: Project.org_id; targets: web, mobile, desktop }

table Project {
  id: int pk
  org_id: string required search
  name: string required
}
```

AppGen still detects conventional tenant fields such as `tenant_id`,
`account_id`, `workspace_id`, and `organization_id`, but explicit `rls`
targets make the generated tenancy helpers and PostgreSQL policy SQL
reviewable in the DSL.

Generated apps include `rls_release_gate()` and
`/row-level-security/release-gate.json`. Use them before production release to
prove the RLS catalog, tenant filters, PostgreSQL policy SQL, PostgreSQL role
sync plan, user grants, and required RLS artifacts are ready.

## Agentic Systems

Declare LLM providers separately from agents. This makes local and API-backed
providers explicit and keeps API keys out of source.

```appgen
llm LocalOps {
  provider: ollama
  mode: local
  endpoint: http://localhost:11434
  model: llama3
}

llm CloudOps {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}

agent InvoiceAssistant {
  provider: CloudOps
  goal: "Help users create and review invoices"
  tools: schema, forms, reports
}
```

Generated apps expose `/agents/release-gate.json` to verify local/API-key
provider coverage, environment-variable secret policy, agent/provider links,
tool allowlists, and execution-plan readiness without making live LLM calls.

## Natural Language Evolution

Generated apps include natural-language evolution contracts. A builder can ask
for changes such as:

```text
Create table Ticket with fields title and status, add TicketForm, add TicketReport,
add TicketDashboard, add SupportBot, and target web mobile desktop.
```

The generated change set must still be reviewed. AppGen treats natural language
as an authoring assistant, not as an unreviewed mutation path. Destructive
requests such as dropping fields or tables are captured as explicit proposals
with data-loss review, backup requirements, generated test plans, and rollback
steps instead of being silently applied.

Natural language proposals cover database tables and fields, forms, workflows,
rules, reports, dashboards, chatbots, agents, platform targets, and ERP template
modules. Report and dashboard requests are reviewed as generated application
surface changes and add report delivery plus dashboard render checks to the
generated test plan.

Generated backup pages expose `/backup/disaster-recovery.json` and
`/backup/release-gate.json` so teams can prove that JSON backups, SHA-256
manifests, autobackup schedules, retention rules, recovery runbooks, and
operator-approved restore workflows are present before release.

## Database Design Workbench

Generated apps include a Studio database workbench derived from the same DSL.
It exposes:

- table and field metadata for visual database design;
- Mermaid ERD output for diagrams;
- DBML export for external schema tools;
- SQL DDL preview for migration review;
- PonyORM entity preview for Python model comparison;
- a parameterized SQL SELECT builder with generated table/field completions and
  read-only guards;
- migration previews for proposed schema changes.

Use this workbench to round-trip between visual design and source-controlled
DSL. The DSL remains the durable source of truth.

For imported sources, check `appgen.json.source_fidelity` or
`/schema-import/fidelity.json` before regenerating. The report proves which
DBML, SQL, PonyORM, live database, or DSL source was normalized, lists the command
that generated the app, records the canonical fingerprint, and calls out
source-specific review areas before generated files are overwritten.
Use `/schema-import/release-gate.json` for the stricter proof that every source
family has validation, round-trip diff, import command, reviewed apply-plan,
fidelity, and database URL dialect evidence.
Use `/schema-import/generation-proof.json` when you need a source-by-source
matrix showing that DBML, SQL, PonyORM, live database, and DSL generation each
have validation plans, round-trip diffs, reviewed apply plans, artifact
evidence, and generated quality checks.

The generated Studio also manages a portfolio of generated applications through
`/studio/applications.json`. Use its create/import/open/export plans to build
new apps from DSL, DBML, SQL, PonyORM, or existing database URLs while keeping
source fidelity, linting, schema diffs, generation jobs, and quality gates in
one review flow. Use `/studio/application-history.json`,
`/studio/application-snapshot.json`, and `/studio/application-restore.json` to
review generated revisions, capture rollback-ready snapshots, compare changed
DSL/schema/code areas, and restore through a reviewed quality-gated plan.
Use `/studio/release-gate.json` before treating the Studio as release-ready;
it combines diagnostics, DSL linting, database workbench exports, safe SQL
guards, schema refactor plans, the parameterized query builder, generation
jobs, app portfolio management, versioned management, capability coverage,
reviewed edits, debug redaction, dependency review, and component sharing. Use
`/studio/database-design-gate.json` and `/studio/schema-refactor.json` to review
table and field rename impact across DSL, models, APIs, GraphQL, migrations,
docs, and generated tests before applying database-design changes. Use
`/studio/capability-matrix.json` when you need a compact proof that the
generated IDE covers DSL authoring, database design, application generation,
application management, versioned app management, debugging, dependency review,
reusable components, and natural-language evolution.
Use `/studio/superiority-profile.json` to show why the generated IDE goes
beyond a scaffolding CLI: it ties authoring, database design, generation,
versioned portfolio management, diagnostics, and component sharing to commands,
workflows, and release evidence.

Generated data-access workbenches expose `data_access_release_gate()` and
`/data-access/release-gate.json` to prove query and mutation readiness. The
gate checks that required artifacts exist, resources are cataloged, query
limits are capped, field projections work, saved queries export cleanly,
create/update/delete plans are reviewed, mutation audit events are emitted, and
workbench metadata is available for low-code builders.

Generated tabbed views also expose `tabbed_views_release_gate()` and
`/tabbed-views/release-gate.json` so each tabbed section has explicit allowed
roles, allowed-role access is proven, unknown roles are denied, and required tab
artifacts are present.

Generated deployment contracts live in `deploy/appgen_deploy.py`. Use
`deployment_release_gate()` before release to prove Docker, Compose, HTTPS,
Kubernetes, on-prem, AWS, GCP, Azure, PostgreSQL/MySQL, Terraform, secret
injection, smoke checks, scaling, rollback, and promotion readiness from the
generated artifacts.
Use `/lifecycle/release-gate.json` to verify environment coverage, production
configuration, release controls, promotion/domain readiness, maintenance/update
plans, feedback, user-testing sessions, issue reports, and lifecycle artifacts
before operating a generated app.

## Design-System QA

Generated apps include `branding.py`, `appgen_branding.html`, and
`static/appgen-theme.css` for design-system review. The contract exposes:

- CSS custom properties for palette, spacing, density, focus, and UI states;
- viewport contracts for mobile, tablet, desktop, and wide layouts;
- component state matrices for hover, focus, disabled, invalid, selected,
  empty, and error states;
- a visual experience quality report with palette balance, WCAG contrast ratios,
  touch readiness, viewport coverage, component-state coverage, and no-overlap
  review evidence;
- a visual regression plan that lists screenshot targets and state coverage;
- a visual test matrix for home, list, form, and dashboard surfaces across
  generated viewports.

Generated apps also include `view_experience.py` for view-level polish. Use
`/view-experience/states.json` and `/view-experience/release-gate.json` to
verify each generated page has a stable shell, layout-preserving loading state,
actionable empty state, recoverable error state, footer context, offline status,
and chatbot/help affordance.
- accessibility audit plans for focus order, landmarks, touch targets, and
  WCAG-oriented checks.

Use the generated `/branding/visual-quality.json` endpoint as the machine gate
and `/branding/ui-release-gate.json` as the aggregate ship gate when validating
that generated applications are polished across web, mobile, and desktop-sized
viewports. `/branding/visual-regression.json` remains the screenshot checklist
for browser-driven visual QA.
Use the generated `coverage_release_gate()` in
`tests/test_generated_coverage.py` to prove table, workflow, view-experience,
quality, diagnostics, and release-gate coverage before claiming generated test
coverage is complete.

Use `/runtime-assurance/excellence-gate.json` as the final generated-app
quality decision. It aggregates the release gate into seven explicit product
outcomes: beautiful, sophisticated, secure, reliable, robust, functional, and
highly capable.

## JHipster-Plus Readiness

Generated apps keep JHipster JDL interoperability while exposing a stricter
low-code capability scorecard in `low_code_features.py`. The scorecard requires
at least eleven AppGen-only gates: visual builders, schema import, native targets,
tenant isolation/security governance, agentic systems, natural-language
evolution, ERP templates, runtime Studio tooling, runtime assurance,
application composition, bidirectional JHipster migration, and the database
IDE/workbench. Use
`/low-code-features/jhipster-superset.json` to check whether a generated app is
still more capable than the JHipster baseline.
Use `/low-code-features/jhipster-superset-certification.json` for the release
gate that combines preserved JHipster overlap, AppGen-only advantage thresholds,
roadmap traceability, composition readiness, and generated artifact evidence.
Use `/low-code-features/jhipster-superiority-tiers.json` when you need the
stricter product-positioning gate: it separates preserved JHipster parity,
AppGen-only outperformance, and generated workbench routes, and it blocks
claims of superiority unless all three tiers pass.
Use `/low-code-features/jhipster-capability-depth.json` to inspect the depth
index behind the claim. Each AppGen-only advantage must show design-time,
generation-time, runtime, and governance evidence rather than only naming a
feature.
Use `/low-code-features/jhipster-frontier-gate.json` to prove advanced
JHipster capability families are still preserved and then exceeded by generated
AppGen-only capabilities before making stronger product-positioning claims.
Generated microservice apps also expose `/microservices/mesh.json` for
service-mesh mTLS, authorization, telemetry, and canary traffic-shift plans.
Use `/low-code-features/composition-release-gate.json` to prove the reusable
application-composition layer itself: block catalog depth, dependency topology,
reviewable install order, sandbox controls, package publication targets, and
artifact evidence.

The generated `jhipster/appgen_jhipster.py` contract also supports migration in
the other direction. Use `jhipster_to_appgen_dsl()` to draft AppGen DSL from the
generated JDL-shaped entity contract, `jhipster_upgrade_migration_plan()` to
plan the move into AppGen targets, and `jhipster_migration_release_gate()` to
prove the required JDL, Studio, schema-import, and AppGen-only upgrade artifacts
are present.

ERP templates are generated as deployable starter packages, not only example
tables. Use `/erp-templates/roadmap.json` for the phased implementation plan
and `/erp-templates/release-gate.json` to verify module coverage, table
blueprints, workflows, reports, migration planning, generation steps, and
required ERP template artifacts.

The same module also exposes `/low-code-features/roadmap-sources.json`, which
maps `docs/ideas.md`, `docs/base_features.md`, and `docs/Lo-code features.md`
to generated capabilities and artifacts. Treat that endpoint as the source
traceability gate before claiming roadmap coverage.

## Linting Workflow

Run the linter before code generation and before committing DSL changes:

```bash
appgen --lint-dsl library.appgen
```

Treat errors as blockers. Warnings identify risky authoring patterns such as
literal API keys or legacy `ref` syntax. Suggestions identify missing design
surfaces such as views or agent declarations.

## CI Workflow

A simple CI gate can fail builds when the DSL is not valid:

```bash
appgen --lint-dsl appgen.appgen
appgen --dsl appgen.appgen --writedir build/generated-app
python -m py_compile build/generated-app/app/models.py
```

For larger projects, add generated quality checks after compilation so schema,
API, PWA, documentation, and generated test surfaces stay aligned.
Use the generated `seed_release_gate()` before release to prove seed scenarios
are dependency ordered, validation-clean, anonymized for fixture export, backed
by SQL previews, and connected to generated coverage plus quality artifacts.
Use `reports_release_gate()` to prove generated reports cover table catalogs,
CSV exports, relationship-aware joins, three-way report paths, query plans, and
required report artifacts before relying on generated operational reporting.
Use `report_delivery_release_gate()` to prove generated report delivery has
CSV/PDF formats, download/email channels, printable previews, PDF attachments,
and required report-delivery artifacts before wiring production email.
Use `media_release_gate()` to prove generated image/file uploads have MIME and
extension validation, oversized upload rejection, sanitized storage paths,
preview contracts, and required media cockpit artifacts.
Use `dashboard_release_gate()` to verify chart catalogs, Vega-Lite render
contracts, accessibility summaries, and web/mobile/desktop renderer targets for
generated analytics dashboards.
Use `document_release_gate()` to prove generated document libraries have version
envelopes, approval workflows, retention/legal-hold policy, e-signature
payloads, audit events, and required document cockpit artifacts.
Use `inventory_release_gate()` to prove generated inventory traceability covers
barcode/RFID scan targets, stock movement, cycle counting, reconciliation,
traceability chains, mobile/offline capabilities, and required artifacts.
Use `finance_release_gate()` to verify generated ERP finance operations cover
tax profiles, currency conversion, budget forecasts, revenue recognition, batch
processing, and required finance cockpit artifacts.
Use `manufacturing_release_gate()` to verify generated manufacturing operations
cover BOM, MRP material requirements, capacity planning, production scheduling,
purchase requisitions, kanban replenishment, and required manufacturing
artifacts.
Use `search_release_gate()` to verify generated searchable-field coverage,
provider readiness for memory/PostgreSQL/Whoosh/Elasticsearch, reindex plans,
and the search cockpit artifacts before switching providers in production.
Use `/database-ops/addon-release-gate.json`, `/database-ops/patroni.json`,
`/database-ops/postgraphile.json`, and `/database-ops/zombodb.json` to verify
generated database add-ons include HA cluster, GraphQL schema, and PostgreSQL
full-text index plans before rollout.
Use `/integrations/release-gate.json` to verify REST/webhook/enterprise
connector coverage, first-class Entando and Invenio contracts, signed webhook
delivery, payment/SMS/email request plans, outbox auditability, and required
integration artifacts before custom connector code sends data.
Use `/project-management/release-gate.json` to verify generated backlog,
sprint, release-control, traceability, Jira/GitHub/Azure Boards/GitLab export,
and project-management artifact coverage before handing a generated app to a
delivery team.
Use `/data-exchange/release-gate.json` to verify schema-aware CSV templates,
JSON exchange round-trips, import validation, reviewed migration batches,
deterministic request errors, and data-exchange artifacts before loading legacy
or operational data.
Use `/productivity/release-gate.json` to verify Microsoft 365 and Google
Workspace provider coverage, schema-derived document/spreadsheet/calendar/task
payloads, and required productivity artifacts before connecting live office
suite APIs.
Use `/api-testing/release-gate.json` before release to verify API request
matrices, response validation, smoke fixtures, UI smoke plans, synthetic
monitors, OpenAPI coverage, and rendered pytest/Playwright modules.
Use `/usage-analytics/release-gate.json` to prove generated app-usage
analytics cover event catalogs, adoption, funnels, retention, real-time
snapshots, and dashboard payloads.
Use `/compliance/release-gate.json` to verify privacy request envelopes,
protected-field redaction, erasure review, retention disposition, audit events,
and compliance artifacts before a generated app is released.
Use `/identity/release-gate.json` to prove generated SSO readiness across OIDC,
SAML, LDAP, Active Directory, trusted headers, AWS Cognito OAuth, token exchange
review, and principal normalization.
