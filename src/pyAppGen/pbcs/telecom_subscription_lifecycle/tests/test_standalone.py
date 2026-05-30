"""Standalone Telecom Subscription Lifecycle PBC tests."""
from pyAppGen.pbcs.telecom_subscription_lifecycle.standalone import (
    TelecomSubscriptionLifecycleStandaloneApp,
    single_pbc_app_contract,
    standalone_smoke_test,
)
from pyAppGen.pbcs.telecom_subscription_lifecycle.forms import form_catalog, form_for
from pyAppGen.pbcs.telecom_subscription_lifecycle.wizards import wizard_catalog, wizard_for
from pyAppGen.pbcs.telecom_subscription_lifecycle.controls import evaluate_control, control_catalog


def test_single_pbc_app_contract_surfaces_domain_runtime_ui_and_agent():
    contract = single_pbc_app_contract()
    assert contract["ok"] is True
    assert contract["pbc"] == "telecom_subscription_lifecycle"
    assert contract["event_contract"] == "AppGen-X"
    assert contract["stream_engine_picker_visible"] is False
    assert "postgresql" in contract["database_backends"]
    assert contract["schema"]["ok"] is True
    assert contract["services"]["ok"] is True
    assert contract["routes"]["ok"] is True
    assert contract["permissions"]["ok"] is True
    assert contract["ui"]["configuration_editor"] is True
    assert contract["ui"]["stream_engine_picker_visible"] is False
    assert contract["forms"]["ok"] is True
    assert contract["wizards"]["ok"] is True
    assert contract["controls"]["ok"] is True
    assert contract["agent"]["ok"] is True
    assert contract["composed_agent"]["single_agent_skill_namespace"] == "telecom_subscription_lifecycle_skills"
    assert contract["dsl"]["single_pbc_app"] is True


def test_forms_wizards_and_controls_cover_table_stakes_telecom_lifecycle():
    forms = {item["key"] for item in form_catalog()["forms"]}
    wizards = {item["key"] for item in wizard_catalog()["wizards"]}
    controls = set(control_catalog()["controls"])
    assert {
        "SubscriptionAggregateForm",
        "ServicePlanVersionForm",
        "SimEsimProfileForm",
        "ActivationRequestForm",
        "UsageSessionForm",
        "RoamingEventForm",
        "PortabilityCaseForm",
        "ChurnRiskForm",
        "SuspensionBarringForm",
        "GovernedAssistantPreviewForm",
    }.issubset(forms)
    assert {
        "NewActivationWizard",
        "EsimInstallWizard",
        "SimSwapControlWizard",
        "PortabilityCaseWizard",
        "RoamingShockProtectionWizard",
        "RetentionSaveWizard",
        "AssistantMutationPreviewWizard",
    }.issubset(wizards)
    assert {
        "subscription_has_customer_plan_and_identifier",
        "plan_version_effective_and_eligible",
        "sim_profile_identity_complete",
        "esim_requires_eid_and_token",
        "activation_ready_for_network_provisioning",
        "port_out_requires_consent_and_no_recent_swap",
        "roaming_high_cost_requires_confirmation",
        "usage_threshold_action_has_policy",
        "retention_offer_requires_approval",
        "agent_mutations_require_confirmation",
    }.issubset(controls)
    assert form_for("SubscriptionAggregateForm")["ok"] is True
    assert wizard_for("NewActivationWizard")["ok"] is True


def test_subscription_activation_roaming_churn_and_assistant_guardrails_execute():
    app = TelecomSubscriptionLifecycleStandaloneApp()
    assert app.configure()["ok"] is True
    assert app.define_plan("P1", "KE", "digital", "2026-06-01", {"data_gb": 20})["ok"] is True
    assert app.create_subscription("S-missing", None, "payer", "254700000", "P1")["ok"] is False
    assert app.create_subscription("S1", "cust-1", "payer", "254700000", "P1")["ok"] is True
    assert app.assign_sim("SIM-bad", "S1", "iccid", None)["ok"] is False
    assert app.assign_sim("SIM1", "S1", "iccid", "imsi")["ok"] is True
    assert app.request_activation("A-bad", "S1", True, True, False, ("hlr",))["ok"] is False
    assert app.request_activation("A1", "S1", True, True, True, ("hlr", "data_policy"))["ok"] is True
    assert app.complete_activation("A1")["ok"] is True
    assert app.subscriptions["S1"]["state"] == "active"
    assert app.open_port_case("PO-risk", "S1", "port_out", "donor", "auth", False)["ok"] is False
    assert app.open_port_case("PI1", "S1", "port_in", "donor", "auth")["ok"] is True
    assert app.record_usage("U1", "S1", "data", 18, "GB", "80_percent", "notify")["ok"] is True
    assert app.enable_roaming("R-risk", "S1", "high_cost_zone", "partner", "daily_pass", 100, False)["ok"] is False
    assert app.enable_roaming("R1", "S1", "high_cost_zone", "partner", "daily_pass", 100, True)["ok"] is True
    assert app.evaluate_churn("C1", "S1", ("price_pressure", "roaming_dissatisfaction"), .81, "roaming_pass_credit")["ok"] is True
    assert app.assistant_preview("port memo", "create activation review", False)["ok"] is False
    assert app.assistant_preview("port memo", "create activation review", True)["ok"] is True


def test_controls_fail_closed_for_high_risk_operations():
    assert evaluate_control("agent_mutations_require_confirmation", {"confirmed": False})["ok"] is False
    assert evaluate_control("roaming_high_cost_requires_confirmation", {"destination": "high_cost_zone", "spend_cap": 100, "confirmed": False})["missing"] == ("confirmed",)
    assert evaluate_control("port_out_requires_consent_and_no_recent_swap", {"authorization_proof": "auth", "recent_swap_clear": False})["missing"] == ("recent_swap_clear",)
    assert evaluate_control("activation_ready_for_network_provisioning", {"identity_approved": True, "plan_locked": True, "sim_bound": False})["missing"] == ("activation_prerequisites",)


def test_standalone_smoke_test_runs_end_to_end_without_side_effects():
    smoke = standalone_smoke_test()
    assert smoke["ok"] is True
    assert smoke["side_effects"] == ()
    assert smoke["runtime"]["ok"] is True
    assert smoke["contract"]["owned_tables"]
