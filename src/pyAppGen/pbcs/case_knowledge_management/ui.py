"""UI fragments for the case_knowledge_management PBC."""
PBC_KEY = 'case_knowledge_management'
UI_FRAGMENTS = ('CaseKnowledgeManagementWorkbench', 'CaseKnowledgeManagementDetail', 'CaseKnowledgeManagementAssistantPanel')


def case_knowledge_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('case_knowledge_management.read', 'case_knowledge_management.create', 'case_knowledge_management.update', 'case_knowledge_management.approve', 'case_knowledge_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def case_knowledge_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('case_knowledge_management.read', 'case_knowledge_management.create', 'case_knowledge_management.update', 'case_knowledge_management.approve', 'case_knowledge_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': case_knowledge_management_ui_contract()['ok'] and case_knowledge_management_render_workbench()['ok'], 'side_effects': ()}
