"""Executable permission contract for the inventory_positioning PBC."""

from __future__ import annotations


PBC_KEY = "inventory_positioning"
PERMISSIONS = (
    "inventory_positioning.read",
    "inventory_positioning.master",
    "inventory_positioning.receive",
    "inventory_positioning.adjust",
    "inventory_positioning.allocate",
    "inventory_positioning.release",
    "inventory_positioning.quality",
    "inventory_positioning.replenish",
    "inventory_positioning.reconcile",
    "inventory_positioning.event",
    "inventory_positioning.configure",
    "inventory_positioning.audit",
)
ACTION_PERMISSIONS = {
    "register_item": "inventory_positioning.master",
    "register_node": "inventory_positioning.master",
    "post_goods_receipt": "inventory_positioning.receive",
    "post_adjustment": "inventory_positioning.adjust",
    "calculate_availability": "inventory_positioning.read",
    "allocate_inventory": "inventory_positioning.allocate",
    "release_allocation": "inventory_positioning.release",
    "apply_quality_hold": "inventory_positioning.quality",
    "generate_replenishment_signal": "inventory_positioning.replenish",
    "reconcile_inventory": "inventory_positioning.reconcile",
    "receive_event": "inventory_positioning.event",
    "register_rule": "inventory_positioning.configure",
    "register_schema_extension": "inventory_positioning.configure",
    "set_parameter": "inventory_positioning.configure",
    "configure_runtime": "inventory_positioning.configure",
    "build_workbench_view": "inventory_positioning.audit",
    "run_control_tests": "inventory_positioning.audit",
    "generate_stock_proof": "inventory_positioning.audit",
}
ROLE_BINDINGS = {
    "inventory_analyst": ("inventory_positioning.read", "inventory_positioning.audit"),
    "inventory_controller": (
        "inventory_positioning.read",
        "inventory_positioning.receive",
        "inventory_positioning.adjust",
        "inventory_positioning.quality",
        "inventory_positioning.audit",
    ),
    "inventory_planner": (
        "inventory_positioning.read",
        "inventory_positioning.allocate",
        "inventory_positioning.release",
        "inventory_positioning.replenish",
        "inventory_positioning.reconcile",
    ),
    "inventory_admin": PERMISSIONS,
}


def permission_manifest() -> dict:
    """Return the permission surface without mutating runtime state."""
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "role_bindings": {role: tuple(perms) for role, perms in ROLE_BINDINGS.items()},
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
    """Evaluate one action against a caller permission set."""
    required = ACTION_PERMISSIONS.get(action)
    granted = set(granted_permissions)
    allowed = required in granted if required else False
    return {
        "ok": required is not None,
        "allowed": allowed,
        "action": action,
        "required_permission": required,
        "granted_permissions": tuple(granted_permissions),
        "side_effects": (),
    }


def permissions_for_role(role: str) -> dict:
    """Return the static permission bundle for one inventory role."""
    permissions = ROLE_BINDINGS.get(role, ())
    return {
        "ok": role in ROLE_BINDINGS,
        "role": role,
        "permissions": tuple(permissions),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise permission manifest and one allow decision side-effect-free."""
    manifest = permission_manifest()
    decision = authorize("register_item", ROLE_BINDINGS["inventory_admin"])
    role = permissions_for_role("inventory_controller")
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"] and role["ok"],
        "manifest": manifest,
        "decision": decision,
        "role": role,
        "side_effects": (),
    }
