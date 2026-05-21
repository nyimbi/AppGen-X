# AppGen DSL

AppGen's DSL is the primary low-code language for describing an application in
one readable file.  It intentionally keeps the core vocabulary small:

For deeper documentation, see the grammar reference (`docs/dsl-grammar.md`),
user guide (`docs/dsl-user-guide.md`), tutorial (`docs/dsl-tutorial.md`), and
linter guide (`docs/dsl-linter.md`).

`app`, `table`, `enum`, `view`, `for`, `flow`, `role`, `rule`, `pk`,
`required`, `unique`, `hidden`, `search`, `default`, `in`, `llm`, and `agent`.

Reusable field groups, arrays, and derived fields do not add keywords:
declare a bare field block, spread it with `...GroupName`, write arrays as
`type[]`, write derived fields with `= expression`, and write references with
the arrow form `field: type -> Other.id`. Relationship cardinality is optional
bracket metadata on the same arrow, for example
`profile_id: int -> Profile.id [one-to-one]`.
Use `#`, `//`, or `/* ... */` comments anywhere whitespace is allowed; comments
are ignored by the parser and do not affect generated artifacts.

The optional `app { ... }` block carries app-level options such as `theme`,
`primary`, `accent`, `logo`, `tagline`, explicit row-level security targets,
and comma-separated `targets` without adding keywords. Supported targets are
`web`, `pwa`, `mobile`, `desktop`, and `chatbot`; unknown targets are reported
as DSL errors instead of being ignored.

## Example

```appgen
app Library { theme: "sage"; targets: web, mobile, desktop; rls: Book.tenant_id }

enum Status { draft published archived }

AuditFields {
  created_at: datetime
  tags: string[]
}

table Author {
  id: int pk
  name: string required search
  email: email unique
}

table Book {
  id: int pk
  ...AuditFields
  title: string required search
  status: Status default draft
  label: string = title + status
  internal_code: string hidden
  author_id: int -> Author.id [many-to-one]
}

view BookList for Book {
  Overview: title, status;
  Publishing: author_id, internal_code;
}

flow Publish {
  draft -> published;
  published -> archived;
}

role Editor {
  Book: read, create, update;
}

rule PublishPolicy for Book {
  title required "Title is required";
  status in draft, published, archived;
  status == published -> review;
}

llm LocalModel {
  provider: ollama
  mode: local
  model: llama3
  endpoint: "http://localhost:11434"
}

llm CloudModel {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}

agent Publisher {
  provider: LocalModel
  goal: "Review and publish books"
  tools: schema, forms, chatbots
  memory: project
  max_steps: 6
}
```

Generate an app from the DSL:

```console
appgen --dsl library.ags --writedir app
```

The same generator also accepts existing schema sources and normalizes them
into the same `AppSchema` model:

```console
appgen --dbml schema.dbml --writedir app
appgen --sql schema.sql --writedir app
appgen --pony entities.py --writedir app
appgen --database-url sqlite:///existing.db --writedir app
```

PonyORM imports are parsed statically rather than executed. `PrimaryKey`,
`Required`, and `Optional` become fields, direct entity references become
foreign keys, reciprocal `Set(...)` declarations become association tables,
class-level composite `PrimaryKey(...)` calls become composite primary keys,
and literal `default=` plus `unique=True` metadata is preserved.
Module-qualified Python types such as `datetime.datetime`, common Pony aliases
such as `LongStr` and `Json`, `Decimal`, and Python `Enum` field types are
normalized into the canonical schema without importing or executing the script.
DBML imports preserve tables, relations, enums, primary keys, direct unique
flags, single-column unique `indexes` entries, composite `Ref` column
pairings, and literal defaults. SQL imports preserve primary keys, foreign keys,
single-column unique constraints, literal defaults, schema-qualified
references, PostgreSQL `CREATE TYPE ... AS ENUM` declarations, post-create
`ALTER TABLE ... ADD CONSTRAINT` primary-key/unique/foreign-key constraints,
composite foreign-key column pairings, and enum-like `CHECK (field IN (...))`
domains.
Live database introspection preserves reflected primary keys, foreign keys,
single-column unique constraints and unique indexes, server defaults, and
SQLAlchemy enum metadata when the dialect exposes it.

## Shape

- `table` defines persistent data models.
- `->` records references without spending a keyword: use
  `author_id: int -> Author.id` inline or `Book.author_id -> Author.id`
  externally. The older `ref` spelling is still accepted for compatibility.
- `hidden` removes a field from generated views, REST include columns, and the
  GraphQL object.
- `search` marks a field for generated Flask-AppBuilder search columns.
- `...GroupName` expands a reusable field group into a table without adding a
  keyword.
- `type[]` declares portable array-like fields, stored by generated apps through
  provider-neutral text/JSON-ready contracts.
- `field: type = expression` declares a derived field. Derived fields stay in
  the manifest and docs but are not generated as database columns or public
  input fields.
- `enum` names a domain vocabulary. Fields typed with an enum generate
  SQLAlchemy `Enum` columns, manifest lookup metadata, select widgets, wizard
  choices, and designer graph choice edges. Reference fields generate
  relationship-picker contracts with target tables, value columns, display
  label fields, and UI-ready lookup choices.
- `view` records the user-facing fields for generated screens. A bare row such
  as `title, status` defines the list order; a labeled row such as
  `Overview: title, status` defines a generated section/tab without adding a
  new keyword.
- `@ field Component x y w h` inside a `view` places a Delphi-style form
  component on the generated design canvas without adding a keyword. For
  example, `@ title TextBox 0 0 6 1` pins the `title` field to a text box.
- `flow` records workflow transitions for generated automation.
- `role` records role-to-resource permissions for generated security policy.
- `app { rls: Table.field }` explicitly chooses tenant-scope fields for
  generated row-level security and PostgreSQL policy SQL. This is useful when
  the tenant field is named for the domain, such as `org_id`, rather than
  `tenant_id`.
- `rule` records table validation and decision branches; `->` names the action
  selected when a condition passes.
- `llm` records local or API-key-backed LLM provider configuration. API keys are
  stored as environment variable names, not secret values. Provider and model
  values may use dotted or dashed names such as `gpt-4.1-mini`.
- `agent` records an agentic system plan with provider, goal, tools, memory,
  and step budget metadata.

Every DSL file is normalized into the canonical `AppSchema` model before code is
generated. During that normalization AppGen validates semantic references:
relations must point at known tables and fields, views/components/rules must use
known fields, role resources must exist, derived fields must use known local
fields, and agents must point at declared `llm` providers when providers are
declared. Duplicate tables, views, workflows, roles, rules, enums, providers,
agents, and fields are reported as errors; the one exception is an intentional
local table field overriding a field imported from a reusable group. Generated
apps include:

- `models.py` and `views.py` for the Flask-AppBuilder application.
- `api.py` with schema-driven REST APIs.
- `gql.py` with a Graphene query schema.
- `security.py` with declared role and permission seed metadata, principal
  normalization, authorization decisions, audit events, policy matrices, and
  reviewable RBAC change proposals that regenerate DSL.
- `runtime_security.py` and `appgen_runtime_security.html` with generated
  inactivity logout and security-header hardening hooks.
- `workflow.py` with transition helpers such as `next_states`,
  `can_transition`, `transition`, `advance_plan`, Mermaid state-chart exports,
  provider-neutral FSM JSON, SCXML export, graph diagnostics, role-aware
  workflow authorization flows derived from declared roles, approval routes,
  SLA/escalation plans, audit events, reviewed transition runbooks, reviewed
  transition proposals that regenerate DSL, and a generated workflow/statechart
  cockpit.
- `rules.py` and `appgen_rules.html` with generated business-rule validation,
  row checks, decision-tree exports, branch action plans, and row-level
  decision traces.
- `validation.py` with schema-driven payload, field, enum, type, required-field,
  relationship, and UI validation contracts for forms, APIs, imports, and
  chatbots.
- `monitoring.py` with liveness/readiness endpoints and generated JSON error
  envelopes.
- `resilience.py` and `appgen_resilience.html` with generated automatic error
  handling, safe user-facing responses, recovery actions, retry plans,
  circuit-breaker state, and operator incident reports.
- `performance.py` and `appgen_performance.html` with generated SLO budgets,
  pagination and cache contracts, deterministic load-test profiles, k6 script
  export, Locust file export, reviewed load-test runbooks, and autoscale
  recommendations.
- `static/appgen.webmanifest`, `static/appgen-sw.js`, and an offline shell for
  progressive web app behavior.
- `branding.py`, `appgen_branding.html`, and `static/appgen-theme.css` with a
  generated brand contract, theme preview, design tokens, component style
  contracts, responsive layout recipes, typography scale, density modes,
  visual quality reports, WCAG-oriented accessibility audit plans, keyboard
  navigation plans, ARIA landmark contracts, focus/touch checks, and CSS custom
  properties.
- `extensions.py`, `appgen_extensions.html`, and `app_custom/extensions.py`
  with stable custom-code hooks that survive regeneration.
- `pyproject.toml`, `MANIFEST.in`, `appgen_package.py`, and `cookiecutter/`
  with publishable package metadata, a quality entry point, FAB extension
  metadata, and a reusable Cookiecutter scaffold for new generated apps.
- `babel.cfg`, `i18n.py`, `appgen_i18n.html`, and
  `translations/en/LC_MESSAGES/messages.po` starter catalogs generated from
  app, table, field, workflow, and role labels, plus locale negotiation,
  fallback translation payloads, and missing-key reports.
- `reports.py` and `appgen_reports.html` with generated report catalogs and CSV
  exports for every table plus relationship-aware join reports and three-way
  table-set reports derived from the schema relation graph.
- `report_delivery.py` and `appgen_report_delivery.html` with generated PDF
  exports and email delivery payloads for reports.
- `dashboards.py` and `appgen_dashboards.html` with generated KPI, bar, line,
  and numeric chart contracts, Vega-Lite visualization specs, renderer-ready
  datasets, accessibility summaries, and web/mobile/desktop dashboard
  workbench payloads for schema-aware data visualization.
- `search.py` and `appgen_search.html` with generated searchable-field indexes
  and provider plans for in-memory, PostgreSQL, Whoosh, and Elasticsearch search,
  including Elasticsearch mappings, Whoosh schema descriptors, and reviewed
  reindex runbooks.
- `media.py` and `appgen_media.html` with generated image and file upload
  validation, preview, and storage contracts for fields typed as image, file,
  upload, blob, or binary.
- `documents.py` and `appgen_documents.html` with generated document libraries,
  version envelopes, approval workflows, retention policies, e-signature
  payloads, and audit events for ERP-style document management.
- `inventory_ops.py` and `appgen_inventory_ops.html` with generated barcode,
  RFID, scan-event, stock-movement, cycle-count, and reconciliation contracts
  for inventory and warehouse traceability.
- `finance_ops.py` and `appgen_finance_ops.html` with generated tax,
  multicurrency conversion, budget forecasting, revenue recognition, and batch
  processing contracts for ERP-grade financial operations.
- `manufacturing_ops.py` and `appgen_manufacturing_ops.html` with generated
  bill-of-material, material-requirements planning, capacity, production
  scheduling, purchase requisition, and lean replenishment contracts.
- `backup.py` with generated JSON backup exports, payload validation,
  SHA-256 integrity manifests, autobackup schedule plans, retention planning,
  recovery runbooks, and restore helpers for reviewed data recovery workflows.
- `data_access.py` and `appgen_data_access.html` with generated low-code
  query/update contracts for table reads, filter validation, sorting, paging,
  field projection, saved queries, portable query exports, create/update
  payload checks, reviewed bulk mutations, mutation audit events, and reviewed
  delete plans.
- `data_exchange.py` and `appgen_data_exchange.html` with schema-aware CSV and
  JSON import/export templates, row validation, reviewed migration batch plans,
  and migration-friendly UI guidance.
- `database_ops.py` and `appgen_database_ops.html` with generated PostgreSQL,
  MySQL, SQLite, MongoDB, DynamoDB, Cassandra, Redis, Patroni, PostGraphile,
  ZomboDB, Elasticsearch, Compose, Kubernetes, NoSQL document projections,
  schema inventory, legacy migration risk assessment, cutover plans, and
  migration-target readiness contracts.
- `schema_import.py` and `appgen_schema_import.html` with generated DBML, SQL
  DDL, PonyORM, and live database source catalogs, source provenance profiles,
  stable source fingerprints, normalization reports, source validation plans,
  import command plans, round-trip export plans, source-to-generated diff plans,
  and reviewed import apply plans before generated files are overwritten. The
  generated `appgen.json` manifest carries the same `source_profile` so an app
  can prove which source family was normalized and which tables, relationships,
  enums, and counts were preserved.
- `integrations.py` and `appgen_integrations.html` with generated REST,
  webhook, Salesforce, SAP, Entando portal, Invenio repository, payment
  gateway, SMS gateway, and transactional email service contracts. Outbound
  calls are represented as reviewed request plans with signed webhook delivery,
  idempotency keys, outbox envelopes, and delivery audit events so generated
  applications do not leak credentials or send data without custom connector
  code.
- `config.py` and `config_admin.py` with secure generated defaults, FAB API
  documentation settings, and a whitelisted setup screen for every generated
  `config.py` assignment. The setup contract includes grouped metadata,
  production-readiness checks, a setup checklist, safe multi-line assignment
  replacement, `/appgen/config/setup.json`, and `.env` export text.
- `integrations.py` and `appgen_integrations.html` with generated REST,
  webhook, Salesforce, SAP, Entando, Invenio, payment gateway, SMS gateway,
  and transactional email connector configuration stubs, reviewed request
  plans, signed webhook delivery, outbox envelopes, and first-class
  Entando/Invenio contract descriptors for routes, payloads, permissions, and
  events.
- `productivity.py` and `appgen_productivity.html` with generated Microsoft
  365 and Google Workspace document, spreadsheet, calendar, and task-sync
  payload contracts.
- `lifecycle.py` and `appgen_lifecycle.html` with generated environment
  readiness, custom-domain plans, release gates, maintenance/update windows,
  feedback items, user-testing sessions, and issue reports.
- `tenancy.py` and `appgen_tenancy.html` with generated tenant-column
  detection, tenant context extraction, and filter helpers for row isolation.
- `rls.py` and `appgen_rls.html` with generated tenant-aware row-level
  security helpers plus PostgreSQL `CREATE POLICY` SQL, tenant session-setting
  SQL, and reviewable database role/user sync SQL for scoped tables.
- `identity.py` and `appgen_identity.html` with generated OIDC, SAML, LDAP,
  Active Directory, AWS Cognito, and trusted-header SSO provider configuration
  checks plus reviewed LDAP bind/search plans and Cognito hosted-ui OAuth,
  token-exchange, logout, and group-role mapping contracts.
- `compliance.py` and `appgen_compliance.html` with generated audit event,
  retention, protected-field redaction, privacy request, subject export,
  erasure planning, and retention-disposition review helpers.
- `assistant.py` and `appgen_assistant.html` with generated prompt context,
  chatbot field questions, deterministic recommendations, prediction feature
  extraction, and human-review task payloads.
- `intelligence.py` and `appgen_intelligence.html` with generated AI analytics,
  preprocessing, anomaly detection, image/video analysis plans, OCR,
  classification, object-detection contracts, NLP, recommendation, A/B testing,
  and predictive-maintenance contracts.
- `chatbot.py` and `appgen_chatbot.html` with in-app guided chatbot flows that
  ask for generated view fields, track missing required answers, and prepare
  create payloads.
- `voice.py` and `appgen_voice.html` with generated speech prompts, utterance
  training phrases, slot-filling plans, SSML responses, and Alexa, Google
  Assistant, and Web Speech export contracts.
- `agents.py` and `appgen_agents.html` with generated agent plans plus local
  and API-key LLM provider readiness checks.
- `designer.py` and `appgen_designer.html` with visual schema graphs, ERD
  exports, reviewable table/field/relationship/workflow proposals, schema-diff
  contracts, migration previews, and regenerated DSL for database design
  workbenches.
- `form_designer.py` and `appgen_form_designer.html` with Delphi-style
  drag-and-drop component palette, snapped form canvas contracts, overlap
  conflict detection, drop proposals, and property-inspector metadata.
- `nl_evolution.py` and `appgen_nl_evolution.html` with natural-language
  proposal planning for tables, fields, forms, workflows, rules, chatbots,
  agents, platform targets, and ERP template modules, including executable
  table DSL for new-table prompts with inferred fields and known-table
  relationship references, approval-ready change sets, migration impact
  summaries, and existing-DSL patch previews.
- `dsl_reference.py` and `appgen_dsl_reference.html` with generated DSL
  keyword-budget checks, compact construct cards, examples, a learning path,
  lightweight lint feedback, structured quick fixes, and fix-result previews so
  every generated app carries an approachable reference for the ANTLR language.
- `view_experience.py`, `appgen_view_experience.html`, and
  `appgen-view-experience.js` with generated base-view contracts for offline
  field state, active viewers on the same page, chatbot/help actions, access log
  events, app version footer context, time-on-page, and current-user display.
- `support_center.py` and `appgen_support_center.html` with generated
  knowledge-base topics, tutorials, onboarding checklists, searchable support
  entries, support-ticket payloads, and sample DSL applications.
- `low_code_features.py` and `appgen_low_code_features.html` with a generated
  capability matrix grounded in `docs/Lo-code features.md`, roadmap alignment,
  readiness reporting for the low-code/no-code platform surface, and an
  explicit broader-than-JHipster benchmark with overlap/AppGen-only rows that
  keeps JDL interoperability while tracking AppGen-only capabilities.
- `prototyping.py` and `appgen_prototyping.html` with rapid mock screens,
  realistic sample data, preview packages, experiment hypotheses, and backlog
  promotion plans for fast stakeholder iteration.
- `text_quality.py` and `appgen_text_quality.html` with generated textarea
  spell, grammar, and character-count feedback contracts.
- `notifications.py` and `appgen_notifications.html` with generated in-app,
  email, webhook, and push-style notification payloads for table events.
- `platforms.py` and `appgen_platforms.html` with generated web, PWA, mobile,
  desktop, and chatbot target contracts plus a web/mobile/desktop generation
  matrix for downstream adapters.
- `frontends/` with generated React, Vue, Angular, Svelte, HTMX, and Express
  starter contracts wired to the generated REST API routes.
- `sdks/` with generated Python, JavaScript, Java, and C# API client
  scaffolds derived from the same REST table contracts.
- `native/` with generated Kivy mobile and BeeWare desktop Python starter
  apps, mobile permission manifests, camera/location capture plans, push
  notification payloads, offline sync batches, conflict-resolution plans,
  offline replay plans, desktop cache snapshots, desktop change-set replay
  plans, desktop local-file actions, offline queue/cache plans, and API route
  contracts.
- `jhipster/app.jdl` and `jhipster/appgen_jhipster.py` with generated
  JHipster JDL exports for Java/TypeScript application generation, preserving
  relation cardinality as JDL `ManyToOne`, `OneToOne`, `OneToMany`, and
  `ManyToMany` blocks. The contract also emits gap analysis and a reviewable
  adoption plan so JHipster remains an interoperability target while AppGen
  provides the broader platform: Python-native web/mobile/desktop starters,
  visual builders, agentic systems, ERP templates, schema round trips, and
  operational workbenches.
- `chatbots/dialogflow/intents.json`,
  `chatbots/botframework/manifest.json`, and `chatbots/appgen_chatbots.py`
  with generated provider intents, field prompts, and conversation checks.
- `automation/node-red/flows.json` and `automation/appgen_node_red.py` with
  generated Node-RED webhook flows for table events, declared workflow
  transitions, webhook endpoint plans, a default Docker Compose Node-RED
  service, runtime readiness checks, and a validation contract.
- `rpa.py` and `appgen_rpa.html` with generated robotic-process automation
  task plans, credential readiness checks, BPMN/UML process models, process
  validation, simulation, UiPath/Blue Prism/Automation Anywhere export
  contracts, audit events, and business-process observations for repetitive
  browser/API work.
- `collaboration.py` and `appgen_collaboration.html` with generated revision
  metadata, change proposals, review decisions, merge plans, conflict reports,
  merge queues, and conflict-resolution plans for concurrent low-code work.
- `version_control.py` and `appgen_version_control.html` with generated
  manifest snapshots, content-addressed revision IDs, branch plans,
  schema-level diffs, and reviewable rollback plans.
- `.vscode/`, `.idea/`, `.project`, `.pydevproject`, `devtools.py`, and
  `appgen_devtools.html` with generated Visual Studio Code, JetBrains
  IDEA/PyCharm, and Eclipse/PyDev launch, task, extension, source-map, and
  readiness contracts.
- `studio.py` and `appgen_studio.html` with a generated IDE/workbench for DSL
  authoring, DSL linting, outline extraction, keyword-budget checks,
  quick fixes, completions/snippets, searchable command palettes, project trees, editor
  sessions, visual database design, Mermaid ERD export, DBML export, SQL DDL
  preview, read-only SQL workbench/explain-plan guards, PonyORM preview, table
  proposals, migration previews, staged
  generation jobs with deterministic IDs, queue/status/log views, target
  artifact manifests, IDE diagnostics, app management, code editing,
  breakpoint/debug plans, dependency update plans, app cloning, and reusable
  component repository exports.
- `realtime.py` and `appgen_realtime.html` with generated event topics,
  Server-Sent Events frames, collaboration messages, and reconnect replay plans.
- `diagnostics.py` and `appgen_diagnostics.html` with generated schema
  invariants, row validation, redacted debug snapshots, remediation plans,
  support bundles, API smoke plans, and load-test plans.
- `tests/test_generated_coverage.py` with a generated per-table pytest coverage
  matrix for schema, API, UI, reports, security, and data exchange/backup
  flows.
- `code_review.py` and `appgen_code_review.html` with generated automated
  schema and artifact review findings for quality gates.
- `components.py` and `appgen_components.html` with generated reusable form,
  list, detail, and card component contracts plus field widget descriptors for
  visual builders. Date, datetime, and time fields produce calendar-aware
  widget contracts with web, mobile, and desktop renderer hints. Custom widgets
  produce reviewable registration plans, renderer mappings, palette entries,
  preview payloads, and accessibility contracts before they are installed.
- `view_composition.py` and `appgen_view_composition.html` with generated
  MasterDetailView, MultipleView, and ChartView contracts derived from schema
  relationships and visible fields.
- `tabbed_views.py` and `appgen_tabbed_views.html` with generated tabbed view
  contracts and role-aware permissions per tab. View sections become tabs, and
  declared role permissions on the view table decide which roles can see them.
- `erp_templates.py` and `appgen_erp_templates.html` with reusable ERP module
  templates for ledgers, accounts, invoicing, AP, AR, inventory, HR, payroll,
  purchasing, procurement, supply chain, warehouse management, manufacturing,
  sales, CRM, e-commerce, assets, maintenance, quality management, document
  management, compliance, projects, and reports. Each module includes table-level
  field blueprints, references, workflows, reports, and AppGen DSL export helpers
  plus recommended finance, distribution, people, manufacturing, and full-ERP
  starter stacks, composite ERP DSL, generation plans, and legacy ERP migration
  plans so users can start from realistic ERP components rather than empty
  placeholder tables.
- `project_management.py` and `appgen_project_management.html` with generated
  agile backlog, sprint, release, traceability, and Jira/GitHub/Azure
  Boards/GitLab issue-export contracts.
- `wizards.py` and `appgen_wizards.html` with generated sequential table
  creation wizards and workflow process wizards derived from existing tables
  and `flow` declarations.
- `events.py` and `appgen_events.html` with generated complex event
  processing, alerting, retry, and dead-letter contracts.
- `api_testing.py` and `appgen_api_testing.html` with generated automated API
  testing, pytest module rendering, UI smoke-test plans, Playwright-style
  smoke module rendering, execution plans, contract coverage, result
  evaluation, and synthetic monitoring contracts.
- `openapi.py`, `appgen_openapi.html`, and `docs/openapi.json` with generated
  OpenAPI 3.1 API documentation.
- `microservices.py` and `appgen_microservices.html` with generated service
  boundaries, gateway routes, event routes, cross-service relationship
  resolvers, consistency reviews, health probes, and scaling plans.
- `usage_analytics.py` and `appgen_usage_analytics.html` with generated
  adoption, funnel, retention, and real-time app-usage analytics.
- `seed.py` with relationship-aware deterministic demo data, dependency-ordered
  seed plans, validation, anonymized fixture exports, and SQL previews;
  `docs/schema.md` with table,
  field, relationship, and Mermaid ERD documentation, and
  `docs/data-dictionary.json` / `docs/data-dictionary.md` with
  machine-readable structure, content-kind, sample-value, display-field, and
  writable-field metadata.
- `docs/accessibility.md` with a generated accessibility baseline checklist.
- `.github/workflows/appgen-ci.yml` and `scripts/appgen_quality.py` with a
  generated CI quality gate for syntax, manifest, PWA, docs, and test-surface
  checks.
- `deploy/` with Docker/Compose-adjacent Kubernetes manifests, Terraform
  starter contracts for AWS, GCP, and Azure, generated deployment runbooks,
  secret-injection plans, smoke checks, rollback plans, and cloud readiness
  helpers.
- `deploy/Caddyfile` and `deploy/appgen_https.py` with generated automatic
  HTTPS reverse proxy configuration and TLS readiness checks.
- `appgen.json`, a manifest containing tables, relations, views, workflows,
  roles, and low-code platform capability targets.
- The generated designer exposes graph nodes/edges plus table, field, and
  workflow-step proposal helpers so visual model edits can regenerate DSL. It
  also exports Mermaid ERD text and a relationship matrix for database design
  tools.
