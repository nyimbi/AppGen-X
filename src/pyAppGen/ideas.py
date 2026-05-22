"""Package-level release evidence for docs/ideas.md."""

from __future__ import annotations

from pathlib import Path

from .capabilities import DEFAULT_CAPABILITIES


IDEAS_DOCUMENT = "docs/ideas.md"

IDEAS_REQUIREMENTS = (
    {
        "section": "ecosystem",
        "items": (
            {
                "id": "full_stack_fastapi_reference",
                "label": "Full-stack FastAPI/PostgreSQL reference",
                "capabilities": ("api.rest", "api.openapi", "deployment.cloud"),
            },
            {
                "id": "zombodb",
                "label": "ZomboDB/PostgreSQL search",
                "capabilities": ("data.database-ops", "data.search"),
            },
            {
                "id": "postgraphile",
                "label": "PostGraphile-style GraphQL/database integration",
                "capabilities": ("api.graphql", "data.database-ops"),
            },
            {
                "id": "patroni",
                "label": "Patroni and database resilience",
                "capabilities": ("data.database-ops", "ops.resilience"),
            },
            {
                "id": "jhipster_dockerization",
                "label": "JHipster and Dockerization",
                "capabilities": ("platform.jhipster", "deployment.cloud"),
            },
            {
                "id": "entando",
                "label": "Entando integration handoff",
                "capabilities": ("integration.enterprise", "components.application-composition"),
            },
            {
                "id": "node_red_default",
                "label": "Node-RED as a default automation runtime",
                "capabilities": ("automation.node-red",),
            },
            {
                "id": "invenio",
                "label": "Invenio repository deposit",
                "capabilities": ("integration.enterprise", "components.application-composition"),
            },
            {
                "id": "automatic_https",
                "label": "Automatic HTTPS",
                "capabilities": ("security.https", "deployment.cloud"),
            },
            {
                "id": "config_flags_editor",
                "label": "FAB API flags and config.py editor view",
                "capabilities": ("ops.configuration",),
            },
        ),
    },
    {
        "section": "other_stuff",
        "items": (
            {
                "id": "view_generation_refactor",
                "label": "Refactor view generation into a class",
                "capabilities": ("codegen.fab", "ui.view-composition"),
            },
            {
                "id": "import_rationalization",
                "label": "Rationalize generated imports",
                "capabilities": ("quality.code-review", "devops.packaging"),
            },
            {
                "id": "master_detail_views",
                "label": "Generate MasterDetail Views",
                "capabilities": ("ui.view-composition",),
            },
            {
                "id": "chartviews",
                "label": "Generate ChartViews",
                "capabilities": ("ui.view-composition", "data.visualization"),
            },
            {
                "id": "reports",
                "label": "Generate Reports",
                "capabilities": ("reports.analytics",),
            },
            {
                "id": "rest_api",
                "label": "REST API",
                "capabilities": ("api.rest",),
            },
            {
                "id": "graphql_interface",
                "label": "GraphQL Interface",
                "capabilities": ("api.graphql",),
            },
            {
                "id": "dbml_sql_ponyorm_generation",
                "label": "Generate code from DBML, SQL, and PonyORM scripts",
                "capabilities": ("schema.import",),
            },
            {
                "id": "existing_database_generation",
                "label": "Generate code from existing database",
                "capabilities": ("schema.import", "data.database-ops"),
            },
            {
                "id": "frontend_frameworks",
                "label": "React, Vue, Angular, and Express front ends",
                "capabilities": ("platform.frontends",),
            },
            {
                "id": "aws_cognito",
                "label": "AWS Cognito Integration",
                "capabilities": ("security.sso",),
            },
            {
                "id": "dockerfile",
                "label": "Dockerfile for deployment",
                "capabilities": ("deployment.cloud",),
            },
            {
                "id": "elasticsearch",
                "label": "Elasticsearch search",
                "capabilities": ("data.search", "data.database-ops"),
            },
            {
                "id": "whoosh",
                "label": "Whoosh search",
                "capabilities": ("data.search",),
            },
            {
                "id": "idea_editor_config",
                "label": "IDE editor file for config editor view",
                "capabilities": ("devops.ide-integration", "ops.configuration"),
            },
            {
                "id": "move_files",
                "label": "Move generated files automatically to the right place",
                "capabilities": ("devops.packaging",),
            },
            {
                "id": "fsm_generator",
                "label": "FSM generator page",
                "capabilities": ("workflow.statecharts",),
            },
            {
                "id": "textarea_grammar",
                "label": "Spell and grammar check all text areas",
                "capabilities": ("components.text-quality",),
            },
            {
                "id": "textarea_counts",
                "label": "Character counters for text areas",
                "capabilities": ("components.text-quality",),
            },
            {
                "id": "lookups",
                "label": "Lookup fields",
                "capabilities": ("components.lookups",),
            },
            {
                "id": "image_upload_fields",
                "label": "Image and upload fields",
                "capabilities": ("components.media",),
            },
            {
                "id": "publishable_package",
                "label": "Make AppGen publishable",
                "capabilities": ("devops.packaging",),
            },
            {
                "id": "fab_extension_cookiecutter",
                "label": "FAB extension and Cookiecutter template",
                "capabilities": ("devops.packaging", "platform.extensibility"),
            },
            {
                "id": "automatic_test_coverage",
                "label": "Automatically generate test coverage",
                "capabilities": ("quality.test-coverage",),
            },
        ),
    },
    {
        "section": "big_things",
        "items": (
            {"id": "seed_scripts", "label": "Database seeding scripts", "capabilities": ("data.seed",)},
            {"id": "jhipster_code", "label": "JHipster code generation", "capabilities": ("platform.jhipster",)},
            {
                "id": "field_type_components",
                "label": "Components for field types and datetime calendars",
                "capabilities": ("components.templates", "components.lookups", "components.media"),
            },
            {"id": "mobile_app", "label": "Mobile app generation", "capabilities": ("platform.native", "platform.targets")},
            {"id": "desktop_app", "label": "Desktop app generation", "capabilities": ("platform.native", "platform.targets")},
            {"id": "relationship_reports", "label": "Table, join, and 3-way reports", "capabilities": ("reports.analytics",)},
            {"id": "aws_gcp_deploy", "label": "Deploy to AWS and GCP", "capabilities": ("deployment.cloud",)},
            {"id": "database_design_tool", "label": "Database design tool", "capabilities": ("devops.studio", "ui.visual-modeling")},
            {"id": "schema_documentation", "label": "Database structure and content documentation", "capabilities": ("api.documentation",)},
            {"id": "erp_data_model_library", "label": "ERP data model library", "capabilities": ("components.erp-templates",)},
        ),
    },
    {
        "section": "docker_deployment",
        "items": (
            {"id": "postgres_deploy", "label": "Deploy and create PostgreSQL database", "capabilities": ("deployment.cloud", "data.database-ops")},
            {"id": "kubernetes", "label": "Deploy to Kubernetes", "capabilities": ("deployment.cloud",)},
            {"id": "deploy_elasticsearch", "label": "Deploy Elasticsearch", "capabilities": ("deployment.cloud", "data.search")},
            {"id": "terraform_clouds", "label": "Terraform for GCP, AWS, and Azure", "capabilities": ("deployment.cloud",)},
            {"id": "postgres_mysql", "label": "PostgreSQL and MySQL databases", "capabilities": ("data.database-ops",)},
        ),
    },
    {
        "section": "dbscript_ideas",
        "items": (
            {"id": "field_groups", "label": "Field groups for large tables", "capabilities": ("dsl.language-design", "schema.import")},
            {"id": "field_group_mixins", "label": "Field groups as mixins", "capabilities": ("dsl.language-design", "schema.import")},
            {"id": "array_types", "label": "Array types", "capabilities": ("dsl.language-design", "schema.import")},
            {"id": "row_level_security", "label": "Row Level Security", "capabilities": ("security.rls", "dsl.language-design")},
            {"id": "derived_hidden_fields", "label": "Derived and hidden fields", "capabilities": ("dsl.language-design", "schema.import")},
        ),
    },
    {
        "section": "extended_bullets",
        "items": (
            {"id": "erdiagram_language", "label": "ER diagram language compatibility", "capabilities": ("ui.visual-modeling", "dsl.language-design")},
            {"id": "erdiagram_editor", "label": "erDiagram editor", "capabilities": ("ui.visual-modeling", "devops.studio")},
            {"id": "field_prompt_chatbot", "label": "Chatbot that asks for each field in a view", "capabilities": ("ai.guided-chatbot", "platform.chatbots")},
            {"id": "statecharts_authorization", "label": "State charts and authorization flows", "capabilities": ("workflow.statecharts", "security.rbac")},
            {"id": "postgres_rls_user_sync", "label": "RLS user sync with PostgreSQL users", "capabilities": ("security.rls", "data.database-ops")},
            {"id": "auto_logout", "label": "Auto logout after inactivity", "capabilities": ("security.session",)},
            {"id": "advanced_reports", "label": "PDF/email graphing and reporting", "capabilities": ("reports.analytics", "data.visualization")},
            {"id": "config_setup_screen", "label": "Configuration and setup screen", "capabilities": ("ops.configuration",)},
            {"id": "tabbed_permissions", "label": "Tabbed views with permissions per tab", "capabilities": ("ui.tabbed-views", "security.rbac")},
            {"id": "autobackup", "label": "Autobackup", "capabilities": ("ops.backup",)},
        ),
    },
)


def _capability_index() -> dict[str, dict]:
    return {item.key: item.__dict__ for item in DEFAULT_CAPABILITIES}


def ideas_document_check(root: Path | str | None = None) -> dict:
    """Return evidence that the original ideas roadmap document is present."""
    base = Path(root) if root is not None else Path(__file__).resolve().parents[2]
    path = base / IDEAS_DOCUMENT
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    required_phrases = (
        "JHipster",
        "Generate MasterDetail Views",
        "Generate code from dbml, sql, ponyORM scripts",
        "Generate a mobile app",
        "Create a database design tool",
        "Add Field Groups",
        "Autobackup",
    )
    missing = tuple(phrase for phrase in required_phrases if phrase not in text)
    return {
        "format": "appgen.ideas-document-check.v1",
        "path": IDEAS_DOCUMENT,
        "exists": path.exists(),
        "required_phrases": required_phrases,
        "missing": missing,
        "ok": path.exists() and not missing,
    }


def ideas_requirement_rows() -> tuple[dict, ...]:
    """Return each docs/ideas.md item mapped to capability evidence."""
    capabilities = _capability_index()
    rows = []
    for section in IDEAS_REQUIREMENTS:
        for item in section["items"]:
            required = tuple(item["capabilities"])
            covered = tuple(
                key
                for key in required
                if capabilities.get(key, {}).get("status") == "implemented"
            )
            missing = tuple(key for key in required if key not in covered)
            rows.append(
                {
                    "section": section["section"],
                    "id": item["id"],
                    "label": item["label"],
                    "required_capabilities": required,
                    "covered_capabilities": covered,
                    "missing_capabilities": missing,
                    "evidence": tuple(capabilities[key]["evidence"] for key in covered),
                    "ok": not missing,
                }
            )
    return tuple(rows)


def ideas_section_summary(rows: tuple[dict, ...] | None = None) -> tuple[dict, ...]:
    """Return section-level coverage summaries for docs/ideas.md."""
    items = rows or ideas_requirement_rows()
    sections = tuple(section["section"] for section in IDEAS_REQUIREMENTS)
    summaries = []
    for section in sections:
        section_rows = tuple(row for row in items if row["section"] == section)
        summaries.append(
            {
                "section": section,
                "total": len(section_rows),
                "covered": sum(1 for row in section_rows if row["ok"]),
                "missing": tuple(row["id"] for row in section_rows if not row["ok"]),
                "ok": bool(section_rows) and all(row["ok"] for row in section_rows),
            }
        )
    return tuple(summaries)


def ideas_release_audit(root: Path | str | None = None) -> dict:
    """Return package-level proof for the original docs/ideas.md roadmap."""
    document = ideas_document_check(root)
    rows = ideas_requirement_rows()
    sections = ideas_section_summary(rows)
    gates = (
        {
            "id": "document_contract",
            "ok": document["ok"],
            "document": document,
        },
        {
            "id": "roadmap_item_coverage",
            "ok": len(rows) == 64 and all(row["ok"] for row in rows),
            "total": len(rows),
            "items": rows,
        },
        {
            "id": "section_coverage",
            "ok": len(sections) == len(IDEAS_REQUIREMENTS) and all(section["ok"] for section in sections),
            "sections": sections,
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.ideas-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "document": document,
        "items": rows,
        "sections": sections,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-ideas-roadmap-readiness-unless-ok-is-true",
    }
