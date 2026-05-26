"""API route contracts for the fraud_anomaly_detection PBC."""

from .services import FraudAnomalyDetectionService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/fraud_anomaly_detection/risk-events', 'handler': 'command_risk_events', 'permission': 'fraud_anomaly_detection.command.1'},
    {'method': 'POST', 'path': '/api/pbc/fraud_anomaly_detection/fraud-checks', 'handler': 'command_fraud_checks', 'permission': 'fraud_anomaly_detection.command.2'},
    {'method': 'GET', 'path': '/api/pbc/fraud_anomaly_detection/risk-cases', 'handler': 'query_risk_cases', 'permission': 'fraud_anomaly_detection.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next(
        (item for item in ROUTES if item['method'] == method and item['path'] == path),
        None,
    )
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found'}
    service = FraudAnomalyDetectionService()
    handler = getattr(service, route['handler'])
    result = handler(payload or {})
    return {
        'ok': result.get('ok') is True,
        'handled': True,
        'route': route,
        'result': result,
        'side_effects': (),
    }


def smoke_test():
    """Execute the first route through its registered service handler."""
    if not ROUTES:
        return {'ok': False, 'reason': 'no_routes'}
    first = ROUTES[0]
    return dispatch_route(first['method'], first['path'], {'smoke': True})
