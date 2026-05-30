"""Executable domain behavior checks for the Customer 360 PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import runtime
from .. import ui
from ..services import Customer360StandaloneService
from ..services import standalone_service_operation_contracts


TENANT = "tenant_customer"
PROFILE_ID = "cust_360_001"


def _configuration(retry_limit: int = 3) -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.CUSTOMER_360_REQUIRED_EVENT_TOPIC,
        "retry_limit": retry_limit,
        "allowed_channels": ("email", "sms", "web", "appgen_inbox"),
        "allowed_regions": ("US", "EU"),
        "allowed_identity_types": ("email", "phone", "did"),
        "default_timezone": "UTC",
        "workbench_limit": 100,
    }


def _rule() -> dict:
    return {
        "rule_id": "customer.privacy.default",
        "tenant": TENANT,
        "rule_type": "privacy",
        "allowed_channels": ("email", "sms", "web"),
        "required_consents": ("marketing",),
        "restricted_regions": ("restricted",),
        "identity_match_fields": ("email", "phone"),
        "segment_rules": ("high_value", "at_risk"),
        "status": "active",
    }


def _runtime_state() -> dict:
    state = runtime.customer_360_empty_state()
    state = runtime.customer_360_configure_runtime(state, _configuration())["state"]
    for name, value in {
        "identity_match_threshold": 0.8,
        "churn_risk_threshold": 0.75,
        "engagement_decay_days": 30,
        "minimum_consent_confidence": 0.9,
        "timeline_limit": 100,
        "retention_days": 365,
        "workbench_limit": 100,
    }.items():
        state = runtime.customer_360_set_parameter(state, name, value)["state"]
    state = runtime.customer_360_register_rule(state, _rule())["state"]
    state = runtime.customer_360_register_schema_extension(state, "customer_profile", {"loyalty_payload": "jsonb"})["state"]
    return state


def _runtime_customer_state() -> dict:
    state = _runtime_state()
    state = runtime.customer_360_create_profile(
        state,
        {
            "profile_id": PROFILE_ID,
            "tenant": TENANT,
            "display_name": "Ada Customer",
            "region": "US",
            "lifecycle_state": "active",
            "account_type": "consumer",
        },
    )["state"]
    state = runtime.customer_360_link_identity(
        state,
        {
            "identity_id": "identity_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "identity_type": "email",
            "identity_value_hash": "hash_ada",
            "confidence": 0.98,
            "verified": True,
        },
    )["state"]
    state = runtime.customer_360_record_consent(
        state,
        {
            "consent_id": "consent_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "purpose": "marketing",
            "region": "US",
            "status": "granted",
            "confidence": 0.96,
        },
    )["state"]
    state = runtime.customer_360_set_preference(
        state,
        {
            "preference_id": "pref_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "channel": "email",
            "topic": "offers",
            "status": "opt_in",
        },
    )["state"]
    state = runtime.customer_360_capture_touchpoint(
        state,
        {
            "touchpoint_id": "touch_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "channel": "web",
            "source": "portal",
        },
    )["state"]
    state = runtime.customer_360_ingest_engagement_event(
        state,
        {
            "event_id": "engage_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "event_type": "purchase",
            "channel": "web",
            "value": 420.0,
            "sentiment": 0.8,
        },
    )["state"]
    opened = runtime.customer_360_open_merge_case(
        state,
        {
            "merge_case_id": "merge_001",
            "tenant": TENANT,
            "winning_profile_id": PROFILE_ID,
            "candidate_profile_id": "cust_duplicate",
            "match_score": 0.91,
            "reason": "same_email",
        },
    )
    state = runtime.customer_360_resolve_merge_case(opened["state"], "merge_001", resolved_by="data_steward")["state"]
    return state


def _service_with_customer() -> Customer360StandaloneService:
    service = Customer360StandaloneService()
    assert service.create_profile(
        {
            "profile_id": PROFILE_ID,
            "tenant": TENANT,
            "display_name": "Ada Customer",
            "region": "US",
        }
    )["ok"] is True
    assert service.link_identity(
        {
            "identity_id": "identity_service_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "identity_type": "email",
            "value": "ada@example.com",
            "confidence": 0.99,
            "verified": True,
        }
    )["ok"] is True
    assert service.record_consent(
        {
            "consent_id": "consent_service_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "purpose": "marketing",
            "region": "US",
            "status": "granted",
            "confidence": 0.95,
        }
    )["ok"] is True
    assert service.set_preference(
        {
            "preference_id": "pref_service_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "channel": "email",
            "topic": "offers",
            "status": "opt_in",
        }
    )["ok"] is True
    assert service.capture_touchpoint(
        {
            "touchpoint_id": "touch_service_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "channel": "web",
            "source": "portal",
        }
    )["ok"] is True
    assert service.ingest_engagement_event(
        {
            "event_id": "engage_service_001",
            "tenant": TENANT,
            "profile_id": PROFILE_ID,
            "event_type": "purchase",
            "channel": "web",
            "value": 350.0,
        }
    )["ok"] is True
    return service


def test_customer_360_one_pbc_customer_lifecycle_is_executable():
    service = _service_with_customer()
    try:
        merge = service.open_merge_case(
            {
                "merge_case_id": "merge_service_001",
                "tenant": TENANT,
                "winning_profile_id": PROFILE_ID,
                "candidate_profile_id": "cust_duplicate",
                "match_score": 0.92,
                "reason": "same_identity",
            }
        )
        resolved = service.resolve_merge_case({"merge_case_id": "merge_service_001", "resolved_by": "data_steward"})
        timeline = service.build_timeline({"profile_id": PROFILE_ID})
        workbench = service.build_workbench({"tenant": TENANT})
        rendered = ui.customer_360_render_standalone_workbench(workbench["result"])

        assert merge["ok"] is True
        assert resolved["ok"] is True
        assert timeline["ok"] is True
        assert timeline["result"]["event_count"] >= 4
        assert workbench["ok"] is True
        assert workbench["result"]["profile_count"] == 1
        assert workbench["result"]["effective_consent_count"] == 1
        assert workbench["result"]["open_merge_case_count"] == 0
        assert rendered["ok"] is True
        assert {form["operation"] for form in rendered["forms"]} >= {"create_profile", "record_consent", "capture_touchpoint"}
        assert {wizard["key"] for wizard in rendered["wizards"]} >= {"CustomerProfileOnboardingWizard", "MergeCaseResolutionWizard"}
    finally:
        service.close()


def test_customer_360_service_ui_agent_and_route_surface_are_first_class():
    service = _service_with_customer()
    try:
        contract = standalone_service_operation_contracts()
        document = agent.document_instruction_plan(
            "Customer onboarding packet for customer cust_360_001 with email consent and web touchpoint.",
            "onboard the profile, record consent, and build the timeline",
        )
        crud = agent.datastore_crud_plan(
            "create",
            "customer_360_customer_profile",
            {"profile_id": PROFILE_ID, "tenant": TENANT},
        )
        profile = service.get_profile({"profile_id": PROFILE_ID})
        listed = service.list_profiles({"tenant": TENANT})

        assert contract["ok"] is True
        assert set(contract["operations"]) >= {
            "create_profile",
            "link_identity",
            "record_consent",
            "capture_touchpoint",
            "receive_event",
            "build_workbench",
        }
        assert document["ok"] is True
        assert "CustomerProfileOnboardingWizard" in document["wizard_candidates"]
        assert crud["ok"] is True
        assert crud["route_candidates"]
        assert profile["result"]["profile"]["profile_id"] == PROFILE_ID
        assert len(listed["result"]["profiles"]) == 1
    finally:
        service.close()


def test_customer_360_events_are_idempotent_retryable_and_boundary_scoped():
    service = _service_with_customer()
    try:
        event = {
            "event_id": "invoice_evt_001",
            "event_type": "InvoiceIssued",
            "payload": {"tenant": TENANT, "profile_id": PROFILE_ID, "amount": 125.0},
        }
        first = service.receive_event(event)
        duplicate = service.receive_event(event)
        failed_1 = service.receive_event({"event_id": "bad_evt_001", "event_type": "UnsupportedEvent", "payload": {"tenant": TENANT}})
        failed_2 = service.receive_event({"event_id": "bad_evt_001", "event_type": "UnsupportedEvent", "payload": {"tenant": TENANT}})
        dead = service.receive_event({"event_id": "bad_evt_001", "event_type": "UnsupportedEvent", "payload": {"tenant": TENANT}})
        workbench = service.build_workbench({"tenant": TENANT})["result"]
        allowed = runtime.customer_360_verify_owned_table_boundary(("customer_profile", "InvoiceIssued", "GET /billing/accounts"))
        blocked = runtime.customer_360_verify_owned_table_boundary(("foreign_customer_table", "shared_billing_account"))

        assert first["ok"] is True
        assert duplicate["ok"] is True
        assert duplicate["result"]["duplicate"] is True
        assert failed_1["ok"] is False
        assert failed_1["result"]["status"] == "retrying"
        assert failed_2["result"]["attempts"] == 2
        assert dead["result"]["status"] == "dead_letter"
        assert dead["result"]["attempts"] == 3
        assert workbench["inbox_count"] >= 2
        assert workbench["dead_letter_count"] == 1
        assert allowed["ok"] is True
        assert blocked["ok"] is False
        assert blocked["violations"] == ("foreign_customer_table", "shared_billing_account")
    finally:
        service.close()


def test_customer_360_runtime_governance_and_advanced_intelligence_are_executable():
    state = _runtime_customer_state()
    api = runtime.customer_360_build_api_contract()
    schema = runtime.customer_360_build_schema_contract()
    service_contract = runtime.customer_360_build_service_contract()
    release = runtime.customer_360_build_release_evidence()
    workbench = runtime.customer_360_build_workbench_view(state, tenant=TENANT)

    assert workbench["profile_count"] == 1
    assert workbench["effective_consent_count"] == 1
    assert workbench["customer_value"] == 420.0
    assert runtime.customer_360_build_timeline(state, PROFILE_ID)["event_count"] >= 2
    assert runtime.customer_360_simulate_preference_change(state, PROFILE_ID, channel="sms", status="opt_in")["reach_delta"] >= 0.1
    assert runtime.customer_360_forecast_customer_value((100.0, 220.0, 420.0), horizon_days=90)["forecast_value"] > 420.0
    assert runtime.customer_360_parse_customer_instruction("customer cust_360_001 channel email action update topic offers")["ok"] is True
    assert runtime.customer_360_score_customer_health({"churn": 0.1, "consent": 0.05, "engagement": 0.1, "value": 1.0})["decision"] == "monitor"
    assert runtime.customer_360_recommend_exception_resolution("duplicate_profile")["action"] == "open_merge_review"
    assert runtime.customer_360_route_customer_event(
        {"event_id": "route_evt_001"},
        rails=({"route": "profile_api", "available": False, "latency": 5}, {"route": "outbox", "available": True, "latency": 1}),
    )["failover_used"] is True
    assert runtime.customer_360_generate_profile_proof(state, PROFILE_ID, disclosure=("profile_id", "region", "lifecycle_state"))["proof"].startswith("zk_customer_")
    assert runtime.customer_360_screen_privacy_policy(state, PROFILE_ID, restricted_regions=("restricted",))["decision"] == "clear"
    assert runtime.customer_360_run_control_tests(state)["ok"] is True
    assert runtime.customer_360_federate_customer_view(state, PROFILE_ID, systems=("commerce", "billing", "service"))["projection"]["region"] == "US"
    assert runtime.customer_360_verify_customer_identity({"did": "did:appgen:customer:001", "issuer": "trusted_registry", "status": "active"})["ok"] is True
    assert runtime.customer_360_run_resilience_drill(state, "profile_api_timeout")["ok"] is True
    assert runtime.customer_360_rotate_crypto_epoch(state, "dilithium3_simulated")["key_id"] == "customer_epoch_0002"
    assert runtime.customer_360_schedule_carbon_aware_processing(({"window": "day", "carbon": 120}, {"window": "night", "carbon": 45}))["window"] == "night"
    assert runtime.customer_360_optimize_segments(({"segment": "all", "reach": 0.9, "risk": 0.4}, {"segment": "loyal", "reach": 0.75, "risk": 0.1}))["segment"] == "loyal"
    assert runtime.customer_360_allocate_channels(({"channel": "email", "priority": 0.8, "capacity": 10}, {"channel": "sms", "priority": 0.5, "capacity": 4}), customers=100)["ok"] is True
    assert runtime.customer_360_detect_engagement_anomaly(state)["ok"] is True
    assert runtime.customer_360_model_stochastic_customer_exposure(value_path=(100, 180, 260), volatility=0.12)["simulation_count"] == 1000
    assert runtime.customer_360_register_governed_model("customer_health", {"auc": 0.9, "drift_score": 0.04, "features": ("value", "consent")})["ok"] is True
    assert api["ok"] is True
    assert schema["ok"] is True
    assert service_contract["ok"] is True
    assert release["ok"] is True


def test_customer_360_rejects_nonstandard_backends_and_user_eventing_pickers():
    state = runtime.customer_360_empty_state()

    bad_backend = {**_configuration(), "database_backend": "sqlite"}
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.customer_360_configure_runtime(state, bad_backend)

    bad_eventing = {**_configuration(), "stream_engine": "user_selected_engine"}
    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.customer_360_configure_runtime(state, bad_eventing)
