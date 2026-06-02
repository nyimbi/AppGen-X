"""Permissions and RBAC contracts for provider_revenue_cycle."""

from __future__ import annotations

PBC_KEY = "provider_revenue_cycle"
PERMISSIONS = (
    "provider_revenue_cycle.read",
    "provider_revenue_cycle.create",
    "provider_revenue_cycle.update",
    "provider_revenue_cycle.approve",
    "provider_revenue_cycle.admin",
)
ACTION_PERMISSIONS = {
    "view_workbench": "provider_revenue_cycle.read",
    "intake_patient_account": "provider_revenue_cycle.create",
    "review_eligibility": "provider_revenue_cycle.update",
    "link_prior_authorization": "provider_revenue_cycle.update",
    "capture_charge": "provider_revenue_cycle.update",
    "review_coding": "provider_revenue_cycle.update",
    "edit_payer_contract": "provider_revenue_cycle.admin",
    "create_or_scrub_claim": "provider_revenue_cycle.update",
    "submit_claim": "provider_revenue_cycle.approve",
    "post_remit_era": "provider_revenue_cycle.update",
    "work_denial_appeal": "provider_revenue_cycle.approve",
    "resolve_patient_balance": "provider_revenue_cycle.update",
    "approve_assistance_or_refund": "provider_revenue_cycle.approve",
    "reconcile_close": "provider_revenue_cycle.approve",
    "configure_controls": "provider_revenue_cycle.admin",
    "assistant_preview": "provider_revenue_cycle.read",
}
ROLES = {
    "operator": (
        "provider_revenue_cycle.read",
        "provider_revenue_cycle.create",
        "provider_revenue_cycle.update",
    ),
    "supervisor": (
        "provider_revenue_cycle.read",
        "provider_revenue_cycle.create",
        "provider_revenue_cycle.update",
        "provider_revenue_cycle.approve",
    ),
    "auditor": (
        "provider_revenue_cycle.read",
        "provider_revenue_cycle.admin",
    ),
    "administrator": PERMISSIONS,
}


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLES),
        "role_bindings": ROLES,
        "action_permissions": ACTION_PERMISSIONS,
        "side_effects": (),
    }


def authorize(permission: str, actor: dict | None = None) -> dict:
    supplied = dict(actor or {})
    granted = set(supplied.get("permissions", ()))
    if not granted and supplied.get("role") in ROLES:
        granted = set(ROLES[supplied["role"]])
    allowed = permission in PERMISSIONS and (not granted or permission in granted)
    return {
        "ok": allowed,
        "permission": permission,
        "actor": supplied,
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = permission_manifest()
    return {
        "ok": manifest["ok"]
        and authorize("provider_revenue_cycle.read", {"role": "operator"})["ok"]
        and authorize("provider_revenue_cycle.admin", {"role": "operator"})["ok"] is False,
        "side_effects": (),
    }
