"""API route contracts for the treasury_cash PBC."""

from .services import TreasuryCashService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/bank-accounts', 'handler': 'command_treasury_bank_accounts', 'permission': 'treasury_cash.command.1'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/balances', 'handler': 'command_treasury_balances', 'permission': 'treasury_cash.command.2'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/statements', 'handler': 'command_treasury_statements', 'permission': 'treasury_cash.command.3'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/statements/{id}/reconcile', 'handler': 'command_treasury_statements_id_reconcile', 'permission': 'treasury_cash.command.4'},
    {'method': 'GET', 'path': '/api/pbc/treasury_cash/treasury/cash-position', 'handler': 'query_treasury_cash_position', 'permission': 'treasury_cash.query.5'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/forecasts', 'handler': 'command_treasury_forecasts', 'permission': 'treasury_cash.command.6'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/liquidity/optimize', 'handler': 'command_treasury_liquidity_optimize', 'permission': 'treasury_cash.command.7'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/payment-rails/route', 'handler': 'command_treasury_payment_rails_route', 'permission': 'treasury_cash.command.8'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/investments', 'handler': 'command_treasury_investments', 'permission': 'treasury_cash.command.9'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/debt-draws', 'handler': 'command_treasury_debt_draws', 'permission': 'treasury_cash.command.10'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/fx/hedge-recommendations', 'handler': 'command_treasury_fx_hedge_recommendations', 'permission': 'treasury_cash.command.11'},
    {'method': 'POST', 'path': '/api/pbc/treasury_cash/treasury/events/inbox', 'handler': 'command_treasury_events_inbox', 'permission': 'treasury_cash.command.12'},
    {'method': 'GET', 'path': '/api/pbc/treasury_cash/treasury/workbench', 'handler': 'query_treasury_workbench', 'permission': 'treasury_cash.query.13'},
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
    service = TreasuryCashService()
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
