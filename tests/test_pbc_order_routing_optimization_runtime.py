import pytest

from pyAppGen.pbcs.order_routing_optimization import (
    ORDER_ROUTING_OPTIMIZATION_RUNTIME_CAPABILITY_KEYS,
)
from pyAppGen.pbcs.order_routing_optimization import implementation_contract
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_build_workbench_view,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_configure_runtime,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_empty_state,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_handle_event,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_ingest_capacity_snapshot,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_register_rule,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_render_workbench,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_route_orders,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_runtime_capabilities,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_runtime_smoke,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_set_parameter,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_ui_contract,
)
from pyAppGen.pbcs.order_routing_optimization import (
    order_routing_optimization_upsert_route_candidate,
)


def test_order_routing_optimization_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = order_routing_optimization_runtime_capabilities()
    smoke = order_routing_optimization_runtime_smoke()

    assert runtime["format"] == "appgen.order-routing-optimization-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/order_routing_optimization"
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {
        check["id"] for check in smoke["checks"]
    } == set(ORDER_ROUTING_OPTIMIZATION_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = implementation_contract()
    assert contract["pbc"] == "order_routing_optimization"
    assert contract["ui_contract"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert (
        "RoutingConfigurationPanel"
        in contract["ui_contract"]["fragments"]
    )
    assert set(contract["advanced_runtime"]["capabilities"]) == set(
        ORDER_ROUTING_OPTIMIZATION_RUNTIME_CAPABILITY_KEYS
    )


def test_order_routing_optimization_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = order_routing_optimization_empty_state()
    state = order_routing_optimization_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.order-routing.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_regions": ("west", "central"),
            "supported_split_policies": ("forbid", "allow"),
            "supported_substitution_modes": ("exact", "equivalent"),
            "topology_systems": ("dom", "inventory", "tax"),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("cost_weight", 0.25),
        ("sla_weight", 0.35),
        ("capacity_weight", 0.2),
        ("risk_weight", 0.1),
        ("carbon_weight", 0.1),
        ("reservation_hold_minutes", 45),
        ("forecast_horizon_hours", 24),
        ("max_split_count", 2),
        ("simulation_sample_size", 500),
        ("confidence_floor", 0.55),
    ):
        state = order_routing_optimization_set_parameter(state, name, value)["state"]

    rule = order_routing_optimization_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "routing",
            "regions": ("west",),
            "eligible_nodes": ("node_fast", "node_green"),
            "preferred_nodes": ("node_fast",),
            "capacity_floor": 2,
            "split_policy": "allow",
            "substitution_mode": "equivalent",
            "status": "active",
        },
    )
    state = rule["state"]
    assert rule["rule"]["compiled_hash"]
    assert rule["rule"]["compiled_evidence"]["rule_id"] == "rule_ops"
    assert rule["rule"]["compiled_evidence"]["required_fields"] == (
        "rule_id",
        "tenant",
        "rule_type",
        "regions",
        "eligible_nodes",
        "capacity_floor",
        "split_policy",
        "substitution_mode",
        "status",
    )

    for event in (
        {
            "event_id": "evt_verify_ops",
            "event_type": "OrderVerified",
            "payload": {"tenant": "tenant_ops", "order_id": "order_ops"},
        },
        {
            "event_id": "evt_availability_ops",
            "event_type": "AvailabilityProjected",
            "payload": {
                "tenant": "tenant_ops",
                "node_id": "node_fast",
                "available_units": 12,
            },
        },
        {
            "event_id": "evt_tax_ops",
            "event_type": "TaxCalculated",
            "payload": {
                "tenant": "tenant_ops",
                "order_id": "order_ops",
                "tax_total": 7.0,
            },
        },
    ):
        state = order_routing_optimization_handle_event(state, event)["state"]

    state = order_routing_optimization_ingest_capacity_snapshot(
        state,
        {
            "snapshot_id": "cap_fast",
            "tenant": "tenant_ops",
            "node_id": "node_fast",
            "available_units": 12,
            "reserved_units": 0,
            "forecast_load": 5,
        },
    )["state"]
    state = order_routing_optimization_ingest_capacity_snapshot(
        state,
        {
            "snapshot_id": "cap_green",
            "tenant": "tenant_ops",
            "node_id": "node_green",
            "available_units": 8,
            "reserved_units": 0,
            "forecast_load": 4,
        },
    )["state"]
    state = order_routing_optimization_upsert_route_candidate(
        state,
        {
            "candidate_id": "cand_fast",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "node_id": "node_fast",
            "region": "west",
            "distance_km": 180,
            "base_cost": 118,
            "sla_hours": 10,
            "carbon_kg": 46,
            "risk_score": 0.08,
            "available_units": 12,
            "inventory_source": "fc_fast",
            "split_supported": True,
            "substitution_eligible": True,
        },
    )["state"]
    state = order_routing_optimization_upsert_route_candidate(
        state,
        {
            "candidate_id": "cand_green",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "node_id": "node_green",
            "region": "west",
            "distance_km": 220,
            "base_cost": 108,
            "sla_hours": 18,
            "carbon_kg": 18,
            "risk_score": 0.12,
            "available_units": 8,
            "inventory_source": "fc_green",
            "split_supported": True,
            "substitution_eligible": True,
        },
    )["state"]

    routed = order_routing_optimization_route_orders(
        state,
        {
            "request_id": "req_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "region": "west",
            "requested_units": 6,
            "sla_target_hours": 24,
            "allow_split": True,
            "substitution_requested": False,
        },
    )
    state = routed["state"]
    assert routed["ok"] is True
    assert routed["decision"]["status"] == "selected"
    assert routed["decision"]["split"] is False
    assert routed["decision"]["selected_node_ids"] == ("node_fast",)
    assert state["outbox"][-1]["idempotency_key"] == (
        "order_routing_optimization:NodeCapacityReserved:order_routing_evt_000009"
    )

    workbench = order_routing_optimization_build_workbench_view(
        state,
        tenant="tenant_ops",
    )
    assert workbench["route_candidate_count"] == 2
    assert workbench["capacity_snapshot_count"] == 2
    assert workbench["routing_decision_count"] == 1
    assert workbench["split_decision_count"] == 0
    assert workbench["reservation_count"] == 1
    assert workbench["reserved_units"] == 6
    assert workbench["substitution_eligible_count"] == 2
    assert workbench["inbox_count"] == 3
    assert workbench["event_outbox_count"] == 6
    assert workbench["dead_letter_count"] == 0
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10
    assert workbench["binding_evidence"]["configuration"] == {
        "bound": True,
        "database_backend": "postgresql",
        "event_contract": "appgen_event_contract",
        "event_topic": "appgen.order-routing.events",
        "visible_event_contracts": ("appgen_event_contract",),
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "supported_fields": (
            "database_backend",
            "event_topic",
            "retry_limit",
            "default_currency",
            "supported_regions",
            "supported_split_policies",
            "supported_substitution_modes",
            "topology_systems",
            "default_timezone",
            "workbench_limit",
        ),
    }
    assert workbench["binding_evidence"]["rules"] == (
        {
            "rule_id": "rule_ops",
            "scope": "routing",
            "compiled_hash": rule["rule"]["compiled_hash"],
            "required_fields": rule["rule"]["compiled_evidence"]["required_fields"],
        },
    )
    assert workbench["binding_evidence"]["parameters"] == {
        "supported": (
            "cost_weight",
            "sla_weight",
            "capacity_weight",
            "risk_weight",
            "carbon_weight",
            "reservation_hold_minutes",
            "forecast_horizon_hours",
            "max_split_count",
            "simulation_sample_size",
            "confidence_floor",
        ),
        "active": (
            "capacity_weight",
            "carbon_weight",
            "confidence_floor",
            "cost_weight",
            "forecast_horizon_hours",
            "max_split_count",
            "reservation_hold_minutes",
            "risk_weight",
            "simulation_sample_size",
            "sla_weight",
        ),
    }

    ui_contract = order_routing_optimization_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == (
        "postgresql",
        "mysql",
        "mariadb",
    )
    assert ui_contract["configuration_editor"]["visible_event_contracts"] == (
        "appgen_event_contract",
    )
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["user_selectable_event_contract"] is False
    assert (
        ui_contract["rule_editor"]["compiled_evidence_fields"]
        == ("compiled_hash", "compiled_evidence")
    )
    rendered = order_routing_optimization_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "order_routing_optimization.route",
            "order_routing_optimization.capacity",
            "order_routing_optimization.event",
            "order_routing_optimization.configure",
            "order_routing_optimization.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert rendered["inbox_count"] == 3
    assert rendered["dead_letter_count"] == 0
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["rules_bound"] == ("rule_ops",)
    assert rendered["parameters_bound"] == (
        "capacity_weight",
        "carbon_weight",
        "confidence_floor",
        "cost_weight",
        "forecast_horizon_hours",
        "max_split_count",
        "reservation_hold_minutes",
        "risk_weight",
        "simulation_sample_size",
        "sla_weight",
    )
    assert rendered["binding_evidence"]["configuration"] == workbench["binding_evidence"][
        "configuration"
    ]
    assert rendered["binding_evidence"]["rules"] == (
        {
            "rule_id": "rule_ops",
            "compiled_hash": rule["rule"]["compiled_hash"],
            "required_fields": rule["rule"]["compiled_evidence"]["required_fields"],
        },
    )
    assert rendered["binding_evidence"]["parameters"] == workbench["binding_evidence"][
        "parameters"
    ]


def test_order_routing_optimization_rejects_invalid_backend_and_preserves_idempotent_retry_evidence() -> None:
    state = order_routing_optimization_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        order_routing_optimization_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.order-routing.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_regions": ("west",),
                "supported_split_policies": ("allow",),
                "supported_substitution_modes": ("exact",),
                "topology_systems": ("dom",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )

    with pytest.raises(ValueError, match="Unsupported Order Routing Optimization configuration fields"):
        order_routing_optimization_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.order-routing.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_regions": ("west",),
                "supported_split_policies": ("allow",),
                "supported_substitution_modes": ("exact",),
                "topology_systems": ("dom",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Order Routing Optimization parameter"):
        order_routing_optimization_set_parameter(state, "stream_engine", 1)

    with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
        order_routing_optimization_set_parameter(state, "confidence_floor", 1.1)

    configured = order_routing_optimization_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.order-routing.events",
            "retry_limit": 2,
            "default_currency": "USD",
            "supported_regions": ("west",),
            "supported_split_policies": ("allow",),
            "supported_substitution_modes": ("exact",),
            "topology_systems": ("dom",),
            "default_timezone": "UTC",
            "workbench_limit": 25,
        },
    )["state"]
    configured = order_routing_optimization_set_parameter(
        configured, "cost_weight", 0.5
    )["state"]

    processed = order_routing_optimization_handle_event(
        configured,
        {
            "event_id": "evt_once",
            "event_type": "OrderVerified",
            "payload": {"tenant": "tenant_ops", "order_id": "order_dup"},
        },
    )
    duplicate = order_routing_optimization_handle_event(
        processed["state"],
        {
            "event_id": "evt_once",
            "event_type": "OrderVerified",
            "payload": {"tenant": "tenant_ops", "order_id": "order_dup"},
        },
    )
    assert processed["ok"] is True
    assert duplicate["duplicate"] is True
    assert len(duplicate["state"]["inbox"]) == 1

    failing = order_routing_optimization_handle_event(
        configured,
        {
            "event_id": "evt_fail",
            "event_type": "TaxCalculated",
            "payload": {"tenant": "tenant_ops", "order_id": "order_fail", "tax_total": 4},
        },
        simulate_failure=True,
    )
    dead_letter = order_routing_optimization_handle_event(
        failing["state"],
        {
            "event_id": "evt_fail",
            "event_type": "TaxCalculated",
            "payload": {"tenant": "tenant_ops", "order_id": "order_fail", "tax_total": 4},
        },
        simulate_failure=True,
    )
    assert failing["ok"] is False
    assert failing["handler"]["status"] == "retrying"
    assert dead_letter["ok"] is False
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["retry_evidence"]) == 2
    assert len(dead_letter["state"]["dead_letter"]) == 1
