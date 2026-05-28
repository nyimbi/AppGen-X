"""UI fragments for the revenue_recognition PBC."""
PBC_KEY = 'revenue_recognition'
UI_FRAGMENTS = ('RevenueRecognitionWorkbench', 'RevenueRecognitionDetail', 'RevenueRecognitionAssistantPanel')


def revenue_recognition_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('revenue_recognition.read', 'revenue_recognition.create', 'revenue_recognition.update', 'revenue_recognition.approve', 'revenue_recognition.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def revenue_recognition_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('revenue_recognition.read', 'revenue_recognition.create', 'revenue_recognition.update', 'revenue_recognition.approve', 'revenue_recognition.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': revenue_recognition_ui_contract()['ok'] and revenue_recognition_render_workbench()['ok'], 'side_effects': ()}
