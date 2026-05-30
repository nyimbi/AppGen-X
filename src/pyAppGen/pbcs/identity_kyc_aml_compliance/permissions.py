"""Permission matrix for the identity KYC / AML slice."""

from __future__ import annotations

PBC_KEY = "identity_kyc_aml_compliance"
PERMISSIONS = (
    "identity_kyc_aml_compliance.read",
    "identity_kyc_aml_compliance.create",
    "identity_kyc_aml_compliance.update",
    "identity_kyc_aml_compliance.approve",
    "identity_kyc_aml_compliance.admin",
    "identity_kyc_aml_compliance.operate",
)
ROLE_GRANTS = {
    "analyst": {"identity_kyc_aml_compliance.read", "identity_kyc_aml_compliance.create", "identity_kyc_aml_compliance.update", "identity_kyc_aml_compliance.operate"},
    "investigator": {"identity_kyc_aml_compliance.read", "identity_kyc_aml_compliance.update", "identity_kyc_aml_compliance.operate"},
    "approver": {"identity_kyc_aml_compliance.read", "identity_kyc_aml_compliance.update", "identity_kyc_aml_compliance.approve", "identity_kyc_aml_compliance.operate"},
    "auditor": {"identity_kyc_aml_compliance.read"},
    "admin": set(PERMISSIONS),
}


def permission_manifest():
    return {"ok": True, "pbc": PBC_KEY, "permissions": PERMISSIONS, "roles": tuple(ROLE_GRANTS), "side_effects": ()}


def authorize(permission, actor=None):
    actor = dict(actor or {})
    roles = tuple(actor.get("roles", ()))
    granted = any(permission in ROLE_GRANTS.get(role, set()) for role in roles)
    return {"ok": permission in PERMISSIONS and granted, "permission": permission, "actor": actor, "side_effects": ()}


def smoke_test():
    return {"ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0], {"roles": ("analyst",)})["ok"], "side_effects": ()}
