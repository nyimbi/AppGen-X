"""Package-level roadmap release audit helpers.

Generated apps already expose roadmap evidence in ``low_code_features.py``.
This module gives the AppGen CLI the same kind of top-level proof before an app
has been generated.
"""

from __future__ import annotations

from pathlib import Path

from .capabilities import DEFAULT_CAPABILITIES


ROADMAP_DOCUMENTS = (
    {
        "path": "docs/ideas.md",
        "required_phrases": (
            "JHipster",
            "Generate a mobile app",
            "Generate a desktop app",
            "database design tool",
            "Data Model Library for an ERP",
        ),
    },
    {
        "path": "docs/base_features.md",
        "required_phrases": (
            "JHipster superset",
            "Delphi-style form design",
            "ERP templates",
            "agentic-system design",
            "natural-language evolution",
            "multi-platform generation",
        ),
    },
    {
        "path": "docs/Lo-code features.md",
        "required_phrases": (
            "Visual, drag-and-drop interface",
            "Cross-platform development support",
            "Pre-built templates",
            "custom widgets/components",
            "CRM and ERP systems",
        ),
    },
)

ROADMAP_CAPABILITY_REQUIREMENTS = (
    {
        "id": "schema-sources",
        "description": (
            "Generate applications from DBML, SQL, PonyORM, DSL, and existing "
            "databases."
        ),
        "capabilities": ("schema.import",),
    },
    {
        "id": "antlr-dsl",
        "description": (
            "Keep an intuitive ANTLR-backed DSL with linter, formatter, and "
            "release gates."
        ),
        "capabilities": ("dsl.language-design",),
    },
    {
        "id": "delphi-form-designer",
        "description": "Allow users to drop components onto forms in a Delphi-style designer.",
        "capabilities": ("ui.form-designer", "ui.visual-modeling"),
    },
    {
        "id": "multi-platform-generation",
        "description": "Generate web, PWA, mobile, desktop, and chatbot targets.",
        "capabilities": ("platform.targets", "platform.native"),
    },
    {
        "id": "agentic-systems",
        "description": "Design agentic systems connected to local and API-key LLM providers.",
        "capabilities": ("ai.agentic-systems",),
    },
    {
        "id": "natural-language-evolution",
        "description": (
            "Use natural language to evolve tables, forms, workflows, chatbots, "
            "agents, and ERP modules."
        ),
        "capabilities": ("ui.nl-evolution",),
    },
    {
        "id": "erp-templates",
        "description": (
            "Provide ERP modules for ledgers, accounts, invoicing, AP, AR, "
            "inventory, HR, and reports."
        ),
        "capabilities": ("components.erp-templates", "operations.finance"),
    },
    {
        "id": "robust-ide",
        "description": (
            "Provide an IDE for app generation, DSL authoring, database design, "
            "diagnostics, and management."
        ),
        "capabilities": ("devops.studio", "devops.ide-integration"),
    },
    {
        "id": "jhipster-plus",
        "description": "Preserve JHipster overlap while proving AppGen-only superiority areas.",
        "capabilities": (
            "platform.jhipster",
            "platform.jhipster-superiority",
            "platform.competitive-benchmark",
        ),
    },
    {
        "id": "secure-reliable-apps",
        "description": (
            "Generate secure, reliable, documented, testable, and "
            "runtime-assured applications."
        ),
        "capabilities": (
            "security.rbac",
            "security.session",
            "security.https",
            "ops.assurance",
            "quality.test-coverage",
        ),
    },
)

JHIPSTER_BASELINE_REQUIREMENTS = (
    {
        "id": "domain-modeling",
        "description": "Schema/model intake and generated application code.",
        "capabilities": ("schema.import", "codegen.fab", "api.rest", "api.graphql"),
    },
    {
        "id": "frontend-and-pwa",
        "description": "Modern front-end and PWA scaffolding.",
        "capabilities": ("platform.frontends", "ui.pwa", "ui.responsive"),
    },
    {
        "id": "security-and-identity",
        "description": "RBAC, session hardening, HTTPS, and enterprise identity.",
        "capabilities": (
            "security.rbac",
            "security.session",
            "security.https",
            "security.sso",
        ),
    },
    {
        "id": "deployment-and-ci",
        "description": "Cloud deployment, packaging, CI/CD, and generated tests.",
        "capabilities": (
            "deployment.cloud",
            "devops.cicd",
            "devops.packaging",
            "quality.test-coverage",
        ),
    },
)

APPGEN_ADVANTAGE_REQUIREMENTS = (
    {
        "id": "visual-low-code-studio",
        "description": "Integrated Studio, visual modeling, and database design.",
        "capabilities": ("devops.studio", "ui.visual-modeling", "devops.ide-integration"),
    },
    {
        "id": "delphi-form-design",
        "description": "Delphi-style drop-target form designer and component palette.",
        "capabilities": ("ui.form-designer", "components.templates"),
    },
    {
        "id": "natural-language-evolution",
        "description": "Natural-language changes for tables, fields, forms, agents, and ERP.",
        "capabilities": ("ui.nl-evolution",),
    },
    {
        "id": "agentic-systems",
        "description": "Local and API-key LLM providers with agent/tool policy evidence.",
        "capabilities": ("ai.agentic-systems",),
    },
    {
        "id": "native-targets",
        "description": "Python mobile and desktop target scaffolds.",
        "capabilities": ("platform.native", "platform.targets"),
    },
    {
        "id": "erp-template-library",
        "description": "ERP templates for finance, inventory, HR, reporting, and operations.",
        "capabilities": ("components.erp-templates", "operations.finance"),
    },
    {
        "id": "runtime-assurance",
        "description": "Runtime assurance, diagnostics, performance, backup, and resilience.",
        "capabilities": (
            "ops.assurance",
            "quality.diagnostics",
            "ops.performance",
            "ops.backup",
            "ops.resilience",
        ),
    },
    {
        "id": "enterprise-composition",
        "description": "Application composition, enterprise integrations, and reusable packages.",
        "capabilities": (
            "components.application-composition",
            "integration.enterprise",
            "platform.extensibility",
        ),
    },
)

GENERATED_APP_EXCELLENCE_REQUIREMENTS = (
    {
        "id": "beautiful",
        "description": (
            "Generated apps expose polished visual design, responsive layouts, "
            "and visual QA evidence."
        ),
        "capabilities": ("ui.branding", "ui.responsive", "a11y.compliance"),
    },
    {
        "id": "sophisticated",
        "description": (
            "Generated apps include advanced UI composition, analytics, "
            "workflows, and integrations."
        ),
        "capabilities": (
            "ui.view-composition",
            "reports.analytics",
            "workflow.automation",
            "integration.enterprise",
        ),
    },
    {
        "id": "secure",
        "description": (
            "Generated apps include RBAC, sessions, HTTPS, SSO, compliance, "
            "and RLS evidence."
        ),
        "capabilities": (
            "security.rbac",
            "security.session",
            "security.https",
            "security.sso",
            "security.compliance",
            "security.rls",
        ),
    },
    {
        "id": "reliable",
        "description": (
            "Generated apps include monitoring, backup, CI, tests, and runtime "
            "assurance."
        ),
        "capabilities": (
            "ops.monitoring",
            "ops.backup",
            "devops.cicd",
            "quality.test-coverage",
            "ops.assurance",
        ),
    },
    {
        "id": "robust",
        "description": (
            "Generated apps include resilience, diagnostics, performance "
            "budgets, and database operations."
        ),
        "capabilities": (
            "ops.resilience",
            "quality.diagnostics",
            "ops.performance",
            "data.database-ops",
        ),
    },
    {
        "id": "functional",
        "description": (
            "Generated apps include data models, APIs, search, reports, forms, "
            "and data exchange."
        ),
        "capabilities": (
            "codegen.fab",
            "api.rest",
            "api.graphql",
            "data.search",
            "reports.analytics",
            "data.exchange",
        ),
    },
    {
        "id": "highly-capable",
        "description": (
            "Generated apps include native targets, ERP templates, agentic "
            "systems, NL evolution, and composition."
        ),
        "capabilities": (
            "platform.native",
            "components.erp-templates",
            "ai.agentic-systems",
            "ui.nl-evolution",
            "components.application-composition",
        ),
    },
)


def _read_document(root: Path, relative_path: str) -> str:
    path = root / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def roadmap_document_checks(root: Path | str | None = None) -> tuple[dict, ...]:
    """Return checks that prove the current roadmap documents are present."""
    base = Path(root) if root is not None else Path.cwd()
    checks = []
    for document in ROADMAP_DOCUMENTS:
        text = _read_document(base, document["path"])
        missing_phrases = tuple(
            phrase
            for phrase in document["required_phrases"]
            if phrase.lower() not in text.lower()
        )
        checks.append(
            {
                "path": document["path"],
                "exists": bool(text),
                "required_phrases": document["required_phrases"],
                "missing_phrases": missing_phrases,
                "ok": bool(text) and not missing_phrases,
            }
        )
    return tuple(checks)


def roadmap_capability_checks() -> tuple[dict, ...]:
    """Return checks binding roadmap requirements to implemented capabilities."""
    capability_status = {
        capability.key: capability.status for capability in DEFAULT_CAPABILITIES
    }
    checks = []
    for requirement in ROADMAP_CAPABILITY_REQUIREMENTS:
        missing = tuple(
            key
            for key in requirement["capabilities"]
            if capability_status.get(key) != "implemented"
        )
        checks.append(
            {
                "id": requirement["id"],
                "description": requirement["description"],
                "capabilities": requirement["capabilities"],
                "missing_capabilities": missing,
                "ok": not missing,
            }
        )
    return tuple(checks)


def _capability_group_checks(requirements: tuple[dict, ...]) -> tuple[dict, ...]:
    capability_status = {
        capability.key: capability.status for capability in DEFAULT_CAPABILITIES
    }
    return tuple(
        {
            "id": requirement["id"],
            "description": requirement["description"],
            "capabilities": requirement["capabilities"],
            "missing_capabilities": tuple(
                key
                for key in requirement["capabilities"]
                if capability_status.get(key) != "implemented"
            ),
            "ok": all(
                capability_status.get(key) == "implemented"
                for key in requirement["capabilities"]
            ),
        }
        for requirement in requirements
    )


def jhipster_superiority_audit() -> dict:
    """Return package-level proof that AppGen preserves and exceeds JHipster."""
    baseline = _capability_group_checks(JHIPSTER_BASELINE_REQUIREMENTS)
    advantages = _capability_group_checks(APPGEN_ADVANTAGE_REQUIREMENTS)
    minimum_advantages = 8
    gates = (
        {
            "id": "jhipster_baseline_preserved",
            "ok": all(item["ok"] for item in baseline),
            "requirements": baseline,
        },
        {
            "id": "appgen_only_advantages",
            "ok": sum(1 for item in advantages if item["ok"]) >= minimum_advantages,
            "minimum": minimum_advantages,
            "requirements": advantages,
        },
        {
            "id": "explicit_superiority_capabilities",
            "ok": all(
                item["ok"]
                for item in _capability_group_checks(
                    (
                        {
                            "id": "competitive-benchmark",
                            "description": "Generated competitive benchmark and superiority gates.",
                            "capabilities": (
                                "platform.jhipster",
                                "platform.jhipster-superiority",
                                "platform.competitive-benchmark",
                            ),
                        },
                    )
                )
            ),
            "capabilities": (
                "platform.jhipster",
                "platform.jhipster-superiority",
                "platform.competitive-benchmark",
            ),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.jhipster-superiority-audit.v1",
        "scope": "package",
        "position": "appgen-is-more-capable-than-jhipster",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "baseline": baseline,
        "advantages": advantages,
        "minimum_advantages": minimum_advantages,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-jhipster-superiority-unless-ok-is-true",
    }


def generated_app_excellence_audit() -> dict:
    """Return package-level proof for generated app quality claims."""
    categories = _capability_group_checks(GENERATED_APP_EXCELLENCE_REQUIREMENTS)
    gates = (
        {
            "id": "objective_quality_categories",
            "ok": all(category["ok"] for category in categories),
            "categories": categories,
        },
        {
            "id": "runtime_assurance_bound",
            "ok": any(
                category["id"] == "reliable"
                and "ops.assurance" in category["capabilities"]
                and category["ok"]
                for category in categories
            ),
            "required_capability": "ops.assurance",
        },
        {
            "id": "visual_quality_bound",
            "ok": any(
                category["id"] == "beautiful"
                and "ui.branding" in category["capabilities"]
                and category["ok"]
                for category in categories
            ),
            "required_capability": "ui.branding",
        },
        {
            "id": "advanced_capability_bound",
            "ok": any(
                category["id"] == "highly-capable"
                and "ai.agentic-systems" in category["capabilities"]
                and "components.erp-templates" in category["capabilities"]
                and category["ok"]
                for category in categories
            ),
            "required_capabilities": (
                "ai.agentic-systems",
                "components.erp-templates",
            ),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.generated-app-excellence-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "categories": categories,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-generated-app-excellence-unless-ok-is-true",
    }


def roadmap_release_audit(root: Path | str | None = None) -> dict:
    """Return package-level proof that roadmap docs map to implemented features."""
    documents = roadmap_document_checks(root)
    capability_checks = roadmap_capability_checks()
    gates = (
        {
            "id": "roadmap_documents",
            "ok": all(document["ok"] for document in documents),
            "documents": documents,
        },
        {
            "id": "capability_requirements",
            "ok": all(check["ok"] for check in capability_checks),
            "requirements": capability_checks,
        },
        {
            "id": "low_code_features_included",
            "ok": any(
                document["path"] == "docs/Lo-code features.md" and document["ok"]
                for document in documents
            ),
            "document": "docs/Lo-code features.md",
        },
        {
            "id": "jhipster_superset_claim_guarded",
            "ok": any(check["id"] == "jhipster-plus" and check["ok"] for check in capability_checks),
            "required_capabilities": (
                "platform.jhipster",
                "platform.jhipster-superiority",
                "platform.competitive-benchmark",
            ),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.roadmap-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "documents": documents,
        "requirements": capability_checks,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
    }
