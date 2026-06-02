"""Executable improve1 controls for the Quality Assurance PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS,
    QUALITY_ASSURANCE_OWNED_TABLES,
    QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
    QUALITY_ASSURANCE_RUNTIME_TABLES,
)

PBC_KEY = "quality_assurance"
EVENT_CONTRACT = "AppGen-X"
QA_ALLOWED_DATABASE_BACKENDS = QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
QA_REQUIRED_EVENT_TOPIC = QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
QA_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in QA_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in QA_CAPABILITIES}
QA_OWNED_TABLES = tuple(
    dict.fromkeys(
        QUALITY_ASSURANCE_OWNED_TABLES
        + QUALITY_ASSURANCE_RUNTIME_TABLES
        + tuple(f"quality_assurance_{capability.slug}_control" for capability in QA_CAPABILITIES)
    )
)
QA_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "ProductionCompleted",
    "GoodsReceiptPosted",
    "InventoryLotMoved",
    "SupplierScoreChanged",
    "CalibrationAssetChanged",
    "CustomerQualityCaseOpened",
    "CertificateIdentityIssued",
)
_BASE_FIELDS = (
    "tenant_id",
    "lot_id",
    "plan_id",
    "result_id",
    "item_id",
    "site_id",
    "inspector_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|plan_readiness_id,inspection_scope,sampling_method,sample_size,revision,status,release_blocker
2|plan_revision_id,previous_revision,next_revision,change_reason,approval_state,effective_date,revision_hash
3|sampling_scheme_id,risk_score,aql_level,confidence_level,sample_size,skip_lot_rule,escalation_rule
4|genealogy_id,batch_id,parent_lot,child_lot,production_order,receipt_reference,trace_depth
5|test_definition_id,characteristic,method,unit,lower_spec,upper_spec,procedure_reference
6|procedure_lock_id,procedure_revision,execution_revision,lock_reason,override_policy,approver,execution_state
7|calibration_readiness_id,asset_id,calibration_status,due_date,tolerance,restriction,readiness_decision
8|calibration_escalation_id,asset_id,schedule_gap,escalation_owner,production_impact,mitigation,escalation_status
9|result_lifecycle_id,current_state,next_state,transition_reason,inspector,approval_state,transition_validity
10|measurement_integrity_id,series_id,measurement_count,outlier_count,missing_value_count,unit_consistency,integrity_hash
11|spc_engine_id,chart_type,mean,sigma,upper_control,lower_control,cpk
12|defect_taxonomy_id,defect_class,severity,category_owner,containment_rule,escape_risk,retirement_status
13|hold_policy_id,hold_reason,severity_threshold,scope_rule,containment_required,approver,hold_decision
14|containment_map_id,hold_id,lot_scope,inventory_locations,customer_shipments,supplier_receipts,containment_status
15|hold_release_id,release_criteria,evidence_packet,approver,release_time,residual_risk,release_decision
16|nonconformance_intake_id,source,result_link,defect_class,severity,root_cause_hint,completeness_status
17|disposition_engine_id,disposition_options,risk_score,cost_impact,customer_impact,approval_requirement,decision
18|capa_lifecycle_id,capa_id,corrective_action,preventive_action,owner,due_date,effectiveness_check
19|root_cause_workbench_id,method,fishbone_factors,why_chain,evidence_links,hypothesis,confirmed_cause
20|supplier_scorecard_id,supplier_id,defect_rate,on_time_response,capa_closure,score_trend,risk_tier
21|supplier_incident_id,supplier_id,incident_type,containment_request,response_due,escalation_state,closure_status
22|customer_quality_case_id,customer_id,case_type,affected_lot,complaint_evidence,customer_response,closure_status
23|escape_risk_id,defect_signal,shipment_exposure,customer_exposure,risk_score,mitigation,alert_state
24|release_package_id,lot_id,inspection_summary,hold_status,nonconformance_status,certificate_status,release_state
25|compliance_package_id,standard,required_artifact,artifact_status,approval_record,export_target,package_state
26|audit_packet_id,audit_scope,minimum_evidence,redaction_rule,proof_reference,recipient,packet_status
27|zk_quality_proof_id,proof_channel,claim,commitment_hash,verifier,disclosure_scope,proof_status
28|policy_screening_id,policy_rule,screened_fact,decision,explanation,override_required,screening_state
29|parameter_guardrail_id,parameter_name,min_value,max_value,current_value,impact_scope,guardrail_status
30|schema_extension_id,target_table,new_field,relationship,compatibility,approval_state,boundary_check
31|inbox_projection_id,event_type,projection_name,idempotency_key,source_boundary,handler_status,projection_state
32|outbox_delivery_id,event_id,topic,delivery_attempt,retry_state,dead_letter_rule,delivery_status
33|boundary_proof_id,adjacent_domain,dependency_contract,shared_table_probe,projection_name,api_reference,boundary_decision
34|workbench_coverage_id,panel_name,queue_name,metric_name,action_binding,permission,coverage_state
35|inspector_console_id,inspection_step,measurement_entry,defect_entry,offline_state,submission_state,operator_feedback
36|manager_exception_id,exception_type,severity,owner,aging_bucket,decision_action,escalation_state
37|agent_mutation_plan_id,intent,preview_payload,required_evidence,permission_check,human_confirmation,write_block
38|document_intake_id,document_type,instruction_text,extracted_entities,attachment_hash,reviewer,intake_state
39|semantic_instruction_id,source_text,parsed_step,test_mapping,safety_warning,confidence,review_state
40|sampling_simulation_id,scenario_name,changed_parameter,affected_lots,escape_delta,cost_delta,simulation_state
41|defect_forecast_id,model_id,horizon,defect_probability,escape_probability,confidence,forecast_state
42|anomaly_detection_id,signal_name,entropy_score,outlier_reason,affected_lot,review_queue,anomaly_state
43|model_evidence_id,model_id,purpose,training_set,validation_metric,approval_state,drift_status
44|certificate_identity_id,lot_identity,issuer,credential_hash,holder,revocation_status,identity_state
45|carbon_schedule_id,inspection_window,energy_signal,carbon_intensity,deadline_risk,chosen_slot,schedule_state
46|resilience_drill_id,drill_type,failure_mode,recovery_route,rto_result,rpo_result,drill_state
47|continuous_control_id,control_rule,population,failing_sample,owner,remediation,closure_evidence
48|shift_close_packet_id,shift_id,open_holds,open_nonconformances,release_queue,handoff_owner,close_state
49|readiness_score_id,score_component,weight,actual_score,gap_reason,owner,readiness_state
50|release_proof_id,feature_count,domain_tests,traceability_matrix,release_evidence,approval_record,release_decision
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    4: ("ProductionCompleted", "GoodsReceiptPosted", "InventoryLotMoved"),
    7: ("CalibrationAssetChanged",),
    8: ("CalibrationAssetChanged",),
    20: ("SupplierScoreChanged",),
    21: ("SupplierScoreChanged",),
    22: ("CustomerQualityCaseOpened",),
    24: ("AuditEventSealed",),
    27: ("AuditEventSealed",),
    31: ("ProductionCompleted", "GoodsReceiptPosted", "InventoryLotMoved"),
    33: ("AuditEventSealed",),
    44: ("CertificateIdentityIssued",),
    50: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 2, 6, 7, 9, 13, 15, 16, 17, 18, 21, 22, 24, 25, 28, 30, 35, 36, 37, 38, 43, 44, 48, 50)
_SUPERVISOR_APPROVAL_FEATURES = (2, 6, 13, 15, 17, 18, 21, 24, 25, 28, 29, 30, 36, 43, 46, 48, 50)
_NON_MUTATING_FEATURES = (3, 4, 5, 7, 8, 10, 11, 12, 14, 19, 20, 23, 26, 27, 29, 31, 32, 33, 34, 37, 38, 39, 40, 41, 42, 45, 46, 47, 49, 50)
_AI_PREVIEW_FEATURES = (37, 38, 39, 40, 41, 42, 43, 49, 50)
_COMPLIANCE_EVIDENCE_FEATURES = (1, 2, 5, 6, 7, 9, 10, 13, 15, 18, 24, 25, 26, 27, 28, 30, 33, 43, 44, 47, 48, 50)
_QUALITY_RISK_FEATURES = (3, 4, 11, 12, 14, 16, 17, 19, 20, 21, 22, 23, 36, 40, 41, 42, 45, 46, 49, 50)
_PROJECTION_ONLY_FEATURES = (4, 7, 8, 20, 21, 22, 24, 27, 31, 33, 44, 50)


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
        "tables": (f"quality_assurance_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"QualityAssurance{_camel(capability.slug)}Panel",
        "route": f"POST /quality-assurance/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in QA_CAPABILITIES}


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
        "event_topic": QA_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "supervisor_approval": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "compliance_evidence_complete": True,
        "quality_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned quality evidence, UI, service/API, event, control, agent, and release proof before approval.")
    if number in _COMPLIANCE_EVIDENCE_FEATURES and payload.get("compliance_evidence_complete") is not True:
        findings.append("inspection plans, revisions, test definitions, procedure locks, calibration, lifecycle transitions, holds, CAPA, release packages, compliance packets, audits, proofs, policies, schemas, boundary proof, model evidence, lot identity, controls, close packets, and release gates require compliance evidence")
    if number in _QUALITY_RISK_FEATURES and payload.get("quality_risk_evidence_complete") is not True:
        findings.append("sampling, genealogy, SPC, defects, containment, nonconformance, disposition, root cause, supplier, customer, escape, exceptions, simulations, forecasts, anomalies, carbon scheduling, resilience, readiness, and release proof require quality risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("quality-changing plans, revisions, procedure locks, calibration readiness, result transitions, holds, dispositions, CAPA, incidents, releases, policies, schema changes, inspector actions, agent mutation plans, documents, model approvals, identities, close packets, and release gates require human confirmation")
    if number in _SUPERVISOR_APPROVAL_FEATURES and payload.get("supervisor_approval") is not True:
        findings.append("revision control, procedure overrides, hold creation/release, disposition, CAPA, supplier incidents, release packages, compliance packages, policies, parameters, schemas, exceptions, models, resilience drills, close packets, and release gates require quality manager approval")
    if number in _AI_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("quality agent skills must produce cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("sampling, genealogy, test definitions, calibration, measurements, SPC, taxonomy, containment, root cause, supplier scorecards, escape scoring, audit minimization, ZK proof, parameters, inbox/outbox, boundary, workbench, agents, simulations, forecasts, anomalies, carbon schedules, resilience, controls, readiness, and release proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("production, receipt, inventory, supplier, calibration, customer, certificate, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != QA_REQUIRED_EVENT_TOPIC:
        findings.append("quality assurance eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in QA_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary quality assurance datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("quality assurance controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_quality_assurance_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in QA_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in QA_DECLARED_DEPENDENCIES)
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
        "required_event_topic": QA_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": QA_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "slug": resolved.slug,
        "title": resolved.title,
        "capability": resolved.as_traceability_row(),
        "payload": candidate,
        "evidence": evidence,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "side_effects": (),
    }


def improve1_quality_assurance_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_quality_assurance_control(capability) for capability in QA_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.quality-assurance-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": QA_OWNED_TABLES,
        "declared_dependencies": QA_DECLARED_DEPENDENCIES,
        "allowed_database_backends": QA_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": QA_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


QUALITY_ASSURANCE_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_quality_assurance_control(slug, payload)) for capability in QA_CAPABILITIES}
