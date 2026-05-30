"""Dynamic release evidence for the loyalty_rewards PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import models
from . import permissions
from . import routes
from . import seed_data
from . import service_contract
from . import services
from . import schema_contract
from . import ui
from .runtime import loyalty_rewards_build_release_evidence as _runtime_build_release_evidence
from .runtime import loyalty_rewards_runtime_smoke


PBC_KEY = "loyalty_rewards"
PACKAGE_DIR = Path(__file__).resolve().parent
REQUIRED_ARTIFACTS = (
    "SPECIFICATION.md",
    "RELEASE_EVIDENCE.md",
    "__init__.py",
    "manifest.py",
    "agent.py",
    "ui.py",
    "routes.py",
    "services.py",
    "seed_data.py",
    "release_evidence.py",
    "standalone.py",
    "tests/test_contract.py",
    "tests/test_standalone.py",
    "migrations/001_initial.sql",
)


def _artifact_paths() -> tuple[dict, ...]:
    return tuple({"artifact": artifact, "exists": (PACKAGE_DIR / artifact).exists()} for artifact in REQUIRED_ARTIFACTS)


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = _runtime_build_release_evidence()
    event_manifest = events.event_contract_manifest()
    agent_manifest = agent.composed_agent_contribution()
    ui_manifest = ui.loyalty_rewards_ui_contract()
    permission_manifest = permissions.permission_manifest()
    model_manifest = models.model_manifest()
    route_manifest = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    seed_manifest = seed_data.seed_plan()
    service_manifest = services.service_operation_manifest()
    artifact_status = _artifact_paths()
    from . import standalone

    standalone_smoke = standalone.workbench_smoke_test()
    gate_results = {
        "pbc_spec_source_audit": all(item["exists"] for item in artifact_status)
        and schema_contract.validate_schema_contract()["ok"]
        and model_manifest["ok"],
        "pbc_implementation_release_audit": runtime_evidence["ok"]
        and service_contract.build_service_contract()["ok"]
        and event_manifest["ok"]
        and route_validation["ok"]
        and ui_manifest["ok"],
        "pbc_generation_smoke_audit": loyalty_rewards_runtime_smoke()["ok"]
        and agent_manifest["ok"]
        and seed_manifest["ok"]
        and standalone_smoke["ok"],
    }
    checks = tuple(runtime_evidence["checks"]) + (
        {"id": "package_artifacts_present", "ok": all(item["exists"] for item in artifact_status)},
        {"id": "agent_surface_present", "ok": agent_manifest["ok"]},
        {
            "id": "ui_forms_wizards_controls_present",
            "ok": bool(ui_manifest.get("forms")) and bool(ui_manifest.get("wizards")) and bool(ui_manifest.get("controls")),
        },
        {"id": "seed_bundle_present", "ok": seed_manifest["ok"]},
        {"id": "route_contracts_valid", "ok": route_manifest["ok"] and route_validation["ok"]},
        {"id": "permissions_match_runtime", "ok": permission_manifest["ok"] and bool(permission_manifest["action_permissions"])},
        {"id": "repo_gate_pbc_spec_source_audit", "ok": gate_results["pbc_spec_source_audit"]},
        {"id": "repo_gate_pbc_implementation_release_audit", "ok": gate_results["pbc_implementation_release_audit"]},
        {"id": "repo_gate_pbc_generation_smoke_audit", "ok": gate_results["pbc_generation_smoke_audit"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.loyalty-rewards-release-evidence.v2",
        "ok": not blocking_gaps,
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema_contract.build_schema_contract(),
        "service": service_contract.build_service_contract(),
        "api": route_manifest,
        "permissions": permission_manifest,
        "events": event_manifest,
        "ui": ui_manifest,
        "agent": agent_manifest,
        "models": models.model_manifest(),
        "seed": seed_manifest,
        "runtime_smoke": loyalty_rewards_runtime_smoke(),
        "standalone_smoke": standalone_smoke,
        "artifact_status": artifact_status,
        "repo_gate_results": gate_results,
        "service_manifest": service_manifest,
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "events", "ui", "agent", "models", "seed")
        if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence["ok"] and bool(evidence["checks"]),
        "pbc": PBC_KEY,
        "format": evidence["format"],
        "sections": sections,
        "checks": tuple(evidence["checks"]),
        "blocking_gaps": tuple(evidence["blocking_gaps"]),
        "required_sections": ("schema", "service", "api", "permissions", "events", "ui", "agent", "models", "seed"),
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
            ("api_shared_table_access", evidence["api"].get("ok") is not True),
            (
                "missing_repo_gate_result",
                set(evidence["repo_gate_results"]) != {
                    "pbc_spec_source_audit",
                    "pbc_implementation_release_audit",
                    "pbc_generation_smoke_audit",
                },
            ),
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
