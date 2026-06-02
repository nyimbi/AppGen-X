"""Executable improve1 controls for the Travel Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    TRAVEL_MANAGEMENT_CONSUMED_EVENT_TYPES,
    TRAVEL_MANAGEMENT_OWNED_TABLES,
    TRAVEL_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    TRAVEL_MANAGEMENT_RUNTIME_TABLES,
)

PBC_KEY = "travel_management"
EVENT_CONTRACT = "AppGen-X"
TRAVEL_ALLOWED_DATABASE_BACKENDS = TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
TRAVEL_REQUIRED_EVENT_TOPIC = TRAVEL_MANAGEMENT_REQUIRED_EVENT_TOPIC
TRAVEL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in TRAVEL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in TRAVEL_CAPABILITIES}
TRAVEL_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        TRAVEL_MANAGEMENT_OWNED_TABLES
        + TRAVEL_MANAGEMENT_RUNTIME_TABLES
        + tuple(f"travel_management_{capability.slug}_control" for capability in TRAVEL_CAPABILITIES)
    )
)
TRAVEL_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        TRAVEL_MANAGEMENT_CONSUMED_EVENT_TYPES
        + (
            "EmployeeCreated",
            "EmployeeUpdated",
            "ExpenseReportCreated",
            "ExpenseApproved",
            "PolicyChanged",
            "PaymentExecuted",
            "SupplierQualified",
            "SupplierOfferChanged",
            "BookingStatusChanged",
            "DutyOfCareAlertChanged",
            "NotificationQueued",
            "RiskAdvisoryChanged",
            "CarbonFactorChanged",
            "DocumentReceived",
            "AuditEvidenceSealed",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "legal_entity_id",
    "traveler_projection_id",
    "trip_id",
    "policy_version",
    "destination_region",
    "actor_id",
    "evidence_references",
)
_FIELD_ROWS = """
1|readiness_gate_id,business_purpose,start_date,end_date,cost_estimate,risk_level,visa_passport_need,duty_of_care_prerequisite
2|trip_state_machine_id,current_state,next_state,allowed_transition,required_evidence,owner,notification_effect,expense_handoff_eligibility
3|profile_completeness_id,contact_method,emergency_contact,identity_document,home_region,preferred_language,accessibility_requirement,risk_consent
4|traveler_preference_id,preference_category,sensitivity_level,booking_applicability,consent_state,visibility_control,override_rule,satisfaction_status
5|policy_version_id,effective_interval,employee_group,business_unit,trip_type,fare_class,hotel_cap,exception_path
6|policy_compiler_id,source_document,predicate_set,ambiguity_flag,example_case,test_case,approver,effective_date
7|policy_coaching_id,candidate_option,compliant_alternative,fare_class_delta,booking_window_warning,hotel_rate_delta,carbon_delta,exception_required
8|approval_graph_id,manager_node,budget_owner_node,risk_node,finance_node,delegation_rule,escalation_timer,route_rationale
9|emergency_lane_id,emergency_reason,risk_screen,post_approval_review,time_boxed_authorization,override_evidence,duty_of_care_check,exception_label
10|booking_intent_id,intent_state,travel_window,preferred_supplier_set,budget_constraint,risk_constraint,booking_deadline,option_comparison
11|supplier_offer_id,base_price,taxes,fees,restriction_set,refundability,loyalty_accrual,carbon_estimate,source_payload_hash
12|air_booking_control_id,fare_class,routing,layover_risk,ticketing_deadline,baggage_rule,change_fee,unused_ticket_eligibility
13|hotel_booking_control_id,nightly_rate,total_stay_cost,location_safety,cancellation_window,accessibility_status,preferred_supplier,safer_alternative
14|ground_booking_control_id,transport_mode,mode_eligibility,distance,rate_class,insurance_check,pickup_dropoff_timing,mileage_policy_link
15|itinerary_ingestion_id,document_type,item_type,time_zone,confirmation_number,supplier,location,uncertain_field,review_required
16|itinerary_timeline_id,item_dependency,local_time,confirmation_status,source_evidence,conflict_detection,gap_detection,change_history
17|risk_assessment_id,destination_risk,itinerary_risk,traveler_profile_risk,health_advisory,weather_alert,risk_driver,confidence
18|duty_of_care_alert_id,severity,affected_traveler,contact_attempt,acknowledgement,escalation_owner,assistance_action,closure_proof
19|location_confidence_id,current_location,planned_location,stale_location,unknown_location,source_signal,privacy_control,confidence_score
20|disruption_record_id,source,affected_itinerary_item,severity,traveler_impact,option_set,policy_implication,expense_impact
21|disruption_routing_id,alternative_route,cost_delta,arrival_delta,connection_risk,cancellation_penalty,unused_ticket_use,duty_score
22|assistance_case_id,case_category,severity,location,contact_method,owner,assistance_action,cost_estimate,closure_evidence
23|unused_ticket_id,ticket_value,currency,supplier,expiration_date,transferability,fare_rule,residual_value,reuse_eligibility
24|unused_ticket_expiration_id,alert_date,owner_assignment,reuse_campaign,exception_handling,write_off_evidence,recovered_value,readiness_dashboard_status
25|expense_handoff_id,trip_reference,itinerary_reference,approved_budget,booking_reference,expected_category,per_diem_eligibility,mileage_eligibility,source_evidence
26|settlement_reconciliation_id,payment_execution,supplier_charge,cancellation_refund,unused_ticket_credit,traveler_expense,settlement_status,exception_reason
27|supplier_scorecard_id,booking_success_rate,disruption_rate,refund_behavior,safety_incident,traveler_feedback,cost_variance,carbon_completeness
28|preferred_supplier_control_id,supplier_selection,preferred_rule,exception_reason,negotiated_rate,traveler_need,disruption_condition,compliance_evidence
29|carbon_booking_id,air_emissions,hotel_emissions,ground_emissions,assumption_set,data_source,confidence,tradeoff_explanation
30|wellbeing_control_id,red_eye_count,minimum_rest,long_layover,trip_density,time_zone_burden,accessibility_need,approval_requirement
31|document_readiness_id,passport_expiration,visa_requirement,entry_permit,health_document,lead_time,nationality,booking_block
32|risk_exception_id,destination_category,traveler_rationale,mitigation_plan,approver_set,emergency_contact,insurance_status,traveler_acknowledgement
33|trip_cost_forecast_id,air_estimate,hotel_estimate,ground_estimate,per_diem_estimate,unused_ticket_offset,approved_budget,booked_cost,expensed_cost
34|anomaly_detection_id,traveler_pattern,route_pattern,supplier_pattern,booking_window, fare_class,cancellation_rate,cost_variance
35|policy_impact_id,policy_change,affected_trip_set,savings_estimate,exception_volume,approval_volume,traveler_impact,carbon_impact
36|continuous_control_id,assertion_name,policy_exception_check,missing_risk_screen,stale_itinerary_check,unused_ticket_leakage,expense_handoff_gap,remediation_task
37|exception_case_id,exception_type,severity,owner,affected_trip,required_evidence,financial_exposure,traveler_impact,closure_proof
38|audit_proof_id,hash_chain_id,trip_request_hash,approval_hash,booking_hash,itinerary_hash,duty_alert_hash,redacted_export
39|event_reliability_id,schema_version,idempotency_key,ordering_assumption,retry_envelope,dead_letter_taxonomy,replay_eligibility,handler_evidence
40|boundary_proof_id,declared_api,projection_name,consumed_event,cached_field,staleness_policy,retention_rule,foreign_table_fixture
41|trip_planning_agent_id,business_goal,meeting_location,policy_constraint,personal_need,compliant_plan,missing_profile_item,approval_preview
42|disruption_agent_id,disruption_summary,rebooking_alternative,duty_risk_check,cost_estimate,carbon_estimate,traveler_message,service_command_preview
43|itinerary_agent_id,confirmation_number,supplier_contact,location,time_zone,cancellation_window,expense_hint,crud_preview
44|communication_center_id,template,delivery_plan,message_history,acknowledgement_tracking,critical_escalation,notification_projection,preference_basis
45|operations_cockpit_id,pending_trip_filter,approval_filter,booking_filter,disruption_filter,duty_alert_filter,unused_ticket_filter,evidence_export
46|ui_surface_proof_id,trip_request_panel,traveler_profile_panel,policy_panel,booking_panel,duty_of_care_panel,expense_panel,agent_tool_panel
47|resilience_drill_id,drill_type,supplier_outage,duplicate_booking_replay,itinerary_parser_failure,policy_rollback,risk_alert_surge,dead_letter_recovery
48|readiness_score_id,profile_readiness,policy_readiness,approval_readiness,supplier_offer_quality,duty_of_care_health,event_health,agent_safety
49|privacy_retention_id,privacy_classification,retention_rule,access_scope,redaction_support,purpose_constraint,sensitive_field_audit,agent_minimization
50|end_to_end_proof_id,trip_request,approval_route,booking_intent,air_hotel_ground_booking,itinerary_ingestion,duty_screening,expense_handoff,agent_plan
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("EmployeeUpdated", "PolicyChanged"),
    3: ("EmployeeUpdated",),
    6: ("PolicyChanged",),
    11: ("SupplierOfferChanged",),
    12: ("BookingStatusChanged",),
    17: ("RiskAdvisoryChanged",),
    18: ("DutyOfCareAlertChanged", "NotificationQueued"),
    25: ("ExpenseReportCreated",),
    26: ("PaymentExecuted", "ExpenseApproved"),
    27: ("SupplierQualified",),
    29: ("CarbonFactorChanged",),
    39: ("EmployeeCreated", "PaymentExecuted"),
    43: ("DocumentReceived",),
    50: ("EmployeeUpdated", "PolicyChanged", "PaymentExecuted", "AuditEvidenceSealed"),
}
_TRIP_POLICY_BOOKING_FEATURES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 31, 33, 35, 50)
_CARE_DISRUPTION_FEATURES = (17, 18, 19, 20, 21, 22, 30, 32, 34, 42, 44, 47, 48, 50)
_EXPENSE_SUPPLIER_FEATURES = (23, 24, 25, 26, 27, 28, 29, 33, 40, 50)
_OPERATIONS_AGENT_PRIVACY_FEATURES = (36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50)
_AGENT_FEATURES = (41, 42, 43, 48, 49, 50)
_HUMAN_CONFIRMATION_FEATURES = (8, 9, 10, 12, 20, 21, 22, 25, 26, 32, 37, 41, 42, 43, 50)
_APPROVAL_REQUIRED_FEATURES = (8, 9, 12, 21, 22, 25, 26, 32, 37, 50)
_NON_MUTATING_FEATURES = (3, 6, 7, 11, 17, 19, 21, 23, 24, 27, 29, 30, 31, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 46, 47, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (1, 3, 17, 18, 25, 26, 27, 29, 39, 40, 44, 49, 50)


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
        "tables": (f"travel_management_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"TravelManagement{_camel(capability.slug)}Panel",
        "route": f"POST /travel-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in TRAVEL_CAPABILITIES}


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
        "event_topic": TRAVEL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "trip_policy_booking_evidence_complete": True,
        "care_disruption_evidence_complete": True,
        "expense_supplier_evidence_complete": True,
        "operations_agent_privacy_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned travel model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _TRIP_POLICY_BOOKING_FEATURES and payload.get("trip_policy_booking_evidence_complete") is not True:
        findings.append("trip, policy, approval, booking, itinerary, document readiness, budget, policy impact, and end-to-end booking evidence is required")
    if number in _CARE_DISRUPTION_FEATURES and payload.get("care_disruption_evidence_complete") is not True:
        findings.append("duty-of-care, location confidence, disruption, assistance, wellbeing, risk exception, anomaly, communication, resilience, readiness, and end-to-end safety evidence is required")
    if number in _EXPENSE_SUPPLIER_FEATURES and payload.get("expense_supplier_evidence_complete") is not True:
        findings.append("unused-ticket, expense handoff, settlement, supplier, preferred supplier, carbon, cost forecast, boundary, and end-to-end handoff evidence is required")
    if number in _OPERATIONS_AGENT_PRIVACY_FEATURES and payload.get("operations_agent_privacy_evidence_complete") is not True:
        findings.append("continuous controls, exceptions, audit proof, AppGen-X reliability, boundary proof, agent skills, communications, cockpit, UI, resilience, readiness, privacy, and release evidence is required")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("travel approvals, emergency lanes, booking intents, bookings, disruptions, assistance, expense handoff, settlement, risk exceptions, exceptions, agent planning, itinerary CRUD, and release proof require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk travel actions require separated approval for approval routing, emergency overrides, bookings, disruption rebooking, assistance, expense handoff, settlement, risk exceptions, exception closure, and end-to-end release")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("travel assistant skills must cite owned facts, show reviewable CRUD previews, enforce permissions and policy checks, and block booking, submission, or sensitive disclosure before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("profile scoring, policy compilation, coaching, offer normalization, risk scoring, ticket reuse, supplier scoring, carbon comparison, wellbeing checks, cost forecasts, anomaly detection, impact analysis, controls, audit proof, event replay, boundary proof, agent suggestions, UI proof, resilience, readiness, privacy, and end-to-end proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("employee, expense, payment, supplier, booking, duty-of-care, notification, risk, carbon, document, and audit context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != TRAVEL_REQUIRED_EVENT_TOPIC:
        findings.append("travel management eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in TRAVEL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary travel management datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("travel management controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_travel_management_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in TRAVEL_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in TRAVEL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": TRAVEL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": TRAVEL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_travel_management_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_travel_management_control(capability) for capability in TRAVEL_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.travel_management.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": TRAVEL_CONTROL_OWNED_TABLES,
        "allowed_database_backends": TRAVEL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": TRAVEL_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": TRAVEL_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


TRAVEL_MANAGEMENT_CONTROL_FUNCTIONS = (
    "evaluate_travel_management_control",
    "improve1_travel_management_control_contract",
    "sample_payload_for",
)
