from __future__ import annotations

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)

PBC_KEY = "wealth_portfolio_management"
STANDALONE_FORMS = (
    "household_client_profile_form",
    "goal_and_risk_profile_form",
    "investment_policy_statement_form",
    "trade_proposal_approval_form",
    "advisor_review_form",
)
STANDALONE_WIZARDS = (
    "portfolio_onboarding_wizard",
    "tax_aware_rebalance_wizard",
    "cash_need_planning_wizard",
    "document_collection_wizard",
    "compliance_surveillance_wizard",
)
STANDALONE_CONTROLS = (
    "household_summary_cards",
    "drift_heatmap",
    "suitability_readiness_badge",
    "restriction_matrix",
    "tax_lot_grid",
    "cash_need_forecast",
    "fee_projection_cards",
    "document_checklist",
    "compliance_alert_queue",
    "governed_ai_assistant_panel",
)


def wealth_portfolio_management_ui_contract():
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "WealthPortfolioManagementWorkbench",
            "WealthPortfolioManagementDetail",
            "WealthPortfolioManagementAssistantPanel",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "wealth_portfolio_management.read",
            "wealth_portfolio_management.create",
            "wealth_portfolio_management.update",
            "wealth_portfolio_management.approve",
            "wealth_portfolio_management.admin",
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
                "onboarding",
                "rebalancing",
                "surveillance",
                "documents",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def wealth_portfolio_management_render_workbench():
    ui = wealth_portfolio_management_ui_contract()
    full = ui["full_capability_surface"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "operation_actions": full["operation_actions"],
        "table_browsers": full["table_browsers"],
        "side_effects": (),
    }


def wealth_portfolio_management_standalone_workbench_blueprint() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": "/app/wealth-portfolio-management/workbench",
        "forms": STANDALONE_FORMS,
        "wizards": STANDALONE_WIZARDS,
        "controls": STANDALONE_CONTROLS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def wealth_portfolio_management_render_standalone_workbench(workbench: dict) -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "cards": (
            {"id": "portfolio_count", "label": "Households", "value": workbench.get("portfolio_count", 0)},
            {"id": "assets", "label": "Total assets", "value": workbench.get("total_assets", 0.0)},
            {"id": "alerts", "label": "Open alerts", "value": workbench.get("open_alert_count", 0)},
            {"id": "rebalances", "label": "Pending rebalances", "value": workbench.get("pending_rebalance_count", 0)},
        ),
        "queues": {
            "portfolio_rows": tuple(workbench.get("portfolio_rows", ())),
            "controls": STANDALONE_CONTROLS,
        },
        "forms": STANDALONE_FORMS,
        "wizards": STANDALONE_WIZARDS,
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": wealth_portfolio_management_ui_contract()["ok"] and wealth_portfolio_management_render_workbench()["ok"],
        "side_effects": (),
    }


def standalone_ui_smoke_test() -> dict:
    blueprint = wealth_portfolio_management_standalone_workbench_blueprint()
    rendered = wealth_portfolio_management_render_standalone_workbench(
        {
            "portfolio_count": 1,
            "total_assets": 2500000.0,
            "open_alert_count": 1,
            "pending_rebalance_count": 1,
            "portfolio_rows": ({"portfolio_id": "ui-smoke", "open_alerts": 1},),
        }
    )
    return {"ok": blueprint["ok"] and rendered["ok"], "blueprint": blueprint, "rendered": rendered, "side_effects": ()}
