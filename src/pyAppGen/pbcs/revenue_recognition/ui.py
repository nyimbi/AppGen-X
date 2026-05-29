"""UI fragments for the revenue_recognition PBC."""
PBC_KEY = 'revenue_recognition'
UI_FRAGMENTS = ('RevenueRecognitionWorkbench', 'RevenueRecognitionDetail', 'RevenueRecognitionAssistantPanel')


def revenue_recognition_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('revenue_recognition.read', 'revenue_recognition.create', 'revenue_recognition.update', 'revenue_recognition.approve', 'revenue_recognition.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def revenue_recognition_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('revenue_recognition.read', 'revenue_recognition.create', 'revenue_recognition.update', 'revenue_recognition.approve', 'revenue_recognition.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': revenue_recognition_ui_contract()['ok'] and revenue_recognition_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as revenue_recognition_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as revenue_recognition_domain_capability_surface_contract

_BASE_REVENUE_RECOGNITION_UI_CONTRACT = revenue_recognition_ui_contract
_BASE_REVENUE_RECOGNITION_RENDER_WORKBENCH = revenue_recognition_render_workbench


def revenue_recognition_ui_contract():
    base = dict(_BASE_REVENUE_RECOGNITION_UI_CONTRACT())
    full = revenue_recognition_ui_capability_surface_contract()
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


def revenue_recognition_render_workbench(state=None):
    base = dict(_BASE_REVENUE_RECOGNITION_RENDER_WORKBENCH(state=state))
    full = revenue_recognition_ui_capability_surface_contract()
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


from .app_surface import (
    revenue_recognition_controls_contract,
    revenue_recognition_forms_contract,
    revenue_recognition_wizards_contract,
    single_pbc_revenue_recognition_app_contract,
)

_BASE_REVENUE_RECOGNITION_UI_CONTRACT_WITH_DEPTH = revenue_recognition_ui_contract
_BASE_REVENUE_RECOGNITION_RENDER_WORKBENCH_WITH_DEPTH = revenue_recognition_render_workbench

def revenue_recognition_ui_contract():
    base = dict(_BASE_REVENUE_RECOGNITION_UI_CONTRACT_WITH_DEPTH())
    return {
        **base,
        'forms_contract': revenue_recognition_forms_contract(),
        'wizards_contract': revenue_recognition_wizards_contract(),
        'controls_contract': revenue_recognition_controls_contract(),
        'single_pbc_app': single_pbc_revenue_recognition_app_contract(),
    }

def revenue_recognition_render_workbench(state=None):
    base = dict(_BASE_REVENUE_RECOGNITION_RENDER_WORKBENCH_WITH_DEPTH(state=state))
    return {**base, 'single_pbc_app': single_pbc_revenue_recognition_app_contract(state=state)}

def smoke_test():
    contract = revenue_recognition_ui_contract()
    workbench = revenue_recognition_render_workbench()
    return {'ok': contract['ok'] and workbench['ok'] and contract['single_pbc_app']['ok'], 'contract': contract, 'workbench': workbench, 'side_effects': ()}
