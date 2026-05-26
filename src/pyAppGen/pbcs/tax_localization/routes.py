"""API route contracts for the tax_localization PBC."""

from .services import TaxLocalizationService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/jurisdictions', 'handler': 'command_tax_jurisdictions', 'permission': 'tax_localization.command.1'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/rules', 'handler': 'command_tax_rules', 'permission': 'tax_localization.command.2'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/quotes', 'handler': 'command_tax_quotes', 'permission': 'tax_localization.command.3'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/invoices/{id}/tax-records', 'handler': 'command_tax_invoices_id_tax_records', 'permission': 'tax_localization.command.4'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/filings', 'handler': 'command_tax_filings', 'permission': 'tax_localization.command.5'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/events/inbox', 'handler': 'command_tax_events_inbox', 'permission': 'tax_localization.command.6'},
    {'method': 'GET', 'path': '/api/pbc/tax_localization/tax/workbench', 'handler': 'query_tax_workbench', 'permission': 'tax_localization.query.7'},
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
    service = TaxLocalizationService()
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
