from __future__ import annotations

from .models import BUSINESS_TABLES
from .routes import STANDALONE_ROUTES, standalone_route_contracts
from .ui import STANDALONE_FORMS, STANDALONE_WIZARDS, STANDALONE_CONTROLS

PBC_KEY = "wealth_portfolio_management"
OWNED_TABLES = BUSINESS_TABLES + (
    "wealth_portfolio_management_wealth_portfolio_management_governed_model",
    "wealth_portfolio_management_wealth_portfolio_management_control_assertion",
)


def _route_candidates(action: str, table: str) -> tuple[str, ...]:
    route_map = {
        "wealth_portfolio_management_client_portfolio": "/app/wealth-portfolio-management/portfolios",
        "wealth_portfolio_management_investment_mandate": "/app/wealth-portfolio-management/investment-policy",
        "wealth_portfolio_management_suitability_profile": "/app/wealth-portfolio-management/suitability",
        "wealth_portfolio_management_fee_schedule": "/app/wealth-portfolio-management/fees",
        "wealth_portfolio_management_document_package": "/app/wealth-portfolio-management/documents",
        "wealth_portfolio_management_rebalance_order": "/app/wealth-portfolio-management/trade-proposals",
        "wealth_portfolio_management_performance_snapshot": "/app/wealth-portfolio-management/performance",
        "wealth_portfolio_management_advisory_review": "/app/wealth-portfolio-management/advisor-reviews",
        "wealth_portfolio_management_compliance_surveillance": "/app/wealth-portfolio-management/surveillance",
    }
    path = route_map.get(table)
    if not path:
        return tuple(item[1] for item in STANDALONE_ROUTES if item[0] == "GET")
    return (path,) if action != "read" else ("/app/wealth-portfolio-management/portfolio-detail", "/app/wealth-portfolio-management/workbench")


def agent_skill_manifest():
    skills = tuple(
        {
            "name": name,
            "scope": PBC_KEY,
            "description": description,
            "requires_confirmation": True,
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for name, description in (
            (f"{PBC_KEY}_guide_household_onboarding", "Guide household, goal, and risk onboarding."),
            (f"{PBC_KEY}_prepare_rebalance", "Prepare tax-aware rebalance proposals with cash and restriction checks."),
            (f"{PBC_KEY}_collect_documents", "Collect and validate IPS, suitability, and disclosure documents."),
            (f"{PBC_KEY}_run_surveillance", "Run compliance surveillance and triage alerts."),
            (f"{PBC_KEY}_review_advisor_package", "Review advisor findings, communications, and approvals."),
        )
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "release_evidence_navigation",
            "workbench_navigation",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document, instruction):
    lowered = f"{document} {instruction}".lower()
    if "ips" in lowered or "investment policy" in lowered:
        tables = ("wealth_portfolio_management_investment_mandate",)
        forms = ("investment_policy_statement_form",)
        wizards = ("document_collection_wizard",)
    elif "review" in lowered or "advisor" in lowered:
        tables = ("wealth_portfolio_management_advisory_review", "wealth_portfolio_management_document_package")
        forms = ("advisor_review_form",)
        wizards = ("compliance_surveillance_wizard",)
    else:
        tables = (
            "wealth_portfolio_management_client_portfolio",
            "wealth_portfolio_management_suitability_profile",
            "wealth_portfolio_management_document_package",
        )
        forms = ("household_client_profile_form", "goal_and_risk_profile_form")
        wizards = ("portfolio_onboarding_wizard", "document_collection_wizard")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "instruction": instruction,
        "document_summary": document[:120],
        "candidate_tables": tables,
        "route_candidates": tuple(_route_candidates("create", table) for table in tables),
        "form_candidates": forms,
        "wizard_candidates": wizards,
        "control_candidates": STANDALONE_CONTROLS[:4],
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or "wealth_portfolio_management_client_portfolio"
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "route_candidates": _route_candidates(action, target),
        "form_candidates": STANDALONE_FORMS,
        "wizard_candidates": STANDALONE_WIZARDS,
        "control_candidates": STANDALONE_CONTROLS,
        "requires_confirmation": action in ("create", "update", "delete"),
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "owned_tables": OWNED_TABLES,
        "side_effects": (),
    }


def standalone_agent_workspace_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "routes": standalone_route_contracts()["routes"],
        "forms": STANDALONE_FORMS,
        "wizards": STANDALONE_WIZARDS,
        "controls": STANDALONE_CONTROLS,
        "skills": agent_skill_manifest()["skills"],
        "side_effects": (),
    }


def smoke_test():
    manifest = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan("signed IPS and client questionnaire", "create a new balanced household portfolio")
    crud = datastore_crud_plan("create", table="wealth_portfolio_management_client_portfolio", payload={"status": "draft"})
    rejected = datastore_crud_plan("update", table="foreign_table")
    workspace = standalone_agent_workspace_contract()
    return {
        "ok": manifest["ok"]
        and chatbot["ok"]
        and all(skill["requires_confirmation"] is True for skill in manifest["skills"])
        and document["ok"]
        and crud["ok"]
        and rejected["ok"] is False
        and workspace["ok"],
        "side_effects": (),
    }
