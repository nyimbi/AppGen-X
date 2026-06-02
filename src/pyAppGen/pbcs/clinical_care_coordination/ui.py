"""UI contracts and standalone rendering for clinical_care_coordination."""

from __future__ import annotations

from .care_coordination_app import care_coordination_controls_contract as app_controls_contract
from .care_coordination_app import care_coordination_forms_contract as app_forms_contract
from .care_coordination_app import care_coordination_workbench
from .care_coordination_app import care_coordination_wizards_contract as app_wizards_contract
from .care_coordination_app import empty_care_coordination_state
from .care_coordination_app import single_pbc_app_contract
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .clinical_control import CLINICAL_CONTROL_CAPABILITIES
from .clinical_control import improve1_clinical_control_contract
from .domain_depth import domain_capability_surface_contract


PBC_KEY = "clinical_care_coordination"
UI_FRAGMENTS = (
    "ClinicalCareCoordinationWorkbench",
    "ClinicalCareCoordinationDetail",
    "ClinicalCareCoordinationAssistantPanel",
)
WORKBENCH_QUEUES = (
    "high_risk_patients",
    "unscheduled_referrals",
    "unreconciled_results",
    "active_transitions",
    "blocked_care_gaps",
    "outreach_due_today",
    "care_team_coverage_gaps",
    "control_failures",
)
ACTION_PERMISSIONS = (
    "clinical_care_coordination.read",
    "clinical_care_coordination.create",
    "clinical_care_coordination.update",
    "clinical_care_coordination.approve",
    "clinical_care_coordination.admin",
)


def clinical_care_coordination_standalone_app_contract() -> dict:
    app = single_pbc_app_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_id": "clinical_care_coordination_one_pbc_app",
        "workbench_route": "/workbench/pbcs/clinical_care_coordination",
        "navigation": (
            {"key": "command_center", "route": "/workbench/pbcs/clinical_care_coordination"},
            {"key": "care_plans", "route": "/workbench/pbcs/clinical_care_coordination/care-plans"},
            {"key": "referrals", "route": "/workbench/pbcs/clinical_care_coordination/referrals"},
            {"key": "transitions", "route": "/workbench/pbcs/clinical_care_coordination/transitions"},
            {"key": "assistant", "route": "/workbench/pbcs/clinical_care_coordination/assistant"},
        ),
        "forms": tuple(form["form_id"] for form in app["forms"]),
        "wizards": tuple(wizard["wizard_id"] for wizard in app["wizards"]),
        "controls": tuple(control["control_id"] for control in app["controls"]),
        "single_agent_namespace": "clinical_care_coordination_skills",
        "side_effects": (),
    }


def clinical_care_coordination_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    forms = app_forms_contract()["forms"]
    wizards = app_wizards_contract()["wizards"]
    controls = app_controls_contract()["controls"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": UI_FRAGMENTS,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "single_pbc_app": single_pbc_app_contract(),
        "standalone_app": clinical_care_coordination_standalone_app_contract(),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": ACTION_PERMISSIONS,
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES + CLINICAL_CONTROL_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "operations",
                "edge_case_triage",
                "advanced_intelligence",
                "release_evidence",
            ),
            "clinical_control_panels": tuple(f"clinical_control_{capability}" for capability in CLINICAL_CONTROL_CAPABILITIES),
            "clinical_control_contract": improve1_clinical_control_contract(),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def clinical_care_coordination_render_workbench(
    state: dict | None = None,
    *,
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    state = state or empty_care_coordination_state()
    ui = clinical_care_coordination_ui_contract()
    workbench = care_coordination_workbench(state)
    shell = clinical_care_coordination_standalone_app_contract()
    granted = set(principal_permissions or ACTION_PERMISSIONS)
    visible_actions = tuple(permission for permission in ACTION_PERMISSIONS if permission in granted)
    cards = tuple(
        {
            "key": queue_name,
            "value": workbench["queue_counts"][queue_name],
            "route": shell["workbench_route"],
        }
        for queue_name in WORKBENCH_QUEUES
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": shell["workbench_route"],
        "shell": shell,
        "queues": workbench["queues"],
        "queue_counts": workbench["queue_counts"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(permission for permission in ACTION_PERMISSIONS if permission not in granted),
        "operation_actions": ui["full_capability_surface"]["operation_actions"],
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "table_browsers": ui["full_capability_surface"]["table_browsers"],
        "side_effects": (),
    }


def clinical_care_coordination_forms_contract() -> dict:
    return app_forms_contract()


def clinical_care_coordination_wizard_contract() -> dict:
    return app_wizards_contract()


def clinical_care_coordination_controls_contract() -> dict:
    return app_controls_contract()


def smoke_test() -> dict:
    rendered = clinical_care_coordination_render_workbench()
    return {
        "ok": clinical_care_coordination_ui_contract()["ok"] and rendered["ok"] and rendered["cards"][0]["key"] == "high_risk_patients",
        "side_effects": (),
    }
