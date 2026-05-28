"""Executable RBAC contract for the checkout_processing PBC."""

from __future__ import annotations

from .runtime import checkout_processing_permissions_contract


PBC_KEY = "checkout_processing"
_RUNTIME_PERMISSIONS = checkout_processing_permissions_contract()
PERMISSIONS = tuple(_RUNTIME_PERMISSIONS["permissions"])
ACTION_PERMISSIONS = {
    **dict(_RUNTIME_PERMISSIONS["action_permissions"]),
    "query_checkout_processing_workbench": "checkout_processing.audit",
    "query_checkout_processing_controls": "checkout_processing.audit",
    "query_checkout_processing_assistant_preview": "checkout_processing.audit",
}
ROLE_BINDINGS = {
    "checkout_operator": (
        "checkout_processing.cart",
        "checkout_processing.checkout",
        "checkout_processing.promotion",
    ),
    "inventory_operator": (
        "checkout_processing.inventory",
        "checkout_processing.audit",
    ),
    "payment_operator": (
        "checkout_processing.payment",
        "checkout_processing.audit",
    ),
    "risk_analyst": (
        "checkout_processing.risk",
        "checkout_processing.audit",
    ),
    "release_manager": (
        "checkout_processing.configure",
        "checkout_processing.audit",
    ),
    "checkout_admin": PERMISSIONS,
}


def permission_manifest() -> dict:
    """Return the role and action permission surface."""
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS) and bool(ROLE_BINDINGS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "roles": dict(ROLE_BINDINGS),
        "side_effects": (),
    }


def expand_roles(roles: tuple[str, ...] = ()) -> tuple[str, ...]:
    """Expand one or more roles into permissions."""
    permissions = []
    for role in roles:
        permissions.extend(ROLE_BINDINGS.get(role, ()))
    return tuple(dict.fromkeys(permissions))


def authorize(action: str, granted_permissions: tuple[str, ...] = (), roles: tuple[str, ...] = ()) -> dict:
    """Evaluate one action against explicit permissions and optional roles."""
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
    """Exercise one role-based permission decision."""
    manifest = permission_manifest()
    decision = authorize("complete_checkout", roles=("checkout_operator",))
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }
