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


def smoke_test():
    view = construction_contracts_commercials_build_workbench_view()
    rendered = construction_contracts_commercials_render_workbench()
    contract = construction_contracts_commercials_ui_contract()
    return {"ok": contract["ok"] and view["ok"] and rendered["ok"], "side_effects": ()}
