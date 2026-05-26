import pytest

from pyAppGen.pbc import CUSTOMER_360_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import customer_360_build_timeline
from pyAppGen.pbc import customer_360_build_workbench_view
from pyAppGen.pbc import customer_360_capture_touchpoint
from pyAppGen.pbc import customer_360_configure_runtime
from pyAppGen.pbc import customer_360_create_profile
from pyAppGen.pbc import customer_360_empty_state
from pyAppGen.pbc import customer_360_ingest_engagement_event
from pyAppGen.pbc import customer_360_link_identity
from pyAppGen.pbc import customer_360_open_merge_case
from pyAppGen.pbc import customer_360_record_consent
from pyAppGen.pbc import customer_360_register_rule
from pyAppGen.pbc import customer_360_render_workbench
from pyAppGen.pbc import customer_360_resolve_merge_case
from pyAppGen.pbc import customer_360_runtime_capabilities
from pyAppGen.pbc import customer_360_runtime_smoke
from pyAppGen.pbc import customer_360_set_parameter
from pyAppGen.pbc import customer_360_set_preference
from pyAppGen.pbc import customer_360_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_customer_360_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = customer_360_runtime_capabilities()
    smoke = customer_360_runtime_smoke()

    assert runtime["format"] == "appgen.customer-360-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/customer_360"
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(CUSTOMER_360_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("customer_360")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "CustomerConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(CUSTOMER_360_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("customer_360",))["ok"] is True
    assert pbc_implemented_capability_audit(("customer_360",))["ok"] is True


def test_customer_360_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = customer_360_empty_state()
    state = customer_360_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.customer.events",
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
    state = customer_360_register_rule(
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
    )["state"]

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

    timeline = customer_360_build_timeline(state, "cust_ops")
    assert timeline["event_count"] == 2

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

    ui_contract = customer_360_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "identity_match_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = customer_360_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "customer_360.profile",
            "customer_360.merge",
            "customer_360.consent",
            "customer_360.engage",
            "customer_360.configure",
            "customer_360.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 8
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_customer_360_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = customer_360_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        customer_360_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.customer.events",
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Customer 360 parameter"):
        customer_360_set_parameter(state, "stream_engine", "hidden_picker")
