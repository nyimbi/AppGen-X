"""Executable improve1 controls for the Pharma Manufacturing Quality PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import PHARMA_MANUFACTURING_QUALITY_ALLOWED_DATABASE_BACKENDS, PHARMA_MANUFACTURING_QUALITY_OWNED_TABLES, PHARMA_MANUFACTURING_QUALITY_REQUIRED_EVENT_TOPIC

PBC_KEY = "pharma_manufacturing_quality"
EVENT_CONTRACT = "AppGen-X"
QUALITY_CONTROL_ALLOWED_DATABASE_BACKENDS = PHARMA_MANUFACTURING_QUALITY_ALLOWED_DATABASE_BACKENDS
QUALITY_CONTROL_REQUIRED_EVENT_TOPIC = PHARMA_MANUFACTURING_QUALITY_REQUIRED_EVENT_TOPIC
QUALITY_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(PHARMA_MANUFACTURING_QUALITY_OWNED_TABLES + tuple(f"pharma_manufacturing_quality_{c.slug}_control" for c in IMPROVE1_CAPABILITIES)))
QUALITY_CONTROL_DECLARED_DEPENDENCIES = (
    "PolicyChanged", "AuditEventSealed", "OperationalKpiChanged", "SupplierQualified", "EquipmentQualified",
    "EnvironmentalMonitoringAlerted", "MaterialLotReceived", "SerializationEventReceived", "ComplaintReceived",
    "RegulatoryInspectionOpened", "CarbonIntensityWindowChanged", "ModelGovernanceChanged", "LabelArtworkChanged",
)
QUALITY_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {c.feature_number: c for c in QUALITY_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {c.slug: c for c in QUALITY_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "site_id", "product_id", "batch_id", "mbr_id", "lot_id", "equipment_id", "quality_event_id", "actor_id", "gmp_region", "policy_version", "evidence_references")
_FIELD_ROWS = """
1|mbr_version,approved_formula,process_step_set,effective_date,obsolete_version,qa_approval
2|ebr_step_id,operator_entry,expected_value,exception_flag,e_signature,step_sequence
3|material_lot_id,input_lot,output_lot,supplier_lot,genealogy_depth,trace_hash
4|equipment_train_id,qualification_state,cleaning_status,calibration_due,changeover_clearance,boundary_exception
5|cpp_id,target_range,actual_value,trend_state,alarm_status,deviation_link
6|ipc_test_id,sampling_point,specification,observed_result,analyst,lab_review_status
7|em_sample_id,room_grade,excursion_level,batch_linkage,investigation_ref,trend_context
8|deviation_id,deviation_type,severity,detectability,product_impact,triage_owner
9|rca_id,hypothesis,evidence_set,method,root_cause_category,qa_conclusion
10|capa_id,action_type,effectiveness_check,due_date,owner,closure_evidence
11|change_control_id,change_type,impacted_mbr,validation_impact,regulatory_impact,implementation_state
12|validation_protocol_id,protocol_type,acceptance_criteria,execution_state,deviation_link,approval_state
13|cpv_id,process_signal,control_limit,trend_result,annual_review_link,action_required
14|cleaning_verification_id,cleaning_method,hold_time_start,hold_time_limit,residue_result,release_decision
15|mixup_control_id,line_clearance,label_reconciliation,segregation_check,contamination_risk,qa_confirmed
16|batch_genealogy_id,parent_batch,child_batch,material_flow,process_stage,traceability_proof
17|serialization_event_id,packaging_level,event_type,serial_count,partner_message,exception_status
18|release_checklist_id,qa_disposition,required_tests,deviation_clearance,label_reconciliation,release_signature
19|quarantine_id,hold_reason,disposition_path,material_status,release_block,destruction_proof
20|stability_study_id,pull_point,storage_condition,test_result,trend_state,expiry_impact
21|oos_oot_id,specification_result,phase,lab_error_check,manufacturing_impact,qa_decision
22|supplier_event_id,supplier_lot,qualification_status,material_impact,scara_link,containment_action
23|training_gate_id,role,training_record,qualification_state,task_restriction,supervisor_override
24|document_record_id,document_class,revision,approval_workflow,retention_rule,controlled_copy
25|data_integrity_id,alcoa_check,audit_trail_gap,manual_entry_reason,reviewer,remediation_action
26|workbench_case_id,deviation_queue,capa_queue,aging_bucket,priority_score,management_review_link
27|narrative_id,source_records,citation_set,generated_summary,reviewer_edit,human_approval
28|agent_command_id,crud_preview,owned_table,permission_check,expected_event,confirmation_record
29|qrm_id,hazard,probability,severity,detectability,risk_control
30|recall_impact_id,impacted_lots,market_distribution,complaint_link,regulatory_notice,field_action
31|complaint_link_id,complaint_source,batch_match,investigation_state,adverse_event_flag,response_due
32|inspection_room_id,request_item,evidence_packet,redaction_rule,inspector_access,audit_log
33|tech_transfer_id,sending_site,receiving_site,process_equivalence,validation_gap,approval_state
34|packaging_reconciliation_id,label_lot,expected_count,actual_count,destruction_count,variance_reason
35|hold_expiry_id,hold_start,expiry_date,extension_reason,qa_approval,release_block
36|metrics_pack_id,deviation_rate,capa_overdue_rate,right_first_time,review_period,management_action
37|predictive_risk_id,feature_vector,batch_risk_score,release_delay_probability,reason_codes,model_version
38|simulation_id,configuration_change,impacted_batches,validation_delta,quality_risk_delta,decision_preview
39|boundary_proof_id,owned_table_check,supplier_table_block,equipment_table_block,ledger_table_block,foreign_write_block
40|signature_meaning_id,meaning,signer_role,credential_strength,part11_statement,signature_hash
41|audit_review_id,audit_trail_scope,review_frequency,exception_count,reviewer,closure_state
42|crypto_proof_id,batch_hash,mbr_hash,ebr_hash,release_hash,verifier_api
43|dead_letter_id,event_type,retry_count,owner,replay_eligibility,recovery_evidence
44|carbon_resource_id,processing_window,resource_intensity,quality_deadline,selected_window,tradeoff
45|scenario_pack_id,scenario_type,fixture_records,expected_events,regression_assertions,release_reference
46|permission_model_id,role,permission_set,segregation_check,approval_scope,least_privilege_proof
47|localization_id,market,regulation_set,label_requirement,release_requirement,translation_evidence
48|release_simulation_id,mbr_ready,ebr_complete,qa_events_clear,serialization_clear,release_decision
49|overlap_guardrail_id,domain_boundary,adjacent_pbc,shared_table_block,api_projection_contract,exception_reason
50|composition_dsl_id,pbc_key,skills_namespace,agent_capability,ui_mount,dependency_contract
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    4: ("EquipmentQualified",), 7: ("EnvironmentalMonitoringAlerted",), 17: ("SerializationEventReceived",),
    22: ("SupplierQualified", "MaterialLotReceived"), 30: ("ComplaintReceived",), 31: ("ComplaintReceived",),
    32: ("RegulatoryInspectionOpened", "AuditEventSealed"), 34: ("LabelArtworkChanged",), 36: ("OperationalKpiChanged",),
    37: ("ModelGovernanceChanged",), 41: ("AuditEventSealed",), 43: ("AuditEventSealed",),
    44: ("CarbonIntensityWindowChanged",), 47: ("PolicyChanged",), 49: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 2, 4, 8, 9, 10, 11, 12, 15, 18, 19, 21, 23, 27, 28, 30, 32, 33, 35, 40, 46, 48, 50)
_PROJECTION_ONLY_FEATURES = (4, 7, 17, 22, 30, 31, 32, 34, 36, 37, 41, 43, 44, 47, 49)
_AGENT_PREVIEW_FEATURES = (27, 28, 50)
_NON_MUTATING_FEATURES = (13, 26, 27, 29, 30, 32, 36, 37, 38, 39, 41, 42, 44, 45, 48, 49, 50)
_QUALITY_RISK_FEATURES = (1, 2, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 18, 19, 21, 23, 25, 29, 30, 32, 34, 35, 37, 40, 41, 42, 43, 48, 49, 50)


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"pharma_manufacturing_quality_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number], "ui": f"PharmaManufacturingQuality{_camel(capability.slug)}Panel", "route": f"POST /pharma-manufacturing-quality/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in QUALITY_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": QUALITY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "dependency_access_mode": "api_event_projection", "human_confirmation": True, "agent_preview_only": True, "non_mutating_simulation": True, "quality_risk_evidence_complete": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires GMP-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _QUALITY_RISK_FEATURES and payload.get("quality_risk_evidence_complete") is not True:
        findings.append("MBR, EBR, genealogy, equipment, CPP, IPC, EM, deviation, CAPA, validation, release, OOS/OOT, supplier, data integrity, recall, signature, audit, and release simulation decisions require complete quality risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("GMP approvals, batch execution exceptions, deviations, CAPA, validation, release, quarantine, OOS/OOT, training, agent commands, inspection rooms, tech transfer, signature, permissions, and release simulations require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("quality agent skills must return cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("CPV, workbench analytics, narratives, QRM, recall impact, evidence rooms, metrics, predictive risk, simulations, boundary proofs, audit, crypto proofs, carbon, seed packs, release simulation, overlap, and DSL exposure must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("equipment, environmental, serialization, supplier, complaint, inspection, label, KPI, model, audit, carbon, regulatory, and boundary facts must use APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != QUALITY_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("pharma quality eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in QUALITY_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary pharma quality datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("pharma quality controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_quality_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in QUALITY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in QUALITY_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "primary_proof": spec["primary_proof"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": QUALITY_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": QUALITY_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_quality_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_quality_control(capability) for capability in QUALITY_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.pharma-manufacturing-quality-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": QUALITY_CONTROL_OWNED_TABLES, "declared_dependencies": QUALITY_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": QUALITY_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": QUALITY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


QUALITY_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_quality_control(slug, payload)) for capability in QUALITY_CONTROL_CAPABILITIES}
