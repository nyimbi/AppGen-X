"""UI contract and standalone workbench surface for airline_operations_control."""

from __future__ import annotations

from .permissions import ACTION_PERMISSIONS
from .runtime import AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS
from .runtime import AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES
from .runtime import AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES
from .runtime import AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES
from .runtime import AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC
from .runtime import AIRLINE_OPERATIONS_CONTROL_RUNTIME_TABLES
from .runtime import airline_operations_control_build_workbench_view
from .runtime import airline_operations_control_permissions_contract


AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS = (
    "AirlineOperationsControlWorkbench",
    "AirlineOperationsControlDetail",
    "AirlineOperationsControlAssistantPanel",
    "AirlineOperationsControlRecoveryConsole",
    "AirlineOperationsControlReleaseWorkbench",
)
AIRLINE_OPERATIONS_CONTROL_FORM_KEYS = (
    "flight_leg_form",
    "rotation_simulation_form",
    "crew_pairing_form",
    "disruption_event_form",
    "reaccommodation_form",
    "decision_pack_form",
    "delay_code_form",
    "document_instruction_form",
)
AIRLINE_OPERATIONS_CONTROL_WIZARD_KEYS = (
    "disruption_recovery_wizard",
    "tail_swap_wizard",
    "reaccommodation_wizard",
)
AIRLINE_OPERATIONS_CONTROL_CONTROL_KEYS = (
    "tenant_scope_picker",
    "role_view_selector",
    "tail_rotation_graph",
    "timeline_scrubber",
    "turn_watchlist_grid",
    "assistant_planning_drawer",
    "release_evidence_drawer",
)


def airline_operations_control_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "flight_leg_form",
            "title": "Flight Leg Intake",
            "command": "command_flight_leg",
            "fields": ("id", "tenant", "flight_number", "tail_number", "origin", "destination", "scheduled_departure_at", "scheduled_arrival_at", "leg_type"),
        },
        {
            "key": "rotation_simulation_form",
            "title": "Rotation Recovery",
            "command": "record_aircraft_rotation",
            "fields": ("rotation_id", "tenant", "tail_number", "leg_ids", "spare_tail_candidates", "maintenance_stop_station"),
        },
        {
            "key": "crew_pairing_form",
            "title": "Crew Pairing Projection",
            "command": "command_crew_pairing",
            "fields": ("crew_pairing_id", "tenant", "remaining_duty_minutes", "legality_state", "reserve_activation_required"),
        },
        {
            "key": "disruption_event_form",
            "title": "Disruption Intake",
            "command": "command_disruption_event",
            "fields": ("disruption_event_id", "tenant", "event_type", "severity", "affected_leg_ids", "source_lineage"),
        },
        {
            "key": "reaccommodation_form",
            "title": "Passenger Recovery",
            "command": "command_reaccommodation_plan",
            "fields": ("reaccommodation_plan_id", "tenant", "passenger_count", "manual_review_required", "blocked_reason"),
        },
        {
            "key": "decision_pack_form",
            "title": "Operations Decision Journal",
            "command": "command_operations_decision",
            "fields": ("operations_decision_id", "tenant", "decision_type", "selected_action", "alternatives", "approval_state"),
        },
        {
            "key": "delay_code_form",
            "title": "Delay Code Journal",
            "command": "record_delay_code",
            "fields": ("delay_code_id", "tenant", "primary_code", "contributing_codes"),
        },
        {
            "key": "document_instruction_form",
            "title": "Assistant Document Intake",
            "command": "document_instruction_plan",
            "fields": ("document", "instruction"),
        },
    )


def airline_operations_control_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "disruption_recovery_wizard",
            "steps": ("disruption_event_form", "rotation_simulation_form", "decision_pack_form", "reaccommodation_form"),
            "goal": "Stabilize one irregular-operations event and publish a governed recovery decision.",
        },
        {
            "key": "tail_swap_wizard",
            "steps": ("flight_leg_form", "rotation_simulation_form", "crew_pairing_form", "decision_pack_form"),
            "goal": "Compare and record tail swap options before a broken turn propagates.",
        },
        {
            "key": "reaccommodation_wizard",
            "steps": ("disruption_event_form", "reaccommodation_form", "decision_pack_form", "document_instruction_form"),
            "goal": "Route passenger recovery through policy-aware review boundaries.",
        },
    )


def airline_operations_control_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "role_view_selector", "type": "segment", "binds_to": "role_view"},
        {"key": "tail_rotation_graph", "type": "graph", "binds_to": "tail_graphs"},
        {"key": "timeline_scrubber", "type": "timeline", "binds_to": "legs"},
        {"key": "turn_watchlist_grid", "type": "table", "binds_to": "turn_watchlist"},
        {"key": "assistant_planning_drawer", "type": "drawer", "binds_to": "assistant_plan"},
        {"key": "release_evidence_drawer", "type": "drawer", "binds_to": "release_evidence"},
    )


def airline_operations_control_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "airline_operations_control",
        "app_id": "airline_operations_control_one_pbc_app",
        "workbench_route": "/workbench/pbcs/airline_operations_control",
        "navigation": (
            {"key": "network", "route": "/workbench/pbcs/airline_operations_control/network"},
            {"key": "tails", "route": "/workbench/pbcs/airline_operations_control/tails"},
            {"key": "crew", "route": "/workbench/pbcs/airline_operations_control/crew"},
            {"key": "disruptions", "route": "/workbench/pbcs/airline_operations_control/disruptions"},
            {"key": "customer", "route": "/workbench/pbcs/airline_operations_control/customer"},
            {"key": "release", "route": "/workbench/pbcs/airline_operations_control/release"},
        ),
        "forms": AIRLINE_OPERATIONS_CONTROL_FORM_KEYS,
        "wizards": AIRLINE_OPERATIONS_CONTROL_WIZARD_KEYS,
        "controls": AIRLINE_OPERATIONS_CONTROL_CONTROL_KEYS,
        "single_agent_namespace": "airline_operations_control_skills",
        "side_effects": (),
    }


def airline_operations_control_ui_contract() -> dict:
    return {
        "format": "appgen.airline-operations-control-ui-contract.v2",
        "ok": True,
        "pbc": "airline_operations_control",
        "implementation_directory": "src/pyAppGen/pbcs/airline_operations_control",
        "fragments": AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in airline_operations_control_standalone_app_contract()["navigation"]) + (
            "/workbench/pbcs/airline_operations_control",
        ),
        "panels": (
            {"key": "network", "fragment": "AirlineOperationsControlWorkbench", "binds_to": ("flight_leg", "aircraft_rotation", "operations_decision"), "commands": ("command_flight_leg", "record_aircraft_rotation", "command_operations_decision")},
            {"key": "crew", "fragment": "AirlineOperationsControlDetail", "binds_to": ("crew_pairing",), "commands": ("command_crew_pairing",)},
            {"key": "disruptions", "fragment": "AirlineOperationsControlRecoveryConsole", "binds_to": ("disruption_event", "reaccommodation_plan"), "commands": ("command_disruption_event", "command_reaccommodation_plan", "plan_recovery_workflow")},
            {"key": "assistant", "fragment": "AirlineOperationsControlAssistantPanel", "binds_to": ("operations_decision", "delay_code"), "commands": ("document_instruction_plan", "record_delay_code")},
            {"key": "release", "fragment": "AirlineOperationsControlReleaseWorkbench", "binds_to": AIRLINE_OPERATIONS_CONTROL_RUNTIME_TABLES, "commands": ("query_schema_contract", "query_service_contract", "query_release_evidence")},
        ),
        "forms": airline_operations_control_form_catalog(),
        "wizards": airline_operations_control_wizard_catalog(),
        "controls": airline_operations_control_control_catalog(),
        "standalone_app": airline_operations_control_standalone_app_contract(),
        "action_permissions": airline_operations_control_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "control_center", "workbench_limit", "assistant_requires_confirmation", "tenant_isolation_mode"),
            "allowed_database_backends": AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_eventing_choice": False,
        },
        "parameter_editor": {
            "numeric_parameters": ("quality_score_floor", "materiality_threshold", "approval_sla_hours", "risk_threshold", "forecast_horizon_days", "workbench_limit"),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("flight_leg_policy", "rotation_recovery_policy", "crew_legality_policy", "reaccommodation_boundary_policy"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES,
            "consumes": AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES,
            "runtime_tables": AIRLINE_OPERATIONS_CONTROL_RUNTIME_TABLES,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
            "required_event_topic": AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC,
        },
    }


def airline_operations_control_render_standalone_app(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = airline_operations_control_ui_contract()
    shell = airline_operations_control_standalone_app_contract()
    snapshot = airline_operations_control_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in ACTION_PERMISSIONS.items()
        if required_permission in permissions
    )
    return {
        "format": "appgen.airline-operations-control-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "shell": {
            "app_id": shell["app_id"],
            "title": "Airline Operations Control",
            "role_views": ("network_control", "crew_control", "station_control", "customer_recovery"),
        },
        "navigation": shell["navigation"],
        "fragments": contract["fragments"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "workbench": snapshot,
        "cards": snapshot["summary_cards"],
        "attention_queue": snapshot["workbench"]["attention_queue"],
        "turn_watchlist": snapshot["workbench"]["turn_watchlist"],
        "tail_graphs": snapshot["workbench"]["tail_graphs"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in ACTION_PERMISSIONS if action not in visible_actions),
        "decision_support_panels": snapshot["decision_support_panels"],
        "assistant_panel": {
            "namespace": shell["single_agent_namespace"],
            "document_intake_enabled": True,
            "crud_preview_enabled": True,
        },
        "binding_evidence": contract["binding_evidence"],
        "side_effects": (),
    }


def airline_operations_control_render_workbench(
    state: dict | None = None,
    tenant: str = "default",
    flight_legs: tuple[dict, ...] = (),
    aircraft_rotations: tuple[dict, ...] = (),
    principal_permissions: tuple[str, ...] | None = None,
):
    permissions = principal_permissions or tuple(sorted(set(ACTION_PERMISSIONS.values())))
    if state is None:
        snapshot = airline_operations_control_build_workbench_view(
            tenant=tenant,
            flight_legs=flight_legs,
            aircraft_rotations=aircraft_rotations,
        )
        return {
            "ok": True,
            "pbc": "airline_operations_control",
            "route": f"/workbench/pbcs/airline_operations_control",
            "decision_support_panels": snapshot["decision_support_panels"],
            "attention_queue": snapshot["workbench"]["attention_queue"],
            "turn_watchlist": snapshot["workbench"]["turn_watchlist"],
            "workbench": snapshot["workbench"],
            "summary_cards": snapshot["summary_cards"],
            "side_effects": (),
        }
    return airline_operations_control_render_standalone_app(state, tenant=tenant, principal_permissions=permissions)


def smoke_test():
    contract = airline_operations_control_ui_contract()
    rendered = airline_operations_control_render_workbench(tenant="tenant-smoke", flight_legs=(), aircraft_rotations=())
    return {"ok": contract["ok"] and rendered["ok"], "contract": contract, "rendered": rendered, "side_effects": ()}
