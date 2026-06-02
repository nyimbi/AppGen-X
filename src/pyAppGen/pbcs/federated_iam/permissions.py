"""Executable permission contract for the federated_iam PBC."""

from __future__ import annotations

from .runtime import federated_iam_permissions_contract


PBC_KEY = "federated_iam"
_PERMISSION_GROUPS = {
    "registry": ("federated_iam.read", "federated_iam.tenant", "federated_iam.principal"),
    "policy": ("federated_iam.policy", "federated_iam.token", "federated_iam.privileged"),
    "governance": ("federated_iam.event", "federated_iam.configure", "federated_iam.audit"),
}


def permission_manifest() -> dict:
    """Return the PBC permission surface plus grouped operating lanes."""
    contract = federated_iam_permissions_contract()
    return {
        **contract,
        "pbc": PBC_KEY,
        "permission_groups": _PERMISSION_GROUPS,
        "group_names": tuple(_PERMISSION_GROUPS),
        "side_effects": (),
    }


def resolve_required_permission(action: str) -> str | None:
    """Return the permission required for one named action or operation."""
    return permission_manifest()["action_permissions"].get(action)


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
    """Evaluate one action or service operation against the caller grants."""
    manifest = permission_manifest()
    required = manifest["action_permissions"].get(action)
    granted = tuple(granted_permissions)
    return {
        "ok": required is not None,
        "allowed": required in set(granted) if required else False,
        "action": action,
        "required_permission": required,
        "granted_permissions": granted,
        "permission_groups": tuple(
            group
            for group, permissions in manifest["permission_groups"].items()
            if required in permissions
        ),
        "side_effects": (),
    }


def access_profile(granted_permissions: tuple[str, ...] = ()) -> dict:
    """Return a UI-friendly summary of the caller's allowed lanes."""
    manifest = permission_manifest()
    granted = set(granted_permissions)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "granted_permissions": tuple(sorted(granted)),
        "allowed_groups": tuple(
            group
            for group, permissions in manifest["permission_groups"].items()
            if granted.intersection(permissions)
        ),
        "allowed_actions": tuple(
            action
            for action, permission in manifest["action_permissions"].items()
            if permission in granted
        ),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise permission lookup, authorization, and grouped access summary."""
    manifest = permission_manifest()
    action = "grant_token"
    required = resolve_required_permission(action)
    decision = authorize(action, (required,) if required else ())
    profile = access_profile((required,) if required else ())
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"] and profile["ok"],
        "manifest": manifest,
        "decision": decision,
        "profile": profile,
        "side_effects": (),
    }
