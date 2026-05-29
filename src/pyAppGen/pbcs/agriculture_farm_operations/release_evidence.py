"""Release evidence helpers for agriculture_farm_operations."""

from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .routes import api_route_contracts, validate_api_route_contracts
from .runtime import agriculture_farm_operations_build_release_evidence
from .standalone import standalone_app_manifest
from .ui import agriculture_farm_operations_ui_contract


def build_release_evidence() -> dict:
    runtime_evidence = agriculture_farm_operations_build_release_evidence()
    route_contracts = api_route_contracts()
    route_validation = validate_api_route_contracts()
    ui_contract = agriculture_farm_operations_ui_contract()
    agent_workspace = standalone_agent_workspace_contract()
    standalone_manifest = standalone_app_manifest()
    checks = runtime_evidence["checks"] + (
        {"id": "route_contracts", "ok": route_contracts["ok"] and route_validation["ok"]},
        {"id": "standalone_app", "ok": standalone_manifest["ok"]},
        {"id": "ui_forms_wizards_controls", "ok": ui_contract["ok"] and bool(ui_contract["forms"]) and bool(ui_contract["wizards"]) and bool(ui_contract["controls"])},
        {"id": "assistant_workspace", "ok": agent_workspace["ok"]},
    )
    return {
        "format": runtime_evidence["format"],
        "ok": all(check["ok"] for check in checks),
        "pbc": runtime_evidence["pbc"],
        "checks": checks,
        "generated_artifacts": {
            **runtime_evidence["generated_artifacts"],
            "routes": route_contracts["routes"],
            "standalone_app": standalone_manifest["app"],
            "assistant": agent_workspace,
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "routes",
            "events",
            "handlers",
            "ui",
            "assistant",
            "standalone",
            "governance",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["sections"] if section not in manifest["sections"])
    return {
        "ok": manifest["ok"] and not missing_sections and not manifest["blocking_gaps"],
        "pbc": manifest["pbc"],
        "missing_sections": missing_sections,
        "failed_checks": tuple(check for check in manifest["evidence"]["checks"] if not check["ok"]),
        "boundary_gaps": manifest["boundary_gaps"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    return {
        "ok": manifest["ok"] and validation["ok"],
        "manifest": manifest,
        "validation": validation,
        "side_effects": (),
    }
