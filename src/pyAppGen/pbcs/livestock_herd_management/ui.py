from .controls import livestock_herd_management_control_catalog
from .forms import livestock_herd_management_form_catalog
from .wizards import livestock_herd_management_wizard_catalog
from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'livestock_herd_management'


def _summarize_standalone_state(state: dict) -> dict:
    animals = state.get('animals', {})
    pregnancies = state.get('pregnancies', {})
    quarantines = state.get('quarantines', {})
    vaccinations = state.get('vaccinations', {})
    yields = state.get('inventory_yields', {})
    welfare = state.get('welfare_assessments', {})
    movement = state.get('movement_permits', {})
    biosecurity = state.get('biosecurity_audits', {})
    weights = [entry.get('average_daily_gain_kg', 0.0) for entries in state.get('weights', {}).values() for entry in entries]
    milk_total = round(sum(item.get('quantity', 0.0) for item in yields.values() if item.get('product_type') == 'milk'), 2)
    return {
        'cards': (
            {'id': 'active_animals', 'label': 'Active animals', 'value': sum(1 for animal in animals.values() if animal.get('status') != 'deceased')},
            {'id': 'pregnancy_queue', 'label': 'Pregnancy queue', 'value': sum(1 for item in pregnancies.values() if item.get('status') == 'confirmed')},
            {'id': 'vaccination_due', 'label': 'Vaccination due', 'value': sum(1 for item in vaccinations.values() if item.get('status') == 'due')},
            {'id': 'quarantine_open', 'label': 'Quarantine open', 'value': sum(1 for item in quarantines.values() if item.get('status') == 'open')},
            {'id': 'milk_litres', 'label': 'Milk litres', 'value': milk_total},
            {'id': 'avg_daily_gain', 'label': 'Avg daily gain kg', 'value': round(sum(weights) / len(weights), 3) if weights else 0.0},
        ),
        'queues': {
            'movement_ready': tuple(sorted(permit_id for permit_id, permit in movement.items() if permit.get('status') == 'approved')),
            'biosecurity_watch': tuple(sorted(audit_id for audit_id, audit in biosecurity.items() if audit.get('status') != 'pass')),
            'welfare_watch': tuple(sorted(assessment_id for assessment_id, assessment in welfare.items() if assessment.get('status') == 'watch')),
            'assistant_previews': tuple(sorted(state.get('assistant_previews', {}))),
        },
    }


def livestock_herd_management_ui_contract():
    surface = domain_capability_surface_contract()
    forms = livestock_herd_management_form_catalog()
    wizards = livestock_herd_management_wizard_catalog()
    controls = livestock_herd_management_control_catalog()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('LivestockHerdManagementWorkbench',
 'LivestockHerdManagementDetail',
 'LivestockHerdManagementAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('livestock_herd_management.read',
 'livestock_herd_management.create',
 'livestock_herd_management.update',
 'livestock_herd_management.approve',
 'livestock_herd_management.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','livestock_cycles','health_and_biosecurity','assistant_previews','release_evidence'), 'coverage': surface['coverage']}, 'forms': forms['forms'], 'wizards': wizards['wizards'], 'controls': controls['controls'], 'workbench_shell': {'app_id': 'livestock_herd_management_one_pbc_app', 'mode': 'standalone_one_pbc_app', 'cards': ('active_animals','pregnancy_queue','vaccination_due','quarantine_open','milk_litres','avg_daily_gain')}, 'domain_coverage': ('animal_registry','herd_groups','breeding_and_pregnancy','calving_and_offspring','health_and_vaccination','feed_and_grazing','weights_and_genetics','movement_and_quarantine','welfare_and_yield','mortality_and_welfare','traceability_and_yield','assistant_preview'), 'side_effects': ()}


def livestock_herd_management_standalone_app_contract() -> dict:
    ui = livestock_herd_management_ui_contract()
    return {
        'ok': ui['ok'],
        'pbc': PBC_KEY,
        'mode': 'standalone_one_pbc_app',
        'forms': ui['forms'],
        'wizards': ui['wizards'],
        'controls': ui['controls'],
        'workbench_shell': ui['workbench_shell'],
        'domain_coverage': ui['domain_coverage'],
        'side_effects': (),
    }


def livestock_herd_management_render_workbench():
    ui = livestock_herd_management_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'forms': tuple(form['form_id'] for form in ui['forms']), 'wizards': tuple(wizard['wizard_id'] for wizard in ui['wizards']), 'controls': tuple(control['control_id'] for control in ui['controls']), 'side_effects': ()}


def livestock_herd_management_render_standalone_app(state: dict, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
    ui = livestock_herd_management_ui_contract()
    summary = _summarize_standalone_state(state)
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'tenant': tenant,
        'shell': {
            'app_id': ui['workbench_shell']['app_id'],
            'mode': ui['workbench_shell']['mode'],
            'principal_permissions': principal_permissions or ui['action_permissions'],
        },
        'workbench': {
            'cards': summary['cards'],
            'queues': summary['queues'],
            'forms': tuple(form['title'] for form in ui['forms']),
            'wizards': tuple(wizard['title'] for wizard in ui['wizards']),
            'controls': tuple(control['title'] for control in ui['controls']),
        },
        'assistant_panel': {
            'preview_count': len(state.get('assistant_previews', {})),
            'latest_preview': next(reversed(tuple(state.get('assistant_previews', {}).values())), None) if state.get('assistant_previews') else None,
        },
        'side_effects': (),
    }


def smoke_test():
    rendered = livestock_herd_management_render_workbench()
    standalone = livestock_herd_management_standalone_app_contract()
    return {'ok': livestock_herd_management_ui_contract()['ok'] and rendered['ok'] and standalone['ok'], 'rendered': rendered, 'standalone': standalone, 'side_effects': ()}
