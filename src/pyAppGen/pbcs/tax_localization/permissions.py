"""Executable RBAC contract for the tax_localization PBC."""

from __future__ import annotations


PBC_KEY = "tax_localization"
PERMISSIONS = (
    "tax_localization.read",
    "tax_localization.jurisdiction",
    "tax_localization.rule_admin",
    "tax_localization.calculate",
    "tax_localization.invoice",
    "tax_localization.file",
    "tax_localization.exemption",
    "tax_localization.reconcile",
    "tax_localization.event",
    "tax_localization.configure",
    "tax_localization.audit",
)
ACTION_PERMISSIONS = {
    "register_jurisdiction": "tax_localization.jurisdiction",
    "register_tax_rule": "tax_localization.rule_admin",
    "calculate_tax_quote": "tax_localization.calculate",
    "record_invoice_tax": "tax_localization.invoice",
    "prepare_tax_filing": "tax_localization.file",
    "validate_exemption_certificate": "tax_localization.exemption",
    "reconcile_tax_collected": "tax_localization.reconcile",
    "receive_event": "tax_localization.event",
    "configure_runtime": "tax_localization.configure",
    "set_parameter": "tax_localization.configure",
    "register_rule": "tax_localization.configure",
    "register_schema_extension": "tax_localization.configure",
    "run_control_tests": "tax_localization.audit",
    "build_workbench_view": "tax_localization.audit",
    "assistant_preview": "tax_localization.audit",
}
ROLE_PERMISSIONS = {
    "tax_analyst": ("tax_localization.read", "tax_localization.calculate", "tax_localization.exemption"),
    "tax_manager": (
        "tax_localization.read",
        "tax_localization.jurisdiction",
        "tax_localization.rule_admin",
        "tax_localization.calculate",
        "tax_localization.invoice",
        "tax_localization.file",
        "tax_localization.exemption",
        "tax_localization.reconcile",
        "tax_localization.audit",
    ),
    "tax_controller": PERMISSIONS,
    "tax_admin": PERMISSIONS,
}


def permission_manifest() -> dict:
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "roles": dict(ROLE_PERMISSIONS),
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
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


def role_permissions(role: str) -> dict:
    permissions = ROLE_PERMISSIONS.get(role)
    return {
        "ok": permissions is not None,
        "role": role,
        "permissions": tuple(permissions or ()),
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = permission_manifest()
    manager = role_permissions("tax_manager")
    decision = authorize("prepare_tax_filing", manager["permissions"])
    return {
        "ok": manifest["ok"] and manager["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "manager": manager,
        "decision": decision,
        "side_effects": (),
    }
