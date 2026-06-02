"""Executable controls for Telecom Network Operations."""
PBC_KEY = "telecom_network_operations"
CONTROL_DESCRIPTIONS = {
 "site_has_geospatial_identity":"Sites require code, coordinates, and site type before dependent topology can attach.",
 "radio_cell_has_parent_site":"Radio cell/sector identity must attach to an existing parent site.",
 "circuit_path_has_endpoints":"Circuit topology requires A-end, Z-end, route membership, and protection state.",
 "alarm_is_normalized":"Alarm events require normalized family, severity, probable cause, and object class.",
 "root_cause_correlation_has_parent":"Suppression requires a parent root-cause alarm or incident.",
 "outage_declaration_complete":"Declared outages require commander, impacted services, and lifecycle state.",
 "maintenance_has_rollback":"Planned work requires MOP version, rollback plan, scope, and no unapproved freeze conflict.",
 "sla_clock_exclusion_approved":"SLA exclusions require explicit approval and reason.",
 "capacity_headroom_positive":"Used plus reserved capacity cannot exceed installed capacity unless emergency headroom is declared.",
 "field_evidence_traceable":"Field closure requires evidence digest or closure note and site/case reference.",
 "agent_mutations_require_confirmation":"Assistant-proposed mutations require human confirmation.",
}

def _failures(control, facts):
    facts=dict(facts or {})
    if control == "site_has_geospatial_identity": return tuple(k for k in ("site_code","latitude","longitude","site_type") if facts.get(k) in (None,""))
    if control == "radio_cell_has_parent_site": return () if facts.get("site_id") and facts.get("technology") and facts.get("sector") else ("parent_site_or_radio_identity_missing",)
    if control == "circuit_path_has_endpoints": return tuple(k for k in ("a_end","z_end","route_membership","protected") if facts.get(k) in (None,""))
    if control == "alarm_is_normalized": return tuple(k for k in ("normalized_family","severity","probable_cause","object_class") if not facts.get(k))
    if control == "root_cause_correlation_has_parent": return () if facts.get("parent") else ("root_cause_parent_missing",)
    if control == "outage_declaration_complete": return tuple(k for k in ("state","bridge_commander","impacted_services") if not facts.get(k))
    if control == "maintenance_has_rollback":
        failures=tuple(k for k in ("mop_version","rollback_plan","scope") if not facts.get(k))
        return failures + (("freeze_window_unapproved",) if facts.get("freeze_window") and not facts.get("freeze_exception") else ())
    if control == "sla_clock_exclusion_approved": return () if not facts.get("excluded") or (facts.get("exclusion_approved") and facts.get("reason")) else ("sla_exclusion_unapproved",)
    if control == "capacity_headroom_positive": return () if (facts.get("installed",0) >= facts.get("used",0)+facts.get("reserved",0)) or facts.get("emergency_headroom") else ("capacity_overcommitted",)
    if control == "field_evidence_traceable": return () if facts.get("case_id") and (facts.get("evidence_digest") or facts.get("closure_note")) else ("field_evidence_missing",)
    if control == "agent_mutations_require_confirmation": return () if facts.get("confirmed") else ("human_confirmation_required",)
    return ("unknown_control",)

def evaluate_control(control, facts=None):
    failures=_failures(control, facts or {})
    return {"ok": not failures, "pbc": PBC_KEY, "control": control, "description": CONTROL_DESCRIPTIONS.get(control,"unknown"), "failures": failures, "facts": dict(facts or {}), "side_effects": ()}
def control_catalog(): return {"ok": True, "pbc": PBC_KEY, "controls": tuple({"key": k, "description": v, "explainable": True} for k,v in CONTROL_DESCRIPTIONS.items()), "side_effects": ()}
def smoke_test(): return {"ok": control_catalog()["ok"] and evaluate_control("site_has_geospatial_identity", {"site_code":"S"})["ok"] is False and evaluate_control("agent_mutations_require_confirmation", {"confirmed": True})["ok"] is True, "side_effects": ()}
