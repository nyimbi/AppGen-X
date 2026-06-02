"""Workflow wizard contracts for the Project Portfolio Management PBC."""
from __future__ import annotations

PBC_KEY = "project_portfolio_management"


def wizard_catalog() -> dict:
    wizards = (
        {
            "id": "intake_to_business_case",
            "label": "Intake to business case",
            "steps": (
                "score readiness",
                "map strategic objectives",
                "extract assumptions",
                "assign accountable sponsor",
                "route remediation or business case drafting",
            ),
        },
        {
            "id": "score_and_prioritize",
            "label": "Score and prioritize portfolio",
            "steps": (
                "compile scoring model",
                "apply capital and capacity constraints",
                "build efficient frontier",
                "select scenario",
                "publish executive rationale",
            ),
        },
        {
            "id": "gate_governance",
            "label": "Gate governance",
            "steps": (
                "assemble required evidence",
                "check decision quorum",
                "record dissent",
                "set approval conditions",
                "emit gate decision",
            ),
        },
        {
            "id": "dependency_and_risk_review",
            "label": "Dependency and risk review",
            "steps": (
                "map predecessor and successor work",
                "propagate dependency risk",
                "identify correlated exposures",
                "route appetite breaches",
                "publish mitigation plan",
            ),
        },
        {
            "id": "capacity_conflict_resolution",
            "label": "Capacity conflict resolution",
            "steps": (
                "forecast demand",
                "compare available supply",
                "find scarce skills",
                "propose swaps and pauses",
                "confirm portfolio plan",
            ),
        },
        {
            "id": "benefits_realization_review",
            "label": "Benefits realization review",
            "steps": (
                "measure actuals",
                "test attribution",
                "detect leakage",
                "recommend intervention",
                "close or reopen benefit review",
            ),
        },
        {
            "id": "executive_scenario_planning",
            "label": "Executive scenario planning",
            "steps": (
                "change capital or capacity constraints",
                "simulate selected portfolio",
                "show risk and benefit tradeoffs",
                "narrate options",
                "save side-effect-free plan",
            ),
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def wizard_for(wizard_id: str) -> dict:
    for wizard in wizard_catalog()["wizards"]:
        if wizard["id"] == wizard_id:
            return {"ok": True, "wizard": wizard, "side_effects": ()}
    return {"ok": False, "reason": "unknown_wizard", "side_effects": ()}


def smoke_test() -> dict:
    catalog = wizard_catalog()
    return {
        "ok": len(catalog["wizards"]) >= 7 and wizard_for("score_and_prioritize")["ok"],
        "catalog": catalog,
        "side_effects": (),
    }
