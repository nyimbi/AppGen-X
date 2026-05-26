import pytest

from pyAppGen.pbcs.quality_assurance import QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.quality_assurance import QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.quality_assurance import QUALITY_ASSURANCE_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.quality_assurance import QUALITY_ASSURANCE_OWNED_TABLES
from pyAppGen.pbcs.quality_assurance import QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.quality_assurance import QUALITY_ASSURANCE_RUNTIME_TABLES
from pyAppGen.pbcs.quality_assurance import implementation_contract as package_implementation_contract
from pyAppGen.pbcs.quality_assurance import quality_assurance_build_api_contract
from pyAppGen.pbcs.quality_assurance import quality_assurance_build_release_evidence
from pyAppGen.pbcs.quality_assurance import quality_assurance_build_schema_contract
from pyAppGen.pbcs.quality_assurance import quality_assurance_build_service_contract
from pyAppGen.pbcs.quality_assurance import quality_assurance_permissions_contract
from pyAppGen.pbcs.quality_assurance import quality_assurance_receive_event
from pyAppGen.pbcs.quality_assurance import quality_assurance_register_schema_extension
from pyAppGen.pbcs.quality_assurance import quality_assurance_ui_binding_contract
from pyAppGen.pbcs.quality_assurance import quality_assurance_verify_owned_table_boundary
from pyAppGen.pbc import QUALITY_ASSURANCE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import quality_assurance_build_workbench_view
from pyAppGen.pbc import quality_assurance_configure_runtime
from pyAppGen.pbc import quality_assurance_create_inspection_plan
from pyAppGen.pbc import quality_assurance_create_quality_hold
from pyAppGen.pbc import quality_assurance_disposition_nonconformance
from pyAppGen.pbc import quality_assurance_empty_state
from pyAppGen.pbc import quality_assurance_raise_nonconformance
from pyAppGen.pbc import quality_assurance_record_inspection_result
from pyAppGen.pbc import quality_assurance_register_rule
from pyAppGen.pbc import quality_assurance_release_quality_hold
from pyAppGen.pbc import quality_assurance_render_workbench
from pyAppGen.pbc import quality_assurance_runtime_capabilities
from pyAppGen.pbc import quality_assurance_runtime_smoke
from pyAppGen.pbc import quality_assurance_set_parameter
from pyAppGen.pbc import quality_assurance_ui_contract


def test_quality_assurance_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = quality_assurance_runtime_capabilities()
    smoke = quality_assurance_runtime_smoke()

    assert runtime["format"] == "appgen.quality-assurance-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/quality_assurance"
    assert runtime["owned_tables"] == QUALITY_ASSURANCE_OWNED_TABLES
    assert runtime["runtime_tables"] == QUALITY_ASSURANCE_RUNTIME_TABLES
    assert runtime["required_event_topic"] == QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
    assert runtime["allowed_database_backends"] == QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
    assert len(runtime["standard_features"]) >= 30
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert {"build_schema_contract", "build_service_contract", "build_release_evidence", "ui_binding_contract"} <= set(runtime["operations"])
    assert smoke["ok"] is True
    assert set(QUALITY_ASSURANCE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("quality_assurance")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == QUALITY_ASSURANCE_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["required_event_topic"] == QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["emitted_events"] == QUALITY_ASSURANCE_EMITTED_EVENT_TYPES
    assert contract["source_package"]["consumed_events"] == QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["api_contract"]["shared_table_access"] is False
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "quality_assurance.event"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["ui_binding_contract"]["ok"] is True
    assert contract["source_package"]["boundary_contract"]["ok"] is True
    assert "QualityConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(QUALITY_ASSURANCE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("quality_assurance",))["ok"] is True
    assert pbc_implemented_capability_audit(("quality_assurance",))["ok"] is True
    package_contract = package_implementation_contract()
    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True
    assert package_contract["ui_binding_contract"]["ok"] is True

    api = quality_assurance_build_api_contract()
    permissions = quality_assurance_permissions_contract()
    assert api["format"] == "appgen.quality-assurance-api-contract.v1"
    assert api["owned_tables"] == QUALITY_ASSURANCE_OWNED_TABLES
    assert api["runtime_tables"] == QUALITY_ASSURANCE_RUNTIME_TABLES
    assert api["database_backends"] == QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
    assert api["required_event_topic"] == QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
    assert api["emits"] == QUALITY_ASSURANCE_EMITTED_EVENT_TYPES
    assert api["consumes"] == QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert api["dependencies"]["shared_tables"] == ()
    assert {route["route"] for route in api["routes"]} >= {
        "PUT /quality/configuration",
        "POST /quality/parameters",
        "POST /quality/rules",
        "POST /quality/events/inbox",
        "GET /quality/workbench",
        "GET /quality/schema-contract",
        "GET /quality/service-contract",
        "GET /quality/release-evidence",
        "GET /quality/ui-binding",
    }
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["receive_event"] == "quality_assurance.event"
    assert permissions["action_permissions"]["build_schema_contract"] == "quality_assurance.audit"
    assert permissions["action_permissions"]["build_service_contract"] == "quality_assurance.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "quality_assurance.audit"


def test_quality_assurance_package_schema_service_release_and_ui_binding_contracts() -> None:
    schema = quality_assurance_build_schema_contract()
    service = quality_assurance_build_service_contract()
    release = quality_assurance_build_release_evidence()
    ui_binding = quality_assurance_ui_binding_contract()
    api = quality_assurance_build_api_contract()

    assert schema["format"] == "appgen.quality-assurance-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(QUALITY_ASSURANCE_OWNED_TABLES)
    assert len(schema["migrations"]) == len(QUALITY_ASSURANCE_OWNED_TABLES)
    assert schema["datastore_backends"] == QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
    assert schema["shared_table_access"] is False
    assert {"calibration_schedule", "procedure_revision", "supplier_quality_profile", "customer_quality_case", "audit_evidence_packet"} <= {
        table["table"] for table in schema["tables"]
    }
    assert schema["runtime_tables"] == (
        {
            "table": QUALITY_ASSURANCE_RUNTIME_TABLES[0],
            "fields": ("tenant", "event_id", "event_type", "topic", "payload", "idempotency_key", "published_at", "audit_hash"),
        },
        {
            "table": QUALITY_ASSURANCE_RUNTIME_TABLES[1],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "status", "audit_hash"),
        },
        {
            "table": QUALITY_ASSURANCE_RUNTIME_TABLES[2],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "reason", "audit_hash"),
        },
    )

    assert service["format"] == "appgen.quality-assurance-service-contract.v1"
    assert service["ok"] is True
    assert service["transaction_boundary"] == "quality_assurance_owned_datastore_plus_appgen_outbox"
    assert service["idempotent_handlers"] == ("receive_event",)
    assert "build_release_evidence" in service["query_methods"]
    assert service["retry_dead_letter_evidence"]["dead_letter_table"] == QUALITY_ASSURANCE_RUNTIME_TABLES[2]
    assert service["eventing"]["contract"] == "AppGen-X"
    assert service["external_dependencies"]["shared_tables"] == ()

    assert ui_binding["format"] == "appgen.quality-assurance-ui-binding-contract.v1"
    assert ui_binding["ok"] is True
    assert ui_binding["binding_evidence"]["runtime_tables"] == QUALITY_ASSURANCE_RUNTIME_TABLES

    assert any(route["command"] == "register_rule" for route in api["routes"])
    assert any(route["command"] == "set_parameter" for route in api["routes"])
    assert any(route["command"] == "configure_runtime" for route in api["routes"])
    assert any(route.get("query") == "build_schema_contract" for route in api["routes"])
    assert any(route.get("query") == "build_service_contract" for route in api["routes"])
    assert any(route.get("query") == "build_release_evidence" for route in api["routes"])
    assert any(route.get("query") == "ui_binding_contract" for route in api["routes"])

    assert release["format"] == "appgen.quality-assurance-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert release["schema"]["format"] == schema["format"]
    assert release["service"]["format"] == service["format"]
    assert release["api"]["required_event_topic"] == QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
    assert release["ui_binding"]["binding_evidence"]["outbox_table"] == QUALITY_ASSURANCE_RUNTIME_TABLES[0]
    assert release["control"]["summary"]["duplicate_status"] == "duplicate"
    assert release["control"]["summary"]["retry_status"] == "retrying"
    assert release["control"]["summary"]["dead_letter_status"] == "dead_letter"


def test_quality_assurance_runtime_rejects_unsupported_backends_and_unknown_parameters() -> None:
    configuration = {
        "database_backend": "sqlite",
        "event_topic": "appgen.quality.events",
        "retry_limit": 3,
        "allowed_sites": ("factory_ops",),
        "allowed_inspection_sources": ("production",),
        "allowed_hold_reasons": ("defect",),
        "allowed_dispositions": ("rework", "release"),
        "default_timezone": "UTC",
        "workbench_limit": 50,
    }

    with pytest.raises(ValueError, match="supports only PostgreSQL, MySQL, or MariaDB"):
        quality_assurance_configure_runtime(quality_assurance_empty_state(), configuration)

    with pytest.raises(ValueError, match="does not allow stream-engine or user-selectable eventing fields"):
        quality_assurance_configure_runtime(quality_assurance_empty_state(), {**configuration, "database_backend": "postgresql", "stream_engine": "kafka"})

    with pytest.raises(ValueError, match="event topic is fixed"):
        quality_assurance_configure_runtime(quality_assurance_empty_state(), {**configuration, "database_backend": "postgresql", "event_topic": "custom.quality.events"})

    with pytest.raises(ValueError, match="Unsupported Quality Assurance parameter"):
        quality_assurance_set_parameter(quality_assurance_empty_state(), "unexpected_parameter", 3)


def test_quality_assurance_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = quality_assurance_empty_state()
    state = quality_assurance_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_sites": ("factory_ops",),
            "allowed_inspection_sources": ("production",),
            "allowed_hold_reasons": ("defect",),
            "allowed_dispositions": ("rework", "release"),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    assert state["configuration"]["event_contract"] == "AppGen-X"
    assert state["configuration"]["event_topic"] == QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
    assert state["configuration"]["owned_tables"] == QUALITY_ASSURANCE_OWNED_TABLES
    assert state["configuration"]["stream_engine_picker_visible"] is False
    assert state["configuration"]["user_eventing_choice"] is False
    state = quality_assurance_set_parameter(state, "default_sample_size", 5)["state"]
    state = quality_assurance_set_parameter(state, "defect_threshold", 1)["state"]
    state = quality_assurance_set_parameter(state, "cpk_minimum", 1.0)["state"]
    state = quality_assurance_set_parameter(state, "hold_severity_threshold", 0.7)["state"]
    state = quality_assurance_set_parameter(state, "capa_due_days", 14)["state"]
    rule_definition = {
        "rule_id": "rule_ops",
        "tenant": "tenant_ops",
        "rule_type": "quality",
        "eligible_sources": ("production",),
        "allowed_sites": ("factory_ops",),
        "sampling_methods": ("fixed",),
        "required_measurements": ("length", "torque"),
        "critical_defect_classes": ("safety",),
        "release_dispositions": ("release", "rework"),
        "status": "active",
    }
    rule = quality_assurance_register_rule(
        state,
        rule_definition,
    )
    state = rule["state"]
    extension = quality_assurance_register_schema_extension(state, "inspection_result", {"camera_payload": "jsonb"})
    state = extension["state"]
    assert extension["fields"]["camera_payload"] == "jsonb"
    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        quality_assurance_register_schema_extension(state, "production_order", {"external_payload": "jsonb"})
    consumed = quality_assurance_receive_event(
        state,
        {
            "event_id": "evt_prod_ops",
            "event_type": "ProductionCompleted",
            "payload": {"tenant": "tenant_ops", "order_id": "order_ops", "item": "machine_kit", "quantity": 10},
        },
    )
    state = consumed["state"]
    assert consumed["handler"]["status"] == "processed"
    assert state["production_completion_projections"]["order_ops"]["quantity"] == 10
    duplicate = quality_assurance_receive_event(
        state,
        {
            "event_id": "evt_prod_ops",
            "event_type": "ProductionCompleted",
            "payload": {"tenant": "tenant_ops", "order_id": "order_ops", "item": "machine_kit", "quantity": 10},
        },
    )
    assert duplicate["duplicate"] is True
    failed = quality_assurance_receive_event(state, {"event_id": "evt_bad_ops", "event_type": "UnsupportedQualitySignal", "payload": {"tenant": "tenant_ops"}}, simulate_failure=True)
    failed = quality_assurance_receive_event(failed["state"], {"event_id": "evt_bad_ops", "event_type": "UnsupportedQualitySignal", "payload": {"tenant": "tenant_ops"}}, simulate_failure=True)
    failed = quality_assurance_receive_event(failed["state"], {"event_id": "evt_bad_ops", "event_type": "UnsupportedQualitySignal", "payload": {"tenant": "tenant_ops"}}, simulate_failure=True)
    state = failed["state"]
    assert failed["handler"]["status"] == "dead_letter"
    assert state["dead_letters"][-1]["reason"] == "unsupported_or_failed_quality_event"
    assert rule["rule"]["compiled_hash"] == rule["rule"]["compile_evidence"]["compiled_hash"]
    assert rule["rule"]["compile_evidence"]["rule_id"] == "rule_ops"
    assert rule["rule"]["compile_evidence"]["required_fields"] == (
        "rule_id",
        "tenant",
        "rule_type",
        "eligible_sources",
        "allowed_sites",
        "sampling_methods",
        "required_measurements",
        "critical_defect_classes",
        "release_dispositions",
        "status",
    )
    assert rule["rule"]["compile_evidence"]["normalized_rule"]["rule_type"] == "quality"
    deterministic_rule = quality_assurance_register_rule(
        quality_assurance_empty_state(),
        {
            "tenant": "tenant_ops",
            "rule_id": "rule_ops",
            "eligible_sources": ("production",),
            "rule_type": "quality",
            "allowed_sites": ("factory_ops",),
            "required_measurements": ("length", "torque"),
            "sampling_methods": ("fixed",),
            "critical_defect_classes": ("safety",),
            "status": "active",
            "release_dispositions": ("release", "rework"),
        },
    )
    assert deterministic_rule["rule"]["compiled_hash"] == rule["rule"]["compiled_hash"]
    assert deterministic_rule["rule"]["compile_evidence"]["normalized_rule"] == rule["rule"]["compile_evidence"]["normalized_rule"]
    plan = quality_assurance_create_inspection_plan(
        state,
        {
            "plan_id": "plan_ops",
            "tenant": "tenant_ops",
            "item": "machine_kit",
            "site": "factory_ops",
            "source": "production",
            "sampling_method": "fixed",
            "sample_size": 5,
            "revision": "A",
            "status": "released",
        },
    )
    state = plan["state"]
    assert plan["inspection_plan"]["status"] == "active"

    result = quality_assurance_record_inspection_result(
        state,
        {
            "result_id": "result_ops",
            "tenant": "tenant_ops",
            "plan_id": "plan_ops",
            "lot_id": "lot_ops",
            "order_id": "order_ops",
            "measurements": {"length": (10.0, 10.1, 9.9), "torque": (5.0, 5.1, 4.9)},
            "defects": ("scratch",),
            "inspector": "qa_ops",
        },
    )
    state = result["state"]
    assert result["decision"] in {"pass", "fail"}
    assert result["spc"]["cpk"] > 0

    hold = quality_assurance_create_quality_hold(
        state,
        {"hold_id": "hold_ops", "tenant": "tenant_ops", "item": "machine_kit", "lot_id": "lot_ops", "site": "factory_ops", "reason": "defect", "severity": 0.8},
    )
    state = hold["state"]
    assert hold["hold"]["status"] == "active"

    nc = quality_assurance_raise_nonconformance(
        state,
        {"nonconformance_id": "nc_ops", "tenant": "tenant_ops", "result_id": "result_ops", "defect_class": "safety", "severity": 0.8, "root_cause": "assembly_variation"},
    )
    state = nc["state"]
    assert nc["nonconformance"]["severity_class"] == "critical"

    disposition = quality_assurance_disposition_nonconformance(state, "nc_ops", disposition="rework", approved_by="qa_mgr")
    state = disposition["state"]
    assert disposition["nonconformance"]["status"] == "dispositioned"

    release = quality_assurance_release_quality_hold(state, "hold_ops", released_by="qa_mgr")
    state = release["state"]
    assert release["hold"]["status"] == "released"
    assert release["handoffs"] == ("inventory_release_projection", "production_quality_projection", "supplier_score_projection")
    assert state["outbox"][-1]["idempotency_key"] == "quality_assurance:QualityHoldReleased:quality_evt_000006"

    workbench = quality_assurance_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["plan_count"] == 1
    assert workbench["inspection_count"] == 1
    assert workbench["hold_count"] == 1
    assert workbench["released_hold_count"] == 1
    assert workbench["nonconformance_count"] == 1
    assert workbench["critical_nonconformance_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rules_bound"] == ("rule_ops",)
    assert "default_sample_size" in workbench["parameters_bound"]
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["owned_tables"] == QUALITY_ASSURANCE_OWNED_TABLES
    assert workbench["binding_evidence"]["runtime_tables"] == {
        "outbox": QUALITY_ASSURANCE_RUNTIME_TABLES[0],
        "inbox": QUALITY_ASSURANCE_RUNTIME_TABLES[1],
        "dead_letter": QUALITY_ASSURANCE_RUNTIME_TABLES[2],
    }
    assert workbench["binding_evidence"]["event_counts"]["inbox"] == 4
    assert workbench["binding_evidence"]["event_counts"]["dead_letter"] == 1
    assert workbench["binding_evidence"]["rbac"]["receive_event"] == "quality_assurance.event"
    assert workbench["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False
    assert workbench["binding_evidence"]["configuration"]["user_eventing_choice"] is False
    assert workbench["binding_evidence"]["ui_binding"]["runtime_tables"] == QUALITY_ASSURANCE_RUNTIME_TABLES
    assert workbench["binding_evidence"]["workbench_route"] == "/workbench/pbcs/quality_assurance"
    assert workbench["binding_evidence"]["rules"] == (
        {
            "rule_id": "rule_ops",
            "scope": "quality",
            "enabled": True,
            "compiled_hash": rule["rule"]["compiled_hash"],
        },
    )
    assert {item["name"] for item in workbench["binding_evidence"]["parameters"]} == {
        "capa_due_days",
        "cpk_minimum",
        "default_sample_size",
        "defect_threshold",
        "hold_severity_threshold",
    }
    assert workbench["binding_evidence"]["binding_hash"]

    ui_contract = quality_assurance_ui_contract()
    assert ui_contract["owned_tables"] == QUALITY_ASSURANCE_OWNED_TABLES
    assert ui_contract["runtime_tables"]["inbox"] == QUALITY_ASSURANCE_RUNTIME_TABLES[1]
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["required_event_topic"] == QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["event_topic"] == QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["visible_event_contracts"] == ("AppGen-X",)
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["user_eventing_choice_visible"] is False
    assert "default_sample_size" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "release_approval_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert ui_contract["parameter_editor"]["supported_parameters"] == ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert "required_measurements" in ui_contract["rule_editor"]["required_fields"]
    assert "quality" not in ui_contract["rule_editor"]["rule_types"]
    assert ui_contract["rule_editor"]["legacy_rule_type_aliases"] == ("quality",)
    assert ui_contract["rule_editor"]["compiled_evidence_fields"] == ("compiled_hash", "compile_evidence")
    assert ui_contract["event_surfaces"]["emits"] == QUALITY_ASSURANCE_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["required_event_topic"] == QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
    assert ui_contract["event_surfaces"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"] == {
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "runtime_tables": QUALITY_ASSURANCE_RUNTIME_TABLES,
        "workbench_route": "/workbench/pbcs/quality_assurance",
        "outbox_table": QUALITY_ASSURANCE_RUNTIME_TABLES[0],
        "inbox_table": QUALITY_ASSURANCE_RUNTIME_TABLES[1],
        "dead_letter_table": QUALITY_ASSURANCE_RUNTIME_TABLES[2],
        "shared_table_access": False,
    }
    assert "CalibrationConsole" in ui_contract["fragments"]
    assert "AuditEvidenceViewer" in ui_contract["fragments"]
    rendered = quality_assurance_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "quality_assurance.inspect",
            "quality_assurance.hold",
            "quality_assurance.disposition",
            "quality_assurance.configure",
            "quality_assurance.audit",
            "quality_assurance.event",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert rendered["event_inbox_count"] == 4
    assert rendered["dead_letter_count"] == 1
    assert rendered["owned_tables"] == QUALITY_ASSURANCE_OWNED_TABLES
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["configuration"] == workbench["binding_evidence"]["configuration"]
    assert rendered["binding_evidence"]["ui_bindings"]["rbac"]["receive_event"] == "quality_assurance.event"

    boundary = quality_assurance_verify_owned_table_boundary(
        ("inspection_result", "ProductionCompleted", "production_completion_projection", "quality_assurance_appgen_inbox_event")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = quality_assurance_verify_owned_table_boundary(("production_order", "inventory_balance"))
    assert violation["ok"] is False
    assert violation["violations"] == ("production_order", "inventory_balance")
    assert rendered["binding_evidence"]["rules"] == workbench["binding_evidence"]["rules"]
    assert rendered["binding_evidence"]["parameters"] == workbench["binding_evidence"]["parameters"]
    assert rendered["binding_evidence"]["ui_bindings"] == {
        "configuration_fragment": "QualityConfigurationPanel",
        "rule_fragment": "QualityRuleStudio",
        "parameter_fragment": "QualityParameterConsole",
        "audit_fragment": "AuditEvidenceViewer",
        "release_fragment": "ReleaseEvidencePanel",
        "outbox_table": QUALITY_ASSURANCE_RUNTIME_TABLES[0],
        "inbox_table": QUALITY_ASSURANCE_RUNTIME_TABLES[1],
        "dead_letter_table": QUALITY_ASSURANCE_RUNTIME_TABLES[2],
        "rbac": ui_contract["action_permissions"],
    }
