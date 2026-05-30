PBC_KEY = 'rail_operations_management'
PERMISSIONS = (
    'rail_operations_management.read',
    'rail_operations_management.create',
    'rail_operations_management.update',
    'rail_operations_management.approve',
    'rail_operations_management.admin',
)
ACTION_PERMISSIONS = {
    'command_train_plan': 'rail_operations_management.create',
    'record_route_path': 'rail_operations_management.update',
    'record_consist': 'rail_operations_management.update',
    'register_rolling_stock_unit': 'rail_operations_management.update',
    'command_crew_assignment': 'rail_operations_management.update',
    'command_dispatch_decision': 'rail_operations_management.approve',
    'register_signal_restriction': 'rail_operations_management.update',
    'review_track_restriction': 'rail_operations_management.update',
    'review_yard_plan': 'rail_operations_management.update',
    'approve_terminal_slot': 'rail_operations_management.approve',
    'schedule_maintenance_window': 'rail_operations_management.update',
    'record_delay_event': 'rail_operations_management.update',
    'command_disruption_event': 'rail_operations_management.update',
    'plan_passenger_service': 'rail_operations_management.update',
    'plan_freight_service': 'rail_operations_management.update',
    'register_safety_rule': 'rail_operations_management.approve',
    'command_incident_response': 'rail_operations_management.approve',
    'resolve_capacity_conflict': 'rail_operations_management.approve',
    'record_energy_profile': 'rail_operations_management.update',
    'record_sla_snapshot': 'rail_operations_management.update',
    'preview_document_instruction': 'rail_operations_management.read',
}


def permission_manifest():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'permissions': PERMISSIONS,
        'roles': ('dispatcher', 'planner', 'yardmaster', 'terminal_controller', 'incident_commander', 'approver', 'auditor'),
        'action_permissions': ACTION_PERMISSIONS,
        'side_effects': (),
    }


def authorize(permission, actor=None):
    return {
        'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate',
        'permission': permission,
        'actor': dict(actor or {}),
        'side_effects': (),
    }


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}
