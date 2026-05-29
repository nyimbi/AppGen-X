from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'actuarial_pricing_reserving'

def actuarial_pricing_reserving_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('ActuarialPricingReservingWorkbench',
 'ActuarialPricingReservingDetail',
 'ActuarialPricingReservingAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('actuarial_pricing_reserving.read',
 'actuarial_pricing_reserving.create',
 'actuarial_pricing_reserving.update',
 'actuarial_pricing_reserving.approve',
 'actuarial_pricing_reserving.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def actuarial_pricing_reserving_render_workbench():
    ui = actuarial_pricing_reserving_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def smoke_test():
    return {'ok': actuarial_pricing_reserving_ui_contract()['ok'] and actuarial_pricing_reserving_render_workbench()['ok'], 'side_effects': ()}


# Standalone one-PBC UI surface extensions.
_BASE_UI_CONTRACT = actuarial_pricing_reserving_ui_contract
_BASE_RENDER_WORKBENCH = actuarial_pricing_reserving_render_workbench
_BASE_SMOKE_TEST = smoke_test


def actuarial_pricing_reserving_ui_contract():
    base = _BASE_UI_CONTRACT()
    from .standalone import actuarial_controls_contract, actuarial_forms_contract, actuarial_wizards_contract, single_pbc_app_contract
    forms = actuarial_forms_contract()
    wizards = actuarial_wizards_contract()
    controls = actuarial_controls_contract()
    app = single_pbc_app_contract()
    return {
        **base,
        'ok': base['ok'] and forms['ok'] and wizards['ok'] and controls['ok'] and app['ok'],
        'forms_contract': forms,
        'wizards_contract': wizards,
        'controls_contract': controls,
        'single_pbc_app': app,
    }


def actuarial_pricing_reserving_render_workbench():
    base = _BASE_RENDER_WORKBENCH()
    from .standalone import single_pbc_app_contract
    app = single_pbc_app_contract()
    return {**base, 'ok': base['ok'] and app['ok'], 'standalone_app': app, 'form_count': len(app['forms']['forms']), 'wizard_count': len(app['wizards']['wizards'])}


def smoke_test():
    base = _BASE_SMOKE_TEST()
    from .standalone import standalone_smoke_test
    standalone = standalone_smoke_test()
    return {'ok': base['ok'] and standalone['ok'], 'base': base, 'standalone': standalone, 'side_effects': ()}
