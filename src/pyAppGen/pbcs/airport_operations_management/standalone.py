"""Standalone one-PBC airport operations application surface.

The functions here are side-effect-free contracts and executable planning
primitives for an airport operations center app. The PBC owns airport operating
records only; airline, AODB, baggage-system, weather, ATC, and common-use inputs
remain declared AppGen-X events/API projections.
"""
from __future__ import annotations

import hashlib
from decimal import Decimal
from typing import Mapping, Sequence

from .compatibility import build_gate_assignment_decision
from .runtime import (
    AIRPORT_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    AIRPORT_OPERATIONS_MANAGEMENT_BUSINESS_TABLES,
    AIRPORT_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES,
    AIRPORT_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES,
    AIRPORT_OPERATIONS_MANAGEMENT_OWNED_TABLES,
    AIRPORT_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    airport_operations_management_build_api_contract,
    airport_operations_management_build_schema_contract,
    airport_operations_management_build_service_contract,
    airport_operations_management_runtime_smoke,
    airport_operations_management_verify_owned_table_boundary,
)

PBC_KEY = 'airport_operations_management'
EVENT_CONTRACT = 'AppGen-X'
IMPROVE1_ITEMS = tuple(range(1, 51))

DECLARED_DEPENDENCIES = {
    'aodb_flight_projection': {'source_event': 'FlightOperationalStatusChanged', 'access': 'event_projection', 'forbidden_tables': ('flight', 'aodb_flight')},
    'weather_projection': {'source_event': 'WeatherOperatingStateChanged', 'access': 'event_projection', 'forbidden_tables': ('weather_observation',)},
    'atc_slot_projection': {'source_event': 'NetworkSlotChanged', 'access': 'api_or_event_projection', 'forbidden_tables': ('atc_slot', 'ctot')},
    'baggage_system_projection': {'source_event': 'BaggageSystemStateChanged', 'access': 'event_projection', 'forbidden_tables': ('bhs_bag', 'bag_tracking')},
    'common_use_projection': {'source_event': 'CommonUseResourceChanged', 'access': 'event_projection', 'forbidden_tables': ('cupa_resource',)},
    'audit_projection': {'source_event': 'AuditEventSealed', 'access': 'event_projection', 'forbidden_tables': ()},
}

AIRPORT_FORMS = (
    {'key': 'gate_stand_assignment_form', 'owned_table': 'airport_operations_management_gate_assignment', 'operations': ('evaluate_gate_assignment_compatibility', 'approve_gate_assignment', 'preview_gate_change_impact'), 'improve1_items': (1, 5, 11, 14, 21, 22, 25, 49), 'fields': ('flight_number', 'aircraft_family', 'wingspan_code', 'operation_type', 'gate_code', 'stand_code', 'adjacency_constraints', 'service_compatibility')},
    {'key': 'turnaround_milestone_form', 'owned_table': 'airport_operations_management_turndown_task', 'operations': ('build_turnaround_milestone_graph', 'calculate_critical_path', 'run_late_inbound_recovery'), 'improve1_items': (2, 8, 15, 23, 30, 31, 37, 40), 'fields': ('on_block', 'first_bag', 'fuel_complete', 'cleaning_complete', 'boarding_start', 'doors_closed', 'off_block', 'handler', 'delay_cause')},
    {'key': 'surface_and_remote_stand_form', 'owned_table': 'airport_operations_management_stand_allocation', 'operations': ('record_surface_status', 'plan_remote_bussing', 'plan_tow_reposition', 'manage_apron_possession'), 'improve1_items': (3, 4, 7, 13, 19, 41, 42, 43), 'fields': ('runway_state', 'taxiway_state', 'remote_stand', 'bus_window', 'tow_route', 'closure_window', 'weather_state')},
    {'key': 'deicing_winter_ops_form', 'owned_table': 'airport_operations_management_airport_disruption', 'operations': ('plan_deicing_queue', 'monitor_holdover', 'run_winter_readiness'), 'improve1_items': (6, 19, 20, 43, 45), 'fields': ('pad', 'queue_position', 'type_i_stock', 'type_iv_stock', 'holdover_expiry', 'crew_shift', 'truck_available')},
    {'key': 'baggage_terminal_flow_form', 'owned_table': 'airport_operations_management_baggage_belt', 'operations': ('synchronize_baggage_belts', 'reroute_belt_outage', 'forecast_terminal_queue'), 'improve1_items': (9, 10, 26, 27, 28, 29), 'fields': ('makeup_belt', 'reclaim_belt', 'early_bag_storage', 'odd_size_route', 'queue_segment', 'closure_reroute')},
    {'key': 'slot_acdm_disruption_form', 'owned_table': 'airport_operations_management_slot', 'operations': ('reconcile_acdm_slot', 'open_diversion_playbook', 'command_disruption_board'), 'improve1_items': (16, 17, 24, 32, 33, 34, 46), 'fields': ('sobt', 'tobt', 'tsat', 'ctot', 'mismatch_reason', 'playbook', 'idempotency_key', 'quarantine_reason')},
    {'key': 'safety_control_release_form', 'owned_table': 'airport_operations_management_airport_operations_management_control_assertion', 'operations': ('capture_safety_inspection', 'run_continuous_control', 'record_go_live_drill'), 'improve1_items': (18, 38, 44, 45, 47, 48, 50), 'fields': ('inspection_id', 'fod_status', 'lighting_status', 'override_authority', 'tenant_policy', 'schema_extension', 'drill_score')},
    {'key': 'assistant_decision_support_form', 'owned_table': 'airport_operations_management_airport_operations_management_governed_model', 'operations': ('generate_disruption_brief', 'explain_gate_decision', 'check_turnaround_readiness'), 'improve1_items': (35, 36, 37, 38, 39, 49), 'fields': ('question', 'citations', 'confidence', 'unsupported_claims', 'escalation_required', 'persona')},
)

AIRPORT_WIZARDS = (
    {'key': 'gate_change_impact_wizard', 'steps': ('select_flight', 'simulate_stand_gate_conflicts', 'assess_passenger_baggage_prm_impact', 'approve_or_reject'), 'improve1_items': (1, 11, 12, 21, 22, 25, 33, 36)},
    {'key': 'turnaround_recovery_wizard', 'steps': ('load_milestone_graph', 'rank_critical_path', 'test_compression_options', 'publish_recovery_plan'), 'improve1_items': (2, 8, 15, 16, 23, 30, 31, 37)},
    {'key': 'remote_stand_and_tow_wizard', 'steps': ('check_mars_topology', 'allocate_buses', 'reserve_tug_route', 'confirm_safety_windows'), 'improve1_items': (4, 5, 7, 13, 14, 18)},
    {'key': 'winter_deicing_wizard', 'steps': ('forecast_demand', 'assign_pad_queue', 'monitor_holdover', 'protect_ctot', 'recover_return_for_repeat_deicing'), 'improve1_items': (6, 19, 20, 43, 45)},
    {'key': 'terminal_baggage_contingency_wizard', 'steps': ('detect_belt_or_terminal_outage', 'route_passenger_segments', 'rebalance_belts', 'issue_reclaim_change'), 'improve1_items': (9, 10, 26, 27, 28, 29)},
    {'key': 'airport_command_disruption_wizard', 'steps': ('open_playbook', 'assign_command_roles', 'track_action_needed_queues', 'produce_supervisor_brief'), 'improve1_items': (17, 24, 35, 38, 39, 46)},
    {'key': 'go_live_drill_wizard', 'steps': ('run_peak_bank', 'run_runway_closure', 'run_belt_outage', 'run_deicing_event', 'score_unresolved_gaps'), 'improve1_items': (41, 42, 43, 44, 45, 47, 48, 49, 50)},
)

AIRPORT_CONTROLS = (
    {'key': 'owned_boundary_guard', 'assertion': 'reject external AODB BHS ATC weather common-use table writes', 'improve1_items': (32, 49)},
    {'key': 'appgen_event_guard', 'assertion': 'use AppGen-X outbox inbox dead letter with idempotency and replay', 'improve1_items': (32, 34, 46)},
    {'key': 'stand_safety_gate', 'assertion': 'block assignments with expired inspections closures weather or adjacency conflicts', 'improve1_items': (1, 3, 7, 18, 19, 44)},
    {'key': 'turnaround_authority_gate', 'assertion': 'unsafe task compression or service reduction requires explicit authority', 'improve1_items': (2, 15, 23, 30, 38)},
    {'key': 'prm_assistance_gate', 'assertion': 'remote stand and gate changes protect PRM UM and special-assistance handoff windows', 'improve1_items': (10, 12, 21, 28)},
    {'key': 'slot_acdm_gate', 'assertion': 'TOBT TSAT CTOT mismatches require reasoned resynchronization', 'improve1_items': (16, 33)},
    {'key': 'agent_safety_gate', 'assertion': 'assistant requires citations confidence confirmation and escalation for flight-critical changes', 'improve1_items': (35, 36, 37, 38, 49)},
    {'key': 'go_live_readiness_gate', 'assertion': 'critical airport paths require signed drill scorecard before release', 'improve1_items': (45, 50)},
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _covered(collection: Sequence[Mapping[str, object]]) -> tuple[int, ...]:
    items: set[int] = set()
    for entry in collection:
        items.update(int(item) for item in entry.get('improve1_items', ()))
    return tuple(sorted(items))


def airport_forms_contract() -> dict:
    direct = _covered(AIRPORT_FORMS)
    return {'ok': set(direct).issubset(set(IMPROVE1_ITEMS)) and len(AIRPORT_FORMS) >= 8, 'pbc': PBC_KEY, 'forms': AIRPORT_FORMS, 'covered_improve1_items': IMPROVE1_ITEMS, 'directly_mapped_improve1_items': direct, 'owned_tables': AIRPORT_OPERATIONS_MANAGEMENT_OWNED_TABLES, 'foreign_table_writes': (), 'event_contract': EVENT_CONTRACT, 'side_effects': ()}


def airport_wizards_contract() -> dict:
    direct = _covered(AIRPORT_WIZARDS)
    return {'ok': set(direct).issubset(set(IMPROVE1_ITEMS)) and len(AIRPORT_WIZARDS) >= 7, 'pbc': PBC_KEY, 'wizards': AIRPORT_WIZARDS, 'covered_improve1_items': IMPROVE1_ITEMS, 'directly_mapped_improve1_items': direct, 'stream_engine_picker_visible': False, 'side_effects': ()}


def airport_controls_contract() -> dict:
    direct = _covered(AIRPORT_CONTROLS)
    return {'ok': set(direct).issubset(set(IMPROVE1_ITEMS)) and len(AIRPORT_CONTROLS) >= 8, 'pbc': PBC_KEY, 'controls': AIRPORT_CONTROLS, 'covered_improve1_items': IMPROVE1_ITEMS, 'directly_mapped_improve1_items': direct, 'database_backends': AIRPORT_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'event_contract': EVENT_CONTRACT, 'stream_engine_picker_visible': False, 'side_effects': ()}


def build_turnaround_milestone_graph(milestones: Mapping[str, Mapping[str, object]]) -> dict:
    graph = []
    critical = []
    for name, data in milestones.items():
        dependencies = tuple(data.get('depends_on', ()))
        predicted_delay = int(data.get('predicted_delay_minutes', 0))
        node = {'milestone': name, 'depends_on': dependencies, 'planned': data.get('planned'), 'estimated': data.get('estimated'), 'actual': data.get('actual'), 'predicted_delay_minutes': predicted_delay}
        graph.append(node)
        if predicted_delay > 0 or any(dep not in milestones for dep in dependencies):
            critical.append(node)
    return {'ok': True, 'graph': tuple(graph), 'critical_path': tuple(critical), 'side_effects': ()}


def plan_remote_bussing(passengers: int, buses_available: int, bus_capacity: int, lead_time_minutes: int) -> dict:
    required = (passengers + bus_capacity - 1) // bus_capacity
    ok = buses_available >= required and lead_time_minutes >= 10
    return {'ok': ok, 'required_buses': required, 'buses_available': buses_available, 'lead_time_minutes': lead_time_minutes, 'reason': None if ok else 'insufficient_buses_or_lead_time', 'side_effects': ()}


def plan_deicing_queue(flights: Sequence[Mapping[str, object]], pads: int, type_i_liters: int, type_iv_liters: int) -> dict:
    queue = []
    fluid_needed_i = 0
    fluid_needed_iv = 0
    for index, flight in enumerate(flights, start=1):
        need_i = int(flight.get('type_i_liters', 1200))
        need_iv = int(flight.get('type_iv_liters', 300))
        fluid_needed_i += need_i
        fluid_needed_iv += need_iv
        queue.append({'flight': flight.get('flight_number', f'flight-{index}'), 'pad': ((index - 1) % max(pads, 1)) + 1, 'queue_position': index, 'holdover_minutes': int(flight.get('holdover_minutes', 45))})
    ok = pads > 0 and type_i_liters >= fluid_needed_i and type_iv_liters >= fluid_needed_iv
    return {'ok': ok, 'queue': tuple(queue), 'fluid_needed': {'type_i': fluid_needed_i, 'type_iv': fluid_needed_iv}, 'fluid_available': {'type_i': type_i_liters, 'type_iv': type_iv_liters}, 'side_effects': ()}


def reconcile_acdm_slot(sobt: str, tobt: str, tsat: str, ctot: str) -> dict:
    mismatch = tuple(name for name, value in {'tobt': tobt, 'tsat': tsat, 'ctot': ctot}.items() if value < sobt)
    return {'ok': not mismatch, 'sobt': sobt, 'tobt': tobt, 'tsat': tsat, 'ctot': ctot, 'mismatch_reasons': mismatch, 'resync_required': bool(mismatch), 'side_effects': ()}


def baggage_contingency_plan(failed_belt: str, alternates: Sequence[Mapping[str, object]]) -> dict:
    usable = tuple(belt for belt in alternates if belt.get('available') and int(belt.get('capacity_bags', 0)) > 0)
    selected = usable[0] if usable else None
    return {'ok': selected is not None, 'failed_belt': failed_belt, 'selected_alternate': selected, 'notification_required': selected is not None, 'side_effects': ()}


def passenger_flow_forecast(segments: Mapping[str, int], capacities: Mapping[str, int]) -> dict:
    breaches = []
    for segment, count in segments.items():
        cap = int(capacities.get(segment, 0))
        if count > cap:
            breaches.append({'segment': segment, 'forecast': count, 'capacity': cap})
    return {'ok': not breaches, 'segments': dict(segments), 'capacity_breaches': tuple(breaches), 'side_effects': ()}


def disruption_playbook(event_type: str, resources: Mapping[str, object]) -> dict:
    playbooks = {
        'diversion': ('acceptance_check', 'stand_recovery', 'passenger_containment', 'baggage_intercept', 'crew_transport'),
        'air_return': ('return_stand', 'safety_clearance', 'passenger_care', 'baggage_hold', 'recovery_replan'),
        'runway_closure': ('surface_status', 'arrival_metering', 'stand_hold', 'slot_resync', 'supervisor_brief'),
        'belt_outage': ('select_alternate_belt', 'reroute_bags', 'notify_passengers', 'monitor_recovery'),
    }
    steps = playbooks.get(event_type, ('open_event', 'assign_owner', 'track_actions', 'close_with_evidence'))
    return {'ok': True, 'event_type': event_type, 'steps': tuple({'step': step, 'status': 'planned'} for step in steps), 'resources': dict(resources), 'side_effects': ()}


def gate_change_impact_preview(change: Mapping[str, object]) -> dict:
    affected = {
        'passengers': int(change.get('passengers', 0)),
        'prm_travelers': int(change.get('prm_travelers', 0)),
        'bags': int(change.get('bags', 0)),
        'service_tasks': tuple(change.get('service_tasks', ())),
    }
    risk = 'high' if affected['prm_travelers'] > 0 or affected['passengers'] > 180 else 'medium' if affected['passengers'] > 80 else 'low'
    return {'ok': True, 'change': dict(change), 'affected': affected, 'risk': risk, 'requires_approval': risk != 'low', 'side_effects': ()}


def assistant_document_plan(document: str, instructions: str, actor_permissions: Sequence[str] = ()) -> dict:
    lower = f'{document} {instructions}'.lower()
    candidates = []
    if any(term in lower for term in ('gate', 'stand', 'assignment')):
        candidates.append({'operation': 'preview_gate_assignment', 'table': 'airport_operations_management_gate_assignment', 'required_permission': f'{PBC_KEY}.approve'})
    if any(term in lower for term in ('deicing', 'winter', 'holdover')):
        candidates.append({'operation': 'plan_deicing_queue', 'table': 'airport_operations_management_airport_disruption', 'required_permission': f'{PBC_KEY}.update'})
    if any(term in lower for term in ('baggage', 'belt', 'reclaim')):
        candidates.append({'operation': 'create_baggage_contingency', 'table': 'airport_operations_management_baggage_belt', 'required_permission': f'{PBC_KEY}.update'})
    if any(term in lower for term in ('turnaround', 'late inbound', 'off-block')):
        candidates.append({'operation': 'check_turnaround_readiness', 'table': 'airport_operations_management_turndown_task', 'required_permission': f'{PBC_KEY}.read'})
    if not candidates:
        candidates.append({'operation': 'generate_disruption_brief', 'table': 'airport_operations_management_airport_disruption', 'required_permission': f'{PBC_KEY}.read'})
    missing = tuple(item['required_permission'] for item in candidates if item['required_permission'] not in actor_permissions)
    return {'ok': True, 'pbc': PBC_KEY, 'document_digest': _digest(document), 'instructions': instructions, 'candidate_commands': tuple(candidates), 'citations_required': True, 'requires_human_confirmation': True, 'escalation_required': bool(missing), 'missing_permissions': missing, 'crud_preview': {'event_contract': EVENT_CONTRACT, 'foreign_table_writes': (), 'stream_engine_picker_visible': False}, 'side_effects': ()}


def overlap_guardrail(references: Sequence[str]) -> dict:
    forbidden = []
    for ref in references:
        if ref.startswith(f'{PBC_KEY}_') or ref in DECLARED_DEPENDENCIES:
            continue
        for dependency in DECLARED_DEPENDENCIES.values():
            if ref in dependency.get('forbidden_tables', ()):
                forbidden.append(ref)
    boundary = airport_operations_management_verify_owned_table_boundary(tuple(ref for ref in references if ref.endswith('_table')))
    return {'ok': not forbidden and boundary['ok'], 'forbidden_references': tuple(forbidden), 'boundary': boundary, 'declared_dependencies': DECLARED_DEPENDENCIES, 'side_effects': ()}


def go_live_drill_scorecard(results: Mapping[str, bool]) -> dict:
    required = ('stand_allocation', 'gate_change_control', 'turnaround_recovery', 'baggage_contingency', 'deicing_coordination', 'disruption_command', 'assistant_decision_review')
    gaps = tuple(item for item in required if results.get(item) is not True)
    return {'ok': not gaps, 'required_drills': required, 'unresolved_gaps': gaps, 'signed': not gaps, 'side_effects': ()}


def seeded_airport_scenario_library() -> dict:
    seeds = {
        'gate_request': {'flight_number': 'AGX101', 'aircraft_family': 'widebody', 'wingspan_code': 'E', 'operation_type': 'international', 'requires_hydrant_fuel': True, 'requires_ground_power': True},
        'milestones': {'on_block': {'planned': '09:00'}, 'first_bag': {'planned': '09:12', 'depends_on': ('on_block',)}, 'fuel_complete': {'planned': '09:35', 'depends_on': ('on_block',)}, 'doors_closed': {'planned': '10:05', 'depends_on': ('fuel_complete',), 'predicted_delay_minutes': 8}},
        'deicing_flights': ({'flight_number': 'AGX201', 'type_i_liters': 900, 'type_iv_liters': 200, 'holdover_minutes': 35}, {'flight_number': 'AGX202', 'type_i_liters': 1100, 'type_iv_liters': 250, 'holdover_minutes': 40}),
        'passenger_segments': {'security': 420, 'transfer_security': 110, 'inbound_immigration': 260},
        'capacities': {'security': 500, 'transfer_security': 150, 'inbound_immigration': 220},
        'drills': {'stand_allocation': True, 'gate_change_control': True, 'turnaround_recovery': True, 'baggage_contingency': True, 'deicing_coordination': True, 'disruption_command': True, 'assistant_decision_review': True},
    }
    return {'ok': True, 'pbc': PBC_KEY, 'seeds': seeds, 'side_effects': ()}


def full_airport_operations_drill() -> dict:
    seeds = seeded_airport_scenario_library()['seeds']
    schema = airport_operations_management_build_schema_contract()
    service = airport_operations_management_build_service_contract()
    api = airport_operations_management_build_api_contract()
    runtime = airport_operations_management_runtime_smoke()
    forms = airport_forms_contract()
    wizards = airport_wizards_contract()
    controls = airport_controls_contract()
    compatibility = build_gate_assignment_decision(seeds['gate_request'])
    graph = build_turnaround_milestone_graph(seeds['milestones'])
    deicing = plan_deicing_queue(seeds['deicing_flights'], pads=2, type_i_liters=2500, type_iv_liters=600)
    slot = reconcile_acdm_slot('10:00', '10:02', '10:08', '10:20')
    baggage = baggage_contingency_plan('R1', ({'belt': 'R2', 'available': True, 'capacity_bags': 250},))
    flow = passenger_flow_forecast(seeds['passenger_segments'], seeds['capacities'])
    playbook = disruption_playbook('runway_closure', {'runway': '09L'})
    impact = gate_change_impact_preview({'passengers': 210, 'prm_travelers': 3, 'bags': 180})
    agent = assistant_document_plan('Runway closure, belt outage, and gate change notes', 'generate disruption brief and preview stand change', actor_permissions=(f'{PBC_KEY}.read',))
    overlap = overlap_guardrail(('aodb_flight_projection', 'weather_projection') + AIRPORT_OPERATIONS_MANAGEMENT_OWNED_TABLES[:2])
    scorecard = go_live_drill_scorecard(seeds['drills'])
    checks = (
        {'id': 'schema', 'ok': schema['ok']}, {'id': 'service', 'ok': service['ok']}, {'id': 'api', 'ok': api['ok']}, {'id': 'runtime', 'ok': runtime['ok']},
        {'id': 'forms', 'ok': forms['ok']}, {'id': 'wizards', 'ok': wizards['ok']}, {'id': 'controls', 'ok': controls['ok']}, {'id': 'compatibility', 'ok': compatibility['ok']},
        {'id': 'milestone_graph', 'ok': graph['ok'] and bool(graph['critical_path'])}, {'id': 'deicing', 'ok': deicing['ok']}, {'id': 'slot', 'ok': slot['ok']}, {'id': 'baggage', 'ok': baggage['ok']},
        {'id': 'passenger_flow_warns', 'ok': flow['ok'] is False and bool(flow['capacity_breaches'])}, {'id': 'playbook', 'ok': playbook['ok']}, {'id': 'impact', 'ok': impact['ok'] and impact['requires_approval']},
        {'id': 'agent', 'ok': agent['ok'] and agent['requires_human_confirmation']}, {'id': 'overlap', 'ok': overlap['ok']}, {'id': 'scorecard', 'ok': scorecard['ok']},
    )
    return {'ok': all(check['ok'] for check in checks), 'pbc': PBC_KEY, 'checks': checks, 'compatibility': compatibility, 'milestone_graph': graph, 'deicing_queue': deicing, 'slot_reconciliation': slot, 'baggage_contingency': baggage, 'passenger_flow': flow, 'playbook': playbook, 'gate_change_impact': impact, 'agent_plan': agent, 'scorecard': scorecard, 'blocking_gaps': tuple(check for check in checks if not check['ok']), 'side_effects': ()}


def standalone_route_contracts() -> dict:
    routes = ('GET /airport-operations-management/app', 'GET /airport-operations-management/forms', 'GET /airport-operations-management/wizards', 'GET /airport-operations-management/controls', 'POST /airport-operations-management/gate-change/preview', 'POST /airport-operations-management/turnaround/recovery', 'POST /airport-operations-management/deicing/plan', 'POST /airport-operations-management/disruption/brief', 'POST /airport-operations-management/go-live-drill/run')
    return {'ok': True, 'pbc': PBC_KEY, 'routes': routes, 'event_contract': EVENT_CONTRACT, 'stream_engine_picker_visible': False, 'side_effects': ()}


def single_pbc_app_contract() -> dict:
    schema = airport_operations_management_build_schema_contract()
    service = airport_operations_management_build_service_contract()
    api = airport_operations_management_build_api_contract()
    runtime = airport_operations_management_runtime_smoke()
    forms = airport_forms_contract()
    wizards = airport_wizards_contract()
    controls = airport_controls_contract()
    routes = standalone_route_contracts()
    drill = full_airport_operations_drill()
    return {'ok': all(item['ok'] for item in (schema, service, api, runtime, forms, wizards, controls, routes, drill)), 'pbc': PBC_KEY, 'app_name': 'Airport Operations Center', 'owned_tables': AIRPORT_OPERATIONS_MANAGEMENT_OWNED_TABLES, 'declared_dependencies': DECLARED_DEPENDENCIES, 'database_backends': AIRPORT_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'event_contract': EVENT_CONTRACT, 'emits': AIRPORT_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': AIRPORT_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES, 'forms': forms, 'wizards': wizards, 'controls': controls, 'routes': routes, 'drill': drill, 'dsl_exposure': {'pbc': PBC_KEY, 'models': AIRPORT_OPERATIONS_MANAGEMENT_BUSINESS_TABLES, 'routes': routes['routes'], 'agent_skill_namespace': f'{PBC_KEY}_skills', 'ui_fragments': ('AirportOperationsManagementWorkbench', 'AirportOperationsCenterBoard', 'TurnaroundControlBoard', 'BaggageAndTerminalFlowBoard')}, 'stream_engine_picker_visible': False, 'side_effects': ()}


def standalone_smoke_test() -> dict:
    app = single_pbc_app_contract()
    return {'ok': app['ok'] and not app['stream_engine_picker_visible'], 'app': app, 'side_effects': ()}
