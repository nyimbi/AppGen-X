from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_EDGE_CASES, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, DOMAIN_PARAMETERS, DOMAIN_RULES, domain_capability_surface_contract
from .student_lifecycle_app import controls_contract, forms_contract, single_pbc_app_contract, wizards_contract

PBC_KEY = "education_student_lifecycle"


def education_student_lifecycle_ui_contract():
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": ("EducationStudentLifecycleWorkbench", "EducationStudentLifecycleDetail", "EducationStudentLifecycleAssistantPanel"),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "education_student_lifecycle.read",
            "education_student_lifecycle.create",
            "education_student_lifecycle.update",
            "education_student_lifecycle.approve",
            "education_student_lifecycle.admin",
        ),
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "single_pbc_app": single_pbc_app_contract(),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": ("admissions", "enrollment", "progression", "advising", "graduation", "assistant", "release_evidence"),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def education_student_lifecycle_render_workbench():
    ui = education_student_lifecycle_ui_contract()
    full = ui["full_capability_surface"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "queues": (
            "admissions_readiness",
            "registration_blockers",
            "high_risk_students",
            "intervention_follow_up",
            "petition_review",
            "graduation_candidates",
            "credential_clearance",
            "exception_backlog",
        ),
        "operation_actions": full["operation_actions"],
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "table_browsers": full["table_browsers"],
        "side_effects": (),
    }


def education_student_lifecycle_forms_contract():
    return forms_contract()


def education_student_lifecycle_wizards_contract():
    return wizards_contract()


def education_student_lifecycle_controls_contract():
    return controls_contract()


def smoke_test():
    return {"ok": education_student_lifecycle_ui_contract()["ok"] and education_student_lifecycle_render_workbench()["ok"], "side_effects": ()}
