import pytest

from pyAppGen.pbcs.customer_360 import CUSTOMER_360_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.customer_360 import CUSTOMER_360_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.customer_360 import CUSTOMER_360_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.customer_360 import CUSTOMER_360_OWNED_TABLES
from pyAppGen.pbcs.customer_360 import CUSTOMER_360_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.customer_360 import CUSTOMER_360_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.customer_360 import CUSTOMER_360_STANDARD_FEATURE_KEYS
from pyAppGen.pbcs.customer_360 import customer_360_build_api_contract
from pyAppGen.pbcs.customer_360 import customer_360_build_release_evidence
from pyAppGen.pbcs.customer_360 import customer_360_build_schema_contract
from pyAppGen.pbcs.customer_360 import customer_360_build_service_contract
from pyAppGen.pbcs.customer_360 import customer_360_build_timeline
from pyAppGen.pbcs.customer_360 import customer_360_build_workbench_view
from pyAppGen.pbcs.customer_360 import customer_360_capture_touchpoint
from pyAppGen.pbcs.customer_360 import customer_360_configure_runtime
from pyAppGen.pbcs.customer_360 import customer_360_create_profile
from pyAppGen.pbcs.customer_360 import customer_360_empty_state
from pyAppGen.pbcs.customer_360 import customer_360_ingest_engagement_event
from pyAppGen.pbcs.customer_360 import customer_360_link_identity
from pyAppGen.pbcs.customer_360 import customer_360_open_merge_case
from pyAppGen.pbcs.customer_360 import customer_360_permissions_contract
from pyAppGen.pbcs.customer_360 import customer_360_receive_event
from pyAppGen.pbcs.customer_360 import customer_360_record_consent
from pyAppGen.pbcs.customer_360 import customer_360_register_rule
from pyAppGen.pbcs.customer_360 import customer_360_register_schema_extension
from pyAppGen.pbcs.customer_360 import customer_360_render_workbench
from pyAppGen.pbcs.customer_360 import customer_360_resolve_merge_case
from pyAppGen.pbcs.customer_360 import customer_360_runtime_capabilities
from pyAppGen.pbcs.customer_360 import customer_360_runtime_smoke
from pyAppGen.pbcs.customer_360 import customer_360_set_parameter
from pyAppGen.pbcs.customer_360 import customer_360_set_preference
from pyAppGen.pbcs.customer_360 import customer_360_ui_contract
from pyAppGen.pbcs.customer_360 import customer_360_verify_owned_table_boundary
from pyAppGen.pbcs.customer_360 import implementation_contract


def test_customer_360_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = customer_360_runtime_capabilities()
    smoke = customer_360_runtime_smoke()

    assert runtime["format"] == "appgen.customer-360-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/customer_360"
    assert len(runtime["standard_features"]) >= 55
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "appgen_event_contract" in runtime["standard_features"]
    assert "owned_datastore_boundary" in runtime["standard_features"]
    assert "cryptographic_profile_proofs" in runtime["standard_features"]
    assert "governed_model_registry" in runtime["standard_features"]
    assert set(runtime["standard_features"]) == set(CUSTOMER_360_STANDARD_FEATURE_KEYS)
    assert smoke["ok"] is True
    assert set(CUSTOMER_360_RUNTIME_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = implementation_contract()
    assert contract["pbc"] == "customer_360"
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert "CustomerConfigurationPanel" in contract["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(CUSTOMER_360_RUNTIME_CAPABILITY_KEYS)
    assert contract["owned_tables"] == CUSTOMER_360_OWNED_TABLES
    assert contract["allowed_database_backends"] == CUSTOMER_360_ALLOWED_DATABASE_BACKENDS
    assert contract["required_event_topic"] == CUSTOMER_360_REQUIRED_EVENT_TOPIC
    assert contract["api_contract"]["shared_table_access"] is False
    assert contract["schema_contract"]["ok"] is True
    assert contract["schema_contract"]["shared_table_access"] is False
    assert len(contract["schema_contract"]["owned_tables"]) >= 45
    assert contract["service_contract"]["ok"] is True
    assert contract["service_contract"]["shared_table_access"] is False
    assert "build_release_evidence" in contract["service_contract"]["command_methods"]
    assert contract["release_evidence_contract"]["ok"] is True
    assert not contract["release_evidence_contract"]["blocking_gaps"]
    assert contract["permissions_contract"]["action_permissions"]["receive_event"] == "customer_360.event"
    assert contract["boundary_contract"]["ok"] is True


def test_customer_360_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = customer_360_empty_state()
    state = customer_360_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_channels": ("email", "sms", "web", "service"),
            "allowed_regions": ("US",),
            "allowed_identity_types": ("email", "phone", "external_id"),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = customer_360_set_parameter(state, "identity_match_threshold", 0.82)["state"]
    state = customer_360_set_parameter(state, "churn_risk_threshold", 0.65)["state"]
    state = customer_360_set_parameter(state, "engagement_decay_days", 90)["state"]
    state = customer_360_set_parameter(state, "minimum_consent_confidence", 0.9)["state"]
    state = customer_360_set_parameter(state, "timeline_limit", 50)["state"]
    rule = customer_360_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "privacy",
            "allowed_channels": ("email", "web", "service"),
            "required_consents": ("marketing",),
            "restricted_regions": ("restricted",),
            "identity_match_fields": ("email", "phone"),
            "segment_rules": ("high_value", "at_risk"),
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
        "allowed_channels",
        "required_consents",
        "status",
    )

    profile = customer_360_create_profile(
        state,
        {"profile_id": "cust_ops", "tenant": "tenant_ops", "display_name": "Ada Lovelace", "region": "US", "lifecycle_state": "active", "account_type": "consumer"},
    )
    state = profile["state"]
    assert profile["profile"]["status"] == "active"

    identity = customer_360_link_identity(
        state,
        {"identity_id": "id_ops", "tenant": "tenant_ops", "profile_id": "cust_ops", "identity_type": "email", "value": "ada@example.com", "confidence": 0.96, "verified": True},
    )
    state = identity["state"]
    assert identity["identity"]["status"] == "linked"

    consent = customer_360_record_consent(
        state,
        {"consent_id": "consent_ops", "tenant": "tenant_ops", "profile_id": "cust_ops", "purpose": "marketing", "region": "US", "status": "granted", "confidence": 0.95},
    )
    state = consent["state"]
    assert consent["consent"]["effective"] is True

    preference = customer_360_set_preference(
        state,
        {"preference_id": "pref_ops", "tenant": "tenant_ops", "profile_id": "cust_ops", "channel": "email", "status": "opt_in", "topic": "offers"},
    )
    state = preference["state"]
    assert preference["preference"]["effective"] is True

    touchpoint = customer_360_capture_touchpoint(
        state,
        {"touchpoint_id": "tp_ops", "tenant": "tenant_ops", "profile_id": "cust_ops", "channel": "web", "source": "storefront", "occurred_at": "2026-05-26T08:00:00Z"},
    )
    state = touchpoint["state"]
    assert touchpoint["touchpoint"]["status"] == "captured"

    engagement = customer_360_ingest_engagement_event(
        state,
        {"event_id": "eng_ops", "tenant": "tenant_ops", "profile_id": "cust_ops", "event_type": "purchase", "channel": "web", "value": 240, "sentiment": 0.8},
    )
    state = engagement["state"]
    assert engagement["handoffs"] == (
        "commerce_customer_projection",
        "billing_account_projection",
        "service_timeline_projection",
        "loyalty_profile_projection",
    )

    merge = customer_360_open_merge_case(
        state,
        {"merge_case_id": "merge_ops", "tenant": "tenant_ops", "winning_profile_id": "cust_ops", "candidate_profile_id": "cust_dup", "match_score": 0.88, "reason": "same_email"},
    )
    state = merge["state"]
    assert merge["merge_case"]["status"] == "open"

    resolved = customer_360_resolve_merge_case(state, "merge_ops", resolved_by="data_steward")
    state = resolved["state"]
    assert resolved["merge_case"]["status"] == "resolved"
    assert state["outbox"][-1]["idempotency_key"] == "customer_360:ProfileMergeResolved:customer_evt_000008"

    workbench = customer_360_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["profile_count"] == 1
    assert workbench["identity_count"] == 1
    assert workbench["effective_consent_count"] == 1
    assert workbench["opt_in_count"] == 1
    assert workbench["touchpoint_count"] == 1
    assert workbench["engagement_event_count"] == 1
    assert workbench["customer_value"] == 240
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5
    assert workbench["binding_evidence"]["owned_tables"] == CUSTOMER_360_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"] == {
        "bound": True,
        "database_backend": "postgresql",
        "event_contract": "AppGen-X",
        "event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
        "visible_event_contracts": ("AppGen-X",),
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "supported_fields": (
            "database_backend",
            "event_topic",
            "retry_limit",
            "allowed_channels",
            "allowed_regions",
            "allowed_identity_types",
            "default_timezone",
            "workbench_limit",
        ),
    }
    assert workbench["binding_evidence"]["rules"] == (
        {
            "rule_id": "rule_ops",
            "scope": "privacy",
            "compiled_hash": rule["rule"]["compiled_hash"],
            "required_fields": rule["rule"]["compiled_evidence"]["required_fields"],
        },
    )
    assert workbench["binding_evidence"]["parameters"] == {
        "supported": (
            "identity_match_threshold",
            "churn_risk_threshold",
            "engagement_decay_days",
            "minimum_consent_confidence",
            "timeline_limit",
            "retention_days",
            "workbench_limit",
        ),
        "active": (
            "churn_risk_threshold",
            "engagement_decay_days",
            "identity_match_threshold",
            "minimum_consent_confidence",
            "timeline_limit",
        ),
    }

    timeline = customer_360_build_timeline(state, "cust_ops")
    assert timeline["event_count"] == 2

    ui_contract = customer_360_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == CUSTOMER_360_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == CUSTOMER_360_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["visible_event_contracts"] == ("AppGen-X",)
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["user_selectable_event_contract"] is False
    assert ui_contract["event_surfaces"]["emits"] == CUSTOMER_360_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == CUSTOMER_360_CONSUMED_EVENT_TYPES
    assert ui_contract["binding_evidence"]["owned_tables"] == CUSTOMER_360_OWNED_TABLES
    assert ui_contract["binding_evidence"]["shared_table_access"] is False
    assert "identity_match_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["rule_editor"]["compiled_evidence_fields"] == ("compiled_hash", "compiled_evidence")
    assert "CustomerReleaseEvidencePanel" in ui_contract["fragments"]
    assert any(panel["key"] == "release_evidence" for panel in ui_contract["panels"])
    rendered = customer_360_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=tuple(sorted(set(customer_360_permissions_contract()["action_permissions"].values()))),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 8
    assert rendered["inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["rules_bound"] == ("rule_ops",)
    assert rendered["parameters_bound"] == (
        "churn_risk_threshold",
        "engagement_decay_days",
        "identity_match_threshold",
        "minimum_consent_confidence",
        "timeline_limit",
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


def test_customer_360_rejects_unsupported_backends_unknown_parameters_and_stream_picker_config() -> None:
    state = customer_360_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        customer_360_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "allowed_channels": ("email",),
                "allowed_regions": ("US",),
                "allowed_identity_types": ("email",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        customer_360_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "allowed_channels": ("email",),
                "allowed_regions": ("US",),
                "allowed_identity_types": ("email",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Customer 360 parameter"):
        customer_360_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="requires AppGen-X event topic"):
        customer_360_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.customer.topic",
                "retry_limit": 3,
                "allowed_channels": ("email",),
                "allowed_regions": ("US",),
                "allowed_identity_types": ("email",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )


def test_customer_360_package_contract_handles_events_schema_api_permissions_and_boundaries() -> None:
    state = customer_360_empty_state()
    state = customer_360_configure_runtime(
        state,
        {
            "database_backend": "mariadb",
            "event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "allowed_channels": ("email", "web"),
            "allowed_regions": ("US",),
            "allowed_identity_types": ("email", "phone"),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]

    extension = customer_360_register_schema_extension(
        state,
        "customer_profile",
        {"loyalty_payload": "jsonb"},
    )
    state = extension["state"]
    assert extension["schema_extension"] == {
        "table": "customer_profile",
        "fields": {"loyalty_payload": "jsonb"},
    }
    assert state["schema_extensions"]["customer_profile"]["loyalty_payload"] == "jsonb"

    with pytest.raises(ValueError, match="owned tables"):
        customer_360_register_schema_extension(state, "invoice_line", {"foreign_payload": "jsonb"})

    bad_field = customer_360_register_schema_extension(state, "communication_preference", {"BadName": "text"})
    assert bad_field["ok"] is False
    assert bad_field["error"] == "invalid_extension_field"

    received = customer_360_receive_event(
        state,
        {
            "event_id": "invoice_evt_ops",
            "event_type": "InvoiceIssued",
            "payload": {
                "tenant": "tenant_ops",
                "invoice_id": "inv_ops",
                "profile_id": "cust_ops",
                "amount": 240,
            },
        },
    )
    state = received["state"]
    assert received["ok"] is True
    assert state["projections"]["invoice_issues"]["inv_ops"]["amount"] == 240

    duplicate = customer_360_receive_event(
        state,
        {
            "event_id": "invoice_evt_ops",
            "event_type": "InvoiceIssued",
            "payload": {
                "tenant": "tenant_ops",
                "invoice_id": "inv_ops",
                "profile_id": "cust_ops",
                "amount": 240,
            },
        },
    )
    assert duplicate["duplicate"] is True
    assert duplicate["state"] is state

    failed_once = customer_360_receive_event(
        state,
        {
            "event_id": "unknown_evt_ops",
            "event_type": "UnknownCustomerEvent",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    assert failed_once["ok"] is False
    assert failed_once["handler"]["status"] == "retrying"
    failed_twice = customer_360_receive_event(
        failed_once["state"],
        {
            "event_id": "unknown_evt_ops",
            "event_type": "UnknownCustomerEvent",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    assert failed_twice["handler"]["status"] == "dead_letter"
    assert failed_twice["state"]["dead_letter"][-1]["reason"] == "unsupported_or_failed_customer_360_event"

    api = customer_360_build_api_contract()
    assert api["format"] == "appgen.customer-360-api-contract.v1"
    assert api["event_contract"] == "AppGen-X"
    assert api["required_event_topic"] == CUSTOMER_360_REQUIRED_EVENT_TOPIC
    assert api["database_backends"] == CUSTOMER_360_ALLOWED_DATABASE_BACKENDS
    assert api["owned_tables"] == CUSTOMER_360_OWNED_TABLES
    assert api["events"] == {
        "emits": CUSTOMER_360_EMITTED_EVENT_TYPES,
        "consumes": CUSTOMER_360_CONSUMED_EVENT_TYPES,
    }
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert any(route["command"] == "receive_event" for route in api["routes"])
    assert any(route.get("query") == "build_release_evidence" for route in api["routes"])

    schema = customer_360_build_schema_contract()
    assert schema["format"] == "appgen.customer-360-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert schema["shared_table_access"] is False
    assert "customer_proof" in schema["owned_tables"]
    assert "customer_360_dead_letter_event" in schema["owned_tables"]
    assert len(schema["tables"]) == len(CUSTOMER_360_OWNED_TABLES)
    assert len(schema["migrations"]) == len(CUSTOMER_360_OWNED_TABLES)
    assert all(path.startswith("pbcs/customer_360/migrations/") for path in schema["migrations"])

    service = customer_360_build_service_contract()
    assert service["format"] == "appgen.customer-360-service-contract.v1"
    assert service["ok"] is True
    assert service["mutates_only_owned_tables"] is True
    assert service["shared_table_access"] is False
    assert service["event_contract"]["contract"] == "AppGen-X"
    assert service["event_contract"]["required_topic"] == CUSTOMER_360_REQUIRED_EVENT_TOPIC
    assert "register_governed_model" in service["command_methods"]
    assert "build_schema_contract" in service["query_methods"]

    release = customer_360_build_release_evidence()
    assert release["format"] == "appgen.customer-360-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert all(check["ok"] for check in release["checks"])

    permissions = customer_360_permissions_contract()
    assert permissions["action_permissions"]["receive_event"] == "customer_360.event"
    assert permissions["action_permissions"]["register_schema_extension"] == "customer_360.configure"
    assert permissions["action_permissions"]["verify_owned_table_boundary"] == "customer_360.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "customer_360.audit"

    valid_boundary = customer_360_verify_owned_table_boundary(
        (
            "customer_profile",
            "customer_360_appgen_inbox_event",
            "InvoiceIssued",
            "commerce_customer_projection",
            "GET /orders/customer-history",
        )
    )
    assert valid_boundary["ok"] is True
    assert valid_boundary["declared_dependencies"]["shared_tables"] == ()

    invalid_boundary = customer_360_verify_owned_table_boundary(("invoice_line", "service_ticket"))
    assert invalid_boundary["ok"] is False
    assert invalid_boundary["violations"] == ("invoice_line", "service_ticket")
