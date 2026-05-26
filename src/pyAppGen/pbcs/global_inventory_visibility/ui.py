"""UI contract for the Global Inventory Visibility PBC."""

from __future__ import annotations

from .runtime import GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS
from .runtime import GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC
from .runtime import GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
from .runtime import global_inventory_visibility_permissions_contract


GLOBAL_INVENTORY_VISIBILITY_UI_FRAGMENT_KEYS = (
    "GlobalInventoryWorkbench",
    "InventoryPoolStudio",
    "SupplyNodeConsole",
    "AvailabilitySnapshotBoard",
    "GlobalAvailabilityConsole",
    "ProjectionLedgerView",
    "ReservationVisibilityPanel",
    "InTransitNetworkView",
    "FreshnessRiskPanel",
    "NodeHealthPanel",
    "PoolRuleStudio",
    "InventoryParameterConsole",
    "InventoryConfigurationPanel",
    "FederationEvidenceView",
    "DeadLetterAuditView",
)


def global_inventory_visibility_ui_contract() -> dict:
    return {
        "format": "appgen.global-inventory-visibility-ui-contract.v1",
        "ok": True,
        "pbc": "global_inventory_visibility",
        "implementation_directory": "src/pyAppGen/pbcs/global_inventory_visibility",
        "fragments": GLOBAL_INVENTORY_VISIBILITY_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/global_inventory_visibility",
            "/workbench/pbcs/global_inventory_visibility/pools",
            "/workbench/pbcs/global_inventory_visibility/nodes",
            "/workbench/pbcs/global_inventory_visibility/snapshots",
            "/workbench/pbcs/global_inventory_visibility/projections",
            "/workbench/pbcs/global_inventory_visibility/reservations",
            "/workbench/pbcs/global_inventory_visibility/in-transit",
            "/workbench/pbcs/global_inventory_visibility/freshness",
            "/workbench/pbcs/global_inventory_visibility/rules",
            "/workbench/pbcs/global_inventory_visibility/parameters",
            "/workbench/pbcs/global_inventory_visibility/configuration",
            "/workbench/pbcs/global_inventory_visibility/audit",
        ),
        "panels": (
            {
                "key": "master_data",
                "fragment": "InventoryPoolStudio",
                "binds_to": ("inventory_pool", "supply_node", "identity"),
                "commands": (
                    "register_inventory_pool",
                    "register_supply_node",
                    "verify_supply_identity",
                ),
            },
            {
                "key": "projection",
                "fragment": "GlobalAvailabilityConsole",
                "binds_to": ("availability_snapshot", "inventory_projection", "in_transit"),
                "commands": (
                    "record_availability_snapshot",
                    "project_availability",
                    "get_global_availability",
                    "route_projection",
                ),
            },
            {
                "key": "execution",
                "fragment": "ReservationVisibilityPanel",
                "binds_to": ("reservation", "allocation", "inbox", "outbox"),
                "commands": (
                    "reserve_inventory",
                    "ingest_event",
                    "simulate_counterfactual_allocation",
                    "resolve_exception",
                ),
            },
            {
                "key": "governance",
                "fragment": "PoolRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": (
                    "register_rule",
                    "set_parameter",
                    "configure_runtime",
                    "run_control_tests",
                ),
            },
            {
                "key": "audit",
                "fragment": "DeadLetterAuditView",
                "binds_to": ("dead_letter", "proof", "governed_model"),
                "commands": (
                    "generate_availability_proof",
                    "register_governed_model",
                    "federate_inventory_view",
                ),
            },
        ),
        "action_permissions": global_inventory_visibility_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "projection_horizon_days",
                "staleness_sla_minutes",
                "workbench_limit",
            ),
            "allowed_database_backends": GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_facing_stream_engine_picker": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "safety_stock_percent",
                "freshness_half_life_hours",
                "availability_confidence_floor",
                "reservation_ttl_minutes",
                "projection_horizon_days",
                "stockout_risk_threshold",
                "staleness_sla_minutes",
                "carbon_cost_weight",
                "federation_lag_tolerance_minutes",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": (
                "allocation",
                "availability",
                "freshness",
                "reservation",
                "projection_route",
                "exception_resolution",
            ),
            "required_fields": ("rule_id", "tenant", "scope", "status", "rule_type"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES,
            "consumes": GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
            "event_contract": "AppGen-X",
            "required_event_topic": GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
            "user_facing_stream_engine_picker": False,
        },
        "binding_evidence": {
            "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
            "runtime_tables": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES,
            "outbox_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[0],
            "inbox_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[1],
            "dead_letter_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[2],
            "required_event_topic": GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "shared_table_access": False,
        },
    }


def global_inventory_visibility_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = global_inventory_visibility_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required in contract["action_permissions"].items()
        if required in permissions
    )
    pools = tuple(
        pool for pool in state["inventory_pools"].values() if pool["tenant"] == tenant
    )
    projections = tuple(
        projection
        for projection in state["inventory_projections"].values()
        if projection["tenant"] == tenant
    )
    cards = (
        {"key": "pools", "value": len(pools), "fragment": "InventoryPoolStudio"},
        {
            "key": "nodes",
            "value": len(tuple(node for node in state["supply_nodes"].values() if node["tenant"] == tenant)),
            "fragment": "SupplyNodeConsole",
        },
        {
            "key": "available_to_promise",
            "value": round(sum(projection["available_to_promise"] for projection in projections), 2),
            "fragment": "GlobalAvailabilityConsole",
        },
        {
            "key": "in_transit",
            "value": round(sum(projection["in_transit"] for projection in projections), 2),
            "fragment": "InTransitNetworkView",
        },
        {
            "key": "rules",
            "value": len(tuple(rule for rule in state["rules"].values() if rule["tenant"] == tenant)),
            "fragment": "PoolRuleStudio",
        },
        {
            "key": "dead_letters",
            "value": len(state.get("dead_letters", ())),
            "fragment": "DeadLetterAuditView",
        },
    )
    return {
        "format": "appgen.global-inventory-visibility-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/global_inventory_visibility",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(
            action for action in contract["action_permissions"] if action not in visible_actions
        ),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(
            sorted(rule_id for rule_id, rule in state.get("rules", {}).items() if rule["tenant"] == tenant)
        ),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "binding_evidence": {
            "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
            "runtime_tables": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES,
            "outbox_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[0],
            "inbox_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[1],
            "dead_letter_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[2],
            "configuration": state.get("configuration", {}).get("event_topic"),
            "configuration_state": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
            "rule_hashes": tuple(
                sorted(
                    rule["compiled_hash"]
                    for rule in state.get("rules", {}).values()
                    if rule["tenant"] == tenant
                )
            ),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "ui_bindings": {
                "configuration_fragment": "InventoryConfigurationPanel",
                "rule_fragment": "PoolRuleStudio",
                "parameter_fragment": "InventoryParameterConsole",
                "workbench_fragment": "GlobalInventoryWorkbench",
                "rbac": contract["action_permissions"],
            },
        },
        "event_outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letters", ())),
    }
