"""Permission contracts for agriculture_farm_operations."""

PBC_KEY = "agriculture_farm_operations"
PERMISSIONS = (
    "agriculture_farm_operations.read",
    "agriculture_farm_operations.create",
    "agriculture_farm_operations.update",
    "agriculture_farm_operations.approve",
    "agriculture_farm_operations.admin",
)
ACTION_PERMISSIONS = {
    "query_workbench": "agriculture_farm_operations.read",
    "query_release_evidence": "agriculture_farm_operations.read",
    "command_field": "agriculture_farm_operations.create",
    "record_crop_plan": "agriculture_farm_operations.create",
    "parse_document_instruction": "agriculture_farm_operations.update",
    "run_advanced_assessment": "agriculture_farm_operations.approve",
    "configure_runtime": "agriculture_farm_operations.admin",
    "set_parameter": "agriculture_farm_operations.admin",
    "register_rule": "agriculture_farm_operations.admin",
    "receive_event": "agriculture_farm_operations.admin",
}


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": ("operator", "approver", "auditor"),
        "action_permissions": ACTION_PERMISSIONS,
        "side_effects": (),
    }


def authorize(permission: str, actor: dict | None = None) -> dict:
    return {
        "ok": permission in PERMISSIONS or permission == f"{PBC_KEY}.operate",
        "permission": permission,
        "actor": dict(actor or {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0])["ok"],
        "side_effects": (),
    }
