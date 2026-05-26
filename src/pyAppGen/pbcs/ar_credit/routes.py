"""API route contracts for the ar_credit PBC."""

from .services import ArCreditService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/customers', 'handler': 'command_ar_customers', 'permission': 'ar_credit.command.1'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/invoices', 'handler': 'command_ar_invoices', 'permission': 'ar_credit.command.2'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/deliveries', 'handler': 'command_ar_deliveries', 'permission': 'ar_credit.command.3'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/remittances/parse', 'handler': 'command_ar_remittances_parse', 'permission': 'ar_credit.command.4'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/cash-applications', 'handler': 'command_ar_cash_applications', 'permission': 'ar_credit.command.5'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/unapplied-cash', 'handler': 'command_ar_unapplied_cash', 'permission': 'ar_credit.command.6'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/credit-memos', 'handler': 'command_ar_credit_memos', 'permission': 'ar_credit.command.7'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/write-offs', 'handler': 'command_ar_write_offs', 'permission': 'ar_credit.command.8'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/refunds', 'handler': 'command_ar_refunds', 'permission': 'ar_credit.command.9'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/disputes', 'handler': 'command_ar_disputes', 'permission': 'ar_credit.command.10'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/collections', 'handler': 'command_ar_collections', 'permission': 'ar_credit.command.11'},
    {'method': 'POST', 'path': '/api/pbc/ar_credit/ar/e-invoices', 'handler': 'command_ar_e_invoices', 'permission': 'ar_credit.command.12'},
    {'method': 'GET', 'path': '/api/pbc/ar_credit/ar/aging', 'handler': 'query_ar_aging', 'permission': 'ar_credit.query.13'},
    {'method': 'GET', 'path': '/api/pbc/ar_credit/ar/statements/{customer_id}', 'handler': 'query_ar_statements_customer_id', 'permission': 'ar_credit.query.14'},
    {'method': 'GET', 'path': '/api/pbc/ar_credit/ar/revenue-schedules/{invoice_id}', 'handler': 'query_ar_revenue_schedules_invoice_id', 'permission': 'ar_credit.query.15'},
    {'method': 'GET', 'path': '/api/pbc/ar_credit/ar/workbench', 'handler': 'query_ar_workbench', 'permission': 'ar_credit.query.16'},
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
    service = ArCreditService()
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
