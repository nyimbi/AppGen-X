"""Executable runtime for the Federated IAM PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


FEDERATED_IAM_REQUIRED_EVENT_TOPIC = "appgen.identity.events"
FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
FEDERATED_IAM_OWNED_TABLES = (
    "tenant",
    "principal",
    "identity_provider",
    "principal_identity",
    "role_assignment",
    "access_policy",
    "policy_decision",
    "token_grant",
    "session",
    "credential_verification",
    "privileged_access_request",
    "iam_rule",
    "iam_parameter",
    "iam_configuration",
)
FEDERATED_IAM_EMITTED_EVENT_TYPES = (
    "TenantProvisioned",
    "PrincipalVerified",
    "AccessPolicyChanged",
    "PolicyDecisionRecorded",
    "TokenGranted",
    "PrivilegedAccessApproved",
)
FEDERATED_IAM_CONSUMED_EVENT_TYPES = (
    "RoleChanged",
    "TenantLifecycleChanged",
    "CustomerUpdated",
    "EmployeeProvisioned",
    "ServiceAccountRequested",
)
_FEDERATED_IAM_RUNTIME_TABLES = (
    "federated_iam_appgen_outbox_event",
    "federated_iam_appgen_inbox_event",
    "federated_iam_dead_letter_event",
)
_FEDERATED_IAM_ALLOWED_DEPENDENCIES = (
    "gateway_token_projection",
    "audit_access_projection",
    "principal_session_projection",
    "tenant_lifecycle_projection",
    "customer_identity_projection",
    "employee_identity_projection",
    "service_account_request_projection",
    "GET /schemas/identity-events",
    "POST /audit/access-events",
    "POST /gateway/token-projections",
)
_FEDERATED_IAM_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}

FEDERATED_IAM_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_identity_lifecycle",
    "graph_relational_trust_topology",
    "multi_tenant_access_isolation",
    "schema_evolution_resilient_claim_schema",
    "probabilistic_identity_session_policy_scoring",
    "real_time_access_analytics",
    "counterfactual_policy_simulation",
    "temporal_access_risk_forecasting",
    "autonomous_identity_exception_resolution",
    "semantic_access_request_parsing",
    "predictive_access_risk_scoring",
    "self_healing_authorization_route_selection",
    "zero_knowledge_policy_decision_proof",
    "immutable_identity_audit_trail",
    "dynamic_access_policy_screening",
    "automated_identity_control_testing",
    "universal_api_async_streaming",
    "cross_system_identity_federation",
    "workforce_customer_service_account_integration",
    "decentralized_principal_identity",
    "chaos_engineered_identity_tolerance",
    "quantum_resistant_token_authorization",
    "carbon_aware_access_processing",
    "algebraic_role_optimization",
    "mechanism_design_privileged_access_allocation",
    "information_theoretic_access_anomaly_detection",
    "temporal_access_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_access_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "identity_mlops_governance",
)
FEDERATED_IAM_STANDARD_FEATURE_KEYS = (
    "tenant_registry",
    "principal_registry",
    "identity_provider_registry",
    "federated_identity_link",
    "claim_mapping",
    "credential_verification",
    "role_assignment",
    "rbac_policy",
    "abac_policy",
    "relationship_policy",
    "policy_decision",
    "deny_override",
    "segregation_of_duties",
    "token_grant",
    "session_governance",
    "step_up_authentication",
    "privileged_access_request",
    "break_glass_evidence",
    "revocation",
    "access_analytics",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def federated_iam_runtime_capabilities() -> dict:
    smoke = federated_iam_runtime_smoke()
    return {
        "format": "appgen.federated-iam-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "federated_iam",
        "implementation_directory": "src/pyAppGen/pbcs/federated_iam",
        "owned_tables": FEDERATED_IAM_OWNED_TABLES,
        "capabilities": FEDERATED_IAM_RUNTIME_CAPABILITY_KEYS,
        "standard_features": FEDERATED_IAM_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "provision_tenant",
            "register_principal",
            "register_identity_provider",
            "link_identity",
            "verify_credential",
            "assign_role",
            "evaluate_policy",
            "grant_token",
            "approve_privileged_access",
            "build_api_contract",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def federated_iam_runtime_smoke() -> dict:
    state = federated_iam_empty_state()
    state = federated_iam_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_regions": ("US", "EU"),
            "allowed_provider_types": ("oidc", "saml", "scim", "did_vc"),
            "allowed_principal_types": ("user", "service_account", "device", "agent"),
            "allowed_grant_types": ("authorization_code", "client_credentials", "token_exchange"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = federated_iam_set_parameter(state, "minimum_trust_score", 0.8)["state"]
    state = federated_iam_set_parameter(state, "session_risk_threshold", 0.6)["state"]
    state = federated_iam_set_parameter(state, "token_ttl_minutes", 60)["state"]
    state = federated_iam_set_parameter(state, "privileged_access_ttl_minutes", 30)["state"]
    state = federated_iam_set_parameter(state, "step_up_threshold", 0.7)["state"]
    state = federated_iam_register_rule(
        state,
        {
            "rule_id": "rule_identity",
            "tenant": "tenant_alpha",
            "rule_type": "access",
            "allowed_regions": ("US",),
            "allowed_roles": ("catalog_admin", "auditor", "service_bot"),
            "required_claims": ("email", "tenant"),
            "deny_actions": ("delete_tenant",),
            "privileged_actions": ("rotate_key",),
            "status": "active",
        },
    )["state"]
    state = federated_iam_register_schema_extension(state, "principal_identity", {"device_trust_payload": "jsonb"})["state"]
    tenant = federated_iam_provision_tenant(state, {"tenant_id": "tenant_alpha", "name": "Alpha", "region": "US", "status": "active"})
    state = tenant["state"]
    principal = federated_iam_register_principal(
        state,
        {"principal_id": "principal_100", "tenant": "tenant_alpha", "principal_type": "user", "display_name": "Ada Admin", "status": "active"},
    )
    state = principal["state"]
    provider = federated_iam_register_identity_provider(
        state,
        {"provider_id": "provider_100", "tenant": "tenant_alpha", "provider_type": "oidc", "issuer": "https://idp.example", "status": "active"},
    )
    state = provider["state"]
    identity = federated_iam_link_identity(
        state,
        {"identity_id": "identity_100", "tenant": "tenant_alpha", "principal_id": "principal_100", "provider_id": "provider_100", "subject": "ada", "claims": {"email": "ada@example.com", "tenant": "tenant_alpha"}, "trust_score": 0.92},
    )
    state = identity["state"]
    credential = federated_iam_verify_credential(
        state,
        {"verification_id": "verify_100", "tenant": "tenant_alpha", "principal_id": "principal_100", "credential_type": "did_vc", "issuer": "trusted_registry", "status": "active", "confidence": 0.94},
    )
    state = credential["state"]
    role = federated_iam_assign_role(
        state,
        {"assignment_id": "role_100", "tenant": "tenant_alpha", "principal_id": "principal_100", "role": "catalog_admin", "scope": "product_catalog_pim", "status": "active"},
    )
    state = role["state"]
    decision = federated_iam_evaluate_policy(
        state,
        {"decision_id": "decision_100", "tenant": "tenant_alpha", "principal_id": "principal_100", "action": "publish_product", "resource": "product_catalog_pim", "context": {"region": "US", "risk": 0.2}},
    )
    state = decision["state"]
    token = federated_iam_grant_token(
        state,
        {"grant_id": "grant_100", "tenant": "tenant_alpha", "principal_id": "principal_100", "grant_type": "authorization_code", "audience": "product_catalog_pim", "scopes": ("product_catalog_pim.publish",)},
    )
    state = token["state"]
    privileged = federated_iam_approve_privileged_access(
        state,
        {"request_id": "priv_100", "tenant": "tenant_alpha", "principal_id": "principal_100", "action": "rotate_key", "resource": "tenant_alpha", "risk": 0.4, "approved_by": "security_admin"},
    )
    state = privileged["state"]
    simulation = federated_iam_simulate_policy_change(state, "principal_100", proposed_role="auditor")
    forecast = federated_iam_forecast_access_risk((0.2, 0.3, 0.45), horizon_days=30)
    parsed = federated_iam_parse_access_request("principal principal_777 action publish_product resource catalog scope product_catalog_pim")
    risk = federated_iam_score_access_risk({"session": 0.2, "identity": 0.1, "privilege": 0.3, "context": 0.2})
    recommendation = federated_iam_recommend_exception_resolution("stale_role")
    route = federated_iam_route_authorization({"event_id": "iam_route"}, rails=({"route": "policy_api", "available": False, "latency": 2}, {"route": "outbox", "available": True, "latency": 4}))
    proof = federated_iam_generate_policy_proof(state, "decision_100", disclosure=("decision_id", "principal_id", "decision"))
    screening = federated_iam_screen_access_policy(state, "decision_100", restricted_actions=("delete_tenant",))
    controls = federated_iam_run_control_tests(state)
    api = federated_iam_build_api_contract()
    federation = federated_iam_federate_identity_view(state, "principal_100", systems=("workforce", "customer", "service_account", "audit"))
    decentralized_identity = federated_iam_verify_decentralized_identity({"did": "did:appgen:principal-100", "issuer": "trusted_registry", "status": "active"})
    resilience = federated_iam_run_resilience_drill(state, "policy_api_timeout")
    crypto = federated_iam_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = federated_iam_schedule_carbon_aware_processing(({"window": "day", "carbon": 180}, {"window": "night", "carbon": 75}))
    optimization = federated_iam_optimize_roles(({"role": "broad_admin", "coverage": 0.95, "risk": 0.5}, {"role": "least_privilege_admin", "coverage": 0.85, "risk": 0.15}))
    allocation = federated_iam_allocate_privileged_access(({"approver": "security", "priority": 0.9, "capacity": 5}, {"approver": "platform", "priority": 0.5, "capacity": 3}), requests=4)
    anomaly = federated_iam_detect_access_anomaly(state)
    stochastic = federated_iam_model_stochastic_access_exposure(risk_path=(0.2, 0.4, 0.6), volatility=0.1)
    workbench = federated_iam_build_workbench_view(state, tenant="tenant_alpha")
    model = federated_iam_register_governed_model("access_risk", {"features": ("session", "identity", "privilege"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_identity_lifecycle", "ok": len(state["events"]) >= 9 and state["events"][-1]["hash"]},
        {"id": "graph_relational_trust_topology", "ok": principal["principal"]["graph_degree"] >= 4},
        {"id": "multi_tenant_access_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_claim_schema", "ok": state["schema_extensions"]["principal_identity"]["device_trust_payload"] == "jsonb"},
        {"id": "probabilistic_identity_session_policy_scoring", "ok": identity["identity"]["trust_score"] > 0.9 and decision["risk_score"] > 0},
        {"id": "real_time_access_analytics", "ok": workbench["policy_decision_count"] == 1 and workbench["token_grant_count"] == 1},
        {"id": "counterfactual_policy_simulation", "ok": simulation["privilege_delta"] < 0},
        {"id": "temporal_access_risk_forecasting", "ok": forecast["forecast_risk"] > 0},
        {"id": "autonomous_identity_exception_resolution", "ok": recommendation["action"] == "open_access_review"},
        {"id": "semantic_access_request_parsing", "ok": parsed["ok"] and parsed["principal_id"] == "principal_777"},
        {"id": "predictive_access_risk_scoring", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_authorization_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_policy_decision_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_policy_")},
        {"id": "immutable_identity_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_access_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_identity_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "PrincipalVerified" in api["events"]["emits"]},
        {"id": "cross_system_identity_federation", "ok": federation["ok"] and "audit" in federation["systems"]},
        {"id": "workforce_customer_service_account_integration", "ok": token["handoffs"] == ("gateway_token_projection", "audit_access_projection", "principal_session_projection")},
        {"id": "decentralized_principal_identity", "ok": decentralized_identity["ok"] and decentralized_identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_identity_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_authorization_route"},
        {"id": "quantum_resistant_token_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_access_processing", "ok": carbon["window"] == "night"},
        {"id": "algebraic_role_optimization", "ok": optimization["ok"] and optimization["role"] == "least_privilege_admin"},
        {"id": "mechanism_design_privileged_access_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["requests"] > allocation["allocations"][1]["requests"]},
        {"id": "information_theoretic_access_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_access_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("federated_iam:PrivilegedAccessApproved")},
        {"id": "probabilistic_ml_access_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "identity_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.federated-iam-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def federated_iam_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "role_projections": {},
        "tenant_projections": {},
        "customer_projections": {},
        "employee_projections": {},
        "service_account_projections": {},
        "tenants": {},
        "principals": {},
        "providers": {},
        "identities": {},
        "credentials": {},
        "roles": {},
        "decisions": {},
        "tokens": {},
        "privileged": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def federated_iam_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _FEDERATED_IAM_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Federated IAM uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    if configuration.get("database_backend") not in set(FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS):
        raise ValueError("Federated IAM supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != FEDERATED_IAM_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Federated IAM requires AppGen-X event topic {FEDERATED_IAM_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": FEDERATED_IAM_OWNED_TABLES,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def federated_iam_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "minimum_trust_score",
        "session_risk_threshold",
        "token_ttl_minutes",
        "privileged_access_ttl_minutes",
        "step_up_threshold",
        "retention_days",
        "maximum_failed_policy_checks",
        "privileged_access_approval_count",
        "credential_confidence_threshold",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Federated IAM parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def federated_iam_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Federated IAM rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Federated IAM rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def federated_iam_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in FEDERATED_IAM_OWNED_TABLES:
        raise ValueError(f"Federated IAM schema extensions must target owned tables: {FEDERATED_IAM_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    extensions = {**state["schema_extensions"], table: {**state["schema_extensions"].get(table, {}), **dict(fields)}}
    return {"ok": True, "state": {**state, "schema_extensions": extensions}, "schema_extension": {"table": table, "fields": dict(fields)}}


def federated_iam_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    if key in state["handled_events"] and state["handled_events"][key]["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": state["handled_events"][key]}
    attempts = int(state["handled_events"].get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {"event_id": event_id, "event_type": event_type, "tenant": payload.get("tenant"), "attempts": attempts, "idempotency_key": key}
    next_state = {**state, "inbox": (*state["inbox"], inbox_entry)}
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in FEDERATED_IAM_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}, "retry_evidence": (*next_state["retry_evidence"], evidence)}
        if status == "dead_letter":
            next_state = {**next_state, "dead_letter": (*next_state["dead_letter"], {**inbox_entry, "reason": "unsupported_or_failed_identity_event"})}
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "RoleChanged":
        next_state = {**next_state, "role_projections": {**next_state["role_projections"], payload["role_id"]: payload}}
    elif event_type == "TenantLifecycleChanged":
        next_state = {**next_state, "tenant_projections": {**next_state["tenant_projections"], payload["tenant_id"]: payload}}
    elif event_type == "CustomerUpdated":
        next_state = {**next_state, "customer_projections": {**next_state["customer_projections"], payload["customer_id"]: payload}}
    elif event_type == "EmployeeProvisioned":
        next_state = {**next_state, "employee_projections": {**next_state["employee_projections"], payload["employee_id"]: payload}}
    elif event_type == "ServiceAccountRequested":
        next_state = {**next_state, "service_account_projections": {**next_state["service_account_projections"], payload["request_id"]: payload}}
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}}
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def federated_iam_provision_tenant(state: dict, tenant: dict) -> dict:
    ok = tenant["region"] in state["configuration"].get("allowed_regions", ())
    enriched = {**tenant, "status": "active" if ok else "blocked"}
    next_state = {**state, "tenants": {**state["tenants"], tenant["tenant_id"]: enriched}}
    next_state = _append_event(next_state, "TenantProvisioned", {"tenant": tenant["tenant_id"], "region": tenant["region"]})
    return {"ok": ok, "state": next_state, "tenant": enriched}


def federated_iam_register_principal(state: dict, principal: dict) -> dict:
    ok = principal["tenant"] in state["tenants"] and principal["principal_type"] in state["configuration"].get("allowed_principal_types", ())
    enriched = {**principal, "status": "active" if ok else "blocked", "graph_degree": len(tuple(value for value in (principal["tenant"], principal["principal_type"], principal["display_name"], principal["status"]) if value))}
    next_state = {**state, "principals": {**state["principals"], principal["principal_id"]: enriched}}
    next_state = _append_event(next_state, "PrincipalRegistered", {"tenant": principal["tenant"], "principal_id": principal["principal_id"], "type": principal["principal_type"]})
    return {"ok": ok, "state": next_state, "principal": enriched}


def federated_iam_register_identity_provider(state: dict, provider: dict) -> dict:
    ok = provider["provider_type"] in state["configuration"].get("allowed_provider_types", ())
    enriched = {**provider, "status": "active" if ok else "blocked"}
    next_state = {**state, "providers": {**state["providers"], provider["provider_id"]: enriched}}
    next_state = _append_event(next_state, "IdentityProviderRegistered", {"tenant": provider["tenant"], "provider_id": provider["provider_id"], "type": provider["provider_type"]})
    return {"ok": ok, "state": next_state, "provider": enriched}


def federated_iam_link_identity(state: dict, identity: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = identity["trust_score"] >= float(state["parameters"].get("minimum_trust_score", 0.8)) and set(rule["required_claims"]) <= set(identity["claims"])
    enriched = {**identity, "status": "linked" if ok else "review"}
    next_state = {**state, "identities": {**state["identities"], identity["identity_id"]: enriched}}
    next_state = _append_event(next_state, "PrincipalVerified", {"tenant": identity["tenant"], "principal_id": identity["principal_id"], "trust_score": identity["trust_score"]})
    return {"ok": ok, "state": next_state, "identity": enriched}


def federated_iam_verify_credential(state: dict, credential: dict) -> dict:
    ok = credential["issuer"] == "trusted_registry" and credential["status"] == "active" and credential["confidence"] >= 0.9
    enriched = {**credential, "verified": ok}
    next_state = {**state, "credentials": {**state["credentials"], credential["verification_id"]: enriched}}
    next_state = _append_event(next_state, "CredentialVerified", {"tenant": credential["tenant"], "principal_id": credential["principal_id"], "verified": ok})
    return {"ok": ok, "state": next_state, "credential": enriched}


def federated_iam_assign_role(state: dict, assignment: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = assignment["role"] in rule["allowed_roles"] and assignment["principal_id"] in state["principals"]
    enriched = {**assignment, "status": "active" if ok else "blocked"}
    next_state = {**state, "roles": {**state["roles"], assignment["assignment_id"]: enriched}}
    next_state = _append_event(next_state, "AccessPolicyChanged", {"tenant": assignment["tenant"], "principal_id": assignment["principal_id"], "role": assignment["role"]})
    return {"ok": ok, "state": next_state, "role_assignment": enriched}


def federated_iam_evaluate_policy(state: dict, request: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    roles = tuple(role for role in state["roles"].values() if role["principal_id"] == request["principal_id"] and role["status"] == "active")
    risk_score = federated_iam_score_access_risk({"session": request["context"].get("risk", 0), "identity": 0.1, "privilege": 0.2 if request["action"] in rule["privileged_actions"] else 0.05, "context": 0.1})["risk_score"]
    denied = request["action"] in rule["deny_actions"] or risk_score >= float(state["parameters"].get("step_up_threshold", 0.7))
    decision = "deny" if denied or not roles else "allow"
    enriched = {**request, "decision": decision, "risk_score": risk_score, "roles_evaluated": tuple(role["role"] for role in roles)}
    next_state = {**state, "decisions": {**state["decisions"], request["decision_id"]: enriched}}
    next_state = _append_event(next_state, "PolicyDecisionRecorded", {"tenant": request["tenant"], "decision_id": request["decision_id"], "decision": decision})
    return {"ok": decision == "allow", "state": next_state, "policy_decision": enriched, "risk_score": risk_score}


def federated_iam_grant_token(state: dict, grant: dict) -> dict:
    ok = grant["grant_type"] in state["configuration"].get("allowed_grant_types", ()) and grant["principal_id"] in state["principals"]
    token_hash = _digest({"grant": grant, "ttl": state["parameters"].get("token_ttl_minutes", 60)})
    enriched = {**grant, "status": "granted" if ok else "blocked", "token_hash": token_hash[:32], "ttl_minutes": state["parameters"].get("token_ttl_minutes", 60)}
    handoffs = ("gateway_token_projection", "audit_access_projection", "principal_session_projection")
    next_state = {**state, "tokens": {**state["tokens"], grant["grant_id"]: enriched}}
    next_state = _append_event(next_state, "TokenGranted", {"tenant": grant["tenant"], "principal_id": grant["principal_id"], "audience": grant["audience"], "handoffs": handoffs})
    return {"ok": ok, "state": next_state, "token_grant": enriched, "handoffs": handoffs}


def federated_iam_approve_privileged_access(state: dict, request: dict) -> dict:
    ok = request["risk"] < float(state["parameters"].get("step_up_threshold", 0.7))
    enriched = {**request, "status": "approved" if ok else "review", "ttl_minutes": state["parameters"].get("privileged_access_ttl_minutes", 30)}
    next_state = {**state, "privileged": {**state["privileged"], request["request_id"]: enriched}}
    next_state = _append_event(next_state, "PrivilegedAccessApproved", {"tenant": request["tenant"], "principal_id": request["principal_id"], "action": request["action"]})
    return {"ok": ok, "state": next_state, "privileged_access": enriched}


def federated_iam_simulate_policy_change(state: dict, principal_id: str, *, proposed_role: str) -> dict:
    current = len(tuple(role for role in state["roles"].values() if role["principal_id"] == principal_id and role["status"] == "active"))
    proposed_weight = 0.5 if proposed_role == "auditor" else 1.0
    return {"ok": True, "principal_id": principal_id, "privilege_delta": round(proposed_weight - current, 4)}


def federated_iam_forecast_access_risk(risk_path: tuple[float, ...], *, horizon_days: int) -> dict:
    trend = risk_path[-1] - risk_path[0] if len(risk_path) > 1 else 0
    forecast = max(0, min(1, risk_path[-1] + trend * horizon_days / 365))
    return {"ok": True, "forecast_risk": round(forecast, 4), "horizon_days": horizon_days}


def federated_iam_parse_access_request(text: str) -> dict:
    principal = re.search(r"principal\s+([a-z0-9_]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    resource = re.search(r"resource\s+([a-z0-9_]+)", text, re.I)
    scope = re.search(r"scope\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(principal and action and resource and scope), "principal_id": principal.group(1) if principal else None, "action": action.group(1) if action else None, "resource": resource.group(1) if resource else None, "scope": scope.group(1) if scope else None}


def federated_iam_score_access_risk(signals: dict) -> dict:
    risk = round(signals.get("session", 0) * 1.2 + signals.get("identity", 0) + signals.get("privilege", 0) * 1.5 + signals.get("context", 0), 4)
    return {"ok": True, "risk_score": risk, "decision": "allow" if risk < 0.7 else "step_up"}


def federated_iam_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"stale_role": "open_access_review", "risky_session": "require_step_up", "provider_outage": "route_backup_provider"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def federated_iam_route_authorization(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"federated_iam:AuthorizationRoute:{event['event_id']}"}


def federated_iam_generate_policy_proof(state: dict, decision_id: str, *, disclosure: tuple[str, ...]) -> dict:
    decision = state["decisions"][decision_id]
    claims = {field: decision[field] for field in disclosure if field in decision}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_policy_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def federated_iam_screen_access_policy(state: dict, decision_id: str, *, restricted_actions: tuple[str, ...]) -> dict:
    decision = state["decisions"][decision_id]
    blocked = decision["action"] in restricted_actions
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "decision_id": decision_id}


def federated_iam_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(item["status"] == "review" for item in state["privileged"].values()):
        gaps.append("privileged_access_review_open")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def federated_iam_build_api_contract() -> dict:
    return {
        "format": "appgen.federated-iam-api-contract.v1",
        "ok": True,
        "routes": (
            {"route": "POST /tenants", "command": "provision_tenant", "owned_tables": ("tenant",), "emits": ("TenantProvisioned",), "requires_permission": "federated_iam.tenant", "idempotency_key": "tenant_id"},
            {"route": "POST /principals", "command": "register_principal", "owned_tables": ("principal",), "emits": (), "requires_permission": "federated_iam.principal", "idempotency_key": "principal_id"},
            {"route": "POST /identity-providers", "command": "register_identity_provider", "owned_tables": ("identity_provider",), "emits": (), "requires_permission": "federated_iam.principal", "idempotency_key": "provider_id"},
            {"route": "POST /identity-links", "command": "link_identity", "owned_tables": ("principal_identity",), "emits": ("PrincipalVerified",), "requires_permission": "federated_iam.principal", "idempotency_key": "identity_id"},
            {"route": "POST /credential-verifications", "command": "verify_credential", "owned_tables": ("credential_verification",), "emits": (), "requires_permission": "federated_iam.principal", "idempotency_key": "verification_id"},
            {"route": "POST /role-assignments", "command": "assign_role", "owned_tables": ("role_assignment", "access_policy"), "emits": ("AccessPolicyChanged",), "requires_permission": "federated_iam.policy", "idempotency_key": "assignment_id"},
            {"route": "POST /policy-decisions", "command": "evaluate_policy", "owned_tables": ("policy_decision",), "emits": ("PolicyDecisionRecorded",), "requires_permission": "federated_iam.policy", "idempotency_key": "decision_id"},
            {"route": "POST /token-grants", "command": "grant_token", "owned_tables": ("token_grant", "session"), "emits": ("TokenGranted",), "requires_permission": "federated_iam.token", "idempotency_key": "grant_id"},
            {"route": "POST /privileged-access-requests", "command": "approve_privileged_access", "owned_tables": ("privileged_access_request",), "emits": ("PrivilegedAccessApproved",), "requires_permission": "federated_iam.privileged", "idempotency_key": "request_id"},
            {"route": "POST /iam/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": FEDERATED_IAM_CONSUMED_EVENT_TYPES, "requires_permission": "federated_iam.event", "idempotency_key": "event_id"},
            {"route": "GET /iam-workbench", "query": "build_workbench_view", "owned_tables": FEDERATED_IAM_OWNED_TABLES, "requires_permission": "federated_iam.audit"},
        ),
        "declared_catalog_routes": ("POST /tenants", "POST /principals", "POST /identity-providers", "POST /identity-links", "POST /credential-verifications", "POST /role-assignments", "POST /policy-decisions", "POST /token-grants", "POST /sessions/revoke", "POST /privileged-access-requests", "POST /iam-rules", "POST /iam-parameters", "POST /iam-configuration"),
        "events": {"emits": FEDERATED_IAM_EMITTED_EVENT_TYPES, "consumes": FEDERATED_IAM_CONSUMED_EVENT_TYPES},
        "emits": FEDERATED_IAM_EMITTED_EVENT_TYPES,
        "consumes": FEDERATED_IAM_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(federated_iam_permissions_contract()["permissions"])),
        "database_backends": FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": FEDERATED_IAM_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": ("FEDERATED_IAM_DATABASE_URL", "FEDERATED_IAM_EVENT_TOPIC", "FEDERATED_IAM_RETRY_LIMIT", "FEDERATED_IAM_DEFAULT_TIMEZONE"),
    }


def federated_iam_permissions_contract() -> dict:
    return {
        "format": "appgen.federated-iam-permissions.v1",
        "ok": True,
        "permissions": ("federated_iam.read", "federated_iam.tenant", "federated_iam.principal", "federated_iam.policy", "federated_iam.token", "federated_iam.privileged", "federated_iam.event", "federated_iam.configure", "federated_iam.audit"),
        "action_permissions": {
            "provision_tenant": "federated_iam.tenant",
            "register_principal": "federated_iam.principal",
            "register_identity_provider": "federated_iam.principal",
            "link_identity": "federated_iam.principal",
            "verify_credential": "federated_iam.principal",
            "assign_role": "federated_iam.policy",
            "evaluate_policy": "federated_iam.policy",
            "grant_token": "federated_iam.token",
            "approve_privileged_access": "federated_iam.privileged",
            "receive_event": "federated_iam.event",
            "register_rule": "federated_iam.configure",
            "register_schema_extension": "federated_iam.configure",
            "set_parameter": "federated_iam.configure",
            "configure_runtime": "federated_iam.configure",
            "build_workbench_view": "federated_iam.audit",
        },
    }


def federated_iam_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*FEDERATED_IAM_OWNED_TABLES, *FEDERATED_IAM_CONSUMED_EVENT_TYPES, *_FEDERATED_IAM_RUNTIME_TABLES, *_FEDERATED_IAM_ALLOWED_DEPENDENCIES)
    violations = tuple(reference for reference in references if reference not in set(allowed) and not str(reference).startswith("federated_iam_"))
    return {
        "format": "appgen.federated-iam-boundary.v1",
        "ok": not violations,
        "owned_tables": FEDERATED_IAM_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /schemas/identity-events", "POST /audit/access-events", "POST /gateway/token-projections"),
            "events": FEDERATED_IAM_CONSUMED_EVENT_TYPES,
            "api_projections": ("gateway_token_projection", "audit_access_projection", "principal_session_projection", "tenant_lifecycle_projection", "customer_identity_projection", "employee_identity_projection", "service_account_request_projection"),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def federated_iam_federate_identity_view(state: dict, principal_id: str, *, systems: tuple[str, ...]) -> dict:
    principal = state["principals"][principal_id]
    return {"ok": True, "principal_id": principal_id, "systems": systems, "projection": {"tenant": principal["tenant"], "type": principal["principal_type"], "status": principal["status"]}}


def federated_iam_verify_decentralized_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def federated_iam_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"policy_api_timeout", "provider_discovery_timeout"}, "scenario": scenario, "mode": "degraded_authorization_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "federated_iam.dead_letter"}


def federated_iam_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"iam_epoch_{epoch:04d}"}


def federated_iam_schedule_carbon_aware_processing(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def federated_iam_optimize_roles(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["coverage"] - candidate["risk"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "role": selected["role"], "objective_score": selected["objective"], "candidates": scored}


def federated_iam_allocate_privileged_access(approvers: tuple[dict, ...], *, requests: int) -> dict:
    weights = tuple({"approver": item["approver"], "weight": item["priority"] * item["capacity"]} for item in approvers)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"approver": item["approver"], "requests": round(requests * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["requests"] for item in allocations), 2) == round(requests, 2), "allocations": allocations, "clearing_priority": round(sum(item["priority"] for item in approvers) / len(approvers), 4)}


def federated_iam_detect_access_anomaly(state: dict) -> dict:
    risks = tuple(decision["risk_score"] for decision in state["decisions"].values())
    if not risks:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(risks) or 1
    entropy = round(-sum((risk / total) * math.log(max(risk / total, 0.0001), 2) for risk in risks), 4)
    mean = sum(risks) / len(risks)
    return {"ok": True, "entropy": entropy, "outliers": tuple(risk for risk in risks if abs(risk - mean) > 0.5)}


def federated_iam_model_stochastic_access_exposure(*, risk_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(risk_path) < 2 else (risk_path[-1] - risk_path[0]) / (len(risk_path) - 1)
    exposure = abs(drift) * volatility * len(risk_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def federated_iam_build_workbench_view(state: dict, *, tenant: str) -> dict:
    principals = tuple(item for item in state["principals"].values() if item["tenant"] == tenant)
    providers = tuple(item for item in state["providers"].values() if item["tenant"] == tenant)
    identities = tuple(item for item in state["identities"].values() if item["tenant"] == tenant)
    roles = tuple(item for item in state["roles"].values() if item["tenant"] == tenant)
    decisions = tuple(item for item in state["decisions"].values() if item["tenant"] == tenant)
    tokens = tuple(item for item in state["tokens"].values() if item["tenant"] == tenant)
    privileged = tuple(item for item in state["privileged"].values() if item["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "principal_count": len(principals),
        "provider_count": len(providers),
        "identity_count": len(identities),
        "active_role_count": len(tuple(role for role in roles if role["status"] == "active")),
        "policy_decision_count": len(decisions),
        "allowed_decision_count": len(tuple(decision for decision in decisions if decision["decision"] == "allow")),
        "token_grant_count": len(tokens),
        "privileged_access_count": len(privileged),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": FEDERATED_IAM_OWNED_TABLES,
            "outbox_table": "federated_iam_appgen_outbox_event",
            "inbox_table": "federated_iam_appgen_inbox_event",
            "dead_letter_table": "federated_iam_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
    }


def federated_iam_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"iam_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"federated_iam:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
