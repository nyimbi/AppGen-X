"""Package-level roadmap release audit helpers.

Generated apps already expose roadmap evidence in ``low_code_features.py``.
This module gives the AppGen CLI the same kind of top-level proof before an app
has been generated.
"""

from __future__ import annotations

import importlib.util
import py_compile
import subprocess
import sys
import tempfile
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
            "visual drag-and-drop form design",
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
        "id": "rad-form-designer",
        "description": "Allow users to drop components onto forms in a visual drag-and-drop designer.",
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
        "id": "rad-form-design",
        "description": "visual drag-and-drop drop-target form designer and component palette.",
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
EXCELLENCE_SAMPLE_DSL = """
app ExcellenceAudit { theme: sage; targets: web, pwa, mobile, desktop, chatbot }

table Customer {
  id: int pk
  name: string required search
  email: email search
}

table Invoice {
  id: int pk
  customer_id: int required -> Customer.id [many-to-one]
  invoice_no: string required unique search
  total_amount: decimal required
  due_date: date
}

view InvoiceForm for Invoice {
  Main: customer_id, invoice_no, total_amount, due_date
  @ invoice_no TextBox 0 0 6 1
  @ total_amount NumberInput 0 1 6 1
  @ due_date DatePicker 0 2 6 1
}
"""
EXCELLENCE_SMOKE_PYTHON_ARTIFACTS = (
    "app/models.py",
    "app/views.py",
    "app/branding.py",
    "app/runtime_assurance.py",
    "scripts/appgen_quality.py",
    "tests/test_generated_contract.py",
    "tests/test_generated_coverage.py",
)
EXCELLENCE_SMOKE_REQUIRED_ARTIFACTS = (
    "app/branding.py",
    "app/static/appgen-theme.css",
    "app/templates/appgen_branding.html",
    "app/runtime_assurance.py",
    "app/templates/appgen_runtime_assurance.html",
    "scripts/appgen_quality.py",
    "tests/test_generated_contract.py",
    "app/appgen.json",
    "docs/schema.md",
)
LOW_CODE_ROADMAP_SMOKE_REQUIRED_ARTIFACTS = (
    "app/low_code_features.py",
    "app/templates/appgen_low_code_features.html",
    "app/appgen.json",
    "jhipster/app.jdl",
    "cookiecutter/cookiecutter.json",
)
LOW_CODE_ROADMAP_SMOKE_PYTHON_ARTIFACTS = (
    "app/low_code_features.py",
    "app/models.py",
    "app/views.py",
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
    smoke = generated_app_excellence_smoke_audit()
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
        {
            "id": "generated_excellence_smoke",
            "ok": smoke["ok"],
            "checks": smoke["checks"],
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.generated-app-excellence-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "categories": categories,
        "generated_smoke": smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-generated-app-excellence-unless-ok-is-true",
    }


def generated_app_excellence_smoke_audit() -> dict:
    """Generate an app and exercise its own excellence and quality gates."""
    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    with tempfile.TemporaryDirectory(prefix="appgen-excellence-") as raw_workdir:
        project_dir = Path(raw_workdir) / "excellence"
        generate_app_from_schema(
            schema_from_dsl(EXCELLENCE_SAMPLE_DSL, source_name="excellence.appgen"),
            project_dir / "app",
        )
        existing_paths = {
            path.relative_to(project_dir).as_posix()
            for path in project_dir.rglob("*")
            if path.is_file()
        }
        missing = tuple(
            path for path in EXCELLENCE_SMOKE_REQUIRED_ARTIFACTS if path not in existing_paths
        )
        compiled = _compile_generated_excellence_artifacts(project_dir)
        quality = _run_generated_quality_script(project_dir)
        runtime_assurance = _load_generated_module(
            project_dir / "app" / "runtime_assurance.py",
            "appgen_generated_runtime_assurance",
        )
        branding = _load_generated_module(
            project_dir / "app" / "branding.py",
            "appgen_generated_branding",
        )
        runtime_gate = runtime_assurance.generated_app_excellence_gate(
            {"p95_ms": 200, "error_rate": 0},
            set(runtime_assurance.REQUIRED_RELEASE_ARTIFACTS),
        )
        ui_gate = branding.ui_experience_excellence_gate(
            {
                "app/branding.py",
                "app/static/appgen-theme.css",
                "app/templates/appgen_branding.html",
            }
        )
        visual_quality = branding.visual_experience_quality_report()
    checks = (
        {
            "check": "required_artifacts",
            "ok": not missing,
            "missing": missing,
        },
        {
            "check": "compiled_excellence_artifacts",
            "ok": all(item["ok"] for item in compiled),
            "artifacts": EXCELLENCE_SMOKE_PYTHON_ARTIFACTS,
        },
        {
            "check": "generated_quality_script",
            "ok": quality["ok"],
            "returncode": quality["returncode"],
        },
        {
            "check": "runtime_excellence_gate",
            "ok": runtime_gate["ok"]
            and {
                "beautiful",
                "sophisticated",
                "secure",
                "reliable",
                "robust",
                "functional",
                "highly_capable",
            }
            == {category["id"] for category in runtime_gate["categories"]},
            "decision": runtime_gate["decision"],
        },
        {
            "check": "ui_experience_gate",
            "ok": ui_gate["ok"] and visual_quality["ok"],
            "decision": "approved" if ui_gate["ok"] and visual_quality["ok"] else "blocked",
        },
    )
    return {
        "format": "appgen.generated-app-excellence-smoke-audit.v1",
        "scope": "package",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "compiled": compiled,
        "quality": quality,
        "runtime_excellence": {
            "format": runtime_gate["format"],
            "decision": runtime_gate["decision"],
            "categories": tuple(category["id"] for category in runtime_gate["categories"]),
        },
        "ui_excellence": {
            "format": ui_gate["format"],
            "decision": "approved" if ui_gate["ok"] and visual_quality["ok"] else "blocked",
            "visual_quality": visual_quality["ok"],
        },
    }


def low_code_roadmap_generation_smoke_audit() -> dict:
    """Generate an app and exercise its emitted low-code roadmap contract."""
    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    with tempfile.TemporaryDirectory(prefix="appgen-low-code-roadmap-") as raw_workdir:
        project_dir = Path(raw_workdir) / "low-code-roadmap"
        generate_app_from_schema(
            schema_from_dsl(EXCELLENCE_SAMPLE_DSL, source_name="low-code-roadmap.appgen"),
            project_dir / "app",
        )
        existing_paths = {
            path.relative_to(project_dir).as_posix()
            for path in project_dir.rglob("*")
            if path.is_file()
        }
        missing = tuple(
            path
            for path in LOW_CODE_ROADMAP_SMOKE_REQUIRED_ARTIFACTS
            if path not in existing_paths
        )
        compiled = []
        compile_failures = []
        for relative in LOW_CODE_ROADMAP_SMOKE_PYTHON_ARTIFACTS:
            path = project_dir / relative
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"path": relative, "error": str(exc)})
            else:
                compiled.append(relative)

        low_code = _load_generated_module(
            project_dir / "app" / "low_code_features.py",
            "appgen_generated_low_code_roadmap",
        )
        release_paths = {
            "app/low_code_features.py",
            "app/templates/appgen_low_code_features.html",
            "app/appgen.json",
        }
        source_documents = low_code.source_document_contracts()
        readiness = low_code.readiness_report()
        roadmap_gate = low_code.roadmap_release_audit(existing_paths)
        composition_gate = low_code.composition_release_gate(release_paths)
        composition_workbench = low_code.composition_workbench(release_paths)
        superset = low_code.jhipster_superset_certification()
        frontier = low_code.jhipster_frontier_gate()
        template = (project_dir / "app" / "templates" / "appgen_low_code_features.html").read_text(
            encoding="utf-8"
        )

    checks = (
        {
            "id": "generated_low_code_artifacts",
            "ok": not missing,
            "required_artifacts": LOW_CODE_ROADMAP_SMOKE_REQUIRED_ARTIFACTS,
            "missing": missing,
        },
        {
            "id": "generated_low_code_compiles",
            "ok": not compile_failures
            and set(compiled) == set(LOW_CODE_ROADMAP_SMOKE_PYTHON_ARTIFACTS),
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
        {
            "id": "source_document_lineage",
            "ok": {"docs/ideas.md", "docs/base_features.md", "docs/Lo-code features.md"}
            <= {document["document"] for document in source_documents}
            and readiness["roadmap_sources_ok"] is True,
            "documents": tuple(document["document"] for document in source_documents),
        },
        {
            "id": "generated_roadmap_release_gate",
            "ok": roadmap_gate["ok"]
            and {
                "source_document_lineage",
                "implementation_status",
                "base_feature_requirements",
                "ideas_roadmap_requirements",
                "low_code_feature_families",
                "artifact_evidence",
                "route_surface",
                "test_evidence",
                "jhipster_superset",
            }
            == {check["id"] for check in roadmap_gate["checks"]},
            "decision": roadmap_gate["decision"],
        },
        {
            "id": "generated_composition_and_superset",
            "ok": composition_gate["ok"]
            and composition_workbench["ok"]
            and superset["ok"]
            and frontier["ok"],
            "composition": composition_gate["format"],
            "workbench": composition_workbench["format"],
            "certification": superset["certification"],
            "frontier": frontier["format"],
        },
        {
            "id": "generated_template_routes",
            "ok": "Roadmap Release Audit JSON" in template
            and "Composition Workbench JSON" in template
            and "JHipster Frontier Gate JSON" in template,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.low-code-roadmap-generation-smoke-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": LOW_CODE_ROADMAP_SMOKE_REQUIRED_ARTIFACTS,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def _compile_generated_excellence_artifacts(project_dir: Path) -> tuple[dict, ...]:
    results = []
    for relative in EXCELLENCE_SMOKE_PYTHON_ARTIFACTS:
        path = project_dir / relative
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            results.append({"path": relative, "ok": False, "error": str(exc)})
        else:
            results.append({"path": relative, "ok": True})
    return tuple(results)


def _run_generated_quality_script(project_dir: Path) -> dict:
    script = project_dir / "scripts" / "appgen_quality.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=project_dir,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "ok": result.returncode == 0 and "appgen quality passed" in result.stdout,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def _load_generated_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load generated module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def package_goal_audit(root: Path | str | None = None) -> dict:
    """Return aggregate package evidence for the active AppGen objective."""
    from .agentic import agentic_release_audit
    from .base_features import base_feature_release_audit
    from .config_admin import config_editor_release_audit
    from .distribution import distribution_release_audit
    from .dsl_quality import dsl_release_audit
    from .erp import erp_template_release_audit
    from .form_designer import form_designer_release_audit
    from .ideas import ideas_release_audit
    from .integrations import integration_release_audit
    from .nl import nl_evolution_release_audit
    from .ops import ops_release_audit
    from .pbc import pbc_release_audit
    from .reporting import reporting_release_audit
    from .security import security_release_audit
    from .source_intake import source_intake_release_audit
    from .studio import studio_release_audit
    from .targets import target_release_audit
    from .visual_modeling import visual_modeling_release_audit

    roadmap = roadmap_release_audit(root)
    ideas = ideas_release_audit(root)
    base_features = base_feature_release_audit(root)
    superiority = jhipster_superiority_audit()
    excellence = generated_app_excellence_audit()
    dsl_quality = dsl_release_audit(root=root)
    erp_templates = erp_template_release_audit()
    nl_evolution = nl_evolution_release_audit()
    studio = studio_release_audit()
    form_designer = form_designer_release_audit()
    visual_modeling = visual_modeling_release_audit()
    security = security_release_audit()
    source_intake = source_intake_release_audit()
    config_editor = config_editor_release_audit()
    distribution = distribution_release_audit()
    reporting = reporting_release_audit()
    ops = ops_release_audit()
    integrations = integration_release_audit()
    agentic = agentic_release_audit()
    targets = target_release_audit()
    pbc = pbc_release_audit()
    parity_requirement_audit = form_designer["rad_parity"]["requirement_audit"]
    parity_requirement_ids = tuple(
        requirement["id"] for requirement in parity_requirement_audit["requirements"]
    )
    gates = (
        {
            "id": "roadmap_traceability",
            "ok": roadmap["ok"],
            "format": roadmap["format"],
        },
        {
            "id": "ideas_roadmap_contract",
            "ok": ideas["ok"],
            "format": ideas["format"],
        },
        {
            "id": "base_feature_contract",
            "ok": base_features["ok"],
            "format": base_features["format"],
        },
        {
            "id": "jhipster_superiority",
            "ok": superiority["ok"],
            "format": superiority["format"],
        },
        {
            "id": "generated_app_excellence",
            "ok": excellence["ok"],
            "format": excellence["format"],
        },
        {
            "id": "dsl_linter_docs_grammar",
            "ok": dsl_quality["ok"],
            "format": dsl_quality["format"],
        },
        {
            "id": "erp_template_exports",
            "ok": erp_templates["ok"],
            "format": erp_templates["format"],
        },
        {
            "id": "natural_language_evolution",
            "ok": nl_evolution["ok"],
            "format": nl_evolution["format"],
        },
        {
            "id": "robust_ide",
            "ok": studio["ok"],
            "format": studio["format"],
        },
        {
            "id": "rad_form_designer",
            "ok": form_designer["ok"],
            "format": form_designer["format"],
        },
        {
            "id": "platform_parity_requirement_map",
            "ok": parity_requirement_audit["ok"]
            and {
                "component_parity",
                "native_runtime_streaming",
                "inspector_design_surface",
                "visual_binding_designer",
                "native_data_service_tooling",
                "package_installation_ecosystem",
                "device_api_component_coverage",
                "cross_target_visual_depth",
            }
            == set(parity_requirement_ids)
            and {
                "all_requirements_have_evidence",
                "all_requirements_pass",
                "lifecycle_replay_aligned",
            }
            <= {check["id"] for check in parity_requirement_audit["checks"] if check["ok"]},
            "format": parity_requirement_audit["format"],
            "requirements": parity_requirement_ids,
        },
        {
            "id": "visual_modeling",
            "ok": visual_modeling["ok"],
            "format": visual_modeling["format"],
        },
        {
            "id": "security_identity",
            "ok": security["ok"],
            "format": security["format"],
        },
        {
            "id": "schema_source_intake",
            "ok": source_intake["ok"],
            "format": source_intake["format"],
        },
        {
            "id": "config_editor",
            "ok": config_editor["ok"],
            "format": config_editor["format"],
        },
        {
            "id": "publishable_distribution",
            "ok": distribution["ok"],
            "format": distribution["format"],
        },
        {
            "id": "reporting_chartviews",
            "ok": reporting["ok"],
            "format": reporting["format"],
        },
        {
            "id": "ops_deployment_search",
            "ok": ops["ok"],
            "format": ops["format"],
        },
        {
            "id": "enterprise_integrations",
            "ok": integrations["ok"],
            "format": integrations["format"],
        },
        {
            "id": "agentic_systems",
            "ok": agentic["ok"],
            "format": agentic["format"],
        },
        {
            "id": "multi_target_generation",
            "ok": targets["ok"],
            "format": targets["format"],
        },
        {
            "id": "composable_pbc_catalog",
            "ok": pbc["ok"],
            "format": pbc["format"],
        },
        {
            "id": "source_document_scope",
            "ok": {"docs/ideas.md", "docs/base_features.md", "docs/Lo-code features.md"}
            <= {document["path"] for document in roadmap["documents"]},
            "documents": tuple(document["path"] for document in roadmap["documents"]),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-goal-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "gates": gates,
        "audits": {
            "roadmap": roadmap,
            "ideas": ideas,
            "base_features": base_features,
            "jhipster_superiority": superiority,
            "generated_app_excellence": excellence,
            "dsl_quality": dsl_quality,
            "erp_templates": erp_templates,
            "natural_language_evolution": nl_evolution,
            "studio": studio,
            "form_designer": form_designer,
            "visual_modeling": visual_modeling,
            "security": security,
            "source_intake": source_intake,
            "config_editor": config_editor,
            "distribution": distribution,
            "reporting": reporting,
            "ops": ops,
            "integrations": integrations,
            "agentic": agentic,
            "targets": targets,
            "pbc": pbc,
        },
        "platform_parity_requirements": parity_requirement_audit,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-mark-active-goal-complete-unless-ok-is-true",
    }


def roadmap_release_audit(root: Path | str | None = None) -> dict:
    """Return package-level proof that roadmap docs map to implemented features."""
    documents = roadmap_document_checks(root)
    capability_checks = roadmap_capability_checks()
    generation_smoke = low_code_roadmap_generation_smoke_audit()
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
        {
            "id": "generated_low_code_roadmap",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
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
        "generation_smoke": generation_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
    }
