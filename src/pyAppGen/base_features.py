"""Package-level release evidence for docs/base_features.md."""

from __future__ import annotations

from pathlib import Path

from .capabilities import DEFAULT_CAPABILITIES


BASE_FEATURE_DOCUMENT = "docs/base_features.md"

BASE_FEATURE_REQUIREMENTS = (
    {
        "id": "data_modeling",
        "label": "Data Modeling",
        "capabilities": ("schema.import", "dsl.language-design", "data.migrations"),
    },
    {
        "id": "user_interface_design",
        "label": "User Interface Design",
        "capabilities": ("ui.form-designer", "ui.visual-modeling", "ui.layout"),
    },
    {
        "id": "data_access",
        "label": "Data Access",
        "capabilities": ("data.access", "api.rest", "api.graphql"),
    },
    {
        "id": "security",
        "label": "Security",
        "capabilities": ("security.rbac", "security.sso", "security.session"),
    },
    {
        "id": "workflow",
        "label": "Workflow",
        "capabilities": ("workflow.automation", "workflow.statecharts"),
    },
    {
        "id": "wizards",
        "label": "Wizards",
        "capabilities": ("ui.wizards",),
    },
    {
        "id": "customization",
        "label": "Customization",
        "capabilities": ("logic.business-rules", "ui.nl-evolution"),
    },
    {
        "id": "reporting",
        "label": "Reporting",
        "capabilities": ("reports.analytics", "reports.usage-analytics"),
    },
    {
        "id": "integration",
        "label": "Integration",
        "capabilities": ("integration.enterprise", "integration.productivity"),
    },
    {
        "id": "data_visualization",
        "label": "Data Visualization",
        "capabilities": ("data.visualization", "ui.view-composition"),
    },
    {
        "id": "automation",
        "label": "Automation",
        "capabilities": ("workflow.automation", "automation.node-red", "automation.cep"),
    },
    {
        "id": "extensibility",
        "label": "Extensibility",
        "capabilities": ("platform.extensibility", "components.application-composition"),
    },
    {
        "id": "debugging",
        "label": "Debugging",
        "capabilities": ("quality.diagnostics", "devops.studio"),
    },
    {
        "id": "testing",
        "label": "Testing",
        "capabilities": ("quality.test-coverage", "quality.api-testing", "devops.cicd"),
    },
    {
        "id": "deployment",
        "label": "Deployment",
        "capabilities": ("deployment.cloud", "devops.packaging", "devops.cicd"),
    },
    {
        "id": "runtime_assurance",
        "label": "Runtime assurance",
        "capabilities": (
            "ops.assurance",
            "ops.monitoring",
            "ops.resilience",
            "ops.backup",
            "ops.performance",
        ),
    },
)

PLATFORM_REQUIREMENTS = (
    {
        "id": "web_desktop_mobile_ui",
        "label": "User interfaces for web, desktop, and mobile applications",
        "capabilities": ("platform.targets", "platform.native", "ui.responsive"),
    },
    {
        "id": "cross_platform_business_logic",
        "label": "Data models and business logic for web, desktop, and mobile",
        "capabilities": ("schema.import", "logic.business-rules", "platform.native"),
    },
    {
        "id": "external_services",
        "label": "Integration with external services and APIs",
        "capabilities": ("integration.enterprise", "api.rest", "api.openapi"),
    },
    {
        "id": "multi_target_codegen",
        "label": "Code generation for different platform targets and technologies",
        "capabilities": ("platform.targets", "platform.frontends", "platform.native"),
    },
    {
        "id": "chatbot_generation",
        "label": "Chatbot platform generation",
        "capabilities": ("platform.chatbots", "ai.guided-chatbot"),
    },
    {
        "id": "mobile_capabilities",
        "label": "Push notifications, location services, and camera access",
        "capabilities": ("platform.native", "ops.notifications"),
    },
    {
        "id": "offline_responsive",
        "label": "Responsive design and offline mode",
        "capabilities": ("ui.responsive", "ui.pwa", "platform.targets"),
    },
    {
        "id": "custom_components",
        "label": "Custom components and widgets",
        "capabilities": ("components.templates", "platform.extensibility"),
    },
    {
        "id": "version_control_collaboration",
        "label": "Version control and collaboration",
        "capabilities": ("team.version-control", "team.collaboration", "team.realtime"),
    },
    {
        "id": "testing_debugging",
        "label": "Testing and debugging",
        "capabilities": ("quality.test-coverage", "quality.diagnostics"),
    },
    {
        "id": "composition_packages",
        "label": "Application composition packages",
        "capabilities": (
            "components.application-composition",
            "integration.enterprise",
            "platform.extensibility",
        ),
    },
)

SUPERSET_REQUIREMENTS = (
    "platform.jhipster",
    "platform.jhipster-superiority",
    "platform.competitive-benchmark",
    "devops.studio",
    "ui.form-designer",
    "components.erp-templates",
    "ai.agentic-systems",
    "ui.nl-evolution",
    "platform.targets",
    "dsl.language-design",
    "team.version-control",
    "ops.assurance",
)


def _capability_index() -> dict[str, dict]:
    return {item.key: item.__dict__ for item in DEFAULT_CAPABILITIES}


def _coverage_rows(requirements: tuple[dict, ...]) -> tuple[dict, ...]:
    capabilities = _capability_index()
    rows = []
    for requirement in requirements:
        required = tuple(requirement["capabilities"])
        covered = tuple(key for key in required if capabilities.get(key, {}).get("status") == "implemented")
        missing = tuple(key for key in required if key not in covered)
        rows.append(
            {
                "id": requirement["id"],
                "label": requirement["label"],
                "required_capabilities": required,
                "covered_capabilities": covered,
                "missing_capabilities": missing,
                "evidence": tuple(capabilities[key]["evidence"] for key in covered),
                "ok": not missing,
            }
        )
    return tuple(rows)


def base_feature_document_check(root: Path | str | None = None) -> dict:
    """Return evidence that the canonical base feature document is present."""
    base = Path(root) if root is not None else Path(__file__).resolve().parents[2]
    path = base / BASE_FEATURE_DOCUMENT
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    required_phrases = (
        "1. Data Modeling",
        "16. Runtime assurance",
        "JHipster superset",
        "The DSL should support web, desktop, and mobile applications",
        "Application composition packages",
    )
    missing = tuple(phrase for phrase in required_phrases if phrase not in text)
    return {
        "format": "appgen.base-feature-document-check.v1",
        "path": BASE_FEATURE_DOCUMENT,
        "exists": path.exists(),
        "required_phrases": required_phrases,
        "missing": missing,
        "ok": path.exists() and not missing,
    }


def base_feature_release_audit(root: Path | str | None = None) -> dict:
    """Return package-level proof for every docs/base_features.md requirement."""
    document = base_feature_document_check(root)
    numbered = _coverage_rows(BASE_FEATURE_REQUIREMENTS)
    platform = _coverage_rows(PLATFORM_REQUIREMENTS)
    capabilities = _capability_index()
    superset_missing = tuple(
        key
        for key in SUPERSET_REQUIREMENTS
        if capabilities.get(key, {}).get("status") != "implemented"
    )
    gates = (
        {
            "id": "document_contract",
            "ok": document["ok"],
            "document": document,
        },
        {
            "id": "numbered_base_features",
            "ok": len(numbered) == 16 and all(row["ok"] for row in numbered),
            "requirements": numbered,
        },
        {
            "id": "platform_bullets",
            "ok": len(platform) == 11 and all(row["ok"] for row in platform),
            "requirements": platform,
        },
        {
            "id": "jhipster_superset_clause",
            "ok": not superset_missing,
            "required_capabilities": SUPERSET_REQUIREMENTS,
            "missing_capabilities": superset_missing,
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.base-feature-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "document": document,
        "numbered_features": numbered,
        "platform_requirements": platform,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-base-feature-readiness-unless-ok-is-true",
    }
