from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'telecom_subscription_lifecycle'

def telecom_subscription_lifecycle_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('TelecomSubscriptionLifecycleWorkbench',
 'TelecomSubscriptionLifecycleDetail',
 'TelecomSubscriptionLifecycleAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('telecom_subscription_lifecycle.read',
 'telecom_subscription_lifecycle.create',
 'telecom_subscription_lifecycle.update',
 'telecom_subscription_lifecycle.approve',
 'telecom_subscription_lifecycle.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def telecom_subscription_lifecycle_render_workbench():
    ui = telecom_subscription_lifecycle_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def smoke_test():
    return {'ok': telecom_subscription_lifecycle_ui_contract()['ok'] and telecom_subscription_lifecycle_render_workbench()['ok'], 'side_effects': ()}


# Improve1 telecom subscription lifecycle control UI extension.
from .telecom_subscription_lifecycle_control import improve1_telecom_subscription_lifecycle_control_contract as _improve1_telecom_subscription_lifecycle_control_contract

_SUBSCRIPTION_CONTROL_BASE_UI_CONTRACT = telecom_subscription_lifecycle_ui_contract
_SUBSCRIPTION_CONTROL_BASE_RENDER_WORKBENCH = telecom_subscription_lifecycle_render_workbench


def telecom_subscription_lifecycle_ui_contract() -> dict:
    ui = dict(_SUBSCRIPTION_CONTROL_BASE_UI_CONTRACT())
    control = _improve1_telecom_subscription_lifecycle_control_contract()
    ui.update({
        "ok": ui.get("ok") is True and control["ok"],
        "telecom_subscription_lifecycle_control_contract": control,
        "telecom_subscription_lifecycle_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "telecom_subscription_lifecycle_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "stream_engine_picker_visible": False,
    })
    return ui


def telecom_subscription_lifecycle_render_workbench(*args, **kwargs) -> dict:
    workbench = dict(_SUBSCRIPTION_CONTROL_BASE_RENDER_WORKBENCH(*args, **kwargs))
    control = _improve1_telecom_subscription_lifecycle_control_contract()
    workbench.update({
        "ok": workbench.get("ok") is True and control["ok"],
        "telecom_subscription_lifecycle_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "telecom_subscription_lifecycle_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "telecom_subscription_lifecycle_control_agent_tools": tuple(f"telecom_subscription_lifecycle.skills.{item['slug']}" for item in control["capabilities"]),
    })
    return workbench
