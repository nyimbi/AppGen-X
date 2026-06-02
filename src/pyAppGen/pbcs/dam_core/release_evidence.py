"""Generated release evidence for the dam_core PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import models
from . import permissions
from . import schema_contract
from . import service_contract
from . import ui
from .manifest import PBC_MANIFEST
from .runtime import dam_core_build_release_evidence as _runtime_build_release_evidence
from .runtime import dam_core_runtime_smoke


_PACKAGE_DIR = Path(__file__).resolve().parent


def _artifact_paths() -> tuple[dict, ...]:
    artifacts = (
        "README.md",
        "SPECIFICATION.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
        "migrations/001_initial.sql",
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
    ui_manifest = ui.dam_core_ui_contract()
    model_manifest = models.model_manifest()
    artifact_status = _artifact_paths()
    from . import standalone

    standalone_smoke = standalone.workbench_smoke_test()
    gate_results = {
        "pbc_source_artifact_contract": all(item["exists"] for item in artifact_status)
        and schema_contract.validate_schema_contract()["ok"]
        and model_manifest["ok"],
        "pbc_implementation_release_audit": runtime_evidence["ok"]
        and service_contract.build_service_contract()["ok"]
        and event_manifest["ok"]
        and ui_manifest["ok"],
        "pbc_generation_smoke_audit": dam_core_runtime_smoke()["ok"]
        and agent_manifest["ok"]
        and standalone_smoke["ok"],
    }
    checks = tuple(runtime_evidence["checks"]) + (
        {"id": "package_artifacts_present", "ok": all(item["exists"] for item in artifact_status)},
        {"id": "agent_surface_present", "ok": agent_manifest["ok"]},
        {"id": "ui_forms_wizards_controls_present", "ok": bool(ui_manifest["forms"]) and bool(ui_manifest["wizards"]) and bool(ui_manifest["controls"])},
        {"id": "repo_gate_pbc_source_artifact_contract", "ok": gate_results["pbc_source_artifact_contract"]},
        {"id": "repo_gate_pbc_implementation_release_audit", "ok": gate_results["pbc_implementation_release_audit"]},
        {"id": "repo_gate_pbc_generation_smoke_audit", "ok": gate_results["pbc_generation_smoke_audit"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.dam-core-release-evidence.v2",
        "ok": not blocking_gaps,
        "pbc": "dam_core",
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema_contract.build_schema_contract(),
        "service": service_contract.build_service_contract(),
        "api": runtime_evidence["api"],
        "permissions": permissions.permission_manifest(),
        "events": event_manifest,
        "ui": ui_manifest,
        "agent": agent_manifest,
        "models": models.database_model_contract(),
        "runtime_smoke": dam_core_runtime_smoke(),
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
        for name in ("schema", "service", "api", "permissions", "events", "ui", "agent", "models")
        if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence["ok"] and bool(evidence["checks"]),
        "pbc": "dam_core",
        "format": evidence["format"],
        "sections": sections,
        "checks": tuple(evidence["checks"]),
        "blocking_gaps": tuple(evidence["blocking_gaps"]),
        "required_sections": ("schema", "service", "api", "events", "ui", "agent", "models"),
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
            ("missing_repo_gate_result", set(evidence["repo_gate_results"]) != {
                "pbc_source_artifact_contract",
                "pbc_implementation_release_audit",
                "pbc_generation_smoke_audit",
            }),
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
        "pbc": "dam_core",
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
