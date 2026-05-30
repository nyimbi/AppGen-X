"""Form contracts for the Renewables Asset Operations PBC."""
PBC_KEY = "renewables_asset_operations"


def form_catalog():
    forms = (
        {"id": "asset_hierarchy", "owned_table": "renewables_asset_operations_renewable_asset", "fields": ("site", "technology", "parent_asset", "oem", "model", "serial", "commissioned_on", "nameplate_mw", "grid_node"), "validations": ("parent child linkage", "technology profile")},
        {"id": "telemetry_meter_reconciliation", "owned_table": "renewables_asset_operations_generation_reading", "fields": ("source", "interval", "scada_mwh", "revenue_meter_mwh", "weather_quality", "correction_reason", "lineage"), "validations": ("source boundary", "tolerance", "late correction")},
        {"id": "curtailment_classification", "owned_table": "renewables_asset_operations_curtailment_event", "fields": ("initiator", "instruction_source", "start", "end", "mw_requested", "mw_delivered", "recoverable", "compensable", "evidence"), "validations": ("cause taxonomy", "dispatch evidence")},
        {"id": "availability_pack", "owned_table": "renewables_asset_operations_availability_record", "fields": ("technical_availability", "contractual_availability", "grid_adjusted_availability", "energy_based_availability", "exclusions", "period_lock"), "validations": ("denominator governance", "exclusion approval")},
        {"id": "ppa_obligation_calendar", "owned_table": "renewables_asset_operations_ppa_obligation", "fields": ("contract", "period", "guarantees", "notice_deadline", "settlement_due", "ld_trigger", "attachments"), "validations": ("calendar mapping", "settlement checklist")},
        {"id": "maintenance_work_planning", "owned_table": "renewables_asset_operations_maintenance_work", "fields": ("asset", "fault", "mw_at_risk", "spares", "weather_window", "crew", "criticality", "permit_to_work"), "validations": ("criticality score", "safety permit")},
        {"id": "site_inspection", "owned_table": "renewables_asset_operations_maintenance_work", "fields": ("template", "geo_stamp", "photos", "defects", "thermal_findings", "follow_on_work", "offline_sync_status"), "validations": ("defect classification", "evidence chain")},
        {"id": "safety_lockout", "owned_table": "renewables_asset_operations_maintenance_work", "fields": ("job_hazard_analysis", "switching_approval", "field_presence", "lockout_tagout", "remote_reset_allowed", "restore_confirmations"), "validations": ("permit gate", "dual confirmation")},
        {"id": "warranty_claim", "owned_table": "renewables_asset_operations_performance_ratio", "fields": ("component", "terms", "fault_recurrence", "outage_duration", "oem_notice_deadline", "evidence_bundle", "responsibility"), "validations": ("threshold", "commercial owner")},
        {"id": "performance_loss_rca", "owned_table": "renewables_asset_operations_performance_ratio", "fields": ("expected_mwh", "actual_mwh", "weather_normalization", "loss_bucket", "candidate_causes", "excluded_causes", "corrective_action"), "validations": ("root cause evidence", "recovery verification")},
        {"id": "storage_dispatch", "owned_table": "renewables_asset_operations_generation_reading", "fields": ("state_of_charge", "dispatch_instruction", "charge_mwh", "discharge_mwh", "round_trip_efficiency", "cycle_count", "degradation"), "validations": ("dispatch compliance", "warranty cycle evidence")},
        {"id": "environmental_sustainability", "owned_table": "renewables_asset_operations_renewables_asset_operations_control_assertion", "fields": ("spill", "waste", "water_use", "vegetation", "habitat", "ghg_impact", "permit"), "validations": ("environmental evidence", "permit linkage")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def form_for(form_id):
    for form in form_catalog()["forms"]:
        if form["id"] == form_id:
            return {"ok": True, "form": form, "side_effects": ()}
    return {"ok": False, "reason": "unknown_form", "side_effects": ()}


def smoke_test():
    return {"ok": len(form_catalog()["forms"]) >= 12 and form_for("curtailment_classification")["ok"], "side_effects": ()}
