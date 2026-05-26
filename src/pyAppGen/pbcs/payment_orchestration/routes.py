"""API route contracts for the payment_orchestration PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/payment-intents', 'handler': 'command_payment_intents', 'permission': 'payment_orchestration.command.1'},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/gateway-routes', 'handler': 'command_gateway_routes', 'permission': 'payment_orchestration.command.2'},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/tokens', 'handler': 'command_tokens', 'permission': 'payment_orchestration.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
