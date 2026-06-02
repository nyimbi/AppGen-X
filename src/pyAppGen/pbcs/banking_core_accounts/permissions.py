PBC_KEY = "banking_core_accounts"
PERMISSIONS = (
    "banking_core_accounts.read",
    "banking_core_accounts.create",
    "banking_core_accounts.update",
    "banking_core_accounts.approve",
    "banking_core_accounts.admin",
    "banking_core_accounts.operate",
)
ROLE_PERMISSIONS = {
    "operator": (
        "banking_core_accounts.read",
        "banking_core_accounts.create",
        "banking_core_accounts.update",
        "banking_core_accounts.operate",
    ),
    "approver": (
        "banking_core_accounts.read",
        "banking_core_accounts.approve",
        "banking_core_accounts.operate",
    ),
    "auditor": (
        "banking_core_accounts.read",
        "banking_core_accounts.admin",
    ),
}
OPERATION_PERMISSIONS = {
    "open_deposit_account": "banking_core_accounts.create",
    "transition_deposit_account": "banking_core_accounts.update",
    "query_account_detail": "banking_core_accounts.read",
    "query_workbench": "banking_core_accounts.read",
    "build_workflow_surface": "banking_core_accounts.read",
    "parse_document_instruction": "banking_core_accounts.read",
    "configure_runtime": "banking_core_accounts.admin",
    "set_parameter": "banking_core_accounts.admin",
    "register_rule": "banking_core_accounts.admin",
}


def permission_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLE_PERMISSIONS),
        "role_permissions": tuple(
            {"role": role, "permissions": permissions}
            for role, permissions in ROLE_PERMISSIONS.items()
        ),
        "side_effects": (),
    }


def permission_for_operation(operation):
    permission = OPERATION_PERMISSIONS.get(operation, f"{PBC_KEY}.operate")
    return {
        "ok": permission in PERMISSIONS,
        "operation": operation,
        "required_permission": permission,
        "side_effects": (),
    }


def authorize(permission, actor=None):
    actor = dict(actor or {})
    if permission not in PERMISSIONS:
        return {
            "ok": False,
            "permission": permission,
            "actor": actor,
            "reason": "unknown_permission",
            "side_effects": (),
        }

    if not actor:
        return {
            "ok": True,
            "permission": permission,
            "actor": actor,
            "granted_by": "implicit_manifest_check",
            "side_effects": (),
        }

    granted = set(actor.get("permissions") or ())
    for role in actor.get("roles") or ():
        granted.update(ROLE_PERMISSIONS.get(role, ()))
    if f"{PBC_KEY}.admin" in granted:
        granted.update(PERMISSIONS)
    authorized = permission in granted
    return {
        "ok": authorized,
        "permission": permission,
        "actor": actor,
        "granted_permissions": tuple(sorted(granted)),
        "reason": None if authorized else "permission_denied",
        "side_effects": (),
    }


def permission_plan(operation, actor=None):
    mapping = permission_for_operation(operation)
    authorization = authorize(mapping["required_permission"], actor=actor)
    return {
        "ok": mapping["ok"] and authorization["ok"],
        "operation": operation,
        "required_permission": mapping["required_permission"],
        "authorization": authorization,
        "side_effects": (),
    }


def smoke_test():
    manifest = permission_manifest()
    allowed = authorize(
        "banking_core_accounts.update", actor={"roles": ("operator",)}
    )
    denied = authorize(
        "banking_core_accounts.approve", actor={"roles": ("operator",)}
    )
    return {
        "ok": manifest["ok"] and allowed["ok"] and denied["ok"] is False,
        "side_effects": (),
    }
