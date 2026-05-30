"""UI contracts for the standalone master_data_governance slice."""
from __future__ import annotations

from .standalone import CONTROL_KEYS
from .standalone import FORM_KEYS
from .standalone import WIZARD_KEYS
from .standalone import master_data_governance_control_catalog
from .standalone import master_data_governance_form_contracts
from .standalone import master_data_governance_render_standalone_workbench
from .standalone import master_data_governance_standalone_workbench_blueprint
from .standalone import master_data_governance_wizard_contracts

PBC_KEY = "master_data_governance"
UI_FRAGMENTS = (
    "MasterDataGovernanceWorkbench",
    "MasterDataGovernanceDetail",
    "MasterDataGovernanceAssistantPanel",
)


def master_data_governance_ui_contract() -> dict:
    shell = master_data_governance_standalone_workbench_blueprint()
    return {
        "format": f"appgen.{PBC_KEY}.ui-contract.v1",
        "ok": shell["ok"],
        "pbc": PBC_KEY,
        "fragments": UI_FRAGMENTS,
        "forms": FORM_KEYS,
        "wizards": WIZARD_KEYS,
        "controls": CONTROL_KEYS,
        "routes": shell["routes"],
        "panels": shell["panels"],
        "navigation": shell["navigation"],
        "workbench_view": UI_FRAGMENTS[0],
        "configuration_editor": True,
        "action_permissions": (
            f"{PBC_KEY}.read",
            f"{PBC_KEY}.create",
            f"{PBC_KEY}.update",
            f"{PBC_KEY}.approve",
            f"{PBC_KEY}.admin",
            f"{PBC_KEY}.audit",
        ),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def master_data_governance_render_workbench(state: dict | None = None):
    return master_data_governance_render_standalone_workbench(state or {"tenant": "default", "summary": {}, "queues": {}, "records": {}})


def smoke_test():
    shell = master_data_governance_standalone_workbench_blueprint()
    forms = master_data_governance_form_contracts()
    wizards = master_data_governance_wizard_contracts()
    controls = master_data_governance_control_catalog()
    rendered = master_data_governance_render_workbench({"tenant": "tenant_smoke", "summary": {}, "queues": {}, "records": {}})
    return {
        "ok": shell["ok"] and forms["ok"] and wizards["ok"] and controls["ok"] and rendered["ok"],
        "shell": shell,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "rendered": rendered,
        "side_effects": (),
    }


# Improve1 master data control UI extension.
from .master_data_control import improve1_master_data_control_contract as _improve1_master_data_control_contract

_MASTER_DATA_GOVERNANCE_BASE_UI_CONTRACT = master_data_governance_ui_contract
_MASTER_DATA_GOVERNANCE_BASE_RENDER_WORKBENCH = master_data_governance_render_workbench


def master_data_governance_ui_contract():
    ui = dict(_MASTER_DATA_GOVERNANCE_BASE_UI_CONTRACT())
    control = _improve1_master_data_control_contract()
    panels = tuple(item["evidence"]["ui_surface"] for item in control["capabilities"])
    service_actions = tuple(item["evidence"]["service_api"] for item in control["capabilities"])
    ui.update({
        "ok": ui.get("ok") is True and control["ok"],
        "master_data_control_contract": control,
        "master_data_control_panels": panels,
        "master_data_control_service_actions": service_actions,
        "stream_engine_picker_visible": False,
    })
    return ui


def master_data_governance_render_workbench(state: dict | None = None):
    workbench = dict(_MASTER_DATA_GOVERNANCE_BASE_RENDER_WORKBENCH(state))
    control = _improve1_master_data_control_contract()
    workbench.update({
        "ok": workbench.get("ok") is True and control["ok"],
        "master_data_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "master_data_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "master_data_control_agent_tools": tuple(f"master_data_governance.skills.{item['slug']}" for item in control["capabilities"]),
    })
    return workbench
