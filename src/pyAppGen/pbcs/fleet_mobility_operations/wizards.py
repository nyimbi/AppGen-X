"""Guided workflows for fleet mobility operations."""
from __future__ import annotations
PBC_KEY = "fleet_mobility_operations"
WIZARDS = (
    {"key": "dispatch_readiness_wizard", "title": "Clear vehicle and driver for dispatch", "steps": ("check_vehicle_status","check_driver_credentials","check_rest_window","check_route_fit","confirm_assignment"), "outputs": ("dispatch_verdict","blocked_reasons","assignment_preview")},
    {"key": "live_reallocation_wizard", "title": "Reallocate after disruption", "steps": ("select_late_route","find_replacement_vehicle","find_eligible_driver","simulate_eta","preview_reassignment","confirm_handoff"), "outputs": ("replan_preview","audit_event","route_reprojection")},
    {"key": "telematics_quarantine_wizard", "title": "Resolve malformed device traffic", "steps": ("inspect_payload","verify_device_identity","check_timestamp_window","dedupe_replay","accept_or_quarantine"), "outputs": ("quarantine_decision","dead_letter_record","freshness_update")},
    {"key": "roadside_incident_wizard", "title": "Run roadside incident command", "steps": ("locate_vehicle","confirm_driver_status","request_tow_or_support","dispatch_replacement","close_return_to_road"), "outputs": ("incident_timeline","replacement_dispatch","readiness_restored_event")},
    {"key": "fuel_fraud_investigation_wizard", "title": "Investigate abnormal burn or card use", "steps": ("compare_fuel_transaction","compare_odometer_delta","check_idle_time","check_geofence","open_or_resolve_exception"), "outputs": ("fraud_score","investigation_notes","exception_state")},
    {"key": "maintenance_planner_wizard", "title": "Plan workshop and return-to-road", "steps": ("project_horizon","reserve_bay","check_parts","hold_routes","clear_return_to_road"), "outputs": ("maintenance_plan","dispatch_hold","return_to_road_evidence")},
)
def wizard_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARDS, "side_effects": ()}
def smoke_test() -> dict:
    return {"ok": len(WIZARDS) >= 6 and all(len(w["steps"]) >= 5 for w in WIZARDS), "side_effects": ()}
