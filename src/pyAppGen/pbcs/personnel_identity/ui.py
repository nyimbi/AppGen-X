"""UI contract for the Personnel Identity PBC."""

from __future__ import annotations


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
        "action_permissions": {
            "register_department": "personnel_identity.create",
            "create_employee": "personnel_identity.create",
            "transition_employee_status": "personnel_identity.update",
            "build_org_chart": "personnel_identity.review",
            "assign_role": "personnel_identity.role",
            "score_access_risk": "personnel_identity.review",
            "simulate_access_policy": "personnel_identity.review",
            "screen_policy": "personnel_identity.audit",
            "upsert_identity_attribute": "personnel_identity.attribute",
            "generate_eligibility_proof": "personnel_identity.audit",
            "run_control_tests": "personnel_identity.audit",
            "route_provisioning": "personnel_identity.update",
            "run_resilience_drill": "personnel_identity.audit",
            "federate_people_view": "personnel_identity.review",
            "register_rule": "personnel_identity.configure",
            "set_parameter": "personnel_identity.configure",
            "configure_runtime": "personnel_identity.configure",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_country", "allowed_worker_types", "allowed_statuses", "privacy_region"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
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
            "emits": ("DepartmentRegistered", "EmployeeCreated", "EmployeeStatusChanged", "RoleChanged", "IdentityAttributeChanged"),
            "consumes": ("EmployeeProvisioned", "AccessPolicyChanged", "OrgUnitChanged", "RoleReviewRequested"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
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
    }
