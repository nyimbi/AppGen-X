"""UI fragments for the enterprise_risk_controls PBC."""
PBC_KEY = 'enterprise_risk_controls'
UI_FRAGMENTS = ('EnterpriseRiskControlsWorkbench', 'EnterpriseRiskControlsDetail', 'EnterpriseRiskControlsAssistantPanel')


def enterprise_risk_controls_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('enterprise_risk_controls.read', 'enterprise_risk_controls.create', 'enterprise_risk_controls.update', 'enterprise_risk_controls.approve', 'enterprise_risk_controls.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def enterprise_risk_controls_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('enterprise_risk_controls.read', 'enterprise_risk_controls.create', 'enterprise_risk_controls.update', 'enterprise_risk_controls.approve', 'enterprise_risk_controls.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': enterprise_risk_controls_ui_contract()['ok'] and enterprise_risk_controls_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as enterprise_risk_controls_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as enterprise_risk_controls_domain_capability_surface_contract

_BASE_ENTERPRISE_RISK_CONTROLS_UI_CONTRACT = enterprise_risk_controls_ui_contract
_BASE_ENTERPRISE_RISK_CONTROLS_RENDER_WORKBENCH = enterprise_risk_controls_render_workbench


def enterprise_risk_controls_ui_contract():
    base = dict(_BASE_ENTERPRISE_RISK_CONTROLS_UI_CONTRACT())
    full = enterprise_risk_controls_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'full_capability_surface': full,
        'operation_actions': full['operation_actions'],
        'rule_editors': full['rule_editors'],
        'parameter_editors': full['parameter_editors'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'navigation_sections': full['navigation_sections'],
    }


def enterprise_risk_controls_render_workbench(state=None):
    base = dict(_BASE_ENTERPRISE_RISK_CONTROLS_RENDER_WORKBENCH(state=state))
    full = enterprise_risk_controls_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'panels': tuple(dict.fromkeys(tuple(base.get('panels', ())) + full['navigation_sections'])),
        'operation_actions': full['operation_actions'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'agent_tools': full['agent_tools'],
    }
