"""Focused package audits for sports_venue_event_operations."""

from __future__ import annotations

from pathlib import Path

from . import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from . import agent, capability_assurance, release_evidence, routes, services, standalone, ui
from .runtime import sports_venue_event_operations_runtime_capabilities, sports_venue_event_operations_verify_owned_table_boundary


def run_source_audit() -> dict:
    implementation = implementation_contract()
    discovery = package_discovery_plan()
    metadata = package_metadata_manifest()
    validation = validate_package_metadata()
    checks = (
        {"id": "implementation_contract", "ok": implementation["pbc"] == "sports_venue_event_operations"},
        {"id": "package_discovery", "ok": discovery["ok"]},
        {"id": "package_metadata", "ok": metadata["pbc"] == "sports_venue_event_operations"},
        {"id": "metadata_validation", "ok": validation["ok"]},
    )
    return {"ok": all(check["ok"] for check in checks), "checks": checks, "side_effects": ()}


def run_package_audit() -> dict:
    manifest = standalone.standalone_manifest()
    docs = standalone.documentation_presence()
    checks = (
        {"id": "standalone_manifest", "ok": manifest["ok"]},
        {"id": "docs_present", "ok": docs["ok"]},
        {"id": "appgen_x_only", "ok": manifest["event_contract"] == "AppGen-X"},
        {"id": "allowed_backends", "ok": manifest["allowed_backends"] == ("postgresql", "mysql", "mariadb")},
    )
    return {"ok": all(check["ok"] for check in checks), "checks": checks, "side_effects": ()}


def run_spec_audit() -> dict:
    spec_text = (Path(__file__).resolve().parent / "SPECIFICATION.md").read_text(encoding="utf-8")
    required_phrases = (
        "venue/zone/seat configuration",
        "ingress/egress",
        "weather delays",
        "broadcast/production readiness",
        "forms, wizards, and controls",
        "AppGen-X",
        "PostgreSQL, MySQL, and MariaDB",
    )
    checks = tuple({"id": phrase, "ok": phrase in spec_text} for phrase in required_phrases)
    return {"ok": all(check["ok"] for check in checks), "checks": checks, "side_effects": ()}


def run_agent_audit() -> dict:
    manifest = agent.agent_skill_manifest()
    workspace = agent.standalone_agent_workspace_contract()
    document = agent.document_instruction_plan(
        "Lightning watch and sponsor activation notes",
        "update the weather delay workflow and sponsor readiness plan",
    )
    crud = agent.datastore_crud_plan(
        "update",
        table="sports_venue_event_operations_weather_delay",
        payload={"state": "delay"},
    )
    checks = (
        {"id": "skill_manifest", "ok": manifest["ok"]},
        {"id": "workspace", "ok": workspace["ok"]},
        {"id": "document_preview", "ok": document["ok"] and bool(document["crud_preview"])},
        {"id": "crud_plan", "ok": crud["ok"] and bool(crud["route_candidates"])},
    )
    return {"ok": all(check["ok"] for check in checks), "checks": checks, "side_effects": ()}


def run_implementation_audit() -> dict:
    smoke = standalone.standalone_smoke_test()
    route_smoke = routes.smoke_test()
    service_manifest = services.standalone_service_manifest()
    checks = (
        {"id": "standalone_smoke", "ok": smoke["ok"]},
        {"id": "route_smoke", "ok": route_smoke["ok"]},
        {"id": "service_methods", "ok": service_manifest["ok"] and len(service_manifest["service_methods"]) >= 20},
    )
    return {"ok": all(check["ok"] for check in checks), "checks": checks, "side_effects": ()}


def run_capability_audit() -> dict:
    runtime = sports_venue_event_operations_runtime_capabilities()
    capability = capability_assurance.validate_table_stakes_capability_coverage()
    boundary = sports_venue_event_operations_verify_owned_table_boundary(
        ("sports_venue_event_operations_event_calendar_table", "foreign_table")
    )
    ui_contract = ui.sports_venue_event_operations_ui_contract()
    checks = (
        {"id": "runtime_capabilities", "ok": runtime["ok"]},
        {"id": "table_stakes", "ok": capability["ok"]},
        {"id": "owned_boundary", "ok": boundary["ok"] is False},
        {"id": "ui_surface", "ok": ui_contract["ok"] and bool(ui_contract["forms"])},
    )
    return {"ok": all(check["ok"] for check in checks), "checks": checks, "side_effects": ()}


def run_generation_audit() -> dict:
    evidence = release_evidence.build_release_evidence()
    tests = (
        Path(__file__).resolve().parent / "tests" / "test_contract.py",
        Path(__file__).resolve().parent / "tests" / "test_standalone_app.py",
    )
    checks = (
        {"id": "release_evidence", "ok": evidence["ok"]},
        {"id": "tests_present", "ok": all(path.exists() for path in tests)},
        {"id": "documentation_present", "ok": evidence["documentation"]["ok"]},
    )
    return {"ok": all(check["ok"] for check in checks), "checks": checks, "side_effects": ()}


def run_sports_venue_event_operations_pbc_audit() -> dict:
    audits = {
        "source": run_source_audit(),
        "package": run_package_audit(),
        "spec": run_spec_audit(),
        "agent": run_agent_audit(),
        "implementation": run_implementation_audit(),
        "capability": run_capability_audit(),
        "generation": run_generation_audit(),
    }
    checks = tuple({"id": name, "ok": result["ok"]} for name, result in audits.items())
    return {
        "format": "appgen.sports-venue-event-operations-package-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": "sports_venue_event_operations",
        "checks": checks,
        "audits": audits,
        "side_effects": (),
    }


def smoke_test() -> dict:
    audit = run_sports_venue_event_operations_pbc_audit()
    return {"ok": audit["ok"], "audit": audit, "side_effects": ()}
