"""UI contract for the Talent Onboarding PBC."""

from __future__ import annotations


TALENT_ONBOARDING_UI_FRAGMENT_KEYS = (
    "TalentOnboardingWorkbench",
    "RequisitionConsole",
    "CandidatePipelineBoard",
    "BackgroundCheckReview",
    "OfferApprovalBoard",
    "OnboardingTaskBoard",
    "TalentRuleStudio",
    "TalentParameterConsole",
    "TalentConfigurationPanel",
)


def talent_onboarding_ui_contract() -> dict:
    return {
        "format": "appgen.talent-onboarding-ui-contract.v1",
        "ok": True,
        "pbc": "talent_onboarding",
        "implementation_directory": "src/pyAppGen/pbcs/talent_onboarding",
        "fragments": TALENT_ONBOARDING_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/talent_onboarding",
            "/workbench/pbcs/talent_onboarding/requisitions",
            "/workbench/pbcs/talent_onboarding/candidates",
            "/workbench/pbcs/talent_onboarding/checks",
            "/workbench/pbcs/talent_onboarding/offers",
            "/workbench/pbcs/talent_onboarding/tasks",
            "/workbench/pbcs/talent_onboarding/rules",
            "/workbench/pbcs/talent_onboarding/parameters",
            "/workbench/pbcs/talent_onboarding/configuration",
        ),
        "panels": (
            {
                "key": "requisition_console",
                "fragment": "RequisitionConsole",
                "binds_to": ("job_requisition", "role_projection"),
                "commands": ("create_job_requisition", "simulate_hiring_policy"),
            },
            {
                "key": "candidate_pipeline",
                "fragment": "CandidatePipelineBoard",
                "binds_to": ("candidate", "background_check", "offer"),
                "commands": ("create_candidate", "advance_candidate_stage", "extend_offer", "accept_offer"),
            },
            {
                "key": "onboarding_tasks",
                "fragment": "OnboardingTaskBoard",
                "binds_to": ("onboarding_task", "candidate", "outbox"),
                "commands": ("create_onboarding_task", "complete_onboarding_task", "provision_employee"),
            },
            {
                "key": "governance_studio",
                "fragment": "TalentRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": {
            "create_job_requisition": "talent_onboarding.requisition",
            "create_candidate": "talent_onboarding.candidate",
            "advance_candidate_stage": "talent_onboarding.candidate",
            "record_background_check": "talent_onboarding.candidate",
            "extend_offer": "talent_onboarding.offer",
            "accept_offer": "talent_onboarding.offer",
            "create_onboarding_task": "talent_onboarding.onboard",
            "complete_onboarding_task": "talent_onboarding.onboard",
            "provision_employee": "talent_onboarding.onboard",
            "register_rule": "talent_onboarding.configure",
            "set_parameter": "talent_onboarding.configure",
            "configure_runtime": "talent_onboarding.configure",
            "run_control_tests": "talent_onboarding.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "minimum_match_score",
                "offer_expiry_days",
                "onboarding_sla_days",
                "background_check_confidence_threshold",
                "retention_days",
            ),
        },
        "rule_editor": {
            "rule_types": ("hiring", "screening", "offer", "onboarding", "retention", "provisioning"),
            "required_fields": ("rule_id", "tenant", "rule_type", "eligible_worker_types", "allowed_countries", "status"),
        },
        "event_surfaces": {
            "emits": ("EmployeeProvisioned", "CandidateHired"),
            "consumes": ("RoleChanged",),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def talent_onboarding_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = talent_onboarding_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(
        action
        for action, required_permission in action_permissions.items()
        if required_permission in permissions
    )
    tenant_requisitions = tuple(req for req in state["requisitions"].values() if req["tenant"] == tenant)
    tenant_candidates = tuple(candidate for candidate in state["candidates"].values() if candidate["tenant"] == tenant)
    tenant_checks = tuple(check for check in state["checks"].values() if check["tenant"] == tenant)
    tenant_offers = tuple(offer for offer in state["offers"].values() if offer["tenant"] == tenant)
    tenant_tasks = tuple(task for task in state["tasks"].values() if task["tenant"] == tenant)
    cards = (
        {"key": "open_requisitions", "value": len(tuple(req for req in tenant_requisitions if req["status"] == "open")), "fragment": "RequisitionConsole"},
        {"key": "active_candidates", "value": len(tuple(candidate for candidate in tenant_candidates if candidate["status"] == "active")), "fragment": "CandidatePipelineBoard"},
        {"key": "hired_candidates", "value": len(tuple(candidate for candidate in tenant_candidates if candidate["stage"] == "hired")), "fragment": "CandidatePipelineBoard"},
        {"key": "background_checks", "value": len(tenant_checks), "fragment": "BackgroundCheckReview"},
        {"key": "offers", "value": len(tenant_offers), "fragment": "OfferApprovalBoard"},
        {"key": "completed_tasks", "value": len(tuple(task for task in tenant_tasks if task["status"] == "completed")), "fragment": "OnboardingTaskBoard"},
    )
    return {
        "format": "appgen.talent-onboarding-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/talent_onboarding",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
    }
