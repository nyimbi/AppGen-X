"""Continuous controls for humanitarian relief operations."""
from __future__ import annotations
PBC_KEY = "humanitarian_relief_operations"
CONTROLS = (
    {"key":"assessment_completeness_control","asserts":"rapid and verified assessments include displacement, household, vulnerability, sector severity, confidence, and review status","blocks":("assessment_approval","distribution_planning")},
    {"key":"beneficiary_duplicate_control","asserts":"probable duplicate households require review and rationale before approval","blocks":("registration_approval","distribution_approval")},
    {"key":"aid_lot_safety_control","asserts":"expired, quarantined, or handling-incomplete lots cannot move or be distributed","blocks":("shipment_loading","handover")},
    {"key":"site_capacity_control","asserts":"distribution site capacity, staffing, time slots, and accessibility controls are within safe thresholds","blocks":("site_opening","distribution_approval")},
    {"key":"distribution_variance_control","asserts":"planned, loaded, handed-over, returned, damaged, and unaccounted quantities reconcile with approved reasons","blocks":("distribution_close",)},
    {"key":"cash_voucher_recovery_control","asserts":"failed payouts enter retry or recovery queue with approved closure outcome","blocks":("payout_batch_close",)},
    {"key":"partner_readiness_control","asserts":"partner due diligence, agreement, safeguarding, controls, and capacity are current","blocks":("partner_assignment",)},
    {"key":"protection_confidentiality_control","asserts":"sensitive narratives and survivor details are masked and only revealed through audited minimum disclosure","blocks":("unauthorized_access","donor_export")},
    {"key":"donor_earmark_control","asserts":"shipments and distributions comply with donor geography, sector, modality, and population restrictions","blocks":("operation_approval","donor_pack_signoff")},
    {"key":"dead_letter_operational_control","asserts":"sync failures, event replays, and payout exceptions have impact, replay safety, notes, and closure code","blocks":("dead_letter_close",)},
    {"key":"agent_guardrail_control","asserts":"assistant drafts are cited, redacted, owned-table scoped, and confirmation gated","blocks":("unconfirmed_mutation","foreign_table_access","unsafe_summary")},
)
def control_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROLS, "side_effects": ()}
def evaluate_control(control_key: str, context: dict | None = None) -> dict:
    context = dict(context or {})
    control = next((c for c in CONTROLS if c['key'] == control_key), None)
    if control is None:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    failures = tuple(item for item in context.get('failures', ()) if item in control['blocks'] or item == control_key)
    return {"ok": not failures, "control": control, "failures": failures, "blocked_actions": control['blocks'] if failures else (), "side_effects": ()}
def smoke_test() -> dict:
    return {"ok": len(CONTROLS) >= 11 and evaluate_control('assessment_completeness_control')['ok'], "side_effects": ()}
