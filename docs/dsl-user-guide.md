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
Use `dsl_language_ergonomics_contract()` or
`/dsl-reference/language-ergonomics.json` when reviewing whether the language
is still pleasant to author. It proves aliases, keyword-free syntax, legacy-ref
quick fixes, formatter stability, learning path, completion-ready samples, and
DBML/SQL/PonyORM/database/DSL source guidance.
Use `dsl_language_experience_gate()` or
`/dsl-reference/language-experience-gate.json` for the outcome gate. It proves
the DSL is delightful to edit, intuitive to learn, functional across data,
forms, workflows, and agentic constructs, ANTLR-backed, keyword-limited, and
ready for DBML/SQL/PonyORM/database/DSL generation sources.
Use `dsl_authoring_release_gate()` or `/dsl-reference/authoring-gate.json` when
reviewing release readiness for the whole authoring loop. The gate combines
language quality, syntax/semantic linting, formatter stability, IDE navigation,
code actions, authoring guidance, language ergonomics, language experience, and
source-family coverage for DBML, SQL, PonyORM, live databases, and DSL files.
Use `dsl_antlr_integrity_report()` when changing the grammar: it proves the
canonical grammar, generated lexer, generated parser, token names, parser rules,
and compact keyword literals are synchronized before the language-service
contract is considered healthy.
Use `schema_source_example_audit()` when validating source imports. It creates
small DBML, SQL, PonyORM, live SQLite database, and DSL examples, runs the real
adapters, and verifies that every family produces an `AppSchema` with tables,
relations, fingerprints, fidelity reports, and generation commands.
Run `appgen --schema-source-audit` to emit the same release proof as JSON from
the command line.
Run `appgen --source-intake-release-audit` to promote DBML, SQL, PonyORM,
database URL, and DSL intake into package-level release evidence. It also
generates temporary apps from all five source families, verifies source-fidelity
manifests, and compiles core generated Python artifacts.
Run `appgen --dsl-antlr-report` before grammar releases to prove the canonical
grammar, generated lexer, and generated parser remain synchronized.
Run `appgen --dsl-authoring-gate appgen.appgen` when reviewing a concrete DSL
file for release readiness across linting, formatting, language ergonomics,
source coverage, and IDE support.
Run `appgen --dsl-release-audit` when reviewing the package-level DSL contract:
it aggregates the authoring gate, ANTLR grammar sync, linter diagnostics and
quick fixes, grammar/user-guide/tutorial/linter docs, CLI commands, and
generated DSL reference artifacts. It also generates a temporary app and
executes the generated DSL reference helpers for language quality, authoring
gates, quick fixes, and formatting.
Run `appgen --roadmap-release-audit` when reviewing whether the package-level
capability map still satisfies `docs/ideas.md`, `docs/base_features.md`, and
`docs/Lo-code features.md`.
Run `appgen --jhipster-superiority-audit` before making product claims that
AppGen is more capable than JHipster; it checks preserved baseline capabilities
and AppGen-only advantage areas.
Run `appgen --generated-app-excellence-audit` before claiming generated apps are
beautiful, sophisticated, secure, reliable, robust, functional, and highly
capable. It generates a temporary app, compiles generated excellence artifacts,
runs the generated quality script, and exercises runtime-assurance plus
UI-experience excellence gates.
Run `appgen --ideas-release-audit` to prove the original `docs/ideas.md`
roadmap entries, from JHipster and source intake through deployment, DBScript
language ideas, reporting, RLS, tabbed permissions, and autobackup, map to
implemented package capability evidence.
Run `appgen --base-features-release-audit` to prove every numbered baseline
feature and platform bullet in `docs/base_features.md` maps to implemented
package capability evidence.
Run `appgen --package-goal-audit` to collect roadmap traceability, JHipster
superiority, generated-app excellence, ideas-roadmap coverage, base-feature
coverage, DSL quality, schema source intake, ERP template, and natural-language
evolution evidence into one package-level JSON bundle.
Run `appgen --erp-template-catalog` to list package-level ERP starter modules,
then `appgen --erp-template invoicing > invoicing.appgen` to export a module as
DSL before generating it with `appgen --dsl`. The ERP release audit also
generates a temporary finance-core ERP starter, verifies core ledger/AP/AR,
invoicing, and reporting tables, checks generated ERP/native/PWA artifacts, and
compiles generated ERP-facing Python modules.
Run `appgen --nl-plan "create table Ticket with fields title required and form
TicketForm agent SupportAgent targets web mobile desktop"` to produce an
audited natural-language change set. Run `appgen --nl-dsl "..."` to emit the
reviewable DSL patch, and `appgen --nl-release-audit` to prove the package-level
NL evolution contract covers tables, fields, forms, workflows, rules, reports,
dashboards, chatbots, agents, ERP modules, platform targets, local LLMs, and
API-key LLMs. The audit also generates a temporary app from an NL-produced DSL
patch, compiles core Python artifacts, and checks native/chatbot/PWA outputs.
Run `appgen --studio-release-audit` to prove the package-level Studio contract
is ready for DSL editing, database design, multi-source intake, generation job
management, and application lifecycle management before any app is generated.
The audit also generates a temporary Studio app, verifies generated IDE,
database-ops, DSL-reference, migration, and quality artifacts, compiles
Studio-facing Python modules, and exercises the generated workspace, DSL editor,
database designer, generation queue, portfolio, release gate, and IDE
superiority contracts.
Run `appgen --form-designer-release-audit` to prove the package-level
Delphi-style form designer has draggable palette categories, snap-to-grid
drop proposals, property inspectors, placement suggestions, overlap guardrails,
and generated form-designer artifact coverage before release. The audit also
generates a temporary app from Delphi-style component placement DSL, verifies
generated form designer, template, model, view, and DSL-reference artifacts,
compiles generated form-designer-facing modules, and exercises generated
palette, catalog, canvas, drop, release-gate, and workbench contracts.
Run `appgen --visual-modeling-release-audit` to prove package-level visual
schema graphs, Mermaid ERDs, DBML/SQL/PonyORM/DSL exports, visual
table/field/relationship proposals, migration previews, and code/database
generation plans before release. The audit also generates a temporary app from
the visual-model DSL, verifies generated designer, template, manifest, model,
view, and migration artifacts, compiles generated designer-facing modules, and
exercises generated graph, ERD, proposal, migration, DSL-regeneration,
workbench, and release-gate contracts.
Run `appgen --security-release-audit` to prove package-level RBAC, authorization
audit events, OIDC/SAML/LDAP/Active Directory/AWS Cognito SSO contracts,
tenant/RLS policy SQL, session hardening, compliance/privacy controls, secret
scanning, and generated security artifact coverage before release. The audit
also generates a temporary app from the security DSL sample, compiles generated
security-facing modules, and exercises generated RBAC, runtime-security,
identity, tenancy, RLS, compliance, workbench, and release-gate contracts.
Run `appgen --config-release-audit` to prove the package-level configuration
editor contract has roadmap-required FAB API flags, whitelisted editable keys,
production safety checks, and environment export coverage.
Run `appgen --distribution-release-audit` to prove publishable package
metadata, Cookiecutter templates, Flask-AppBuilder extension hooks, generated
coverage tests, and seed-script contracts are present before release.
Run `appgen --reporting-release-audit` to prove every table has a report,
relations have join reports, two-hop paths have 3-way reports, ChartView
contracts exist, and PDF/email report delivery is covered. The audit also
generates a temporary reporting app, verifies generated report, delivery,
dashboard, template, model, and view artifacts, compiles the generated reporting
stack, and exercises generated table/join/3-way catalogs, CSV export, PDF
rendering, email payloads, dashboard chart rendering, workbench, and release
gates.
Run `appgen --ops-release-audit` to prove Docker, Kubernetes, Terraform cloud
targets, automatic HTTPS, Elasticsearch, Whoosh, default Node-RED, and database
operations contracts are covered before release. The audit also generates a
temporary app, compiles generated deployment, HTTPS, search, database-ops, and
Node-RED modules, and exercises generated deployment runbooks, autoscaling, TLS
readiness, search provider mappings, database HA/add-on plans, migration
cutover, NoSQL projections, Node-RED flow validation, workbench, and
release-gate contracts.
Run `appgen --integration-release-audit` to prove REST/webhook, Salesforce,
SAP, Entando, Invenio, Stripe, M-Pesa, Twilio SMS, and SendGrid email
connectors, signed delivery, idempotency, and portal/repository contracts are
covered before release. The audit also generates a temporary app, compiles the
generated integration module, and exercises generated connector catalog,
Entando/Invenio contracts, signed webhook delivery, outbox audit events,
payment/SMS/email plans, portal publication, repository deposit, workbench, and
release-gate contracts.
Run `appgen --agentic-release-audit` to prove DSL `llm`/`agent` blocks, local
Ollama/LM Studio providers, API-key OpenAI/Anthropic providers, secret
guardrails, reviewed tool policies, execution matrices, and generated agent
artifacts are covered before release. The audit also generates a temporary app
from the agentic DSL sample, compiles generated agent modules, and exercises
generated local/API-key provider readiness, agent plans, tool policies,
execution matrices, workbench, and release-gate contracts.
Run `appgen --target-release-audit` to prove web, PWA, mobile, desktop, and
chatbot target selection, generated package artifacts, compiled Python target
modules, JSON provider exports, PWA runtime assets, Kivy mobile
permissions/offline queues, and BeeWare desktop local-cache/sync contracts are
covered before release.

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

Use `/components/release-gate.json` or `component_release_gate()` before
publishing a component library. The gate proves reusable component coverage,
widget registry depth, web/mobile/desktop renderers, lookup contracts, calendar
widgets, layout contracts, custom-widget extension points, visual-builder
payloads, and required artifacts.

Use `/form-designer/release-gate.json` or `form_designer_release_gate()` before
shipping a generated visual builder. The gate proves the component palette is
wide enough for business forms, the canvas contract is stable, fields map to
appropriate components, dropped components include property-inspector metadata,
and overlap detection blocks invalid layouts.

Use `/view-composition/release-gate.json` or
`view_composition_release_gate()` before publishing composed screens. The gate
proves MasterDetailView contracts, optional MultipleView group integrity,
ChartView field coverage, aggregate catalog shape, generated FAB view-class
support, and required artifacts.

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
Generated SDK contracts expose `sdk_release_gate()` in `sdks/appgen_sdks.py` to
prove Python, JavaScript, Java, and C# client coverage, scaffold artifacts,
REST route catalogs, client method names, and OpenAPI path alignment.

Generated apps include `/localization/` for translation catalog review. Use
`/localization/release-gate.json` or `i18n_release_gate()` before publishing a
localized app to prove Babel artifacts, locale metadata, default catalog
coverage, fallback translation behavior, locale negotiation, missing-key
reports, and runtime payload shape.
Use `/localization/workbench.json` or `i18n_workbench()` inside the IDE to
inspect locale catalogs, fallback behavior, negotiated payloads, missing-key
reports, artifact readiness, and route evidence.

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

Generated apps include `/resilience/` for exception-management review. Use
`/resilience/release-gate.json` or `resilience_release_gate()` before release
to prove required resilience artifacts, exception taxonomy, safe user-facing
responses, retry and circuit-breaker behavior, incident reports, and the
exception-management plan.
Use `/resilience/workbench.json` or `resilience_workbench()` to inspect
taxonomy, safe responses, retry and circuit-breaker evidence, incident reports,
routes, artifacts, and release-gate evidence.

Use `rule` for validation and decisions:

```appgen
rule PublishPolicy for Book {
  title required "Title is required"
  status in draft, published -> review
}
```

Generated business rules expose `rules_release_gate()` and
`/rules/release-gate.json`. Use this gate to prove rule catalogs, validation
success/error behavior, branch decision plans, decision-tree exports, decision
traces, and required rule artifacts before treating low-code customization as
release-ready.

Generated schema validation exposes `validation_release_gate()` to prove
field-level and payload-level contracts before generated forms, APIs, imports,
or chatbots accept writes. The gate checks valid payloads, required-field
errors, partial updates, UI validation schemas, enum errors, type errors, and
the required validation artifact.

Use `role` for generated access policies:

```appgen
role Editor {
  Book: read, create, update
}
```

Use `security_workbench()` in generated `app/security.py` to inspect policy
matrix, authorization decision, audit event, RBAC change proposal, resource
catalog, threat model, secret scan, dependency review, API security tests,
release gate, and signoff evidence before publishing an app.
Use `/runtime-security/workbench.json` or `runtime_security_workbench()` to
inspect generated idle-timeout policy, public-path bypasses, expired and active
session states, activity markers, security headers, route coverage, and release
gate evidence.

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
Use `/tenancy/workbench.json` or `tenancy_workbench()` in the generated IDE to
inspect tenant catalogs, context sources, filter helpers, tenant requirement
checks, route coverage, and release readiness for the multi-tenant helper layer.

Generated apps include `rls_release_gate()` and
`/row-level-security/release-gate.json`. Use them before production release to
prove the RLS catalog, tenant filters, PostgreSQL policy SQL, PostgreSQL role
sync plan, user grants, and required RLS artifacts are ready.
Use `/row-level-security/workbench.json` or `rls_workbench()` to inspect policy
catalog, tenant filter behavior, row filtering, PostgreSQL policy SQL, tenant
session SQL, role sync, artifact, route, and release-gate evidence.

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

Use `/assistant/workbench.json`, `assistant_workbench()`,
`/assistant/release-gate.json`, or `assistant_release_gate()` before shipping
generated AI assistance. The workbench and gate prove prompt context excludes
hidden fields, chatbot questions cover visible and required fields, prediction
features stay within visible fields, recommendations catch missing required
values, route coverage is present, and human-review tasks carry context for
assisted changes.

Use `/intelligence/workbench.json`, `intelligence_workbench()`,
`/intelligence/release-gate.json`, or `intelligence_release_gate()` before
shipping generated AI analytics. The workbench and gate prove table feature
catalogs, anomaly and recommendation behavior, NLP helpers, local and API
vision plans, A/B assignment, predictive-maintenance signals, route coverage,
and required cockpit artifacts without invoking external model APIs.

Use `/guided-chatbot/release-gate.json` or `chatbot_release_gate()` before
shipping generated in-app chatbots. The gate proves generated intents exist,
field prompts cover required values, incomplete conversations block create
payloads, answered conversations progress to readiness, and create payloads are
scoped to the target table.
Use `/voice/release-gate.json` or `voice_release_gate()` before publishing
speech interfaces. The gate proves Alexa, Google Assistant, and Web Speech
exports are present, utterances match generated intents, required slots block
incomplete requests, ready responses render valid SSML, and platform model
exports contain generated commands.
Use `/voice/workbench.json` or `voice_workbench()` while designing speech
interfaces in the IDE. The workbench returns provider catalogs, utterance
matching checks, slot-filling plans, SSML previews, platform model exports,
artifact readiness, and route evidence for the generated voice surface.

Use `/text-quality/release-gate.json` or `text_quality_release_gate()` before
shipping generated long-form inputs. The gate proves textarea quality catalogs,
character and word counters, grammar hints, repeated-word detection,
required-field enforcement, hard length limits, and per-form feedback without
requiring external NLP services.

Use `/notifications/release-gate.json` or `notification_release_gate()` before
shipping generated notification flows. The gate proves in-app, email, webhook,
and push channel coverage, environment-variable secret policy, table event
coverage, payload shape, queue metadata, and unknown-channel guardrails without
dispatching external messages.

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

Use `/nl-evolution/release-gate.json` or `nl_evolution_release_gate()` before
allowing natural-language app changes into a release. The gate proves generated
artifacts are present, the sample plain-language plan covers schema, UI,
automation, chatbot, agent, ERP, and target changes, reviewable change sets are
created, destructive requests require backups, and generated test plans include
DSL lint, migration preview, UI smoke, agent readiness, report/dashboard, and
platform-target checks.

Before generation, the package CLI exposes the same idea with
`appgen --nl-plan`, `appgen --nl-dsl`, and `appgen --nl-release-audit`.
`--nl-dsl` emits parseable AppGen DSL for schema, forms, flows, rules, local and
API-key LLM providers, agents, and requested ERP module tables/flows; report,
dashboard, and chatbot requests remain explicit review comments so the builder
can apply them deliberately.

Generated backup pages expose `/backups/disaster-recovery.json` and
`/backups/release-gate.json` so teams can prove that JSON backups, SHA-256
manifests, autobackup schedules, retention rules, recovery runbooks, and
operator-approved restore workflows are present before release.
Use `/backups/workbench.json` or `backup_workbench()` in the generated IDE to
inspect payload validation, manifest integrity, schedule, retention, recovery,
DR, route coverage, and release readiness together.

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

Use `/designer/schema-diagram-release-gate.json` or
`schema_diagram_release_gate()` before claiming database-design readiness. The
gate proves generated designer artifacts, visual graph completeness, Mermaid
ERD coverage, relationship metadata, diagram checks, and reviewed migration
preview evidence.

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
the package-level `appgen --studio-release-audit` before generation to verify
the same IDE readiness contract exists outside a generated app. The package
audit includes a generation smoke that writes and compiles a temporary generated
Studio app and executes its workspace, DSL editor, database designer, generation,
application portfolio, release-gate, and superiority contracts. Use
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

Generated configuration editors expose `config_admin_release_gate()` and
`/appgen/config/release-gate.json`. Use this gate to prove editable
`config.py` coverage, production readiness, unsafe blocker detection, safe
assignment rewriting, setup checklist coverage, and `.env` export behavior
before promoting generated setup screens.
Use `/appgen/config/workbench.json` or `config_admin_workbench()` in the
generated IDE to inspect the editable config schema, grouped sections, setup
readiness, setup checklist, safe rewrite proof, environment export, route
surface, and release gate together.

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
Use `deployment_workbench()` to inspect target coverage, artifact coverage,
database engines, AWS/GCP/Azure readiness, Terraform artifacts, Kubernetes
autoscaling, secret injection, smoke checks, runbooks, rollback, promotion,
on-prem readiness, and release-gate evidence.
Use `https_workbench()` in `deploy/appgen_https.py` to inspect automatic HTTPS
artifact coverage, public TLS environment, localhost fallback, Caddy upstream,
ports, HSTS/header contract, and release-gate evidence.
Use `/lifecycle/release-gate.json` to verify environment coverage, production
configuration, release controls, promotion/domain readiness, maintenance/update
plans, feedback, user-testing sessions, issue reports, and lifecycle artifacts
before operating a generated app.
Use `/lifecycle/workbench.json` or `lifecycle_workbench()` in the generated IDE
to inspect environment catalogs, production readiness, release controls,
promotion/domain evidence, maintenance/update plans, feedback/testing/issue
loops, route coverage, and release readiness together.
Use `/emerging/workbench.json`, `emerging_workbench()`,
`/emerging/release-gate.json`, or `emerging_release_gate()` before promoting
generated IoT or blockchain adapters. The workbench and gate prove device
catalogs, telemetry validation, command guardrails, hash-only blockchain anchor
verification, smart-contract adapter plans, edge/offline buffering, retry
guidance, route coverage, and required emerging-tech cockpit artifacts without
connecting to external devices or networks.

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

Generated apps include `/support-center/` for built-in learning and help. Use
`/support-center/release-gate.json` or `support_center_release_gate()` before
shipping onboarding content to prove knowledge-base coverage, guided tutorials,
builder/admin/end-user onboarding, support search, sample DSL starters, and
support-ticket correlation.
Use `/support-center/workbench.json` or `support_center_workbench()` inside the
IDE to inspect support topics, tutorials, role-specific onboarding, support
search, sample DSL starters, support-ticket correlation, artifact readiness, and
route evidence.

Use `/prototyping/release-gate.json` or `prototyping_release_gate()` before
promoting a rapid prototype. The gate proves generated prototype artifacts,
schema-backed resource catalogs, list/create/detail/dashboard screens, sample
data, portable preview packages, experiment hypotheses, and backlog promotion
items.
- accessibility audit plans for focus order, landmarks, touch targets, and
  WCAG-oriented checks.

Use `/branding/accessibility-workbench.json` or `accessibility_workbench()` in
the generated IDE to inspect WCAG checklist coverage, skip-link baseline,
keyboard navigation, ARIA landmarks, focus/touch checks, audit requirements,
`docs/accessibility.md` coverage, route evidence, and the resulting release
decision.

Use the generated `/branding/visual-quality.json` endpoint as the machine gate
and `/branding/experience-excellence.json` when validating the beautiful and
sophisticated outcome claim. The excellence gate binds palette and contrast,
typography, density, layout recipes, mobile/tablet/desktop/wide viewport
coverage, component state coverage, accessibility, visual-regression review,
and generated branding assets. Use `/branding/ui-release-gate.json` as the
aggregate ship gate when validating that generated applications are polished
across web, mobile, and desktop-sized viewports.
`/branding/visual-regression.json` remains the screenshot checklist for
browser-driven visual QA.
Use the generated `coverage_release_gate()` in
`tests/test_generated_coverage.py` to prove table, workflow, view-experience,
quality, diagnostics, and release-gate coverage before claiming generated test
coverage is complete.
Use `coverage_workbench()` in the same generated pytest module to inspect table
matrix, workflow matrix, area catalog, minimum case count, pytest entrypoints,
artifact, and release-gate evidence.
Use `ci_release_gate()` in `scripts/appgen_quality.py` to prove the generated
GitHub Actions workflow, quality script, required CI stages, quality/test
commands, and generated test artifacts before claiming CI/CD readiness.
Use `/diagnostics/release-gate.json` or `diagnostics_release_gate()` to prove
debugging readiness. The gate checks diagnostic artifacts, schema self-tests,
secret redaction, remediation planning, support bundle shape, API smoke plans,
and load-test plans.
Use `/diagnostics/workbench.json` or `diagnostics_workbench()` in the generated
IDE to inspect self-test, debug snapshot, remediation, support bundle, API
smoke, load-test, artifact, route, and release-gate evidence.
Use `health_release_gate()` in `app/health.py` to prove generated health
metadata before wiring runtime endpoints. The gate checks the health artifact,
status payload, schema metadata, UI counts, and automation counts.
Use `/monitoring/release-gate.json` or `monitoring_release_gate()` to prove
operations monitoring readiness. The gate checks monitoring artifacts,
liveness metadata, readiness checks, JSON error envelopes, and generated
monitoring endpoint contracts.
Use `/monitoring/workbench.json` or `monitoring_workbench()` to inspect
liveness, readiness, error-envelope, endpoint, route, artifact, and release-gate
evidence in the generated IDE.
Use `/performance/release-gate.json` or `performance_release_gate()` to prove
performance readiness. The gate checks generated budget catalogs, bounded
pagination and cache behavior, load-test matrices, executable k6 and Locust
exports, reviewed runbooks, SLO reporting, autoscale recommendations, and
required performance artifacts.
Use `/performance/workbench.json` or `performance_workbench()` to inspect
budget, pagination/cache, load-test, executable-export, runbook, SLO, autoscale,
route, artifact, and release-gate evidence.
Use `/rpa/release-gate.json` or `rpa_release_gate()` to prove generated
automation readiness. The gate checks RPA/BPA task catalogs, process models,
BPMN/UML exports, simulations, vendor export packages, queue payloads,
credential contracts, audit envelopes, business-process observations, and
required automation artifacts.
Use `/realtime/release-gate.json` or `realtime_release_gate()` to prove
interactive event-stream readiness. The gate checks table topic catalogs,
event payload shape, SSE frame rendering, collaboration message payloads,
reconnect replay bounds, and required realtime artifacts.
Use `/realtime/workbench.json` or `realtime_workbench()` in the generated IDE to
inspect topic catalog, event payload, SSE frame, collaboration message, replay,
artifact, route, and release-gate evidence.
Use `/events/release-gate.json` or `event_release_gate()` to prove complex
event processing readiness. The gate checks generated table/workflow topics,
event envelopes, processing actions, failure alerting, retry backoff,
dead-letter payloads, and required event-processing artifacts.
Use `/collaboration/release-gate.json` or `collaboration_release_gate()` to
prove team change-management readiness. The gate checks proposal creation,
review decisions, merge plans, conflict detection, merge queues,
conflict-resolution plans, and required collaboration artifacts.
Use `/collaboration/workbench.json` or `collaboration_workbench()` in the
generated IDE to inspect proposal, review, merge, conflict, queue, resolution,
artifact, route, and release-gate evidence.
Use `/version-control/release-gate.json` or
`version_control_release_gate()` to prove version-history readiness. The gate
checks content-addressed snapshots, schema diffs, branch contracts, rollback
review plans, resource catalogs, and required version-control artifacts.
Use `/version-control/workbench.json` or `version_control_workbench()` in the
generated IDE to inspect resource catalog, snapshot history, diff, branch,
rollback, artifact, route, and release-gate evidence.
Use `/code-review/release-gate.json` or `code_review_release_gate()` to prove
generated quality-review readiness. The gate checks required artifact coverage,
schema-rule coverage, primary-key checks, searchability review, required-field
review, and protected hidden-field review.
Use `/code-review/workbench.json` or `code_review_workbench()` in the generated
IDE to inspect finding catalog, review summary, artifact review, schema-rule,
route, and release-gate evidence.
Use `/devtools/release-gate.json` or `devtools_release_gate()` to prove
external IDE readiness. The gate checks IDE catalogs, VS Code debugging/tasks,
JetBrains run configurations/tasks, Eclipse/PyDev metadata, schema source maps,
and required editor artifacts.
Use `/devtools/workbench.json` or `devtools_workbench()` inside the generated
IDE to inspect tool catalogs, VS Code, JetBrains, Eclipse/PyDev, source-map,
artifact, route, and release-gate evidence.
Use `/extensions/release-gate.json` or `extension_release_gate()` to prove
custom-code extensibility is ready: the gate checks generated artifacts, stable
hook catalogs, table lifecycle hooks, generated-rule dispatch, custom-module
wiring, packaging handoff, and hook category coverage.
Use `packaging_release_gate()` in `appgen_package.py` before distributing a
generated app. The gate checks build metadata, publish metadata, FAB extension
handoff, Cookiecutter context, the generated quality entry point, and required
package artifacts.

Use `/runtime-assurance/excellence-gate.json` as the final generated-app
quality decision. It aggregates the release gate into seven explicit product
outcomes: beautiful, sophisticated, secure, reliable, robust, functional, and
highly capable. The package-level `appgen --generated-app-excellence-audit`
mirrors that by generating a temporary app and running its quality script plus
runtime/UI excellence gates before approving the claim.
Use `/runtime-assurance/workbench.json` or `runtime_assurance_workbench()` in
the generated IDE to inspect the assurance matrix, runtime report, artifact
coverage, application release gate, generated-app excellence gate, and route
surface together before certifying operations readiness.

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
Use `/low-code-features/jhipster-capability-proof.json` for the stricter proof
matrix. It requires every AppGen-only superiority area to carry benchmark,
capability, artifact, depth, and generated route evidence before the
certification gate can pass.
Use `/low-code-features/jhipster-frontier-gate.json` to prove advanced
JHipster capability families are still preserved and then exceeded by generated
AppGen-only capabilities before making stronger product-positioning claims.
Use `/low-code-features/jhipster-feature-superiority-index.json` for the
domain-scored feature index: each modeling, target, IDE/UX, enterprise
operations, AI/ERP/composition, and migration domain must show more generated
AppGen features than the JHipster baseline, with generated routes and artifacts
present.
Generated microservice apps also expose `/microservices/mesh.json` for
service-mesh mTLS, authorization, telemetry, and canary traffic-shift plans.
Use `/microservices/release-gate.json` or `microservice_release_gate()` to prove
service catalogs, gateway routes, event ownership, cross-service relationship
consistency, service-mesh policy, health/scaling plans, and canary rollback.
Use `/low-code-features/composition-release-gate.json` to prove the reusable
application-composition layer itself: block catalog depth, dependency topology,
reviewable install order, sandbox controls, package publication targets, and
artifact evidence.
Use `/low-code-features/composition-workbench.json` when the IDE needs the full
reusable-block installation surface: catalog evidence, dependency audit,
reviewed install plan, non-destructive preview, Entando/Invenio/Cookiecutter
publication handoffs, artifact readiness, and generated route evidence.

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
required ERP template artifacts. Package-level release evidence includes a
finance-core generation smoke that parses exported ERP DSL, writes a generated
app, verifies ERP/native/PWA artifacts, and compiles the generated finance,
ERP-template, reporting, mobile, and desktop modules.

The same module also exposes `/low-code-features/roadmap-sources.json`, which
maps `docs/ideas.md`, `docs/base_features.md`, and `docs/Lo-code features.md`
to generated capabilities and artifacts. Use
`/low-code-features/roadmap-release-audit.json` or `roadmap_release_audit()` as
the stricter release proof: it requires implemented capability status,
generated artifact evidence, critical IDE/workbench routes, generated tests, and
JHipster-superset gates before claiming roadmap coverage.

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
Use `migration_release_gate()` before applying database changes to prove Alembic
artifact coverage, schema inventory, revision plans, SQL previews, rollback
plans, review checklists, and command evidence. Use `migration_workbench()` to
inspect the same evidence in database-design and release-review flows.
Use the generated `seed_release_gate()` before release to prove seed scenarios
are dependency ordered, validation-clean, anonymized for fixture export, backed
by SQL previews, and connected to generated coverage plus quality artifacts.
Use `seed_workbench()` to inspect seed plans, insert order, scenario matrices,
smoke fixtures, anonymized exports, SQL previews, validation, artifact coverage,
and release-gate evidence in the IDE.
Use `reports_release_gate()` to prove generated reports cover table catalogs,
CSV exports, relationship-aware joins, three-way report paths, query plans, and
required report artifacts before relying on generated operational reporting.
Use `/reports/workbench.json` or `reports_workbench()` inside the IDE to inspect
report catalogs, query plans, CSV export previews, relationship report evidence,
artifact readiness, and generated report routes.
Use `report_delivery_release_gate()` to prove generated report delivery has
CSV/PDF formats, download/email channels, printable previews, PDF attachments,
and required report-delivery artifacts before wiring production email.
Use `media_release_gate()` to prove generated image/file uploads have MIME and
extension validation, oversized upload rejection, sanitized storage paths,
preview contracts, and required media cockpit artifacts.
Use `dashboard_release_gate()` to verify chart catalogs, Vega-Lite render
contracts, accessibility summaries, and web/mobile/desktop renderer targets for
generated analytics dashboards.
Use `/dashboards/workbench.json` or `visualization_workbench()` inside the IDE
to inspect aggregate dashboard catalogs, chart render contracts, accessibility
summaries, analytics payloads, renderer targets, artifact readiness, and route
evidence.
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
Use `/integrations/workbench.json` or `integration_workbench()` in the generated
IDE to inspect connector catalog, first-class Entando/Invenio contracts, signed
delivery, commercial channels, portal/repository handoffs, route coverage, and
release readiness together.
Use `node_red_release_gate()` before promoting generated automation. The gate
proves Node-RED is present as the default local automation runtime, validates
the generated flow export, confirms table and workflow webhook endpoints, and
checks the Docker Compose service plan for the generated `node-red` service.
Use `/project-management/release-gate.json` to verify generated backlog,
sprint, release-control, traceability, Jira/GitHub/Azure Boards/GitLab export,
and project-management artifact coverage before handing a generated app to a
delivery team.
Use `/project-management/workbench.json` or `project_management_workbench()` in
the generated IDE to inspect provider, backlog, sprint, release, traceability,
DevOps export, artifact, route, and release-gate evidence.
Use `/data-exchange/release-gate.json` to verify schema-aware CSV templates,
JSON exchange round-trips, import validation, reviewed migration batches,
deterministic request errors, and data-exchange artifacts before loading legacy
or operational data.
Use `/productivity/release-gate.json` to verify Microsoft 365 and Google
Workspace provider coverage, schema-derived document/spreadsheet/calendar/task
payloads, and required productivity artifacts before connecting live office
suite APIs.
Use `/productivity/workbench.json` or `productivity_workbench()` in the generated
IDE to inspect provider catalogs, schema-derived templates, document,
spreadsheet, calendar, and task payloads, route coverage, and release readiness
together.
Use `/api-testing/release-gate.json` before release to verify API request
matrices, response validation, smoke fixtures, UI smoke plans, synthetic
monitors, OpenAPI coverage, and rendered pytest/Playwright modules.
Use `/api-testing/workbench.json` or `api_testing_workbench()` in the generated
IDE to inspect request matrix, response validation, fixtures, UI smoke,
monitoring, contract coverage, rendered module, execution-plan, artifact,
route, and release-gate evidence.
Use `/openapi/release-gate.json` before API publication to verify OpenAPI 3.1
metadata, generated path catalogs, operation IDs/responses, component schemas,
bearer-token security metadata, and required OpenAPI artifacts.
Use `/usage-analytics/release-gate.json` to prove generated app-usage
analytics cover event catalogs, adoption, funnels, retention, real-time
snapshots, and dashboard payloads.
Use `/usage-analytics/workbench.json` in the generated IDE to inspect event
catalogs, activity summaries, adoption, funnels, retention, realtime snapshots,
artifact evidence, route coverage, and the resulting release decision.
Use `/compliance/release-gate.json` to verify privacy request envelopes,
protected-field redaction, erasure review, retention disposition, audit events,
and compliance artifacts before a generated app is released.
Use `/compliance/workbench.json` or `compliance_workbench()` to inspect catalog,
redaction, privacy request, subject export, erasure, retention disposition,
audit, artifact, route, and release-gate evidence.
Use `/identity/release-gate.json` to prove generated SSO readiness across OIDC,
SAML, LDAP, Active Directory, trusted headers, AWS Cognito OAuth, token exchange
review, and principal normalization.
Use `/identity/workbench.json` or `identity_workbench()` to inspect provider
configuration, login plan, directory bind/search plans, Cognito OAuth/token/
logout contracts, group-role mapping, trusted-header plan, principal
normalization, artifact, route, and release-gate evidence.
