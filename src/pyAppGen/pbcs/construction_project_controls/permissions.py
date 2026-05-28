"""RBAC and approval routing for construction project controls."""
from __future__ import annotations

PBC_KEY = "construction_project_controls"
PERMISSIONS = (
    "construction_project_controls.read",
    "construction_project_controls.create",
    "construction_project_controls.update",
    "construction_project_controls.approve",
    "construction_project_controls.admin",
)
ROLE_GRANTS = {
    "project_engineer": {
        "construction_project_controls.read",
        "construction_project_controls.create",
        "construction_project_controls.update",
    },
    "scheduler": {
        "construction_project_controls.read",
        "construction_project_controls.update",
    },
    "cost_engineer": {
        "construction_project_controls.read",
        "construction_project_controls.update",
    },
    "project_controls_manager": set(PERMISSIONS[:-1]),
    "executive": {
        "construction_project_controls.read",
        "construction_project_controls.approve",
    },
    "auditor": {"construction_project_controls.read"},
    "admin": set(PERMISSIONS),
}
ACTION_THRESHOLDS = {
    "approve_baseline_revision": {"minimum_role": "project_controls_manager"},
    "freeze_reporting_period": {"minimum_role": "project_controls_manager"},
    "approve_major_change": {"minimum_role": "executive", "cost_threshold": 50000.0},
    "accept_progress": {"minimum_role": "project_controls_manager"},
}


def permission_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLE_GRANTS),
        "action_thresholds": ACTION_THRESHOLDS,
        "side_effects": (),
    }


def authorize(permission, actor=None, context=None):
    actor = dict(actor or {})
    context = dict(context or {})
    role = actor.get("role", "auditor")
    grants = ROLE_GRANTS.get(role, set())
    allowed = permission in grants or permission == f"{PBC_KEY}.operate"
    threshold_reason = None
    if context.get("action") == "approve_major_change":
        within_threshold = (
            float(context.get("cost_impact", 0.0))
            <= ACTION_THRESHOLDS["approve_major_change"]["cost_threshold"]
        )
        allowed = (allowed and within_threshold) or role in ("executive", "admin")
        threshold_reason = "major_change_threshold" if not allowed else None
    return {
        "ok": allowed,
        "permission": permission,
        "actor": actor,
        "context": context,
        "threshold_reason": threshold_reason,
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": permission_manifest()["ok"]
        and authorize(PERMISSIONS[0], {"role": "project_engineer"})["ok"]
        and not authorize(
            PERMISSIONS[3],
            {"role": "project_engineer"},
            {"action": "approve_major_change", "cost_impact": 60000.0},
        )["ok"],
        "side_effects": (),
    }
