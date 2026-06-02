from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'utilities_metering_billing'

def utilities_metering_billing_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('UtilitiesMeteringBillingWorkbench',
 'UtilitiesMeteringBillingDetail',
 'UtilitiesMeteringBillingAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('utilities_metering_billing.read',
 'utilities_metering_billing.create',
 'utilities_metering_billing.update',
 'utilities_metering_billing.approve',
 'utilities_metering_billing.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def utilities_metering_billing_render_workbench():
    ui = utilities_metering_billing_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def smoke_test():
    return {'ok': utilities_metering_billing_ui_contract()['ok'] and utilities_metering_billing_render_workbench()['ok'], 'side_effects': ()}


# Improve1 utilities metering billing control UI extension.
from .utilities_metering_billing_control import improve1_utilities_metering_billing_control_contract as _improve1_utilities_metering_billing_control_contract

_UTILITY_CONTROL_BASE_UI_CONTRACT = utilities_metering_billing_ui_contract
_UTILITY_CONTROL_BASE_RENDER_WORKBENCH = utilities_metering_billing_render_workbench


def utilities_metering_billing_ui_contract() -> dict:
    ui = dict(_UTILITY_CONTROL_BASE_UI_CONTRACT())
    control = _improve1_utilities_metering_billing_control_contract()
    ui.update({
        "ok": ui.get("ok") is True and control["ok"],
        "utilities_metering_billing_control_contract": control,
        "utilities_metering_billing_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "utilities_metering_billing_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "stream_engine_picker_visible": False,
    })
    return ui


def utilities_metering_billing_render_workbench(*args, **kwargs) -> dict:
    workbench = dict(_UTILITY_CONTROL_BASE_RENDER_WORKBENCH(*args, **kwargs))
    control = _improve1_utilities_metering_billing_control_contract()
    workbench.update({
        "ok": workbench.get("ok") is True and control["ok"],
        "utilities_metering_billing_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "utilities_metering_billing_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "utilities_metering_billing_control_agent_tools": tuple(f"utilities_metering_billing.skills.{item['slug']}" for item in control["capabilities"]),
    })
    return workbench
