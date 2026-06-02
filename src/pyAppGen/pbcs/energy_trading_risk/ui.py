from .controls import energy_trading_risk_control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract
from .forms import energy_trading_risk_form_catalog
from .trading_control import improve1_trading_control_contract
from .forms import energy_trading_risk_get_form
from .wizards import energy_trading_risk_plan_wizard
from .wizards import energy_trading_risk_wizard_catalog

PBC_KEY = "energy_trading_risk"



def energy_trading_risk_form_contract(form_id: str = "energy_trade_capture"):
    form = energy_trading_risk_get_form(form_id)
    return {"ok": form["ok"], "pbc": PBC_KEY, **form, "shared_table_access": False, "side_effects": ()}



def energy_trading_risk_wizard_contract(wizard_id: str = "trade_capture_release"):
    plan = energy_trading_risk_plan_wizard(wizard_id, {})
    return {"ok": plan["ok"], "pbc": PBC_KEY, "wizard_id": wizard_id, "wizard": plan, "shared_table_access": False, "side_effects": ()}



def energy_trading_risk_control_manifest():
    catalog = energy_trading_risk_control_catalog()
    return {"ok": catalog["ok"], "pbc": PBC_KEY, **catalog, "shared_table_access": False, "side_effects": ()}



def energy_trading_risk_single_pbc_app_ui_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_shell": "EnergyTradingRiskAppShell",
        "forms": energy_trading_risk_form_catalog()["form_ids"],
        "wizards": energy_trading_risk_wizard_catalog()["wizard_ids"],
        "controls": energy_trading_risk_control_catalog()["control_ids"],
        "workbench_views": (
            "ready_for_release",
            "trade_exceptions",
            "nomination_exceptions",
            "curve_exceptions",
            "settlement_exceptions",
        ),
        "agent_help_surface": "EnergyTradingRiskAssistantPanel",
        "shared_table_access": False,
        "side_effects": (),
    }



def energy_trading_risk_ui_contract():
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": ("EnergyTradingRiskWorkbench", "EnergyTradingRiskDetail", "EnergyTradingRiskAssistantPanel"),
        "configuration_editor": True,
        "parameter_editor": True,
        "rule_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "energy_trading_risk.read",
            "energy_trading_risk.create",
            "energy_trading_risk.update",
            "energy_trading_risk.approve",
            "energy_trading_risk.admin",
        ),
        "forms": energy_trading_risk_form_catalog()["forms"],
        "wizards": energy_trading_risk_wizard_catalog()["wizards"],
        "controls": energy_trading_risk_control_catalog()["controls"],
        "app_shell": energy_trading_risk_single_pbc_app_ui_contract(),
        "trading_control_contract": improve1_trading_control_contract(),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "trading_control_panels": tuple(item["evidence"]["ui_surface"] for item in improve1_trading_control_contract()["capabilities"]),
            "navigation_sections": (
                "overview",
                "trade_capture",
                "nomination_governance",
                "curve_quality",
                "workbench",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }



def energy_trading_risk_render_workbench():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "queue_views": energy_trading_risk_single_pbc_app_ui_contract()["workbench_views"],
        "columns": (
            "id",
            "status_badge",
            "commodity",
            "market_hub",
            "delivery_period",
            "book",
            "signed_volume_mwh",
            "projected_mark_to_market",
            "workbench_queue",
        ),
        "controls": energy_trading_risk_control_catalog()["controls"],
        "side_effects": (),
    }



def smoke_test():
    return {
        "ok": energy_trading_risk_ui_contract()["ok"]
        and energy_trading_risk_render_workbench()["ok"]
        and energy_trading_risk_form_contract()["ok"]
        and energy_trading_risk_wizard_contract()["ok"]
        and energy_trading_risk_control_manifest()["ok"],
        "side_effects": (),
    }
