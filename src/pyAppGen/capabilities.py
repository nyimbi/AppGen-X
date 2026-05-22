"""Low-code platform capability contracts.

The roadmap spans visual modeling, generated APIs, workflow, deployment,
security, collaboration, and operations.  Generated apps carry this manifest so
future DSL, designer, documentation, and deployment tools can target the same
explicit contract instead of inferring features from generated Python files.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path

from .schema import AppSchema
from .schema import normalize_platform_targets


@dataclass(frozen=True)
class Capability:
    key: str
    label: str
    status: str
    evidence: str


DEFAULT_CAPABILITIES: tuple[Capability, ...] = (
    Capability("schema.import", "DBML, SQL, PonyORM, and database import", "implemented", "canonical schema adapters with DBML table groups and unique indexes, live unique/search indexes and computed columns, SQL comments, identity/generated columns, SQL enum/ALTER TABLE support, static PonyORM enum/type/index normalization, and generated import provenance, source fidelity, validation, and review cockpit"),
    Capability("dsl.language-design", "ANTLR DSL reference, keyword budget, examples, linting, and quick fixes", "implemented", "generated DSL reference cockpit, ANTLR integrity, compact keyword budget, language-experience gate, examples, readability lint helpers, deterministic formatting, authoring release gate, and structured quick fixes"),
    Capability("codegen.fab", "Flask-AppBuilder app generation", "implemented", "models, views, templates, support files"),
    Capability("ui.visual-modeling", "Visual data, form, and workflow modeling", "implemented", "generated designer graph, ERD exports, relationship matrix, table/field/relationship/workflow edit proposals, schema diffs, migration previews, DSL regeneration helpers, visual modeling workbench, route surface, and visual modeling release gate"),
    Capability("ui.view-composition", "Master-detail, multiple-view, and chart view composition", "implemented", "generated relationship-driven MasterDetailView, MultipleView, and ChartView contracts, composed-view catalogs, chart field coverage, generated view-class evidence, workbench route, and release gates"),
    Capability("ui.tabbed-views", "Tabbed views with permissions per tab", "implemented", "generated tab contracts, role-aware per-tab access policies, permission matrices, positive/negative access checks, visible tab filtering, workbench route, and release gates"),
    Capability("ui.form-designer", "Delphi-style drag-and-drop form designer", "implemented", "generated component palette categories, per-table form workbench, field-to-component mapping matrix, snapped canvas bounds, property inspector metadata, placement suggestions, drop proposal application, overlap guardrails, route surface, and form designer release/workbench gates"),
    Capability("ui.nl-evolution", "Natural-language application evolution", "implemented", "generated NL proposal parser and workbench for tables, fields, forms, workflows, rules, reports, dashboards, chatbots, agents, platform targets, ERP modules, DSL patch previews, approval workflows, migration impact, destructive-change guardrails, rollback plans, generated test plans, and route/release gates"),
    Capability("ui.rapid-prototyping", "Rapid prototyping and preview packages", "implemented", "generated schema-backed mock screens, realistic sample data, prototype plans, portable preview packages, experiment hypotheses, backlog promotion, workbench route, and release gates"),
    Capability("ui.view-experience", "Shared generated view experience", "implemented", "generated offline field state, active viewers, help/chatbot actions, access logs, polished shell/loading/empty/error states, version footer, time-on-page, current-user context, view state matrices, browser helper, workbench route, and release gates"),
    Capability("ui.layout", "Declarative screen sections and tabs", "implemented", "generated declared view sections, fallback form sections, list/detail/card layout contracts, visual-builder payloads, layout workbench route, and release evidence"),
    Capability("ui.responsive", "Responsive customizable generated UI", "implemented", "generated breakpoint tokens, mobile/tablet/desktop/wide viewport contracts, responsive layout recipes, touch density, visual matrices, responsive workbench route, and UI release evidence"),
    Capability("ui.branding", "Customizable branding and theming", "implemented", "generated theme CSS, branding contract, design-system report, layout recipes, viewport contracts, component state matrices, visual regression plans, typography scale, density modes, quality report, responsive evidence, branding workbench route, and preview cockpit"),
    Capability("ui.wizards", "Sequential input and process wizards", "implemented", "generated table creation and workflow wizard contracts, field questions, step validation, session payloads, reviewable submission plans, workflow progression, workbench route, and release gates"),
    Capability("ui.pwa", "Progressive web app and offline shell", "implemented", "generated web manifest, service worker, offline shell, icon, theme assets, PWA cockpit, installability matrix, safe fetch scope, and PWA release gate"),
    Capability("platform.targets", "Web, PWA, mobile, desktop, and chatbot target contracts", "implemented", "generated platform descriptors, generation artifacts, export contracts, target package matrix, target experience matrix, platform release gate, and aggregate web/PWA/mobile/desktop/chatbot target experience gate"),
    Capability("platform.frontends", "React, Vue, Angular, Svelte, HTMX, and Express front-end scaffolds", "implemented", "generated React, Vue, Angular, Svelte, HTMX, and Express starter files, hypermedia/API-proxy starters, shared API contracts, route bindings, command matrix, quality matrix, framework parity matrix, and front-end generation experience gate"),
    Capability("platform.microservices", "Microservices architecture support", "implemented", "generated service boundaries, gateway routes, event routes, cross-service relationship resolver contracts, health probes, scaling policies, service mesh, canary release plans, microservice workbench route, and release gates"),
    Capability("platform.native", "Python mobile and desktop app scaffolds", "implemented", "generated Kivy mobile and BeeWare desktop starters with mobile permission manifests, camera/location plans, push payloads, desktop file actions, offline queues, cache plans, native release gate, and aggregate platform target experience evidence"),
    Capability("platform.jhipster", "JHipster JDL export and interoperability", "implemented", "generated JHipster JDL, import contract, gap analysis, adoption plan, bidirectional migration plan, and broader-than-JHipster comparison in the low-code matrix"),
    Capability("platform.competitive-benchmark", "JHipster-plus capability benchmark", "implemented", "generated roadmap source report, overlap, AppGen-only benchmark rows, artifact evidence, capability-depth proof, frontier gate, and superset scorecard gates for visual builders, database IDE, native targets, agentic systems, NL evolution, ERP templates, studio operations, runtime assurance, and schema import"),
    Capability("platform.jhipster-superiority", "Measurable JHipster-superiority release gate", "implemented", "generated superiority tiers, feature superiority index, preserved JHipster parity, AppGen-only advantage thresholds, and generated IDE/workbench routes before superiority claims are allowed"),
    Capability("platform.chatbots", "Dialogflow and Bot Framework chatbot exports", "implemented", "generated chatbot intents, prompts, provider manifests, provider export matrix, artifact coverage checks, and provider release gate"),
    Capability("ai.guided-chatbot", "In-app guided chatbot creation flows", "implemented", "generated chatbot view, schema prompts, conversation state, required-field blocking, create payloads, and guided chatbot release gate"),
    Capability("ai.voice-assistant", "Voice assistant and speech interface generation", "implemented", "generated speech prompts, utterances, slots, SSML responses, Alexa/Google/Web Speech exports, voice workbench route, provider export checks, utterance matching, slot-filling readiness, platform model exports, and release gates"),
    Capability("components.templates", "Reusable templates and modules", "implemented", "generated component template packages, widget descriptors, custom widget contracts, registration plans, previews, palette entries, visual-builder payloads, layout contracts, template workbench route, and release gates"),
    Capability("components.lookups", "Relationship and enum lookup fields", "implemented", "DSL references and enums generate manifest metadata, SQLAlchemy relationship columns, relationship picker contracts, enum select contracts, label fields, UI-ready lookup choices, lookup workbench route, and release evidence"),
    Capability("components.media", "Image and file upload fields", "implemented", "generated image/file upload catalogs, extension/MIME/size validation, unsafe-upload rejection, sanitized storage paths, preview contracts, media workbench route, and release gates"),
    Capability("components.text-quality", "Textarea spell, grammar, and character counts", "implemented", "generated textarea catalogs, character and word counters, grammar and repeated-word hints, per-form feedback, text quality workbench route, and release gates"),
    Capability("content.document-management", "Document management, versioning, retention, and e-signature contracts", "implemented", "generated document libraries, version envelopes, approval workflows, retention policies, e-signature payloads, audit events, document workbench route, and release gates"),
    Capability("components.erp-templates", "ERP component templates", "implemented", "generated ledgers, accounts, invoicing, AP, AR, inventory, HR, payroll, purchasing, procurement, supply chain, warehouse, manufacturing, sales, CRM, ecommerce, assets, maintenance, quality, documents, compliance, projects, report templates, recommended ERP stacks, composite ERP DSL, starter manifests, generation plans, legacy migration plans, domain coverage, implementation roadmaps, ERP workbench, and release gates"),
    Capability("components.application-composition", "Application composition marketplace and install plans", "implemented", "generated composable blocks for schema, visual builders, workflows, ERP modules, agents, integrations, native targets, dependency topology, reviewed install plans, reusable packages, Entando/Invenio/Cookiecutter publication handoffs, composition workbench route, and release gates"),
    Capability("platform.extensibility", "Custom code extension hooks", "implemented", "generated hook registry, app_custom extension package, lifecycle dispatch, packaging handoff, extension workbench route, and release gates"),
    Capability("api.rest", "REST API generation", "implemented", "schema-driven ModelRestApi files"),
    Capability("api.graphql", "GraphQL schema generation", "implemented", "schema-driven Graphene schema files"),
    Capability("data.access", "Low-code query, mutation, and validation contracts", "implemented", "generated table read/write contracts with filters, sorting, paging, projections, saved queries, mutation plans, audit events, data access workbench route, and release gates"),
    Capability("api.documentation", "Automatic API and schema documentation", "implemented", "generated README, schema docs, data dictionary, content guide, OpenAPI docs, accessibility baseline, documentation workbench contract, and quality gates"),
    Capability("api.openapi", "OpenAPI contract generation", "implemented", "generated OpenAPI 3.1 spec, docs/openapi.json, API docs view, OpenAPI workbench route, and release gates"),
    Capability("api.sdks", "Multi-language API SDK exports", "implemented", "generated Python, JavaScript, Java, and C# client scaffolds, route catalogs, method catalogs, OpenAPI alignment checks, SDK workbench contract, and release gates"),
    Capability("data.exchange", "Schema-aware CSV and JSON data exchange", "implemented", "generated import templates, row validation, export helpers, reviewed migration batches, request contracts, data exchange workbench route, and release gates"),
    Capability("data.search", "Schema-aware full-text search", "implemented", "generated search indexes, provider adapter plans, Elasticsearch mappings, Whoosh schemas, reviewed reindex runbooks, search workbench route, and release gates"),
    Capability("data.database-ops", "Database provider and operations contracts", "implemented", "generated PostgreSQL, MySQL, SQLite, MongoDB, DynamoDB, Cassandra, Redis, Patroni, PostGraphile, ZomboDB, Elasticsearch, Compose, Kubernetes, NoSQL, migration cutover, database operations workbench route, and release gates"),
    Capability("operations.inventory-traceability", "Barcode, RFID, and inventory traceability operations", "implemented", "generated scan targets, barcode labels, RFID payloads, stock movements, cycle counts, reconciliation helpers, inventory workbench route, and release gates"),
    Capability("operations.finance", "Tax, multicurrency, forecasting, and batch finance operations", "implemented", "generated tax calculations, exchange-rate conversion plans, budget forecasts, revenue schedules, batch processing helpers, finance workbench route, and release gates"),
    Capability("operations.manufacturing", "Manufacturing, MRP, capacity planning, and production scheduling", "implemented", "generated BOM plans, material requirements, capacity checks, finite schedules, purchase requisitions, kanban signals, manufacturing workbench route, and release gates"),
    Capability("workflow.automation", "Low-code workflow and decision trees", "implemented", "generated transition runtime, role-aware authorization flows, approval routes, SLA runbooks, transition proposals, aggregate workflow workbench route, and release gates"),
    Capability("workflow.statecharts", "FSM and state-chart workflow exports", "implemented", "generated Mermaid state diagrams, FSM JSON, SCXML, authorization flows, workflow graph validation, aggregate workflow workbench route, and release gates"),
    Capability("logic.business-rules", "Low-code business rules and decisions", "implemented", "generated rule validation, decision helpers, decision trees, decision traces, rules workbench route, and release gates"),
    Capability("automation.node-red", "Node-RED automation runtime", "implemented", "generated Node-RED flow export, webhook contracts, default Docker Compose service, runtime descriptor, workbench evidence, and release gates"),
    Capability("automation.cep", "Complex event processing and alerting", "implemented", "generated event catalog, CEP rule matching, alerting, retry, dead-letter contracts, event workbench route, and release gates"),
    Capability("automation.rpa-bpa", "Robotic process automation and business-process analysis", "implemented", "generated RPA task plans, credential readiness, BPMN/UML process models, simulations, UiPath/Blue Prism/Automation Anywhere exports, bottleneck analysis, process observations, audit events, RPA workbench route, and release gates"),
    Capability("security.rbac", "Role-based access control", "implemented", "generated role policy helpers, principal normalization, authorization decisions, audit events, policy matrices, reviewed RBAC change proposals, threat models, secret scans, dependency security plans, API security tests, security workbench evidence, release gates, and security signoff envelopes"),
    Capability("security.session", "Session timeout and runtime hardening", "implemented", "generated inactivity timeout, public-path bypass, activity markers, session-state checks, security-header hooks, runtime security workbench route, artifact evidence, route coverage, and release gates"),
    Capability("security.https", "Automatic HTTPS deployment", "implemented", "generated Caddy reverse proxy, TLS environment checks, localhost fallback, upstream/port contracts, HSTS/header expectations, HTTPS workbench evidence, artifact evidence, and release gates"),
    Capability("security.rls", "Tenant-aware row-level security", "implemented", "DSL-declared RLS targets, generated Python RLS helpers, PostgreSQL policy SQL, tenant session-setting SQL, reviewable database role/user sync SQL, RLS workbench route, artifact evidence, route coverage, and release gates"),
    Capability("security.sso", "SSO and enterprise authentication", "implemented", "generated OIDC, SAML, LDAP, Active Directory, AWS Cognito hosted-ui OAuth/token/logout contracts, group-role mapping, trusted-header registry, identity workbench route, artifact evidence, route coverage, and release gates"),
    Capability("security.compliance", "Compliance-oriented data protection", "implemented", "generated audit events, retention policy, redaction, privacy requests, subject exports, erasure plans, retention-disposition reviews, compliance workbench route, artifact evidence, route coverage, and release gates"),
    Capability("reports.analytics", "Reports, dashboards, and analytics", "implemented", "generated table, join, and three-way report catalogs plus dashboard contracts, CSV/PDF exports, email delivery payloads, report query plans, reports workbench route, export evidence, relationship report evidence, and release gates"),
    Capability("reports.usage-analytics", "Application usage analytics", "implemented", "generated usage events, adoption, funnels, retention, real-time activity summaries, IDE usage workbench route, artifact evidence, route coverage, and release gates"),
    Capability("data.visualization", "Charts, graphs, and KPI visualization", "implemented", "generated dashboards, chart data contracts, Vega-Lite specs, accessible summaries, web/mobile/desktop renderer workbenches, aggregate visualization workbench route, analytics payload evidence, route coverage, and release gates"),
    Capability("i18n.localization", "Internationalization and localization", "implemented", "generated Babel config, translation catalogs, locale negotiation, missing-key reports, localization cockpit, localization workbench route, fallback translation checks, runtime payloads, artifact evidence, and release gates"),
    Capability("a11y.compliance", "Accessibility compliance", "implemented", "generated WCAG checklist, skip-link baseline, keyboard navigation plans, ARIA landmark contracts, accessibility audit plans, IDE accessibility workbench route, documentation baseline evidence, route coverage, and release gates"),
    Capability("deployment.cloud", "Cloud and on-prem deployment", "implemented", "generated Docker, Compose, HTTPS, Kubernetes, HPA autoscaling, on-prem, AWS/GCP/Azure Terraform scaffolds, secret plans, smoke checks, topology reports, deployment runbooks, rollback plans, release promotion, infrastructure scaling, cloud readiness matrix, deployment workbench evidence, and release gates"),
    Capability("devops.cicd", "CI/CD and automated review gates", "implemented", "generated GitHub Actions workflow, quality script, CI pipeline contract, required stage evidence, command coverage, artifact coverage, and CI release gate"),
    Capability("devops.packaging", "Publishable package and reusable templates", "implemented", "generated pyproject, MANIFEST, package contract, FAB extension metadata, Cookiecutter scaffold, packaging workbench payload, and release gates"),
    Capability("devops.ide-integration", "Visual Studio Code, JetBrains, and Eclipse workspace integration", "implemented", "generated VS Code launch/tasks/extensions, JetBrains IDEA/PyCharm run configs, Eclipse PyDev project files, IDE workbench route, schema source-map evidence, artifact evidence, route coverage, and release gates"),
    Capability("devops.studio", "In-app developer studio", "implemented", "generated project tree, searchable command palette, DSL outline/lint/quick-fix/completions, database table proposals, safe SQL workbench plans, generation jobs, multi-application registry, create/import/open/export plans, diagnostics, code-edit plans, debug sessions, dependency update plans, app cloning, component sharing, Studio release gate, database-design release gate, and IDE superiority profile"),
    Capability("devops.project-management", "Agile project and DevOps tool integration", "implemented", "generated backlog, sprint, release, traceability, Jira/GitHub/Azure Boards/GitLab export contracts, project-management workbench route, artifact evidence, route coverage, and release gates"),
    Capability("support.training", "Generated training, support, tutorials, and sample apps", "implemented", "generated support center, knowledge-base topics, onboarding checklists, tutorials, sample DSL apps, search, support-ticket payloads, support workbench route, role onboarding evidence, route coverage, and release gates"),
    Capability("team.collaboration", "Collaboration and version-control workflows", "implemented", "generated change proposals, revision IDs, review decisions, conflict reports, merge queues, resolution plans, collaboration workbench route, artifact evidence, route coverage, and release gates"),
    Capability("team.version-control", "Low-code version history and rollback", "implemented", "generated manifest snapshots, branch plans, diffs, rollback plans, version-control workbench route, artifact evidence, route coverage, and release gates"),
    Capability("team.realtime", "Real-time collaboration and event streams", "implemented", "generated event topics, SSE frames, collaboration message payloads, replay plans, realtime workbench route, artifact evidence, route coverage, and release gates"),
    Capability("quality.diagnostics", "Testing, debugging, and diagnostic tools", "implemented", "generated self-tests, debug snapshots, remediation plans, redacted support bundles, API smoke plans, load-test plans, diagnostics workbench route, artifact evidence, route coverage, and release gates"),
    Capability("quality.api-testing", "Automated API and UI smoke testing plus synthetic monitoring", "implemented", "generated API request catalog, response expectations, pytest module rendering, UI smoke plans, Playwright-style module rendering, execution plans, contract coverage, monitor probes, API testing workbench route, artifact evidence, route coverage, and release gates"),
    Capability("quality.code-review", "Automated code review", "implemented", "generated schema and artifact review findings, summaries, code-review workbench route, route coverage, and release gates"),
    Capability("quality.test-coverage", "Generated test coverage", "implemented", "generated per-table pytest coverage matrix for schema, API, UI, reports, security, data flows, workflow coverage, coverage workbench evidence, pytest entrypoints, artifact evidence, and release gates"),
    Capability("data.migrations", "Database migrations", "implemented", "generated Alembic scaffold, schema inventory, revision plans, SQL previews, rollback plans, review checklists, migration workbench evidence, and release gates"),
    Capability("data.seed", "Database seed data", "implemented", "generated relationship-aware deterministic seed script with dependency-ordered insert plans, demo/smoke/load scenarios, table factories, validation, anonymized fixture exports, SQL previews, seed workbench evidence, and release gates"),
    Capability("ops.notifications", "Notifications and alert delivery", "implemented", "generated in-app, email, webhook, and push notification payloads, event queues, secret policy checks, notification workbench route, and release gates"),
    Capability("ops.monitoring", "Monitoring, alerting, and error handling", "implemented", "generated liveness/readiness endpoints, JSON error envelopes, monitoring workbench route, endpoint route coverage, artifact evidence, and release gates"),
    Capability("ops.resilience", "Automatic error handling and exception management", "implemented", "generated exception taxonomy, safe error responses, recovery actions, retry plans, circuit breakers, incident reports, resilience workbench route, route coverage, artifact evidence, and release gates"),
    Capability("ops.performance", "Performance budgets and scaling plans", "implemented", "generated SLO budgets, pagination/cache plans, load-test matrices, k6 and Locust exports, reviewed runbooks, autoscale recommendations, performance workbench route, route coverage, artifact evidence, and release gates"),
    Capability("ops.assurance", "Runtime assurance and readiness management", "implemented", "generated assurance matrix, runtime assurance report, artifact checks, application release gate, generated app excellence gate, runtime assurance workbench route, route coverage, and release gates"),
    Capability("ops.configuration", "Runtime configuration management", "partial", "generated config.py setup editor, readiness checks, checklist, and .env export"),
    Capability("ops.lifecycle", "Environment, release, feedback, and lifecycle management", "partial", "generated environment readiness, custom-domain plans, release gates, maintenance windows, feedback, and issue reports"),
    Capability("ops.backup", "Backup and disaster recovery", "partial", "generated JSON backup exports, integrity manifests, autobackup schedules, retention plans, recovery runbooks, and restore helpers"),
    Capability("scale.multi-tenancy", "Multi-tenancy and scaling", "partial", "generated tenant-scope registry and filter helpers"),
    Capability("integration.enterprise", "Enterprise service integrations", "partial", "generated REST, webhook, Salesforce, SAP, Entando, Invenio, payment gateway, SMS gateway, transactional email registry, signed webhook plans, idempotency keys, outbox envelopes, and delivery audit events"),
    Capability("integration.productivity", "Microsoft 365 and Google Workspace productivity integrations", "partial", "generated document, spreadsheet, calendar, and task-sync payload contracts"),
    Capability("integration.emerging", "IoT and blockchain integration contracts", "partial", "generated device telemetry, edge sync, command, and blockchain audit-anchor contracts"),
    Capability("ai.assistance", "AI and machine-learning assistance", "partial", "generated assistant context, recommendations, prediction hooks, and review tasks"),
    Capability("ai.intelligence", "AI analytics, computer vision, NLP, recommendation, and UX optimization", "partial", "generated feature preprocessing, anomaly detection, image/video analysis plans, OCR/classification/object-detection contracts, NLP helpers, A/B testing, and predictive maintenance"),
    Capability("ai.agentic-systems", "Agentic systems with local and API-key LLM providers", "implemented", "DSL llm/agent blocks, generated local/API-key provider catalogs, provider readiness matrices, API-key environment guards, secret-safe provider policies, agent catalogs, reviewed tool policies, execution matrices, agentic workbench, cockpit routes, and release gates"),
)


def build_manifest(schema: AppSchema) -> dict:
    """Build a generated-app manifest from the canonical schema."""
    platform_targets, unknown_platform_targets = normalize_platform_targets(
        schema.app_options.get("targets")
    )
    return {
        "schema_version": "0.1",
        "app_name": schema.app_name,
        "app_options": dict(schema.app_options),
        "platform_targets": list(platform_targets),
        "unknown_platform_targets": list(unknown_platform_targets),
        "source": schema.source,
        "source_profile": schema.source_profile(),
        "source_fidelity": schema.source_fidelity_report(),
        "tables": [
            {
                "name": table.name,
                "columns": [
                    {
                        "name": column.name,
                        "type": column.type_name,
                        "nullable": column.nullable,
                        "primary_key": column.primary_key,
                        "unique": column.unique,
                        "default": column.default,
                        "references": list(column.references) if column.references else None,
                        "hidden": column.hidden,
                        "searchable": column.searchable,
                        "derived": column.derived,
                        "expression": column.expression,
                        "source_group": column.source_group,
                    }
                    for column in table.columns
                ],
            }
            for table in schema.tables
        ],
        "relations": [asdict(relation) for relation in schema.relations],
        "views": [asdict(view) for view in schema.views],
        "flows": [asdict(flow) for flow in schema.flows],
        "roles": [asdict(role) for role in schema.roles],
        "rules": [asdict(rule) for rule in schema.rules],
        "enums": [asdict(enum) for enum in schema.enums],
        "llm_providers": [asdict(provider) for provider in schema.llm_providers],
        "agents": [asdict(agent) for agent in schema.agents],
        "capabilities": [asdict(capability) for capability in DEFAULT_CAPABILITIES],
    }


def write_manifest(schema: AppSchema, output_dir: str | Path) -> Path:
    """Write the generated app's low-code capability manifest."""
    output_path = Path(output_dir) / "appgen.json"
    output_path.write_text(json.dumps(build_manifest(schema), indent=2, sort_keys=True) + "\n")
    return output_path
