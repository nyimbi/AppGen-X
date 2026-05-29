"""Package-local guided wizards for the Energy Trading and Risk workbench."""

from __future__ import annotations

from .forms import energy_trading_risk_form_catalog


ENERGY_TRADING_RISK_WIZARDS = (
    {
        "wizard_id": "trade_capture_release",
        "title": "Trade capture and release",
        "goal": "Capture a trade, validate market data, and clear risk gates before booking.",
        "steps": (
            {"step_id": "capture_trade", "label": "Capture trade", "form_id": "energy_trade_capture", "operation": "command_trade_position"},
            {"step_id": "check_market_curve", "label": "Check market curve", "form_id": "price_curve_publish", "operation": "command_market_price_curve"},
            {"step_id": "review_limits", "label": "Review limits", "form_id": "exposure_limit_setup", "operation": "command_exposure_limit"},
            {"step_id": "review_decision", "label": "Review workbench", "form_id": "energy_trade_capture", "operation": "query_workbench"},
        ),
    },
    {
        "wizard_id": "nomination_exception_recovery",
        "title": "Nomination exception recovery",
        "goal": "Resolve post-cutoff nominations without losing version lineage.",
        "steps": (
            {"step_id": "submit_nomination", "label": "Submit nomination", "form_id": "nomination_submission", "operation": "command_nomination"},
            {"step_id": "review_schedule", "label": "Review schedule", "form_id": "schedule_submission", "operation": "command_schedule"},
            {"step_id": "verify_workbench", "label": "Verify queue", "form_id": "nomination_submission", "operation": "query_workbench"},
        ),
    },
    {
        "wizard_id": "end_of_day_risk_review",
        "title": "End-of-day risk review",
        "goal": "Refresh curves, inspect net exposure buckets, and confirm release readiness.",
        "steps": (
            {"step_id": "refresh_curve", "label": "Refresh market curve", "form_id": "price_curve_publish", "operation": "command_market_price_curve"},
            {"step_id": "check_limits", "label": "Check limit coverage", "form_id": "exposure_limit_setup", "operation": "command_exposure_limit"},
            {"step_id": "inspect_controls", "label": "Inspect controls", "form_id": "energy_trade_capture", "operation": "energy_risk_controls"},
            {"step_id": "capture_settlement", "label": "Capture settlement", "form_id": "settlement_capture", "operation": "command_settlement"},
        ),
    },
)



def energy_trading_risk_wizard_catalog() -> dict:
    forms = energy_trading_risk_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in ENERGY_TRADING_RISK_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(ENERGY_TRADING_RISK_WIZARDS) and not missing_form_bindings,
        "pbc": "energy_trading_risk",
        "wizards": ENERGY_TRADING_RISK_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in ENERGY_TRADING_RISK_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }



def energy_trading_risk_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    wizard = next((item for item in ENERGY_TRADING_RISK_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}
    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "trade_capture_release" and step["step_id"] != "capture_trade" and not supplied.get("trade_id"):
            blocked_by = ("trade_id",)
        if wizard_id == "nomination_exception_recovery" and step["step_id"] == "review_schedule" and not supplied.get("nomination_id"):
            blocked_by = ("nomination_id",)
        planned_steps.append({**step, "position": position, "ready": not blocked_by, "blocked_by": blocked_by})
    return {
        "ok": True,
        "pbc": "energy_trading_risk",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }



def smoke_test() -> dict:
    catalog = energy_trading_risk_wizard_catalog()
    plan = energy_trading_risk_plan_wizard("trade_capture_release", {"trade_id": "TRADE-1"})
    return {"ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]), "catalog": catalog, "plan": plan, "side_effects": ()}
