"""API route contracts for real estate property management."""
from .standalone import api_route_contracts as _api_route_contracts
from .standalone import validate_api_route_contracts as _validate_api_route_contracts
from .standalone import dispatch_route as _dispatch_route


def api_route_contracts():
    return _api_route_contracts()


def validate_api_route_contracts():
    return _validate_api_route_contracts()


def dispatch_route(route, payload=None, state=None, idempotency_key=None):
    result = _dispatch_route(route, payload, state=state)
    if idempotency_key is not None and isinstance(result, dict):
        result['idempotency_key'] = idempotency_key
    return result


def smoke_test():
    probe = dispatch_route('GET /real-estate-property-management-workbench', idempotency_key='route-smoke')
    return {'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and probe['ok'], 'stream_engine_picker_visible': False, 'side_effects': ()}
