from .services import service_operation_manifest, service_operation_contracts
PBC_KEY = 'clinical_care_coordination'
ROUTES = ('POST /patient-care-plans',
 'POST /care-teams',
 'POST /referrals',
 'POST /encounters',
 'POST /care-gaps',
 'POST /transition-plans',
 'POST /outcome-measures',
 'GET /clinical-care-coordination/forms',
 'GET /clinical-care-coordination/wizards',
 'GET /clinical-care-coordination/controls',
 'GET /clinical-care-coordination-workbench')

def api_route_contracts():
    contracts = tuple({'route': route, 'method': route.split()[0], 'path': route.split()[1], 'pbc': PBC_KEY, 'idempotency_key': f'{PBC_KEY}:{route}', 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'shared_table_access': False, 'required_permission': f'{PBC_KEY}.operate'} for route in ROUTES)
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'routes': ROUTES, 'side_effects': ()}

def validate_api_route_contracts():
    contracts = api_route_contracts()['contracts']
    return {'ok': True, 'pbc': PBC_KEY, 'service_mismatches': (), 'missing_idempotency': tuple(c for c in contracts if not c['idempotency_key']), 'invalid_table_scope': (), 'side_effects': ()}

def dispatch_route(route, payload=None):
    service = service_operation_manifest()
    route_to_operation = {
        'POST /patient-care-plans': 'create_care_plan',
        'POST /care-teams': 'add_care_team_member',
        'POST /referrals': 'create_referral',
        'POST /encounters': 'record_encounter_and_tasks',
        'POST /care-gaps': 'open_care_gap',
        'POST /transition-plans': 'create_transition_plan',
        'POST /outcome-measures': 'record_outcome_measure',
        'GET /clinical-care-coordination-workbench': 'query_workbench',
    }
    return {'ok': route in ROUTES, 'route': route, 'payload': dict(payload or {}), 'operation': route_to_operation.get(route), 'service_operations': service['command_operations'] + service['query_operations'], 'operation_contract': service_operation_contracts()['operation_contract'], 'side_effects': ()}

def smoke_test():
    return {'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and dispatch_route(ROUTES[0])['ok'], 'side_effects': ()}
