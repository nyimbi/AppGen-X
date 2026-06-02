"""Executable improve1 controls for the Telecom Subscription Lifecycle PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    TELECOM_SUBSCRIPTION_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
    TELECOM_SUBSCRIPTION_LIFECYCLE_CONSUMED_EVENT_TYPES,
    TELECOM_SUBSCRIPTION_LIFECYCLE_OWNED_TABLES,
    TELECOM_SUBSCRIPTION_LIFECYCLE_REQUIRED_EVENT_TOPIC,
    TELECOM_SUBSCRIPTION_LIFECYCLE_RUNTIME_TABLES,
)

PBC_KEY = "telecom_subscription_lifecycle"
EVENT_CONTRACT = "AppGen-X"
SUBSCRIPTION_ALLOWED_DATABASE_BACKENDS = TELECOM_SUBSCRIPTION_LIFECYCLE_ALLOWED_DATABASE_BACKENDS
SUBSCRIPTION_REQUIRED_EVENT_TOPIC = TELECOM_SUBSCRIPTION_LIFECYCLE_REQUIRED_EVENT_TOPIC
SUBSCRIPTION_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in SUBSCRIPTION_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in SUBSCRIPTION_CAPABILITIES}
SUBSCRIPTION_OWNED_TABLES = tuple(
    dict.fromkeys(
        TELECOM_SUBSCRIPTION_LIFECYCLE_OWNED_TABLES
        + TELECOM_SUBSCRIPTION_LIFECYCLE_RUNTIME_TABLES
        + tuple(f"telecom_subscription_lifecycle_{capability.slug}_control" for capability in SUBSCRIPTION_CAPABILITIES)
    )
)
SUBSCRIPTION_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        TELECOM_SUBSCRIPTION_LIFECYCLE_CONSUMED_EVENT_TYPES
        + (
            "PolicyChanged",
            "CustomerUpdated",
            "SupplierQualified",
            "IdentityVerified",
            "SimFulfillmentUpdated",
            "EsimProfileStatusChanged",
            "ProvisioningOrderUpdated",
            "PortabilityStatusChanged",
            "UsageRatedExternally",
            "BillingDisputeOpened",
            "CustomerNotificationQueued",
            "PaymentEligibilityChanged",
            "RoamingPartnerStatusChanged",
            "FraudRiskChanged",
            "DocumentReceived",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "brand_id",
    "market_id",
    "subscription_id",
    "subscriber_account_id",
    "policy_version",
    "operator_id",
    "evidence_references",
)
_FIELD_ROWS = """
1|subscription_aggregate_id,customer_party_ref,billing_party_ref,line_or_seat,msisdn,current_plan,active_sim_profile
2|state_machine_id,current_state,next_state,allowed_transition,actor_rule,event_mapping,invalid_transition_reason
3|telecom_identifier_id,msisdn,iccid,imsi,eid,activation_code,identifier_history
4|relationship_rule_id,subscriber_role,payer_role,account_owner_role,sponsor_role,delegated_admin_role,approval_path
5|sim_inventory_id,sim_state,warehouse_reference,courier_reference,assignment_state,delivery_projection,boundary_note
6|esim_flow_id,eid,profile_reservation,download_token,installation_attempt,timeout_handling,assisted_activation
7|sim_swap_control_id,swap_type,cool_off_rule,identity_reverification,fraud_alert,prior_sim_deactivation,customer_notification
8|plan_version_id,market,channel,segment,effective_date,allowance_set,retirement_date
9|plan_eligibility_id,commercial_model,network_technology,device_class,credit_posture,esim_support,compatibility_decision
10|future_plan_change_id,effective_date,cancellation_window,dependency_check,conflict_state,customer_intent,execution_status
11|addon_catalog_id,addon_category,stacking_rule,exclusivity_rule,prerequisite,expiry_rule,base_plan_impact
12|addon_semantics_id,depletion_rule,rollover_rule,proration_rule,renewal_rule,grace_use,threshold_interaction
13|activation_decomposition_id,identity_step,subscription_validation,plan_lock,sim_binding,provisioning_order,ready_for_billing_handoff
14|provisioning_dependency_id,domain,subscriber_registry_status,data_policy_status,voice_feature_status,apn_default_status,partner_entitlement
15|activation_rollback_id,failure_type,sim_unbind,esim_cancel,feature_reversal,billing_release_suppression,intervention_queue
16|portability_case_id,port_type,donor_network,recipient_network,validation_stage,cutover_window,fallback_path
17|port_in_validation_id,identity_match,account_number_match,authorization_proof,number_status,donor_response,cutover_date
18|port_out_protection_id,transfer_lock,recent_swap_cooling,high_risk_channel,extra_identity_check,consent_proof,escalation_state
19|suspension_lifecycle_id,suspension_reason,voice_state,sms_state,data_state,roaming_state,resume_condition
20|threshold_action_id,threshold_type,percentage,hard_cap,fair_use_throttle,roaming_spend_block,auto_unblock
21|usage_normalization_id,usage_type,time_zone,session_source,duplicate_check,unit_conversion,charge_advice_event
22|threshold_notification_id,usage_threshold,preference_set,customer_message,agent_alert,intervention_recommendation,deduplication_key
23|shared_pool_id,pool_owner_line,member_line_set,allocation_policy,reserve_capacity,priority_rule,member_throttle
24|roaming_entitlement_id,zone,destination_group,included_country,pass_type,permanent_restriction,partner_eligibility
25|roaming_spend_control_id,spend_cap,session_cutoff,default_off_destination,customer_confirmation,reenable_status,upgrade_option
26|roaming_exception_id,visited_network,partner_failure,entitlement_status,provisioning_lag,manual_override,remediation_owner
27|billing_boundary_id,charge_advice,proration_preview,allowance_consumption,effective_date_decision,invoice_ownership_block,tax_ownership_block
28|commercial_model_id,prepaid_bucket,postpaid_exposure,hybrid_rule,recharge_dependency,grace_period,reserve_threshold
29|charge_preview_id,proration_direction,one_time_fee,contract_impact,addon_carryover,next_cycle_effect,estimate_label
30|dispute_evidence_id,invoice_reference,subscription_event_set,usage_session_set,roaming_activity_set,threshold_notification_set,ledger_mutation_block
31|churn_reason_id,reason_code,coverage_issue,price_pressure,provisioning_failure,bill_shock,competitor_port_intent
32|retention_offer_id,offer_type,eligibility_rule,margin_guardrail,approval_threshold,save_journey,outcome_record
33|cancellation_lifecycle_id,cancel_state,grace_timer,number_quarantine,win_back_window,reactivation_rule,evidence_retention
34|self_service_workbench_id,plan_detail,active_addon_set,sim_status,usage_threshold,roaming_control,pending_change
35|agent_queue_id,queue_type,next_action,blocking_dependency,skill_level,sla_badge,customer_impact
36|agent_skill_id,skill_name,read_scope,allowed_mutation_set,mandatory_confirmation,approval_point,preview_payload
37|event_taxonomy_id,event_name,schema_version,business_milestone,payload_contract,consumer_hint,record_snapshot
38|event_ordering_id,idempotency_key,correlation_id,causation_id,replay_rule,ordering_rule,coherent_history
39|exception_taxonomy_id,exception_category,severity,owner_role,retry_policy,customer_impact,closure_evidence
40|release_flow_matrix_id,journey_name,test_reference,screenshot_reference,event_trace,rollback_note,release_check
41|operational_sla_id,sla_type,target_duration,aging_bucket,queue_level,exception_level,breach_indicator
42|parameter_governance_id,parameter_name,proposed_value,impact_preview,approval_threshold,history,activation_state
43|audit_trail_id,actor_type,channel,session_provenance,device_fingerprint,approval_path,notification_link
44|tenant_market_isolation_id,brand_scope,market_scope,numbering_rule,roaming_zone,suspension_policy,leakage_check
45|document_intake_id,document_type,authorization_form,identity_document,corporate_approval,consent_artifact,source_span
46|test_data_factory_id,fixture_type,msisdn_pool,iccid_value,eid_value,plan_structure,failure_mode
47|scenario_simulation_id,scenario_type,current_path,proposed_path,predicted_outcome,confirmed_state_label,risk_note
48|reconciliation_control_id,subscription_status,sim_assignment,provisioning_confirmation,usage_evidence,billing_reference,mismatch_flag
49|api_hardening_id,endpoint,idempotency_key,async_status,domain_error_code,evidence_link,dependency_delay
50|readiness_scorecard_id,domain_area,test_reference,workbench_evidence,event_trace,runbook_reference,approval_status
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    4: ("CustomerUpdated",),
    5: ("SimFulfillmentUpdated", "SupplierQualified"),
    6: ("EsimProfileStatusChanged",),
    7: ("FraudRiskChanged", "CustomerNotificationQueued"),
    13: ("IdentityVerified", "ProvisioningOrderUpdated"),
    14: ("ProvisioningOrderUpdated",),
    16: ("PortabilityStatusChanged",),
    18: ("FraudRiskChanged", "PortabilityStatusChanged"),
    22: ("CustomerNotificationQueued",),
    26: ("RoamingPartnerStatusChanged",),
    30: ("BillingDisputeOpened", "UsageRatedExternally"),
    42: ("PolicyChanged",),
    45: ("DocumentReceived",),
    50: ("PolicyChanged", "CustomerUpdated", "SupplierQualified"),
}
_SUBSCRIPTION_IDENTITY_FEATURES = (1, 2, 3, 4, 5, 6, 7, 13, 15, 33, 43, 44, 46, 50)
_PLAN_ACTIVATION_FEATURES = (8, 9, 10, 11, 12, 13, 14, 15, 27, 28, 29, 34, 35, 40, 49, 50)
_PORT_USAGE_ROAMING_FEATURES = (16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 48, 50)
_CHURN_GOVERNANCE_FEATURES = (31, 32, 36, 37, 38, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50)
_AGENT_FEATURES = (7, 29, 30, 31, 32, 36, 45, 47, 50)
_HUMAN_CONFIRMATION_FEATURES = (7, 10, 13, 15, 16, 18, 19, 25, 29, 32, 33, 36, 42, 45, 47, 50)
_APPROVAL_REQUIRED_FEATURES = (7, 15, 18, 25, 32, 33, 36, 42, 45, 50)
_NON_MUTATING_FEATURES = (9, 10, 21, 22, 27, 29, 30, 31, 36, 40, 41, 42, 44, 46, 47, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (4, 5, 13, 14, 27, 30, 48)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"telecom_subscription_lifecycle_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"TelecomSubscriptionLifecycle{_camel(capability.slug)}Panel",
        "route": f"POST /telecom-subscription-lifecycle/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in SUBSCRIPTION_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({
        "database_backend": "postgresql",
        "event_contract": EVENT_CONTRACT,
        "event_topic": SUBSCRIPTION_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "subscription_identity_evidence_complete": True,
        "plan_activation_evidence_complete": True,
        "port_usage_roaming_evidence_complete": True,
        "churn_governance_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned subscription model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _SUBSCRIPTION_IDENTITY_FEATURES and payload.get("subscription_identity_evidence_complete") is not True:
        findings.append("subscription identity evidence is required for canonical aggregate, lifecycle states, identifiers, customer roles, SIM/eSIM flows, swap controls, activation rollback, cancellation, audit, market isolation, test data, and readiness proof")
    if number in _PLAN_ACTIVATION_FEATURES and payload.get("plan_activation_evidence_complete") is not True:
        findings.append("plan and activation evidence is required for plan versioning, eligibility, future changes, add-ons, activation, provisioning, rollback, billing boundary, commercial models, previews, workbenches, queues, release flows, APIs, and readiness")
    if number in _PORT_USAGE_ROAMING_FEATURES and payload.get("port_usage_roaming_evidence_complete") is not True:
        findings.append("portability, usage, roaming, threshold, shared-pool, billing dispute, reconciliation, and readiness evidence is required")
    if number in _CHURN_GOVERNANCE_FEATURES and payload.get("churn_governance_evidence_complete") is not True:
        findings.append("churn, retention, agent playbooks, event taxonomy, idempotency, exceptions, release evidence, SLAs, policy parameters, document intake, test data, simulations, reconciliation, API hardening, and go-live evidence is required")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("SIM swap, future changes, activation, rollback, portability, suspension, roaming spend, previews, retention, cancellation, agent plans, policy changes, document intake, simulation, and readiness actions require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk subscription actions require separated approval for SIM swap, rollback, port-out, roaming spend, save offers, cancellation, agent mutations, policy parameters, documents, and go-live")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("telecom subscription assistant skills must cite owned facts, show reversible CRUD previews, enforce role/policy checks, and block direct writes before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("eligibility checks, future changes, usage normalization, notifications, billing boundary facts, previews, disputes, churn analysis, agent plans, release matrices, SLAs, parameters, isolation, test data, simulations, reconciliation, APIs, and scorecards must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("customer, SIM fulfillment, provisioning, billing, dispute, and reconciliation context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != SUBSCRIPTION_REQUIRED_EVENT_TOPIC:
        findings.append("telecom subscription lifecycle eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in SUBSCRIPTION_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary telecom subscription lifecycle datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("telecom subscription lifecycle controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_telecom_subscription_lifecycle_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in SUBSCRIPTION_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in SUBSCRIPTION_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "primary_proof": spec["primary_proof"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": SUBSCRIPTION_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": SUBSCRIPTION_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "configurable_rules_parameters": True,
        "agent_assisted": True,
        "side_effect_free": True,
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "slug": resolved.slug,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "evidence": evidence,
        "payload_digest": _digest(candidate)[:20],
        "side_effects": (),
    }


def improve1_telecom_subscription_lifecycle_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_telecom_subscription_lifecycle_control(capability) for capability in SUBSCRIPTION_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.telecom_subscription_lifecycle.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": SUBSCRIPTION_OWNED_TABLES,
        "allowed_database_backends": SUBSCRIPTION_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": SUBSCRIPTION_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": SUBSCRIPTION_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


TELECOM_SUBSCRIPTION_LIFECYCLE_CONTROL_FUNCTIONS = (
    "evaluate_telecom_subscription_lifecycle_control",
    "improve1_telecom_subscription_lifecycle_control_contract",
    "sample_payload_for",
)
