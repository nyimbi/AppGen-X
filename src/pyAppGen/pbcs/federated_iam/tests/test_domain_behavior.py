"""Executable domain behavior tests for the federated_iam PBC."""

import pytest

from .. import agent
from .. import permissions
from .. import routes
from .. import runtime
from .. import seed_data
from .. import services
from .. import ui


def _all_permissions():
    return tuple(permissions.permission_manifest()["permissions"])


def test_identity_lifecycle_is_executable_through_service_ui_routes_and_agent():
    service = services.create_seeded_service(_all_permissions())

    tenant = service.execute(
        "provision_tenant",
        {
            "tenant_id": "tenant_domain_alpha",
            "name": "Domain Alpha",
            "region": "US",
            "encryption_key_id": "key_domain_alpha",
            "compliance_boundary": "regulated_identity",
        },
    )
    principal = service.execute(
        "register_principal",
        {
            "tenant": "tenant_domain_alpha",
            "principal_id": "principal_domain_001",
            "principal_type": "user",
            "display_name": "Ada Domain",
            "status": "active",
            "attributes": {"department": "security", "clearance": "high"},
        },
    )
    provider = service.execute(
        "register_identity_provider",
        {
            "tenant": "tenant_domain_alpha",
            "provider_id": "provider_domain_corp",
            "provider_type": "oidc",
            "issuer": "https://identity.example.test",
            "status": "active",
        },
    )
    identity = service.execute(
        "link_identity",
        {
            "tenant": "tenant_domain_alpha",
            "identity_id": "identity_domain_001",
            "principal_id": "principal_domain_001",
            "provider_id": "provider_domain_corp",
            "subject": "ada.domain@example.test",
            "claims": {"email": "ada.domain@example.test", "tenant": "tenant_domain_alpha"},
            "trust_score": 0.97,
        },
    )
    credential = service.execute(
        "verify_credential",
        {
            "tenant": "tenant_domain_alpha",
            "verification_id": "credential_domain_001",
            "principal_id": "principal_domain_001",
            "credential_type": "verified_employee",
            "issuer": "trusted_registry",
            "confidence": 0.96,
            "status": "active",
        },
    )
    role = service.execute(
        "assign_role",
        {
            "tenant": "tenant_domain_alpha",
            "assignment_id": "role_domain_admin",
            "principal_id": "principal_domain_001",
            "role": "tenant_admin",
            "scope": "federated_iam",
            "status": "active",
            "expires_at": "2026-12-31T00:00:00Z",
        },
    )
    decision = service.execute(
        "evaluate_policy",
        {
            "tenant": "tenant_domain_alpha",
            "decision_id": "decision_domain_publish",
            "principal_id": "principal_domain_001",
            "action": "publish_identity_policy",
            "resource": "federated_iam",
            "context": {"network": "managed", "device": "compliant"},
            "risk_score": 0.24,
        },
    )
    token = service.execute(
        "grant_token",
        {
            "tenant": "tenant_domain_alpha",
            "grant_id": "grant_domain_001",
            "principal_id": "principal_domain_001",
            "grant_type": "authorization_code",
            "audience": "api_gateway_mesh",
            "scopes": ("identity:read", "identity:policy"),
        },
    )
    privileged = service.execute(
        "approve_privileged_access",
        {
            "tenant": "tenant_domain_alpha",
            "request_id": "priv_domain_001",
            "principal_id": "principal_domain_001",
            "action": "rotate_signing_key",
            "reason": "scheduled crypto hygiene",
            "approvers": ("security_lead", "platform_owner"),
            "risk": 0.22,
        },
    )
    workbench = service.execute("build_workbench_view", {"tenant": "tenant_domain_alpha"})
    rendered = ui.federated_iam_render_workbench(
        service.state,
        tenant="tenant_domain_alpha",
        principal_permissions=_all_permissions(),
    )
    routed = routes.dispatch_route(
        "GET",
        "/iam-workbench",
        {"tenant": "tenant_domain_alpha"},
        service=service,
        granted_permissions=_all_permissions(),
    )
    assistant_plan = agent.document_instruction_plan(
        "Verify a high-assurance employee credential and issue a scoped token.",
        "create principal principal_domain_001 then grant token for api_gateway_mesh",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "federated_iam_principal",
        {"principal_id": "principal_domain_001"},
    )

    assert tenant["ok"] is True
    assert principal["ok"] is True
    assert provider["ok"] is True
    assert identity["ok"] is True
    assert credential["ok"] is True
    assert role["ok"] is True
    assert decision["ok"] is True
    assert token["ok"] is True
    assert privileged["ok"] is True
    assert workbench["result"]["principal_count"] == 1
    assert workbench["result"]["token_grant_count"] == 1
    assert rendered["ok"] is True
    assert "principal_form" in rendered["visible_forms"]
    assert "identity_onboarding" in rendered["visible_wizards"]
    assert routed["ok"] is True
    assert routed["result"]["result"]["tenant"] == "tenant_domain_alpha"
    assert assistant_plan["ok"] is True
    assert crud_plan["ok"] is True
    assert crud_plan["requires_confirmation"] is True
    assert all(event["topic"] == runtime.FEDERATED_IAM_REQUIRED_EVENT_TOPIC for event in service.state["outbox"])
    assert any(event["event_type"] == "TokenGranted" for event in service.state["outbox"])


def test_event_handlers_are_idempotent_and_capture_retry_dead_letter_evidence():
    service = services.create_seeded_service(_all_permissions())
    role_event = {
        "event_id": "role_evt_domain",
        "event_type": "RoleChanged",
        "idempotency_key": "role:domain",
        "payload": {
            "tenant": "tenant_seed_alpha",
            "role_id": "role_evt_domain",
            "principal_id": "principal_seed_alice",
            "role": "security_auditor",
            "scope": "federated_iam",
            "status": "active",
        },
    }
    first = service.execute("receive_event", role_event)
    duplicate = service.execute("receive_event", role_event)
    unsupported_event = {
        "event_id": "unsupported_iam_evt",
        "event_type": "UnsupportedIamEvent",
        "idempotency_key": "unsupported:iam",
        "payload": {"tenant": "tenant_seed_alpha"},
    }
    retry_1 = service.execute("receive_event", unsupported_event)
    retry_2 = service.execute("receive_event", unsupported_event)
    dead_letter = service.execute("receive_event", unsupported_event)

    assert first["ok"] is True
    assert first["result"]["handler"]["status"] == "processed"
    assert duplicate["ok"] is True
    assert duplicate["result"]["duplicate"] is True
    assert retry_1["ok"] is False
    assert retry_1["result"]["handler"]["status"] == "retrying"
    assert retry_2["result"]["handler"]["status"] == "retrying"
    assert dead_letter["result"]["handler"]["status"] == "dead_letter"
    assert service.state["dead_letter"][-1]["reason"] == "unsupported_or_failed_identity_event"
    assert service.state["retry_evidence"][-1]["attempts"] == 3


def test_advanced_identity_controls_are_domain_specific_and_executable():
    state = seed_data.build_seed_state()["state"]

    policy_change = runtime.federated_iam_simulate_policy_change(
        state,
        "principal_seed_alice",
        proposed_role="auditor",
    )
    risk_forecast = runtime.federated_iam_forecast_access_risk((0.2, 0.3, 0.45), horizon_days=30)
    parsed = runtime.federated_iam_parse_access_request(
        "principal principal_777 action publish_product resource catalog scope product_catalog_pim"
    )
    risk_score = runtime.federated_iam_score_access_risk(
        {"session": 0.1, "identity": 0.1, "privilege": 0.1, "context": 0.1}
    )
    resolution = runtime.federated_iam_recommend_exception_resolution("stale_role")
    route = runtime.federated_iam_route_authorization(
        {"event_id": "route_evt_001"},
        rails=(
            {"route": "policy_api_primary", "available": False, "latency": 1},
            {"route": "outbox_fallback", "available": True, "latency": 9},
        ),
    )
    proof = runtime.federated_iam_generate_policy_proof(
        state,
        "decision_seed_publish",
        disclosure=("decision_id", "principal_id", "decision"),
    )
    sanctions = runtime.federated_iam_screen_access_policy(
        state,
        "decision_seed_publish",
        restricted_actions=("delete_tenant",),
    )
    controls = runtime.federated_iam_run_control_tests(state)
    identity_view = runtime.federated_iam_federate_identity_view(
        state,
        "principal_seed_alice",
        systems=("workforce", "customer", "audit"),
    )
    decentralized = runtime.federated_iam_verify_decentralized_identity(
        {"did": "did:appgen:principal:001", "issuer": "trusted_registry", "status": "active"}
    )
    resilience = runtime.federated_iam_run_resilience_drill(state, "policy_api_timeout")
    crypto = runtime.federated_iam_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = runtime.federated_iam_schedule_carbon_aware_processing(
        ({"window": "day", "carbon": 180}, {"window": "night", "carbon": 75})
    )
    role = runtime.federated_iam_optimize_roles(
        (
            {"role": "broad_admin", "coverage": 0.95, "risk": 0.5},
            {"role": "least_privilege_admin", "coverage": 0.85, "risk": 0.15},
        )
    )
    allocation = runtime.federated_iam_allocate_privileged_access(
        (
            {"approver": "security", "priority": 0.9, "capacity": 5},
            {"approver": "platform", "priority": 0.5, "capacity": 3},
        ),
        requests=4,
    )
    anomaly = runtime.federated_iam_detect_access_anomaly(state)
    exposure = runtime.federated_iam_model_stochastic_access_exposure(
        risk_path=(0.2, 0.4, 0.6),
        volatility=0.1,
    )
    governed_model = runtime.federated_iam_register_governed_model(
        "access_risk",
        {"auc": 0.91, "drift_score": 0.04, "features": ("session", "identity", "privilege")},
    )

    assert policy_change["privilege_delta"] < 0
    assert risk_forecast["forecast_risk"] > 0.45
    assert parsed["ok"] is True
    assert risk_score["decision"] == "allow"
    assert resolution["action"] == "open_access_review"
    assert route["route"] == "outbox_fallback"
    assert route["failover_used"] is True
    assert proof["proof"].startswith("zk_policy_")
    assert sanctions["decision"] == "clear"
    assert controls["ok"] is True
    assert identity_view["ok"] is True
    assert decentralized["ok"] is True
    assert resilience["ok"] is True
    assert crypto["key_id"] == "iam_epoch_0002"
    assert carbon["window"] == "night"
    assert role["role"] == "least_privilege_admin"
    assert allocation["ok"] is True
    assert anomaly["ok"] is True
    assert exposure["simulation_count"] == 1000
    assert governed_model["ok"] is True


def test_runtime_configuration_rejects_unsupported_backends_and_eventing_choices():
    state = runtime.federated_iam_empty_state()
    config = seed_data.default_runtime_configuration()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.federated_iam_configure_runtime(state, {**config, "database_backend": "sqlite"})

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.federated_iam_configure_runtime(state, {**config, "stream_engine": "kafka"})


def test_owned_boundary_allows_declared_dependencies_and_rejects_shared_tables():
    allowed = runtime.federated_iam_verify_owned_table_boundary(
        (
            "principal",
            "RoleChanged",
            "GET /schemas/identity-events",
            "gateway_token_projection",
        )
    )
    blocked = runtime.federated_iam_verify_owned_table_boundary(
        ("external_customer_table", "ledger_journal_entry")
    )

    assert allowed["ok"] is True
    assert allowed["declared_dependencies"]["shared_tables"] == ()
    assert blocked["ok"] is False
    assert blocked["violations"] == ("external_customer_table", "ledger_journal_entry")


def test_contract_builders_return_release_ready_identity_package_evidence():
    assert runtime.federated_iam_build_api_contract()["ok"] is True
    assert runtime.federated_iam_build_schema_contract()["ok"] is True
    assert runtime.federated_iam_build_service_contract()["ok"] is True
    evidence = runtime.federated_iam_build_release_evidence()

    assert evidence["ok"] is True
    assert evidence["api"]["event_contract"] == "AppGen-X"
    assert all(check["ok"] for check in evidence["checks"])
    assert evidence["workbench"]["ok"] is True
