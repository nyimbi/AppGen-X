import pytest

from pyAppGen.pbc import PRODUCTION_CONTROL_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import production_control_allocate_capacity_plan
from pyAppGen.pbc import production_control_append_audit_entry
from pyAppGen.pbc import production_control_book_labor_time
from pyAppGen.pbc import production_control_book_machine_time
from pyAppGen.pbc import production_control_build_workbench_view
from pyAppGen.pbc import production_control_capture_oee_snapshot
from pyAppGen.pbc import production_control_complete_production_order
from pyAppGen.pbc import production_control_configure_runtime
from pyAppGen.pbc import production_control_confirm_operation
from pyAppGen.pbc import production_control_create_production_order
from pyAppGen.pbc import production_control_define_routing_step
from pyAppGen.pbc import production_control_empty_state
from pyAppGen.pbc import production_control_open_exception_case
from pyAppGen.pbc import production_control_record_completion_proof
from pyAppGen.pbc import production_control_record_downtime
from pyAppGen.pbc import production_control_record_material_consumption
from pyAppGen.pbc import production_control_record_quality_gate_result
from pyAppGen.pbc import production_control_record_scrap_rework
from pyAppGen.pbc import production_control_register_rule
from pyAppGen.pbc import production_control_register_work_center
from pyAppGen.pbc import production_control_render_workbench
from pyAppGen.pbc import production_control_runtime_capabilities
from pyAppGen.pbc import production_control_runtime_smoke
from pyAppGen.pbc import production_control_schedule_order
from pyAppGen.pbc import production_control_set_parameter
from pyAppGen.pbc import production_control_start_operation
from pyAppGen.pbc import production_control_ui_contract
from pyAppGen.pbcs.production_control import PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.production_control import PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.production_control import PRODUCTION_CONTROL_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.production_control import PRODUCTION_CONTROL_OWNED_TABLES
from pyAppGen.pbcs.production_control import PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.production_control import production_control_build_api_contract
from pyAppGen.pbcs.production_control import production_control_build_release_evidence
from pyAppGen.pbcs.production_control import production_control_build_schema_contract
from pyAppGen.pbcs.production_control import production_control_build_service_contract
from pyAppGen.pbcs.production_control import production_control_permissions_contract
from pyAppGen.pbcs.production_control import production_control_receive_event
from pyAppGen.pbcs.production_control import production_control_register_schema_extension
from pyAppGen.pbcs.production_control import production_control_verify_owned_table_boundary


def test_production_control_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = production_control_runtime_capabilities()
    smoke = production_control_runtime_smoke()

    assert runtime["format"] == "appgen.production-control-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/production_control"
    assert len(runtime["standard_features"]) >= 24
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(PRODUCTION_CONTROL_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("production_control")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "ProductionConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(PRODUCTION_CONTROL_ADVANCED_CAPABILITY_KEYS)
    assert contract["source_package"]["owned_tables"] == PRODUCTION_CONTROL_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["required_event_topic"] == PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["api_contract"]["shared_table_access"] is False
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "production_control.event"
    assert pbc_implementation_release_audit(("production_control",))["ok"] is True
    assert pbc_implemented_capability_audit(("production_control",))["ok"] is True


def test_production_control_package_schema_service_and_release_evidence_contracts() -> None:
    schema = production_control_build_schema_contract()
    service = production_control_build_service_contract()
    release = production_control_build_release_evidence()
    api = production_control_build_api_contract()

    assert schema["format"] == "appgen.production-control-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(PRODUCTION_CONTROL_OWNED_TABLES)
    assert schema["runtime_tables"] == (
        {
            "table": "production_control_appgen_outbox_event",
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "published_at", "audit_hash"),
        },
        {
            "table": "production_control_appgen_inbox_event",
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "audit_hash"),
        },
        {
            "table": "production_control_dead_letter_event",
            "fields": ("tenant", "event_id", "event_type", "payload", "reason", "attempts", "audit_hash"),
        },
    )
    assert schema["datastore_backends"] == PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS
    assert schema["shared_table_access"] is False
    assert {
        "material_consumption",
        "wip_inventory",
        "labor_time_booking",
        "machine_time_booking",
        "quality_gate_result",
        "production_completion_record",
        "completion_proof",
        "production_audit_entry",
    } <= {table["table"] for table in schema["tables"]}
    assert {
        ("material_consumption", "production_order"),
        ("quality_gate_result", "routing_step"),
        ("completion_proof", "production_order"),
    } <= {(relationship["from_table"], relationship["to_table"]) for relationship in schema["relationships"]}

    assert service["format"] == "appgen.production-control-service-contract.v1"
    assert service["ok"] is True
    assert service["transaction_boundary"] == "production_control_owned_datastore_plus_appgen_outbox"
    assert "receive_event" in service["idempotent_handlers"]
    assert {"record_material_consumption", "book_labor_time", "record_quality_gate_result", "record_completion_proof"} <= set(service["command_methods"])
    assert "build_release_evidence" in service["query_methods"]
    assert service["external_dependencies"]["shared_tables"] == ()

    assert any(route["command"] == "register_rule" for route in api["routes"])
    assert any(route["command"] == "record_material_consumption" for route in api["routes"])
    assert any(route["command"] == "record_quality_gate_result" for route in api["routes"])
    assert any(route["command"] == "record_completion_proof" for route in api["routes"])
    assert any(route["command"] == "set_parameter" for route in api["routes"])
    assert any(route["command"] == "configure_runtime" for route in api["routes"])
    assert any(route.get("query") == "build_schema_contract" for route in api["routes"])
    assert any(route.get("query") == "build_service_contract" for route in api["routes"])
    assert any(route.get("query") == "build_release_evidence" for route in api["routes"])

    assert release["format"] == "appgen.production-control-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert "execution_record_depth" in {check["id"] for check in release["checks"] if check["ok"]}
    assert release["schema"]["format"] == schema["format"]
    assert release["service"]["format"] == service["format"]
    assert release["api"]["required_event_topic"] == PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC


def test_production_control_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = production_control_empty_state()
    state = production_control_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_sites": ("factory_ops",),
            "allowed_work_center_types": ("assembly",),
            "allowed_downtime_reasons": ("maintenance", "material"),
            "allowed_production_routes": ("make",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = production_control_set_parameter(state, "capacity_threshold", 0.85)["state"]
    state = production_control_set_parameter(state, "oee_target", 0.75)["state"]
    state = production_control_set_parameter(state, "scrap_threshold", 0.05)["state"]
    state = production_control_set_parameter(state, "takt_time_minutes", 10)["state"]
    state = production_control_set_parameter(state, "schedule_horizon_days", 14)["state"]
    state = production_control_set_parameter(state, "downtime_severity_minutes", 30)["state"]
    rule = production_control_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "production",
            "eligible_work_center_types": ("assembly",),
            "allowed_sites": ("factory_ops",),
            "allowed_routes": ("make",),
            "quality_gates": ("final_test",),
            "asset_commissioning_items": ("machine_kit",),
            "dispatch_priorities": ("expedite", "standard"),
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
        "eligible_work_center_types",
        "allowed_sites",
        "allowed_routes",
        "status",
    )
    state = production_control_register_work_center(
        state,
        {
            "work_center_id": "wc_ops",
            "tenant": "tenant_ops",
            "site": "factory_ops",
            "name": "Assembly Cell",
            "work_center_type": "assembly",
            "capacity_hours": 8,
            "efficiency": 0.9,
            "status": "available",
            "identity": {"did": "did:appgen:wc-ops", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    order = production_control_create_production_order(
        state,
        {
            "order_id": "order_ops",
            "tenant": "tenant_ops",
            "site": "factory_ops",
            "item": "machine_kit",
            "quantity": 10,
            "route": "make",
            "priority": "standard",
            "planned_order_id": "po_ops",
        },
    )
    state = order["state"]
    assert order["production_order"]["status"] == "created"

    state = production_control_define_routing_step(
        state,
        {
            "step_id": "step_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "sequence": 10,
            "work_center_id": "wc_ops",
            "standard_minutes": 100,
            "setup_minutes": 20,
            "quality_gate": "final_test",
        },
    )["state"]
    schedule = production_control_schedule_order(state, "order_ops", scheduled_by="scheduler_ops")
    state = schedule["state"]
    assert schedule["schedule"]["step_count"] == 1

    state = production_control_start_operation(state, "step_ops", started_by="operator_ops")["state"]
    material = production_control_record_material_consumption(
        state,
        {
            "consumption_id": "mat_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "material_id": "steel_kit",
            "quantity": 10,
            "uom": "EA",
            "source": "inventory_material_readiness_projection",
        },
    )
    state = material["state"]
    assert material["wip"]["quantity_in_process"] == 10
    labor = production_control_book_labor_time(
        state,
        {
            "booking_id": "lab_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "step_id": "step_ops",
            "operator_id": "operator_ops",
            "hours": 2,
        },
    )
    state = labor["state"]
    machine = production_control_book_machine_time(
        state,
        {
            "booking_id": "mach_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "step_id": "step_ops",
            "work_center_id": "wc_ops",
            "hours": 2.3,
        },
    )
    state = machine["state"]
    downtime = production_control_record_downtime(
        state,
        {"downtime_id": "dt_ops", "tenant": "tenant_ops", "work_center_id": "wc_ops", "order_id": "order_ops", "reason": "maintenance", "minutes": 20},
    )
    state = downtime["state"]
    assert downtime["downtime"]["status"] == "captured"
    quality = production_control_record_quality_gate_result(
        state,
        {
            "gate_id": "qg_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "step_id": "step_ops",
            "quality_gate": "final_test",
            "result": "passed",
            "inspector": "qa_ops",
        },
    )
    state = quality["state"]
    assert quality["quality_gate"]["status"] == "accepted"
    scrap = production_control_record_scrap_rework(
        state,
        {
            "scrap_rework_id": "sr_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "step_id": "step_ops",
            "scrap_qty": 1,
            "rework_qty": 0,
            "reason": "setup_loss",
        },
    )
    state = scrap["state"]
    assert scrap["scrap_rework"]["status"] == "captured"

    confirmation = production_control_confirm_operation(
        state,
        "step_ops",
        good_qty=9,
        scrap_qty=1,
        labor_hours=2,
        machine_hours=2.3,
        confirmed_by="operator_ops",
    )
    state = confirmation["state"]
    assert confirmation["routing_step"]["status"] == "confirmed"

    oee_snapshot = production_control_capture_oee_snapshot(
        state,
        {"snapshot_id": "oee_ops", "tenant": "tenant_ops", "work_center_id": "wc_ops", "order_id": "order_ops"},
    )
    state = oee_snapshot["state"]
    assert oee_snapshot["snapshot"]["status"] == "captured"
    exception = production_control_open_exception_case(
        state,
        {"case_id": "case_ops", "tenant": "tenant_ops", "order_id": "order_ops", "case_type": "downtime", "severity": "minor", "status": "resolved"},
    )
    state = exception["state"]
    assert exception["case"]["recommended_action"] == "route_maintenance_review"
    capacity = production_control_allocate_capacity_plan(
        state,
        {"allocation_id": "cap_ops", "tenant": "tenant_ops", "order_id": "order_ops", "work_center_id": "wc_ops", "allocated_hours": 7, "priority": "standard"},
    )
    state = capacity["state"]
    assert capacity["allocation"]["status"] == "allocated"
    completed = production_control_complete_production_order(state, "order_ops", completed_by="supervisor_ops")
    state = completed["state"]
    assert completed["production_order"]["status"] == "completed"
    assert completed["handoffs"] == ("inventory_receipt_projection", "quality_completion_projection", "asset_commissioning_projection")
    assert state["outbox"][-1]["idempotency_key"] == "production_control:ProductionCompleted:production_evt_000014"
    proof = production_control_record_completion_proof(
        state,
        {"proof_id": "proof_ops", "tenant": "tenant_ops", "order_id": "order_ops", "proof_hash": "hash_ops", "proof_type": "completion"},
    )
    state = proof["state"]
    audit = production_control_append_audit_entry(state, "completion_proof", proof["proof"])
    state = audit["state"]
    assert proof["proof"]["status"] == "sealed"
    assert audit["audit_entry"]["status"] == "sealed"

    workbench = production_control_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["work_center_count"] == 1
    assert workbench["order_count"] == 1
    assert workbench["completed_order_count"] == 1
    assert workbench["routing_step_count"] == 1
    assert workbench["downtime_count"] == 1
    assert workbench["completed_qty"] == 9
    assert workbench["oee"] > 0
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 6
    assert workbench["binding_evidence"]["configuration"] == {
        "bound": True,
        "database_backend": "postgresql",
        "event_contract": "AppGen-X",
        "event_topic": PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
        "visible_event_contracts": ("AppGen-X",),
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "supported_fields": (
            "database_backend",
            "event_topic",
            "retry_limit",
            "allowed_sites",
            "allowed_work_center_types",
            "allowed_downtime_reasons",
            "allowed_production_routes",
            "default_timezone",
            "workbench_limit",
        ),
    }
    assert workbench["binding_evidence"]["rules"] == (
        {
            "rule_id": "rule_ops",
            "scope": "production",
            "compiled_hash": rule["rule"]["compiled_hash"],
            "required_fields": rule["rule"]["compiled_evidence"]["required_fields"],
        },
    )
    assert workbench["binding_evidence"]["parameters"] == {
        "supported": (
            "capacity_threshold",
            "oee_target",
            "scrap_threshold",
            "takt_time_minutes",
            "schedule_horizon_days",
            "downtime_severity_minutes",
        ),
        "active": (
            "capacity_threshold",
            "downtime_severity_minutes",
            "oee_target",
            "schedule_horizon_days",
            "scrap_threshold",
            "takt_time_minutes",
        ),
    }

    ui_contract = production_control_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["required_event_topic"] == PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["visible_event_contracts"] == ("AppGen-X",)
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["user_selectable_event_contract"] is False
    assert ui_contract["event_surfaces"]["emits"] == PRODUCTION_CONTROL_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES
    assert ui_contract["binding_evidence"]["owned_tables"] == PRODUCTION_CONTROL_OWNED_TABLES
    assert ui_contract["binding_evidence"]["shared_table_access"] is False
    assert "capacity_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert "allowed_routes" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["rule_editor"]["compiled_evidence_fields"] == ("compiled_hash", "compiled_evidence")
    rendered = production_control_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "production_control.schedule",
            "production_control.operate",
            "production_control.complete",
            "production_control.event",
            "production_control.configure",
            "production_control.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 14
    assert rendered["inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["rules_bound"] == ("rule_ops",)
    assert rendered["parameters_bound"] == (
        "capacity_threshold",
        "downtime_severity_minutes",
        "oee_target",
        "schedule_horizon_days",
        "scrap_threshold",
        "takt_time_minutes",
    )
    assert rendered["binding_evidence"]["configuration"] == workbench["binding_evidence"]["configuration"]
    assert rendered["binding_evidence"]["rules"] == (
        {
            "rule_id": "rule_ops",
            "compiled_hash": rule["rule"]["compiled_hash"],
            "required_fields": rule["rule"]["compiled_evidence"]["required_fields"],
        },
    )
    assert rendered["binding_evidence"]["parameters"] == workbench["binding_evidence"]["parameters"]


def test_production_control_rejects_unsupported_backends_unknown_parameters_and_stream_picker_config() -> None:
    state = production_control_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        production_control_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "allowed_sites": ("factory_ops",),
                "allowed_work_center_types": ("assembly",),
                "allowed_downtime_reasons": ("maintenance",),
                "allowed_production_routes": ("make",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        production_control_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "allowed_sites": ("factory_ops",),
                "allowed_work_center_types": ("assembly",),
                "allowed_downtime_reasons": ("maintenance",),
                "allowed_production_routes": ("make",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Production Control parameter"):
        production_control_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="requires AppGen-X event topic"):
        production_control_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.topic",
                "retry_limit": 3,
                "allowed_sites": ("factory_ops",),
                "allowed_work_center_types": ("assembly",),
                "allowed_downtime_reasons": ("maintenance",),
                "allowed_production_routes": ("make",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )


def test_production_control_package_contract_handles_events_schema_api_permissions_and_boundaries() -> None:
    state = production_control_empty_state()
    state = production_control_configure_runtime(
        state,
        {
            "database_backend": "mariadb",
            "event_topic": PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "allowed_sites": ("factory_ops",),
            "allowed_work_center_types": ("assembly",),
            "allowed_downtime_reasons": ("maintenance",),
            "allowed_production_routes": ("make",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]

    extension = production_control_register_schema_extension(
        state,
        "production_order",
        {"digital_thread_payload": "jsonb"},
    )
    state = extension["state"]
    assert extension["schema_extension"] == {
        "table": "production_order",
        "fields": {"digital_thread_payload": "jsonb"},
    }
    assert state["schema_extensions"]["production_order"]["digital_thread_payload"] == "jsonb"

    with pytest.raises(ValueError, match="owned tables"):
        production_control_register_schema_extension(state, "inventory_balance", {"foreign_payload": "jsonb"})

    bad_field = production_control_register_schema_extension(state, "routing_step", {"BadName": "text"})
    assert bad_field["ok"] is False
    assert bad_field["error"] == "invalid_extension_field"

    planned = production_control_receive_event(
        state,
        {
            "event_id": "mrp_evt_ops",
            "event_type": "PlannedOrderReleased",
            "payload": {
                "planned_order_id": "po_ops",
                "tenant": "tenant_ops",
                "site": "factory_ops",
                "item": "machine_kit",
                "quantity": 12,
                "route": "make",
                "priority": "expedite",
            },
        },
    )
    state = planned["state"]
    assert planned["ok"] is True
    assert state["planned_order_projections"]["po_ops"]["quantity"] == 12
    duplicate = production_control_receive_event(
        state,
        {
            "event_id": "mrp_evt_ops",
            "event_type": "PlannedOrderReleased",
            "payload": {
                "planned_order_id": "po_ops",
                "tenant": "tenant_ops",
                "site": "factory_ops",
                "item": "machine_kit",
                "quantity": 12,
            },
        },
    )
    assert duplicate["duplicate"] is True
    assert duplicate["state"] is state

    failed_once = production_control_receive_event(
        state,
        {
            "event_id": "quality_evt_ops",
            "event_type": "QualityGateReleased",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    assert failed_once["ok"] is False
    assert failed_once["handler"]["status"] == "retrying"
    failed_twice = production_control_receive_event(
        failed_once["state"],
        {
            "event_id": "quality_evt_ops",
            "event_type": "QualityGateReleased",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    assert failed_twice["handler"]["status"] == "dead_letter"
    assert failed_twice["state"]["dead_letter"][-1]["reason"] == "unsupported_or_failed_production_control_event"

    api = production_control_build_api_contract()
    assert api["format"] == "appgen.production-control-api-contract.v1"
    assert api["event_contract"] == "AppGen-X"
    assert api["required_event_topic"] == PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC
    assert api["database_backends"] == PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS
    assert api["owned_tables"] == PRODUCTION_CONTROL_OWNED_TABLES
    assert api["events"] == {
        "emits": PRODUCTION_CONTROL_EMITTED_EVENT_TYPES,
        "consumes": PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES,
    }
    assert api["shared_table_access"] is False
    assert any(route["command"] == "receive_event" for route in api["routes"])

    permissions = production_control_permissions_contract()
    assert permissions["action_permissions"]["receive_event"] == "production_control.event"
    assert permissions["action_permissions"]["register_schema_extension"] == "production_control.configure"
    assert permissions["action_permissions"]["verify_owned_table_boundary"] == "production_control.audit"
    assert permissions["action_permissions"]["build_schema_contract"] == "production_control.audit"
    assert permissions["action_permissions"]["build_service_contract"] == "production_control.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "production_control.audit"

    valid_boundary = production_control_verify_owned_table_boundary(
        (
            "production_order",
            "production_control_appgen_inbox_event",
            "PlannedOrderReleased",
            "mrp_planned_order_projection",
            "POST /inventory-receipts",
        )
    )
    assert valid_boundary["ok"] is True
    assert valid_boundary["declared_dependencies"]["shared_tables"] == ()

    invalid_boundary = production_control_verify_owned_table_boundary(("inventory_balance", "quality_result"))
    assert invalid_boundary["ok"] is False
    assert invalid_boundary["violations"] == ("inventory_balance", "quality_result")
