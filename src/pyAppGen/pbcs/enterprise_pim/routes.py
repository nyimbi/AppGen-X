"""API route contracts for the enterprise_pim PBC."""

from .services import EnterprisePimService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-taxonomies', 'handler': 'command_product_taxonomies', 'permission': 'enterprise_pim.command.1'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-attributes', 'handler': 'command_product_attributes', 'permission': 'enterprise_pim.command.2'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/localized-content', 'handler': 'command_localized_content', 'permission': 'enterprise_pim.command.3'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows', 'handler': 'command_validation_workflows', 'permission': 'enterprise_pim.command.4'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows/{id}/approve', 'handler': 'command_validation_workflows_id_approve', 'permission': 'enterprise_pim.command.5'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/dependency-schemas', 'handler': 'command_dependency_schemas', 'permission': 'enterprise_pim.command.6'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-events', 'handler': 'command_pim_events', 'permission': 'enterprise_pim.command.7'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-publications', 'handler': 'command_pim_publications', 'permission': 'enterprise_pim.command.8'},
    {'method': 'GET', 'path': '/api/pbc/enterprise_pim/pim-workbench', 'handler': 'query_pim_workbench', 'permission': 'enterprise_pim.query.9'},
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
    service = EnterprisePimService()
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
