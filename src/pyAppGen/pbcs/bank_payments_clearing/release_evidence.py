"""Executable release evidence for bank_payments_clearing."""

from __future__ import annotations

from pathlib import Path

from . import agent, capability_assurance, events, handlers, permissions, routes, seed_data, standalone, ui
from .manifest import PBC_MANIFEST
from .models import database_model_contract, model_manifest
from .runtime import bank_payments_clearing_runtime_smoke
from .schema_contract import build_schema_contract, validate_schema_contract
from .service_contract import build_service_contract, validate_service_contract


PBC_KEY = "bank_payments_clearing"
PACKAGE_DIR = Path(__file__).resolve().parent


def _artifact_paths() -> tuple[dict, ...]:
    artifacts = (
        "README.md",
        "SPECIFICATION.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
        "standalone.py",
        "migrations/001_initial.sql",
        "tests/test_contract.py",
        "tests/test_payment_operations.py",
        "tests/test_standalone.py",
    )
    return tuple(
        {
            "artifact": artifact,
            "exists": (PACKAGE_DIR / artifact).exists(),
        }
        for artifact in artifacts
    )


def build_release_evidence() -> dict:
    runtime_smoke = bank_payments_clearing_runtime_smoke()
    schema = build_schema_contract()
    service = build_service_contract()
    api = routes.api_route_contracts()
    event_manifest = events.event_contract_manifest()
    handler_manifest = handlers.handler_manifest()
    ui_manifest = ui.bank_payments_clearing_ui_contract()
    single_pbc_app = ui.bank_payments_clearing_single_pbc_app_contract()
    agent_manifest = agent.composed_agent_contribution()
    model_contract = database_model_contract()
    standalone_smoke = standalone.workbench_smoke_test()
    artifact_status = _artifact_paths()
    gate_results = {
        "pbc_source_artifact_contract": all(item["exists"] for item in artifact_status)
        and validate_schema_contract()["ok"]
        and model_manifest()["ok"],
        "pbc_implementation_release_audit": validate_service_contract()["ok"]
        and api["ok"]
        and event_manifest["ok"]
        and handler_manifest["ok"]
        and ui_manifest["ok"]
        and permissions.permission_manifest()["ok"]
        and seed_data.validate_seed_data()["ok"],
        "pbc_generation_smoke_audit": runtime_smoke["ok"]
        and standalone_smoke["ok"]
        and capability_assurance.smoke_test()["ok"]
        and agent.smoke_test()["ok"],
    }
    checks = tuple(runtime_smoke["checks"]) + (
        {"id": "package_artifacts_present", "ok": all(item["exists"] for item in artifact_status)},
        {"id": "agent_surface_present", "ok": agent_manifest["ok"]},
        {"id": "ui_forms_wizards_controls_present", "ok": bool(ui_manifest["forms"]) and bool(ui_manifest["wizards"]) and bool(ui_manifest["controls"])},
        {"id": "payment_operations_execution", "ok": runtime_smoke["payment_operations"]["ok"]},
        {"id": "single_pbc_app_forms_wizards_controls", "ok": single_pbc_app["ok"]},
        {"id": "standalone_app_surface_present", "ok": standalone_smoke["ok"]},
        {"id": "repo_gate_pbc_source_artifact_contract", "ok": gate_results["pbc_source_artifact_contract"]},
        {"id": "repo_gate_pbc_implementation_release_audit", "ok": gate_results["pbc_implementation_release_audit"]},
        {"id": "repo_gate_pbc_generation_smoke_audit", "ok": gate_results["pbc_generation_smoke_audit"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.bank-payments-clearing-release-evidence.v2",
        "ok": not blocking_gaps,
        "pbc": PBC_KEY,
        "manifest": PBC_MANIFEST,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions.permission_manifest(),
        "events": event_manifest,
        "handlers": handler_manifest,
        "ui": ui_manifest,
        "single_pbc_app": single_pbc_app,
        "agent": agent_manifest,
        "models": model_contract,
        "runtime_smoke": runtime_smoke,
        "standalone_smoke": standalone_smoke,
        "artifact_status": artifact_status,
        "repo_gate_results": gate_results,
        "side_effects": (),
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "events", "handlers", "ui", "agent", "models")
        if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence["ok"] and bool(evidence["checks"]),
        "pbc": evidence["pbc"],
        "format": evidence["format"],
        "sections": sections,
        "checks": tuple(evidence["checks"]),
        "blocking_gaps": tuple(evidence["blocking_gaps"]),
        "required_sections": ("schema", "service", "api", "events", "handlers", "ui", "agent", "models"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(
        section for section in manifest["required_sections"] if section not in manifest["sections"]
    )
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", evidence["schema"].get("shared_table_access") is not False),
            ("service_shared_table_access", evidence["service"].get("shared_table_access") is not False),
            ("api_shared_table_access", evidence["api"].get("shared_table_access") is not False),
            (
                "missing_repo_gate_result",
                set(evidence["repo_gate_results"]) != {
                    "pbc_source_artifact_contract",
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
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
