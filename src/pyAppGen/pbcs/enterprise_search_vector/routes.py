"""API route contracts for the enterprise_search_vector PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/enterprise_search_vector/indexes', 'handler': 'command_indexes', 'permission': 'enterprise_search_vector.command.1'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_search_vector/embeddings', 'handler': 'command_embeddings', 'permission': 'enterprise_search_vector.command.2'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_search_vector/search', 'handler': 'command_search', 'permission': 'enterprise_search_vector.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
