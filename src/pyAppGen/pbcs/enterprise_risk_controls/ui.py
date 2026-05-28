"""UI fragments for the enterprise_risk_controls PBC."""
PBC_KEY = 'enterprise_risk_controls'
UI_FRAGMENTS = ('EnterpriseRiskControlsWorkbench', 'EnterpriseRiskControlsDetail', 'EnterpriseRiskControlsAssistantPanel')


def enterprise_risk_controls_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('enterprise_risk_controls.read', 'enterprise_risk_controls.create', 'enterprise_risk_controls.update', 'enterprise_risk_controls.approve', 'enterprise_risk_controls.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def enterprise_risk_controls_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('enterprise_risk_controls.read', 'enterprise_risk_controls.create', 'enterprise_risk_controls.update', 'enterprise_risk_controls.approve', 'enterprise_risk_controls.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': enterprise_risk_controls_ui_contract()['ok'] and enterprise_risk_controls_render_workbench()['ok'], 'side_effects': ()}
