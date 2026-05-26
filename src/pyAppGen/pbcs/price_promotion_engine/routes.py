"""API route contracts for the price_promotion_engine PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/price_promotion_engine/price-quotes', 'handler': 'command_price_quotes', 'permission': 'price_promotion_engine.command.1'},
    {'method': 'POST', 'path': '/api/pbc/price_promotion_engine/promotions', 'handler': 'command_promotions', 'permission': 'price_promotion_engine.command.2'},
    {'method': 'GET', 'path': '/api/pbc/price_promotion_engine/price-decisions', 'handler': 'query_price_decisions', 'permission': 'price_promotion_engine.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
