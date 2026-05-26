"""API route contracts for the quality_assurance PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/quality_assurance/inspections', 'handler': 'command_inspections', 'permission': 'quality_assurance.command.1'},
    {'method': 'POST', 'path': '/api/pbc/quality_assurance/non-conformances', 'handler': 'command_non_conformances', 'permission': 'quality_assurance.command.2'},
    {'method': 'POST', 'path': '/api/pbc/quality_assurance/quality-holds', 'handler': 'command_quality_holds', 'permission': 'quality_assurance.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
