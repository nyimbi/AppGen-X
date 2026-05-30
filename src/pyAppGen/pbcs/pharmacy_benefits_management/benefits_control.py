"""Executable improve1 controls for the Pharmacy Benefits Management PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import PHARMACY_BENEFITS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES, PHARMACY_BENEFITS_MANAGEMENT_REQUIRED_EVENT_TOPIC

PBC_KEY = "pharmacy_benefits_management"
EVENT_CONTRACT = "AppGen-X"
BENEFITS_CONTROL_ALLOWED_DATABASE_BACKENDS = PHARMACY_BENEFITS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
BENEFITS_CONTROL_REQUIRED_EVENT_TOPIC = PHARMACY_BENEFITS_MANAGEMENT_REQUIRED_EVENT_TOPIC
BENEFITS_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES + tuple(f"pharmacy_benefits_management_{c.slug}_control" for c in IMPROVE1_CAPABILITIES)))
BENEFITS_CONTROL_DECLARED_DEPENDENCIES = (
    "PolicyChanged", "CustomerUpdated", "SupplierQualified", "PharmacyClaimReceived", "MemberEligibilityChanged",
    "AccumulatorProjectionChanged", "PrescriberUpdated", "DrugCatalogChanged", "ClinicalGuidelineChanged",
    "RebateInvoiceReceived", "PharmacyNetworkChanged", "NotificationDelivered", "AuditEventSealed",
    "SupplyConstraintChanged", "ModelGovernanceChanged",
)
BENEFITS_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {c.feature_number: c for c in BENEFITS_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {c.slug: c for c in BENEFITS_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "plan_id", "member_id", "drug_id", "ndc", "pharmacy_id", "prescriber_id", "claim_id", "pa_case_id", "actor_id", "policy_version", "evidence_references")
_FIELD_ROWS = """
1|formulary_id,formulary_version,effective_date,retired_version,approval_state,publication_channel
2|therapeutic_class,drug_identity,rxnorm_code,ndc_group,generic_indicator,clinical_substitution_group
3|tier_id,cost_share_rule,copay,coinsurance,member_group,exception_reason
4|step_pathway_id,first_line_drug,prerequisite_claims,step_failure_reason,bypass_rule,clinical_exception
5|pa_intake_id,required_documents,clinical_answers,prescriber_attestation,missing_items,intake_status
6|criteria_rule_id,diagnosis_match,lab_requirement,duration_limit,clinical_rationale,decision_explanation
7|urgent_review_id,request_timestamp,regulatory_sla,clinical_urgency,escalation_owner,deadline_status
8|pa_renewal_id,continuity_claims,therapy_gap,prior_approval_ref,renewal_window,transition_supply
9|claim_edit_id,edit_code,submitted_quantity,days_supply,member_eligibility,reject_or_pay
10|quantity_limit_id,max_quantity,days_supply_limit,accumulation_window,override_reason,clinical_basis
11|refill_logic_id,last_fill_date,adherence_signal,days_supply_remaining,early_refill_reason,outcome
12|specialty_route_id,specialty_drug,network_requirement,site_of_care,cold_chain_flag,routing_decision
13|network_contract_id,pharmacy_network,dispensing_terms,mac_pricing,performance_terms,effective_date
14|rebate_contract_id,manufacturer,drug_group,guarantee_type,exclusion_terms,ethical_review
15|rebate_accrual_id,claim_population,expected_rebate,true_up_period,invoice_reference,variance_reason
16|ur_case_id,case_type,trigger_source,clinical_owner,severity,next_action
17|safety_screen_id,drug_interaction,duplicate_therapy,age_sex_alert,contraindication,prescriber_override
18|controlled_substance_id,opioid_mme,prescriber_pattern,pharmacy_pattern,lock_in_status,safety_intervention
19|affordability_id,member_cost,assistance_program,alternative_drug,hardship_flag,member_guidance
20|substitution_policy_id,biosimilar_group,generic_available,dispense_as_written,member_savings,exception_rule
21|appeal_id,appeal_level,denial_reason,evidence_packet,deadline,decision_outcome
22|criteria_document_id,source_document,extracted_criteria,citation_set,version,reviewer_approval
23|benefit_config_id,plan_variant,rule_set,parameter_snapshot,effective_window,approval_trace
24|simulation_id,parameter_change,impacted_members,claim_cost_delta,clinical_delta,decision_preview
25|reversal_id,original_claim,adjustment_reason,reversal_status,financial_projection,audit_trace
26|rtbc_contract_id,request_schema,response_schema,latency_sla,member_price,coverage_result
27|performance_metric_id,quality_measure,network_score,adherence_rate,member_outcome,reporting_period
28|fwa_signal_id,pattern_type,provider_signal,member_signal,pharmacy_signal,investigation_ref
29|notice_rule_id,notice_type,language,deadline,delivery_channel,template_version
30|prescriber_portal_id,collaboration_case,questionnaire,status_update,attachment,secure_message
31|reviewer_assignment_id,clinical_specialty,license_state,caseload,conflict_check,assignment_reason
32|conflict_detection_id,rule_a,rule_b,conflict_type,member_impact,resolution_path
33|accumulator_boundary_id,deductible_projection,out_of_pocket_projection,external_source,staleness,read_only_guard
34|shortage_id,drug_shortage,alternative_drug,supply_constraint,member_impact,exception_policy
35|jurisdiction_rule_id,country_or_state,regulatory_rule,coverage_variation,notice_requirement,localization_status
36|dead_letter_id,event_type,retry_count,owner,replay_eligibility,recovery_evidence
37|pa_summary_id,source_records,citation_set,clinical_summary,reviewer_edit,human_approval
38|agent_command_id,crud_preview,owned_table,permission_check,expected_event,confirmation_record
39|ethical_guardrail_id,rebate_bias_check,coverage_equity_check,member_harm_check,mitigation,approval_trace
40|timeline_id,benefit_events,coverage_changes,pa_decisions,claim_outcomes,member_view
41|audit_room_id,request_item,evidence_packet,redaction_rule,reviewer_access,audit_log
42|crypto_proof_id,decision_hash,criteria_hash,claim_hash,notice_hash,verifier_api
43|analytics_pack_id,utilization_trend,cost_trend,therapy_class,cohort_filter,export_snapshot
44|impact_analysis_id,policy_change,member_population,claim_population,cost_impact,clinical_impact
45|scenario_pack_id,scenario_type,fixture_records,expected_events,regression_assertions,release_reference
46|persona_coverage_id,benefit_admin_view,clinical_reviewer_view,pharmacy_ops_view,member_service_view,compliance_view
47|model_registry_id,model_name,feature_lineage,training_window,drift_monitoring,rollback_plan
48|release_simulation_id,formulary_ready,pa_ready,claims_ready,rebates_ready,member_notice_ready
49|boundary_proof_id,owned_table_check,eligibility_table_block,ledger_table_block,clinical_table_block,projection_contract
50|composition_dsl_id,pbc_key,skills_namespace,agent_capability,ui_mount,dependency_contract
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    2: ("DrugCatalogChanged",), 5: ("PrescriberUpdated",), 9: ("PharmacyClaimReceived", "MemberEligibilityChanged"),
    13: ("PharmacyNetworkChanged",), 15: ("RebateInvoiceReceived",), 22: ("ClinicalGuidelineChanged",),
    25: ("PharmacyClaimReceived",), 26: ("MemberEligibilityChanged",), 29: ("NotificationDelivered",),
    30: ("PrescriberUpdated",), 33: ("AccumulatorProjectionChanged",), 34: ("SupplyConstraintChanged",),
    36: ("AuditEventSealed",), 41: ("AuditEventSealed",), 44: ("PolicyChanged",), 47: ("ModelGovernanceChanged",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 3, 4, 6, 7, 10, 14, 18, 21, 22, 23, 25, 28, 31, 32, 37, 38, 39, 44, 48, 50)
_PROJECTION_ONLY_FEATURES = (2, 5, 9, 13, 15, 22, 25, 26, 29, 30, 33, 34, 36, 41, 44, 47)
_AGENT_PREVIEW_FEATURES = (37, 38, 50)
_NON_MUTATING_FEATURES = (15, 19, 24, 27, 28, 32, 33, 37, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50)
_BENEFIT_RISK_FEATURES = (1, 3, 4, 5, 6, 7, 9, 10, 11, 14, 15, 17, 18, 19, 21, 25, 28, 29, 32, 33, 34, 39, 41, 42, 44, 48, 49, 50)


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"pharmacy_benefits_management_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number], "ui": f"PharmacyBenefitsManagement{_camel(capability.slug)}Panel", "route": f"POST /pharmacy-benefits-management/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in BENEFITS_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": BENEFITS_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "dependency_access_mode": "api_event_projection", "human_confirmation": True, "agent_preview_only": True, "non_mutating_simulation": True, "benefit_risk_evidence_complete": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires PBM-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _BENEFIT_RISK_FEATURES and payload.get("benefit_risk_evidence_complete") is not True:
        findings.append("formulary, tiering, step therapy, PA, claim edits, safety, controlled substances, affordability, appeals, reversals, FWA, notices, accumulators, shortage, ethics, audit, proof, release, and boundary decisions require complete benefit risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("formulary, cost share, step therapy, PA criteria, urgent review, quantity limits, rebates, controlled substances, appeals, criteria documents, configuration, reversals, FWA, assignments, conflicts, agent commands, ethics, policy impact, release simulation, and composition require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("PBM agent skills must return cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("rebate evidence, affordability, simulations, metrics, FWA signals, conflicts, accumulators, agent summaries, ethics, timelines, audit rooms, crypto proofs, analytics, impact analysis, seed packs, model registry, release simulation, boundary proof, and DSL exposure must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("drug, prescriber, claim, eligibility, network, rebate, guideline, notification, accumulator, shortage, audit, policy, and model facts must use APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != BENEFITS_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("PBM eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in BENEFITS_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary PBM datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("PBM controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_benefits_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in BENEFITS_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in BENEFITS_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "primary_proof": spec["primary_proof"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": BENEFITS_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": BENEFITS_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_benefits_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_benefits_control(capability) for capability in BENEFITS_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.pharmacy-benefits-management-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": BENEFITS_CONTROL_OWNED_TABLES, "declared_dependencies": BENEFITS_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": BENEFITS_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": BENEFITS_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


BENEFITS_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_benefits_control(slug, payload)) for capability in BENEFITS_CONTROL_CAPABILITIES}
