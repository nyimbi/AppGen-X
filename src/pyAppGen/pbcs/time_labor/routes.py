"""API route contracts for the time_labor PBC."""

from .services import TimeLaborService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/time_labor/shifts', 'handler': 'command_shifts', 'permission': 'time_labor.command.1'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/shift-patterns', 'handler': 'command_shift_patterns', 'permission': 'time_labor.command.2'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/shift-swaps', 'handler': 'command_shift_swaps', 'permission': 'time_labor.command.3'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/clock-events', 'handler': 'command_clock_events', 'permission': 'time_labor.command.4'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/time-entries/calculate', 'handler': 'command_time_entries_calculate', 'permission': 'time_labor.command.5'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/absences', 'handler': 'command_absences', 'permission': 'time_labor.command.6'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/labor-summaries/{id}/approve', 'handler': 'command_labor_summaries_id_approve', 'permission': 'time_labor.command.7'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/time/events/inbox', 'handler': 'command_time_events_inbox', 'permission': 'time_labor.command.8'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/time/rules', 'handler': 'command_time_rules', 'permission': 'time_labor.command.9'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/time/parameters', 'handler': 'command_time_parameters', 'permission': 'time_labor.command.10'},
    {'method': 'POST', 'path': '/api/pbc/time_labor/time/configuration', 'handler': 'command_time_configuration', 'permission': 'time_labor.command.11'},
    {'method': 'GET', 'path': '/api/pbc/time_labor/labor-summaries', 'handler': 'query_labor_summaries', 'permission': 'time_labor.query.12'},
    {'method': 'GET', 'path': '/api/pbc/time_labor/time-workbench', 'handler': 'query_time_workbench', 'permission': 'time_labor.query.13'},
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
    service = TimeLaborService()
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
