"""API route contracts for the field_service_management PBC."""
PBC_KEY = 'field_service_management'
from .app_surface import field_service_management_controls_contract, field_service_management_forms_contract, field_service_management_wizards_contract, single_pbc_field_service_management_app_contract
ROUTES = tuple({'method': api.split()[0], 'path': api.split(maxsplit=1)[1], 'operation': api.lower().replace(' ', '_').replace('/', '_'), 'idempotency_key': f'{PBC_KEY}:{api}'} for api in ('POST /field-work-orders', 'POST /dispatch-assignments', 'POST /mobile-tasks', 'POST /parts-usage', 'GET /field-service-workbench'))


def api_route_contracts():
    contracts = tuple({
        **route,
        'pbc': PBC_KEY,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'shared_table_access': False,
        'required_permission': f'{PBC_KEY}.operate',
    } for route in ROUTES)
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'contracts': contracts,
        'routes': ROUTES,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def validate_api_route_contracts():
    route_contract = api_route_contracts()
    contracts = route_contract['contracts']
    missing_idempotency = tuple(item for item in contracts if not item.get('idempotency_key'))
    invalid_table_scope = tuple(item for item in contracts if item.get('shared_table_access') is not False)
    service_mismatches = ()
    return {
        'ok': route_contract['ok'] and not missing_idempotency and not invalid_table_scope,
        'pbc': PBC_KEY,
        'contracts': route_contract,
        'service_mismatches': service_mismatches,
        'missing_idempotency': missing_idempotency,
        'invalid_table_scope': invalid_table_scope,
        'side_effects': (),
    }

def dispatch_route(path, payload=None):
    route = next((item for item in ROUTES if item['path'] == path), None)
    return {'ok': route is not None, 'route': route, 'payload': dict(payload or {}), 'side_effects': ()}


def smoke_test():
    first = ROUTES[0]
    dispatched = dispatch_route(first['path'], {'tenant': 'tenant-smoke'})
    return {'ok': validate_api_route_contracts()['ok'] and dispatched['ok'] and standalone_app_route_contracts()['ok'], 'standalone_app_routes': standalone_app_route_contracts(), 'side_effects': ()}


def standalone_app_route_contracts():
    routes = (
        {'method': 'GET', 'path': '/api/pbc/field_service_management/app-shell', 'handler': 'single_pbc_field_service_management_app_contract', 'permission': 'field_service_management.read', 'read_tables': single_pbc_field_service_management_app_contract()['owned_tables']},
        {'method': 'GET', 'path': '/api/pbc/field_service_management/forms', 'handler': 'field_service_management_forms_contract', 'permission': 'field_service_management.read', 'read_tables': tuple(form['writes_table'] for form in field_service_management_forms_contract()['forms'])},
        {'method': 'GET', 'path': '/api/pbc/field_service_management/wizards', 'handler': 'field_service_management_wizards_contract', 'permission': 'field_service_management.read', 'read_tables': ()},
        {'method': 'GET', 'path': '/api/pbc/field_service_management/controls', 'handler': 'field_service_management_controls_contract', 'permission': 'field_service_management.read', 'read_tables': tuple(table for control in field_service_management_controls_contract()['controls'] for table in control['table_scope'])},
    )
    invalid_tables = tuple(table for route in routes for table in route['read_tables'] if not table.startswith(f'{PBC_KEY}_'))
    contracts = tuple({**route, 'route_id': f"{route['method']} {route['path']}", 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'shared_table_access': False, 'side_effects': ()} for route in routes)
    return {'ok': bool(contracts) and not invalid_tables, 'pbc': PBC_KEY, 'contracts': contracts, 'routes': tuple(item['route_id'] for item in contracts), 'invalid_tables': invalid_tables, 'side_effects': ()}
