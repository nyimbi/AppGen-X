"""Executable permission contract for the workflow_orchestration PBC."""

from __future__ import annotations

from .runtime import workflow_orchestration_permissions_contract as _runtime_permissions_contract


PBC_KEY = "workflow_orchestration"
ROLE_PERMISSIONS = {
    "workflow_orchestration_admin": (
        "workflow_orchestration.read",
        "workflow_orchestration.define",
        "workflow_orchestration.start",
        "workflow_orchestration.signal",
        "workflow_orchestration.compensate",
        "workflow_orchestration.event",
        "workflow_orchestration.configure",
        "workflow_orchestration.audit",
    ),
    "workflow_orchestration_operator": (
        "workflow_orchestration.read",
        "workflow_orchestration.start",
        "workflow_orchestration.signal",
        "workflow_orchestration.compensate",
        "workflow_orchestration.event",
    ),
    "workflow_orchestration_designer": (
        "workflow_orchestration.read",
        "workflow_orchestration.define",
        "workflow_orchestration.configure",
        "workflow_orchestration.audit",
    ),
    "workflow_orchestration_auditor": (
        "workflow_orchestration.read",
        "workflow_orchestration.audit",
    ),
}
ABAC_ATTRIBUTES = ("tenant", "workflow_id", "instance_id", "severity", "state", "assignee_group")


def permission_manifest() -> dict:
    """Return the permission surface without mutating runtime state."""
    runtime = _runtime_permissions_contract()
    return {
        "ok": runtime["ok"] and bool(ROLE_PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": runtime["permissions"],
        "action_permissions": dict(runtime["action_permissions"]),
        "roles": dict(ROLE_PERMISSIONS),
        "abac_attributes": ABAC_ATTRIBUTES,
        "policy_controls": ("shared_table_access_forbidden", "stream_engine_picker_hidden", "agent_mutation_preview_required"),
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = (), *, context: dict | None = None) -> dict:
    """Evaluate one action against a caller permission set."""
    manifest = permission_manifest()
    required = manifest["action_permissions"].get(action)
    supplied_context = dict(context or {})
    allowed = required in set(granted_permissions) if required else False
    context_gate = bool(supplied_context.get("tenant", True))
    return {
        "ok": required is not None,
        "allowed": allowed and context_gate,
        "action": action,
        "required_permission": required,
        "granted_permissions": tuple(granted_permissions),
        "context_gate": context_gate,
        "context": supplied_context,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one permission decision side-effect-free."""
    manifest = permission_manifest()
    action = "build_release_evidence"
    permission = manifest["action_permissions"][action]
    decision = authorize(action, (permission,), context={"tenant": "tenant_smoke"})
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }
