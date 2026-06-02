"""Field-ready forms for the mining_safety_permits PBC."""
from __future__ import annotations
PBC_KEY = "mining_safety_permits"

def form_catalog() -> dict:
    forms = (
        {"id":"permit_to_work_register","owned_table":"mining_safety_permits_mine_permit","fields":("permit_class","area","start_hour","expiry_hour","simops_flags","issuer","crew","assets","control_bundle"),"validations":("permit class required","expiry after start","critical controls mapped")},
        {"id":"isolation_lockout_verification","owned_table":"mining_safety_permits_control_action","fields":("energy_sources","isolation_points","lock_tag_ids","applied_by","verified_by","zero_energy_confirmed","boundary_version"),"validations":("multi point isolation complete","zero energy proof required","boundary versioned")},
        {"id":"confined_space_gas_test","owned_table":"mining_safety_permits_safety_inspection","fields":("space_id","instrument_id","bump_tested","tester_competency","readings","limits","tested_at_hour","valid_until_hour","ventilation_status"),"validations":("instrument bump test required","readings within limits","retest interval enforced")},
        {"id":"ground_control_assessment","owned_table":"mining_safety_permits_safety_inspection","fields":("support_type","last_scaling_hour","geo_inspection","seismic_alert","water_ingress","unsupported_span_risk","defects"),"validations":("geo evidence required","high defects open exception","area barricade captured")},
        {"id":"blast_plan_clearance","owned_table":"mining_safety_permits_blast_plan","fields":("shotfirer","magazine_issue","hole_readiness","exclusion_zone","firing_window","circuit_check","misfire_plan","reentry_checks"),"validations":("shotfirer authorized","exclusion signed","reentry evidence complete")},
        {"id":"shift_handover","owned_table":"mining_safety_permits_shift_roster","fields":("outgoing_supervisor","incoming_supervisor","active_permits","open_isolations","changed_conditions","pending_retests","open_exceptions"),"validations":("incoming acknowledgement required","open items visible","handover cannot hide active risk")},
        {"id":"incident_precursor_report","owned_table":"mining_safety_permits_incident_report","fields":("event_type","area","linked_permit","severity","immediate_hold","evidence","corrective_actions","regulator_notifiable"),"validations":("high potential escalated","evidence preserved","corrective owner assigned")},
        {"id":"regulatory_evidence_pack","owned_table":"mining_safety_permits_regulatory_submission","fields":("permit_ids","gas_tests","isolations","handovers","inspections","incidents","event_history","export_hash"),"validations":("pack reproducible","artifact hashes included","submission scope explicit")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}

def form_for(form_id: str) -> dict:
    for form in form_catalog()["forms"]:
        if form["id"] == form_id:
            return {"ok": True, "form": form, "side_effects": ()}
    return {"ok": False, "reason": "unknown_form", "side_effects": ()}

def smoke_test() -> dict:
    return {"ok": len(form_catalog()["forms"]) >= 8 and form_for("blast_plan_clearance")["ok"], "side_effects": ()}
