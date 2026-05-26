"""API route contracts for the cross_border_trade PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/landed-cost', 'handler': 'command_landed_cost', 'permission': 'cross_border_trade.command.1'},
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/export-checks', 'handler': 'command_export_checks', 'permission': 'cross_border_trade.command.2'},
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/declarations', 'handler': 'command_declarations', 'permission': 'cross_border_trade.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
