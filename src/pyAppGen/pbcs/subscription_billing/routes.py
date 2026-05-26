"""API route contracts for the subscription_billing PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/subscriptions', 'handler': 'command_subscriptions', 'permission': 'subscription_billing.command.1'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/usage', 'handler': 'command_usage', 'permission': 'subscription_billing.command.2'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/renewals', 'handler': 'command_renewals', 'permission': 'subscription_billing.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
