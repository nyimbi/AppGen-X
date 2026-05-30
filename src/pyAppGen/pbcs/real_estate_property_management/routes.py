from .standalone import api_route_contracts, validate_api_route_contracts, dispatch_route


def smoke_test():
    probe = dispatch_route('GET /real-estate-property-management-workbench')
    return {'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and probe['ok'], 'side_effects': ()}
