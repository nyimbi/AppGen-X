"""Focused standalone audit helpers for court_case_management."""
from __future__ import annotations

from . import agent
from . import runtime
from . import services
from . import standalone
from . import ui


def run_court_case_management_pbc_audit() -> dict:
    standalone_smoke = standalone.standalone_smoke_test()
    implementation = standalone.pbc_implementation_release_audit()
    generation = standalone.pbc_generation_smoke_audit()
    docs = standalone.documentation_presence()
    service_manifest = services.standalone_service_manifest()
    ui_contract = ui.court_case_management_ui_contract()
    agent_manifest = agent.agent_skill_manifest()
    boundary = runtime.court_case_management_verify_owned_table_boundary(runtime.COURT_CASE_MANAGEMENT_OWNED_TABLES)
    checks = (
        {"id": "standalone_smoke", "ok": standalone_smoke["ok"]},
        {"id": "implementation_audit", "ok": implementation["ok"]},
        {"id": "generation_audit", "ok": generation["ok"]},
        {"id": "documentation_present", "ok": docs["ok"]},
        {"id": "service_methods_present", "ok": service_manifest["ok"] and len(service_manifest["service_methods"]) >= 12},
        {"id": "ui_forms_wizards_controls", "ok": bool(ui_contract.get("forms")) and bool(ui_contract.get("wizards")) and bool(ui_contract.get("controls"))},
        {"id": "agent_document_intake", "ok": agent_manifest["ok"] and len(agent_manifest["skills"]) >= 3},
        {"id": "owned_boundary_clean", "ok": boundary["ok"]},
    )
    return {
        "format": "appgen.court_case_management.package-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": "court_case_management",
        "checks": checks,
        "standalone": standalone_smoke,
        "implementation": implementation,
        "generation": generation,
        "docs": docs,
        "boundary": boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    audit = run_court_case_management_pbc_audit()
    return {"ok": audit["ok"], "audit": audit, "side_effects": ()}
