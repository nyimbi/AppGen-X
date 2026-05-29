"""UI contracts and standalone workbench rendering for energy_grid_operations."""

from __future__ import annotations

from .domain_depth import domain_capability_surface_contract
from .runtime import (
    DEFAULT_CONFIGURATION,
    ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES,
    ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES,
    ENERGY_GRID_OPERATIONS_OWNED_TABLES,
    ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
    ENERGY_GRID_OPERATIONS_RUNTIME_TABLES,
    ENERGY_GRID_OPERATIONS_UI_FRAGMENT_KEYS,
    PARAMETER_DEFINITIONS,
    PERMISSION_MAP,
    PBC_KEY,
    RULE_DEFINITIONS,
    energy_grid_operations_build_workbench_view,
    energy_grid_operations_empty_state,
    energy_grid_operations_permissions_contract,
)

ENERGY_GRID_OPERATIONS_FORM_KEYS = (
    "grid_asset_intake_form",
    "topology_publish_form",
    "switching_order_form",
    "dispatch_instruction_form",
    "outage_restoration_form",
    "reliability_constraint_form",
    "policy_rule_form",
    "assistant_document_form",
)
ENERGY_GRID_OPERATIONS_WIZARD_KEYS = (
    "feeder_modeling_wizard",
    "planned_switching_wizard",
    "outage_restoration_wizard",
    "release_readiness_wizard",
)
ENERGY_GRID_OPERATIONS_CONTROL_KEYS = (
    "tenant_scope_picker",
    "feeder_tree",
    "switching_step_timeline",
    "dispatch_conflict_banner",
    "restoration_priority_queue",
    "event_stream_timeline",
    "release_gate_drawer",
)


def energy_grid_operations_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "grid_asset_intake_form",
            "title": "Grid Asset Intake",
            "command": "create_grid_asset",
            "fields": ("asset_id", "tenant", "asset_type", "asset_name", "voltage_kv", "substation_id", "feeder_id", "normal_state", "gis_reference", "scada_points"),
        },
        {
            "key": "topology_publish_form",
            "title": "Topology Publication",
            "command": "record_grid_topology",
            "fields": ("topology_id", "tenant", "feeder_id", "source_asset_id", "energized_sections", "normally_open_ties", "backfeed_paths", "phase_map"),
        },
        {
            "key": "switching_order_form",
            "title": "Switching Order Review",
            "command": "review_switching_order",
            "fields": ("switching_order_id", "tenant", "feeder_id", "substation_id", "clearance_id", "requested_by", "steps"),
        },
        {
            "key": "dispatch_instruction_form",
            "title": "Dispatch Instruction",
            "command": "approve_dispatch_instruction",
            "fields": ("dispatch_instruction_id", "tenant", "objective_type", "feeder_id", "target_asset_id", "expected_load_shift_mw", "telemetry_freshness_seconds", "rollback_conditions"),
        },
        {
            "key": "outage_restoration_form",
            "title": "Outage Restoration",
            "command": "simulate_outage_event",
            "fields": ("outage_event_id", "tenant", "feeder_id", "substation_id", "cause", "affected_customers", "eta_minutes", "crew_status"),
        },
        {
            "key": "reliability_constraint_form",
            "title": "Reliability Constraint",
            "command": "create_reliability_constraint",
            "fields": ("constraint_id", "tenant", "constraint_type", "scope_id", "scope_level", "severity", "limit_value"),
        },
        {
            "key": "policy_rule_form",
            "title": "Policy Rule",
            "command": "review_energy_grid_operations_policy_rule",
            "fields": ("rule_id", "tenant", "scope", "policy_version", "required_fields", "required_approver_role"),
        },
        {
            "key": "assistant_document_form",
            "title": "Assistant Intake",
            "command": "document_instruction_plan",
            "fields": ("document", "instruction"),
        },
    )


def energy_grid_operations_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "feeder_modeling_wizard",
            "steps": ("grid_asset_intake_form", "topology_publish_form", "reliability_constraint_form"),
            "goal": "Model one feeder, its topology, and its active operating constraints inside the standalone package.",
        },
        {
            "key": "planned_switching_wizard",
            "steps": ("switching_order_form", "dispatch_instruction_form", "policy_rule_form"),
            "goal": "Simulate one switching and dispatch plan before the dispatcher approves it.",
        },
        {
            "key": "outage_restoration_wizard",
            "steps": ("outage_restoration_form", "dispatch_instruction_form", "assistant_document_form"),
            "goal": "Capture outage state, recommend restoration action, and explain operator follow-up work.",
        },
        {
            "key": "release_readiness_wizard",
            "steps": ("policy_rule_form", "reliability_constraint_form", "assistant_document_form"),
            "goal": "Collect governance evidence and release readiness proof for the package-local workbench.",
        },
    )


def energy_grid_operations_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "feeder_tree", "type": "tree", "binds_to": "grid_asset"},
        {"key": "switching_step_timeline", "type": "timeline", "binds_to": "switching_order"},
        {"key": "dispatch_conflict_banner", "type": "banner", "binds_to": "dispatch_instruction"},
        {"key": "restoration_priority_queue", "type": "queue", "binds_to": "outage_event"},
        {"key": "event_stream_timeline", "type": "timeline", "binds_to": "events"},
        {"key": "release_gate_drawer", "type": "drawer", "binds_to": "release_evidence"},
    )


def energy_grid_operations_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_id": "energy_grid_operations_one_pbc_app",
        "workbench_route": "/app/energy-grid-operations/workbench",
        "navigation": (
            {"key": "overview", "route": "/app/energy-grid-operations/workbench"},
            {"key": "assets", "route": "/workbench/pbcs/energy_grid_operations/assets"},
            {"key": "switching", "route": "/workbench/pbcs/energy_grid_operations/switching"},
            {"key": "dispatch", "route": "/workbench/pbcs/energy_grid_operations/dispatch"},
            {"key": "outages", "route": "/workbench/pbcs/energy_grid_operations/outages"},
            {"key": "governance", "route": "/workbench/pbcs/energy_grid_operations/governance"},
            {"key": "release", "route": "/workbench/pbcs/energy_grid_operations/release"},
        ),
        "forms": ENERGY_GRID_OPERATIONS_FORM_KEYS,
        "wizards": ENERGY_GRID_OPERATIONS_WIZARD_KEYS,
        "controls": ENERGY_GRID_OPERATIONS_CONTROL_KEYS,
        "single_agent_namespace": f"{PBC_KEY}_skills",
        "side_effects": (),
    }


def energy_grid_operations_ui_contract() -> dict:
    permissions = energy_grid_operations_permissions_contract()
    return {
        "format": "appgen.energy-grid-operations-ui-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "fragments": ENERGY_GRID_OPERATIONS_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in energy_grid_operations_standalone_app_contract()["navigation"]),
        "forms": energy_grid_operations_form_catalog(),
        "wizards": energy_grid_operations_wizard_catalog(),
        "controls": energy_grid_operations_control_catalog(),
        "standalone_app": energy_grid_operations_standalone_app_contract(),
        "configuration_editor": {
            "required_fields": tuple(DEFAULT_CONFIGURATION),
            "allowed_database_backends": ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_eventing_choice": False,
        },
        "parameter_editor": {
            "parameters": tuple(PARAMETER_DEFINITIONS),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rules": tuple(RULE_DEFINITIONS),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES,
            "consumes": ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "action_permissions": PERMISSION_MAP,
        "binding_evidence": {
            "owned_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES,
            "runtime_tables": ENERGY_GRID_OPERATIONS_RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "required_event_topic": ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "shared_table_access": False,
        },
        "full_capability_surface": domain_capability_surface_contract(),
        "permission_contract": permissions,
        "side_effects": (),
    }


def energy_grid_operations_render_workbench(
    state: dict | None = None,
    *,
    tenant: str = "tenant_demo",
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    current_state = energy_grid_operations_empty_state() if state is None else state
    shell = energy_grid_operations_standalone_app_contract()
    contract = energy_grid_operations_ui_contract()
    snapshot = energy_grid_operations_build_workbench_view(current_state, {"tenant": tenant})
    allowed = set(principal_permissions or contract["permission_contract"]["permission_set"])
    visible_actions = tuple(
        action for action, permission in contract["action_permissions"].items() if permission in allowed
    )
    return {
        "format": "appgen.energy-grid-operations-workbench-render.v2",
        "ok": snapshot["ok"],
        "tenant": tenant,
        "route": shell["workbench_route"],
        "shell": shell,
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "workbench": {
            "cards": snapshot["cards"],
            "queues": snapshot["queues"],
            "configuration_bound": snapshot["configuration_bound"],
            "parameters_bound": snapshot["parameters_bound"],
            "rules_bound": snapshot["rules_bound"],
            "owned_tables": snapshot["owned_tables"],
            "highlight_feeders": tuple(
                item for item in snapshot["queues"]["restoration_priority"] if item
            ),
        },
        "binding_evidence": contract["binding_evidence"],
        "side_effects": (),
    }


def energy_grid_operations_render_standalone_app(
    state: dict | None = None,
    *,
    tenant: str = "tenant_demo",
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    return energy_grid_operations_render_workbench(
        state,
        tenant=tenant,
        principal_permissions=principal_permissions,
    )


def smoke_test() -> dict:
    rendered = energy_grid_operations_render_workbench(tenant="tenant_ui")
    return {
        "ok": energy_grid_operations_ui_contract()["ok"] and rendered["ok"] and bool(rendered["forms"]) and bool(rendered["wizards"]) and bool(rendered["controls"]),
        "side_effects": (),
    }
