"""API route contracts for the Fraud Anomaly Detection PBC."""

from .app_surface import fraud_anomaly_detection_controls_contract
from .app_surface import fraud_anomaly_detection_forms_contract
from .app_surface import fraud_anomaly_detection_wizards_contract
from .app_surface import single_pbc_fraud_anomaly_detection_app_contract
from .services import FraudAnomalyDetectionService
from .services import service_operation_contracts


ROUTES = tuple(
    {
        'method': contract['method'],
        'path': contract['path'],
        'handler': contract['operation'],
        'permission': contract['permission'],
    }
    for contract in service_operation_contracts()['contracts']
)

STANDALONE_APP_ROUTES = (
    {"method": "GET", "path": "/api/pbc/fraud_anomaly_detection/app-shell", "handler": "single_pbc_fraud_anomaly_detection_app_contract", "permission": "fraud_anomaly_detection.audit", "read_tables": single_pbc_fraud_anomaly_detection_app_contract()["owned_tables"]},
    {"method": "GET", "path": "/api/pbc/fraud_anomaly_detection/forms", "handler": "fraud_anomaly_detection_forms_contract", "permission": "fraud_anomaly_detection.audit", "read_tables": tuple(form["writes_table"] for form in fraud_anomaly_detection_forms_contract()["forms"])},
    {"method": "GET", "path": "/api/pbc/fraud_anomaly_detection/wizards", "handler": "fraud_anomaly_detection_wizards_contract", "permission": "fraud_anomaly_detection.audit", "read_tables": ()},
    {"method": "GET", "path": "/api/pbc/fraud_anomaly_detection/controls", "handler": "fraud_anomaly_detection_controls_contract", "permission": "fraud_anomaly_detection.audit", "read_tables": tuple(table for control in fraud_anomaly_detection_controls_contract()["controls"] for table in control["table_scope"])},
)

API_ROUTE_CONTRACTS = tuple(
    {
        **contract,
        'handler': contract['operation'],
        'idempotency_required': contract['operation_kind'] == 'command',
        'idempotency_key': f"fraud_anomaly_detection:{contract['operation']}:idempotency_key" if contract['operation_kind'] == 'command' else None,
        'shared_table_access': False,
        'stream_engine_picker_visible': False,
    }
    for contract in service_operation_contracts()['contracts']
)


def standalone_app_route_contracts():
    """Return route contracts for the standalone one-PBC fraud app shell."""
    contracts = tuple({**route, 'route_id': f"{route['method']} {route['path']}", 'operation_kind': 'query', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_read_only', 'stream_engine_picker_visible': False, 'shared_table_access': False, 'side_effects': ()} for route in STANDALONE_APP_ROUTES)
    invalid_tables = tuple(table for route in contracts for table in route['read_tables'] if not table.startswith('fraud_anomaly_detection_'))
    return {'ok': bool(contracts) and not invalid_tables, 'pbc': 'fraud_anomaly_detection', 'contracts': contracts, 'routes': tuple(item['route_id'] for item in contracts), 'invalid_tables': invalid_tables, 'side_effects': ()}


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts():
    """Return executable API route contracts with policy and boundary evidence."""
    service_index = {
        (item['operation'], item['method'], item['path']): item
        for item in service_operation_contracts()['contracts']
    }
    contracts = tuple(
        {
            **contract,
            'service_operation': service_index.get((contract['operation'], contract['method'], contract['path'])),
            'route_id': f"{contract['method']} {contract['path']}",
        }
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        'ok': len(contracts) >= 9
        and all(item['event_contract'] == 'AppGen-X' for item in contracts)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in contracts)
        and all(item['stream_engine_picker_visible'] is False for item in contracts)
        and all(item['shared_table_access'] is False for item in contracts),
        'pbc': 'fraud_anomaly_detection',
        'contracts': contracts,
        'routes': tuple(item['route_id'] for item in contracts),
        'side_effects': (),
    }


def validate_api_route_contracts():
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest['contracts']
    service_mismatches = tuple(
        item['route_id']
        for item in contracts
        if not item['service_operation']
        or item['service_operation']['method'] != item['method']
        or item['service_operation']['path'] != item['path']
        or item['service_operation']['permission'] != item['permission']
    )
    missing_idempotency = tuple(item['route_id'] for item in contracts if item['idempotency_required'] and not item['idempotency_key'])
    invalid_table_scope = tuple(
        item['route_id']
        for item in contracts
        for table in item['owned_tables'] + item['read_tables']
        if not table.startswith('fraud_anomaly_detection_')
    )
    return {
        'ok': manifest['ok'] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        'pbc': 'fraud_anomaly_detection',
        'contracts': contracts,
        'service_mismatches': service_mismatches,
        'missing_idempotency': missing_idempotency,
        'invalid_table_scope': invalid_table_scope,
        'side_effects': (),
    }


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next((item for item in ROUTES if item['method'] == method and item['path'] == path), None)
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found'}
    service = FraudAnomalyDetectionService()
    handler = getattr(service, route['handler'])
    result = handler(payload or {})
    return {'ok': result.get('ok') is True, 'handled': True, 'route': route, 'result': result, 'side_effects': ()}


def smoke_test():
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    app_routes = standalone_app_route_contracts()
    if not ROUTES:
        return {'ok': False, 'reason': 'no_routes'}
    first = ROUTES[0]
    dispatched = dispatch_route(first['method'], first['path'], {'smoke': True})
    return {'ok': validation['ok'] and dispatched['ok'] and app_routes['ok'], 'validation': validation, 'dispatch': dispatched, 'standalone_app_routes': app_routes, 'side_effects': ()}
