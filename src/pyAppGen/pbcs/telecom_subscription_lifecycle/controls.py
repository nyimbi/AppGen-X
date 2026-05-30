"""Controls for Telecom Subscription Lifecycle."""
PBC_KEY = "telecom_subscription_lifecycle"
CONTROL_DEFINITIONS = {
    "subscription_has_customer_plan_and_identifier": ("customer_ref","plan_id","msisdn"),
    "plan_version_effective_and_eligible": ("effective_date","allowances","eligibility"),
    "sim_profile_identity_complete": ("iccid","imsi"),
    "esim_requires_eid_and_token": ("eid","profile_token"),
    "activation_ready_for_network_provisioning": ("identity_approved","plan_locked","sim_bound"),
    "port_out_requires_consent_and_no_recent_swap": ("authorization_proof","recent_swap_clear"),
    "roaming_high_cost_requires_confirmation": ("destination","spend_cap","confirmed"),
    "usage_threshold_action_has_policy": ("threshold_state","policy_action"),
    "retention_offer_requires_approval": ("save_offer","approval_required"),
    "agent_mutations_require_confirmation": ("confirmed",),
}
def evaluate_control(control_id, facts):
    required = CONTROL_DEFINITIONS.get(control_id, ())
    missing = tuple(name for name in required if facts.get(name) in (None, "", (), []))
    ok = not missing
    if control_id == "activation_ready_for_network_provisioning" and ok:
        ok = facts.get("identity_approved") is True and facts.get("plan_locked") is True and facts.get("sim_bound") is True
        missing = () if ok else ("activation_prerequisites",)
    if control_id == "port_out_requires_consent_and_no_recent_swap" and ok:
        ok = facts.get("recent_swap_clear") is True
        missing = () if ok else ("recent_swap_clear",)
    if control_id in ("roaming_high_cost_requires_confirmation", "agent_mutations_require_confirmation"):
        ok = facts.get("confirmed") is True
        missing = () if ok else ("confirmed",)
    return {"ok": ok, "control_id": control_id, "missing": missing, "side_effects": ()}
def control_catalog(): return {"ok": True, "pbc": PBC_KEY, "controls": tuple(CONTROL_DEFINITIONS), "side_effects": ()}
