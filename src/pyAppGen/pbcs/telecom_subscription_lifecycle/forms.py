"""Forms for the Telecom Subscription Lifecycle standalone app."""
PBC_KEY = "telecom_subscription_lifecycle"
FORMS = (
    {"key":"SubscriptionAggregateForm","owned_table":"telecom_subscription_lifecycle_subscriber_account","fields":("subscription_id","customer_ref","payer_ref","msisdn","plan_id","sim_id","state")},
    {"key":"ServicePlanVersionForm","owned_table":"telecom_subscription_lifecycle_service_plan","fields":("plan_id","market","channel","effective_date","allowances","contract_term","retired_at")},
    {"key":"SimEsimProfileForm","owned_table":"telecom_subscription_lifecycle_sim_profile","fields":("sim_id","iccid","imsi","eid","profile_token","state","assigned_subscription")},
    {"key":"ActivationRequestForm","owned_table":"telecom_subscription_lifecycle_activation_request","fields":("activation_id","subscription_id","identity_approved","plan_locked","sim_bound","provisioning_steps","ready_for_billing_handoff")},
    {"key":"UsageSessionForm","owned_table":"telecom_subscription_lifecycle_usage_session","fields":("usage_id","subscription_id","usage_type","quantity","unit","threshold_state","duplicate_key")},
    {"key":"RoamingEventForm","owned_table":"telecom_subscription_lifecycle_roaming_event","fields":("roaming_id","subscription_id","destination","partner_network","entitlement","spend_cap","confirmation_required")},
    {"key":"PortabilityCaseForm","owned_table":"telecom_subscription_lifecycle_activation_request","fields":("port_id","subscription_id","port_type","donor_network","authorization_proof","cutover_window","risk_flags")},
    {"key":"ChurnRiskForm","owned_table":"telecom_subscription_lifecycle_churn_risk","fields":("risk_id","subscription_id","reason_codes","score","save_offer","approval_required")},
    {"key":"SuspensionBarringForm","owned_table":"telecom_subscription_lifecycle_subscriber_account","fields":("subscription_id","reason","voice_barred","sms_barred","data_barred","roaming_barred","resume_condition")},
    {"key":"GovernedAssistantPreviewForm","owned_table":"telecom_subscription_lifecycle_governed_instruction_preview","fields":("document","instruction","candidate_table","requires_confirmation","preview_only")},
)
def form_catalog(): return {"ok": True, "pbc": PBC_KEY, "forms": FORMS, "side_effects": ()}
def form_for(key):
    form = next((item for item in FORMS if item["key"] == key), None)
    return {"ok": form is not None, "form": form, "side_effects": ()}
