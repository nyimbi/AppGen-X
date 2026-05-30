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
