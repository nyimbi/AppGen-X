"""API route contracts for the multi_sided_market PBC."""
from .services import MultiSidedMarketService, service_operation_contracts


def api_route_contracts():
    contracts = tuple({**item, 'idempotency_key': f"multi_sided_market:{item['operation']}:{{request_id}}", 'stream_engine_picker_visible': False, 'shared_table_access': False} for item in service_operation_contracts()['contracts'])
    return {'ok': bool(contracts), 'pbc': 'multi_sided_market', 'contracts': contracts, 'side_effects': ()}


def validate_api_route_contracts():
    route_contracts = api_route_contracts()['contracts']
    return {'ok': all(item['event_contract'] == 'AppGen-X' and not item['stream_engine_picker_visible'] and not item['shared_table_access'] for item in route_contracts), 'pbc': 'multi_sided_market', 'service_mismatches': (), 'missing_idempotency': tuple(item for item in route_contracts if not item['idempotency_key']), 'invalid_table_scope': tuple(item for item in route_contracts if item['operation_kind'] == 'command' and not item['owned_tables']), 'side_effects': ()}


def dispatch_route(operation, payload=None):
    service = MultiSidedMarketService()
    if not hasattr(service, operation):
        return {'ok': False, 'reason': 'unknown_route', 'side_effects': ()}
    return getattr(service, operation)(payload or {})


def smoke_test():
    validation = validate_api_route_contracts()
    operation = service_operation_contracts()['operations'][0]
    dispatch = dispatch_route(operation, {'request_id': 'smoke'})
    return {'ok': validation['ok'] and dispatch['ok'], 'validation': validation, 'dispatch': dispatch, 'side_effects': ()}
