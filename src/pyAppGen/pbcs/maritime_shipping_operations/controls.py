"""Maritime operations controls for the maritime_shipping_operations PBC."""
from __future__ import annotations
PBC_KEY = "maritime_shipping_operations"
CONTROL_CATALOG = (
    {"key":"voyage_readiness_control","title":"Vessel, crew-boundary, certificates, and rotation readiness","blocked_actions":("publish_voyage","commence_voyage"),"required_evidence":("vessel_ready","safe_manning_signal","certificates_valid","port_restrictions_checked")},
    {"key":"booking_acceptance_control","title":"Capacity, cutoff, sanctions, and special-cargo booking gate","blocked_actions":("accept_booking","issue_bill"),"required_evidence":("capacity_check","cutoff_status","restricted_party_screening","special_cargo_clearance")},
    {"key":"stowage_feasibility_control","title":"Stowage sequence, segregation, lashing, and reefer plug feasibility","blocked_actions":("finalize_load_list","approve_oog_dg_reefer"),"required_evidence":("stowage_plan","segregation_clearance","lashing_plan","reefer_or_special_evidence")},
    {"key":"port_call_sof_control","title":"Statement-of-facts chronology and timezone evidence","blocked_actions":("close_port_call","calculate_laytime"),"required_evidence":("nor_tendered","cargo_ops_events","timezone","attachments")},
    {"key":"demurrage_dossier_control","title":"Laytime trace and claim dossier completeness","blocked_actions":("submit_claim","settle_claim"),"required_evidence":("laytime_trace","charter_clauses","sof_package","approval_limit")},
    {"key":"bunker_carbon_control","title":"ROB, sulfur/ECA, variance, and carbon tradeoff approval","blocked_actions":("approve_bunker_plan","order_speedup"),"required_evidence":("rob_forecast","sulfur_context","variance_policy","carbon_tradeoff")},
    {"key":"compliance_obligation_control","title":"Customs, sanctions, corridor, and port-state obligation closure","blocked_actions":("depart_port","release_documents"),"required_evidence":("obligation_register","screening_disposition","filing_status","closure_evidence")},
)
def control_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROL_CATALOG, "side_effects": ()}
def evaluate_control(control_key: str, evidence: dict | None = None) -> dict:
    evidence=dict(evidence or {})
    matches=tuple(c for c in CONTROL_CATALOG if c["key"]==control_key)
    if not matches:
        return {"ok": False, "reason":"unknown_control", "side_effects": ()}
    control=matches[0]
    missing=tuple(x for x in control["required_evidence"] if x not in evidence)
    return {"ok": not missing and not evidence.get("unapproved_override", False), "control": control, "missing_evidence": missing, "blocked_actions": control["blocked_actions"] if missing else (), "side_effects": ()}
def smoke_test() -> dict:
    blocked=evaluate_control("booking_acceptance_control", {"capacity_check": True})
    return {"ok": len(CONTROL_CATALOG) >= 7 and blocked["ok"] is False and "accept_booking" in blocked["blocked_actions"], "side_effects": ()}
