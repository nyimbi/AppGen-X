"""Executable seed-data contract for the federated_iam PBC."""

from __future__ import annotations

from .runtime import FEDERATED_IAM_REQUIRED_EVENT_TOPIC
from .runtime import federated_iam_approve_privileged_access
from .runtime import federated_iam_assign_role
from .runtime import federated_iam_build_workbench_view
from .runtime import federated_iam_configure_runtime
from .runtime import federated_iam_empty_state
from .runtime import federated_iam_evaluate_policy
from .runtime import federated_iam_grant_token
from .runtime import federated_iam_link_identity
from .runtime import federated_iam_provision_tenant
from .runtime import federated_iam_receive_event
from .runtime import federated_iam_register_identity_provider
from .runtime import federated_iam_register_principal
from .runtime import federated_iam_register_rule
from .runtime import federated_iam_set_parameter
from .runtime import federated_iam_verify_credential


PBC_KEY = "federated_iam"
_DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "allowed_regions": ("US", "EU", "KE"),
    "allowed_provider_types": ("oidc", "saml", "scim", "did_vc"),
    "allowed_principal_types": ("user", "service_account", "device", "agent"),
    "allowed_grant_types": ("authorization_code", "client_credentials", "token_exchange"),
    "default_timezone": "UTC",
    "workbench_limit": 100,
}
_DEFAULT_PARAMETERS = {
    "minimum_trust_score": 0.8,
    "session_risk_threshold": 0.6,
    "token_ttl_minutes": 60,
    "privileged_access_ttl_minutes": 30,
    "step_up_threshold": 0.7,
    "retention_days": 365,
    "maximum_failed_policy_checks": 3,
    "privileged_access_approval_count": 2,
    "credential_confidence_threshold": 0.9,
    "workbench_limit": 100,
}
_DEFAULT_RULES = (
    {
        "rule_id": "seed_rule_access_default",
        "tenant": "tenant_seed_alpha",
        "rule_type": "access",
        "scope": "tenant_boundary",
        "allowed_regions": ("US",),
        "allowed_roles": ("tenant_admin", "security_auditor", "service_bot"),
        "required_claims": ("email", "tenant"),
        "deny_actions": ("delete_tenant",),
        "privileged_actions": ("rotate_key", "approve_break_glass"),
        "status": "active",
    },
    {
        "rule_id": "seed_rule_break_glass",
        "tenant": "tenant_seed_alpha",
        "rule_type": "privileged_access",
        "scope": "break_glass",
        "allowed_regions": ("US",),
        "allowed_roles": ("security_auditor",),
        "required_claims": ("email", "tenant"),
        "deny_actions": (),
        "privileged_actions": ("rotate_key", "approve_break_glass"),
        "status": "active",
    },
)
SEED_DATA = (
    {
        "table": "federated_iam_tenant",
        "rows": (
            {"code": "TENANT-ALPHA", "status": "active", "tenant_id": "tenant_seed_alpha", "name": "Seed Alpha", "region": "US"},
        ),
    },
    {
        "table": "federated_iam_principal",
        "rows": (
            {"code": "PRINCIPAL-ALICE", "status": "active", "tenant": "tenant_seed_alpha", "principal_id": "principal_seed_alice"},
            {"code": "PRINCIPAL-BOT", "status": "active", "tenant": "tenant_seed_alpha", "principal_id": "principal_seed_service_bot"},
        ),
    },
    {
        "table": "federated_iam_identity_provider",
        "rows": (
            {"code": "PROVIDER-CORP", "status": "active", "tenant": "tenant_seed_alpha", "provider_id": "provider_seed_corp"},
        ),
    },
    {
        "table": "federated_iam_iam_rule",
        "rows": tuple({"code": rule["rule_id"], "status": rule["status"], "tenant": rule["tenant"]} for rule in _DEFAULT_RULES),
    },
    {
        "table": "federated_iam_iam_parameter",
        "rows": tuple(
            {"code": key.upper(), "status": "active", "parameter_name": key, "parameter_value": value}
            for key, value in _DEFAULT_PARAMETERS.items()
        ),
    },
)


def default_runtime_configuration() -> dict:
    """Return the default standalone runtime configuration."""
    return dict(_DEFAULT_CONFIGURATION)


def default_parameter_values() -> dict:
    """Return the default standalone parameter set."""
    return dict(_DEFAULT_PARAMETERS)


def default_rules() -> tuple[dict, ...]:
    """Return the default standalone rule catalog."""
    return tuple(dict(rule) for rule in _DEFAULT_RULES)


def seed_plan() -> dict:
    """Return deterministic standalone seed rows without applying them."""
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "configuration": default_runtime_configuration(),
        "parameters": default_parameter_values(),
        "rules": default_rules(),
        "tables": tuple(dict.fromkeys(item["table"] for item in SEED_DATA)),
        "rows": SEED_DATA,
        "workflow_starters": (
            "tenant_onboarding",
            "provider_linking",
            "credential_verification",
            "access_review",
            "privileged_access_approval",
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    """Validate seed ownership and minimum row shape."""
    plan = seed_plan()
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code") or not row.get("status")
    )
    missing_seed_tenants = tuple(
        row.get("tenant")
        for item in SEED_DATA
        for row in item.get("rows", ())
        if row.get("tenant") and row.get("tenant") != "tenant_seed_alpha"
    )
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_rows and not missing_seed_tenants,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "missing_seed_tenants": missing_seed_tenants,
        "side_effects": (),
    }


def build_seed_state() -> dict:
    """Build a deterministic standalone runtime state from package-local seeds."""
    state = federated_iam_empty_state()
    configured = federated_iam_configure_runtime(state, default_runtime_configuration())
    state = configured["state"]
    for key, value in default_parameter_values().items():
        state = federated_iam_set_parameter(state, key, value)["state"]
    for rule in default_rules():
        state = federated_iam_register_rule(state, rule)["state"]
    state = federated_iam_provision_tenant(
        state,
        {"tenant_id": "tenant_seed_alpha", "name": "Seed Alpha", "region": "US", "status": "active"},
    )["state"]
    state = federated_iam_register_principal(
        state,
        {
            "tenant": "tenant_seed_alpha",
            "principal_id": "principal_seed_alice",
            "principal_type": "user",
            "display_name": "Alice Seed",
            "status": "active",
        },
    )["state"]
    state = federated_iam_register_principal(
        state,
        {
            "tenant": "tenant_seed_alpha",
            "principal_id": "principal_seed_service_bot",
            "principal_type": "agent",
            "display_name": "Seed Service Bot",
            "status": "active",
        },
    )["state"]
    state = federated_iam_register_identity_provider(
        state,
        {
            "tenant": "tenant_seed_alpha",
            "provider_id": "provider_seed_corp",
            "provider_type": "oidc",
            "issuer": "https://login.seed.example",
            "status": "active",
        },
    )["state"]
    state = federated_iam_link_identity(
        state,
        {
            "tenant": "tenant_seed_alpha",
            "identity_id": "identity_seed_alice",
            "principal_id": "principal_seed_alice",
            "provider_id": "provider_seed_corp",
            "subject": "alice.seed",
            "claims": {"email": "alice.seed@example.com", "tenant": "tenant_seed_alpha"},
            "trust_score": 0.93,
        },
    )["state"]
    state = federated_iam_verify_credential(
        state,
        {
            "tenant": "tenant_seed_alpha",
            "verification_id": "verify_seed_alice",
            "principal_id": "principal_seed_alice",
            "credential_type": "did_vc",
            "issuer": "trusted_registry",
            "status": "active",
            "confidence": 0.95,
        },
    )["state"]
    state = federated_iam_assign_role(
        state,
        {
            "tenant": "tenant_seed_alpha",
            "assignment_id": "assignment_seed_admin",
            "principal_id": "principal_seed_alice",
            "role": "tenant_admin",
            "scope": "tenant_seed_alpha",
            "status": "active",
        },
    )["state"]
    state = federated_iam_evaluate_policy(
        state,
        {
            "tenant": "tenant_seed_alpha",
            "decision_id": "decision_seed_publish",
            "principal_id": "principal_seed_alice",
            "action": "publish_product",
            "resource": "tenant_seed_alpha",
            "context": {"region": "US", "risk": 0.2},
        },
    )["state"]
    state = federated_iam_grant_token(
        state,
        {
            "tenant": "tenant_seed_alpha",
            "grant_id": "grant_seed_publish",
            "principal_id": "principal_seed_alice",
            "grant_type": "authorization_code",
            "audience": "tenant_seed_alpha",
            "scopes": ("tenant_seed_alpha.read", "tenant_seed_alpha.publish"),
        },
    )["state"]
    state = federated_iam_approve_privileged_access(
        state,
        {
            "tenant": "tenant_seed_alpha",
            "request_id": "priv_seed_rotate",
            "principal_id": "principal_seed_alice",
            "action": "rotate_key",
            "resource": "tenant_seed_alpha",
            "risk": 0.3,
            "approved_by": "security_seed_reviewer",
        },
    )["state"]
    state = federated_iam_receive_event(
        state,
        {
            "event_id": "seed-role-change-1",
            "event_type": "RoleChanged",
            "payload": {"tenant": "tenant_seed_alpha", "role_id": "tenant_admin", "role": "tenant_admin"},
        },
    )["state"]
    workbench = federated_iam_build_workbench_view(state, tenant="tenant_seed_alpha")
    return {
        "ok": workbench["ok"] and workbench["principal_count"] >= 2,
        "pbc": PBC_KEY,
        "state": state,
        "workbench": workbench,
        "summary": {
            "tenant_count": len(state["tenants"]),
            "principal_count": len(state["principals"]),
            "provider_count": len(state["providers"]),
            "rule_count": len(state["rules"]),
            "parameter_count": len(state["parameters"]),
            "outbox_count": len(state["outbox"]),
        },
        "side_effects": (),
    }


def standalone_install_plan() -> dict:
    """Return a package-local install and bootstrap plan for one-PBC deployments."""
    seeds = seed_plan()
    return {
        "ok": seeds["ok"],
        "pbc": PBC_KEY,
        "steps": (
            "apply migrations/001_initial.sql",
            "configure AppGen-X event topic and relational backend",
            "load parameters and rules",
            "load deterministic tenant/principal/provider seeds",
            "expose workbench, API routes, and chatbot surface",
        ),
        "seed_tables": seeds["tables"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise seed validation and deterministic standalone bootstrap."""
    validation = validate_seed_data()
    seeded = build_seed_state()
    install = standalone_install_plan()
    return {
        "ok": validation["ok"] and seeded["ok"] and install["ok"],
        "validation": validation,
        "seeded": seeded,
        "install": install,
        "side_effects": (),
    }
