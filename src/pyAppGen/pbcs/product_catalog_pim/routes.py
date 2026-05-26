"""API route contracts for the product_catalog_pim PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/product_catalog_pim/products', 'handler': 'command_products', 'permission': 'product_catalog_pim.command.1'},
    {'method': 'GET', 'path': '/api/pbc/product_catalog_pim/product-read-models', 'handler': 'query_product_read_models', 'permission': 'product_catalog_pim.query.2'},
    {'method': 'POST', 'path': '/api/pbc/product_catalog_pim/prices', 'handler': 'command_prices', 'permission': 'product_catalog_pim.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
