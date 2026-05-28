"""UI fragments for the case_knowledge_management PBC."""
PBC_KEY = 'case_knowledge_management'
UI_FRAGMENTS = ('CaseKnowledgeManagementWorkbench', 'CaseKnowledgeManagementDetail', 'CaseKnowledgeManagementAssistantPanel')


def case_knowledge_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('case_knowledge_management.read', 'case_knowledge_management.create', 'case_knowledge_management.update', 'case_knowledge_management.approve', 'case_knowledge_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def case_knowledge_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('case_knowledge_management.read', 'case_knowledge_management.create', 'case_knowledge_management.update', 'case_knowledge_management.approve', 'case_knowledge_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': case_knowledge_management_ui_contract()['ok'] and case_knowledge_management_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as case_knowledge_management_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as case_knowledge_management_domain_capability_surface_contract

_BASE_CASE_KNOWLEDGE_MANAGEMENT_UI_CONTRACT = case_knowledge_management_ui_contract
_BASE_CASE_KNOWLEDGE_MANAGEMENT_RENDER_WORKBENCH = case_knowledge_management_render_workbench


def case_knowledge_management_ui_contract():
    base = dict(_BASE_CASE_KNOWLEDGE_MANAGEMENT_UI_CONTRACT())
    full = case_knowledge_management_ui_capability_surface_contract()
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


def case_knowledge_management_render_workbench(state=None):
    base = dict(_BASE_CASE_KNOWLEDGE_MANAGEMENT_RENDER_WORKBENCH(state=state))
    full = case_knowledge_management_ui_capability_surface_contract()
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
