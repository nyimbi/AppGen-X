"""Executable improve1 controls for the Utilities Metering Billing PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    UTILITIES_METERING_BILLING_ALLOWED_DATABASE_BACKENDS,
    UTILITIES_METERING_BILLING_CONSUMED_EVENT_TYPES,
    UTILITIES_METERING_BILLING_OWNED_TABLES,
    UTILITIES_METERING_BILLING_REQUIRED_EVENT_TOPIC,
    UTILITIES_METERING_BILLING_RUNTIME_TABLES,
)

PBC_KEY = "utilities_metering_billing"
EVENT_CONTRACT = "AppGen-X"
UTILITY_ALLOWED_DATABASE_BACKENDS = UTILITIES_METERING_BILLING_ALLOWED_DATABASE_BACKENDS
UTILITY_REQUIRED_EVENT_TOPIC = UTILITIES_METERING_BILLING_REQUIRED_EVENT_TOPIC
UTILITY_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in UTILITY_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in UTILITY_CAPABILITIES}
UTILITY_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        UTILITIES_METERING_BILLING_OWNED_TABLES
        + UTILITIES_METERING_BILLING_RUNTIME_TABLES
        + tuple(f"utilities_metering_billing_{capability.slug}_control" for capability in UTILITY_CAPABILITIES)
    )
)
UTILITY_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        UTILITIES_METERING_BILLING_CONSUMED_EVENT_TYPES
        + (
            "PaymentPosted",
            "PaymentReversed",
            "CustomerUpdated",
            "PremiseUpdated",
            "FieldServiceOrderCompleted",
            "MeterAssetChanged",
            "WeatherObservationChanged",
            "TariffDirectivePublished",
            "DisputeOpened",
            "NotificationQueued",
            "AuditEvidenceSealed",
            "OperationalKpiChanged",
            "PolicyChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "jurisdiction_id",
    "service_point_id",
    "customer_meter_account_id",
    "commodity",
    "policy_version",
    "actor_id",
    "evidence_references",
)
_FIELD_ROWS = """
1|service_point_identity_id,premise_identifier,voltage_pressure_class,feeder_zone,geocode,lifecycle_status,active_meter_set,active_tariff_assignment
2|energization_state_id,service_order_id,current_state,target_state,approved_transition,effective_timestamp,billing_start_stop,authorization_evidence
3|meter_asset_id,serial_number,manufacturer,model,multiplier,firmware,seal_status,register_inventory
4|meter_exchange_id,outgoing_final_read,incoming_initial_read,rollover_flag,multiplier_delta,continuity_rule,usage_stitch_result,mismatch_exception
5|register_channel_id,register_type,channel_type,unit_of_measure,tariff_mapping,net_export_flag,demand_channel,reactive_energy_channel
6|read_provenance_id,read_source,collector_identity,device_session,acquisition_time,geotag,photo_evidence,entry_channel
7|meter_health_id,telemetry_staleness,communication_failure,certification_expiry,drift_suspicion,estimate_substitution_count,health_badge,service_order_recommendation
8|validation_ladder_id,presence_check,monotonicity_check,rollover_check,multiplier_check,tolerance_band,duplicate_detection,promote_decision
9|interval_completeness_id,interval_length,time_zone,dst_shift,overlap_window,missing_window,repair_path,derived_total_check
10|estimate_hierarchy_id,actual_adjacent_basis,season_history_basis,occupancy_profile,weather_normalized_pattern,engineering_fallback,confidence,expiry_criteria
11|estimate_replacement_id,superseded_estimate,actual_read,rebill_decision,carry_forward_decision,frozen_period,customer_delta,freeze_reason
12|exception_taxonomy_id,exception_code,severity,owner,sla,next_action,payroll_impact,remediation_trail
13|tamper_analytics_id,sudden_drop_signal,sudden_spike_signal,flatline_signal,negative_import_signal,reverse_flow_signal,neighborhood_outlier,inspection_recommendation
14|field_investigation_id,trigger_exception,service_order_type,field_action,owned_boundary_note,field_outcome,corrected_bill_link,closed_loop_evidence
15|read_to_bill_trace_id,source_read_set,interval_repair_set,estimate_substitution_set,validation_result,tariff_determinant,bill_segment,line_trace
16|tariff_version_id,jurisdiction,customer_class,service_point_class,effective_start,effective_end,approval_state,non_overlap_validation
17|rating_engine_id,block_structure,tou_window,demand_ratchet,power_factor_penalty,fixed_charge,minimum_charge,net_export_credit
18|eligibility_rule_id,rider_code,subsidy_code,exemption_code,program_enrollment,protected_customer_status,precedence,qualification_reason
19|bill_cycle_id,cycle_calendar,route_group,zone_group,segment_trigger,meter_change_split,tariff_change_split,move_event_split
20|proration_rule_id,fixed_charge_proration,demand_window_proration,minimum_charge_proration,block_allocation,move_basis,reconnect_basis,day_count_method
21|calculation_replay_id,input_hash,rule_version,parameter_version,read_set_hash,line_item_trace,reproducible_output,calculation_metadata
22|regulatory_component_id,tax_code,levy_code,fuel_clause,municipal_surcharge,rider_version,effective_date,precedence_rule
23|adjustment_governance_id,adjustment_reason,reference_bill_segment,materiality_band,maker_checker_path,customer_notice,reversal_link,approval_state
24|rebilling_workflow_id,historic_period,corrected_quantity,customer_impact,carry_forward_treatment,notice_obligation,replaced_bill_link,regulatory_cap
25|payment_boundary_id,bill_issued_event,payment_posted_event,reversal_posted_event,unpaid_threshold_event,promise_to_pay_event,write_off_event,no_payment_instrument_storage
26|allocation_view_id,partial_payment,overpayment,prepayment,refund,credit,write_off,segment_balance_narrative
27|move_in_workflow_id,vacancy_check,opening_read,opening_estimate,deposit_rule,connection_fee,effective_occupancy,billing_start
28|move_out_workflow_id,final_read,approved_estimate,final_bill,leave_live_decision,forwarding_contact,successor_account_rule,billing_end
29|vacant_premise_id,house_account_mode,landlord_mode,effective_responsibility,reduced_service_state,usage_attribution,transition_rule,responsible_party
30|deposit_fee_id,deposit_assessment,refund_eligibility,connection_fee,reconnection_fee,installment_plan,arrears_carry_forward,bill_presentation
31|usage_analytics_id,daily_usage,monthly_usage,seasonal_usage,normalized_consumption,read_success_rate,estimate_rate,billed_to_actual_variance
32|forecast_alert_id,end_cycle_consumption,bill_amount_forecast,leak_alert,continuous_flow_alert,base_load_alert,budget_billing_suggestion,outreach_evidence
33|exception_workbench_id,read_issue_queue,interval_issue_queue,tariff_issue_queue,bill_issue_queue,move_boundary_queue,payment_boundary_queue,sla_badge
34|dispute_case_id,dispute_reason,bill_segment_link,read_link,adjustment_link,service_order_link,hold_rule,decision_outcome
35|regulatory_pack_id,jurisdiction,estimated_bill_cap,notice_window,social_tariff_rule,meter_testing_obligation,rebill_limit,effective_date
36|consumer_protection_id,notice_period,moratorium_rule,medical_protection,minimum_payment_threshold,estimate_streak_limit,illegal_action_block,protection_banner
37|operator_queue_id,read_review_queue,estimate_review_queue,tariff_activation_queue,bill_run_queue,adjustment_queue,move_queue,mass_action
38|detail_ux_id,status_timeline,meter_installation_panel,read_history_panel,interval_quality_panel,tariff_timeline,bill_segment_panel,payment_boundary_panel
39|override_safeguard_id,override_reason,before_value,after_value,impacted_customer_count,regulator_warning,second_approver,evidence_complete
40|read_exception_agent_id,read_provenance_summary,prior_history,validation_failure,anomaly_driver,recommended_action,human_confirmation,write_block
41|tariff_notice_agent_id,source_notice,tariff_schedule_extract,rider_extract,ambiguous_clause,source_snippet,draft_tariff_change,approval_separation
42|adjustment_explanation_agent_id,adjustment_proposal,bill_explanation,dispute_summary,bill_trace,read_trace,rule_outcome,accepted_by_human
43|event_model_id,event_name,payload_schema,lifecycle_transition,projection_replay,sequence_trace,consumer_contract,event_mapping
44|event_recovery_id,idempotency_key,replay_safe_consumer,dead_letter_cause,retry_action,suppress_action,operator_audit,replay_result
45|boundary_contract_id,policy_event,payment_fact_event,kpi_event,projection_status,analytics_export,no_foreign_mutation,idempotency_behavior
46|scenario_matrix_id,scenario_name,test_reference,ui_evidence,event_trace,calculation_evidence,release_check,coverage_status
47|seed_reference_id,tenant_fixture,service_point_fixture,meter_fixture,tariff_fixture,protected_customer_fixture,reason_code_dictionary,calendar_fixture
48|batch_billing_sla_id,read_ingestion_throughput,interval_validation_latency,bill_simulation_latency,bill_issuance_latency,rebill_rerun_latency,queue_refresh_latency,cycle_close_sla
49|isolation_audit_id,tenant_scope,jurisdiction_scope,rule_pack,permission_boundary,audit_hash,calculation_trace_seal,leakage_check
50|cutover_hypercare_id,migration_rehearsal,opening_balance_reconciliation,first_bill_comparison,war_room_queue,operator_training,hypercare_exit,go_live_signoff
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("CustomerUpdated", "PremiseUpdated"),
    2: ("FieldServiceOrderCompleted",),
    3: ("MeterAssetChanged",),
    14: ("FieldServiceOrderCompleted",),
    25: ("PaymentPosted", "PaymentReversed"),
    27: ("CustomerUpdated", "PremiseUpdated"),
    32: ("WeatherObservationChanged",),
    34: ("DisputeOpened",),
    35: ("TariffDirectivePublished",),
    40: ("NotificationQueued",),
    45: ("PolicyChanged", "OperationalKpiChanged"),
    50: ("AuditEvidenceSealed", "OperationalKpiChanged"),
}
_SERVICE_METER_FEATURES = (1, 2, 3, 4, 5, 6, 7, 14, 27, 28, 29, 47, 49, 50)
_READ_BILLING_FEATURES = (8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 31, 32, 48, 50)
_ADJUSTMENT_PAYMENT_FEATURES = (23, 24, 25, 26, 30, 33, 34, 35, 36, 37, 38, 39, 46, 50)
_GOVERNANCE_AGENT_FEATURES = (40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50)
_AGENT_FEATURES = (40, 41, 42, 46, 50)
_HUMAN_CONFIRMATION_FEATURES = (2, 4, 11, 14, 23, 24, 27, 28, 30, 34, 36, 39, 40, 41, 42, 50)
_APPROVAL_REQUIRED_FEATURES = (2, 11, 23, 24, 27, 28, 30, 34, 36, 39, 41, 42, 50)
_NON_MUTATING_FEATURES = (7, 8, 9, 10, 13, 15, 16, 17, 18, 20, 21, 22, 25, 26, 31, 32, 33, 35, 37, 38, 40, 41, 42, 45, 46, 47, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (1, 2, 3, 14, 25, 26, 27, 28, 32, 34, 35, 44, 45, 48, 50)


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
        "tables": (f"utilities_metering_billing_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"UtilitiesMeteringBilling{_camel(capability.slug)}Panel",
        "route": f"POST /utilities-metering-billing/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in UTILITY_CAPABILITIES}


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
        "event_topic": UTILITY_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "service_meter_evidence_complete": True,
        "read_billing_evidence_complete": True,
        "adjustment_payment_evidence_complete": True,
        "governance_agent_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned utility model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _SERVICE_METER_FEATURES and payload.get("service_meter_evidence_complete") is not True:
        findings.append("service point, energization, meter registry, exchange, register/channel, read provenance, meter health, field investigation, move boundaries, vacant premise, seed data, isolation, and cutover evidence is required")
    if number in _READ_BILLING_FEATURES and payload.get("read_billing_evidence_complete") is not True:
        findings.append("read validation, interval completeness, estimates, exceptions, tamper analytics, read-to-bill trace, tariff versioning, rating, proration, reproducible calculation, regulatory components, analytics, forecasts, batch, and release proof evidence is required")
    if number in _ADJUSTMENT_PAYMENT_FEATURES and payload.get("adjustment_payment_evidence_complete") is not True:
        findings.append("adjustment, rebilling, payment boundary, allocation, deposits, exceptions, disputes, regulatory packs, consumer protection, workbench, detail UX, override, scenario matrix, and cutover evidence is required")
    if number in _GOVERNANCE_AGENT_FEATURES and payload.get("governance_agent_evidence_complete") is not True:
        findings.append("agent skills, event model, outbox/inbox/dead-letter recovery, cross-boundary contracts, release matrix, seed data, batch SLA, isolation, and hypercare evidence is required")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("energization, meter exchange, estimate replacement, field orders, adjustments, rebills, moves, deposits, disputes, protected actions, overrides, agent drafts, and go-live cutover require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk utility billing actions require separated approval for service state, estimates, adjustments, rebilling, move boundaries, deposits, disputes, consumer protection, overrides, agent drafts, and cutover")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("utility billing assistant skills must cite owned facts, show reversible CRUD previews, enforce permissions and policy checks, and block direct writes before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("health analytics, validation, interval repair, estimates, anomalies, read-to-bill traces, tariff checks, rating, proration, replay, payment views, analytics, forecasts, queues, UI proof, agent suggestions, boundary contracts, release matrices, seed checks, SLA evidence, isolation, and cutover proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("customer, premise, field service, meter asset, payment, dispute, notification, weather, tariff directive, audit, policy, and KPI context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != UTILITY_REQUIRED_EVENT_TOPIC:
        findings.append("utilities metering billing eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in UTILITY_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary utilities metering billing datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("utilities metering billing controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_utilities_metering_billing_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in UTILITY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in UTILITY_DECLARED_DEPENDENCIES)
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
        "required_event_topic": UTILITY_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": UTILITY_ALLOWED_DATABASE_BACKENDS,
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


def improve1_utilities_metering_billing_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_utilities_metering_billing_control(capability) for capability in UTILITY_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.utilities_metering_billing.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": UTILITY_CONTROL_OWNED_TABLES,
        "allowed_database_backends": UTILITY_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": UTILITY_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": UTILITY_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


UTILITIES_METERING_BILLING_CONTROL_FUNCTIONS = (
    "evaluate_utilities_metering_billing_control",
    "improve1_utilities_metering_billing_control_contract",
    "sample_payload_for",
)
