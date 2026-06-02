"""Guided workflows for the facility_energy_management PBC."""
from __future__ import annotations

PBC_KEY = "facility_energy_management"

WIZARDS = (
    {
        "key": "meter_commissioning_wizard",
        "title": "Commission a meter hierarchy",
        "steps": ("map_service_point", "attach_parent_meter", "verify_heartbeat", "upload_calibration", "approve_active_use"),
        "outputs": ("meter_topology", "health_queue_entry", "rollup_reconciliation"),
    },
    {
        "key": "interval_correction_wizard",
        "title": "Correct estimated interval reads",
        "steps": ("select_profile", "compare_raw_estimated_corrected", "capture_reason", "preview_reprocessing", "confirm_outbox_refresh"),
        "outputs": ("corrected_profile", "supersession_trace", "projection_refresh_event"),
    },
    {
        "key": "tariff_scenario_wizard",
        "title": "Compare tariff scenarios",
        "steps": ("choose_baseline_load", "select_current_tariff", "select_candidate_tariff", "compute_demand_determinants", "review_cost_delta"),
        "outputs": ("scenario_report", "demand_charge_breakdown", "no_mutation_analysis"),
    },
    {
        "key": "demand_response_dispatch_wizard",
        "title": "Dispatch and settle demand response",
        "steps": ("validate_asset_eligibility", "notify_operators", "capture_acknowledgement", "track_execution", "measure_settlement", "stage_rebound"),
        "outputs": ("dispatch_timeline", "settlement_summary", "rebound_plan"),
    },
    {
        "key": "anomaly_investigation_wizard",
        "title": "Investigate baseload, drift, and HVAC faults",
        "steps": ("open_case_pack", "inspect_meter_context", "compare_schedule_state", "review_tariff_band", "accept_or_dismiss_recommendation"),
        "outputs": ("exception_case_pack", "operator_feedback", "next_best_action"),
    },
    {
        "key": "baseline_versioning_wizard",
        "title": "Approve a weather-normalized baseline version",
        "steps": ("select_scope", "choose_method", "load_weather_source", "check_overlap", "approve_supersession"),
        "outputs": ("baseline_version", "weather_normalization_trace", "approval_evidence"),
    },
)


def wizard_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARDS, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": len(WIZARDS) >= 6 and all(len(wizard["steps"]) >= 5 for wizard in WIZARDS), "side_effects": ()}
