"""API route contracts for the loyalty_rewards PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/loyalty_rewards/points', 'handler': 'command_points', 'permission': 'loyalty_rewards.command.1'},
    {'method': 'POST', 'path': '/api/pbc/loyalty_rewards/redemptions', 'handler': 'command_redemptions', 'permission': 'loyalty_rewards.command.2'},
    {'method': 'GET', 'path': '/api/pbc/loyalty_rewards/reward-accounts', 'handler': 'query_reward_accounts', 'permission': 'loyalty_rewards.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
