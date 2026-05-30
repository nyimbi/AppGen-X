"""Operational controls for the Waste and Recycling Operations standalone app."""
PBC_KEY = "waste_recycling_operations"

CONTROL_DEFINITIONS = {
    "route_has_crew_vehicle_and_facility_window": ("crew_projection","vehicle_projection","facility_window"),
    "bin_has_identity_and_location": ("serial","rfid","location"),
    "pickup_has_proof_or_exception": ("outcome",),
    "material_stream_has_rules": ("accepted_materials","prohibited_materials","contamination_threshold"),
    "contamination_has_photo_and_notice": ("photo_digest","notice_required"),
    "disposal_ticket_weights_reconcile": ("gross_weight","tare_weight","net_weight"),
    "yield_has_reject_and_recovered_weight": ("inbound_weight","reject_weight","recovered_weight"),
    "hazardous_exception_blocks_normal_pickup": ("material_type","safety_instruction","route_hold"),
    "agent_mutations_require_confirmation": ("confirmed",),
}

def evaluate_control(control_id, facts):
    required = CONTROL_DEFINITIONS.get(control_id, ())
    missing = tuple(name for name in required if facts.get(name) in (None, "", (), []))
    ok = not missing
    if control_id == "disposal_ticket_weights_reconcile" and ok:
        ok = round(float(facts["gross_weight"]) - float(facts["tare_weight"]), 3) == round(float(facts["net_weight"]), 3)
        missing = () if ok else ("net_weight_mismatch",)
    if control_id == "pickup_has_proof_or_exception" and ok:
        ok = bool(facts.get("photo_digest") or facts.get("exception_code") or facts.get("lift_sensor_digest"))
        missing = () if ok else ("proof_or_exception",)
    if control_id == "agent_mutations_require_confirmation":
        ok = facts.get("confirmed") is True
        missing = () if ok else ("confirmed",)
    return {"ok": ok, "control_id": control_id, "missing": missing, "side_effects": ()}

def control_catalog():
    return {"ok": True, "pbc": PBC_KEY, "controls": tuple(CONTROL_DEFINITIONS), "side_effects": ()}
