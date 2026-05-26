"""UI contract for the Order Routing Optimization PBC."""

from __future__ import annotations

from .runtime import ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS
from .runtime import ORDER_ROUTING_OPTIMIZATION_REQUIRED_RULE_FIELDS
from .runtime import ORDER_ROUTING_OPTIMIZATION_SUPPORTED_CONFIGURATION_FIELDS
from .runtime import ORDER_ROUTING_OPTIMIZATION_SUPPORTED_PARAMETER_KEYS
from .runtime import order_routing_optimization_build_workbench_view

ORDER_ROUTING_OPTIMIZATION_UI_FRAGMENT_KEYS = (
    "OrderRoutingWorkbench",
    "RoutingRuleStudio",
    "RouteCandidateGrid",
    "CapacitySnapshotBoard",
    "RoutingDecisionLedger",
    "ReservationConsole",
    "CounterfactualSimulationLab",
    "RoutingInboxMonitor",
    "RoutingParameterConsole",
    "RoutingConfigurationPanel",
    "RoutingPolicyScreeningPanel",
    "RoutingAuditTrailView",
)


def order_routing_optimization_ui_contract() -> dict:
    return {
        "format": "appgen.order-routing-optimization-ui-contract.v1",
        "ok": True,
        "pbc": "order_routing_optimization",
        "implementation_directory": "src/pyAppGen/pbcs/order_routing_optimization",
        "fragments": ORDER_ROUTING_OPTIMIZATION_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/order_routing_optimization",
            "/workbench/pbcs/order_routing_optimization/rules",
            "/workbench/pbcs/order_routing_optimization/candidates",
            "/workbench/pbcs/order_routing_optimization/capacity",
            "/workbench/pbcs/order_routing_optimization/decisions",
            "/workbench/pbcs/order_routing_optimization/reservations",
            "/workbench/pbcs/order_routing_optimization/simulations",
            "/workbench/pbcs/order_routing_optimization/inbox",
            "/workbench/pbcs/order_routing_optimization/parameters",
            "/workbench/pbcs/order_routing_optimization/configuration",
            "/workbench/pbcs/order_routing_optimization/policy",
            "/workbench/pbcs/order_routing_optimization/audit",
        ),
        "panels": (
            {
                "key": "routing_workbench",
                "fragment": "OrderRoutingWorkbench",
                "binds_to": ("routing_decision", "route_candidate", "node_reservation"),
                "commands": ("route_orders", "reserve_node_capacity"),
            },
            {
                "key": "capacity_and_candidates",
                "fragment": "CapacitySnapshotBoard",
                "binds_to": ("capacity_snapshot", "route_candidate"),
                "commands": (
                    "ingest_capacity_snapshot",
                    "upsert_route_candidate",
                ),
            },
            {
                "key": "eventing_and_exception_flow",
                "fragment": "RoutingInboxMonitor",
                "binds_to": ("inbox_event", "dead_letter", "retry_evidence"),
                "commands": ("handle_event", "simulate_counterfactual"),
            },
            {
                "key": "governance",
                "fragment": "RoutingRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": (
                    "register_rule",
                    "set_parameter",
                    "configure_runtime",
                    "run_control_tests",
                ),
            },
        ),
        "action_permissions": {
            "route_orders": "order_routing_optimization.route",
            "reserve_node_capacity": "order_routing_optimization.route",
            "ingest_capacity_snapshot": "order_routing_optimization.capacity",
            "upsert_route_candidate": "order_routing_optimization.capacity",
            "handle_event": "order_routing_optimization.event",
            "simulate_counterfactual": "order_routing_optimization.audit",
            "register_rule": "order_routing_optimization.configure",
            "set_parameter": "order_routing_optimization.configure",
            "configure_runtime": "order_routing_optimization.configure",
            "run_control_tests": "order_routing_optimization.audit",
        },
        "configuration_editor": {
            "required_fields": ORDER_ROUTING_OPTIMIZATION_SUPPORTED_CONFIGURATION_FIELDS,
            "allowed_database_backends": ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "visible_event_contracts": ("appgen_event_contract",),
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": ORDER_ROUTING_OPTIMIZATION_SUPPORTED_PARAMETER_KEYS,
            "supported_parameters": ORDER_ROUTING_OPTIMIZATION_SUPPORTED_PARAMETER_KEYS,
        },
        "rule_editor": {
            "rule_types": (
                "routing",
                "split",
                "capacity",
                "reservation",
                "substitution",
                "screening",
            ),
            "required_fields": ORDER_ROUTING_OPTIMIZATION_REQUIRED_RULE_FIELDS,
            "compiled_evidence_fields": ("compiled_hash", "compiled_evidence"),
        },
        "event_surfaces": {
            "emits": (
                "FulfillmentRouteSelected",
                "NodeCapacityReserved",
            ),
            "consumes": (
                "OrderVerified",
                "AvailabilityProjected",
                "TaxCalculated",
            ),
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def order_routing_optimization_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = order_routing_optimization_ui_contract()
    view = order_routing_optimization_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(
        action
        for action, required_permission in action_permissions.items()
        if required_permission in permissions
    )
    cards = (
        {
            "key": "route_candidates",
            "value": view["route_candidate_count"],
            "fragment": "RouteCandidateGrid",
        },
        {
            "key": "capacity_snapshots",
            "value": view["capacity_snapshot_count"],
            "fragment": "CapacitySnapshotBoard",
        },
        {
            "key": "routing_decisions",
            "value": view["routing_decision_count"],
            "fragment": "RoutingDecisionLedger",
        },
        {
            "key": "split_decisions",
            "value": view["split_decision_count"],
            "fragment": "CounterfactualSimulationLab",
        },
        {
            "key": "reserved_units",
            "value": view["reserved_units"],
            "fragment": "ReservationConsole",
        },
        {
            "key": "dead_letter",
            "value": view["dead_letter_count"],
            "fragment": "RoutingInboxMonitor",
        },
    )
    return {
        "format": "appgen.order-routing-optimization-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/order_routing_optimization",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(
            action for action in action_permissions if action not in visible_actions
        ),
        "configuration_bound": view["configuration_bound"],
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "binding_evidence": {
            "configuration": view["binding_evidence"]["configuration"],
            "rules": tuple(
                {
                    "rule_id": item["rule_id"],
                    "compiled_hash": item["compiled_hash"],
                    "required_fields": item["required_fields"],
                }
                for item in view["binding_evidence"]["rules"]
            ),
            "parameters": view["binding_evidence"]["parameters"],
        },
        "event_outbox_count": view["event_outbox_count"],
        "inbox_count": view["inbox_count"],
        "dead_letter_count": view["dead_letter_count"],
    }
