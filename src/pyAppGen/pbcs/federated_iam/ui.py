"""UI contract for the Federated IAM PBC."""

from __future__ import annotations


FEDERATED_IAM_UI_FRAGMENT_KEYS = (
    "FederatedIamWorkbench",
    "TenantRegistry",
    "PrincipalRegistry",
    "IdentityProviderConsole",
    "CredentialVerificationPanel",
    "RoleAssignmentBoard",
    "PolicyDecisionWorkbench",
    "TokenGrantConsole",
    "PrivilegedAccessReview",
    "IdentityAuditDashboard",
    "IamRuleStudio",
    "IamParameterConsole",
    "IamConfigurationPanel",
)


def federated_iam_ui_contract() -> dict:
    return {
        "format": "appgen.federated-iam-ui-contract.v1",
        "ok": True,
        "pbc": "federated_iam",
        "implementation_directory": "src/pyAppGen/pbcs/federated_iam",
        "fragments": FEDERATED_IAM_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/federated_iam",
            "/workbench/pbcs/federated_iam/tenants",
            "/workbench/pbcs/federated_iam/principals",
            "/workbench/pbcs/federated_iam/providers",
            "/workbench/pbcs/federated_iam/credentials",
            "/workbench/pbcs/federated_iam/roles",
            "/workbench/pbcs/federated_iam/policies",
            "/workbench/pbcs/federated_iam/tokens",
            "/workbench/pbcs/federated_iam/privileged-access",
            "/workbench/pbcs/federated_iam/audit",
            "/workbench/pbcs/federated_iam/rules",
            "/workbench/pbcs/federated_iam/parameters",
            "/workbench/pbcs/federated_iam/configuration",
        ),
        "panels": (
            {
                "key": "identity_registry",
                "fragment": "PrincipalRegistry",
                "binds_to": ("tenant", "principal", "identity_provider", "principal_identity"),
                "commands": ("provision_tenant", "register_principal", "register_identity_provider", "link_identity"),
            },
            {
                "key": "access_control",
                "fragment": "PolicyDecisionWorkbench",
                "binds_to": ("role_assignment", "access_policy", "policy_decision", "token_grant"),
                "commands": ("assign_role", "evaluate_policy", "grant_token"),
            },
            {
                "key": "privileged_access",
                "fragment": "PrivilegedAccessReview",
                "binds_to": ("credential_verification", "privileged_access_request", "outbox"),
                "commands": ("verify_credential", "approve_privileged_access", "run_control_tests"),
            },
            {
                "key": "governance_studio",
                "fragment": "IamRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
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
            "register_rule": "federated_iam.configure",
            "set_parameter": "federated_iam.configure",
            "configure_runtime": "federated_iam.configure",
            "run_control_tests": "federated_iam.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "minimum_trust_score",
                "session_risk_threshold",
                "token_ttl_minutes",
                "privileged_access_ttl_minutes",
                "step_up_threshold",
                "retention_days",
            ),
        },
        "rule_editor": {
            "rule_types": ("access", "tenant", "identity", "token", "privileged_access", "segregation_of_duties"),
            "required_fields": ("rule_id", "tenant", "rule_type", "allowed_regions", "allowed_roles", "status"),
        },
        "event_surfaces": {
            "emits": ("TenantProvisioned", "PrincipalVerified", "AccessPolicyChanged", "PolicyDecisionRecorded", "TokenGranted", "PrivilegedAccessApproved"),
            "consumes": ("RoleChanged", "TenantProvisioned", "CustomerUpdated", "EmployeeProvisioned", "ServiceAccountRequested"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def federated_iam_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = federated_iam_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, required_permission in action_permissions.items() if required_permission in permissions)
    principals = tuple(item for item in state["principals"].values() if item["tenant"] == tenant)
    providers = tuple(item for item in state["providers"].values() if item["tenant"] == tenant)
    decisions = tuple(item for item in state["decisions"].values() if item["tenant"] == tenant)
    tokens = tuple(item for item in state["tokens"].values() if item["tenant"] == tenant)
    privileged = tuple(item for item in state["privileged"].values() if item["tenant"] == tenant)
    cards = (
        {"key": "principals", "value": len(principals), "fragment": "PrincipalRegistry"},
        {"key": "providers", "value": len(providers), "fragment": "IdentityProviderConsole"},
        {"key": "policy_decisions", "value": len(decisions), "fragment": "PolicyDecisionWorkbench"},
        {"key": "token_grants", "value": len(tokens), "fragment": "TokenGrantConsole"},
        {"key": "privileged_access", "value": len(privileged), "fragment": "PrivilegedAccessReview"},
        {"key": "outbox", "value": len(state["outbox"]), "fragment": "IdentityAuditDashboard"},
    )
    return {
        "format": "appgen.federated-iam-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/federated_iam",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
    }
