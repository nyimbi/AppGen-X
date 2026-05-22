"""Package-level Studio/IDE contracts for AppGen.

Generated apps expose a rich in-app Studio.  This module provides the same
pre-generation contract for CLI and package users who are designing databases,
writing DSL, and managing application generation before an app exists.
"""

from __future__ import annotations

import hashlib

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


def studio_release_audit(source: str = SAMPLE_DSL) -> dict:
    """Return package-level proof for robust Studio/IDE readiness."""
    workspace = studio_workspace(source)
    editor = workspace["dsl_authoring"]
    database = workspace["database_design"]
    jobs = workspace["generation_jobs"]
    management = workspace["application_management"]
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
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-studio-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "workspace": workspace,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-robust-ide-unless-ok-is-true",
    }
