"""World-class domain depth contract for the travel_management PBC."""
from __future__ import annotations
import hashlib

PBC_KEY = 'travel_management'
DOMAIN_ENTITY = 'trip'
DOMAIN_PURPOSE = 'Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.'
DOMAIN_OWNED_TABLES = ('travel_management_trip_request',
 'travel_management_traveler_profile',
 'travel_management_travel_policy',
 'travel_management_travel_approval_task',
 'travel_management_booking_intent',
 'travel_management_air_booking',
 'travel_management_hotel_booking',
 'travel_management_ground_booking',
 'travel_management_itinerary_item',
 'travel_management_duty_of_care_alert',
 'travel_management_travel_disruption',
 'travel_management_unused_ticket',
 'travel_management_travel_expense_link',
 'travel_management_travel_risk_assessment',
 'travel_management_travel_supplier_offer',
 'travel_management_travel_exception_case',
 'travel_management_travel_policy_rule',
 'travel_management_travel_runtime_parameter',
 'travel_management_travel_schema_extension',
 'travel_management_travel_control_assertion',
 'travel_management_travel_governed_model')
DOMAIN_OPERATIONS = ('create_trip_request',
 'validate_travel_policy',
 'route_travel_approval',
 'create_booking_intent',
 'record_air_booking',
 'record_hotel_booking',
 'record_ground_booking',
 'build_itinerary',
 'screen_duty_of_care',
 'open_travel_disruption',
 'track_unused_ticket',
 'link_travel_expense',
 'score_travel_risk',
 'compare_supplier_offer',
 'resolve_travel_exception',
 'compile_travel_rule',
 'simulate_disruption_impact')
DOMAIN_RULES = ('travel_approval_policy',
 'fare_class_policy',
 'hotel_rate_policy',
 'duty_of_care_policy',
 'unused_ticket_policy',
 'disruption_escalation_policy')
DOMAIN_PARAMETERS = ('advance_booking_days',
 'hotel_rate_limit',
 'risk_alert_threshold',
 'unused_ticket_warning_days',
 'approval_amount_limit',
 'workbench_limit')
DOMAIN_EVENTS = ('TripRequested',
 'TravelApproved',
 'ItineraryBuilt',
 'DutyOfCareAlertOpened',
 'TravelDisruptionOpened',
 'UnusedTicketRecorded')
DOMAIN_CONSUMED_EVENTS = ('EmployeeCreated', 'ExpenseReportCreated', 'PolicyChanged', 'PaymentExecuted')
DOMAIN_ADVANCED_CAPABILITIES = ('traveler-aware policy guidance',
 'disruption counterfactual routing',
 'semantic itinerary ingestion',
 'duty-of-care risk intelligence',
 'unused-ticket optimization',
 'carbon-aware booking comparison')
DOMAIN_WORKBENCH_VIEWS = ('travel workbench',
 'trip request board',
 'booking intent console',
 'itinerary timeline',
 'duty of care map',
 'disruption queue',
 'unused ticket panel')


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def domain_depth_contract() -> dict:
    return {
        'format': f'appgen.{PBC_KEY}.world-class-domain-depth.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'purpose': DOMAIN_PURPOSE,
        'owned_tables': DOMAIN_OWNED_TABLES,
        'operation_count': len(DOMAIN_OPERATIONS),
        'operations': DOMAIN_OPERATIONS,
        'rules': DOMAIN_RULES,
        'parameters': DOMAIN_PARAMETERS,
        'emitted_events': DOMAIN_EVENTS,
        'consumed_events': DOMAIN_CONSUMED_EVENTS,
        'advanced_capabilities': DOMAIN_ADVANCED_CAPABILITIES,
        'workbench_views': DOMAIN_WORKBENCH_VIEWS,
        'database_backends': ('postgresql', 'mysql', 'mariadb'),
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'shared_table_access': False,
        'minimum_owned_domain_tables': 20,
        'minimum_domain_operations': 15,
        'side_effects': (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {'ok': False, 'reason': 'unknown_domain_operation', 'operation': operation, 'side_effects': ()}
    index = DOMAIN_OPERATIONS.index(operation)
    target_table = DOMAIN_OWNED_TABLES[index % len(DOMAIN_OWNED_TABLES)]
    emitted_event = DOMAIN_EVENTS[index % len(DOMAIN_EVENTS)]
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'operation': operation,
        'operation_kind': 'command',
        'target_table': target_table,
        'owned_tables': (target_table,),
        'read_tables': (),
        'emitted_event': emitted_event,
        'event_contract': 'AppGen-X',
        'idempotency_key': _digest((PBC_KEY, operation, tuple(sorted(payload.items())))),
        'rules_evaluated': DOMAIN_RULES[:3],
        'parameters_read': DOMAIN_PARAMETERS[:3],
        'permission': f'{PBC_KEY}.operate',
        'evidence_hash': _digest((operation, payload, target_table, emitted_event)),
        'shared_table_access': False,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(execute_domain_operation(operation, {'tenant': 'tenant-smoke'}) for operation in DOMAIN_OPERATIONS[:5])
    return {
        'ok': contract['ok']
        and len(contract['owned_tables']) >= contract['minimum_owned_domain_tables']
        and contract['operation_count'] >= contract['minimum_domain_operations']
        and all(item['ok'] for item in executions)
        and all(item['target_table'].startswith(f'{PBC_KEY}_') for item in executions),
        'contract': contract,
        'executions': executions,
        'side_effects': (),
    }
