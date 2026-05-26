"""API route contracts for the workflow_orchestration PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/workflow_orchestration/workflows', 'handler': 'command_workflows', 'permission': 'workflow_orchestration.command.1'},
    {'method': 'POST', 'path': '/api/pbc/workflow_orchestration/instances', 'handler': 'command_instances', 'permission': 'workflow_orchestration.command.2'},
    {'method': 'POST', 'path': '/api/pbc/workflow_orchestration/signals', 'handler': 'command_signals', 'permission': 'workflow_orchestration.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
