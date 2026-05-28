"""UI fragments for the professional_services_automation PBC."""
PBC_KEY = 'professional_services_automation'
UI_FRAGMENTS = ('ProfessionalServicesAutomationWorkbench', 'ProfessionalServicesAutomationDetail', 'ProfessionalServicesAutomationAssistantPanel')


def professional_services_automation_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('professional_services_automation.read', 'professional_services_automation.create', 'professional_services_automation.update', 'professional_services_automation.approve', 'professional_services_automation.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def professional_services_automation_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('professional_services_automation.read', 'professional_services_automation.create', 'professional_services_automation.update', 'professional_services_automation.approve', 'professional_services_automation.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': professional_services_automation_ui_contract()['ok'] and professional_services_automation_render_workbench()['ok'], 'side_effects': ()}
