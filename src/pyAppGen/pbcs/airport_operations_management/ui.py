from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'airport_operations_management'

def airport_operations_management_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('AirportOperationsManagementWorkbench',
 'AirportOperationsManagementDetail',
 'AirportOperationsManagementAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('airport_operations_management.read',
 'airport_operations_management.create',
 'airport_operations_management.update',
 'airport_operations_management.approve',
 'airport_operations_management.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'decision_support_panels': ('stand_compatibility_matrix','rejected_assignment_reason_codes','conditional_remote_stand_warnings'), 'coverage': surface['coverage']}, 'side_effects': ()}

def airport_operations_management_render_workbench():
    ui = airport_operations_management_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'decision_support': {'columns': ('stand_code','gate_code','decision','reason_codes'), 'legend': ('usable','conditional','blocked'), 'panels': full['decision_support_panels']}, 'side_effects': ()}

def smoke_test():
    return {'ok': airport_operations_management_ui_contract()['ok'] and airport_operations_management_render_workbench()['ok'], 'side_effects': ()}


# Standalone one-PBC UI surface extensions.
_BASE_UI_CONTRACT = airport_operations_management_ui_contract
_BASE_RENDER_WORKBENCH = airport_operations_management_render_workbench
_BASE_SMOKE_TEST = smoke_test


def airport_operations_management_ui_contract():
    base = _BASE_UI_CONTRACT()
    from .standalone import airport_controls_contract, airport_forms_contract, airport_wizards_contract, single_pbc_app_contract
    forms = airport_forms_contract()
    wizards = airport_wizards_contract()
    controls = airport_controls_contract()
    app = single_pbc_app_contract()
    return {**base, 'ok': base['ok'] and forms['ok'] and wizards['ok'] and controls['ok'] and app['ok'], 'forms_contract': forms, 'wizards_contract': wizards, 'controls_contract': controls, 'single_pbc_app': app}


def airport_operations_management_render_workbench():
    base = _BASE_RENDER_WORKBENCH()
    from .standalone import single_pbc_app_contract
    app = single_pbc_app_contract()
    return {**base, 'ok': base['ok'] and app['ok'], 'standalone_app': app, 'form_count': len(app['forms']['forms']), 'wizard_count': len(app['wizards']['wizards'])}


def smoke_test():
    base = _BASE_SMOKE_TEST()
    from .standalone import standalone_smoke_test
    standalone = standalone_smoke_test()
    return {'ok': base['ok'] and standalone['ok'], 'base': base, 'standalone': standalone, 'side_effects': ()}
