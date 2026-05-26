"""API route contracts for the federated_iam PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/federated_iam/tokens', 'handler': 'command_tokens', 'permission': 'federated_iam.command.1'},
    {'method': 'GET', 'path': '/api/pbc/federated_iam/principals', 'handler': 'query_principals', 'permission': 'federated_iam.query.2'},
    {'method': 'POST', 'path': '/api/pbc/federated_iam/policy-decisions', 'handler': 'command_policy_decisions', 'permission': 'federated_iam.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
