"""Permission descriptors for the enterprise_risk_controls PBC."""

PBC_KEY = "enterprise_risk_controls"
PERMISSIONS = (
    "enterprise_risk_controls.read",
    "enterprise_risk_controls.register_risk",
    "enterprise_risk_controls.assess_risk",
    "enterprise_risk_controls.manage_controls",
    "enterprise_risk_controls.attest_controls",
    "enterprise_risk_controls.manage_remediation",
    "enterprise_risk_controls.compile_assurance",
    "enterprise_risk_controls.configure",
    "enterprise_risk_controls.audit",
    "enterprise_risk_controls.admin",
)
ROLE_BINDINGS = {
    "reader": ("enterprise_risk_controls.read",),
    "risk_analyst": (
        "enterprise_risk_controls.read",
        "enterprise_risk_controls.register_risk",
        "enterprise_risk_controls.assess_risk",
        "enterprise_risk_controls.audit",
    ),
    "control_operator": (
        "enterprise_risk_controls.read",
        "enterprise_risk_controls.manage_controls",
        "enterprise_risk_controls.attest_controls",
        "enterprise_risk_controls.audit",
    ),
    "remediation_lead": (
        "enterprise_risk_controls.read",
        "enterprise_risk_controls.manage_remediation",
        "enterprise_risk_controls.audit",
    ),
    "assurance_lead": (
        "enterprise_risk_controls.read",
        "enterprise_risk_controls.compile_assurance",
        "enterprise_risk_controls.audit",
        "enterprise_risk_controls.configure",
    ),
    "admin": PERMISSIONS,
}
ACTION_PERMISSIONS = {
    "register_risk": "enterprise_risk_controls.register_risk",
    "assess_inherent_risk": "enterprise_risk_controls.assess_risk",
    "define_control": "enterprise_risk_controls.manage_controls",
    "schedule_control_test": "enterprise_risk_controls.manage_controls",
    "record_attestation": "enterprise_risk_controls.attest_controls",
    "open_remediation": "enterprise_risk_controls.manage_remediation",
    "generate_assurance_packet": "enterprise_risk_controls.compile_assurance",
    "query_enterprise_risk_controls_workbench": "enterprise_risk_controls.read",
    "query_enterprise_risk_controls_controls": "enterprise_risk_controls.audit",
    "query_enterprise_risk_controls_assistant_preview": "enterprise_risk_controls.audit",
    "review_rules": "enterprise_risk_controls.configure",
    "review_parameters": "enterprise_risk_controls.configure",
    "review_release_evidence": "enterprise_risk_controls.audit",
}


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "rbac_roles": tuple(ROLE_BINDINGS),
        "role_bindings": ROLE_BINDINGS,
        "action_permissions": ACTION_PERMISSIONS,
        "side_effects": (),
    }


def authorize(actor, permission, actor_permissions=None):
    assigned = set(actor_permissions or PERMISSIONS)
    allowed = permission in assigned and permission in PERMISSIONS
    return {
        "ok": allowed,
        "allowed": allowed,
        "actor": actor,
        "permission": permission,
        "side_effects": (),
    }


def smoke_test():
    manifest = permission_manifest()
    return {
        "ok": manifest["ok"] and authorize("system", PERMISSIONS[0])["allowed"],
        "manifest": manifest,
        "side_effects": (),
    }
