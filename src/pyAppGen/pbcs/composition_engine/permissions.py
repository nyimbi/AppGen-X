"""Executable permission contract for the composition_engine PBC."""

from __future__ import annotations


PBC_KEY = "composition_engine"
PERMISSIONS = (
    "composition_engine.read",
    "composition_engine.compose",
    "composition_engine.approve",
    "composition_engine.publish",
    "composition_engine.event",
    "composition_engine.configure",
    "composition_engine.audit",
)
ACTION_PERMISSIONS = {
    "create_workspace": "composition_engine.compose",
    "select_pbc": "composition_engine.compose",
    "register_component": "composition_engine.compose",
    "register_ui_fragment": "composition_engine.compose",
    "bind_layout": "composition_engine.compose",
    "preview_selection_impact": "composition_engine.compose",
    "validate_composition_plan": "composition_engine.approve",
    "plan_package_registration": "composition_engine.publish",
    "generate_composition_dsl": "composition_engine.publish",
    "publish_composition": "composition_engine.publish",
    "release_rehearsal": "composition_engine.publish",
    "assistant_document_preview": "composition_engine.read",
    "route_agent_intent": "composition_engine.read",
    "agent_competency_catalog": "composition_engine.read",
    "receive_event": "composition_engine.event",
    "register_rule": "composition_engine.configure",
    "register_schema_extension": "composition_engine.configure",
    "set_parameter": "composition_engine.configure",
    "configure_runtime": "composition_engine.configure",
    "run_control_tests": "composition_engine.audit",
    "build_control_center": "composition_engine.audit",
    "build_workbench_view": "composition_engine.audit",
    "build_smoke_plan": "composition_engine.audit",
    "build_artifact_lineage": "composition_engine.audit",
    "build_documentation_matrix": "composition_engine.audit",
    "build_security_review": "composition_engine.audit",
    "build_release_notes": "composition_engine.audit",
    "build_schema_contract": "composition_engine.audit",
    "build_service_contract": "composition_engine.audit",
    "build_release_evidence": "composition_engine.audit",
}
ROLE_GRANTS = {
    "composition_operator": (
        "composition_engine.read",
        "composition_engine.compose",
    ),
    "composition_reviewer": (
        "composition_engine.read",
        "composition_engine.approve",
        "composition_engine.audit",
    ),
    "composition_publisher": (
        "composition_engine.read",
        "composition_engine.publish",
        "composition_engine.audit",
    ),
    "composition_admin": PERMISSIONS,
}


def permission_manifest():
    """Return the permission surface without mutating runtime state."""
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "roles": dict(ROLE_GRANTS),
        "side_effects": (),
    }


def authorize(action, granted_permissions=()):
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


def role_permissions(role: str) -> dict:
    """Return the permission bundle granted to one named role."""
    permissions = ROLE_GRANTS.get(role)
    return {
        "ok": permissions is not None,
        "pbc": PBC_KEY,
        "role": role,
        "permissions": tuple(permissions or ()),
        "side_effects": (),
    }


def smoke_test():
    """Exercise permission and role decisions side-effect-free."""
    manifest = permission_manifest()
    decision = authorize("publish_composition", ROLE_GRANTS["composition_admin"])
    reviewer = role_permissions("composition_reviewer")
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"] and reviewer["ok"],
        "manifest": manifest,
        "decision": decision,
        "reviewer": reviewer,
        "side_effects": (),
    }
