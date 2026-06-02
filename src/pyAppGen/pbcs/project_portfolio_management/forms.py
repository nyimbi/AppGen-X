"""Professional form contracts for the Project Portfolio Management PBC."""
from __future__ import annotations

PBC_KEY = "project_portfolio_management"


def form_catalog() -> dict:
    forms = (
        {
            "id": "initiative_intake",
            "label": "Initiative intake",
            "owned_table": "project_portfolio_management_portfolio_item",
            "fields": (
                "title",
                "sponsor",
                "archetype",
                "strategic_objectives",
                "expected_benefits",
                "cost_basis",
                "risk_hypothesis",
                "resource_needs",
                "evidence",
                "readiness_score",
            ),
            "validations": ("readiness score", "sponsor authority", "strategic traceability"),
        },
        {
            "id": "business_case_assumptions",
            "label": "Business case assumptions",
            "owned_table": "project_portfolio_management_business_case",
            "fields": (
                "assumption",
                "owner",
                "confidence",
                "source",
                "expiry",
                "sensitivity",
                "validation_plan",
                "counterfactual",
            ),
            "validations": ("confidence", "expiry", "sensitivity coverage"),
        },
        {
            "id": "portfolio_scoring_model",
            "label": "Portfolio scoring model",
            "owned_table": "project_portfolio_management_portfolio_score",
            "fields": (
                "strategic_value",
                "financial_value",
                "execution_risk",
                "benefit_confidence",
                "regulatory_need",
                "weights",
                "model_version",
                "explanation",
            ),
            "validations": ("weights sum to one", "explainable score", "model version"),
        },
        {
            "id": "prioritization_run",
            "label": "Prioritization run",
            "owned_table": "project_portfolio_management_prioritization_run",
            "fields": (
                "budget",
                "capacity",
                "constraints",
                "scores",
                "pareto_frontier",
                "selected_items",
                "rejected_items",
                "executive_rationale",
            ),
            "validations": ("constraint fit", "executive rationale", "selection traceability"),
        },
        {
            "id": "stage_gate_decision",
            "label": "Stage gate decision",
            "owned_table": "project_portfolio_management_gate_decision",
            "fields": (
                "gate",
                "evidence",
                "quorum",
                "decision",
                "conditions",
                "dissent",
                "expiry",
                "next_review",
            ),
            "validations": ("required evidence", "decision authority", "dissent captured"),
        },
        {
            "id": "resource_capacity",
            "label": "Resource capacity and assignment",
            "owned_table": "project_portfolio_management_resource_assignment",
            "fields": (
                "skill",
                "period",
                "demand",
                "supply",
                "scarcity",
                "assignment",
                "conflict",
                "mitigation",
            ),
            "validations": ("capacity not overrun", "skill match", "scarcity highlighted"),
        },
        {
            "id": "benefit_realization",
            "label": "Benefit realization",
            "owned_table": "project_portfolio_management_benefit_realization",
            "fields": (
                "metric",
                "baseline",
                "target",
                "actual",
                "attribution",
                "confidence",
                "leakage",
                "intervention",
            ),
            "validations": ("attribution evidence", "overclaim guard", "confidence floor"),
        },
        {
            "id": "risk_issue_change",
            "label": "Risk, issue, and change control",
            "owned_table": "project_portfolio_management_portfolio_risk",
            "fields": (
                "risk",
                "correlation",
                "issue",
                "change_request",
                "portfolio_impact",
                "mitigation",
                "accepted_by",
                "accepted_until",
            ),
            "validations": ("risk appetite", "impact analysis", "exception owner"),
        },
        {
            "id": "financial_snapshot",
            "label": "Financial snapshot",
            "owned_table": "project_portfolio_management_portfolio_financial_snapshot",
            "fields": (
                "baseline",
                "forecast",
                "actual",
                "variance_driver",
                "funding_source",
                "contingency",
                "capitalization",
                "explanation",
            ),
            "validations": ("material variance explanation", "funding envelope", "capitalization policy"),
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def form_for(form_id: str) -> dict:
    for form in form_catalog()["forms"]:
        if form["id"] == form_id:
            return {"ok": True, "form": form, "side_effects": ()}
    return {"ok": False, "reason": "unknown_form", "side_effects": ()}


def smoke_test() -> dict:
    catalog = form_catalog()
    return {
        "ok": len(catalog["forms"]) >= 9 and form_for("prioritization_run")["ok"],
        "catalog": catalog,
        "side_effects": (),
    }
