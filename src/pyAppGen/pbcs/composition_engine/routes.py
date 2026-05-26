"""API route contracts for the composition_engine PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/composition_engine/compositions', 'handler': 'command_compositions', 'permission': 'composition_engine.command.1'},
    {'method': 'POST', 'path': '/api/pbc/composition_engine/fragments', 'handler': 'command_fragments', 'permission': 'composition_engine.command.2'},
    {'method': 'GET', 'path': '/api/pbc/composition_engine/component-registry', 'handler': 'query_component_registry', 'permission': 'composition_engine.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
