"""Domain-depth metadata and capability surfaces for energy_grid_operations."""

from __future__ import annotations

from .runtime import (
    ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    ENERGY_GRID_OPERATIONS_BUSINESS_TABLES,
    ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES,
    ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES,
    ENERGY_GRID_OPERATIONS_OWNED_TABLES,
    ENERGY_GRID_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
    DOMAIN_OPERATIONS as RUNTIME_DOMAIN_OPERATIONS,
    PARAMETER_DEFINITIONS,
    PBC_KEY,
    RULE_DEFINITIONS,
    energy_grid_operations_operation_preview,
)

DOMAIN_ENTITY = "grid_asset"
DOMAIN_PURPOSE = (
    "Control-room operations for feeder and substation assets, topology, switching, "
    "dispatch, outage restoration, reliability constraints, and governed automation."
)
DOMAIN_OWNED_TABLES = ENERGY_GRID_OPERATIONS_OWNED_TABLES
DOMAIN_OPERATIONS = RUNTIME_DOMAIN_OPERATIONS
DOMAIN_RULES = tuple(item["rule_id"] for item in RULE_DEFINITIONS)
DOMAIN_PARAMETERS = tuple(item["name"] for item in PARAMETER_DEFINITIONS)
DOMAIN_EVENTS = ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES
DOMAIN_CONSUMED_EVENTS = ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES
DOMAIN_ADVANCED_CAPABILITIES = ENERGY_GRID_OPERATIONS_RUNTIME_CAPABILITY_KEYS
DOMAIN_WORKBENCH_VIEWS = (
    "grid asset board",
    "switching order workbench",
    "dispatch coordination board",
    "outage restoration queue",
    "governance and release evidence",
)
DOMAIN_EDGE_CASES = (
    "asset_quality_below_floor",
    "missing_topology_for_switching",
    "backfeed_risk_detected",
    "stale_dispatch_telemetry",
    "constraint_conflict",
    "policy_reapproval_required",
    "dead_letter_event",
    "cross_tenant_access_attempt",
)
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    list(DOMAIN_ADVANCED_CAPABILITIES)
    + [f"grid_operator.{operation}" for operation in DOMAIN_OPERATIONS]
    + [f"grid_policy.{rule}" for rule in DOMAIN_RULES]
)


def domain_depth_contract() -> dict:
    return {
        "format": "appgen.energy-grid-operations-world-class-domain-depth.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "entity": DOMAIN_ENTITY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "business_tables": ENERGY_GRID_OPERATIONS_BUSINESS_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "database_backends": ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "minimum_owned_domain_tables": 15,
        "minimum_domain_operations": 10,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    preview = energy_grid_operations_operation_preview(operation, payload)
    if not preview["ok"]:
        return preview
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": preview["operation_kind"],
        "target_table": preview.get("owned_tables", (None,))[0],
        "owned_tables": preview.get("owned_tables", ()),
        "read_tables": preview.get("read_tables", ()),
        "emitted_event": preview.get("emitted_event"),
        "permission": preview.get("permission"),
        "event_contract": preview.get("event_contract"),
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def domain_capability_surface_contract() -> dict:
    return {
        "format": "appgen.energy-grid-operations-capability-surface.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": operation,
                "surface": f"{PBC_KEY}.ui.operation.{operation}",
                "action": operation,
                "target_table": execute_domain_operation(operation).get("target_table"),
                "permission": execute_domain_operation(operation).get("permission"),
                "requires_confirmation": operation not in {"record_load_forecast", "record_grid_topology"},
                "event": execute_domain_operation(operation).get("emitted_event"),
            }
            for operation in DOMAIN_OPERATIONS
        ),
        "rule_surfaces": tuple(
            {
                "rule": rule,
                "surface": f"{PBC_KEY}.ui.rule.{rule}",
                "editor": True,
                "explainable": True,
            }
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": parameter,
                "surface": f"{PBC_KEY}.ui.parameter.{parameter}",
                "bounded": True,
                "editable": True,
            }
            for parameter in DOMAIN_PARAMETERS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{capability}",
                "explainable": True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        "edge_case_surfaces": tuple(
            {
                "edge_case": edge_case,
                "surface": f"{PBC_KEY}.ui.edge-case.{edge_case}",
                "triage_queue": True,
            }
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        "specialist_capabilities": DOMAIN_SPECIALIST_CAPABILITIES,
        "coverage": {
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        },
        "side_effects": (),
    }
