from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)
from .standalone import (
    land_real_estate_development_build_controls_contract,
    land_real_estate_development_build_forms_contract,
    land_real_estate_development_build_wizards_contract,
    land_real_estate_development_standalone_workbench_blueprint,
)

PBC_KEY = "land_real_estate_development"


def land_real_estate_development_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    standalone = land_real_estate_development_standalone_workbench_blueprint()
    forms = land_real_estate_development_build_forms_contract()
    wizards = land_real_estate_development_build_wizards_contract()
    controls = land_real_estate_development_build_controls_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "LandRealEstateDevelopmentWorkbench",
            "LandRealEstateDevelopmentDetail",
            "LandRealEstateDevelopmentAssistantPanel",
            "LandRealEstateDevelopmentParcelCockpit",
            "LandRealEstateDevelopmentEntitlementCockpit",
            "LandRealEstateDevelopmentFeasibilityCockpit",
            "LandRealEstateDevelopmentHandoffCockpit",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "land_real_estate_development.read",
            "land_real_estate_development.create",
            "land_real_estate_development.update",
            "land_real_estate_development.approve",
            "land_real_estate_development.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "parcel_cockpit",
                "entitlement_pipeline",
                "feasibility_investment_committee",
                "handoff_readiness",
                "assistant_previews",
                "release_evidence",
            ),
            "forms": forms["forms"],
            "wizards": wizards["wizards"],
            "controls": controls["controls"],
            "standalone_shell": standalone,
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def land_real_estate_development_render_workbench() -> dict:
    ui = land_real_estate_development_ui_contract()
    full = ui["full_capability_surface"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "operation_actions": full["operation_actions"],
        "table_browsers": full["table_browsers"],
        "cockpit_sections": full["navigation_sections"],
        "forms": tuple(form["name"] for form in full["forms"]),
        "wizards": tuple(wizard["name"] for wizard in full["wizards"]),
        "controls": tuple(control["name"] for control in full["controls"]),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": (
            land_real_estate_development_ui_contract()["ok"]
            and land_real_estate_development_render_workbench()["ok"]
        ),
        "side_effects": (),
    }
