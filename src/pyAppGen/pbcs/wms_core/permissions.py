"""Executable permission contract for the wms_core PBC."""

from __future__ import annotations


PBC_KEY = "wms_core"
PERMISSIONS = (
    "wms_core.read",
    "wms_core.master",
    "wms_core.receive",
    "wms_core.putaway",
    "wms_core.pick",
    "wms_core.pack",
    "wms_core.ship",
    "wms_core.count",
    "wms_core.edge",
    "wms_core.event",
    "wms_core.configure",
    "wms_core.audit",
)
ACTION_PERMISSIONS = {
    "register_warehouse": "wms_core.master",
    "register_bin": "wms_core.master",
    "receive_inbound": "wms_core.receive",
    "create_putaway_task": "wms_core.putaway",
    "confirm_putaway": "wms_core.putaway",
    "create_pick_wave": "wms_core.pick",
    "execute_pick": "wms_core.pick",
    "create_pack_task": "wms_core.pack",
    "confirm_pack": "wms_core.pack",
    "confirm_shipment": "wms_core.ship",
    "route_edge_command": "wms_core.edge",
    "receive_event": "wms_core.event",
    "register_rule": "wms_core.configure",
    "register_schema_extension": "wms_core.configure",
    "set_parameter": "wms_core.configure",
    "configure_runtime": "wms_core.configure",
    "generate_shipment_proof": "wms_core.audit",
    "run_control_tests": "wms_core.audit",
    "build_workbench_view": "wms_core.audit",
}


def permission_manifest() -> dict:
    """Return the permission surface without mutating runtime state."""
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
    """Evaluate one action against a caller permission set."""
    required = ACTION_PERMISSIONS.get(action)
    allowed = required in set(granted_permissions) if required else False
    return {
        "ok": required is not None,
        "allowed": allowed,
        "action": action,
        "required_permission": required,
        "granted_permissions": tuple(granted_permissions),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one permission decision side-effect-free."""
    manifest = permission_manifest()
    action = "confirm_shipment"
    decision = authorize(action, ("wms_core.ship",))
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }
