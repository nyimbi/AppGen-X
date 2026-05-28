from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'agri_supply_chain_traceability'
RELEASE_GATE_ACTION = 'assess_release_readiness'

def agri_supply_chain_traceability_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('AgriSupplyChainTraceabilityWorkbench',
 'AgriSupplyChainTraceabilityDetail',
 'AgriSupplyChainTraceabilityAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('agri_supply_chain_traceability.read',
 'agri_supply_chain_traceability.create',
 'agri_supply_chain_traceability.update',
 'agri_supply_chain_traceability.approve',
 'agri_supply_chain_traceability.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS + (RELEASE_GATE_ACTION,), 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES + ('release_gate_blocked',), 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS + (RELEASE_GATE_ACTION,)), 'navigation_sections': ('overview','operations','release_gate','edge_case_triage','advanced_intelligence','release_evidence'), 'release_gate': {'action': RELEASE_GATE_ACTION, 'required_evidence': ('farm_lot','provenance_proof','certification','storage_event','transport_leg','recall_link'), 'decision_states': ('approved','blocked'), 'blocker_classes': ('provenance','certification','storage','transport','recall','quality_hold')}, 'coverage': surface['coverage']}, 'side_effects': ()}

def agri_supply_chain_traceability_render_workbench():
    ui = agri_supply_chain_traceability_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'release_gate_panel': full['release_gate'], 'side_effects': ()}

def smoke_test():
    return {'ok': agri_supply_chain_traceability_ui_contract()['ok'] and agri_supply_chain_traceability_render_workbench()['ok'], 'side_effects': ()}
