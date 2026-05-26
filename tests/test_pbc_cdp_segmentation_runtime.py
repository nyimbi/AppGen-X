import pytest

from pyAppGen.pbc import cdp_segmentation_activate_segment
from pyAppGen.pbc import cdp_segmentation_build_api_contract
from pyAppGen.pbc import cdp_segmentation_build_workbench_view
from pyAppGen.pbc import cdp_segmentation_configure_runtime
from pyAppGen.pbc import cdp_segmentation_define_segment
from pyAppGen.pbc import cdp_segmentation_empty_state
from pyAppGen.pbc import cdp_segmentation_evaluate_segments
from pyAppGen.pbc import cdp_segmentation_ingest_customer_event
from pyAppGen.pbc import cdp_segmentation_permissions_contract
from pyAppGen.pbc import cdp_segmentation_receive_event
from pyAppGen.pbc import cdp_segmentation_register_rule
from pyAppGen.pbc import cdp_segmentation_register_schema_extension
from pyAppGen.pbc import cdp_segmentation_render_workbench
from pyAppGen.pbc import cdp_segmentation_runtime_capabilities
from pyAppGen.pbc import cdp_segmentation_runtime_smoke
from pyAppGen.pbc import cdp_segmentation_set_parameter
from pyAppGen.pbc import cdp_segmentation_ui_contract
from pyAppGen.pbc import cdp_segmentation_verify_owned_table_boundary
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.cdp_segmentation import CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.cdp_segmentation import CDP_SEGMENTATION_OWNED_TABLES
from pyAppGen.pbcs.cdp_segmentation import CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.cdp_segmentation import cdp_segmentation_build_release_evidence
from pyAppGen.pbcs.cdp_segmentation import cdp_segmentation_build_schema_contract
from pyAppGen.pbcs.cdp_segmentation import cdp_segmentation_build_service_contract


def test_cdp_segmentation_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = cdp_segmentation_runtime_capabilities()
    smoke = cdp_segmentation_runtime_smoke()

    assert runtime["format"] == "appgen.cdp-segmentation-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/cdp_segmentation"
    assert runtime["owned_tables"] == CDP_SEGMENTATION_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 45
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("cdp_segmentation")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["api_contract"]["ok"] is True
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert len(contract["source_package"]["schema_contract"]["owned_tables"]) >= 45
    assert (
        contract["source_package"]["permissions_contract"]["action_permissions"]["evaluate_segments"]
        == "cdp_segmentation.membership.evaluate"
    )
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "CdpConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert pbc_implementation_release_audit(("cdp_segmentation",))["ok"] is True


def test_cdp_segmentation_runtime_applies_rules_parameters_configuration_events_and_ui() -> None:
    state = _configured_state()
    extension = cdp_segmentation_register_schema_extension(
        state, "profile_property", {"identity_confidence": "numeric"}
    )
    state = extension["state"]
    assert extension["extension"]["version"] == 1
    state = cdp_segmentation_receive_event(
        state,
        {"event_id": "customer_ops", "event_type": "CustomerUpdated", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "email": "buyer@example.com", "region": "US", "opt_in": True}},
    )["state"]
    state = cdp_segmentation_receive_event(
        state,
        {"event_id": "payment_ops", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "amount": 1200.0, "currency": "USD"}},
    )["state"]
    state = cdp_segmentation_ingest_customer_event(
        state,
        {"event_id": "engage_ops", "tenant": "tenant_ops", "customer_id": "cust_ops", "event_type": "engagement", "region": "US", "properties": {"clicks": 5}},
    )["state"]
    state = cdp_segmentation_define_segment(
        state,
        {"segment_id": "seg_ops", "tenant": "tenant_ops", "name": "Ops High Value", "criteria": {"min_payment_value": 1000, "requires_shipment": False, "min_engagement": 0.2}, "status": "active"},
    )["state"]
    evaluated = cdp_segmentation_evaluate_segments(state, "cust_ops")
    state = evaluated["state"]
    assert evaluated["memberships"][0]["status"] == "member"
    state = cdp_segmentation_activate_segment(state, "seg_ops")["state"]
    assert state["outbox"][-1]["idempotency_key"].startswith("cdp_segmentation:ProfileEnriched")

    workbench = cdp_segmentation_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["event_count"] == 3
    assert workbench["profile_count"] == 1
    assert workbench["segment_count"] == 1
    assert workbench["active_membership_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = cdp_segmentation_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = cdp_segmentation_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "cdp_segmentation.event.write",
            "cdp_segmentation.segment.write",
            "cdp_segmentation.membership.evaluate",
            "cdp_segmentation.event.consume",
            "cdp_segmentation.configure",
            "cdp_segmentation.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == CDP_SEGMENTATION_OWNED_TABLES

    api_contract = cdp_segmentation_build_api_contract()
    assert api_contract["database_backends"] == CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
    assert api_contract["event_contract"] == "AppGen-X"
    assert api_contract["stream_engine_picker_visible"] is False
    assert api_contract["shared_table_access"] is False
    assert any(route.get("query") == "build_release_evidence" for route in api_contract["routes"])
    assert {route["command"] for route in api_contract["routes"] if "command" in route} >= {
        "ingest_customer_event",
        "upsert_profile_property",
        "define_segment",
        "evaluate_segments",
        "activate_segment",
        "receive_event",
    }
    permissions = cdp_segmentation_permissions_contract()
    assert permissions["action_permissions"]["verify_owned_table_boundary"] == "cdp_segmentation.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "cdp_segmentation.audit"

    schema = cdp_segmentation_build_schema_contract()
    service = cdp_segmentation_build_service_contract()
    release = cdp_segmentation_build_release_evidence()
    assert schema["format"] == "appgen.cdp-segmentation-owned-schema-contract.v1"
    assert schema["shared_table_access"] is False
    assert "profile_consent" in schema["owned_tables"]
    assert "cdp_segmentation_dead_letter_event" in schema["owned_tables"]
    assert len(schema["migrations"]) == len(CDP_SEGMENTATION_OWNED_TABLES)
    assert all(path.startswith("pbcs/cdp_segmentation/migrations/") for path in schema["migrations"])
    assert service["eventing"]["contract"] == "AppGen-X"
    assert service["shared_table_access"] is False
    assert "build_schema_contract" in service["query_methods"]
    assert "register_governed_model" in service["command_methods"]
    assert release["ok"] is True
    assert not release["blocking_gaps"]


def test_cdp_segmentation_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = cdp_segmentation_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        cdp_segmentation_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.cdp_segmentation.events",
                "retry_limit": 3,
                "default_region": "US",
                "supported_regions": ("US",),
                "supported_event_types": ("profile",),
                "identity_keys": ("customer_id",),
                "default_timezone": "UTC",
                "activation_mode": "policy",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported CDP Segmentation parameter"):
        cdp_segmentation_set_parameter(state, "stream_engine", 1)

    failed = cdp_segmentation_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "CustomerUpdated", "payload": {"tenant": "tenant_ops", "customer_id": "cust_fail"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = cdp_segmentation_verify_owned_table_boundary(
        (
            "customer_event",
            "segment_definition",
            "segment_membership",
            "profile_property",
            "CustomerUpdated",
            "payment_projection",
            "cdp_segmentation_appgen_outbox_event",
        )
    )
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == CDP_SEGMENTATION_OWNED_TABLES
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    assert "payment_projection" in boundary["declared_dependencies"]["api_projections"]
    violated = cdp_segmentation_verify_owned_table_boundary(("customer",))
    assert violated["ok"] is False
    assert violated["violations"] == ("customer",)
    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        cdp_segmentation_register_schema_extension(state, "customer", {"email": "text"})


def _configured_state() -> dict:
    state = cdp_segmentation_empty_state()
    state = cdp_segmentation_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.cdp_segmentation.events",
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US",),
            "supported_event_types": ("profile", "payment", "shipment", "engagement"),
            "identity_keys": ("customer_id", "email"),
            "default_timezone": "UTC",
            "activation_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("membership_score_threshold", 0.6),
        ("profile_merge_confidence_threshold", 0.85),
        ("event_freshness_days", 180),
        ("payment_value_weight", 0.35),
        ("order_recency_weight", 0.25),
        ("engagement_weight", 0.4),
        ("consent_risk_threshold", 0.6),
        ("activation_batch_limit", 5000),
        ("max_segments_per_profile", 20),
        ("workbench_limit", 50),
    ):
        state = cdp_segmentation_set_parameter(state, name, value)["state"]
    state = cdp_segmentation_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "cdp_segmentation",
            "status": "active",
            "allowed_event_types": ("profile", "payment", "shipment", "engagement"),
            "allowed_regions": ("US",),
            "segment_policy": {"minimum_score": 0.6, "required_properties": ("customer_id",)},
            "consent_policy": {"require_opt_in": True, "restricted_regions": ()},
            "activation_policy": {"destinations": ("pricing", "loyalty")},
        },
    )["state"]
    return state
