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

BASE_FEATURE_SAMPLE_DSL = """
app BaseFeatureAudit { theme: sage; targets: web, pwa, mobile, desktop, chatbot }

table Customer {
  id: int pk
  name: string required search
  email: email search
}

table SupportTicket {
  id: int pk
  customer_id: int required -> Customer.id [many-to-one]
  title: string required search
  status: string required
  priority: string required
}

flow TicketLifecycle {
  open -> assigned
  assigned -> resolved
}

role SupportAgent {
  SupportTicket: read, update;
}

view TicketForm for SupportTicket {
  Main: customer_id, title, status, priority
  @ title TextBox 0 0 6 1
  @ status Select 0 1 4 1
  @ priority Select 4 1 4 1
}
"""

BASE_FEATURE_SMOKE_REQUIRED_ARTIFACTS = (
    "app/models.py",
    "app/views.py",
    "app/api.py",
    "app/gql.py",
    "app/data_access.py",
    "app/templates/appgen_data_access.html",
    "app/security.py",
    "app/workflow.py",
    "app/wizards.py",
    "app/reports.py",
    "app/integrations.py",
    "app/dashboards.py",
    "app/events.py",
    "app/extensions.py",
    "app/diagnostics.py",
    "app/api_testing.py",
    "app/runtime_assurance.py",
    "app/platforms.py",
    "app/low_code_features.py",
    "app/templates/appgen_low_code_features.html",
    "native/mobile/app.py",
    "native/desktop/app.py",
    "Dockerfile",
    ".github/workflows/appgen-ci.yml",
    "scripts/appgen_quality.py",
    "app/appgen.json",
)

BASE_FEATURE_SMOKE_PYTHON_ARTIFACTS = (
    "app/models.py",
    "app/views.py",
    "app/api.py",
    "app/gql.py",
    "app/data_access.py",
    "app/security.py",
    "app/workflow.py",
    "app/wizards.py",
    "app/reports.py",
    "app/integrations.py",
    "app/dashboards.py",
    "app/events.py",
    "app/extensions.py",
    "app/diagnostics.py",
    "app/api_testing.py",
    "app/runtime_assurance.py",
    "app/platforms.py",
    "app/low_code_features.py",
    "native/mobile/app.py",
    "native/desktop/app.py",
    "scripts/appgen_quality.py",
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


def base_feature_generation_smoke_audit(source: str = BASE_FEATURE_SAMPLE_DSL) -> dict:
    """Generate an app and exercise generated docs/base_features.md evidence."""
    import importlib.util
    import py_compile
    import tempfile

    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    with tempfile.TemporaryDirectory(prefix="appgen-base-features-") as raw_workdir:
        project_dir = Path(raw_workdir) / "base-features"
        generate_app_from_schema(
            schema_from_dsl(source, source_name="base-features.appgen"),
            project_dir / "app",
        )
        existing_paths = {
            path.relative_to(project_dir).as_posix()
            for path in project_dir.rglob("*")
            if path.is_file()
        }
        missing = tuple(
            artifact
            for artifact in BASE_FEATURE_SMOKE_REQUIRED_ARTIFACTS
            if artifact not in existing_paths
        )
        compiled = []
        compile_failures = []
        for relative in BASE_FEATURE_SMOKE_PYTHON_ARTIFACTS:
            path = project_dir / relative
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"path": relative, "error": str(exc)})
            else:
                compiled.append(relative)

        def load_module(relative: str, module_name: str):
            spec = importlib.util.spec_from_file_location(module_name, project_dir / relative)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        low_code = load_module("app/low_code_features.py", "appgen_base_low_code")
        runtime_assurance = load_module(
            "app/runtime_assurance.py",
            "appgen_base_runtime_assurance",
        )
        platforms = load_module("app/platforms.py", "appgen_base_platforms")
        data_access = load_module("app/data_access.py", "appgen_base_data_access")

        base_alignment = low_code.base_feature_alignment()
        source_report = low_code.roadmap_source_report()
        roadmap_gate = low_code.roadmap_release_audit(existing_paths)
        runtime_gate = runtime_assurance.application_release_gate(existing_paths=existing_paths)
        platform_gate = platforms.platform_release_gate(existing_paths)
        data_gate = data_access.data_access_release_gate(
            {"app/data_access.py", "app/templates/appgen_data_access.html"}
        )

    checks = (
        {
            "id": "generated_base_artifacts",
            "ok": not missing,
            "required_artifacts": BASE_FEATURE_SMOKE_REQUIRED_ARTIFACTS,
            "missing": missing,
        },
        {
            "id": "generated_python_compiles",
            "ok": not compile_failures
            and set(compiled) == set(BASE_FEATURE_SMOKE_PYTHON_ARTIFACTS),
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
        {
            "id": "generated_base_feature_alignment",
            "ok": len(base_alignment) == 16
            and all(item["covered"] for item in base_alignment)
            and source_report["base_features_complete"] is True,
            "requirements": tuple(item["id"] for item in base_alignment),
        },
        {
            "id": "generated_roadmap_release_gate",
            "ok": roadmap_gate["ok"],
            "decision": roadmap_gate["decision"],
        },
        {
            "id": "generated_runtime_assurance",
            "ok": runtime_gate["ok"]
            and {
                "security",
                "operations",
                "experience",
                "delivery",
            }
            <= {area["id"] for area in runtime_gate["areas"]},
            "decision": runtime_gate["decision"],
        },
        {
            "id": "generated_platform_and_data_access",
            "ok": platform_gate["ok"] and data_gate["ok"],
            "platform_targets": platform_gate["targets"],
            "data_access_format": data_gate["format"],
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.base-feature-generation-smoke-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": BASE_FEATURE_SMOKE_REQUIRED_ARTIFACTS,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
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
    generation_smoke = base_feature_generation_smoke_audit()
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
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
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
        "generation_smoke": generation_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-base-feature-readiness-unless-ok-is-true",
    }
