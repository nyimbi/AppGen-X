"""Workbench UI surface for real estate property management."""
from .standalone import real_estate_property_management_ui_contract as _real_estate_property_management_ui_contract
from .standalone import real_estate_property_management_render_workbench as _real_estate_property_management_render_workbench


def real_estate_property_management_ui_contract():
    contract = _real_estate_property_management_ui_contract()
    contract['configuration_editor'] = True
    contract['stream_engine_picker_visible'] = False
    contract.setdefault('action_permissions', ('real_estate_property_management.read', 'real_estate_property_management.create', 'real_estate_property_management.update', 'real_estate_property_management.approve', 'real_estate_property_management.admin'))
    return contract


def real_estate_property_management_render_workbench():
    return _real_estate_property_management_render_workbench()


def smoke_test():
    rendered = real_estate_property_management_render_workbench()
    return {'ok': real_estate_property_management_ui_contract()['ok'] and rendered['ok'] and 'queues' in rendered, 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': real_estate_property_management_ui_contract()['action_permissions'], 'side_effects': ()}

# Improve1 real estate property management control UI extension.
from .real_estate_property_management_control import improve1_real_estate_property_management_control_contract as _improve1_real_estate_property_management_control_contract

_REAL_ESTATE_CONTROL_BASE_UI_CONTRACT = real_estate_property_management_ui_contract
_REAL_ESTATE_CONTROL_BASE_RENDER_WORKBENCH = real_estate_property_management_render_workbench


def real_estate_property_management_ui_contract() -> dict:
    ui = dict(_REAL_ESTATE_CONTROL_BASE_UI_CONTRACT())
    control = _improve1_real_estate_property_management_control_contract()
    ui.update({
        "ok": ui.get("ok") is True and control["ok"],
        "real_estate_property_management_control_contract": control,
        "real_estate_property_management_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "real_estate_property_management_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "stream_engine_picker_visible": False,
    })
    return ui


def real_estate_property_management_render_workbench(*args, **kwargs) -> dict:
    workbench = dict(_REAL_ESTATE_CONTROL_BASE_RENDER_WORKBENCH(*args, **kwargs))
    control = _improve1_real_estate_property_management_control_contract()
    workbench.update({
        "ok": workbench.get("ok") is True and control["ok"],
        "real_estate_property_management_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "real_estate_property_management_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "real_estate_property_management_control_agent_tools": tuple(f"real_estate_property_management.skills.{item['slug']}" for item in control["capabilities"]),
    })
    return workbench
