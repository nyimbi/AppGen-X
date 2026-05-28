"""Executable RBAC contract for the clinical_trials_management PBC."""

from __future__ import annotations

from .runtime import clinical_trials_management_permissions_contract


PBC_KEY = "clinical_trials_management"
_RUNTIME_PERMISSIONS = clinical_trials_management_permissions_contract()
PERMISSIONS = tuple(_RUNTIME_PERMISSIONS["permissions"])
ACTION_PERMISSIONS = dict(_RUNTIME_PERMISSIONS["action_permissions"])
ROLE_BINDINGS = dict(_RUNTIME_PERMISSIONS["roles"])


def permission_manifest() -> dict:
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS) and bool(ROLE_BINDINGS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "roles": dict(ROLE_BINDINGS),
        "side_effects": (),
    }


def expand_roles(roles: tuple[str, ...] = ()) -> tuple[str, ...]:
    permissions = []
    for role in roles:
        permissions.extend(ROLE_BINDINGS.get(role, ()))
    return tuple(dict.fromkeys(permissions))


def authorize(action: str, granted_permissions: tuple[str, ...] = (), roles: tuple[str, ...] = ()) -> dict:
    required = ACTION_PERMISSIONS.get(action)
    effective_permissions = set(granted_permissions) | set(expand_roles(roles))
    allowed = required in effective_permissions if required else False
    return {
        "ok": required is not None,
        "allowed": allowed,
        "action": action,
        "required_permission": required,
        "granted_permissions": tuple(sorted(effective_permissions)),
        "roles": tuple(roles),
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = permission_manifest()
    decision = authorize("command_subjects", roles=("clinical_trial_coordinator",))
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }
