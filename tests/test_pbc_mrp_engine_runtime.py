import pytest

from pyAppGen.pbc import MRP_ENGINE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import mrp_engine_build_workbench_view
from pyAppGen.pbc import mrp_engine_calculate_material_plan
from pyAppGen.pbc import mrp_engine_configure_runtime
from pyAppGen.pbc import mrp_engine_create_mrp_run
from pyAppGen.pbc import mrp_engine_empty_state
from pyAppGen.pbc import mrp_engine_explode_bom
from pyAppGen.pbc import mrp_engine_ingest_demand_projection
from pyAppGen.pbc import mrp_engine_ingest_inventory_projection
from pyAppGen.pbc import mrp_engine_register_bom
from pyAppGen.pbc import mrp_engine_register_rule
from pyAppGen.pbc import mrp_engine_release_planned_order
from pyAppGen.pbc import mrp_engine_render_workbench
from pyAppGen.pbc import mrp_engine_runtime_capabilities
from pyAppGen.pbc import mrp_engine_runtime_smoke
from pyAppGen.pbc import mrp_engine_set_parameter
from pyAppGen.pbc import mrp_engine_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.mrp_engine import MRP_ENGINE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.mrp_engine import MRP_ENGINE_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.mrp_engine import MRP_ENGINE_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.mrp_engine import MRP_ENGINE_OWNED_TABLES
from pyAppGen.pbcs.mrp_engine import MRP_ENGINE_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.mrp_engine import mrp_engine_build_api_contract
from pyAppGen.pbcs.mrp_engine import mrp_engine_build_release_evidence
from pyAppGen.pbcs.mrp_engine import mrp_engine_build_schema_contract
from pyAppGen.pbcs.mrp_engine import mrp_engine_build_service_contract
from pyAppGen.pbcs.mrp_engine import mrp_engine_permissions_contract
from pyAppGen.pbcs.mrp_engine import mrp_engine_receive_event
from pyAppGen.pbcs.mrp_engine import mrp_engine_register_schema_extension
from pyAppGen.pbcs.mrp_engine import mrp_engine_verify_owned_table_boundary


def test_mrp_engine_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = mrp_engine_runtime_capabilities()
    smoke = mrp_engine_runtime_smoke()

    assert runtime["format"] == "appgen.mrp-engine-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/mrp_engine"
    assert runtime["owned_tables"] == MRP_ENGINE_OWNED_TABLES
    assert len(runtime["owned_tables"]) >= 40
    assert len(runtime["standard_features"]) >= 40
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "appgen_x_inbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(MRP_ENGINE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("mrp_engine")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "MrpConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(MRP_ENGINE_ADVANCED_CAPABILITY_KEYS)
    assert contract["source_package"]["api_contract"]["shared_table_access"] is False
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "mrp_engine.event"
    assert contract["source_package"]["owned_tables"] == MRP_ENGINE_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == MRP_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["required_event_topic"] == MRP_ENGINE_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["consumes"] == MRP_ENGINE_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["emits"] == MRP_ENGINE_EMITTED_EVENT_TYPES
    schema = mrp_engine_build_schema_contract()
    service = mrp_engine_build_service_contract()
    release = mrp_engine_build_release_evidence()
    assert schema["format"] == "appgen.mrp-engine-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(MRP_ENGINE_OWNED_TABLES)
    assert len(schema["migrations"]) == len(MRP_ENGINE_OWNED_TABLES)
    assert {"bom_component", "item_planning_profile", "mrp_run_item", "planned_purchase_suggestion", "mrp_governed_model"} <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.mrp-engine-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 25
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.mrp-engine-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert pbc_implementation_release_audit(("mrp_engine",))["ok"] is True
    assert pbc_implemented_capability_audit(("mrp_engine",))["ok"] is True


def test_mrp_engine_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = mrp_engine_empty_state()
    state = mrp_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": MRP_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_sites": ("factory_ops",),
            "allowed_order_types": ("production", "purchase"),
            "allowed_procurement_routes": ("buy",),
            "allowed_production_routes": ("make",),
            "default_planning_bucket": "daily",
            "workbench_limit": 50,
        },
    )["state"]
    state = mrp_engine_set_parameter(state, "planning_horizon_days", 30)["state"]
    state = mrp_engine_set_parameter(state, "bucket_size_days", 1)["state"]
    state = mrp_engine_set_parameter(state, "safety_stock_multiplier", 1.0)["state"]
    state = mrp_engine_set_parameter(state, "lot_size_minimum", 10)["state"]
    state = mrp_engine_set_parameter(state, "lead_time_days", 3)["state"]
    state = mrp_engine_set_parameter(state, "capacity_threshold", 0.85)["state"]
    state = mrp_engine_set_parameter(state, "shortage_severity_threshold", 20)["state"]
    state = mrp_engine_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "planning",
            "eligible_item_types": ("finished_good", "component"),
            "allowed_sites": ("factory_ops",),
            "allowed_bom_statuses": ("released",),
            "demand_sources": ("order", "forecast"),
            "release_routes": {"component_ops": "buy", "fg_ops": "make"},
            "substitutions": {"component_ops": ("component_alt",)},
            "status": "active",
        },
    )["state"]
    state = mrp_engine_register_bom(
        state,
        {
            "bom_id": "bom_ops",
            "tenant": "tenant_ops",
            "parent_item": "fg_ops",
            "component_item": "component_ops",
            "component_qty": 2,
            "scrap_percent": 0,
            "revision": "A",
            "status": "released",
            "site": "factory_ops",
        },
    )["state"]
    state = mrp_engine_ingest_demand_projection(
        state,
        {"demand_id": "demand_ops", "tenant": "tenant_ops", "item": "fg_ops", "site": "factory_ops", "quantity": 30, "source": "order", "need_date": "2026-06-01"},
    )["state"]
    state = mrp_engine_ingest_inventory_projection(
        state,
        {"inventory_id": "inv_ops", "tenant": "tenant_ops", "item": "component_ops", "site": "factory_ops", "available_qty": 40, "quality_status": "released"},
    )["state"]
    run = mrp_engine_create_mrp_run(
        state,
        {"run_id": "run_ops", "tenant": "tenant_ops", "site": "factory_ops", "horizon_days": 30, "scenario": "base", "planner": "planner_ops"},
    )
    state = run["state"]
    assert run["mrp_run"]["status"] == "running"

    explosion = mrp_engine_explode_bom(state, "fg_ops", quantity=30)
    assert explosion["requirements"][0]["component_item"] == "component_ops"
    assert explosion["requirements"][0]["required_qty"] == 60

    plan = mrp_engine_calculate_material_plan(state, "run_ops")
    state = plan["state"]
    assert plan["shortage_total"] == 20
    assert plan["planned_orders"][0]["quantity"] == 20

    release = mrp_engine_release_planned_order(state, "po_run_ops_component_ops", released_by="planner_ops")
    state = release["state"]
    assert release["planned_order"]["status"] == "released"
    assert state["outbox"][-1]["idempotency_key"] == "mrp_engine:PlannedOrderReleased:mrp_evt_000006"

    workbench = mrp_engine_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["bom_count"] == 1
    assert workbench["demand_count"] == 1
    assert workbench["run_count"] == 1
    assert workbench["planned_order_count"] == 1
    assert workbench["released_order_count"] == 1
    assert workbench["shortage_total"] == 20
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 7
    assert workbench["binding_evidence"]["owned_tables"] == MRP_ENGINE_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["configuration"]["event_topic"] == MRP_ENGINE_REQUIRED_EVENT_TOPIC
    assert workbench["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False

    ui_contract = mrp_engine_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == MRP_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["fixed_event_topic"] == MRP_ENGINE_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert "planning_horizon_days" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["event_surfaces"]["emits"] == MRP_ENGINE_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == MRP_ENGINE_CONSUMED_EVENT_TYPES
    rendered = mrp_engine_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "mrp_engine.master",
            "mrp_engine.plan",
            "mrp_engine.release",
            "mrp_engine.event",
            "mrp_engine.configure",
            "mrp_engine.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert rendered["event_inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["owned_tables"] == MRP_ENGINE_OWNED_TABLES
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_mrp_engine_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = mrp_engine_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        mrp_engine_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": MRP_ENGINE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_planning_bucket": "daily",
            },
        )

    with pytest.raises(ValueError, match="Unsupported MRP Engine parameter"):
        mrp_engine_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="requires AppGen-X event topic"):
        mrp_engine_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.mrp.events",
                "retry_limit": 3,
                "default_planning_bucket": "daily",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        mrp_engine_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": MRP_ENGINE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_planning_bucket": "daily",
                "stream_engine_picker": "visible",
            },
        )


def test_mrp_engine_contracts_events_schema_and_boundaries_are_package_local() -> None:
    state = mrp_engine_configure_runtime(
        mrp_engine_empty_state(),
        {
            "database_backend": "mysql",
            "event_topic": MRP_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_planning_bucket": "daily",
        },
    )["state"]

    extension = mrp_engine_register_schema_extension(
        state,
        "planned_order",
        {"simulation_payload": "jsonb", "constraint_score": "numeric"},
    )
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["planned_order"]["constraint_score"] == "numeric"

    with pytest.raises(ValueError, match="owned tables"):
        mrp_engine_register_schema_extension(state, "inventory_balance", {"foreign_stock": "numeric"})

    invalid = mrp_engine_register_schema_extension(state, "planned_order", {"BadField": "text"})
    assert invalid["ok"] is False
    assert invalid["error"] == "invalid_extension_field"

    api = mrp_engine_build_api_contract()
    assert api["format"] == "appgen.mrp-engine-api-contract.v1"
    assert api["database_backends"] == MRP_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert api["owned_tables"] == MRP_ENGINE_OWNED_TABLES
    assert api["events"]["emits"] == MRP_ENGINE_EMITTED_EVENT_TYPES
    assert api["events"]["consumes"] == MRP_ENGINE_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert any(route["command"] == "receive_event" for route in api["routes"])

    permissions = mrp_engine_permissions_contract()
    assert permissions["ok"] is True
    assert permissions["action_permissions"]["receive_event"] == "mrp_engine.event"
    assert "mrp_engine.configure" in permissions["permissions"]

    processed = mrp_engine_receive_event(
        state,
        {
            "event_id": "evt_inventory_1",
            "event_type": "InventoryReleased",
            "payload": {"tenant": "tenant_ops", "release_id": "rel_1", "item": "component_ops", "available_qty": 10},
        },
    )
    state = processed["state"]
    assert processed["ok"] is True
    assert state["inventory_release_projections"]["rel_1"]["available_qty"] == 10
    duplicate = mrp_engine_receive_event(
        state,
        {
            "event_id": "evt_inventory_1",
            "event_type": "InventoryReleased",
            "payload": {"tenant": "tenant_ops", "release_id": "rel_1"},
        },
    )
    assert duplicate["duplicate"] is True
    assert len(duplicate["state"]["inbox"]) == 1

    retry = mrp_engine_receive_event(
        state,
        {
            "event_id": "evt_bad",
            "event_type": "UnknownPlanningEvent",
            "payload": {"tenant": "tenant_ops"},
        },
    )
    assert retry["ok"] is False
    assert retry["handler"]["status"] == "retrying"
    dead = mrp_engine_receive_event(retry["state"], {"event_id": "evt_bad", "event_type": "UnknownPlanningEvent", "payload": {"tenant": "tenant_ops"}})
    assert dead["handler"]["status"] == "dead_letter"
    assert dead["state"]["dead_letters"][-1]["reason"] == "unsupported_or_failed_mrp_event"

    boundary = mrp_engine_verify_owned_table_boundary(("planned_order", "InventoryReleased", "inventory_release_projection", "mrp_engine_custom_projection"))
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = mrp_engine_verify_owned_table_boundary(("inventory_balance", "customer_profile"))
    assert violation["ok"] is False
    assert violation["violations"] == ("inventory_balance", "customer_profile")
