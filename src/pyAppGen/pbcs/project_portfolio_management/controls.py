"""Governance controls for the Project Portfolio Management PBC."""
from __future__ import annotations

PBC_KEY = "project_portfolio_management"


def control_catalog() -> dict:
    controls = (
        ("intake_readiness_required", "blocking", "Initiatives below readiness floor enter remediation."),
        ("business_case_assumptions_current", "blocking", "Expired assumptions block case approval."),
        ("scoring_weights_balanced", "blocking", "Scoring weights must total one."),
        ("prioritization_must_fit_constraints", "blocking", "Selected portfolio must fit capital and capacity constraints."),
        ("gate_requires_evidence_and_quorum", "blocking", "Gate decisions need evidence and quorum."),
        ("resource_capacity_not_exceeded", "blocking", "Assignments cannot exceed available skill capacity."),
        ("benefit_claim_requires_attribution", "blocking", "Benefit claims require attribution evidence."),
        ("risk_appetite_breach_requires_acceptance", "blocking", "Risk appetite breaches require explicit acceptance."),
        ("financial_variance_requires_explanation", "blocking", "Material financial variance requires explanation."),
        ("agent_mutations_require_confirmation", "blocking", "Agent-authored datastore mutations require human confirmation."),
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": tuple({"id": cid, "severity": severity, "description": description} for cid, severity, description in controls),
        "side_effects": (),
    }


def evaluate_control(control_id: str, facts: dict | None = None) -> dict:
    facts = dict(facts or {})
    controls = {control["id"]: control for control in control_catalog()["controls"]}
    if control_id not in controls:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}

    failures: list[str] = []
    if control_id == "intake_readiness_required" and facts.get("score", 0) < facts.get("floor", 70):
        failures.append("readiness_low")
    elif control_id == "business_case_assumptions_current" and facts.get("expired_assumptions", 0) > 0:
        failures.append("assumption_expired")
    elif control_id == "scoring_weights_balanced" and round(sum(facts.get("weights", ())), 6) != 1:
        failures.append("weights_do_not_sum_to_one")
    elif control_id == "prioritization_must_fit_constraints" and (
        facts.get("cost", 0) > facts.get("budget", 0) or facts.get("demand", 0) > facts.get("capacity", 0)
    ):
        failures.append("constraint_breach")
    elif control_id == "gate_requires_evidence_and_quorum" and (not facts.get("evidence") or not facts.get("quorum")):
        failures.append("gate_evidence_or_quorum_missing")
    elif control_id == "resource_capacity_not_exceeded" and facts.get("demand", 0) > facts.get("supply", 0):
        failures.append("resource_overallocated")
    elif control_id == "benefit_claim_requires_attribution" and not facts.get("attribution"):
        failures.append("attribution_missing")
    elif control_id == "risk_appetite_breach_requires_acceptance" and facts.get("breach") and not facts.get("accepted"):
        failures.append("risk_acceptance_missing")
    elif control_id == "financial_variance_requires_explanation" and (
        abs(facts.get("variance", 0)) >= facts.get("materiality", 1) and not facts.get("explanation")
    ):
        failures.append("variance_unexplained")
    elif control_id == "agent_mutations_require_confirmation" and not facts.get("confirmed"):
        failures.append("confirmation_required")

    return {
        "ok": not failures,
        "control": controls[control_id],
        "failures": tuple(failures),
        "requires_exception": bool(failures),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": not evaluate_control("intake_readiness_required", {"score": 10})["ok"]
        and evaluate_control("gate_requires_evidence_and_quorum", {"evidence": ("case",), "quorum": True})["ok"]
        and not evaluate_control("scoring_weights_balanced", {"weights": (0.5, 0.5, 0.2)})["ok"],
        "side_effects": (),
    }
