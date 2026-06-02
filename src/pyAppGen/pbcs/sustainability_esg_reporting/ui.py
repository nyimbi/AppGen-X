"""UI fragments for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import PBC_KEY
from .slice_app import build_standalone_app, build_ui_contract

UI_FRAGMENTS = tuple(build_ui_contract()['fragments'])


def sustainability_esg_reporting_ui_contract() -> dict:
    return build_ui_contract()


def sustainability_esg_reporting_render_workbench(state: dict | None = None) -> dict:
    tenant = (state or {}).get('tenant', 'default')
    limit = (state or {}).get('limit', 10)
    app = build_standalone_app()
    workbench = app.build_workbench_view(tenant=tenant, limit=limit)
    return {
        'ok': workbench['ok'],
        'pbc': PBC_KEY,
        'view': workbench['view'],
        'panels': workbench['panels'],
        'forms': workbench['forms'],
        'wizards': workbench['wizards'],
        'controls': workbench['controls'],
        'summary': workbench['summary'],
        'configuration_editor': True,
        'stream_engine_picker_visible': False,
        'action_permissions': tuple(build_ui_contract()['action_permissions']),
        'advanced_panels': tuple(build_ui_contract()['advanced_panels']),
        'agent_tools': tuple(build_ui_contract()['agent_tools']),
        'side_effects': (),
    }


def smoke_test() -> dict:
    contract = sustainability_esg_reporting_ui_contract()
    workbench = sustainability_esg_reporting_render_workbench({'tenant': 'tenant-smoke'})
    return {'ok': contract['ok'] and workbench['ok'] and bool(workbench['forms']) and bool(workbench['wizards']) and bool(workbench['controls']), 'contract': contract, 'workbench': workbench, 'side_effects': ()}


# Improve1 sustainability ESG reporting control UI extension.
from .sustainability_esg_reporting_control import improve1_sustainability_esg_reporting_control_contract as _improve1_sustainability_esg_reporting_control_contract

_ESG_CONTROL_BASE_UI_CONTRACT = sustainability_esg_reporting_ui_contract
_ESG_CONTROL_BASE_RENDER_WORKBENCH = sustainability_esg_reporting_render_workbench


def sustainability_esg_reporting_ui_contract() -> dict:
    ui = dict(_ESG_CONTROL_BASE_UI_CONTRACT())
    control = _improve1_sustainability_esg_reporting_control_contract()
    ui.update({
        "ok": ui.get("ok") is True and control["ok"],
        "sustainability_esg_reporting_control_contract": control,
        "sustainability_esg_reporting_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "sustainability_esg_reporting_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "stream_engine_picker_visible": False,
    })
    return ui


def sustainability_esg_reporting_render_workbench(*args, **kwargs) -> dict:
    workbench = dict(_ESG_CONTROL_BASE_RENDER_WORKBENCH(*args, **kwargs))
    control = _improve1_sustainability_esg_reporting_control_contract()
    workbench.update({
        "ok": workbench.get("ok") is True and control["ok"],
        "sustainability_esg_reporting_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "sustainability_esg_reporting_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "sustainability_esg_reporting_control_agent_tools": tuple(f"sustainability_esg_reporting.skills.{item['slug']}" for item in control["capabilities"]),
    })
    return workbench
