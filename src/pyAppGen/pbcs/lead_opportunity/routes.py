"""API route contracts for the lead_opportunity PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/lead_opportunity/leads', 'handler': 'command_leads', 'permission': 'lead_opportunity.command.1'},
    {'method': 'POST', 'path': '/api/pbc/lead_opportunity/opportunities', 'handler': 'command_opportunities', 'permission': 'lead_opportunity.command.2'},
    {'method': 'GET', 'path': '/api/pbc/lead_opportunity/pipeline', 'handler': 'query_pipeline', 'permission': 'lead_opportunity.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
