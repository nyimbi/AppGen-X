"""API route contracts for the checkout_processing PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/checkout_processing/carts', 'handler': 'command_carts', 'permission': 'checkout_processing.command.1'},
    {'method': 'POST', 'path': '/api/pbc/checkout_processing/checkout', 'handler': 'command_checkout', 'permission': 'checkout_processing.command.2'},
    {'method': 'POST', 'path': '/api/pbc/checkout_processing/coupons', 'handler': 'command_coupons', 'permission': 'checkout_processing.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
