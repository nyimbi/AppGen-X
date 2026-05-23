"""Package-level Studio/IDE contracts for AppGen.

Generated apps expose a rich in-app Studio.  This module provides the same
pre-generation contract for CLI and package users who are designing databases,
writing DSL, and managing application generation before an app exists.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .dsl import dsl_authoring_release_gate
from .dsl import dsl_code_actions
from .dsl import dsl_completion_items
from .dsl import dsl_outline
from .dsl import format_dsl
from .dsl import lint_dsl
from .schema import schema_source_contract


SAMPLE_DSL = """app StudioDemo { targets: web, mobile, desktop }
table Customer { id: int pk; name: string required search; email: email search }
table Invoice { id: int pk; customer_id: int required -> Customer.id [many-to-one]; invoice_no: string required search; total_amount: decimal required }
view InvoiceForm for Invoice { Main: customer_id, invoice_no, total_amount; @ invoice_no TextBox 0 0 6 1; @ total_amount NumberInput 0 1 6 1; }
llm LocalModel { provider: ollama; mode: local; model: llama3 }
agent BuilderAssistant { provider: LocalModel; goal: "Help design and generate applications"; tools: schema, forms, chatbots }
"""


def studio_workspace(source: str = SAMPLE_DSL) -> dict:
    """Return the package Studio workspace contract."""
    formatted = format_dsl(source)
    stable_source = formatted["formatted"] if formatted["after"]["ok"] else source
    editor = dsl_editor_state(stable_source)
    return {
        "format": "appgen.package-studio-workspace.v1",
        "sections": (
            "dsl_authoring",
            "database_design",
            "source_intake",
            "generation_jobs",
            "application_management",
            "natural_language_evolution",
        ),
        "dsl_authoring": editor,
        "database_design": database_design_workspace(stable_source),
        "source_intake": source_intake_profiles(),
        "generation_jobs": generation_job_queue((generation_job_manifest(changed_paths=("appgen.dsl",)),)),
        "application_management": application_management_plan(),
        "formatted_preview": stable_source,
    }


def dsl_editor_state(text: str = SAMPLE_DSL) -> dict:
    """Return IDE-ready DSL authoring feedback."""
    lint = lint_dsl(text, source_name="studio.dsl")
    return {
        "format": "appgen.package-dsl-editor-state.v1",
        "ok": lint["ok"],
        "commands": (
            "open_dsl",
            "lint_dsl",
            "format_dsl",
            "show_outline",
            "apply_code_action",
            "preview_schema",
            "apply_natural_language_change",
        ),
        "panels": ("outline", "diagnostics", "completions", "code_actions", "schema_preview"),
        "lint": lint,
        "outline": dsl_outline(text, source_name="studio.dsl"),
        "completions": dsl_completion_items(""),
        "code_actions": dsl_code_actions(text, source_name="studio.dsl"),
        "release_gate": dsl_authoring_release_gate(text, source_name="studio.dsl"),
    }


def database_design_workspace(source: str = SAMPLE_DSL) -> dict:
    """Return database-design data the Studio can render before generation."""
    lint = lint_dsl(source, source_name="studio.dsl")
    outline = dsl_outline(source, source_name="studio.dsl")
    tables = tuple(
        {
            "table": table["name"],
            "fields": tuple(table["fields"]),
            "primary_action": "edit_table",
        }
        for table in outline.get("tables", ())
    )
    return {
        "format": "appgen.package-database-design-workspace.v1",
        "ok": lint["ok"] and bool(tables),
        "tables": tables,
        "proposal_kinds": ("add_table", "add_field", "relationship", "index", "enum", "rename"),
        "guards": ("dsl_lint", "schema_diff", "migration_preview", "rollback_plan"),
        "exports": ("appgen_dsl", "dbml", "sql_ddl", "ponyorm"),
    }


def source_intake_profiles() -> dict:
    """Return source families the IDE can import into the database designer."""
    contract = schema_source_contract()
    return {
        "format": "appgen.package-source-intake.v1",
        "ok": contract["ok"],
        "sources": contract["source_kinds"],
        "commands": tuple(item["command"] for item in contract["sources"]),
    }


def generation_job_manifest(
    command: str = "generate",
    targets: tuple[str, ...] = ("web", "mobile", "desktop"),
    changed_paths: tuple[str, ...] = (),
) -> dict:
    """Return a deterministic generation job manifest."""
    stages = ("lint_dsl", "schema_diff", "generate", "quality", "package")
    job_key = "|".join((command, ",".join(targets), ",".join(changed_paths or ("appgen.dsl",))))
    return {
        "format": "appgen.package-generation-job.v1",
        "job_id": hashlib.sha1(job_key.encode("utf-8")).hexdigest()[:12],
        "command": command,
        "targets": targets,
        "changed_paths": changed_paths or ("appgen.dsl",),
        "stages": stages,
        "status": "planned",
        "quality_gates": ("dsl_authoring_gate", "schema_source_audit", "package_goal_audit"),
    }


def generation_job_queue(jobs: tuple[dict, ...] = ()) -> dict:
    """Return the Studio generation queue contract."""
    queued = jobs or (generation_job_manifest(),)
    return {
        "format": "appgen.package-generation-queue.v1",
        "ok": bool(queued),
        "jobs": queued,
        "commands": ("plan_generation", "run_generation", "open_artifacts", "rerun_quality"),
    }


def application_management_plan() -> dict:
    """Return generated-application management capabilities for Studio."""
    return {
        "format": "appgen.package-application-management.v1",
        "commands": (
            "create_application",
            "import_source",
            "snapshot_application",
            "restore_application",
            "compare_versions",
            "export_package",
        ),
        "managed_artifacts": ("appgen.dsl", "generated_app", "migration_plan", "quality_report"),
        "history": ("draft", "generated", "verified", "packaged"),
    }


def studio_browser_smoke_ci_contract(repo_root: str | Path | None = None) -> dict:
    """Return CI/prepared-host evidence for the Studio browser smoke harness."""
    root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
    frontend = root / "appgen-frontend"
    package_path = frontend / "package.json"
    smoke_script = frontend / "scripts" / "browser-smoke.mjs"
    workflow_path = root / ".github" / "workflows" / "studio-browser-smoke.yml"
    package = {}
    if package_path.exists():
        package = json.loads(package_path.read_text(encoding="utf-8"))
    script_text = smoke_script.read_text(encoding="utf-8") if smoke_script.exists() else ""
    workflow_text = workflow_path.read_text(encoding="utf-8") if workflow_path.exists() else ""
    scenarios = ("studio_shell", "device_palette_filter", "storage_search_filter", "empty_palette_state")
    checks = (
        {
            "id": "frontend_package_script",
            "ok": package.get("scripts", {}).get("test:browser") == "npm run build && node scripts/browser-smoke.mjs",
        },
        {
            "id": "browser_smoke_script",
            "ok": smoke_script.exists()
            and "appgen.studio-browser-smoke.v1" in script_text
            and all(scenario in script_text for scenario in scenarios),
        },
        {
            "id": "ci_workflow",
            "ok": workflow_path.exists()
            and "npm ci" in workflow_text
            and "npm run test:browser" in workflow_text
            and "APPGEN_CHROME_BIN" in workflow_text,
        },
        {
            "id": "prepared_host_contract",
            "ok": "Set APPGEN_CHROME_BIN" in script_text
            and "--disable-crash-reporter" in script_text
            and "--user-data-dir=" in script_text,
        },
    )
    return {
        "format": "appgen.studio-browser-smoke-ci-contract.v1",
        "ok": all(check["ok"] for check in checks),
        "frontend": str(frontend),
        "command": "npm run test:browser",
        "workflow": str(workflow_path),
        "script": str(smoke_script),
        "scenarios": scenarios,
        "environment": {
            "browser_binary": "APPGEN_CHROME_BIN",
            "node": "20",
            "working_directory": "appgen-frontend",
        },
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def studio_generation_smoke_audit(source: str = SAMPLE_DSL) -> dict:
    """Generate a temporary app and exercise its generated Studio contract."""
    import importlib.util
    import py_compile
    import tempfile
    from pathlib import Path

    from .gen import generate_app_from_schema
    from .schema import load_schema

    required_artifacts = (
        "app/studio.py",
        "app/templates/appgen_studio.html",
        "app/dsl_reference.py",
        "app/database_ops.py",
        "app/designer.py",
        "app/models.py",
        "migrations/README.md",
        "scripts/appgen_quality.py",
    )
    compile_artifacts = (
        "app/studio.py",
        "app/dsl_reference.py",
        "app/database_ops.py",
        "app/designer.py",
        "app/models.py",
    )

    with tempfile.TemporaryDirectory(prefix="appgen-studio-smoke-") as tmp:
        project_dir = Path(tmp)
        dsl_path = project_dir / "studio.appgen"
        dsl_path.write_text(source, encoding="utf-8")
        schema = load_schema(dsl_path, source_type="dsl")
        output_dir = project_dir / "app"
        generate_app_from_schema(schema, output_dir)

        missing_artifacts = tuple(
            artifact for artifact in required_artifacts if not (project_dir / artifact).exists()
        )
        compiled = []
        compile_failures = []
        for artifact in compile_artifacts:
            path = project_dir / artifact
            if not path.exists():
                continue
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"artifact": artifact, "error": str(exc)})
            else:
                compiled.append(artifact)

        module_path = output_dir / "studio.py"
        spec = importlib.util.spec_from_file_location("generated_studio_smoke", module_path)
        generated_studio = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated_studio)
        existing_paths = set(required_artifacts)
        workspace = generated_studio.ide_workspace()
        editor_state = generated_studio.dsl_editor_state(
            text="app Bad { targets: web, toaster } table Book { title: string ref Author.id }"
        )
        database_workspace = generated_studio.database_design_workspace()
        job = generated_studio.generation_job_manifest(
            targets=("web", "mobile", "desktop"), changed_paths=("appgen.dsl",)
        )
        portfolio = generated_studio.application_portfolio_check()
        release_gate = generated_studio.studio_release_gate(existing_paths)
        superiority = generated_studio.ide_superiority_profile(existing_paths)

    checks = (
        {
            "id": "generated_artifacts",
            "ok": not missing_artifacts,
            "required_artifacts": required_artifacts,
            "missing": missing_artifacts,
        },
        {
            "id": "generated_python_compiles",
            "ok": not compile_failures and set(compiled) == set(compile_artifacts),
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
        {
            "id": "workspace_contract",
            "ok": {
                "dsl_authoring",
                "database_design",
                "generation",
                "applications",
                "source_intake",
            }
            <= set(workspace),
            "targets": workspace["generation"]["targets"],
        },
        {
            "id": "dsl_editor_contract",
            "ok": editor_state["language"] == "appgen-dsl"
            and not editor_state["lint"]["ok"]
            and {"normalize_targets", "replace_ref_with_arrow"}
            <= {action["id"] for action in editor_state["code_actions"]},
        },
        {
            "id": "database_designer_contract",
            "ok": database_workspace["erd"].startswith("erDiagram\n")
            and "relationship" in database_workspace["proposal_kinds"],
        },
        {
            "id": "generation_management_contract",
            "ok": tuple(stage["name"] for stage in job["plan"]["stages"])
            == ("lint_dsl", "schema_diff", "generate", "quality")
            and portfolio["ok"]
            and release_gate["ok"]
            and superiority["ok"],
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.studio-generation-smoke-audit.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": required_artifacts,
        "compiled_artifacts": tuple(compiled),
        "workspace_sections": tuple(workspace),
        "release_gate": {
            "format": release_gate["format"],
            "ok": release_gate["ok"],
        },
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def studio_release_audit(source: str = SAMPLE_DSL) -> dict:
    """Return package-level proof for robust Studio/IDE readiness."""
    workspace = studio_workspace(source)
    editor = workspace["dsl_authoring"]
    database = workspace["database_design"]
    jobs = workspace["generation_jobs"]
    management = workspace["application_management"]
    generation_smoke = studio_generation_smoke_audit(source)
    browser_smoke = studio_browser_smoke_ci_contract()
    gates = (
        {
            "id": "workspace_sections",
            "ok": {
                "dsl_authoring",
                "database_design",
                "source_intake",
                "generation_jobs",
                "application_management",
            }
            <= set(workspace["sections"]),
        },
        {"id": "dsl_authoring", "ok": editor["ok"] and editor["release_gate"]["ok"]},
        {"id": "database_design", "ok": database["ok"] and "migration_preview" in database["guards"]},
        {"id": "source_intake", "ok": workspace["source_intake"]["ok"]},
        {"id": "generation_queue", "ok": jobs["ok"] and jobs["jobs"][0]["stages"][0] == "lint_dsl"},
        {"id": "application_management", "ok": "create_application" in management["commands"]},
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
        },
        {
            "id": "browser_smoke_ci",
            "ok": browser_smoke["ok"],
            "checks": tuple(check["id"] for check in browser_smoke["checks"]),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-studio-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "workspace": workspace,
        "generation_smoke": generation_smoke,
        "browser_smoke": browser_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-robust-ide-unless-ok-is-true",
    }
