"""UI contract for the Personnel Identity PBC."""

from __future__ import annotations

from .runtime import PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS
from .runtime import PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES
from .runtime import PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES
from .runtime import PERSONNEL_IDENTITY_OWNED_TABLES
from .runtime import PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC
from .runtime import personnel_identity_permissions_contract


PERSONNEL_IDENTITY_UI_FRAGMENT_KEYS = (
    "PersonnelIdentityWorkbench",
    "DepartmentMasterConsole",
    "EmployeeMasterConsole",
    "EmploymentLifecycleBoard",
    "ManagerHierarchyView",
    "OrgChartWorkbench",
    "RoleAssignmentConsole",
    "RoleChangeReviewQueue",
    "IdentityAttributeConsole",
    "SegregationOfDutiesPanel",
    "IdentityAssurancePanel",
    "ProvisioningHandlerMonitor",
    "EmployeeEventTimeline",
    "PrivacyResidencyRetentionPanel",
    "DirectorySearchView",
    "ApprovalReviewQueue",
    "PersonnelRuleStudio",
    "PersonnelParameterConsole",
    "PersonnelConfigurationPanel",
)


def personnel_identity_ui_contract() -> dict:
    return {
        "format": "appgen.personnel-identity-ui-contract.v1",
        "ok": True,
        "pbc": "personnel_identity",
        "implementation_directory": "src/pyAppGen/pbcs/personnel_identity",
        "fragments": PERSONNEL_IDENTITY_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/personnel_identity",
            "/workbench/pbcs/personnel_identity/departments",
            "/workbench/pbcs/personnel_identity/employees",
            "/workbench/pbcs/personnel_identity/lifecycle",
            "/workbench/pbcs/personnel_identity/managers",
            "/workbench/pbcs/personnel_identity/org-chart",
            "/workbench/pbcs/personnel_identity/roles",
            "/workbench/pbcs/personnel_identity/role-reviews",
            "/workbench/pbcs/personnel_identity/attributes",
            "/workbench/pbcs/personnel_identity/sod",
            "/workbench/pbcs/personnel_identity/assurance",
            "/workbench/pbcs/personnel_identity/provisioning",
            "/workbench/pbcs/personnel_identity/events",
            "/workbench/pbcs/personnel_identity/privacy",
            "/workbench/pbcs/personnel_identity/search",
            "/workbench/pbcs/personnel_identity/approvals",
            "/workbench/pbcs/personnel_identity/rules",
            "/workbench/pbcs/personnel_identity/parameters",
            "/workbench/pbcs/personnel_identity/configuration",
        ),
        "panels": (
            {
                "key": "directory",
                "fragment": "EmployeeMasterConsole",
                "binds_to": ("department", "employee", "manager", "identity"),
                "commands": ("register_department", "create_employee", "transition_employee_status", "build_org_chart"),
            },
            {
                "key": "access",
                "fragment": "RoleAssignmentConsole",
                "binds_to": ("role_assignment", "segregation_of_duties", "access_risk", "review"),
                "commands": ("assign_role", "score_access_risk", "simulate_access_policy", "screen_policy"),
            },
            {
                "key": "attributes",
                "fragment": "IdentityAttributeConsole",
                "binds_to": ("identity_attribute", "assurance", "eligibility_proof", "privacy_policy"),
                "commands": ("upsert_identity_attribute", "generate_eligibility_proof", "run_control_tests"),
            },
            {
                "key": "provisioning",
                "fragment": "ProvisioningHandlerMonitor",
                "binds_to": ("provisioning_event", "route", "dead_letter", "outbox"),
                "commands": ("route_provisioning", "run_resilience_drill", "federate_people_view"),
            },
            {
                "key": "governance",
                "fragment": "PersonnelRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": personnel_identity_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_country", "allowed_worker_types", "allowed_statuses", "privacy_region"),
            "allowed_database_backends": PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "max_roles_per_worker",
                "access_risk_threshold",
                "manager_span_limit",
                "identity_assurance_threshold",
                "stale_attribute_age_days",
                "review_cadence_days",
                "lifecycle_grace_days",
                "provisioning_retry_limit",
                "org_depth_limit",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("identity", "worker_eligibility", "role_assignment", "segregation_of_duties", "lifecycle", "privacy", "provisioning", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES,
            "consumes": PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {"owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES, "shared_table_access": False},
    }


def personnel_identity_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = personnel_identity_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    departments = tuple(dept for dept in state["departments"].values() if dept["tenant"] == tenant)
    employees = tuple(employee for employee in state["employees"].values() if employee["tenant"] == tenant)
    roles = tuple(role for role in state["roles"].values() if role["tenant"] == tenant)
    attributes = tuple(attribute for attribute in state["attributes"].values() if attribute["tenant"] == tenant)
    cards = (
        {"key": "departments", "value": len(departments), "fragment": "DepartmentMasterConsole"},
        {"key": "employees", "value": len(employees), "fragment": "EmployeeMasterConsole"},
        {"key": "active_employees", "value": len(tuple(employee for employee in employees if employee["status"] == "active")), "fragment": "EmploymentLifecycleBoard"},
        {"key": "role_assignments", "value": len(tuple(role for role in roles if role["status"] == "active")), "fragment": "RoleAssignmentConsole"},
        {"key": "identity_attributes", "value": len(attributes), "fragment": "IdentityAttributeConsole"},
        {"key": "assurance_floor", "value": min((attribute["assurance"] for attribute in attributes), default=0), "fragment": "IdentityAssurancePanel"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "PersonnelRuleStudio"},
    )
    return {
        "format": "appgen.personnel-identity-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/personnel_identity",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES,
            "outbox_table": "personnel_identity_appgen_outbox_event",
            "inbox_table": "personnel_identity_appgen_inbox_event",
            "dead_letter_table": "personnel_identity_dead_letter_event",
            "permissions": contract["action_permissions"],
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = personnel_identity_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = personnel_identity_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }


PERSONNEL_IDENTITY_FORM_KEYS = ("department_setup_form", "employee_identity_form", "employment_lifecycle_form", "role_assignment_form", "identity_attribute_form", "personnel_governance_form")
PERSONNEL_IDENTITY_WIZARD_KEYS = ("hire_to_identity_wizard", "role_access_review_wizard", "identity_assurance_wizard", "offboarding_wizard")
PERSONNEL_IDENTITY_CONTROL_KEYS = ("tenant_scope_picker", "org_chart_control", "role_risk_matrix", "identity_assurance_meter", "provisioning_reliability_drawer", "assistant_skill_panel")


def personnel_identity_form_catalog() -> tuple[dict, ...]:
    return (
        {"key": "department_setup_form", "title": "Department Setup", "command": "register_department", "owned_table": "personnel_department", "fields": ("department_id", "tenant", "name", "parent_department_id", "cost_center")},
        {"key": "employee_identity_form", "title": "Employee Identity", "command": "create_employee", "owned_table": "personnel_employee", "fields": ("employee_id", "tenant", "department_id", "manager_employee_id", "worker_type", "status", "job", "country")},
        {"key": "employment_lifecycle_form", "title": "Employment Lifecycle", "command": "transition_employee_status", "owned_table": "personnel_employment_lifecycle", "fields": ("employee_id", "status", "changed_by", "effective_at")},
        {"key": "role_assignment_form", "title": "Role Assignment", "command": "assign_role", "owned_table": "personnel_role_assignment", "fields": ("employee_id", "role", "scope", "assigned_by", "review_required")},
        {"key": "identity_attribute_form", "title": "Identity Attribute", "command": "upsert_identity_attribute", "owned_table": "personnel_identity_attribute", "fields": ("employee_id", "name", "value", "assurance", "verification_source")},
        {"key": "personnel_governance_form", "title": "Personnel Governance", "command": "register_rule", "owned_table": "personnel_policy_rule", "fields": ("rule_id", "tenant", "rule_type", "allowed_worker_types", "allowed_statuses", "required_attributes", "blocked_role_pairs", "status")},
    )


def personnel_identity_wizard_catalog() -> tuple[dict, ...]:
    return (
        {"key": "hire_to_identity_wizard", "steps": ("department_setup_form", "employee_identity_form", "identity_attribute_form", "role_assignment_form"), "goal": "Create a governed employee identity with verified attributes and role access."},
        {"key": "role_access_review_wizard", "steps": ("role_assignment_form", "identity_attribute_form"), "goal": "Review role risk, segregation of duties, and identity assurance before access activation."},
        {"key": "identity_assurance_wizard", "steps": ("identity_attribute_form", "personnel_governance_form"), "goal": "Raise identity assurance with required attributes and proof evidence."},
        {"key": "offboarding_wizard", "steps": ("employment_lifecycle_form", "role_assignment_form"), "goal": "Transition worker status and remove risky active access."},
    )


def personnel_identity_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "org_chart_control", "type": "tree", "binds_to": "personnel_org_chart_projection"},
        {"key": "role_risk_matrix", "type": "matrix", "binds_to": "personnel_role_assignment"},
        {"key": "identity_assurance_meter", "type": "meter", "binds_to": "personnel_identity_assurance"},
        {"key": "provisioning_reliability_drawer", "type": "drawer", "binds_to": "personnel_provisioning_event"},
        {"key": "assistant_skill_panel", "type": "assistant", "binds_to": "personnel_identity_skills"},
    )


def personnel_identity_standalone_app_contract() -> dict:
    return {"ok": True, "pbc": "personnel_identity", "app_id": "personnel_identity_one_pbc_app", "workbench_route": "/workbench/pbcs/personnel_identity", "navigation": ({"key": "departments", "route": "/workbench/pbcs/personnel_identity/departments"}, {"key": "employees", "route": "/workbench/pbcs/personnel_identity/employees"}, {"key": "roles", "route": "/workbench/pbcs/personnel_identity/roles"}, {"key": "attributes", "route": "/workbench/pbcs/personnel_identity/attributes"}, {"key": "provisioning", "route": "/workbench/pbcs/personnel_identity/provisioning"}, {"key": "governance", "route": "/workbench/pbcs/personnel_identity/configuration"}), "forms": PERSONNEL_IDENTITY_FORM_KEYS, "wizards": PERSONNEL_IDENTITY_WIZARD_KEYS, "controls": PERSONNEL_IDENTITY_CONTROL_KEYS, "single_agent_namespace": "personnel_identity_skills", "side_effects": ()}


def personnel_identity_ui_contract() -> dict:
    shell = personnel_identity_standalone_app_contract()
    return {
        "format": "appgen.personnel-identity-ui-contract.v1", "ok": True, "pbc": "personnel_identity", "implementation_directory": "src/pyAppGen/pbcs/personnel_identity", "fragments": PERSONNEL_IDENTITY_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in shell["navigation"]) + (shell["workbench_route"],),
        "panels": (
            {"key": "directory", "fragment": "EmployeeMasterConsole", "binds_to": ("department", "employee", "manager", "identity"), "commands": ("register_department", "create_employee", "transition_employee_status", "build_org_chart")},
            {"key": "access", "fragment": "RoleAssignmentConsole", "binds_to": ("role_assignment", "segregation_of_duties", "access_risk", "review"), "commands": ("assign_role", "score_access_risk", "simulate_access_policy", "screen_policy")},
            {"key": "attributes", "fragment": "IdentityAttributeConsole", "binds_to": ("identity_attribute", "assurance", "eligibility_proof", "privacy_policy"), "commands": ("upsert_identity_attribute", "generate_eligibility_proof", "run_control_tests")},
            {"key": "provisioning", "fragment": "ProvisioningHandlerMonitor", "binds_to": ("provisioning_event", "route", "dead_letter", "outbox"), "commands": ("route_provisioning", "run_resilience_drill", "federate_people_view")},
            {"key": "governance", "fragment": "PersonnelRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "forms": personnel_identity_form_catalog(), "wizards": personnel_identity_wizard_catalog(), "controls": personnel_identity_control_catalog(), "standalone_app": shell,
        "action_permissions": personnel_identity_permissions_contract()["action_permissions"],
        "configuration_editor": {"required_fields": ("database_backend", "event_topic", "retry_limit", "default_country", "allowed_worker_types", "allowed_statuses", "privacy_region"), "allowed_database_backends": PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS, "required_event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "user_selectable_event_contract": False},
        "parameter_editor": {"numeric_parameters": ("max_roles_per_worker", "access_risk_threshold", "manager_span_limit", "identity_assurance_threshold", "stale_attribute_age_days", "review_cadence_days", "lifecycle_grace_days", "provisioning_retry_limit", "org_depth_limit", "workbench_limit"), "bounded_supported_parameters": True},
        "rule_editor": {"rule_types": ("identity", "worker_eligibility", "role_assignment", "segregation_of_duties", "lifecycle", "privacy", "provisioning", "release_gate"), "required_fields": ("rule_id", "tenant", "scope", "status"), "compiled_evidence_required": True},
        "event_surfaces": {"emits": PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES, "consumes": PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES, "outbox_status": "visible", "inbox_status": "visible", "dead_letter_status": "visible"},
        "binding_evidence": {"owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES, "outbox_table": "personnel_identity_appgen_outbox_event", "inbox_table": "personnel_identity_appgen_inbox_event", "dead_letter_table": "personnel_identity_dead_letter_event", "shared_table_access": False, "required_event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC, "rbac_permissions": personnel_identity_permissions_contract()["permissions"]},
    }


def personnel_identity_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = personnel_identity_ui_contract()
    shell = personnel_identity_standalone_app_contract()
    from .runtime import personnel_identity_build_workbench_view
    snapshot = personnel_identity_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    cards = ({"key": "departments", "value": snapshot["department_count"], "fragment": "DepartmentMasterConsole"}, {"key": "employees", "value": snapshot["employee_count"], "fragment": "EmployeeMasterConsole"}, {"key": "active_employees", "value": snapshot["active_employee_count"], "fragment": "EmploymentLifecycleBoard"}, {"key": "role_assignments", "value": snapshot["role_assignment_count"], "fragment": "RoleAssignmentConsole"}, {"key": "identity_attributes", "value": snapshot["attribute_count"], "fragment": "IdentityAttributeConsole"})
    return {"format": "appgen.personnel-identity-workbench-render.v1", "ok": True, "tenant": tenant, "route": shell["workbench_route"], "fragments": contract["fragments"], "navigation": shell["navigation"], "forms": contract["forms"], "wizards": contract["wizards"], "controls": contract["controls"], "cards": cards, "visible_actions": visible_actions, "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions), "configuration_bound": snapshot["configuration_bound"], "rules_bound": tuple(sorted(state.get("rules", {}))), "parameters_bound": tuple(sorted(state.get("parameters", {}))), "event_outbox_count": len(state.get("outbox", ())), "event_inbox_count": snapshot["inbox_count"], "dead_letter_count": snapshot["dead_letter_count"], "binding_evidence": contract["binding_evidence"], "workbench": snapshot}


def personnel_identity_render_standalone_app(state: dict, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
    contract = personnel_identity_ui_contract()
    permissions = principal_permissions or tuple(sorted(set(contract["action_permissions"].values())))
    rendered = personnel_identity_render_workbench(state, tenant=tenant, principal_permissions=permissions)
    return {"ok": rendered["ok"], "pbc": "personnel_identity", "shell": personnel_identity_standalone_app_contract(), "workbench": rendered, "side_effects": ()}


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = personnel_identity_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = personnel_identity_render_workbench(_appgen_smoke_state(), tenant="smoke", principal_permissions=permissions)
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {"rule_types": ("configuration", "parameter", "release_gate"), "required_fields": ("rule_id", "scope", "status")}
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {"configuration_editor": configuration_editor, "parameter_editor": contract.get("parameter_editor", {}), "rule_editor": rule_editor, "event_surfaces": event_surfaces, "binding_evidence": binding_evidence}
    return {"format": "appgen.pbc-ui-smoke-test.v1", "ok": contract.get("ok") is True and rendered.get("ok") is True and bool(contract.get("fragments")) and bool(contract.get("routes")) and bool(contract.get("forms")) and bool(contract.get("wizards")) and bool(contract.get("controls")) and bool(cards) and bool(contract.get("action_permissions")) and bool(configuration_editor) and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False and bool(contract.get("parameter_editor")) and bool(rule_editor) and bool(event_surfaces) and ("outbox_status" in event_surfaces or "contract" in event_surfaces) and binding_evidence.get("shared_table_access") is not True and not binding_evidence.get("shared_tables", ()), "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ()), "forms": tuple(item["key"] for item in contract.get("forms", ())), "wizards": tuple(item["key"] for item in contract.get("wizards", ())), "controls": tuple(item["key"] for item in contract.get("controls", ()))}, "contract": contract, "governance": governance, "rendered": rendered, "cards": cards, "side_effects": ()}
