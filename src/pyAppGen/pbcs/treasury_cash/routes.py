"""API route contracts for the treasury_cash PBC."""

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
