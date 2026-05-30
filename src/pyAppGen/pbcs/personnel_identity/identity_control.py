"""Executable improve1 controls for the Personnel Identity PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS, PERSONNEL_IDENTITY_OWNED_TABLES, PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC

PBC_KEY = "personnel_identity"
EVENT_CONTRACT = "AppGen-X"
IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS = PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS
IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC = PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC
IDENTITY_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(PERSONNEL_IDENTITY_OWNED_TABLES + tuple(f"personnel_identity_{c.slug}_control" for c in IMPROVE1_CAPABILITIES)))
IDENTITY_CONTROL_DECLARED_DEPENDENCIES = (
    "EmployeeProvisioned", "AccessPolicyChanged", "OrgUnitChanged", "RoleReviewRequested", "AuditEventSealed",
    "IdentityProviderChanged", "DirectoryProjectionChanged", "ManagerCapacityChanged", "ResidencyPolicyChanged",
    "CarbonIntensityWindowChanged", "ModelGovernanceChanged", "CryptoPolicyChanged", "PrivacyConsentChanged",
)
IDENTITY_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {c.feature_number: c for c in IDENTITY_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {c.slug: c for c in IDENTITY_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "employee_id", "department_id", "position_id", "job_id", "role_id", "manager_id", "country", "privacy_region", "actor_id", "policy_version", "evidence_references")
_FIELD_ROWS = """
1|department_code,department_status,effective_date,owner,closure_reason,approval_trace
2|parent_department,child_department,valid_from,valid_to,cycle_check,depth_limit
3|position_code,headcount_budget,incumbent_employee,position_status,vacancy_reason,approval_path
4|job_code,job_family,grade,competency_profile,legal_classification,version_reason
5|identity_spine_id,canonical_person_key,source_system_ids,duplicate_score,merge_decision,survivorship_rule
6|readiness_gate_id,identity_verified,position_ready,manager_ready,work_location_ready,privacy_notice_ready
7|contact_record_id,contact_type,consent_basis,visibility_scope,redaction_rule,access_purpose
8|document_id,document_type,retention_class,verification_status,expiry_date,chain_of_custody
9|lifecycle_event_id,status_from,status_to,reason,effective_date,illegal_transition_block
10|status_history_id,valid_time,transaction_time,correction_reason,prior_state,reconstruction_proof
11|manager_relationship_id,relationship_type,span_of_control,delegation_state,conflict_check,approval_trace
12|org_assignment_id,primary_assignment,cost_center,work_location,department,assignment_completeness
13|location_rule_id,work_location,residency_country,tax_region,remote_work_flag,exception_reason
14|cost_center_assignment_id,cost_center,allocation_percent,effective_date,source_projection,lineage_hash
15|role_catalog_id,risk_level,privilege_scope,conflict_tags,approval_required,review_cadence
16|role_assignment_id,assignment_state,effective_window,request_source,revocation_reason,provisioning_route
17|sod_check_id,conflicting_role,mitigation_control,approval_exception,risk_score,block_reason
18|role_review_id,reviewer,review_cycle,attestation_status,remediation_action,closure_proof
19|attribute_taxonomy_id,attribute_name,sensitivity_class,source_authority,quality_rule,usage_policy
20|assurance_score_id,identity_strength,document_score,source_reliability,staleness_penalty,score_explanation
21|verification_workflow_id,verification_method,provider,step_status,challenge_result,manual_review
22|eligibility_proof_id,eligibility_rule,proof_claim,zk_or_redacted_evidence,verifier,audit_hash
23|policy_projection_id,policy_version,projection_source,received_event,handler_idempotency,staleness_state
24|access_exception_id,exception_type,scope,expiry,compensating_control,reviewer_approval
25|provisioning_route_id,target_system,route_policy,precheck_result,rollback_route,dead_letter_plan
26|replay_id,source_event,sequence_number,idempotency_key,replay_window,projection_result
27|directory_projection_id,quality_score,missing_attribute,stale_record_count,reconciliation_action,projection_hash
28|org_chart_projection_id,root_department,manager_tree,cycle_detection,as_of_time,reconstruction_hash
29|consent_id,data_category,consent_status,lawful_basis,withdrawal_path,processing_limit
30|retention_policy_id,data_class,minimization_rule,delete_after,legal_hold,disposal_proof
31|residency_rule_id,data_region,employee_region,transfer_mechanism,violation_reason,remediation_path
32|policy_screening_id,policy_scope,attributes_evaluated,decision,explanation,override_path
33|anomaly_id,attribute_entropy,role_change_spike,manager_drift,source_mismatch,reason_codes
34|risk_forecast_id,attrition_signal,access_risk_distribution,org_change_forecast,mitigation_options,confidence
35|capacity_allocation_id,manager_capacity,team_load,skill_mix,assignment_recommendation,approval_required
36|optimization_id,role_bundle,cost_function,risk_reduction,access_coverage,constraint_explanation
37|model_registry_id,feature_lineage,training_window,drift_monitoring,fairness_check,rollback_plan
38|audit_chain_id,identity_hash,role_hash,policy_hash,provisioning_hash,temporal_reconstruction
39|event_cockpit_id,inbox_status,outbox_status,dead_letter_age,replay_eligibility,projection_freshness
40|boundary_proof_id,owned_table_check,employee_master_block,access_table_block,org_table_block,foreign_write_block
41|workbench_coverage_id,directory_surface,role_surface,privacy_surface,provisioning_surface,agent_panel
42|document_intake_id,extracted_identity_fact,owned_table_preview,permission_check,confidence,expected_event
43|identity_role_plan_id,command,owned_tables,affected_employee,risk_impact,human_approval
44|simulation_id,org_change,role_policy_change,manager_capacity_change,risk_delta,historical_comparison
45|carbon_processing_id,processing_window,statutory_deadline,employee_experience_constraint,selected_window,tradeoff
46|resilience_drill_id,scenario,target_system,retry_path,dead_letter_recovery,recovery_time
47|crypto_epoch_id,algorithm,key_id,signature_policy,rotation_plan,crypto_agility_proof
48|control_test_id,sod_check,privacy_check,boundary_check,dead_letter_check,agent_bypass_check
49|readiness_score_id,setup_score,identity_score,role_score,privacy_score,event_score
50|workforce_proof_id,department_proof,employee_proof,role_proof,provisioning_proof,audit_proof
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    2: ("OrgUnitChanged",), 6: ("EmployeeProvisioned",), 14: ("OrgUnitChanged",), 18: ("RoleReviewRequested",),
    23: ("AccessPolicyChanged",), 25: ("IdentityProviderChanged",), 26: ("EmployeeProvisioned",),
    27: ("DirectoryProjectionChanged",), 28: ("OrgUnitChanged", "DirectoryProjectionChanged"), 29: ("PrivacyConsentChanged",),
    31: ("ResidencyPolicyChanged",), 35: ("ManagerCapacityChanged",), 37: ("ModelGovernanceChanged",),
    38: ("AuditEventSealed",), 39: ("AuditEventSealed",), 45: ("CarbonIntensityWindowChanged",), 47: ("CryptoPolicyChanged",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 3, 5, 6, 11, 16, 17, 18, 21, 22, 24, 29, 31, 32, 35, 36, 42, 43, 47, 50)
_PROJECTION_ONLY_FEATURES = (2, 6, 14, 18, 23, 25, 26, 27, 28, 29, 31, 35, 37, 38, 39, 45, 47)
_AGENT_PREVIEW_FEATURES = (42, 43, 50)
_NON_MUTATING_FEATURES = (20, 22, 27, 28, 33, 34, 35, 36, 37, 38, 39, 40, 44, 45, 46, 48, 49, 50)
_IDENTITY_RISK_FEATURES = (5, 6, 7, 8, 9, 13, 15, 16, 17, 18, 20, 21, 22, 24, 29, 30, 31, 32, 33, 34, 38, 39, 40, 47, 48, 50)


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"personnel_identity_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number], "ui": f"PersonnelIdentity{_camel(capability.slug)}Panel", "route": f"POST /personnel-identity/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in IDENTITY_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "dependency_access_mode": "api_event_projection", "human_confirmation": True, "agent_preview_only": True, "non_mutating_simulation": True, "identity_risk_evidence_complete": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires personnel-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _IDENTITY_RISK_FEATURES and payload.get("identity_risk_evidence_complete") is not True:
        findings.append("identity, lifecycle, contact privacy, document, role, assurance, eligibility, access, policy, audit, crypto, control, and workforce proof decisions require complete risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("department, position, employee, manager, role, verification, privacy, residency, policy, agent, optimization, crypto, and workforce proof decisions require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("personnel agent skills must return cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("assurance scores, proofs, projections, anomalies, forecasts, optimization, audit, cockpit, boundary, simulations, carbon, drills, testing, readiness, and workforce proofs must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("org, provisioning, access, directory, privacy, residency, manager capacity, model, audit, carbon, and crypto facts must use APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("personnel identity eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary personnel identity datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("personnel identity controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_identity_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in IDENTITY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in IDENTITY_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "primary_proof": spec["primary_proof"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_identity_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_identity_control(capability) for capability in IDENTITY_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.personnel-identity-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": IDENTITY_CONTROL_OWNED_TABLES, "declared_dependencies": IDENTITY_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


IDENTITY_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_identity_control(slug, payload)) for capability in IDENTITY_CONTROL_CAPABILITIES}
