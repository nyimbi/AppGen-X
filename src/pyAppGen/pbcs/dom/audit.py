"""Package-local audit helpers for the DOM standalone PBC."""

from __future__ import annotations

from . import agent
from . import runtime
from . import services
from . import standalone
from . import ui


def run_dom_pbc_audit() -> dict:
    standalone_smoke = standalone.standalone_smoke_test()
    service_manifest = services.standalone_service_manifest()
    ui_contract = ui.dom_ui_contract()
    agent_manifest = agent.agent_skill_manifest()
    docs = standalone.documentation_presence()
    boundary = runtime.dom_verify_owned_table_boundary(("sales_order", "dom_appgen_outbox_event"))
    checks = (
        {"id": "standalone_smoke", "ok": standalone_smoke["ok"]},
        {"id": "service_methods_present", "ok": service_manifest["ok"] and len(service_manifest["service_methods"]) >= 12},
        {"id": "ui_forms_wizards_controls", "ok": bool(ui_contract.get("forms")) and bool(ui_contract.get("wizards")) and bool(ui_contract.get("controls"))},
        {"id": "agent_document_intake", "ok": agent_manifest["ok"] and agent_manifest["skills"]},
        {"id": "documentation_present", "ok": docs["ok"]},
        {"id": "owned_boundary_clean", "ok": boundary["ok"]},
        {"id": "fixed_event_contract", "ok": service_manifest["event_contract"] == "AppGen-X" and service_manifest["event_topic"] == runtime.DOM_REQUIRED_EVENT_TOPIC},
    )
    return {
        "format": "appgen.dom-package-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": "dom",
        "checks": checks,
        "standalone": standalone_smoke,
        "service": service_manifest,
        "ui": {
            "forms": tuple(ui_contract.get("forms", {})),
            "wizards": tuple(ui_contract.get("wizards", {})),
            "controls": tuple(ui_contract.get("controls", {})),
        },
        "agent": {
            "skills": tuple(item["name"] for item in agent_manifest["skills"]),
            "document_actions": tuple(agent_manifest["skills"][0]["document_actions"]) if agent_manifest["skills"] else (),
        },
        "docs": docs,
        "boundary": boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    audit = run_dom_pbc_audit()
    return {
        "ok": audit["ok"],
        "audit": audit,
        "side_effects": (),
    }
