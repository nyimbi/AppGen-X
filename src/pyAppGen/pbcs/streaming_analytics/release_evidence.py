"""Dynamic release evidence for the streaming_analytics PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import permissions
from . import schema_contract
from . import service_contract
from . import seed_data
from . import ui
from .runtime import streaming_analytics_build_release_evidence as _runtime_build_release_evidence
from .runtime import streaming_analytics_runtime_smoke


PBC_KEY = "streaming_analytics"
PACKAGE_DIR = Path(__file__).resolve().parent


def _artifact_paths() -> tuple[dict, ...]:
    artifacts = (
        "RELEASE_EVIDENCE.md",
        "SPECIFICATION.md",
        "migrations/001_initial.sql",
        "tests/test_contract.py",
        "tests/test_standalone.py",
        "standalone.py",
    )
    return tuple(
        {
            "artifact": artifact,
            "exists": (PACKAGE_DIR / artifact).exists(),
        }
        for artifact in artifacts
    )


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = _runtime_build_release_evidence()
    event_manifest = events.event_contract_manifest()
    agent_manifest = agent.composed_agent_contribution()
    ui_manifest = ui.streaming_analytics_ui_contract()
    permission_manifest = permissions.permission_manifest()
    seed_manifest = seed_data.seed_bundle()
    artifact_status = _artifact_paths()
    from . import standalone

    standalone_smoke = standalone.workbench_smoke_test()
    checks = tuple(runtime_evidence["checks"]) + (
        {"id": "package_artifacts_present", "ok": all(item["exists"] for item in artifact_status)},
        {"id": "agent_surface_present", "ok": agent_manifest["ok"]},
        {"id": "ui_forms_wizards_controls_present", "ok": bool(ui_manifest["forms"]) and bool(ui_manifest["wizards"]) and bool(ui_manifest["controls"])},
        {"id": "standalone_workbench_smoke", "ok": standalone_smoke["ok"]},
        {"id": "seed_bundle_present", "ok": seed_manifest["ok"]},
        {"id": "permission_manifest_present", "ok": permission_manifest["ok"] and bool(permission_manifest["action_permissions"])},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.streaming-analytics-release-evidence.v2",
        "ok": not blocking_gaps,
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema_contract.build_schema_contract(),
        "service": service_contract.build_service_contract(),
        "api": runtime_evidence["api"],
        "permissions": permission_manifest,
        "events": event_manifest,
        "ui": ui_manifest,
        "agent": agent_manifest,
        "seed": seed_manifest,
        "runtime_smoke": streaming_analytics_runtime_smoke(),
        "standalone_smoke": standalone_smoke,
        "artifact_status": artifact_status,
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "events", "ui", "agent", "seed")
        if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence["ok"] and bool(evidence["checks"]),
        "pbc": PBC_KEY,
        "format": evidence["format"],
        "sections": sections,
        "checks": tuple(evidence["checks"]),
        "blocking_gaps": tuple(evidence["blocking_gaps"]),
        "required_sections": ("schema", "service", "api", "permissions", "events", "ui", "agent", "seed"),
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
