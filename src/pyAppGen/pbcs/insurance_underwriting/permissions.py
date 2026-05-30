"""Permission and authority contracts for insurance underwriting."""

from __future__ import annotations


PBC_KEY = "insurance_underwriting"
PERMISSIONS = (
    "insurance_underwriting.read",
    "insurance_underwriting.submission.write",
    "insurance_underwriting.quote.write",
    "insurance_underwriting.decision.approve",
    "insurance_underwriting.bind.approve",
    "insurance_underwriting.admin",
)
ACTION_PERMISSIONS = {
    "create_submission": "insurance_underwriting.submission.write",
    "build_risk_profile": "insurance_underwriting.submission.write",
    "review_rating_factor": "insurance_underwriting.quote.write",
    "generate_quote": "insurance_underwriting.quote.write",
    "issue_underwriting_decision": "insurance_underwriting.decision.approve",
    "assemble_bind_package": "insurance_underwriting.bind.approve",
    "view_workbench": "insurance_underwriting.read",
}
AUTHORITY_LIMITS = {
    "junior": 500000.0,
    "senior": 2500000.0,
    "chief": 10000000.0,
}


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": {
            "operator": (
                "insurance_underwriting.read",
                "insurance_underwriting.submission.write",
                "insurance_underwriting.quote.write",
            ),
            "approver": (
                "insurance_underwriting.read",
                "insurance_underwriting.quote.write",
                "insurance_underwriting.decision.approve",
                "insurance_underwriting.bind.approve",
            ),
            "admin": PERMISSIONS,
        },
        "action_permissions": ACTION_PERMISSIONS,
        "authority_limits": AUTHORITY_LIMITS,
        "side_effects": (),
    }


def authorize(permission: str, actor: dict | None = None, context: dict | None = None) -> dict:
    actor = dict(actor or {})
    context = dict(context or {})
    roles = permission_manifest()["roles"]
    granted = set(actor.get("permissions", ()))
    for role in actor.get("roles", ()):
        granted.update(roles.get(role, ()))
    allowed = permission in granted or actor.get("is_admin") is True
    if permission == "insurance_underwriting.decision.approve":
        authority_level = actor.get("authority_level", "junior")
        allowed = allowed and float(context.get("requested_limit", 0.0)) <= AUTHORITY_LIMITS.get(
            authority_level,
            0.0,
        )
    return {
        "ok": allowed,
        "permission": permission,
        "actor": actor,
        "context": context,
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = permission_manifest()
    operator = authorize(
        "insurance_underwriting.submission.write",
        {"roles": ("operator",)},
    )
    approval_denied = authorize(
        "insurance_underwriting.decision.approve",
        {"roles": ("approver",), "authority_level": "junior"},
        {"requested_limit": 1000000.0},
    )
    approval_granted = authorize(
        "insurance_underwriting.decision.approve",
        {"roles": ("approver",), "authority_level": "senior"},
        {"requested_limit": 1000000.0},
    )
    return {
        "ok": manifest["ok"] and operator["ok"] and not approval_denied["ok"] and approval_granted["ok"],
        "manifest": manifest,
        "side_effects": (),
    }
