"""API route contracts for the audit_ledger PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/audit_ledger/audit-events', 'handler': 'command_audit_events', 'permission': 'audit_ledger.command.1'},
    {'method': 'GET', 'path': '/api/pbc/audit_ledger/signature-chain', 'handler': 'query_signature_chain', 'permission': 'audit_ledger.query.2'},
    {'method': 'POST', 'path': '/api/pbc/audit_ledger/exports', 'handler': 'command_exports', 'permission': 'audit_ledger.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
