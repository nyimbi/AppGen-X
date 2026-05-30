"""Guided maritime workflows for the maritime_shipping_operations PBC."""
from __future__ import annotations
PBC_KEY = "maritime_shipping_operations"
WIZARD_CATALOG = (
    {"key":"voyage_publish_wizard","title":"Plan, validate, and publish a voyage rotation","steps":("register_vessel","build_legs","apply_port_restrictions","check_bunker_plan","confirm_readiness","publish_voyage"),"owned_tables":("maritime_shipping_operations_voyage","maritime_shipping_operations_vessel"),"emits":("MaritimeShippingOperationsCreated",)},
    {"key":"booking_to_bill_wizard","title":"Accept cargo and issue bill of lading","steps":("screen_parties","reserve_capacity","validate_cutoffs","check_special_cargo","draft_bill","approve_issue"),"owned_tables":("maritime_shipping_operations_cargo_booking",),"emits":("MaritimeShippingOperationsApproved",)},
    {"key":"port_call_execution_wizard","title":"Execute port call and capture statement of facts","steps":("nominate_terminal","confirm_berth_window","order_pilot_tugs_gang","capture_sof_events","resolve_rollover","depart_call"),"owned_tables":("maritime_shipping_operations_port_call",),"emits":("MaritimeShippingOperationsUpdated",)},
    {"key":"laytime_demurrage_wizard","title":"Compute laytime and assemble demurrage claim","steps":("load_charter_clauses","replay_sof","stop_resume_clock","calculate_exposure","build_dossier","submit_or_rebut"),"owned_tables":("maritime_shipping_operations_charter_party","maritime_shipping_operations_demurrage_claim"),"emits":("MaritimeShippingOperationsExceptionOpened",)},
    {"key":"bunker_carbon_wizard","title":"Choose bunker plan with ROB, cost, and carbon tradeoffs","steps":("forecast_rob","compare_uplift_ports","validate_sulfur_and_eca","estimate_emissions","approve_plan","track_variance"),"owned_tables":("maritime_shipping_operations_bunker_event","maritime_shipping_operations_voyage"),"emits":("MaritimeShippingOperationsApproved",)},
    {"key":"compliance_restriction_wizard","title":"Clear voyage compliance and restricted corridor obligations","steps":("create_register","screen_parties","check_port_corridor_rules","track_filings","seal_audit_package","escalate_breach"),"owned_tables":("maritime_shipping_operations_maritime_shipping_operations_control_assertion",),"emits":("MaritimeShippingOperationsExceptionOpened",)},
    {"key":"schedule_recovery_wizard","title":"Simulate and approve schedule recovery options","steps":("detect_slip","model_skip_swap_speedup","compare_customer_cost_carbon","preview_mutations","approve_plan","notify_dependents"),"owned_tables":("maritime_shipping_operations_voyage","maritime_shipping_operations_port_call","maritime_shipping_operations_cargo_booking"),"emits":("MaritimeShippingOperationsUpdated",)},
)
def wizard_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARD_CATALOG, "side_effects": ()}
def smoke_test() -> dict:
    return {"ok": len(WIZARD_CATALOG) >= 7 and all(w["owned_tables"] for w in WIZARD_CATALOG), "side_effects": ()}
