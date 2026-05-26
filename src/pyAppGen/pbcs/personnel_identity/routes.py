"""API route contracts for the personnel_identity PBC."""

from .services import PersonnelIdentityService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/departments', 'handler': 'command_personnel_departments', 'permission': 'personnel_identity.command.1'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/departments/{id}/hierarchy', 'handler': 'command_personnel_departments_id_hierarchy', 'permission': 'personnel_identity.command.2'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/employees', 'handler': 'command_personnel_employees', 'permission': 'personnel_identity.command.3'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/employees/{id}/contacts', 'handler': 'command_personnel_employees_id_contacts', 'permission': 'personnel_identity.command.4'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/employees/{id}/documents', 'handler': 'command_personnel_employees_id_documents', 'permission': 'personnel_identity.command.5'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/employees/{id}/status', 'handler': 'command_personnel_employees_id_status', 'permission': 'personnel_identity.command.6'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/employees/{id}/roles', 'handler': 'command_personnel_employees_id_roles', 'permission': 'personnel_identity.command.7'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/employees/{id}/attributes', 'handler': 'command_personnel_employees_id_attributes', 'permission': 'personnel_identity.command.8'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/employees/{id}/verification', 'handler': 'command_personnel_employees_id_verification', 'permission': 'personnel_identity.command.9'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/employees/{id}/proofs', 'handler': 'command_personnel_employees_id_proofs', 'permission': 'personnel_identity.command.10'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/provisioning/routes', 'handler': 'command_personnel_provisioning_routes', 'permission': 'personnel_identity.command.11'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/events/inbox', 'handler': 'command_personnel_events_inbox', 'permission': 'personnel_identity.command.12'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/rules', 'handler': 'command_personnel_rules', 'permission': 'personnel_identity.command.13'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/parameters', 'handler': 'command_personnel_parameters', 'permission': 'personnel_identity.command.14'},
    {'method': 'POST', 'path': '/api/pbc/personnel_identity/personnel/configuration', 'handler': 'command_personnel_configuration', 'permission': 'personnel_identity.command.15'},
    {'method': 'GET', 'path': '/api/pbc/personnel_identity/personnel/org-chart', 'handler': 'query_personnel_org_chart', 'permission': 'personnel_identity.query.16'},
    {'method': 'GET', 'path': '/api/pbc/personnel_identity/personnel/workbench', 'handler': 'query_personnel_workbench', 'permission': 'personnel_identity.query.17'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next(
        (item for item in ROUTES if item['method'] == method and item['path'] == path),
        None,
    )
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found'}
    service = PersonnelIdentityService()
    handler = getattr(service, route['handler'])
    result = handler(payload or {})
    return {
        'ok': result.get('ok') is True,
        'handled': True,
        'route': route,
        'result': result,
        'side_effects': (),
    }


def smoke_test():
    """Execute the first route through its registered service handler."""
    if not ROUTES:
        return {'ok': False, 'reason': 'no_routes'}
    first = ROUTES[0]
    return dispatch_route(first['method'], first['path'], {'smoke': True})
