from __future__ import annotations

from .core import (
    PBC_KEY,
    construction_contracts_commercials_build_workbench_view,
    construction_contracts_commercials_render_workbench as _construction_contracts_commercials_render_workbench,
    construction_contracts_commercials_ui_contract as _construction_contracts_commercials_ui_contract,
)


def construction_contracts_commercials_ui_contract():
    contract = _construction_contracts_commercials_ui_contract()
    return {
        **contract,
        "configuration_editor": contract.get("configuration_editor", {"event_contract": "AppGen-X"}),
        "stream_engine_picker_visible": False,
        "action_permissions": contract.get("action_permissions", {}),
    }


def construction_contracts_commercials_render_workbench(state=None, tenant="default"):
    rendered = _construction_contracts_commercials_render_workbench(state=state, tenant=tenant)
    return {**rendered, "pbc": PBC_KEY}


def construction_contracts_commercials_standalone_workbench_blueprint():
    contract = construction_contracts_commercials_ui_contract()
    return {
        "format": "appgen.construction-contracts-commercials-standalone-workbench.v1",
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "forms": ("contract_award_wizard", "pay_application_certification_wizard", "lien_waiver_review_form"),
        "views": ("contracts", "pay_applications", "retainage", "claims", "workbench"),
        "agent_panel": "ConstructionContractsCommercialsAssistantPanel",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def construction_contracts_commercials_render_standalone_workbench(workbench):
    return {
        "format": "appgen.construction-contracts-commercials-standalone-workbench-render.v1",
        "ok": bool(workbench.get("ok", True)),
        "pbc": PBC_KEY,
        "cards": tuple((workbench.get("result") or workbench).get("cards", ())),
        "queues": (workbench.get("result") or workbench).get("queues", {}),
        "source": workbench,
        "side_effects": (),
    }


def smoke_test():
    view = construction_contracts_commercials_build_workbench_view()
    rendered = construction_contracts_commercials_render_workbench()
    contract = construction_contracts_commercials_ui_contract()
    return {"ok": contract["ok"] and view["ok"] and rendered["ok"], "side_effects": ()}
