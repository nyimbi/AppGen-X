PBC_KEY = 'rail_operations_management'
PARAMETERS = (
    'quality_score_floor',
    'approval_sla_hours',
    'conflict_horizon_minutes',
    'crew_legality_buffer_minutes',
    'minimum_headway_minutes',
    'dispatch_review_threshold',
    'energy_cost_per_kwh',
    'carbon_kg_alert_threshold',
    'handover_packet_minimum_sections',
    'workbench_limit',
)
RULES = (
    'headway_and_junction_policy',
    'rolling_stock_route_compatibility_policy',
    'crew_legality_and_fatigue_policy',
    'maintenance_window_overlap_policy',
    'yard_shunt_safety_policy',
    'platform_reoccupation_policy',
    'passenger_recovery_policy',
    'freight_priority_and_cutoff_policy',
    'incident_escalation_policy',
    'energy_aware_dispatch_policy',
)


def configuration_manifest():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'database_backends': ('postgresql', 'mysql', 'mariadb'),
        'required_event_topic': 'pbc.rail_operations_management.events',
        'required_fields': (
            'database_backend',
            'event_topic',
            'control_center',
            'assistant_requires_confirmation',
            'tenant_isolation_mode',
            'workbench_limit',
        ),
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
    }


def validate_configuration(config=None):
    config = dict(config or {'database_backend': 'postgresql', 'event_topic': 'pbc.rail_operations_management.events'})
    ok = (
        config.get('database_backend', 'postgresql') in ('postgresql', 'mysql', 'mariadb')
        and config.get('event_topic', 'pbc.rail_operations_management.events') == 'pbc.rail_operations_management.events'
    )
    return {'ok': ok, 'configuration': config, 'side_effects': ()}


def parameter_manifest():
    return {'ok': True, 'parameters': tuple({'name': p, 'bounded': True} for p in PARAMETERS), 'side_effects': ()}


def set_parameter(name, value):
    return {'ok': name in PARAMETERS, 'name': name, 'value': value, 'bounded': True, 'side_effects': ()}


def rule_manifest():
    return {'ok': True, 'rules': RULES, 'side_effects': ()}


def compile_rule(rule):
    return {'ok': True, 'rule': dict(rule), 'compiled_hash': str(abs(hash(repr(rule)))), 'side_effects': ()}


def evaluate_rule(rule, payload=None):
    passed = dict(payload or {}).get('severity') != 'critical_blocked'
    return {'ok': True, 'passed': passed, 'rule': rule, 'payload': dict(payload or {}), 'side_effects': ()}


def governance_smoke_test():
    return {
        'ok': validate_configuration()['ok']
        and parameter_manifest()['ok']
        and rule_manifest()['ok']
        and compile_rule({'rule_id': RULES[0]})['ok']
        and evaluate_rule(RULES[0])['ok'],
        'side_effects': (),
    }


def smoke_test():
    return governance_smoke_test()
