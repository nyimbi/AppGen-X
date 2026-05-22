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
The legacy `ref Other.id` form is still parsed for existing sources, but it is
not part of the canonical keyword budget; the linter reports it and offers
`replace_ref_with_arrow`.
Beginner-friendly aliases are also keyword-free: `entity` and `model`
normalize to `table`, `form` and `screen` normalize to `view`, and `workflow`
normalizes to `flow` before ANTLR parsing. The linter reports these aliases
and offers `normalize_authoring_aliases` so committed source stays canonical.
Field modifier aliases follow the same rule: `searchable` normalizes to
`search`, and `hide` normalizes to `hidden`, with a
`normalize_modifier_aliases` quick fix.
Use `#`, `//`, or `/* ... */` comments anywhere whitespace is allowed; comments
are ignored by the parser and do not affect generated artifacts.
The DSL authoring release gate proves the language remains learnable and
operational: it checks the ANTLR parser, keyword budget, syntax/semantic
linting, formatter stability, IDE navigation, code actions, authoring guidance,
language ergonomics, and source-family coverage for DBML, SQL, PonyORM, live
database introspection, and DSL files. `dsl_language_ergonomics_contract()`
proves friendly aliases, keyword-free expressiveness, quick fixes,
deterministic formatting, the progressive learning path, and multi-source
guidance before the authoring gate can pass. `dsl_language_experience_gate()`
adds the user-facing language promise: generated evidence must prove the DSL is
delightful, intuitive, functional, ANTLR-backed, keyword-limited, and ready for
all supported schema source families.
`dsl_antlr_integrity_report()` additionally proves the canonical grammar and
generated lexer/parser metadata are synchronized, including token names, parser
rules, required DSL constructs, and compact keyword literals.

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
appgen --database-url postgresql+psycopg2://user@host/db --writedir app
```

PonyORM imports are parsed statically rather than executed. `PrimaryKey`,
`Required`, and `Optional` become fields, direct entity references become
foreign keys, reciprocal `Set(...)` declarations become association tables,
class-level composite `PrimaryKey(...)` calls become composite primary keys,
declared non-`id` primary keys remain relation targets, single-column
`composite_key(...)` calls become unique fields, `index=True` and
`composite_index(...)` become searchable hints, and literal `default=` plus
`unique=True` metadata is preserved.
Module-qualified Python types such as `datetime.datetime`, common Pony aliases
such as `LongStr` and `Json`, `Decimal`, and Python `Enum` field types are
normalized into the canonical schema without importing or executing the script.
DBML imports preserve tables, relations, enums, primary keys, direct unique
flags, single-column unique `indexes` entries, composite `Ref` column
pairings, `Ref` direction, one-to-one `-` cardinality, `TableGroup`
membership as source grouping metadata, and literal defaults.
SQL imports preserve primary keys, foreign keys,
single-column unique constraints, literal defaults, schema-qualified
references, PostgreSQL `CREATE TYPE ... AS ENUM` declarations, post-create
`ALTER TABLE ... ADD CONSTRAINT` primary-key/unique/foreign-key constraints,
composite foreign-key column pairings, implicit primary-key references such as
`REFERENCES publisher`, SQL comments, identity columns, generated columns as
derived fields, and enum-like `CHECK (field IN (...))` domains.
Live database introspection accepts SQLAlchemy database URLs with or without
driver suffixes, such as `sqlite:///existing.db`,
`postgresql+psycopg2://...`, and `mysql+pymysql://...`. It preserves reflected
primary keys, foreign keys, single-column unique constraints and unique indexes,
ordinary indexes as searchable hints, computed columns as derived fields,
server defaults, and SQLAlchemy enum metadata when the dialect exposes it.
Reflected primary keys are normalized as non-null even when a dialect reports
nullable metadata for legacy schemas.

Every imported source also produces a source-fidelity report in the generated
`appgen.json` manifest and `schema_import.py`. The report records the import
command, canonical fingerprint, supported source contract, round-trip targets,
normalization checks, SQLAlchemy database URL dialect support, and known lossy
areas that need review, such as SQL triggers/views, DBML notes, PonyORM custom
methods, or database grants.
Use `schema_source_example_audit()` during release review to parse concrete DBML,
SQL, PonyORM, live SQLite database, and DSL examples through the real adapters.
The audit proves each source family produces an `AppSchema` with tables,
relations, fingerprints, fidelity reports, and generator commands.
The same proof is available from the CLI:

```console
appgen --schema-source-audit
```

Promote that adapter proof into the package-level objective audit before
claiming AppGen can generate from DBML, SQL, PonyORM, existing databases, and
DSL sources. This audit parses every source family, generates a temporary app
from each one, checks the generated source-fidelity manifest, and compiles core
generated Python artifacts:

```console
appgen --source-intake-release-audit
```

Check that the ANTLR grammar and generated parser artifacts are synchronized:

```console
appgen --dsl-antlr-report
```

Run the full authoring release gate for a DSL file with
`dsl_authoring_release_gate()` or the CLI:

```console
appgen --dsl-authoring-gate library.ags
```

Run the package-level DSL release audit before claiming the language has a
ready linter, synchronized grammar, complete guide/tutorial/linter docs, and
generated reference artifacts:

```console
appgen --dsl-release-audit
```

Run the package-level roadmap audit before claiming AppGen satisfies the full
low-code objective from `docs/ideas.md`, `docs/base_features.md`, and
`docs/Lo-code features.md`:

```console
appgen --roadmap-release-audit
```

Run the package-level JHipster superiority audit before claiming AppGen is more
capable than JHipster:

```console
appgen --jhipster-superiority-audit
```

Run the generated-app excellence audit before claiming generated apps are
beautiful, sophisticated, secure, reliable, robust, functional, and highly
capable:

```console
appgen --generated-app-excellence-audit
```

Run the ideas-roadmap audit before claiming the original `docs/ideas.md`
roadmap items are covered by implemented package capability evidence:

```console
appgen --ideas-release-audit
```

Run the base-feature audit before claiming every numbered item and platform
bullet in `docs/base_features.md` has implemented package capability evidence:

```console
appgen --base-features-release-audit
```

Run the aggregate package goal audit when you need one machine-readable bundle
covering roadmap traceability, JHipster superiority, and generated-app
excellence, ideas-roadmap coverage, base-feature coverage,
DSL linter/grammar/docs, schema source intake, ERP templates, and package-level
natural-language evolution:

```console
appgen --package-goal-audit
```

Discover package-level ERP starter modules and export one as AppGen DSL:

```console
appgen --erp-template-catalog
appgen --erp-template invoicing > invoicing.appgen
appgen --dsl invoicing.appgen --writedir apps/invoicing
```

Convert a natural-language app change into an audited plan or a reviewable DSL
patch before generation:

```console
appgen --nl-plan "create table Ticket with fields title required and form TicketForm agent SupportAgent targets web mobile desktop"
appgen --nl-dsl "create table Ticket with fields title required and form TicketForm agent SupportAgent targets web mobile desktop" > ticket_patch.appgen
appgen --nl-release-audit
```

The package-level NL surface emits tables, fields, Delphi-style forms, flows,
rules, report/dashboard comments, chatbot handoff comments, local/API-key LLM
providers, agents, ERP module commands, platform targets, migration impact, and
rollback guidance. Destructive prompts such as `drop table` or `remove field`
return `requires_approval: true` instead of applying the change.

Audit the package-level Studio/IDE contract before claiming AppGen can manage
application design before generation:

```console
appgen --studio-release-audit
```

The Studio audit covers DSL editor diagnostics, completions and code actions,
database-design workspaces, source intake for DBML/SQL/PonyORM/live DB/DSL,
reviewable generation jobs, and application snapshot/restore/version-management
commands.

Audit the package-level Delphi-style form designer contract before claiming
users can drop components onto generated forms:

```console
appgen --form-designer-release-audit
```

The form-designer audit proves draggable component palette breadth, a stable
snap-to-grid canvas, field-to-component mappings, snapped drop proposals,
property-inspector metadata, placement suggestions, overlap guardrails, and the
generated form-designer artifact contract.

Audit the package-level visual modeling and database-design contract before
claiming visual models can generate code and database schema:

```console
appgen --visual-modeling-release-audit
```

The visual-modeling audit proves graph nodes and edges, Mermaid ERD export,
DBML/SQL/PonyORM/DSL export, reviewable table/field/relationship proposals,
migration previews, and generated code/database artifact plans.

Audit the package-level security and identity contract before claiming
generated apps are secure:

```console
appgen --security-release-audit
```

The security audit proves DSL role policies, authorization decisions and audit
events, OIDC/SAML/LDAP/Active Directory/AWS Cognito SSO provider contracts,
environment-only secret policy, tenant/RLS PostgreSQL policy SQL, session
timeout and security headers, compliance/privacy controls, secret scanning, and
required generated security artifacts.

Audit the package-level configuration editor contract before claiming the
roadmap `config.py` setup screen is ready:

```console
appgen --config-release-audit
```

The config audit proves roadmap-required `FAB_API_SHOW_STACKTRACE` and
`FAB_API_SWAGGER_UI` defaults, whitelisted editable keys, production safety
warnings, environment export, and generated `config.py`/`config_admin.py`/
template artifact expectations.

Audit the package-level distribution contract before claiming AppGen is a
publishable generator with reusable templates:

```console
appgen --distribution-release-audit
```

The distribution audit covers publishable package metadata, Cookiecutter
template artifacts, Flask-AppBuilder extension hooks, generated coverage tests,
and idempotent seed-script expectations.

Audit package-level reporting and ChartView coverage before claiming the
roadmap reporting lane is complete:

```console
appgen --reporting-release-audit
```

The reporting audit proves every table receives a report, relations receive
join reports, two-hop relation paths receive 3-way reports, every table receives
a ChartView contract, and report delivery covers PDF export plus email
attachments.

Audit package-level operations readiness before claiming Docker, Kubernetes,
cloud, search, HTTPS, and automation outputs are ready:

```console
appgen --ops-release-audit
```

The ops audit proves Docker Compose, Kubernetes, autoscaling, Terraform for AWS,
GCP, and Azure, automatic HTTPS, Elasticsearch and Whoosh search plans, default
Node-RED flows, and database operations contracts for Patroni, ZomboDB, and
PostGraphile.

Audit package-level enterprise integration readiness before claiming generated
apps can connect to external APIs, webhooks, portals, repositories, payments,
SMS, and email:

```console
appgen --integration-release-audit
```

The integration audit proves REST and signed-webhook contracts, Salesforce and
SAP stubs, Stripe and M-Pesa payment plans, Twilio SMS, SendGrid email, stable
idempotency keys, and first-class generated contracts for Entando
micro-frontends and Invenio repository deposits.

Audit package-level agentic readiness before claiming the DSL can design
agentic systems across local and API-key LLM providers:

```console
appgen --agentic-release-audit
```

The agentic audit parses DSL `llm` and `agent` blocks, proves Ollama and
LM Studio local provider contracts, OpenAI and Anthropic API-key contracts,
environment-only secret policy, missing-key guardrails, reviewed agent tool
policies, execution matrices, and generated agent artifact expectations.

Audit package-level target readiness before claiming AppGen can generate web,
PWA, mobile, desktop, and chatbot applications:

```console
appgen --target-release-audit
```

The target audit parses DSL target selection and proves Flask-AppBuilder web,
installable PWA, Kivy mobile, BeeWare desktop, and chatbot provider contracts,
including package artifacts, mobile permissions/offline queues, and desktop
local-cache/sync replay expectations.

## Shape

- `table` defines persistent data models.
- `->` records references without spending a keyword: use
  `author_id: int -> Author.id` inline or `Book.author_id -> Author.id`
  externally. The older `ref` spelling is still accepted for compatibility.
- `entity`, `model`, `form`, `screen`, and `workflow` are authoring aliases,
  not grammar keywords. They normalize before parsing and can be rewritten by
  the linter.
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
  reviewable RBAC change proposals that regenerate DSL, plus generated threat
  models, secret exposure scans, dependency security plans, API security test
  plans, release security gates, signoff envelopes, and `security_workbench()`
  evidence for policy, authorization, audit, RBAC proposal, threat, secret,
  dependency, API-security, release-gate, and signoff readiness before
  `security.rbac` is marked implemented.
- `runtime_security.py` and `appgen_runtime_security.html` with generated
  inactivity logout and security-header hardening hooks. The generated
  `runtime_security_release_gate()` and `runtime_security_workbench()` prove
  artifact coverage, timeout policy, public-path bypass, expired/active session
  handling, activity markers, security headers, and
  `/runtime-security/workbench.json` route evidence before `security.session`
  is marked implemented.
- `workflow.py` with transition helpers such as `next_states`,
  `can_transition`, `transition`, `advance_plan`, Mermaid state-chart exports,
  provider-neutral FSM JSON, SCXML export, graph diagnostics, role-aware
  workflow authorization flows derived from declared roles, approval routes,
  SLA/escalation plans, audit events, reviewed transition runbooks, reviewed
  transition proposals that regenerate DSL, and a generated workflow/statechart
  cockpit. The generated `workflow_release_gate()` proves workflow artifacts,
  FSM/Mermaid/SCXML exports, graph diagnostics, authorization flows, approval
  routes, SLA metadata, and reviewed runbooks before workflow readiness is
  claimed. `workflow_workbench()` adds aggregate IDE-ready evidence for workflow
  catalogs, statechart exports, graph diagnostics, authorization flows, approval
  routes, SLA runbooks, release decisions, and `/workflows/workbench.json` route
  coverage.
- `rules.py` and `appgen_rules.html` with generated business-rule validation,
  row checks, decision-tree exports, branch action plans, and row-level
  decision traces. The generated `rules_release_gate()` proves required
  artifacts, rule catalogs, validation success/error contracts, decision plans,
  decision-tree exports, and decision traces before customization readiness is
  claimed. `rules_workbench()` adds IDE-ready evidence for artifact coverage,
  rule catalogs, validation contracts, decision plans, decision trees, decision
  traces, release decisions, and `/rules/workbench.json` route coverage.
- `validation.py` with schema-driven payload, field, enum, type, required-field,
  relationship, and UI validation contracts for forms, APIs, imports, and
  chatbots. The generated `validation_release_gate()` proves table validation
  contracts, valid payloads, required-field errors, partial updates, UI
  schemas, enum errors, type errors, and required validation artifacts.
- `health.py` with generated schema and automation health metadata. The
  generated `health_release_gate()` proves the health artifact, status payload,
  schema metadata, UI counts, and automation counts.
- `monitoring.py` with liveness/readiness endpoints and generated JSON error
  envelopes. The generated `monitoring_release_gate()` proves monitoring
  artifacts, liveness metadata, readiness checks, JSON error envelopes, and
  endpoint contracts. `monitoring_workbench()` exposes IDE-ready liveness,
  readiness, error-envelope, endpoint, route, artifact, and release-gate
  evidence before `ops.monitoring` is marked implemented.
- `resilience.py` and `appgen_resilience.html` with generated automatic error
  handling, safe user-facing responses, recovery actions, retry plans,
  circuit-breaker state, and operator incident reports. The generated
  `resilience_release_gate()` proves required artifacts, exception taxonomy,
  safe user responses, retry and circuit-breaker behavior, incident reporting,
  and the exception-management plan. `resilience_workbench()` exposes IDE-ready
  taxonomy, safe-response, retry, circuit-breaker, incident, route, artifact,
  and release-gate evidence before `ops.resilience` is marked implemented.
- `performance.py` and `appgen_performance.html` with generated SLO budgets,
  pagination and cache contracts, deterministic load-test profiles, k6 script
  export, Locust file export, reviewed load-test runbooks, and autoscale
  recommendations. The generated `performance_release_gate()` proves required
  artifacts, budget catalogs, bounded pagination and cache behavior, load-test
  matrices, executable k6/Locust exports, reviewed runbooks, SLO reporting, and
  autoscale recommendations. `performance_workbench()` exposes IDE-ready budget,
  pagination/cache, load-test, executable-export, runbook, SLO, autoscale, route,
  artifact, and release-gate evidence before `ops.performance` is marked
  implemented.
- `runtime_assurance.py` and `appgen_runtime_assurance.html` with a generated
  readiness matrix that ties security hardening, health checks, resilience,
  SLOs, backup integrity, recovery runbooks, visual/accessibility quality, and
  the generated quality gate into one auditable operations contract. It also
  emits `application_release_gate()`, an aggregate release decision over
  security signoff, operations readiness, polished generated UI, tests, docs,
  manifests, and required artifacts. `generated_app_excellence_gate()` is the
  stricter product-level gate: it blocks release claims unless the generated
  app proves the seven roadmap outcomes of beautiful, sophisticated, secure,
  reliable, robust, functional, and highly capable. `runtime_assurance_workbench()`
  and `/runtime-assurance/workbench.json` aggregate the matrix, assurance report,
  artifact coverage, application release gate, generated-app excellence gate,
  and route surface into one IDE-ready assurance review.
- `pwa.py`, `appgen_pwa.html`, `static/appgen.webmanifest`,
  `static/appgen-sw.js`, `static/appgen-offline.html`, icons, and theme assets
  for installable progressive web app behavior. The generated
  `pwa_release_gate()` proves PWA target selection, artifact coverage,
  standalone manifest readiness, service-worker precache/offline fallback,
  safe fetch scope, and offline shell registration.
- `branding.py`, `appgen_branding.html`, and `static/appgen-theme.css` with a
  generated brand contract, theme preview, design tokens, component style
  contracts, responsive layout recipes, typography scale, density modes,
  viewport contracts, component state matrices, visual regression plans, visual
  quality reports for contrast, palette balance, no-overlap review, and
  viewport coverage, deterministic visual test matrices, WCAG-oriented
  accessibility audit plans, keyboard navigation plans, ARIA landmark
  contracts, focus/touch checks, CSS custom properties, an experience-excellence
  gate, and a UI experience release gate that aggregates theme quality,
  beautiful/sophisticated outcome evidence, accessibility, visual regression,
  responsive coverage, component states, and required assets. The generated
  `branding_workbench()` proves theme contract, CSS variables, design-system
  coverage, palette quality, visual quality, responsive evidence, release-gate
  readiness, and route coverage before `ui.branding` is marked implemented.
  `accessibility_workbench()` proves WCAG checklist coverage, skip-link
  baseline, keyboard navigation, ARIA landmarks, focus/touch checks, audit
  requirements, `docs/accessibility.md` coverage, and
  `/branding/accessibility-workbench.json` route evidence before
  `a11y.compliance` is marked implemented.
  The generated
  `responsive_workbench()` proves breakpoint tokens, mobile/tablet/desktop/wide
  viewport contracts, responsive layout recipes, touch density, visual matrices,
  and route evidence before `ui.responsive` is marked implemented.
- `extensions.py`, `appgen_extensions.html`, and `app_custom/extensions.py`
  with stable custom-code hooks that survive regeneration. A generated
  `extension_workbench()` proves artifact presence, hook registry coverage,
  table lifecycle hooks, generated-rule dispatch, custom-module wiring,
  packaging handoff, hook categories, release gates, and route coverage before
  `platform.extensibility` is marked implemented.
- `pyproject.toml`, `MANIFEST.in`, `appgen_package.py`, and `cookiecutter/`
  with publishable package metadata, a quality entry point, FAB extension
  metadata, and a reusable Cookiecutter scaffold for new generated apps. A
  generated `packaging_workbench()` proves package artifacts, build metadata,
  publish metadata, FAB extension handoff, Cookiecutter context, quality entry
  point, and release gates before `devops.packaging` is marked implemented.
- `babel.cfg`, `i18n.py`, `appgen_i18n.html`, and
  `translations/en/LC_MESSAGES/messages.po` starter catalogs generated from
  app, table, field, workflow, and role labels, plus locale negotiation,
  fallback translation payloads, and missing-key reports. The generated
  `i18n_release_gate()` proves localization artifacts, locale metadata, default
  catalog coverage, fallback translation behavior, locale negotiation,
  missing-key report visibility, and runtime payload shape. The generated
  `i18n_workbench()` exposes IDE-ready locale catalog, fallback translation,
  negotiation, missing-key, artifact, and route-surface evidence.
- `reports.py` and `appgen_reports.html` with generated report catalogs and CSV
  exports for every table plus relationship-aware join reports and three-way
  table-set reports derived from the schema relation graph. A generated reports
  release gate proves table catalogs, CSV exports, join and three-way reports,
  relationship CSV output, query plans, and required report artifacts. The
  generated `reports_workbench()` exposes IDE-ready report catalogs, query
  plans, CSV export previews, relationship CSV evidence, artifact readiness,
  and route-surface evidence.
- `report_delivery.py` and `appgen_report_delivery.html` with generated PDF
  exports and email delivery payloads for reports, plus a release gate proving
  delivery catalog coverage, CSV/PDF format coverage, download/email channel
  coverage, HTML/PDF rendering previews, email attachment payloads, and required
  artifacts.
- `dashboards.py` and `appgen_dashboards.html` with generated KPI, bar, line,
  and numeric chart contracts, Vega-Lite visualization specs, renderer-ready
  datasets, accessibility summaries, and web/mobile/desktop dashboard
  workbench payloads for schema-aware data visualization. A generated dashboard
  release gate proves dashboard/catalog coverage, Vega-Lite rendering contracts,
  accessibility summaries, web/mobile/desktop renderer targets, and required
  dashboard artifacts. The generated `visualization_workbench()` provides
  aggregate IDE evidence for dashboard catalogs, chart render contracts,
  accessibility text, analytics payloads, renderer targets, artifacts, and
  dashboard route coverage.
- `search.py` and `appgen_search.html` with generated searchable-field indexes
  and provider plans for in-memory, PostgreSQL, Whoosh, and Elasticsearch search,
  including Elasticsearch mappings, Whoosh schema descriptors, and reviewed
  reindex runbooks. A generated search release gate proves index coverage,
  provider coverage/readiness, reindex planning, and search artifact coverage;
  `search_workbench()` adds IDE-ready evidence for index catalogs, provider
  coverage, required-provider readiness, provider index plans, reindex plans,
  artifact coverage, release decisions, and `/search/workbench.json` route
  coverage.
- `media.py` and `appgen_media.html` with generated image and file upload
  validation, preview, and storage contracts for fields typed as image, file,
  upload, blob, or binary. A generated media release gate proves MIME/extension
  validation, unsafe-upload rejection, sanitized storage paths, preview
  contracts, and required media artifacts. The generated
  `media_upload_workbench()` proves upload catalogs, validation matrices,
  storage safety, preview contracts, release gates, and route evidence before
  `components.media` is marked implemented.
- `documents.py` and `appgen_documents.html` with generated document libraries,
  version envelopes, approval workflows, retention policies, e-signature
  payloads, and audit events for ERP-style document management. A generated
  `document_management_workbench()` proves document catalogs, version envelopes,
  approval workflows, retention/legal-hold policy, e-signature payloads, audit
  events, status models, release gates, and route coverage before
  `content.document-management` is marked implemented.
- `inventory_ops.py` and `appgen_inventory_ops.html` with generated barcode,
  RFID, scan-event, stock-movement, cycle-count, and reconciliation contracts
  for inventory and warehouse traceability. A generated `inventory_workbench()`
  proves scan targets, barcode/RFID payloads, movement/count/reconciliation
  contracts, traceability chains, mobile/offline capabilities, release gates,
  and route coverage before `operations.inventory-traceability` is marked
  implemented.
- `finance_ops.py` and `appgen_finance_ops.html` with generated tax,
  multicurrency conversion, budget forecasting, revenue recognition, and batch
  processing contracts for ERP-grade financial operations. A generated
  `finance_workbench()` proves finance-resource coverage, tax profiles,
  currency conversion, budget forecasting, revenue recognition, batch
  processing, release gates, and route coverage before `operations.finance` is
  marked implemented.
- `manufacturing_ops.py` and `appgen_manufacturing_ops.html` with generated
  bill-of-material, material-requirements planning, capacity, production
  scheduling, purchase requisition, and lean replenishment contracts. A
  generated `manufacturing_workbench()` proves the BOM, MRP, capacity,
  scheduling, requisition, kanban, release gates, and route coverage before
  `operations.manufacturing` is marked implemented.
- `backup.py` with generated JSON backup exports, payload validation,
  SHA-256 integrity manifests, autobackup schedule plans, retention planning,
  recovery runbooks, disaster-recovery plans, backup release gates, and restore
  helpers for reviewed data recovery workflows. `backup_workbench()` and
  `/backups/workbench.json` aggregate payload validation, manifest integrity,
  autobackup scheduling, retention policy, recovery runbooks, disaster recovery,
  route surface, and release-gate evidence before `ops.backup` is marked
  implemented.
- `data_access.py` and `appgen_data_access.html` with generated low-code
  query/update contracts for table reads, filter validation, sorting, paging,
  field projection, saved queries, portable query exports, create/update
  payload checks, reviewed bulk mutations, mutation audit events, and reviewed
  delete plans. A generated `data_access_workbench_index()` proves required
  artifacts, resource catalogs, limit-capped projections, saved-query exports,
  create/update/delete mutation plans, mutation audit events, workbench
  metadata, release gates, and route coverage before `data.access` is marked
  implemented.
- `data_exchange.py` and `appgen_data_exchange.html` with schema-aware CSV and
  JSON import/export templates, row validation, reviewed migration batch plans,
  migration-friendly UI guidance, and a generated data-exchange release gate
  that proves catalog, CSV templates, JSON round-trips, import validation,
  migration batches, request error contracts, and required artifacts. A generated
  `data_exchange_workbench()` adds IDE-ready evidence for artifact coverage,
  catalog, templates, JSON round-trips, validation, migration batches, request
  contracts, release decisions, and `/data-exchange/workbench.json` route
  coverage.
- `database_ops.py` and `appgen_database_ops.html` with generated PostgreSQL,
  MySQL, SQLite, MongoDB, DynamoDB, Cassandra, Redis, Patroni, PostGraphile,
  ZomboDB, Elasticsearch, Compose, Kubernetes, NoSQL document projections,
  schema inventory, legacy migration risk assessment, cutover plans, and
  migration-target readiness contracts. Patroni HA cluster plans,
  PostGraphile schema exposure plans, ZomboDB index plans, and a generated
  database add-on release gate make these capabilities reviewable before
  production rollout. `database_ops_workbench()` adds IDE-ready evidence for
  provider catalogs, add-on catalogs, Compose services, Kubernetes stateful
  workloads, schema inventory, migration targets, cutover plans, NoSQL
  projections, release gates, and `/database-ops/workbench.json` route coverage.
- `migrations/appgen_migrations.py` with generated schema inventory, Alembic
  revision plans, SQL previews, rollback plans, migration review checklists, and
  a migration workbench. `migration_release_gate()` proves artifact coverage,
  inventory, revision planning, SQL preview, rollback, review checklist, and
  Alembic command evidence before `data.migrations` is marked implemented.
- `schema_import.py` and `appgen_schema_import.html` with generated DBML, SQL
  DDL, PonyORM, live database, and DSL source catalogs, source provenance profiles,
  stable source fingerprints, source-fidelity reports, normalization reports,
  source validation plans, import command plans, round-trip export plans,
  source-to-generated diff plans, reviewed import apply plans, and source
  generation proof matrices before
  generated files are overwritten. A schema-import release gate combines
  artifact readiness, source-family coverage, validation, round-trip targets,
  source fidelity, database URL dialect evidence, and generation proof before generation coverage
  is claimed. The generated `appgen.json` manifest carries
  the same `source_profile` and `source_fidelity` evidence so an app can prove
  which source family was normalized, which tables, relationships, enums, and
  counts were preserved, and which source-specific features require review.
- `integrations.py` and `appgen_integrations.html` with generated REST,
  webhook, Salesforce, SAP, Entando portal, Invenio repository, payment
  gateway, SMS gateway, and transactional email service contracts. Outbound
  calls are represented as reviewed request plans with signed webhook delivery,
  idempotency keys, outbox envelopes, and delivery audit events so generated
  applications do not leak credentials or send data without custom connector
  code. A generated integration release gate proves connector coverage,
  first-class Entando/Invenio contracts, signed delivery, commercial channels,
  portal/repository plans, and required integration artifacts.
  `integration_workbench()` and `/integrations/workbench.json` aggregate the
  connector catalog, first-class Entando/Invenio contracts, signed webhook
  delivery, payment/SMS/email plans, portal/repository handoffs, route surface,
  and release-gate evidence before `integration.enterprise` is marked
  implemented.
- `config.py` and `config_admin.py` with secure generated defaults, FAB API
  documentation settings, and a whitelisted setup screen for every generated
  `config.py` assignment. The setup contract includes grouped metadata,
  production-readiness checks, a setup checklist, safe multi-line assignment
  replacement, `/appgen/config/setup.json`, and `.env` export text. A generated
  config-admin release gate proves config artifacts, editable-key coverage,
  production readiness, unsafe blocker detection, setup checklists, safe
  assignment rewrites, and environment export behavior. `config_admin_workbench()`
  and `/appgen/config/workbench.json` aggregate the editable schema, grouped
  sections, readiness, checklist, assignment rewrite proof, environment export,
  route surface, and release gate into one IDE configuration review.
- `integrations.py` and `appgen_integrations.html` with generated REST,
  webhook, Salesforce, SAP, Entando, Invenio, payment gateway, SMS gateway,
  and transactional email connector configuration stubs, reviewed request
  plans, signed webhook delivery, outbox envelopes, and first-class
  Entando/Invenio contract descriptors for routes, payloads, permissions, and
  events, plus a generated integration release gate for connector, delivery,
  portal, repository, payment, SMS, email, and artifact coverage.
- `productivity.py` and `appgen_productivity.html` with generated Microsoft
  365 and Google Workspace document, spreadsheet, calendar, and task-sync
  payload contracts. A generated productivity release gate proves provider
  coverage, schema-derived templates, document merge payloads, spreadsheet
  exports, calendar events, task sync, and required productivity artifacts.
  `productivity_workbench()` and `/productivity/workbench.json` aggregate
  provider catalogs, schema-derived templates, document/spreadsheet/calendar/
  task payloads, route coverage, and release-gate evidence before
  `integration.productivity` is marked implemented.
- `lifecycle.py` and `appgen_lifecycle.html` with generated environment
  readiness, custom-domain plans, release gates, maintenance/update windows,
  feedback items, user-testing sessions, and issue reports. A generated
  lifecycle release gate proves environment coverage, production configuration,
  release controls, promotion/domain readiness, maintenance/update plans,
  feedback/testing/issue loops, and required lifecycle artifacts.
  `lifecycle_workbench()` and `/lifecycle/workbench.json` aggregate environment
  catalogs, production readiness, release controls, promotion/domain evidence,
  maintenance/update plans, feedback/testing/issue loops, route surface, and the
  release gate into one generated IDE lifecycle review.
- `emerging.py` and `appgen_emerging.html` with generated IoT device catalogs,
  telemetry validation, device command payloads, blockchain audit anchors,
  smart-contract adapter plans, and edge/offline sync guidance. A generated
  emerging release gate proves device and topic coverage, telemetry and command
  guardrails, hash-only anchor verification, private-channel contract plans,
  edge buffering/retry behavior, and required emerging-tech artifacts.
  `emerging_workbench()` and `/emerging/workbench.json` aggregate those signals
  with route coverage into one IDE-ready IoT and blockchain integration review.
- `tenancy.py` and `appgen_tenancy.html` with generated tenant-column
  detection, tenant context extraction, and filter helpers for row isolation.
  `tenancy_release_gate()` and `tenancy_workbench()` prove tenant catalog
  coverage, header/query/session context resolution, scoped filter helpers,
  tenant requirement checks, route coverage, and required tenancy artifacts
  before `scale.multi-tenancy` is marked implemented.
- `rls.py` and `appgen_rls.html` with generated tenant-aware row-level
  security helpers plus PostgreSQL `CREATE POLICY` SQL, tenant session-setting
  SQL, reviewable database role/user sync SQL for scoped tables, and an
  `rls_release_gate()` that blocks release when tenant filters, PostgreSQL
  policies, role sync, or required RLS artifacts are incomplete.
  `rls_workbench()` exposes IDE-ready policy catalog, tenant filter, row
  filtering, PostgreSQL policy SQL, tenant session SQL, role sync, artifact,
  route, and release-gate evidence before `security.rls` is marked implemented.
- `identity.py` and `appgen_identity.html` with generated OIDC, SAML, LDAP,
  Active Directory, AWS Cognito, and trusted-header SSO provider configuration
  checks plus reviewed LDAP bind/search plans and Cognito hosted-ui OAuth,
  token-exchange, logout, and group-role mapping contracts. A generated
  identity release gate proves SSO provider coverage, provider configuration,
  login planning, LDAP/Active Directory plans, Cognito OAuth metadata,
  reviewable token exchange, and principal normalization. `identity_workbench()`
  exposes IDE-ready provider, login, directory, Cognito OAuth/token/logout,
  group mapping, trusted-header, principal, artifact, route, and release-gate
  evidence before `security.sso` is marked implemented.
- `compliance.py` and `appgen_compliance.html` with generated audit event,
  retention, protected-field redaction, privacy request, subject export,
  erasure planning, and retention-disposition review helpers. A generated
  compliance release gate proves privacy request coverage, redaction, erasure
  review, retention disposition, audit events, and required compliance
  artifacts. `compliance_workbench()` exposes IDE-ready catalog, redaction,
  privacy request, subject export, erasure, retention, audit, artifact, route,
  and release-gate evidence before `security.compliance` is marked implemented.
- `assistant.py` and `appgen_assistant.html` with generated prompt context,
  chatbot field questions, deterministic recommendations, prediction feature
  extraction, and human-review task payloads. The generated
  `assistant_release_gate()` proves artifact coverage, table assistance
  catalogs, non-hidden prompt context, chatbot questions, prediction features,
  recommendation behavior, and human-review payloads. `assistant_workbench()`
  and `/assistant/workbench.json` aggregate those checks with route coverage for
  generated IDE review.
- `intelligence.py` and `appgen_intelligence.html` with generated AI analytics,
  preprocessing, anomaly detection, image/video analysis plans, OCR,
  classification, object-detection contracts, NLP, recommendation, A/B testing,
  and predictive-maintenance contracts. The generated
  `intelligence_release_gate()` proves feature catalogs, anomaly and
  recommendation checks, NLP helpers, local/API vision plans, A/B assignment,
  predictive-maintenance signals, and required intelligence cockpit artifacts.
  `intelligence_workbench()` and `/intelligence/workbench.json` aggregate those
  signals with route coverage for generated IDE review.
- `chatbot.py` and `appgen_chatbot.html` with in-app guided chatbot flows that
  ask for generated view fields, track missing required answers, and prepare
  create payloads. The generated `chatbot_release_gate()` proves artifact
  coverage, intent catalogs, prompt coverage, required-field blocking,
  conversation progression, and create-payload readiness, which makes guided
  creation flows a first-class generated capability.
- `voice.py` and `appgen_voice.html` with generated speech prompts, utterance
  training phrases, slot-filling plans, SSML responses, and Alexa, Google
  Assistant, and Web Speech export contracts. The generated
  `voice_release_gate()` proves provider exports, utterance matching,
  slot-filling readiness, SSML responses, platform model exports, and required
  voice cockpit artifacts. The generated `voice_workbench()` gives the IDE a
  route-backed speech design surface for provider export checks, utterance
  matching, required slot prompts, SSML preview, platform model exports, and
  artifact readiness.
- `agents.py` and `appgen_agents.html` with generated agent plans, local and
  API-key LLM provider readiness checks, provider connection matrices, agent
  tool policies, execution matrices, and agentic release gates. The generated
  `agentic_workbench()` proves local/API-key provider modes, secret-safe API-key
  environment guards, agent/provider links, reviewed tool allowlists, execution
  readiness, release gates, and route coverage before `ai.agentic-systems` is
  marked implemented.
- `designer.py` and `appgen_designer.html` with visual schema graphs, ERD
  exports, reviewable table/field/relationship/workflow proposals, schema-diff
  contracts, migration previews, and regenerated DSL for database design
  workbenches. The generated `schema_diagram_release_gate()` proves required
  designer artifacts, visual graph completeness, Mermaid ERD coverage,
  relationship metadata, diagram readiness, and migration-preview review. The
  generated `visual_modeling_release_gate()` proves the broader visual modeling
  workbench: workspace catalogs, table/field/relationship/workflow proposal
  breadth, schema diffs, reviewed migration previews, DSL regeneration, and
  route coverage for model, relationship, ERD, proposal, migration, and DSL
  endpoints.
- `form_designer.py` and `appgen_form_designer.html` with Delphi-style
  drag-and-drop component palette, snapped form canvas contracts, overlap
  conflict detection, drop proposals, property-inspector metadata, and
  `form_designer_release_gate()` evidence for palette breadth, canvas contracts,
  field-to-component mapping, drop metadata, and overlap guardrails. The
  generated `form_designer_workbench()` proves the fuller Delphi-style design
  surface: palette categories, per-table form generation, field mapping
  matrices, snap/bounds behavior, property inspectors, placement suggestions,
  proposal application, conflict guardrails, and workbench route coverage.
- `nl_evolution.py` and `appgen_nl_evolution.html` with natural-language
  proposal planning for tables, fields, forms, workflows, rules, chatbots,
  agents, reports, dashboards, platform targets, and ERP template modules,
  including executable table DSL for new-table prompts with inferred fields and
  known-table relationship references, approval-ready change sets,
  destructive-intent detection, generated test plans, rollback plans, migration
  impact summaries, existing-DSL patch previews, and
  `nl_evolution_release_gate()` readiness evidence for artifact coverage,
  plain-language scope, review workflow, destructive guardrails, generated test
  plans, and platform target patches. The generated `nl_evolution_workbench()`
  proves prompt-to-plan coverage for database tables/fields, forms, workflows,
  rules, reports, dashboards, chatbots, agents, ERP modules, platform targets,
  DSL patch previews, approval workflows, migration impact, destructive-change
  guardrails, rollback plans, generated test plans, and route coverage.
- `dsl_reference.py` and `appgen_dsl_reference.html` with generated DSL
  keyword-budget checks, compact construct cards, examples, a learning path,
  lightweight lint feedback, structured quick fixes, deterministic formatting,
  fix-result previews, format-result previews, language-ergonomics evidence,
  and authoring-score guidance so every generated app carries an approachable
  reference for the ANTLR language.
- `view_experience.py`, `appgen_view_experience.html`, and
  `appgen-view-experience.js` with generated base-view contracts for offline
  field state, active viewers on the same page, chatbot/help actions, access log
  events, polished page shells, layout-preserving loading skeletons,
  actionable empty states, recoverable error states, app version footer context,
  time-on-page, current-user display, view state matrices, and a
  view-experience release gate. The generated `view_experience_workbench()`
  proves feature catalogs, offline state, presence/access logs, help/footer
  context, polished view states, release gates, and route coverage before
  `ui.view-experience` is marked implemented.
- `support_center.py` and `appgen_support_center.html` with generated
  knowledge-base topics, tutorials, onboarding checklists, searchable support
  entries, support-ticket payloads, and sample DSL applications. The generated
  `support_center_release_gate()` proves artifact coverage, knowledge-base
  breadth, tutorial paths, role-aware onboarding, searchability, usable sample
  DSL, and support-ticket correlation. The generated
  `support_center_workbench()` exposes IDE-ready knowledge-base, tutorial,
  role-onboarding, support search, sample DSL, ticket-correlation, artifact,
  and route-surface evidence.
- `low_code_features.py` and `appgen_low_code_features.html` with a generated
  capability matrix grounded in `docs/ideas.md`, `docs/base_features.md`, and
  `docs/Lo-code features.md`, roadmap alignment, readiness reporting for the
  low-code/no-code platform surface, and an explicit broader-than-JHipster
  benchmark with overlap/AppGen-only rows that keeps JDL interoperability while
  tracking AppGen-only capabilities, superset scorecard gates, and artifact
  evidence proving each required advantage is generated, including database IDE
  workbench evidence. The same contract now
  emits a JHipster-superset blueprint with concrete generated workbench routes
  for design, generation, operations, evolution, and composition workflows so
  the comparison is tied to usable in-app surfaces rather than a static claim.
  A generated superiority-tier gate separately proves preserved baseline
  parity, at least eleven AppGen-only advantages, and generated IDE/workbench
  routes before a release can claim to be more capable than JHipster. A
  generated capability-depth index also requires design-time, generation-time,
  runtime, and governance evidence for every AppGen-only advantage. A generated
  capability-proof matrix then binds every superiority claim to benchmark,
  capability, artifact, depth, and route evidence so AppGen-only claims cannot
  pass as documentation-only assertions. The
  JHipster frontier gate proves advanced JHipster families such as domain
  modeling, front-end targets, service architecture, data operations, quality
  operations, and enterprise experience are preserved before each family is
  exceeded by AppGen-only generated capabilities. A generated feature
  superiority index then scores modeling sources, application targets, IDE/UX,
  enterprise operations, AI/ERP/composition, and migration interoperability so
  every domain must have deeper generated AppGen feature coverage than the
  JHipster baseline plus route and artifact evidence. The generated
  `roadmap_release_audit()` and `/low-code-features/roadmap-release-audit.json`
  bind roadmap-source rows to implemented capability status, generated
  artifacts, critical route surfaces, generated test evidence, and JHipster
  superset gates. The
  application-composition release gate proves reusable block catalog depth,
  dependency topology, reviewable install order, sandbox controls, package
  publication targets, and artifact evidence. The generated composition
  workbench exposes IDE-ready catalog, dependency, reviewed install,
  publication handoff, artifact, and route-surface checks for reusable blocks.
- `prototyping.py` and `appgen_prototyping.html` with rapid mock screens,
  realistic sample data, preview packages, experiment hypotheses, and backlog
  promotion plans for fast stakeholder iteration. The generated
  `prototyping_release_gate()` proves artifact coverage, schema-backed
  prototype catalogs, list/create/detail/dashboard screen coverage, usable
  sample data, portable preview packages, experiment hypotheses, and backlog
  promotion before a prototype is released. The generated
  `prototyping_workbench()` proves resource catalogs, screen mockups, sample
  data, preview packages, experiment hypotheses, backlog promotion, release
  gates, and route coverage before `ui.rapid-prototyping` is marked
  implemented.
- `text_quality.py` and `appgen_text_quality.html` with generated textarea
  spell, grammar, and character-count feedback contracts. The generated
  `text_quality_workbench()` proves textarea catalogs, counters, grammar
  hints, repeated-word detection, per-form feedback, release gates, and route
  coverage before `components.text-quality` is marked implemented.
- `notifications.py` and `appgen_notifications.html` with generated in-app,
  email, webhook, and push-style notification payloads for table events. The
  generated `notification_workbench()` proves channel catalogs, environment
  secret policy, generated table events, payload contracts, queue metadata,
  unknown-channel guardrails, release gates, and route coverage before
  `ops.notifications` is marked implemented.
- `platforms.py` and `appgen_platforms.html` with generated web, PWA, mobile,
  desktop, and chatbot target contracts plus a web/mobile/desktop generation
  matrix, target package matrix, mobile capability contract, and platform
  release gate for downstream adapters. The generated
  `platform_target_experience_gate()` proves the selected target breadth,
  artifact evidence, per-target UX checks, generated route surface, native
  starter coverage, and chatbot table intents as one aggregate
  web/PWA/mobile/desktop/chatbot app-generation contract.
- `frontends/` with generated React, Vue, Angular, Svelte, HTMX, and Express
  starter contracts wired to the generated REST API routes, shared API
  environment variables, route-binding matrices, dev/build command matrices,
  responsive/accessibility quality checks, framework parity matrices for SPA,
  hypermedia, and API-proxy targets, and a front-end generation experience
  gate.
- `sdks/` with generated Python, JavaScript, Java, and C# API client
  scaffolds derived from the same REST table contracts. A generated SDK release
  gate proves multi-language target coverage, scaffold artifacts, REST route
  catalogs, client method names, and OpenAPI path alignment; `sdk_workbench()`
  packages the same target matrix, artifact coverage, method catalog, route
  catalog, OpenAPI alignment, and release decision for generated IDE review.
- `native/` with generated Kivy mobile and BeeWare desktop Python starter
  apps, mobile permission manifests, camera/location capture plans, push
  notification payloads, offline sync batches, conflict-resolution plans,
  offline replay plans, desktop cache snapshots, desktop change-set replay
  plans, desktop local-file actions, offline queue/cache plans, and API route
  contracts. The generated `native_release_gate()` proves selected targets,
  native package files, mobile permissions, mobile offline replay, desktop
  cache replay, and shared API routes before native readiness is claimed.
- `jhipster/app.jdl` and `jhipster/appgen_jhipster.py` with generated
  JHipster JDL exports for Java/TypeScript application generation, preserving
  relation cardinality as JDL `ManyToOne`, `OneToOne`, `OneToMany`, and
  `ManyToMany` blocks. The contract also emits gap analysis and a reviewable
  adoption plan so JHipster remains an interoperability target while AppGen
  provides the broader platform: Python-native web/mobile/desktop starters,
  visual builders, tenant isolation and security governance, agentic systems,
  ERP templates, schema round trips, operational workbenches, native release
  gates, and runtime assurance evidence. The same contract renders an AppGen
  DSL migration draft from the generated JDL shape and exposes
  a migration release gate for upgrading JHipster/JDL-shaped projects into the
  broader AppGen platform. Generated low-code feature contracts also expose a
  JHipster-superset certification gate combining overlap preservation,
  AppGen-only advantage thresholds, roadmap traceability, bidirectional
  JHipster migration readiness, composition readiness, and artifact evidence.
- `chatbots/dialogflow/intents.json`,
  `chatbots/botframework/manifest.json`, and `chatbots/appgen_chatbots.py`
  with generated provider intents, field prompts, conversation checks, provider
  export matrices, and `chatbot_provider_release_gate()` evidence for
  Dialogflow and Bot Framework artifact readiness.
- `automation/node-red/flows.json` and `automation/appgen_node_red.py` with
  generated Node-RED webhook flows for table events, declared workflow
  transitions, webhook endpoint plans, a default Docker Compose Node-RED
  service, runtime readiness checks, flow validation, and
  `node_red_release_gate()` evidence for artifact coverage, event-topic
  coverage, webhook contracts, workflow transition webhooks, and Compose
  runtime readiness. `node_red_workbench()` adds generated IDE evidence for
  artifacts, flow validation, table/workflow webhooks, default runtime, Compose
  service, release decisions, and `/appgen/...` webhook route coverage.
- `rpa.py` and `appgen_rpa.html` with generated robotic-process automation
  task plans, credential readiness checks, BPMN/UML process models, process
  validation, simulation, UiPath/Blue Prism/Automation Anywhere export
  contracts, audit events, and business-process observations for repetitive
  browser/API work. A generated RPA/BPA release gate proves task catalogs,
  process models, BPMN/UML exports, simulations, platform exports, queue
  payloads, credential contracts, audit events, business-process observations,
  and required automation artifacts. `rpa_workbench()` adds generated IDE
  evidence for task catalogs, process models, platform export packages, queue
  payloads, credentials, audit/BPA observations, release decisions, and
  `/rpa/workbench.json` route coverage.
- `collaboration.py` and `appgen_collaboration.html` with generated revision
  metadata, change proposals, review decisions, merge plans, conflict reports,
  merge queues, and conflict-resolution plans for concurrent low-code work. A
  generated collaboration release gate proves proposal review, merge behavior,
  conflict detection, merge queues, conflict-resolution plans, and required
  collaboration artifacts. `collaboration_workbench()` exposes IDE-ready
  proposal, review, merge, conflict, queue, resolution, artifact, release-gate,
  and `/collaboration/workbench.json` route evidence before
  `team.collaboration` is marked implemented.
- `version_control.py` and `appgen_version_control.html` with generated
  manifest snapshots, content-addressed revision IDs, branch plans,
  schema-level diffs, and reviewable rollback plans. A generated version-control
  release gate proves content-addressed snapshots, schema diffs, branch
  contracts, rollback review plans, resource catalogs, and required version
  artifacts. `version_control_workbench()` exposes IDE-ready resource catalog,
  snapshot history, diff, branch, rollback, artifact, release-gate, and
  `/version-control/workbench.json` route evidence before
  `team.version-control` is marked implemented.
- `.vscode/`, `.idea/`, `.project`, `.pydevproject`, `devtools.py`, and
  `appgen_devtools.html` with generated Visual Studio Code, JetBrains
  IDEA/PyCharm, and Eclipse/PyDev launch, task, extension, source-map, and
  readiness contracts. A generated developer-tools release gate proves IDE
  catalogs, VS Code debugging/tasks, JetBrains run configurations/tasks,
  Eclipse/PyDev metadata, schema source maps, and required editor artifacts.
  `devtools_workbench()` adds IDE-ready evidence for tool catalogs, VS Code,
  JetBrains, Eclipse/PyDev, schema source maps, artifact coverage, and
  `/devtools/workbench.json` route coverage before `devops.ide-integration` is
  marked implemented.
- `studio.py` and `appgen_studio.html` with a generated IDE/workbench for DSL
  authoring, DSL linting, outline extraction, keyword-budget checks,
  quick fixes, completions/snippets, searchable command palettes, project trees, editor
  sessions, visual database design, Mermaid ERD export, DBML export, SQL DDL
  preview, read-only SQL workbench/explain-plan guards, parameterized SELECT
  builder, SQL completions, PonyORM preview, table proposals, schema refactor
  plans for table and field renames, migration previews, staged
  generation jobs with deterministic IDs, queue/status/log views, target
  artifact manifests, IDE diagnostics, IDE capability matrices, workflow
  blueprints, multi-application registry, reviewed create/import/open/export
  plans, version history, snapshot/diff/restore plans, app management, code
  editing, breakpoint/debug plans, dependency update plans, app cloning, and
  reusable component repository exports. The Studio also emits a release gate
  that checks DSL linting, database workbench exports, safe SQL, query-builder
  validation, database-design release evidence, capability coverage, generation
  jobs, app portfolio management, versioned management, reviewed edits,
  debug redaction, dependency review, and
  component sharing before IDE readiness is claimed. A separate IDE superiority
  profile proves that the Studio is an integrated low-code IDE for authoring,
  database design, generation, versioned portfolio management, diagnostics, and
  component sharing rather than only a scaffolding command runner, and is the
  manifest evidence for the implemented `devops.studio` capability.
- `realtime.py` and `appgen_realtime.html` with generated event topics,
  Server-Sent Events frames, collaboration messages, and reconnect replay plans.
  A generated realtime release gate proves topic catalogs, event payloads, SSE
  rendering, collaboration message payloads, replay bounds, and required
  realtime artifacts. `realtime_workbench()` exposes IDE-ready topic catalog,
  event payload, SSE frame, collaboration message, replay, artifact,
  release-gate, and `/realtime/workbench.json` route evidence before
  `team.realtime` is marked implemented.
- `diagnostics.py` and `appgen_diagnostics.html` with generated schema
  invariants, row validation, redacted debug snapshots, remediation plans,
  support bundles, API smoke plans, and load-test plans. A generated
  diagnostics release gate proves artifact presence, schema self-tests,
  redaction, remediation planning, support bundle shape, API smoke coverage,
  and load-test planning before debugging readiness is claimed.
  `diagnostics_workbench()` exposes IDE-ready self-test, debug snapshot,
  remediation, support bundle, API smoke, load-test, artifact, release-gate,
  and `/diagnostics/workbench.json` route evidence before
  `quality.diagnostics` is marked implemented.
- `tests/test_generated_coverage.py` with a generated per-table pytest coverage
  matrix for schema, API, UI, reports, security, and data exchange/backup
  flows, plus view-experience, accessibility, diagnostics, release-gate, and
  generated-test artifact coverage. A generated coverage release gate proves
  table areas, workflow areas, experience cases, quality cases, minimum case
  counts, and required quality artifacts before test coverage is claimed.
  `coverage_workbench()` exposes test-runner/IDE-ready table matrix, workflow
  matrix, area catalog, minimum case count, pytest entrypoint, artifact, and
  release-gate evidence before `quality.test-coverage` is marked implemented.
- `code_review.py` and `appgen_code_review.html` with generated automated
  schema and artifact review findings for quality gates. The generated
  `code_review_release_gate()` proves required artifact coverage, schema-rule
  coverage, primary-key checks, searchability review, required-field review,
  and protected-hidden-field review before code quality is claimed.
  `code_review_workbench()` exposes IDE-ready finding catalog, summary,
  artifact review, schema-rule, release-gate, and `/code-review/workbench.json`
  route evidence before `quality.code-review` is marked implemented.
- `components.py` and `appgen_components.html` with generated reusable form,
  list, detail, and card component contracts plus field widget descriptors for
  visual builders. Date, datetime, and time fields produce calendar-aware
  widget contracts with web, mobile, and desktop renderer hints. Custom widgets
  produce reviewable registration plans, renderer mappings, palette entries,
  preview payloads, and accessibility contracts before they are installed. The
  generated `lookup_workbench()` proves relationship picker contracts, enum
  select contracts, label-field selection, UI-ready lookup options, widget
  mappings, and route evidence before `components.lookups` is marked
  implemented. The
  generated `component_release_gate()` proves component catalog coverage,
  widget registry depth, platform renderers, lookup contracts, calendar
  widgets, layout contracts, custom-widget extension points, visual-builder
  payload readiness, and required component artifacts. The generated
  `component_template_workbench()` proves reusable component packages, widget
  descriptors, layout contracts, custom-widget templates, visual-builder
  payloads, release gates, and route evidence before `components.templates` is
  marked implemented. The generated
  `layout_workbench()` proves declared view sections, fallback form sections,
  list/detail/card contracts, visual-builder payloads, and route evidence
  before `ui.layout` is marked implemented.
- `view_composition.py` and `appgen_view_composition.html` with generated
  MasterDetailView, MultipleView, and ChartView contracts derived from schema
  relationships and visible fields. The generated
  `view_composition_release_gate()` proves required artifacts, master/detail
  contracts, optional MultipleView group integrity, ChartView field coverage,
  aggregate catalog shape, and generated FAB view-class support. The generated
  `view_composition_workbench()` proves aggregate catalog, release, and route
  evidence before `ui.view-composition` is marked implemented.
- `tabbed_views.py` and `appgen_tabbed_views.html` with generated tabbed view
  contracts and role-aware permissions per tab. View sections become tabs, and
  declared role permissions on the view table decide which roles can see them.
  The generated `tabbed_views_release_gate()` proves tab artifacts, role
  policies, positive access for allowed roles, and denial for unknown roles
  before tabbed-view readiness is claimed. The generated
  `tabbed_views_workbench()` proves permission matrices, visible-tab filtering,
  positive/negative access checks, release gates, and route coverage before
  `ui.tabbed-views` is marked implemented.
- `erp_templates.py` and `appgen_erp_templates.html` with reusable ERP module
  templates for ledgers, accounts, invoicing, AP, AR, inventory, HR, payroll,
  purchasing, procurement, supply chain, warehouse management, manufacturing,
  sales, CRM, e-commerce, assets, maintenance, quality management, document
  management, compliance, projects, and reports. Each module includes table-level
  field blueprints, references, workflows, reports, and AppGen DSL export helpers
  plus recommended finance, distribution, people, manufacturing, and full-ERP
  starter stacks, composite ERP DSL, generation plans, and legacy ERP migration
  plans. Generated ERP packages also include domain coverage reports,
  implementation roadmaps, and ERP release gates so users can start from
  realistic, deployable ERP components rather than empty placeholder tables.
  The generated `erp_template_workbench()` proves full module coverage, table
  blueprints, starter stacks, domain coverage, composite DSL, starter manifests,
  generation/migration plans, release gates, and route coverage before
  `components.erp-templates` is marked implemented.
- `project_management.py` and `appgen_project_management.html` with generated
  agile backlog, sprint, release, traceability, and Jira/GitHub/Azure
  Boards/GitLab issue-export contracts, plus a project-management release gate
  for provider coverage, backlog/sprint readiness, release controls,
  traceability, DevOps exports, and required artifacts.
  `project_management_workbench()` exposes IDE-ready provider, backlog, sprint,
  release, traceability, DevOps export, artifact, release-gate, and
  `/project-management/workbench.json` route evidence before
  `devops.project-management` is marked implemented.
- `wizards.py` and `appgen_wizards.html` with generated sequential table
  creation wizards and workflow process wizards derived from existing tables
  and `flow` declarations. The generated `wizard_release_gate()` proves table
  and workflow wizard coverage, field prompts, step validation, progression
  behavior, and required wizard artifacts before wizard readiness is claimed.
  The generated `wizard_workbench()` proves catalog, table/workflow wizard
  coverage, session payloads, reviewable submission plans, workflow progression,
  release gates, and route evidence before `ui.wizards` is marked implemented.
- `events.py` and `appgen_events.html` with generated complex event
  processing, alerting, retry, and dead-letter contracts. The generated
  `event_release_gate()` proves artifact coverage, table/workflow topic
  catalogs, event envelope shape, processing actions, failure alerting,
  retry/dead-letter behavior, and workflow-event handling. `event_workbench()`
  adds generated IDE evidence for topic catalogs, event envelopes, processing
  plans, failure alerting, retry/dead-letter behavior, workflow events, release
  decisions, and `/events/workbench.json` route coverage.
- `api_testing.py` and `appgen_api_testing.html` with generated automated API
  testing, pytest module rendering, smoke/load fixture handoff plans tied to
  generated seed scenarios, UI smoke-test plans, Playwright-style smoke module
  rendering, execution plans, contract coverage, result evaluation, and
  synthetic monitoring contracts. A generated API testing release gate combines
  artifact readiness, request matrices, response validation, fixture strategy,
  UI smoke coverage, synthetic monitoring, OpenAPI contract coverage, and
  rendered pytest/Playwright modules. `api_testing_workbench()` exposes
  IDE-ready request matrix, response validation, fixture, UI smoke, synthetic
  monitor, OpenAPI coverage, rendered module, execution-plan, artifact,
  release-gate, and `/api-testing/workbench.json` route evidence before
  `quality.api-testing` is marked implemented.
- `openapi.py`, `appgen_openapi.html`, and `docs/openapi.json` with generated
  OpenAPI 3.1 API documentation. A generated `openapi_workbench()` proves
  artifact readiness, OpenAPI version, path catalogs, operation contracts,
  component schemas, bearer-token security metadata, release gates, and route
  coverage before `api.openapi` is marked implemented.
- `microservices.py` and `appgen_microservices.html` with generated service
  boundaries, gateway routes, event routes, cross-service relationship
  resolvers, consistency reviews, service-mesh mTLS/authorization/telemetry
  policies, canary traffic-shift plans, health probes, and scaling plans. A
  generated microservice release gate proves service catalogs, gateway routes,
  event ownership, relationship consistency, service-mesh policy,
  health/scaling plans, and canary rollback. `microservice_workbench()` adds
  generated IDE evidence for artifact coverage, service catalogs, gateway and
  event routes, relationships, service-mesh policy, health/scaling plans,
  canary rollback, release decisions, and `/microservices/workbench.json` route
  coverage.
- `usage_analytics.py` and `appgen_usage_analytics.html` with generated
  adoption, funnel, retention, and real-time app-usage analytics. A generated
  analytics release gate proves event catalog coverage, activity summaries,
  adoption, funnels, retention, realtime snapshots, and required analytics
  artifacts. `usage_analytics_workbench()` exposes IDE-ready evidence for
  event catalogs, activity summaries, adoption, funnels, retention, realtime
  snapshots, artifact readiness, release decisions, and
  `/usage-analytics/workbench.json` route coverage.
- `seed.py` with relationship-aware deterministic demo data, dependency-ordered
  seed plans, demo/smoke/load fixture scenarios, table factories, pytest fixture
  modules, validation, anonymized fixture exports, SQL previews, scenario
  matrices, and a seed release gate that proves dependency order, fixture
  validation, anonymized export readiness, SQL preview coverage, and required
  seed/test/quality artifacts. `seed_workbench()` exposes IDE-ready plan,
  dependency order, scenario matrix, smoke fixture, anonymized export, SQL
  preview, validation, artifact, and release-gate evidence before `data.seed`
  is marked implemented;
  `docs/schema.md` with table,
  field, relationship, and Mermaid ERD documentation, and
  `docs/data-dictionary.json` / `docs/data-dictionary.md` with
  machine-readable structure, content-kind, sample-value, display-field, and
  writable-field metadata. The generated
  `docs/documentation-workbench.json` proves schema Markdown, data dictionary
  JSON/Markdown, OpenAPI, accessibility baseline, and documentation artifact
  coverage before `api.documentation` is marked implemented.
- `docs/accessibility.md` with a generated accessibility baseline checklist
  referenced by the generated accessibility workbench and release evidence.
- `.github/workflows/appgen-ci.yml` and `scripts/appgen_quality.py` with a
  generated CI quality gate for syntax, manifest, PWA, docs, runtime assurance,
  and test-surface checks. The generated quality script exposes
  `ci_pipeline_contract()` and `ci_release_gate()` to prove workflow artifacts,
  required CI stages, quality/test commands, and generated test artifact
  coverage before `devops.cicd` is marked implemented.
- `deploy/` with Docker/Compose-adjacent Kubernetes manifests, Kubernetes HPA
  autoscaling manifests, on-prem topology plans, Terraform starter contracts
  for AWS, GCP, and Azure, generated deployment runbooks, secret-injection
  plans, smoke checks, rollback plans, release promotion plans, infrastructure
  scaling plans, cloud readiness helpers, and a deployment release gate covering
  Docker, Compose, HTTPS, Kubernetes, on-prem, AWS, GCP, Azure, PostgreSQL, and
  MySQL readiness evidence. `deployment_workbench()` exposes IDE-ready target,
  artifact, database, cloud readiness, Terraform, autoscale, secret, smoke,
  runbook, rollback, promotion, on-prem, and release-gate evidence before
  `deployment.cloud` is marked implemented.
- `deploy/Caddyfile` and `deploy/appgen_https.py` with generated automatic
  HTTPS reverse proxy configuration and TLS readiness checks. The generated
  `https_release_gate()` and `https_workbench()` prove Caddy artifact coverage,
  public TLS environment, localhost fallback, upstream and TLS ports, HSTS/header
  expectations, and release readiness before `security.https` is marked
  implemented.
- `appgen.json`, a manifest containing tables, relations, views, workflows,
  roles, and low-code platform capability targets.
- The generated designer exposes graph nodes/edges plus table, field, and
  workflow-step proposal helpers so visual model edits can regenerate DSL. It
  also exports Mermaid ERD text and a relationship matrix for database design
  tools.
