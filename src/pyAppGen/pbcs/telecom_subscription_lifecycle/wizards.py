"""Guided workflows for Telecom Subscription Lifecycle."""
PBC_KEY = "telecom_subscription_lifecycle"
WIZARDS = (
    {"key":"NewActivationWizard","steps":("identity","plan_lock","sim_or_esim","provisioning","service_test","billing_handoff"),"forms":("SubscriptionAggregateForm","ActivationRequestForm")},
    {"key":"EsimInstallWizard","steps":("eid_capture","profile_reserve","token_issue","install_attempt","callback_or_timeout"),"forms":("SimEsimProfileForm",)},
    {"key":"SimSwapControlWizard","steps":("risk_check","identity_reverify","cool_off","prior_sim_deactivate","notify"),"forms":("SimEsimProfileForm",)},
    {"key":"PortabilityCaseWizard","steps":("authorization","donor_validation","risk_review","cutover","fallback"),"forms":("PortabilityCaseForm",)},
    {"key":"RoamingShockProtectionWizard","steps":("destination","entitlement","spend_cap","confirmation","partner_exception"),"forms":("RoamingEventForm",)},
    {"key":"RetentionSaveWizard","steps":("reason_codes","eligibility","offer_preview","approval","outcome"),"forms":("ChurnRiskForm",)},
    {"key":"AssistantMutationPreviewWizard","steps":("document_intake","owned_table_preview","human_confirmation","appgen_event_plan"),"forms":("GovernedAssistantPreviewForm",)},
)
def wizard_catalog(): return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARDS, "side_effects": ()}
def wizard_for(key):
    wizard = next((item for item in WIZARDS if item["key"] == key), None)
    return {"ok": wizard is not None, "wizard": wizard, "side_effects": ()}
