"""Generated release evidence for the procurement_sourcing PBC."""

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
from .runtime import procurement_sourcing_build_release_evidence as _runtime_build_release_evidence
from .runtime import procurement_sourcing_runtime_smoke


_PACKAGE_DIR = Path(__file__).resolve().parent


def _artifact_paths() -> tuple[dict, ...]:
    artifacts = (
        "README.md",
        "SPECIFICATION.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
        "repository.py",
        "standalone.py",
        "migrations/001_initial.sql",
        "tests/test_contract.py",
        "tests/test_runtime_capabilities.py",
        "tests/test_standalone.py",
    )
    return tuple({"artifact": artifact, "exists": (_PACKAGE_DIR / artifact).exists()} for artifact in artifacts)


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = _runtime_build_release_evidence()
    event_manifest = events.event_contract_manifest()
    agent_manifest = agent.composed_agent_contribution()
    ui_manifest = ui.procurement_sourcing_ui_contract()
    model_manifest = models.model_manifest()
    repository_manifest = repository.procurement_sourcing_repository_contract()
    artifact_status = _artifact_paths()
    from . import standalone

    standalone_smoke = standalone.workbench_smoke_test()
    checks = tuple(runtime_evidence["checks"]) + (
        {"id": "package_artifacts_present", "ok": all(item["exists"] for item in artifact_status)},
        {"id": "agent_surface_present", "ok": agent_manifest["ok"]},
        {
            "id": "ui_forms_wizards_controls_present",
            "ok": bool(ui_manifest["forms"]) and bool(ui_manifest["wizards"]) and bool(ui_manifest["controls"]),
        },
        {"id": "repository_surface_present", "ok": repository_manifest["ok"]},
        {"id": "standalone_smoke", "ok": standalone_smoke["ok"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.procurement-sourcing-release-evidence.v1",
        "ok": not blocking_gaps,
        "pbc": "procurement_sourcing",
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema_contract.build_schema_contract(),
        "service": service_contract.build_service_contract(),
        "api": runtime_evidence["api"],
        "permissions": permissions.permission_manifest(),
        "events": event_manifest,
        "ui": ui_manifest,
        "agent": agent_manifest,
        "models": model_manifest,
        "repository": repository_manifest,
        "runtime_smoke": procurement_sourcing_runtime_smoke(),
        "standalone_smoke": standalone_smoke,
        "artifact_status": artifact_status,
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
        "pbc": "procurement_sourcing",
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
        "pbc": "procurement_sourcing",
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
