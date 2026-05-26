"""API route contracts for the schema_registry PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/schema_registry/schemas', 'handler': 'command_schemas', 'permission': 'schema_registry.command.1'},
    {'method': 'POST', 'path': '/api/pbc/schema_registry/compatibility-checks', 'handler': 'command_compatibility_checks', 'permission': 'schema_registry.command.2'},
    {'method': 'GET', 'path': '/api/pbc/schema_registry/subjects', 'handler': 'query_subjects', 'permission': 'schema_registry.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
