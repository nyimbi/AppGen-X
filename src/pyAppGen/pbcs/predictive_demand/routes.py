"""API route contracts for the predictive_demand PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/predictive_demand/forecast-runs', 'handler': 'command_forecast_runs', 'permission': 'predictive_demand.command.1'},
    {'method': 'GET', 'path': '/api/pbc/predictive_demand/forecast-results', 'handler': 'query_forecast_results', 'permission': 'predictive_demand.query.2'},
    {'method': 'POST', 'path': '/api/pbc/predictive_demand/signals', 'handler': 'command_signals', 'permission': 'predictive_demand.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
