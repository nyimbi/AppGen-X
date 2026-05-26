"""API route contracts for the talent_onboarding PBC."""

from .services import TalentOnboardingService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/job-requisitions', 'handler': 'command_job_requisitions', 'permission': 'talent_onboarding.command.1'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/job-requisitions/{id}/approvals', 'handler': 'command_job_requisitions_id_approvals', 'permission': 'talent_onboarding.command.2'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/candidates', 'handler': 'command_candidates', 'permission': 'talent_onboarding.command.3'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/candidates/{id}/stage', 'handler': 'command_candidates_id_stage', 'permission': 'talent_onboarding.command.4'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/interviews', 'handler': 'command_interviews', 'permission': 'talent_onboarding.command.5'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/background-checks', 'handler': 'command_background_checks', 'permission': 'talent_onboarding.command.6'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/offers', 'handler': 'command_offers', 'permission': 'talent_onboarding.command.7'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/offers/{id}/acceptance', 'handler': 'command_offers_id_acceptance', 'permission': 'talent_onboarding.command.8'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/onboarding/tasks', 'handler': 'command_onboarding_tasks', 'permission': 'talent_onboarding.command.9'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/onboarding/provision', 'handler': 'command_onboarding_provision', 'permission': 'talent_onboarding.command.10'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/talent/events/inbox', 'handler': 'command_talent_events_inbox', 'permission': 'talent_onboarding.command.11'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/talent-rules', 'handler': 'command_talent_rules', 'permission': 'talent_onboarding.command.12'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/talent-parameters', 'handler': 'command_talent_parameters', 'permission': 'talent_onboarding.command.13'},
    {'method': 'POST', 'path': '/api/pbc/talent_onboarding/talent-configuration', 'handler': 'command_talent_configuration', 'permission': 'talent_onboarding.command.14'},
    {'method': 'GET', 'path': '/api/pbc/talent_onboarding/talent-workbench', 'handler': 'query_talent_workbench', 'permission': 'talent_onboarding.query.15'},
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
    service = TalentOnboardingService()
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
