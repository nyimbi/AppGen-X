"""UI contract for the Order Routing Optimization PBC."""

from __future__ import annotations

from .runtime import ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS
from .runtime import ORDER_ROUTING_OPTIMIZATION_OWNED_TABLES
from .runtime import ORDER_ROUTING_OPTIMIZATION_REQUIRED_RULE_FIELDS
from .runtime import ORDER_ROUTING_OPTIMIZATION_REQUIRED_EVENT_TOPIC
from .runtime import ORDER_ROUTING_OPTIMIZATION_SUPPORTED_CONFIGURATION_FIELDS
from .runtime import ORDER_ROUTING_OPTIMIZATION_SUPPORTED_PARAMETER_KEYS
from .runtime import order_routing_optimization_build_workbench_view
from .runtime import order_routing_optimization_permissions_contract
from .app_surface import routing_controls_contract
from .app_surface import routing_forms_contract
from .app_surface import routing_wizards_contract
from .app_surface import single_pbc_routing_app_contract

ORDER_ROUTING_OPTIMIZATION_UI_FRAGMENT_KEYS = (
    "OrderRoutingWorkbench",
    "RoutingNodeTopologyMap",
    "RoutingRuleStudio",
    "RouteCandidateGrid",
    "CapacitySnapshotBoard",
    "RoutingDecisionLedger",
    "RoutingPromiseBoard",
    "SplitShipmentStudio",
    "ReservationConsole",
    "CounterfactualSimulationLab",
    "RoutingOptimizationWorkbench",
    "RoutingExceptionConsole",
    "RoutingApprovalQueue",
    "RoutingFeedbackLedger",
    "RoutingInboxMonitor",
    "RoutingParameterConsole",
    "RoutingConfigurationPanel",
    "RoutingPolicyScreeningPanel",
    "RoutingAuditTrailView",
)


def order_routing_optimization_forms_contract() -> dict:
    """Return standalone database-backed form metadata for generated apps."""
    return routing_forms_contract()


def order_routing_optimization_wizards_contract() -> dict:
    """Return standalone wizard metadata for generated apps."""
    return routing_wizards_contract()


def order_routing_optimization_controls_contract() -> dict:
    """Return standalone release/operator controls for generated apps."""
    return routing_controls_contract()


def order_routing_optimization_ui_contract() -> dict:
    return {
        "format": "appgen.order-routing-optimization-ui-contract.v1",
        "ok": True,
        "pbc": "order_routing_optimization",
        "implementation_directory": "src/pyAppGen/pbcs/order_routing_optimization",
        "fragments": ORDER_ROUTING_OPTIMIZATION_UI_FRAGMENT_KEYS,
        "forms": order_routing_optimization_forms_contract()["forms"],
        "wizards": order_routing_optimization_wizards_contract()["wizards"],
        "controls": order_routing_optimization_controls_contract()["controls"],
        "single_pbc_app": single_pbc_routing_app_contract(),
        "routes": (
            "/workbench/pbcs/order_routing_optimization",
            "/workbench/pbcs/order_routing_optimization/rules",
            "/workbench/pbcs/order_routing_optimization/candidates",
            "/workbench/pbcs/order_routing_optimization/capacity",
            "/workbench/pbcs/order_routing_optimization/nodes",
            "/workbench/pbcs/order_routing_optimization/decisions",
            "/workbench/pbcs/order_routing_optimization/promises",
            "/workbench/pbcs/order_routing_optimization/splits",
            "/workbench/pbcs/order_routing_optimization/reservations",
            "/workbench/pbcs/order_routing_optimization/simulations",
            "/workbench/pbcs/order_routing_optimization/optimizations",
            "/workbench/pbcs/order_routing_optimization/exceptions",
            "/workbench/pbcs/order_routing_optimization/approvals",
            "/workbench/pbcs/order_routing_optimization/feedback",
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
                "key": "topology_and_nodes",
                "fragment": "RoutingNodeTopologyMap",
                "binds_to": (
                    "routing_plan",
                    "routing_node",
                    "routing_constraint",
                    "inventory_input_projection",
                    "transport_input_projection",
                    "service_input_projection",
                ),
                "commands": (
                    "ingest_capacity_snapshot",
                    "upsert_route_candidate",
                    "federate_routing_view",
                ),
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
                "binds_to": (
                    "routing_exception",
                    "exception_resolution",
                    "routing_approval",
                    "routing_feedback",
                    "inbox_event",
                    "dead_letter",
                    "retry_evidence",
                ),
                "commands": (
                    "handle_event",
                    "recommend_exception_resolution",
                    "simulate_counterfactual",
                ),
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
            {
                "key": "simulation_and_optimization",
                "fragment": "RoutingOptimizationWorkbench",
                "binds_to": (
                    "route_simulation",
                    "optimization_run",
                    "routing_promise",
                    "split_shipment",
                ),
                "commands": (
                    "simulate_counterfactual",
                    "optimize_route_network",
                    "clear_capacity_auction",
                    "schedule_carbon_aware_route",
                ),
            },
        ),
        "action_permissions": order_routing_optimization_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ORDER_ROUTING_OPTIMIZATION_SUPPORTED_CONFIGURATION_FIELDS,
            "allowed_database_backends": ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": ORDER_ROUTING_OPTIMIZATION_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "visible_event_contracts": ("AppGen-X",),
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
            "topic": ORDER_ROUTING_OPTIMIZATION_REQUIRED_EVENT_TOPIC,
            "contract_locked": True,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": ORDER_ROUTING_OPTIMIZATION_OWNED_TABLES,
            "shared_table_access": False,
            "workbench_fragments": ORDER_ROUTING_OPTIMIZATION_UI_FRAGMENT_KEYS,
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
            "key": "routing_promises",
            "value": view["routing_promise_count"],
            "fragment": "RoutingPromiseBoard",
        },
        {
            "key": "split_decisions",
            "value": view["split_decision_count"],
            "fragment": "SplitShipmentStudio",
        },
        {
            "key": "reserved_units",
            "value": view["reserved_units"],
            "fragment": "ReservationConsole",
        },
        {
            "key": "route_simulations",
            "value": view["route_simulation_count"],
            "fragment": "CounterfactualSimulationLab",
        },
        {
            "key": "optimization_runs",
            "value": view["optimization_run_count"],
            "fragment": "RoutingOptimizationWorkbench",
        },
        {
            "key": "approvals",
            "value": view["approval_count"],
            "fragment": "RoutingApprovalQueue",
        },
        {
            "key": "feedback",
            "value": view["feedback_count"],
            "fragment": "RoutingFeedbackLedger",
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
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "single_pbc_app": contract["single_pbc_app"],
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
            "events": view["binding_evidence"]["events"],
            "workbench": view["binding_evidence"]["workbench"],
            "owned_tables": view["binding_evidence"]["owned_tables"],
            "outbox_table": view["binding_evidence"]["outbox_table"],
            "inbox_table": view["binding_evidence"]["inbox_table"],
            "dead_letter_table": view["binding_evidence"]["dead_letter_table"],
        },
        "event_outbox_count": view["event_outbox_count"],
        "inbox_count": view["inbox_count"],
        "dead_letter_count": view["dead_letter_count"],
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = order_routing_optimization_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = order_routing_optimization_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and contract.get("single_pbc_app", {}).get("ok") is True
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
