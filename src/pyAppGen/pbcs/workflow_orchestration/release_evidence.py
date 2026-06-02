"""Generated release evidence for the workflow_orchestration PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import models
from . import permissions
from . import repository
from . import schema_contract
from . import service_contract
from . import ui
from .runtime import workflow_orchestration_build_release_evidence as _runtime_build_release_evidence
from .runtime import workflow_orchestration_runtime_smoke


PBC_KEY = "workflow_orchestration"
_PACKAGE_DIR = Path(__file__).resolve().parent


def _artifact_paths() -> tuple[dict, ...]:
    artifacts = (
        "README.md",
        "SPECIFICATION.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
        "migrations/001_initial.sql",
        "repository.py",
        "standalone.py",
        "tests/test_contract.py",
        "tests/test_standalone.py",
    )
    return tuple(
        {
            "artifact": artifact,
            "exists": (_PACKAGE_DIR / artifact).exists(),
        }
        for artifact in artifacts
    )


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = _runtime_build_release_evidence()
    event_manifest = events.event_contract_manifest()
    agent_manifest = agent.composed_agent_contribution()
    ui_manifest = ui.workflow_orchestration_ui_contract()
    model_manifest = models.model_manifest()
    database_models = models.database_model_contract()
    repository_manifest = repository.workflow_orchestration_repository_contract()
    repository_smoke = repository.smoke_test()
    artifact_status = _artifact_paths()
    from . import standalone

    standalone_smoke = standalone.workbench_smoke_test()
    gate_results = {
        "pbc_source_artifact_contract": all(item["exists"] for item in artifact_status)
        and schema_contract.validate_schema_contract()["ok"]
        and model_manifest["ok"]
        and repository_smoke["ok"],
        "pbc_implementation_release_audit": runtime_evidence["ok"]
        and service_contract.build_service_contract()["ok"]
        and event_manifest["ok"]
        and ui_manifest["ok"]
        and agent_manifest["ok"],
        "pbc_generation_smoke_audit": workflow_orchestration_runtime_smoke()["ok"]
        and repository_smoke["ok"]
        and standalone_smoke["ok"],
    }
    checks = tuple(runtime_evidence["checks"]) + (
        {"id": "package_artifacts_present", "ok": all(item["exists"] for item in artifact_status)},
        {"id": "repository_surface_present", "ok": repository_manifest["ok"] and repository_smoke["ok"]},
        {"id": "agent_surface_present", "ok": agent_manifest["ok"]},
        {"id": "ui_forms_wizards_controls_present", "ok": bool(ui_manifest["forms"]) and bool(ui_manifest["wizards"]) and bool(ui_manifest["controls"])},
        {"id": "standalone_surface_present", "ok": standalone_smoke["ok"]},
        {"id": "repo_gate_pbc_source_artifact_contract", "ok": gate_results["pbc_source_artifact_contract"]},
        {"id": "repo_gate_pbc_implementation_release_audit", "ok": gate_results["pbc_implementation_release_audit"]},
        {"id": "repo_gate_pbc_generation_smoke_audit", "ok": gate_results["pbc_generation_smoke_audit"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.workflow-orchestration-release-evidence.v2",
        "ok": not blocking_gaps,
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema_contract.build_schema_contract(),
        "service": service_contract.build_service_contract(),
        "api": runtime_evidence["api"],
        "permissions": permissions.permission_manifest(),
        "events": event_manifest,
        "ui": ui_manifest,
        "agent": agent_manifest,
        "models": database_models,
        "repository": repository_manifest,
        "runtime_smoke": workflow_orchestration_runtime_smoke(),
        "repository_smoke": repository_smoke,
        "standalone_smoke": standalone_smoke,
        "artifact_status": artifact_status,
        "repo_gate_results": gate_results,
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "events", "ui", "agent", "models", "repository")
        if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence["ok"] and bool(evidence["checks"]),
        "pbc": PBC_KEY,
        "format": evidence["format"],
        "sections": sections,
        "checks": tuple(evidence["checks"]),
        "blocking_gaps": tuple(evidence["blocking_gaps"]),
        "required_sections": ("schema", "service", "api", "events", "ui", "agent", "models", "repository"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", evidence["schema"].get("shared_table_access") is not False),
            ("service_shared_table_access", evidence["service"].get("shared_table_access") is not False),
            ("api_shared_table_access", evidence["api"].get("shared_table_access") is not False),
            ("repository_shared_table_access", evidence["repository"].get("shared_table_access") is not False),
            ("missing_repo_gate_result", set(evidence["repo_gate_results"]) != {"pbc_source_artifact_contract", "pbc_implementation_release_audit", "pbc_generation_smoke_audit"}),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and evidence["pbc"] == manifest["pbc"]
        and not manifest["blocking_gaps"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence["ok"],
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
