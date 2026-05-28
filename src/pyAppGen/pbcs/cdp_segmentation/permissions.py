"""Executable RBAC surface for the cdp_segmentation PBC."""

from __future__ import annotations

from .runtime import cdp_segmentation_permissions_contract


PBC_KEY = "cdp_segmentation"


def permission_manifest() -> dict:
    """Return package-local RBAC evidence aligned with runtime operations."""
    contract = cdp_segmentation_permissions_contract()
    permissions = tuple(contract["permissions"])
    return {
        "ok": contract["ok"] and bool(permissions),
        "pbc": PBC_KEY,
        "permissions": permissions,
        "action_permissions": dict(contract["action_permissions"]),
        "roles": {
            "segment_operator": (
                "cdp_segmentation.event.write",
                "cdp_segmentation.segment.write",
                "cdp_segmentation.membership.evaluate",
            ),
            "segmentation_analyst": (
                "cdp_segmentation.analytics.write",
                "cdp_segmentation.audit",
            ),
            "privacy_steward": (
                "cdp_segmentation.profile.govern",
                "cdp_segmentation.audit",
            ),
            "platform_admin": permissions,
        },
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
    """Evaluate whether a caller can execute one named package action."""
    manifest = permission_manifest()
    required = manifest["action_permissions"].get(action)
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
    """Exercise a representative governance decision."""
    manifest = permission_manifest()
    action = "screen_consent_policy"
    decision = authorize(action, ("cdp_segmentation.profile.govern",))
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }
