"""UI contract and standalone workbench surface for rail_operations_management."""

from __future__ import annotations

from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OPERATIONS, DOMAIN_PARAMETERS, DOMAIN_RULES
from .permissions import ACTION_PERMISSIONS
from .runtime import (
    DEFAULT_CONFIGURATION,
    RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES,
    RAIL_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES,
    RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES,
    RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES,
    rail_operations_management_build_workbench_view,
    rail_operations_management_empty_state,
    rail_operations_management_permissions_contract,
)


RAIL_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS = (
    'RailOperationsManagementWorkbench',
    'RailOperationsManagementDetail',
    'RailOperationsManagementAssistantPanel',
    'RailOperationsManagementDispatchConsole',
    'RailOperationsManagementReleaseWorkbench',
)
RAIL_OPERATIONS_MANAGEMENT_FORM_KEYS = (
    'train_plan_form',
    'route_path_form',
    'consist_form',
    'crew_assignment_form',
    'dispatch_decision_form',
    'restriction_form',
    'yard_terminal_form',
    'incident_form',
    'service_plan_form',
    'energy_sla_form',
    'document_instruction_form',
)
RAIL_OPERATIONS_MANAGEMENT_WIZARD_KEYS = (
    'dispatch_recovery_wizard',
    'terminal_turnback_wizard',
    'incident_handover_wizard',
)
RAIL_OPERATIONS_MANAGEMENT_CONTROL_KEYS = (
    'tenant_scope_picker',
    'corridor_selector',
    'dispatch_timeline',
    'yard_ladder_grid',
    'terminal_occupation_timeline',
    'assistant_preview_drawer',
    'release_evidence_drawer',
)


def rail_operations_management_form_catalog() -> tuple[dict, ...]:
    return (
        {
            'key': 'train_plan_form',
            'title': 'Train Plan Intake',
            'command': 'command_train_plan',
            'fields': ('tenant', 'train_id', 'service_type', 'published_departure_at', 'working_departure_at', 'control_departure_at', 'line_id', 'path_id'),
        },
        {
            'key': 'route_path_form',
            'title': 'Route Pathing',
            'command': 'record_route_path',
            'fields': ('tenant', 'path_id', 'line_id', 'primary_path', 'fallback_paths', 'junctions', 'headway_minutes'),
        },
        {
            'key': 'consist_form',
            'title': 'Consist and Rolling Stock',
            'command': 'record_consist',
            'fields': ('tenant', 'consist_id', 'train_id', 'locomotive_class', 'vehicle_order', 'length_meters', 'trailing_tonnage'),
        },
        {
            'key': 'crew_assignment_form',
            'title': 'Crew Assignment',
            'command': 'command_crew_assignment',
            'fields': ('tenant', 'assignment_id', 'train_id', 'driver_id', 'conductor_id', 'remaining_legal_minutes', 'handover_station'),
        },
        {
            'key': 'dispatch_decision_form',
            'title': 'Dispatch Decision',
            'command': 'command_dispatch_decision',
            'fields': ('tenant', 'decision_id', 'train_id', 'selected_action', 'hold_reason', 'approved_by'),
        },
        {
            'key': 'restriction_form',
            'title': 'Signal, Track, and Maintenance Restriction',
            'command': 'register_signal_restriction',
            'fields': ('tenant', 'restriction_id', 'line_id', 'start_point', 'end_point', 'restriction_type', 'severity'),
        },
        {
            'key': 'yard_terminal_form',
            'title': 'Yard and Terminal Workflow',
            'command': 'review_yard_plan',
            'fields': ('tenant', 'yard_plan_id', 'origin_track', 'destination_track', 'terminal_id', 'platform_id', 'status'),
        },
        {
            'key': 'incident_form',
            'title': 'Incident Command',
            'command': 'command_incident_response',
            'fields': ('tenant', 'incident_id', 'severity', 'location', 'protection_state', 'handover_summary'),
        },
        {
            'key': 'service_plan_form',
            'title': 'Passenger or Freight Recovery',
            'command': 'plan_passenger_service',
            'fields': ('tenant', 'plan_id', 'service_type', 'impacted_trains', 'playbook', 'approval_state'),
        },
        {
            'key': 'energy_sla_form',
            'title': 'Energy and Reliability Analytics',
            'command': 'record_energy_profile',
            'fields': ('tenant', 'record_id', 'energy_kwh', 'carbon_kg', 'status', 'reliability_score'),
        },
        {
            'key': 'document_instruction_form',
            'title': 'Assistant Document Intake',
            'command': 'preview_document_instruction',
            'fields': ('document', 'instruction'),
        },
    )


def rail_operations_management_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            'key': 'dispatch_recovery_wizard',
            'steps': ('train_plan_form', 'route_path_form', 'dispatch_decision_form', 'service_plan_form', 'document_instruction_form'),
            'goal': 'Stabilize a corridor conflict with timetable, dispatch, and passenger or freight recovery evidence.',
        },
        {
            'key': 'terminal_turnback_wizard',
            'steps': ('yard_terminal_form', 'consist_form', 'crew_assignment_form', 'dispatch_decision_form'),
            'goal': 'Rebuild a terminal turnback with stock, crew, yard, and platform constraints in one flow.',
        },
        {
            'key': 'incident_handover_wizard',
            'steps': ('incident_form', 'restriction_form', 'service_plan_form', 'document_instruction_form'),
            'goal': 'Package an incident chronology, protection state, and next actions for the next control shift.',
        },
    )


def rail_operations_management_control_catalog() -> tuple[dict, ...]:
    return (
        {'key': 'tenant_scope_picker', 'type': 'selector', 'binds_to': 'tenant'},
        {'key': 'corridor_selector', 'type': 'segment', 'binds_to': 'corridor'},
        {'key': 'dispatch_timeline', 'type': 'timeline', 'binds_to': 'dispatch_board'},
        {'key': 'yard_ladder_grid', 'type': 'table', 'binds_to': 'yard_board'},
        {'key': 'terminal_occupation_timeline', 'type': 'timeline', 'binds_to': 'terminal_board'},
        {'key': 'assistant_preview_drawer', 'type': 'drawer', 'binds_to': 'assistant_center'},
        {'key': 'release_evidence_drawer', 'type': 'drawer', 'binds_to': 'release_evidence'},
    )


def rail_operations_management_standalone_app_contract() -> dict:
    return {
        'ok': True,
        'pbc': 'rail_operations_management',
        'app_id': 'rail_operations_management_one_pbc_app',
        'workbench_route': '/workbench/pbcs/rail_operations_management',
        'navigation': (
            {'key': 'corridor', 'route': '/workbench/pbcs/rail_operations_management/corridor'},
            {'key': 'yards', 'route': '/workbench/pbcs/rail_operations_management/yards'},
            {'key': 'terminals', 'route': '/workbench/pbcs/rail_operations_management/terminals'},
            {'key': 'incidents', 'route': '/workbench/pbcs/rail_operations_management/incidents'},
            {'key': 'analytics', 'route': '/workbench/pbcs/rail_operations_management/analytics'},
            {'key': 'assistant', 'route': '/workbench/pbcs/rail_operations_management/assistant'},
            {'key': 'release', 'route': '/workbench/pbcs/rail_operations_management/release'},
        ),
        'forms': RAIL_OPERATIONS_MANAGEMENT_FORM_KEYS,
        'wizards': RAIL_OPERATIONS_MANAGEMENT_WIZARD_KEYS,
        'controls': RAIL_OPERATIONS_MANAGEMENT_CONTROL_KEYS,
        'single_agent_namespace': 'rail_operations_management_skills',
        'side_effects': (),
    }


def rail_operations_management_ui_contract() -> dict:
    return {
        'format': 'appgen.rail-operations-management-ui-contract.v2',
        'ok': True,
        'pbc': 'rail_operations_management',
        'implementation_directory': 'src/pyAppGen/pbcs/rail_operations_management',
        'fragments': RAIL_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS,
        'routes': tuple(item['route'] for item in rail_operations_management_standalone_app_contract()['navigation']) + ('/workbench/pbcs/rail_operations_management',),
        'panels': (
            {'key': 'corridor', 'fragment': 'RailOperationsManagementDispatchConsole', 'binds_to': ('train_plan', 'route_path', 'dispatch_decision', 'capacity_conflict'), 'commands': ('command_train_plan', 'record_route_path', 'command_dispatch_decision', 'resolve_capacity_conflict')},
            {'key': 'stock_and_crew', 'fragment': 'RailOperationsManagementDetail', 'binds_to': ('consist', 'rolling_stock_unit', 'crew_assignment'), 'commands': ('record_consist', 'register_rolling_stock_unit', 'command_crew_assignment')},
            {'key': 'yard_and_terminal', 'fragment': 'RailOperationsManagementWorkbench', 'binds_to': ('yard_plan', 'terminal_slot', 'maintenance_window'), 'commands': ('review_yard_plan', 'approve_terminal_slot', 'schedule_maintenance_window')},
            {'key': 'incident', 'fragment': 'RailOperationsManagementAssistantPanel', 'binds_to': ('disruption_event', 'incident_response', 'safety_rule'), 'commands': ('command_disruption_event', 'command_incident_response', 'register_safety_rule')},
            {'key': 'analytics', 'fragment': 'RailOperationsManagementReleaseWorkbench', 'binds_to': ('delay_event', 'energy_profile', 'sla_snapshot'), 'commands': ('record_delay_event', 'record_energy_profile', 'record_sla_snapshot')},
        ),
        'forms': rail_operations_management_form_catalog(),
        'wizards': rail_operations_management_wizard_catalog(),
        'controls': rail_operations_management_control_catalog(),
        'standalone_app': rail_operations_management_standalone_app_contract(),
        'action_permissions': rail_operations_management_permissions_contract()['action_permissions'],
        'configuration_editor': {
            'required_fields': tuple(DEFAULT_CONFIGURATION.keys()),
            'allowed_database_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            'required_event_topic': RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
            'user_eventing_choice': False,
        },
        'parameter_editor': {
            'numeric_parameters': DOMAIN_PARAMETERS,
            'bounded_supported_parameters': True,
        },
        'rule_editor': {
            'rule_types': DOMAIN_RULES,
            'required_fields': ('rule_id', 'tenant', 'scope', 'status'),
            'compiled_evidence_required': True,
        },
        'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES,
        'event_surfaces': {
            'emits': RAIL_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES,
            'consumes': RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES,
            'outbox_status': 'visible',
            'inbox_status': 'visible',
            'dead_letter_status': 'visible',
        },
        'binding_evidence': {
            'owned_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES,
            'runtime_tables': RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES,
            'shared_table_access': False,
            'event_contract': 'AppGen-X',
            'required_event_topic': RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        },
    }


def rail_operations_management_render_standalone_app(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = rail_operations_management_ui_contract()
    shell = rail_operations_management_standalone_app_contract()
    snapshot = rail_operations_management_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required_permission in ACTION_PERMISSIONS.items() if required_permission in permissions)
    return {
        'format': 'appgen.rail-operations-management-workbench-render.v2',
        'ok': True,
        'tenant': tenant,
        'route': shell['workbench_route'],
        'shell': {
            'app_id': shell['app_id'],
            'title': 'Rail Operations Management',
            'role_views': ('network_dispatch', 'yardmaster', 'terminal_control', 'incident_command', 'service_recovery'),
        },
        'navigation': shell['navigation'],
        'fragments': contract['fragments'],
        'forms': contract['forms'],
        'wizards': contract['wizards'],
        'controls': contract['controls'],
        'workbench': snapshot,
        'cards': snapshot['summary_cards'],
        'dispatch_board': snapshot['dispatch_board'],
        'conflict_queue': snapshot['workbench']['conflict_queue'],
        'yard_board': snapshot['yard_board'],
        'terminal_board': snapshot['terminal_board'],
        'analytics': snapshot['analytics'],
        'visible_actions': visible_actions,
        'locked_actions': tuple(action for action in ACTION_PERMISSIONS if action not in visible_actions),
        'assistant_panel': {
            'namespace': shell['single_agent_namespace'],
            'document_intake_enabled': True,
            'crud_preview_enabled': True,
            'latest_preview_count': snapshot['assistant_center']['preview_count'],
        },
        'binding_evidence': contract['binding_evidence'],
        'side_effects': (),
    }


def rail_operations_management_render_workbench(state: dict | None = None, tenant: str = 'default', principal_permissions: tuple[str, ...] | None = None) -> dict:
    state = state or rail_operations_management_empty_state()
    permissions = principal_permissions or tuple(sorted(set(ACTION_PERMISSIONS.values())))
    return rail_operations_management_render_standalone_app(state, tenant=tenant, principal_permissions=permissions)


def smoke_test():
    rendered = rail_operations_management_render_workbench()
    return {'ok': rail_operations_management_ui_contract()['ok'] and rendered['ok'], 'side_effects': ()}
