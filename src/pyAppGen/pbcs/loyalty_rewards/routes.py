"""API route contracts for the loyalty_rewards PBC."""

from .services import LoyaltyRewardsService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/loyalty_rewards/points', 'handler': 'command_points', 'permission': 'loyalty_rewards.command.1'},
    {'method': 'POST', 'path': '/api/pbc/loyalty_rewards/redemptions', 'handler': 'command_redemptions', 'permission': 'loyalty_rewards.command.2'},
    {'method': 'GET', 'path': '/api/pbc/loyalty_rewards/reward-accounts', 'handler': 'query_reward_accounts', 'permission': 'loyalty_rewards.query.3'},
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
    service = LoyaltyRewardsService()
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
