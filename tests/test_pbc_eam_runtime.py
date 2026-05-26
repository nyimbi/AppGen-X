import pytest

from pyAppGen.pbcs.eam import EAM_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.eam import EAM_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.eam import EAM_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.eam import EAM_OWNED_TABLES
from pyAppGen.pbcs.eam import EAM_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.eam import EAM_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.eam import eam_allocate_labor_and_spares
from pyAppGen.pbcs.eam import eam_build_api_contract
from pyAppGen.pbcs.eam import eam_build_release_evidence
from pyAppGen.pbcs.eam import eam_build_schema_contract
from pyAppGen.pbcs.eam import eam_build_service_contract
from pyAppGen.pbcs.eam import eam_build_workbench_view
from pyAppGen.pbcs.eam import eam_complete_work_order
from pyAppGen.pbcs.eam import eam_configure_runtime
from pyAppGen.pbcs.eam import eam_create_maintenance_plan
from pyAppGen.pbcs.eam import eam_create_safety_permit
from pyAppGen.pbcs.eam import eam_create_work_order
from pyAppGen.pbcs.eam import eam_detect_failure_anomaly
from pyAppGen.pbcs.eam import eam_empty_state
from pyAppGen.pbcs.eam import eam_forecast_failures
from pyAppGen.pbcs.eam import eam_generate_compliance_proof
from pyAppGen.pbcs.eam import eam_issue_spare_part
from pyAppGen.pbcs.eam import eam_model_stochastic_maintenance_exposure
from pyAppGen.pbcs.eam import eam_optimize_maintenance_schedule
from pyAppGen.pbcs.eam import eam_parse_maintenance_instruction
from pyAppGen.pbcs.eam import eam_permissions_contract
from pyAppGen.pbcs.eam import eam_receive_event
from pyAppGen.pbcs.eam import eam_recommend_exception_resolution
from pyAppGen.pbcs.eam import eam_record_condition_reading
from pyAppGen.pbcs.eam import eam_record_meter_reading
from pyAppGen.pbcs.eam import eam_register_equipment
from pyAppGen.pbcs.eam import eam_register_governed_model
from pyAppGen.pbcs.eam import eam_register_rule
from pyAppGen.pbcs.eam import eam_register_schema_extension
from pyAppGen.pbcs.eam import eam_render_workbench
from pyAppGen.pbcs.eam import eam_route_maintenance
from pyAppGen.pbcs.eam import eam_run_control_tests
from pyAppGen.pbcs.eam import eam_runtime_capabilities
from pyAppGen.pbcs.eam import eam_runtime_smoke
from pyAppGen.pbcs.eam import eam_schedule_carbon_aware_maintenance
from pyAppGen.pbcs.eam import eam_schedule_work_order
from pyAppGen.pbcs.eam import eam_screen_policy
from pyAppGen.pbcs.eam import eam_set_parameter
from pyAppGen.pbcs.eam import eam_simulate_strategy
from pyAppGen.pbcs.eam import eam_ui_contract
from pyAppGen.pbcs.eam import eam_verify_owned_table_boundary
from pyAppGen.pbcs.eam import implementation_contract as eam_package_contract


def test_eam_runtime_executes_standard_capabilities_with_package_local_contracts() -> None:
    runtime = eam_runtime_capabilities()
    smoke = eam_runtime_smoke()

    assert runtime["format"] == "appgen.eam-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/eam"
    assert runtime["owned_tables"] == EAM_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 25
    assert {"configuration_schema", "rule_engine", "parameter_engine", "workbench"} <= set(runtime["standard_features"])
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(EAM_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    package_contract = eam_package_contract()
    assert package_contract["pbc"] == "eam"
    assert package_contract["owns_code"] is True
    assert package_contract["side_effect_free"] is True
    assert package_contract["owned_tables"] == EAM_OWNED_TABLES
    assert package_contract["allowed_database_backends"] == EAM_ALLOWED_DATABASE_BACKENDS
    assert package_contract["required_event_topic"] == EAM_REQUIRED_EVENT_TOPIC
    assert package_contract["consumes"] == EAM_CONSUMED_EVENT_TYPES
    assert package_contract["emits"] == EAM_EMITTED_EVENT_TYPES
    assert package_contract["advanced_runtime"]["ok"] is True
    assert package_contract["ui_contract"]["ok"] is True
    assert package_contract["api_contract"]["event_contract"] == "AppGen-X"
    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True
    assert package_contract["permissions_contract"]["action_permissions"]["receive_event"] == "eam.execute"

    schema = eam_build_schema_contract()
    service = eam_build_service_contract()
    release = eam_build_release_evidence()
    assert schema["format"] == "appgen.eam-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(EAM_OWNED_TABLES)
    assert len(schema["migrations"]) == len(EAM_OWNED_TABLES)
    assert {"equipment", "work_order", "maintenance_outbox", "maintenance_inbox", "maintenance_dead_letter"} <= {
        item["table"] for item in schema["tables"]
    }
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.eam-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 16
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.eam-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]


def test_eam_runtime_applies_rules_parameters_events_and_ui() -> None:
    state = _configured_state()

    extension = eam_register_schema_extension(state, "equipment", {"inspection_payload": "jsonb"})
    state = extension["state"]
    assert extension["extension"]["version"] == 1

    equipment = eam_register_equipment(
        state,
        {
            "equipment_id": "eq_ops",
            "tenant": "tenant_ops",
            "site": "plant_ops",
            "asset_tag": "compressor_ops",
            "criticality": "A",
            "location": "line_ops",
            "parent_equipment_id": None,
            "warranty_until": "2027-12-31",
        },
    )
    state = equipment["state"]
    assert equipment["equipment"]["status"] == "active"

    plan = eam_create_maintenance_plan(
        state,
        {
            "plan_id": "plan_ops",
            "tenant": "tenant_ops",
            "equipment_id": "eq_ops",
            "strategy": "predictive",
            "interval_days": 30,
            "meter_threshold": 500,
            "condition_threshold": 0.7,
            "status": "released",
        },
    )
    state = plan["state"]
    assert plan["maintenance_plan"]["status"] == "active"

    condition = eam_record_condition_reading(
        state,
        {
            "reading_id": "cond_ops",
            "tenant": "tenant_ops",
            "equipment_id": "eq_ops",
            "sensor": "vibration",
            "value": 0.8,
            "unit": "ips",
            "captured_at": "2026-05-26T08:00:00Z",
        },
    )
    state = condition["state"]
    assert condition["condition_reading"]["alarm"] is True

    meter = eam_record_meter_reading(
        state,
        {
            "meter_id": "meter_ops",
            "tenant": "tenant_ops",
            "equipment_id": "eq_ops",
            "meter_name": "runtime_hours",
            "value": 560,
            "unit": "hours",
        },
    )
    state = meter["state"]
    assert meter["meter_reading"]["triggered_plans"] == ("plan_ops",)

    permit = eam_create_safety_permit(
        state,
        {
            "permit_id": "permit_ops",
            "tenant": "tenant_ops",
            "equipment_id": "eq_ops",
            "permit_type": "electrical",
            "risk_score": 0.6,
            "approved_by": "safety_ops",
        },
    )
    state = permit["state"]
    assert permit["permit"]["status"] == "approved"

    work_order = eam_create_work_order(
        state,
        {
            "work_order_id": "wo_ops",
            "tenant": "tenant_ops",
            "equipment_id": "eq_ops",
            "plan_id": "plan_ops",
            "work_type": "predictive",
            "priority": "critical",
            "failure_code": "bearing",
            "estimated_hours": 4,
            "required_skill": "mechanic",
            "permit_id": "permit_ops",
        },
    )
    state = work_order["state"]
    assert work_order["work_order"]["status"] == "planned"

    scheduled = eam_schedule_work_order(
        state,
        "wo_ops",
        window={"start": "2026-05-27T02:00:00Z", "carbon": 80},
        technician="tech_ops",
    )
    state = scheduled["state"]
    assert scheduled["work_order"]["status"] == "scheduled"

    spare = eam_issue_spare_part(
        state,
        {
            "usage_id": "spare_ops",
            "tenant": "tenant_ops",
            "work_order_id": "wo_ops",
            "part_number": "bearing_kit",
            "quantity": 2,
            "unit_cost": 125,
        },
    )
    state = spare["state"]
    assert spare["cost"] == 250

    complete = eam_complete_work_order(
        state,
        "wo_ops",
        completed_by="tech_ops",
        actual_hours=5,
        downtime_hours=3,
        resolution="bearing_replaced",
    )
    state = complete["state"]
    assert complete["work_order"]["status"] == "completed"
    assert complete["handoffs"] == (
        "production_uptime_projection",
        "inventory_spares_projection",
        "procurement_vendor_projection",
        "quality_reliability_projection",
    )
    assert state["outbox"][-1]["idempotency_key"] == "eam:MaintenanceCompleted:eam_evt_000009"

    simulation = eam_simulate_strategy(state, "plan_ops", proposed_interval_days=20)
    forecast = eam_forecast_failures((1, 2, 4), fleet_size=40)
    parsed = eam_parse_maintenance_instruction("equipment eq_777 work predictive priority high action schedule")
    route = eam_route_maintenance(
        {"event_id": "maint_route"},
        rails=(
            {"route": "mobile_api", "available": False, "latency": 3},
            {"route": "outbox", "available": True, "latency": 5},
        ),
    )
    recommendation = eam_recommend_exception_resolution("condition_alarm")
    proof = eam_generate_compliance_proof(state, "wo_ops", disclosure=("work_order_id", "equipment_id", "status"))
    screening = eam_screen_policy(state, "wo_ops", restricted_sites=("restricted_site",))
    controls = eam_run_control_tests(state)
    optimization = eam_optimize_maintenance_schedule(
        (
            {"plan": "defer", "risk_reduction": 0.4, "cost": 0.1},
            {"plan": "night_pm", "risk_reduction": 0.8, "cost": 0.25},
        )
    )
    allocation = eam_allocate_labor_and_spares(
        (
            {"crew": "mechanic", "priority": 0.9, "capacity": 6},
            {"crew": "contractor", "priority": 0.5, "capacity": 4},
        ),
        work_orders=5,
    )
    anomaly = eam_detect_failure_anomaly(state)
    stochastic = eam_model_stochastic_maintenance_exposure(failure_path=(1, 2, 5), volatility=0.15)
    carbon_window = eam_schedule_carbon_aware_maintenance(({"window": "day", "carbon": 180}, {"window": "night", "carbon": 75}))
    model = eam_register_governed_model(
        "maintenance_risk",
        {"features": ("condition", "criticality", "downtime"), "auc": 0.91, "drift_score": 0.03},
    )
    assert simulation["risk_delta"] < 0
    assert forecast["forecast_failures"] > 0
    assert parsed["equipment_id"] == "eq_777"
    assert route["route"] == "outbox"
    assert recommendation["action"] == "create_predictive_work_order"
    assert proof["proof"].startswith("zk_maintenance_")
    assert screening["decision"] == "clear"
    assert controls["ok"] is True
    assert optimization["plan"] == "night_pm"
    assert allocation["ok"] is True
    assert anomaly["ok"] is True
    assert stochastic["tail_risk"] > 0
    assert carbon_window["window"] == "night"
    assert model["governance"]["regulated"] is True

    workbench = eam_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["equipment_count"] == 1
    assert workbench["plan_count"] == 1
    assert workbench["work_order_count"] == 1
    assert workbench["completed_work_order_count"] == 1
    assert workbench["critical_work_order_count"] == 1
    assert workbench["spare_cost"] == 250
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 6
    assert workbench["rules_bound"] == ("rule_ops",)
    assert workbench["parameters_bound"] == (
        "criticality_weight",
        "default_pm_interval_days",
        "failure_risk_threshold",
        "mttr_target_hours",
        "retention_days",
        "safety_risk_threshold",
    )
    assert workbench["binding_evidence"]["shared_table_access"] is False
    assert workbench["binding_evidence"]["configuration_topic"] == EAM_REQUIRED_EVENT_TOPIC
    assert workbench["outbox_table"] == "maintenance_outbox"
    assert workbench["inbox_table"] == "maintenance_inbox"
    assert workbench["dead_letter_table"] == "maintenance_dead_letter"

    ui_contract = eam_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == EAM_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == EAM_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker"] is False
    assert ui_contract["configuration_editor"]["user_selectable_eventing"] is False
    assert "failure_risk_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["rule_editor"]["compile_evidence_visible"] is True
    assert ui_contract["binding_evidence"]["shared_table_access"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == EAM_OWNED_TABLES

    rendered = eam_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "eam.equipment",
            "eam.plan",
            "eam.execute",
            "eam.safety",
            "eam.configure",
            "eam.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert rendered["rules_bound"] == ("rule_ops",)
    assert rendered["parameters_bound"] == (
        "criticality_weight",
        "default_pm_interval_days",
        "failure_risk_threshold",
        "mttr_target_hours",
        "retention_days",
        "safety_risk_threshold",
    )
    assert rendered["event_outbox_count"] == 9
    assert rendered["binding_evidence"]["shared_table_access"] is False
    assert rendered["binding_evidence"]["configuration_topic"] == EAM_REQUIRED_EVENT_TOPIC
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]

    api = eam_build_api_contract()
    assert api["owned_tables"] == EAM_OWNED_TABLES
    assert api["database_backends"] == EAM_ALLOWED_DATABASE_BACKENDS
    assert api["required_event_topic"] == EAM_REQUIRED_EVENT_TOPIC
    assert api["events"]["emits"] == EAM_EMITTED_EVENT_TYPES
    assert api["events"]["consumes"] == EAM_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["command"] for route in api["route_definitions"] if "command" in route} >= {
        "register_equipment",
        "create_work_order",
        "configure_runtime",
    }
    assert api["idempotent_handlers"]["outbox_table"] == "maintenance_outbox"

    permissions = eam_permissions_contract()
    assert permissions["action_permissions"]["receive_event"] == "eam.execute"


def test_eam_rejects_invalid_inputs_and_proves_owned_boundaries_and_idempotency() -> None:
    state = eam_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        eam_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": EAM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "allowed_sites": ("plant_ops",),
                "allowed_priorities": ("low", "medium", "high", "critical"),
                "allowed_work_types": ("preventive", "predictive", "corrective"),
                "allowed_permit_types": ("electrical",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )

    with pytest.raises(ValueError, match=EAM_REQUIRED_EVENT_TOPIC):
        eam_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.topic",
                "retry_limit": 3,
                "allowed_sites": ("plant_ops",),
                "allowed_priorities": ("low", "medium", "high", "critical"),
                "allowed_work_types": ("preventive", "predictive", "corrective"),
                "allowed_permit_types": ("electrical",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )

    with pytest.raises(ValueError, match="does not expose stream-engine selection"):
        eam_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": EAM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "allowed_sites": ("plant_ops",),
                "allowed_priorities": ("low", "medium", "high", "critical"),
                "allowed_work_types": ("preventive", "predictive", "corrective"),
                "allowed_permit_types": ("electrical",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
                "stream_engine": "picker",
            },
        )

    state = _configured_state()

    with pytest.raises(ValueError, match="Unsupported Enterprise Asset Management parameter"):
        eam_set_parameter(state, "stream_engine", 1)

    with pytest.raises(ValueError, match="must be between"):
        eam_set_parameter(state, "failure_risk_threshold", 1.5)

    with pytest.raises(ValueError, match="Missing required Enterprise Asset Management rule fields"):
        eam_register_rule(
            state,
            {
                "rule_id": "rule_incomplete",
                "tenant": "tenant_ops",
                "status": "active",
            },
        )

    assert eam_register_schema_extension(state, "equipment", {"inspection_payload": "jsonb"})["ok"] is True
    assert eam_register_schema_extension(state, "inventory_lot", {"lot_payload": "jsonb"})["error"] == "table_not_owned"
    assert eam_register_schema_extension(state, "equipment", {"InvalidField": "jsonb"})["error"] == "invalid_extension_field"

    inbound = {
        "event_id": "inventory_reservation_ops",
        "event_type": "InventoryReservationConfirmed",
        "tenant": "tenant_ops",
        "payload": {"reservation_id": "res_ops", "work_order_id": "wo_ops", "part_number": "bearing_kit", "quantity": 2},
    }
    received = eam_receive_event(state, inbound)
    assert received["ok"] is True
    assert received["status"] == "processed"
    assert received["projection"] == "inventory_spares_projection"
    assert received["state"]["inventory_spares_projection"]["wo_ops"]["quantity"] == 2
    duplicate = eam_receive_event(received["state"], inbound)
    assert duplicate["status"] == "duplicate"
    assert duplicate["state"] == received["state"]
    dead_letter = eam_receive_event(
        received["state"],
        {"event_id": "bad_ops", "event_type": "UnknownMaintenanceEvent", "tenant": "tenant_ops", "payload": {}},
    )
    assert dead_letter["status"] == "dead_lettered"
    assert dead_letter["state"]["dead_letters"][-1]["reason"] == "unsupported_event_type"
    assert dead_letter["state"]["retry_evidence"][-1]["status"] == "dead_lettered"

    allowed = eam_verify_owned_table_boundary(
        (
            "equipment",
            "maintenance_plan",
            "maintenance_outbox",
            "eam_appgen_outbox_event",
            "inventory_spares_projection",
            "GET /quality/nonconformances/{id}",
        )
    )
    assert allowed["ok"] is True
    assert allowed["declared_dependencies"]["shared_tables"] == ()
    rejected = eam_verify_owned_table_boundary(("inventory_lot", "supplier_master"))
    assert rejected["ok"] is False
    assert rejected["violations"] == ("inventory_lot", "supplier_master")


def _configured_state() -> dict:
    state = eam_empty_state()
    state = eam_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": EAM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_sites": ("plant_ops",),
            "allowed_priorities": ("low", "medium", "high", "critical"),
            "allowed_work_types": ("preventive", "predictive", "corrective"),
            "allowed_permit_types": ("electrical",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("default_pm_interval_days", 30),
        ("failure_risk_threshold", 0.65),
        ("mttr_target_hours", 6),
        ("criticality_weight", 0.4),
        ("safety_risk_threshold", 0.7),
        ("retention_days", 90),
    ):
        state = eam_set_parameter(state, name, value)["state"]
    state = eam_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "maintenance",
            "eligible_work_types": ("preventive", "predictive", "corrective"),
            "allowed_sites": ("plant_ops",),
            "criticality_classes": ("A", "B"),
            "required_permits": ("electrical",),
            "failure_codes": ("bearing", "overheat"),
            "status": "active",
        },
    )["state"]
    return state
