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
    Capability("schema.import", "DBML, SQL, PonyORM, and database import", "implemented", "canonical schema adapters with DBML/live unique indexes, SQL enum/ALTER TABLE support, static PonyORM enum/type normalization, and generated import provenance, validation, and review cockpit"),
    Capability("dsl.language-design", "ANTLR DSL reference, keyword budget, examples, linting, and quick fixes", "partial", "generated DSL reference cockpit, keyword budget checks, examples, readability lint helpers, and structured quick fixes"),
    Capability("codegen.fab", "Flask-AppBuilder app generation", "implemented", "models, views, templates, support files"),
    Capability("ui.visual-modeling", "Visual data, form, and workflow modeling", "partial", "generated designer graph, table/field/relationship edit proposals, schema diffs, migration previews, and DSL regeneration helpers"),
    Capability("ui.view-composition", "Master-detail, multiple-view, and chart view composition", "partial", "generated relationship-driven view composition contracts and cockpit"),
    Capability("ui.tabbed-views", "Tabbed views with permissions per tab", "partial", "generated tab contracts and role-aware per-tab access policies"),
    Capability("ui.form-designer", "Delphi-style drag-and-drop form designer", "partial", "DSL component placements, generated component palette, form canvas contracts, and drop proposals"),
    Capability("ui.nl-evolution", "Natural-language application evolution", "partial", "generated NL proposal parser for tables, fields, forms, chatbots, agents, platform targets, and ERP template modules"),
    Capability("ui.rapid-prototyping", "Rapid prototyping and preview packages", "partial", "generated mock screens, sample data, prototype plans, experiment hypotheses, and backlog promotion"),
    Capability("ui.view-experience", "Shared generated view experience", "partial", "generated offline field state, active viewers, help/chatbot actions, access logs, version footer, time-on-page, and current-user context"),
    Capability("ui.layout", "Declarative screen sections and tabs", "partial", "view sections feed generated FAB metadata and component form layouts"),
    Capability("ui.responsive", "Responsive customizable generated UI", "partial", "FAB templates and view mixins"),
    Capability("ui.branding", "Customizable branding and theming", "partial", "generated theme CSS, branding contract, design-system report, layout recipes, typography scale, density modes, quality report, and preview cockpit"),
    Capability("ui.wizards", "Sequential input and process wizards", "partial", "generated table creation and workflow wizard contracts"),
    Capability("ui.pwa", "Progressive web app and offline shell", "partial", "generated web manifest and service worker"),
    Capability("platform.targets", "Web, PWA, mobile, desktop, and chatbot target contracts", "partial", "generated platform descriptors, generation artifacts, and export contracts"),
    Capability("platform.frontends", "React, Vue, Angular, Svelte, HTMX, and Express front-end scaffolds", "partial", "generated front-end starter files, hypermedia starters, and API contracts"),
    Capability("platform.microservices", "Microservices architecture support", "partial", "generated service boundaries, gateway routes, event routes, cross-service relationship resolver contracts, health probes, and scaling policies"),
    Capability("platform.native", "Python mobile and desktop app scaffolds", "partial", "generated Kivy mobile and BeeWare desktop starters with mobile permission manifests, camera/location plans, push payloads, desktop file actions, offline queues, and cache plans"),
    Capability("platform.jhipster", "JHipster JDL export and interoperability", "partial", "generated JHipster JDL, import contract, gap analysis, adoption plan, and broader-than-JHipster comparison in the low-code matrix"),
    Capability("platform.competitive-benchmark", "JHipster-plus capability benchmark", "partial", "generated overlap and AppGen-only benchmark rows for visual builders, database IDE, native targets, agentic systems, NL evolution, ERP templates, studio operations, and schema import"),
    Capability("platform.chatbots", "Dialogflow and Bot Framework chatbot exports", "partial", "generated chatbot intents, prompts, and provider manifests"),
    Capability("ai.guided-chatbot", "In-app guided chatbot creation flows", "partial", "generated chatbot view, schema prompts, conversation state, and create payloads"),
    Capability("ai.voice-assistant", "Voice assistant and speech interface generation", "partial", "generated speech prompts, utterances, slots, SSML responses, and Alexa/Google/Web Speech exports"),
    Capability("components.templates", "Reusable templates and modules", "partial", "generated component registry, widget descriptors, custom widget registration plans, previews, and layout contracts"),
    Capability("components.lookups", "Relationship and enum lookup fields", "partial", "DSL references and enums generate manifest metadata, SQLAlchemy relationship columns, select widgets, lookup picker contracts, label fields, and UI-ready lookup choices"),
    Capability("components.media", "Image and file upload fields", "partial", "generated media field validation and storage contracts"),
    Capability("components.text-quality", "Textarea spell, grammar, and character counts", "partial", "generated text quality descriptors and validation helpers"),
    Capability("content.document-management", "Document management, versioning, retention, and e-signature contracts", "partial", "generated document libraries, version envelopes, approval workflows, retention policies, e-signature payloads, and audit events"),
    Capability("components.erp-templates", "ERP component templates", "partial", "generated ledgers, accounts, invoicing, AP, AR, inventory, HR, payroll, report templates, recommended ERP stacks, composite ERP DSL, starter generation plans, and legacy migration plans"),
    Capability("components.application-composition", "Application composition marketplace and install plans", "partial", "generated composable blocks for schema, visual builders, workflows, ERP modules, agents, integrations, native targets, dependencies, reviewed install plans, and reusable packages"),
    Capability("platform.extensibility", "Custom code extension hooks", "partial", "generated hook registry and app_custom extension package"),
    Capability("api.rest", "REST API generation", "implemented", "schema-driven ModelRestApi files"),
    Capability("api.graphql", "GraphQL schema generation", "implemented", "schema-driven Graphene schema files"),
    Capability("data.access", "Low-code query, mutation, and validation contracts", "partial", "generated table read/write contracts with filters, sorting, paging, projections, mutation plans, and schema-driven payload validation"),
    Capability("api.documentation", "Automatic API and schema documentation", "partial", "generated README, schema docs, data dictionary, content guide, and Flask-AppBuilder API metadata"),
    Capability("api.openapi", "OpenAPI contract generation", "partial", "generated OpenAPI 3.1 spec, docs/openapi.json, and API docs view"),
    Capability("api.sdks", "Multi-language API SDK exports", "partial", "generated Python, JavaScript, Java, and C# client scaffolds"),
    Capability("data.exchange", "Schema-aware CSV and JSON data exchange", "partial", "generated import templates, row validation, and export helpers"),
    Capability("data.search", "Schema-aware full-text search", "partial", "generated search indexes, provider adapter plans, Elasticsearch mappings, Whoosh schemas, and reviewed reindex runbooks"),
    Capability("data.database-ops", "Database provider and operations contracts", "partial", "generated PostgreSQL, MySQL, SQLite, MongoDB, DynamoDB, Cassandra, Redis, Patroni, PostGraphile, ZomboDB, and Elasticsearch readiness plans"),
    Capability("operations.inventory-traceability", "Barcode, RFID, and inventory traceability operations", "partial", "generated scan targets, barcode labels, RFID payloads, stock movements, cycle counts, and reconciliation helpers"),
    Capability("operations.finance", "Tax, multicurrency, forecasting, and batch finance operations", "partial", "generated tax calculations, exchange-rate conversion plans, budget forecasts, revenue schedules, and batch processing helpers"),
    Capability("operations.manufacturing", "Manufacturing, MRP, capacity planning, and production scheduling", "partial", "generated BOM plans, material requirements, capacity checks, finite schedules, purchase requisitions, and kanban signals"),
    Capability("workflow.automation", "Low-code workflow and decision trees", "partial", "generated transition runtime, role-aware authorization flows, and workflow cockpit"),
    Capability("workflow.statecharts", "FSM and state-chart workflow exports", "partial", "generated Mermaid state diagrams, FSM JSON, SCXML, authorization flows, and workflow graph validation"),
    Capability("logic.business-rules", "Low-code business rules and decisions", "partial", "generated rule validation and decision helpers"),
    Capability("automation.node-red", "Node-RED automation runtime", "partial", "generated Node-RED flow export, webhook contracts, default Docker Compose service, runtime descriptor, and readiness checks"),
    Capability("automation.cep", "Complex event processing and alerting", "partial", "generated event catalog, CEP rule matching, alerting, retry, and dead-letter contracts"),
    Capability("automation.rpa-bpa", "Robotic process automation and business-process analysis", "partial", "generated RPA task plans, credential readiness, BPMN/UML process models, simulations, UiPath/Blue Prism/Automation Anywhere export contracts, bottleneck analysis, process observations, and audit events"),
    Capability("security.rbac", "Role-based access control", "partial", "generated role policy helpers, principal normalization, authorization decisions, audit events, policy matrices, and reviewed RBAC change proposals"),
    Capability("security.session", "Session timeout and runtime hardening", "partial", "generated inactivity timeout and security-header hooks"),
    Capability("security.https", "Automatic HTTPS deployment", "partial", "generated Caddy reverse proxy and TLS readiness checks"),
    Capability("security.rls", "Tenant-aware row-level security", "partial", "DSL-declared RLS targets, generated Python RLS helpers, PostgreSQL policy SQL, tenant session-setting SQL, and reviewable database role/user sync SQL"),
    Capability("security.sso", "SSO and enterprise authentication", "partial", "generated OIDC, SAML, LDAP, Active Directory, AWS Cognito hosted-ui OAuth/token/logout contracts, group-role mapping, and trusted-header registry"),
    Capability("security.compliance", "Compliance-oriented data protection", "partial", "generated audit events, retention policy, redaction, privacy requests, subject exports, erasure plans, and retention-disposition reviews"),
    Capability("reports.analytics", "Reports, dashboards, and analytics", "partial", "generated table, join, and three-way report catalogs plus dashboard contracts, CSV/PDF exports, and email delivery payloads"),
    Capability("reports.usage-analytics", "Application usage analytics", "partial", "generated usage events, adoption, funnels, retention, and real-time activity summaries"),
    Capability("data.visualization", "Charts, graphs, and KPI visualization", "partial", "generated dashboards, chart data contracts, Vega-Lite specs, accessible summaries, and web/mobile/desktop renderer workbenches"),
    Capability("i18n.localization", "Internationalization and localization", "partial", "generated Babel config, translation catalogs, locale negotiation, missing-key reports, and localization cockpit"),
    Capability("a11y.compliance", "Accessibility compliance", "partial", "generated WCAG checklist, skip-link baseline, keyboard navigation plans, ARIA landmark contracts, and accessibility audit plans"),
    Capability("deployment.cloud", "Cloud and on-prem deployment", "partial", "generated Docker, Compose, Kubernetes, Terraform scaffolds, secret plans, smoke checks, deployment runbooks, rollback plans, and cloud readiness matrix"),
    Capability("devops.cicd", "CI/CD and automated review gates", "partial", "generated CI workflow and quality gate"),
    Capability("devops.packaging", "Publishable package and reusable templates", "partial", "generated pyproject, MANIFEST, package contract, FAB extension metadata, and Cookiecutter scaffold"),
    Capability("devops.ide-integration", "Visual Studio Code, JetBrains, and Eclipse workspace integration", "partial", "generated VS Code launch/tasks/extensions, JetBrains IDEA/PyCharm run configs, and Eclipse PyDev project files"),
    Capability("devops.studio", "In-app developer studio", "partial", "generated project tree, searchable command palette, DSL outline/lint/quick-fix/completions, database table proposals, safe SQL workbench plans, generation jobs, diagnostics, code-edit plans, debug sessions, dependency update plans, app cloning, and component sharing"),
    Capability("devops.project-management", "Agile project and DevOps tool integration", "partial", "generated backlog, sprint, release, traceability, and Jira/GitHub/Azure Boards/GitLab export contracts"),
    Capability("support.training", "Generated training, support, tutorials, and sample apps", "partial", "generated support center, knowledge-base topics, onboarding checklists, tutorials, sample DSL apps, search, and support-ticket payloads"),
    Capability("team.collaboration", "Collaboration and version-control workflows", "partial", "generated change proposals, revision IDs, review decisions, conflict reports, merge queues, and resolution plans"),
    Capability("team.version-control", "Low-code version history and rollback", "partial", "generated manifest snapshots, branch plans, diffs, and rollback plans"),
    Capability("team.realtime", "Real-time collaboration and event streams", "partial", "generated event topics, SSE frames, and collaboration message payloads"),
    Capability("quality.diagnostics", "Testing, debugging, and diagnostic tools", "partial", "generated self-tests, debug snapshots, remediation plans, redacted support bundles, API smoke plans, and load-test plans"),
    Capability("quality.api-testing", "Automated API and UI smoke testing plus synthetic monitoring", "partial", "generated API request catalog, response expectations, pytest module rendering, UI smoke plans, Playwright-style module rendering, execution plans, contract coverage, and monitor probes"),
    Capability("quality.code-review", "Automated code review", "partial", "generated schema and artifact review findings"),
    Capability("quality.test-coverage", "Generated test coverage", "partial", "generated per-table pytest coverage matrix for schema, API, UI, reports, security, and data flows"),
    Capability("data.migrations", "Database migrations", "partial", "generated Alembic scaffold"),
    Capability("data.seed", "Database seed data", "partial", "generated relationship-aware deterministic seed script with dependency-ordered insert plans, validation, anonymized fixture exports, and SQL previews"),
    Capability("ops.notifications", "Notifications and alert delivery", "partial", "generated in-app, email, webhook, and push notification payloads"),
    Capability("ops.monitoring", "Monitoring, alerting, and error handling", "partial", "generated monitoring endpoints and error envelopes"),
    Capability("ops.resilience", "Automatic error handling and exception management", "partial", "generated safe error responses, recovery actions, retry plans, circuit breakers, and incident reports"),
    Capability("ops.performance", "Performance budgets and scaling plans", "partial", "generated SLO budgets, pagination/cache plans, and autoscale recommendations"),
    Capability("ops.configuration", "Runtime configuration management", "partial", "generated config.py setup editor, readiness checks, checklist, and .env export"),
    Capability("ops.lifecycle", "Environment, release, feedback, and lifecycle management", "partial", "generated environment readiness, custom-domain plans, release gates, maintenance windows, feedback, and issue reports"),
    Capability("ops.backup", "Backup and disaster recovery", "partial", "generated JSON backup exports, integrity manifests, autobackup schedules, retention plans, recovery runbooks, and restore helpers"),
    Capability("scale.multi-tenancy", "Multi-tenancy and scaling", "partial", "generated tenant-scope registry and filter helpers"),
    Capability("integration.enterprise", "Enterprise service integrations", "partial", "generated REST, webhook, Salesforce, SAP, Entando, Invenio, payment gateway, SMS gateway, transactional email registry, signed webhook plans, idempotency keys, outbox envelopes, and delivery audit events"),
    Capability("integration.productivity", "Microsoft 365 and Google Workspace productivity integrations", "partial", "generated document, spreadsheet, calendar, and task-sync payload contracts"),
    Capability("integration.emerging", "IoT and blockchain integration contracts", "partial", "generated device telemetry, edge sync, command, and blockchain audit-anchor contracts"),
    Capability("ai.assistance", "AI and machine-learning assistance", "partial", "generated assistant context, recommendations, prediction hooks, and review tasks"),
    Capability("ai.intelligence", "AI analytics, computer vision, NLP, recommendation, and UX optimization", "partial", "generated feature preprocessing, anomaly detection, image/video analysis plans, OCR/classification/object-detection contracts, NLP helpers, A/B testing, and predictive maintenance"),
    Capability("ai.agentic-systems", "Agentic systems with local and API-key LLM providers", "partial", "DSL llm/agent blocks, generated provider readiness, and agent execution plans"),
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
