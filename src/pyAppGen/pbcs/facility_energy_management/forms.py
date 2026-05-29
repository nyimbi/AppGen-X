"""Form catalog for the facility_energy_management PBC."""
from __future__ import annotations

PBC_KEY = "facility_energy_management"

FORM_CATALOG = (
    {
        "key": "meter_topology_form",
        "title": "Meter and submeter topology",
        "target_table": "facility_energy_management_energy_meter",
        "fields": (
            "meter_id", "parent_meter_id", "meter_role", "virtual_formula", "service_account",
            "premise_id", "tariff_eligibility", "tenant_tag", "commissioned_on", "heartbeat_minutes",
            "health_status", "calibration_evidence_uri",
        ),
        "validations": ("owned_meter_scope", "service_mapping_required", "stale_meter_block"),
        "permission": "facility_energy_management.update",
    },
    {
        "key": "interval_load_profile_form",
        "title": "Interval load profile import",
        "target_table": "facility_energy_management_load_profile",
        "fields": (
            "meter_id", "timezone", "interval_minutes", "channel", "observed_intervals",
            "estimated_intervals", "duplicate_policy", "provenance_code", "correction_reason",
            "source_document_uri",
        ),
        "validations": ("dst_boundary_check", "missing_interval_check", "provenance_required"),
        "permission": "facility_energy_management.create",
    },
    {
        "key": "tariff_signal_form",
        "title": "Tariff and demand determinant",
        "target_table": "facility_energy_management_tariff_signal",
        "fields": (
            "tariff_id", "utility", "season_calendar", "time_bands", "holiday_overrides",
            "ratchet_percent", "contract_demand_kw", "coincident_peak_window", "minimum_bill_rule",
        ),
        "validations": ("effective_window_required", "time_band_non_overlap", "demand_rule_complete"),
        "permission": "facility_energy_management.approve",
    },
    {
        "key": "equipment_schedule_form",
        "title": "HVAC schedule hierarchy and overrides",
        "target_table": "facility_energy_management_equipment_schedule",
        "fields": (
            "schedule_id", "hierarchy_level", "parent_schedule_id", "equipment_group", "zone_id",
            "occupied_hours", "holiday_calendar", "weather_thresholds", "lock_windows", "maintenance_blackouts",
        ),
        "validations": ("inheritance_resolves", "lock_window_respected", "conflict_free"),
        "permission": "facility_energy_management.update",
    },
    {
        "key": "demand_response_dispatch_form",
        "title": "Demand response dispatch",
        "target_table": "facility_energy_management_demand_response_event",
        "fields": (
            "event_id", "program", "notice_at", "starts_at", "ends_at", "eligible_assets",
            "excluded_tenants", "shed_capacity_kw", "acknowledged_by", "settlement_baseline_id",
            "rebound_plan",
        ),
        "validations": ("eligibility_required", "critical_load_excluded", "state_transition_valid"),
        "permission": "facility_energy_management.approve",
    },
    {
        "key": "baseline_version_form",
        "title": "Weather-normalized baseline",
        "target_table": "facility_energy_management_energy_baseline",
        "fields": (
            "baseline_id", "scope", "version", "effective_from", "effective_to", "method",
            "weather_source", "degree_day_model", "supersedes_baseline_id", "reviewer",
        ),
        "validations": ("no_overlapping_active_baseline", "weather_source_required", "reviewer_required"),
        "permission": "facility_energy_management.approve",
    },
    {
        "key": "control_assertion_form",
        "title": "Comfort and safety guardrail",
        "target_table": "facility_energy_management_facility_energy_management_control_assertion",
        "fields": (
            "assertion_id", "scope", "comfort_band", "ventilation_minimum", "freezer_limit",
            "pressure_relationship", "life_safety_constraint", "blocks_action_when_false",
        ),
        "validations": ("guardrail_has_scope", "thresholds_bounded", "blocker_explained"),
        "permission": "facility_energy_management.admin",
    },
)


def form_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "forms": FORM_CATALOG, "side_effects": ()}


def smoke_test() -> dict:
    forms = form_catalog()["forms"]
    return {
        "ok": len(forms) >= 7 and all(form["target_table"].startswith(f"{PBC_KEY}_") for form in forms),
        "form_count": len(forms),
        "side_effects": (),
    }
