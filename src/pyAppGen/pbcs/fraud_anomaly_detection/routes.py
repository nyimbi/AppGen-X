"""API route contracts for the fraud_anomaly_detection PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/fraud_anomaly_detection/risk-events', 'handler': 'command_risk_events', 'permission': 'fraud_anomaly_detection.command.1'},
    {'method': 'POST', 'path': '/api/pbc/fraud_anomaly_detection/fraud-checks', 'handler': 'command_fraud_checks', 'permission': 'fraud_anomaly_detection.command.2'},
    {'method': 'GET', 'path': '/api/pbc/fraud_anomaly_detection/risk-cases', 'handler': 'query_risk_cases', 'permission': 'fraud_anomaly_detection.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
