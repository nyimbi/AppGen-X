"""UI fragments for the sustainability_esg_reporting PBC."""
PBC_KEY = 'sustainability_esg_reporting'
UI_FRAGMENTS = ('SustainabilityEsgReportingWorkbench', 'SustainabilityEsgReportingDetail', 'SustainabilityEsgReportingAssistantPanel')


def sustainability_esg_reporting_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('sustainability_esg_reporting.read', 'sustainability_esg_reporting.create', 'sustainability_esg_reporting.update', 'sustainability_esg_reporting.approve', 'sustainability_esg_reporting.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def sustainability_esg_reporting_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('sustainability_esg_reporting.read', 'sustainability_esg_reporting.create', 'sustainability_esg_reporting.update', 'sustainability_esg_reporting.approve', 'sustainability_esg_reporting.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': sustainability_esg_reporting_ui_contract()['ok'] and sustainability_esg_reporting_render_workbench()['ok'], 'side_effects': ()}
