"""Continuous controls for grant and fund accounting."""
from __future__ import annotations
PBC_KEY = "grant_fund_accounting"
CONTROLS = (
    {"key": "award_activation_control", "asserts": "award has source document, period, amount, restrictions, budget, match, reports, indirect rate, and closeout terms", "blocks": ("award_activation","cost_recording")},
    {"key": "award_lifecycle_control", "asserts": "award state allows spending, draws, reports, and closeout actions", "blocks": ("cost_recording","draw_submission","report_submission")},
    {"key": "restriction_allowability_control", "asserts": "costs satisfy period, purpose, budget, prior approval, procurement, match, and evidence rules", "blocks": ("cost_approval","draw_submission")},
    {"key": "budget_version_control", "asserts": "costs reference active budget version and do not exceed approved line authority", "blocks": ("cost_approval","rebudget_close")},
    {"key": "drawdown_readiness_control", "asserts": "draw contains only eligible, documented, paid or funder-eligible costs", "blocks": ("draw_submission",)},
    {"key": "draw_receipt_reconciliation_control", "asserts": "cash receipts reconcile to draw requests and rejected lines become exceptions", "blocks": ("draw_close","cash_reconciliation_close")},
    {"key": "match_shortfall_control", "asserts": "match requirements are scheduled, evidenced, valued, not double-counted, and forecast", "blocks": ("report_submission","closeout")},
    {"key": "report_to_ledger_control", "asserts": "funder reports reconcile to owned costs, budgets, draws, receipts, and match", "blocks": ("report_submission",)},
    {"key": "evidence_retention_control", "asserts": "compliance evidence has type, link, retention, reviewer, redaction, and cryptographic proof", "blocks": ("cost_approval","closeout")},
    {"key": "closeout_readiness_control", "asserts": "final costs, draws, reports, match, property, program income, and funder acceptance are complete", "blocks": ("grant_closeout",)},
    {"key": "agent_mutation_control", "asserts": "assistant extracts and CRUD plans are citation-backed, owned-table scoped, and confirmation gated", "blocks": ("unconfirmed_mutation","foreign_table_access")},
)
def control_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROLS, "side_effects": ()}
def evaluate_control(control_key: str, context: dict | None = None) -> dict:
    context = dict(context or {})
    control = next((c for c in CONTROLS if c["key"] == control_key), None)
    if control is None:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    failures = tuple(item for item in context.get("failures", ()) if item in control["blocks"] or item == control_key)
    return {"ok": not failures, "control": control, "failures": failures, "blocked_actions": control["blocks"] if failures else (), "side_effects": ()}
def smoke_test() -> dict:
    return {"ok": len(CONTROLS) >= 11 and evaluate_control("award_activation_control")["ok"], "side_effects": ()}
