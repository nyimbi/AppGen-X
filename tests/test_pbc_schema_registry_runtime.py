import pytest

from pyAppGen.pbc import SCHEMA_REGISTRY_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbc import SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES
from pyAppGen.pbc import SCHEMA_REGISTRY_EMITTED_EVENT_TYPES
from pyAppGen.pbc import SCHEMA_REGISTRY_OWNED_TABLES
from pyAppGen.pbc import SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC
from pyAppGen.pbc import schema_registry_build_api_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import schema_registry_build_workbench_view
from pyAppGen.pbc import schema_registry_configure_runtime
from pyAppGen.pbc import schema_registry_define_compatibility_rule
from pyAppGen.pbc import schema_registry_empty_state
from pyAppGen.pbc import schema_registry_permissions_contract
from pyAppGen.pbc import schema_registry_publish_contract_projection
from pyAppGen.pbc import schema_registry_receive_event
from pyAppGen.pbc import schema_registry_record_contract_violation
from pyAppGen.pbc import schema_registry_register_consumer_binding
from pyAppGen.pbc import schema_registry_register_rule
from pyAppGen.pbc import schema_registry_register_schema_extension
from pyAppGen.pbc import schema_registry_register_subject
from pyAppGen.pbc import schema_registry_render_workbench
from pyAppGen.pbc import schema_registry_run_compatibility_check
from pyAppGen.pbc import schema_registry_runtime_capabilities
from pyAppGen.pbc import schema_registry_runtime_smoke
from pyAppGen.pbc import schema_registry_set_parameter
from pyAppGen.pbc import schema_registry_submit_schema_version
from pyAppGen.pbc import schema_registry_ui_contract
from pyAppGen.pbc import schema_registry_validate_payload
from pyAppGen.pbc import schema_registry_verify_owned_table_boundary


def test_schema_registry_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = schema_registry_runtime_capabilities()
    smoke = schema_registry_runtime_smoke()

    assert runtime["format"] == "appgen.schema-registry-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/schema_registry"
    assert runtime["owned_tables"] == SCHEMA_REGISTRY_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(SCHEMA_REGISTRY_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("schema_registry")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == SCHEMA_REGISTRY_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "schema_registry.event"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "SchemaConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(SCHEMA_REGISTRY_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("schema_registry",))["ok"] is True
    assert pbc_implemented_capability_audit(("schema_registry",))["ok"] is True

    api = schema_registry_build_api_contract()
    permissions = schema_registry_permissions_contract()
    assert api["format"] == "appgen.schema-registry-api-contract.v1"
    assert api["owned_tables"] == SCHEMA_REGISTRY_OWNED_TABLES
    assert api["database_backends"] == SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == SCHEMA_REGISTRY_EMITTED_EVENT_TYPES
    assert api["consumes"] == SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {"POST /schemas/subjects", "POST /schemas/events/inbox", "GET /schemas/subjects"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["publish_contract_projection"] == "schema_registry.publish"


def test_schema_registry_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = schema_registry_empty_state()
    state = schema_registry_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_formats": ("json", "event", "api"),
            "default_compatibility": "backward_forward",
            "namespace_policy": "tenant_scoped",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = schema_registry_set_parameter(state, "compatibility_threshold", 0.9)["state"]
    state = schema_registry_set_parameter(state, "max_schema_fields", 64)["state"]
    state = schema_registry_set_parameter(state, "semantic_similarity_floor", 0.82)["state"]
    state = schema_registry_set_parameter(state, "violation_risk_threshold", 0.45)["state"]
    state = schema_registry_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "event",
            "mode": "backward_forward",
            "classification": "regulated",
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    extension = schema_registry_register_schema_extension(state, "schema_version", {"semantic_tags": "jsonb", "lineage_payload": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["schema_version"]["lineage_payload"] == "jsonb"
    deployed_event = schema_registry_receive_event(
        state,
        {"event_id": "evt_pbc_ops", "event_type": "PbcDeployed", "payload": {"tenant": "tenant_ops", "pbc": "checkout_processing", "subject_id": "subject_order"}},
    )
    state = deployed_event["state"]
    assert deployed_event["handler"]["status"] == "processed"
    duplicate = schema_registry_receive_event(
        state,
        {"event_id": "evt_pbc_ops", "event_type": "PbcDeployed", "payload": {"tenant": "tenant_ops", "pbc": "checkout_processing", "subject_id": "subject_order"}},
    )
    assert duplicate["duplicate"] is True

    subject = schema_registry_register_subject(
        state,
        {
            "subject_id": "subject_order",
            "tenant": "tenant_ops",
            "owner_pbc": "checkout_processing",
            "name": "OrderAccepted",
            "channel": "event",
            "format": "json",
            "namespace": "commerce.order",
        },
    )
    state = subject["state"]
    assert subject["subject"]["status"] == "active"

    compatibility_rule = schema_registry_define_compatibility_rule(
        state,
        {"rule_id": "compat_order", "tenant": "tenant_ops", "subject_id": "subject_order", "mode": "backward_forward", "status": "active"},
    )
    state = compatibility_rule["state"]
    assert compatibility_rule["rule"]["transitive"] is True

    binding = schema_registry_register_consumer_binding(
        state,
        {"binding_id": "consumer_dom", "tenant": "tenant_ops", "subject_id": "subject_order", "consumer_pbc": "dom", "consumer_type": "handler", "min_version": 1},
    )
    state = binding["state"]
    assert binding["binding"]["status"] == "active"

    first_version = schema_registry_submit_schema_version(
        state,
        {
            "version_id": "order_v1",
            "tenant": "tenant_ops",
            "subject_id": "subject_order",
            "semantic_version": "1.0.0",
            "schema": {"fields": {"order_id": {"type": "string", "required": True}, "total": {"type": "number", "required": True}}},
        },
    )
    state = first_version["state"]
    assert first_version["decision"] == "accepted"

    compatible = schema_registry_run_compatibility_check(
        state,
        "subject_order",
        {"fields": {"order_id": {"type": "string", "required": True}, "total": {"type": "number", "required": True}, "currency": {"type": "string", "required": False}}},
    )
    state = compatible["state"]
    assert compatible["decision"] == "accepted"

    second_version = schema_registry_submit_schema_version(
        state,
        {
            "version_id": "order_v2",
            "tenant": "tenant_ops",
            "subject_id": "subject_order",
            "semantic_version": "1.1.0",
            "schema": compatible["proposed_schema"],
        },
    )
    state = second_version["state"]
    assert second_version["decision"] == "accepted"

    breaking = schema_registry_run_compatibility_check(state, "subject_order", {"fields": {"order_id": {"type": "number", "required": True}}})
    state = breaking["state"]
    assert breaking["decision"] == "blocked"
    assert breaking["risk_score"] > 0

    validation = schema_registry_validate_payload(state, "subject_order", {"order_id": "ORD-1", "total": 99.5, "currency": "USD"})
    state = validation["state"]
    assert validation["ok"] is True

    violation = schema_registry_record_contract_violation(
        state,
        {
            "violation_id": "viol_order",
            "tenant": "tenant_ops",
            "subject_id": "subject_order",
            "producer_pbc": "checkout_processing",
            "consumer_pbc": "dom",
            "severity": "high",
            "reason": "type_change",
            "status": "open",
        },
    )
    state = violation["state"]
    assert violation["violation"]["release_blocking"] is True

    projection = schema_registry_publish_contract_projection(state, "subject_order", systems=("gateway", "audit", "composition", "workflow"))
    state = projection["state"]
    assert projection["handoffs"] == (
        "gateway_contract_projection",
        "audit_contract_projection",
        "composition_contract_projection",
        "workflow_contract_projection",
    )
    assert state["outbox"][-1]["idempotency_key"] == "schema_registry:ContractProjectionPublished:schema_evt_000008"

    workbench = schema_registry_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["subject_count"] == 1
    assert workbench["version_count"] == 2
    assert workbench["validation_count"] == 3
    assert workbench["violation_count"] == 1
    assert workbench["consumer_binding_count"] == 1
    assert workbench["release_blocking_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 4
    assert workbench["inbox_count"] == 1
    assert workbench["binding_evidence"]["owned_tables"] == SCHEMA_REGISTRY_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"

    ui_contract = schema_registry_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == SCHEMA_REGISTRY_OWNED_TABLES
    assert "compatibility_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = schema_registry_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "schema_registry.register",
            "schema_registry.approve",
            "schema_registry.validate",
            "schema_registry.triage",
            "schema_registry.publish",
            "schema_registry.event",
            "schema_registry.configure",
            "schema_registry.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 8
    assert rendered["inbox_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == SCHEMA_REGISTRY_OWNED_TABLES

    boundary = schema_registry_verify_owned_table_boundary(
        ("schema_version", "PbcDeployed", "gateway_contract_projection", "POST /audit/contract-events", "schema_registry_appgen_outbox_event")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation_boundary = schema_registry_verify_owned_table_boundary(("api_gateway_mesh",))
    assert violation_boundary["ok"] is False
    assert violation_boundary["violations"] == ("api_gateway_mesh",)


def test_schema_registry_rejects_unsupported_database_backends_eventing_and_boundaries() -> None:
    state = schema_registry_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        schema_registry_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        schema_registry_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Schema Registry parameter"):
        schema_registry_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        schema_registry_register_schema_extension(state, "api_gateway_mesh", {"schema_ref": "jsonb"})

    configured = schema_registry_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "allowed_formats": ("json", "event"),
            "default_compatibility": "backward_forward",
            "namespace_policy": "tenant_scoped",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    retrying = schema_registry_receive_event(
        configured,
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    dead_letter = schema_registry_receive_event(
        retrying["state"],
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1
