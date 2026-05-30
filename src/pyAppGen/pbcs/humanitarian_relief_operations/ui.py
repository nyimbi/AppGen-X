from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
from .forms import form_catalog
from .wizards import wizard_catalog
from .controls import control_catalog
PBC_KEY = 'humanitarian_relief_operations'

def humanitarian_relief_operations_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('HumanitarianReliefOperationsWorkbench',
 'HumanitarianReliefOperationsDetail',
 'HumanitarianReliefOperationsAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('humanitarian_relief_operations.read',
 'humanitarian_relief_operations.create',
 'humanitarian_relief_operations.update',
 'humanitarian_relief_operations.approve',
 'humanitarian_relief_operations.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','assessment_queues','beneficiary_dedupe','warehouse_lots','shipments','distribution_reconciliation','protection_referrals','partner_readiness','donor_packs','agent_workspace','release_evidence'), 'forms': form_catalog()['forms'], 'wizards': wizard_catalog()['wizards'], 'controls': control_catalog()['controls'], 'coverage': surface['coverage']}, 'side_effects': ()}

def humanitarian_relief_operations_render_workbench():
    ui = humanitarian_relief_operations_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def humanitarian_relief_operations_standalone_ui_contract():
    ui = humanitarian_relief_operations_ui_contract()
    surface = ui['full_capability_surface']
    return {'ok': ui['ok'] and len(surface['forms']) >= 8 and len(surface['wizards']) >= 6 and len(surface['controls']) >= 11, 'pbc': PBC_KEY, 'fragments': ui['fragments'], 'forms': surface['forms'], 'wizards': surface['wizards'], 'controls': surface['controls'], 'side_effects': ()}

def smoke_test():
    standalone = humanitarian_relief_operations_standalone_ui_contract()
    return {'ok': humanitarian_relief_operations_ui_contract()['ok'] and humanitarian_relief_operations_render_workbench()['ok'] and standalone['ok'], 'side_effects': ()}
