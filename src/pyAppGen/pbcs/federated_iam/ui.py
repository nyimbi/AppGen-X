"""UI contract for the Federated IAM PBC."""

from __future__ import annotations

from .runtime import FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
from .runtime import FEDERATED_IAM_CONSUMED_EVENT_TYPES
from .runtime import FEDERATED_IAM_EMITTED_EVENT_TYPES
from .runtime import FEDERATED_IAM_OWNED_TABLES
from .runtime import FEDERATED_IAM_REQUIRED_EVENT_TOPIC
from .runtime import FEDERATED_IAM_RUNTIME_TABLES
from .runtime import federated_iam_permissions_contract


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
        "action_permissions": federated_iam_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
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
            "emits": FEDERATED_IAM_EMITTED_EVENT_TYPES,
            "consumes": FEDERATED_IAM_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
            "event_contract": "AppGen-X",
            "required_event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
        },
        "binding_evidence": {
            "owned_tables": FEDERATED_IAM_OWNED_TABLES,
            "runtime_tables": FEDERATED_IAM_RUNTIME_TABLES,
            "outbox_table": FEDERATED_IAM_RUNTIME_TABLES[0],
            "inbox_table": FEDERATED_IAM_RUNTIME_TABLES[1],
            "dead_letter_table": FEDERATED_IAM_RUNTIME_TABLES[2],
            "required_event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "shared_table_access": False,
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
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": FEDERATED_IAM_OWNED_TABLES,
            "runtime_tables": FEDERATED_IAM_RUNTIME_TABLES,
            "outbox_table": FEDERATED_IAM_RUNTIME_TABLES[0],
            "inbox_table": FEDERATED_IAM_RUNTIME_TABLES[1],
            "dead_letter_table": FEDERATED_IAM_RUNTIME_TABLES[2],
            "rules": tuple(sorted(state["rules"])),
            "parameters": tuple(sorted(state["parameters"])),
            "configuration": {
                "event_contract": state["configuration"].get("event_contract"),
                "event_topic": state["configuration"].get("event_topic"),
                "stream_engine_picker_visible": state["configuration"].get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state["configuration"].get("user_selectable_event_contract"),
            },
            "ui_bindings": {
                "configuration_fragment": "IamConfigurationPanel",
                "rule_fragment": "IamRuleStudio",
                "parameter_fragment": "IamParameterConsole",
                "outbox_table": FEDERATED_IAM_RUNTIME_TABLES[0],
                "inbox_table": FEDERATED_IAM_RUNTIME_TABLES[1],
                "dead_letter_table": FEDERATED_IAM_RUNTIME_TABLES[2],
                "rbac": contract["action_permissions"],
            },
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = federated_iam_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = federated_iam_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
