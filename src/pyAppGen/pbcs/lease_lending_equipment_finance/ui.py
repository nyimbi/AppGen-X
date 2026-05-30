from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
from .controls import control_catalog
from .forms import form_catalog
from .wizards import wizard_catalog
PBC_KEY = 'lease_lending_equipment_finance'

def lease_lending_equipment_finance_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('LeaseLendingEquipmentFinanceWorkbench',
 'LeaseLendingEquipmentFinanceDetail',
 'LeaseLendingEquipmentFinanceAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('lease_lending_equipment_finance.read',
 'lease_lending_equipment_finance.create',
 'lease_lending_equipment_finance.update',
 'lease_lending_equipment_finance.approve',
 'lease_lending_equipment_finance.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','origination','collateral','pricing','servicing','collections','investor_reporting','release_evidence'), 'forms': form_catalog()['forms'], 'wizards': wizard_catalog()['wizards'], 'controls': control_catalog()['controls'], 'coverage': surface['coverage']}, 'side_effects': ()}

def lease_lending_equipment_finance_render_workbench():
    ui = lease_lending_equipment_finance_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}


def lease_lending_equipment_finance_standalone_ui_contract():
    ui = lease_lending_equipment_finance_ui_contract()
    full = ui['full_capability_surface']
    return {'ok': ui['ok'] and len(full['forms']) >= 9 and len(full['wizards']) >= 7 and len(full['controls']) >= 8, 'pbc': PBC_KEY, 'single_pbc_app_route': f'/apps/{PBC_KEY}', 'forms': full['forms'], 'wizards': full['wizards'], 'controls': full['controls'], 'assistant_panel': 'LeaseLendingEquipmentFinanceAssistantPanel', 'side_effects': ()}

def smoke_test():
    return {'ok': lease_lending_equipment_finance_ui_contract()['ok'] and lease_lending_equipment_finance_render_workbench()['ok'] and lease_lending_equipment_finance_standalone_ui_contract()['ok'], 'side_effects': ()}
