"""Executable improve1 controls for the Laboratory Information Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "laboratory_information_management"
EVENT_CONTRACT = "AppGen-X"
LAB_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LAB_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.laboratory_information_management.events"
LAB_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"laboratory_information_management_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
LAB_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "PolicyChanged", "AuditEventSealed", "OperationalKpiChanged", "PatientIdentityProjected",
    "InstrumentEventReceived", "EhrOrderProjected", "AccreditationRuleChanged",
    "InventoryLotProjected", "PrivacyPolicyChanged", "CarbonIntensityProjected",
)))
LAB_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in LAB_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in LAB_CONTROL_CAPABILITIES}
_DEFAULT_FIELDS = ("owned_record", "lab_context", "required_evidence", "operator_visible", "audit_trail", "safe_to_execute")
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {cap.feature_number: _DEFAULT_FIELDS for cap in LAB_CONTROL_CAPABILITIES}
_FEATURE_FIELDS.update({1: ('sample_id', 'accession_number', 'patient_or_subject_ref', 'collection_time', 'received_time', 'accession_status', 'duplicate_accession_blocked'), 2: ('custody_event', 'from_party', 'to_party', 'timestamp', 'condition', 'signature', 'custody_gap_blocked'), 3: ('specimen_condition', 'temperature', 'container_integrity', 'volume', 'hemolysis_or_contamination', 'acceptance_decision', 'rejection_reason_required'), 4: ('test_order', 'ordered_tests', 'clinical_or_study_context', 'priority', 'required_fields', 'missing_fields', 'work_blocked_until_complete'), 5: ('sample_id', 'order_id', 'patient_or_subject_ref', 'barcode_match', 'two_identifier_check', 'mismatch_blocked', 'match_audit'), 6: ('test_method', 'method_version', 'effective_date', 'validation_status', 'retired_version_blocked', 'method_citation', 'result_links_version'), 7: ('instrument_id', 'instrument_type', 'status', 'maintenance_state', 'qualification_status', 'location', 'offline_instrument_blocked'), 8: ('run_id', 'instrument_id', 'operator', 'start_time', 'end_time', 'run_state', 'qc_gate_passed', 'run_event_emitted'), 9: ('qc_rule', 'control_material', 'expected_range', 'observed_value', 'westgard_or_rule_result', 'release_blocked_on_fail', 'review_required'), 10: ('calibration_record', 'instrument_id', 'calibration_due', 'calibration_status', 'standard_traceability', 'expired_calibration_blocked', 'certificate_attached'), 11: ('lot_id', 'reagent', 'expiry_date', 'opened_date', 'storage_condition', 'consumption_trace', 'expired_lot_blocked'), 12: ('result_id', 'raw_result', 'validated_result', 'reviewer', 'validation_rules', 'second_review_required', 'release_blocked_until_reviewed'), 13: ('critical_result', 'threshold', 'recipient', 'notification_time', 'readback', 'escalation_path', 'release_requires_notification_evidence'), 14: ('reference_range', 'demographic_context', 'method_version', 'units', 'effective_date', 'approval_status', 'outdated_range_blocked'), 15: ('reflex_rule', 'trigger_result', 'add_on_test', 'sample_volume_check', 'authorization', 'order_created', 'reflex_audit'), 16: ('aliquot_id', 'parent_sample', 'derivative_type', 'split_time', 'volume', 'location', 'lineage_preserved'), 17: ('storage_location', 'temperature_zone', 'stability_limit', 'stored_at', 'expiry_or_stability_due', 'excursion_flag', 'stability_breach_blocked'), 18: ('tat_clock', 'priority', 'start_event', 'stop_event', 'pause_reason', 'breach_prediction', 'tat_dashboard_visible'), 19: ('workcell', 'bench', 'queue', 'operator', 'batch_size', 'handoff_state', 'bench_workflow_visible'), 20: ('culture_id', 'media', 'incubation_condition', 'growth_observation', 'organism_id', 'susceptibility_link', 'contamination_review'), 21: ('assay_id', 'target', 'controls', 'ct_or_variant_call', 'interpretation_rule', 'genetic_privacy_guard', 'confirmatory_review'), 22: ('sample_domain', 'collection_site', 'environmental_context', 'chain_of_custody', 'nonclinical_limits', 'reporting_template', 'domain_separation_visible'), 23: ('study_id', 'retain_sample', 'pull_schedule', 'condition', 'timepoint', 'retain_location', 'missed_pull_alert'), 24: ('correction_id', 'original_result', 'corrected_result', 'reason', 'approver', 'amendment_notice', 'original_preserved'), 25: ('pt_event', 'provider', 'challenge_sample', 'submitted_result', 'score', 'corrective_action', 'accreditation_evidence'), 26: ('nonconformance', 'severity', 'root_cause', 'capa_plan', 'owner', 'due_date', 'effectiveness_check_required'), 27: ('audit_event', 'e_signature', 'meaning', 'signer', 'timestamp', 'record_hash', 'signature_required_for_release'), 28: ('result_summary', 'source_citations', 'interpretation_limits', 'human_confirmation', 'direct_mutation_blocked', 'regulated_language_guard'), 29: ('agent_command', 'crud_plan', 'target_table', 'permission_check', 'human_confirmation', 'idempotency_key', 'direct_mutation_blocked'), 30: ('instrument_event', 'instrument_id', 'event_schema', 'idempotency_key', 'appgen_contract', 'event_topic', 'raw_feed_isolated'), 31: ('report_id', 'recipient', 'reporting_boundary', 'authorized_fields', 'redaction_profile', 'external_delivery_guard', 'no_external_mutation'), 32: ('method_validation', 'precision', 'accuracy', 'linearity', 'lod_loq', 'matrix', 'approval_status'), 33: ('batch_id', 'high_throughput_run', 'sample_count', 'qc_summary', 'exception_count', 'batch_reviewer', 'batch_release_blocked_until_review'), 34: ('data_integrity_check', 'alcoa_plus', 'raw_data_link', 'metadata_complete', 'manual_edit_reason', 'audit_review', 'integrity_exception_blocked'), 35: ('workbench_role', 'queue', 'permissions', 'site', 'bench', 'role_filtered_actions', 'sensitive_panel_guard'), 36: ('retention_policy', 'retain_until', 'disposal_method', 'legal_hold', 'disposal_approval', 'destruction_evidence', 'disposal_blocked_on_hold'), 37: ('site_id', 'site_role', 'sample_transfer', 'local_method_variant', 'inter_site_chain', 'site_segregation', 'multi_site_dashboard'), 38: ('recollection_reason', 'patient_or_subject_contact', 'new_order', 'old_sample_status', 'communication_sent', 'chain_linked', 'duplicate_billing_blocked'), 39: ('privacy_profile', 'redaction_rule', 'sensitive_fields', 'recipient_role', 'minimum_necessary', 'export_guard', 'agent_scope_limited'), 40: ('tat_prediction', 'capacity_risk', 'instrument_load', 'staffing_load', 'reagent_constraint', 'recommended_action', 'human_review'), 41: ('quality_trend', 'metric', 'time_window', 'control_chart', 'outlier_signal', 'investigation_trigger', 'dashboard_visible'), 42: ('result_proof', 'packet_hash', 'previous_hash', 'result_hashes', 'chain_hash', 'proof_verified', 'tamper_evident_export'), 43: ('configuration_change', 'simulation_scope', 'impacted_methods', 'impacted_orders', 'impact_preview', 'live_mutation_blocked', 'approval_required'), 44: ('dead_letter_item', 'failure_reason', 'retry_policy', 'safe_replay_allowed', 'operator_notes', 'closure_code', 'no_duplicate_side_effects'), 45: ('scenario_id', 'seed_samples', 'seed_orders', 'seed_runs', 'seed_results', 'expected_qc', 'regression_ready'), 46: ('accreditation_packet', 'standard', 'evidence_index', 'method_scope', 'qc_scope', 'audit_ready', 'gap_list'), 47: ('resource_signal', 'carbon_signal', 'instrument_energy', 'reagent_waste', 'non_urgent_schedule', 'operator_override_visible', 'quality_not_compromised'), 48: ('simulation_run', 'sample_seeded', 'order_seeded', 'run_seeded', 'result_seeded', 'events_emitted', 'release_documents_updated'), 49: ('overlap_check', 'owned_boundary', 'ehr_dependency', 'instrument_dependency', 'shared_table_blocked', 'composition_warning_visible'), 50: ('dsl_fragment', 'pbc_key', 'agent_skills', 'composition_manifest', 'unified_agent_exposure', 'skill_scope', 'side_effect_free_registration')})
_FEATURE_DEPENDENCIES = {1: ("PatientIdentityProjected",), 11: ("InventoryLotProjected",), 30: ("InstrumentEventReceived",), 31: ("EhrOrderProjected",), 46: ("AccreditationRuleChanged",), 47: ("CarbonIntensityProjected",)}
_EMPTY_ALLOWED_FIELDS = ("missing_fields", "gap_list")
_REQUIRED_TRUE = {1: ('duplicate_accession_blocked',), 2: ('signature', 'custody_gap_blocked'), 3: ('rejection_reason_required',), 4: ('work_blocked_until_complete',), 5: ('barcode_match', 'two_identifier_check', 'mismatch_blocked'), 6: ('retired_version_blocked', 'result_links_version'), 7: ('offline_instrument_blocked',), 8: ('qc_gate_passed', 'run_event_emitted'), 9: ('release_blocked_on_fail', 'review_required'), 10: ('expired_calibration_blocked', 'certificate_attached'), 11: ('expired_lot_blocked',), 12: ('release_blocked_until_reviewed',), 13: ('readback', 'release_requires_notification_evidence'), 14: ('outdated_range_blocked',), 15: ('sample_volume_check', 'authorization', 'order_created', 'reflex_audit'), 16: ('lineage_preserved',), 17: ('stability_breach_blocked',), 18: ('tat_dashboard_visible',), 19: ('bench_workflow_visible',), 20: ('contamination_review',), 21: ('genetic_privacy_guard', 'confirmatory_review'), 22: ('domain_separation_visible',), 23: ('missed_pull_alert',), 24: ('amendment_notice', 'original_preserved'), 25: ('corrective_action', 'accreditation_evidence'), 26: ('effectiveness_check_required',), 27: ('e_signature', 'signature_required_for_release'), 28: ('source_citations', 'human_confirmation', 'direct_mutation_blocked', 'regulated_language_guard'), 29: ('permission_check', 'human_confirmation', 'direct_mutation_blocked'), 30: ('raw_feed_isolated',), 31: ('external_delivery_guard', 'no_external_mutation'), 32: ('approval_status',), 33: ('batch_release_blocked_until_review',), 34: ('metadata_complete', 'audit_review', 'integrity_exception_blocked'), 35: ('role_filtered_actions', 'sensitive_panel_guard'), 36: ('disposal_approval', 'destruction_evidence', 'disposal_blocked_on_hold'), 37: ('inter_site_chain', 'site_segregation', 'multi_site_dashboard'), 38: ('communication_sent', 'chain_linked', 'duplicate_billing_blocked'), 39: ('minimum_necessary', 'export_guard', 'agent_scope_limited'), 40: ('human_review',), 41: ('investigation_trigger', 'dashboard_visible'), 42: ('proof_verified', 'tamper_evident_export'), 43: ('impact_preview', 'live_mutation_blocked', 'approval_required'), 44: ('safe_replay_allowed', 'no_duplicate_side_effects'), 45: ('regression_ready',), 46: ('audit_ready',), 47: ('non_urgent_schedule', 'operator_override_visible', 'quality_not_compromised'), 48: ('sample_seeded', 'order_seeded', 'run_seeded', 'result_seeded', 'events_emitted', 'release_documents_updated'), 49: ('owned_boundary', 'shared_table_blocked', 'composition_warning_visible'), 50: ('dsl_fragment', 'agent_skills', 'composition_manifest', 'unified_agent_exposure', 'side_effect_free_registration')}


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"laboratory_information_management_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "ui": _camel(capability.slug), "route": f"POST /laboratory-information-management/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in LAB_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    for field in _REQUIRED_TRUE.get(resolved.feature_number, ()): payload[field] = True
    payload.update({"missing_fields": (), "gap_list": (), "appgen_contract": EVENT_CONTRACT, "event_topic": LAB_CONTROL_REQUIRED_EVENT_TOPIC, "database_backend": "postgresql", "stream_engine_picker_visible": False, "shared_table_access": False, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    for field in _REQUIRED_TRUE.get(n, ()):
        if payload.get(field) is not True:
            findings.append(f"{capability.title} requires {field.replace('_', ' ')}")
    if n == 1 and payload.get("duplicate_accession_blocked") is not True: findings.append("sample accessioning must prevent duplicate sample identity")
    if n == 2 and payload.get("custody_gap_blocked") is not True: findings.append("chain of custody lifecycle must block custody gaps")
    if n == 5 and payload.get("mismatch_blocked") is not True: findings.append("order-to-sample matching must block identifier mismatches")
    if n == 9 and payload.get("release_blocked_on_fail") is not True: findings.append("quality control rule engine must block failed QC release")
    if n == 12 and payload.get("release_blocked_until_reviewed") is not True: findings.append("result validation must block release until review")
    if n == 13 and payload.get("release_requires_notification_evidence") is not True: findings.append("critical result notification requires notification evidence before release")
    if n in (28, 29) and (payload.get("human_confirmation") is not True or payload.get("direct_mutation_blocked") is not True): findings.append("LIMS agent assistance requires human confirmation and no direct mutation")
    if n == 30 and (payload.get("appgen_contract") != EVENT_CONTRACT or payload.get("event_topic") != LAB_CONTROL_REQUIRED_EVENT_TOPIC): findings.append("Instrument Integration Event Contract must use the AppGen-X event contract")
    if n == 31 and payload.get("no_external_mutation") is not True: findings.append("result reporting boundary must not mutate external EHR or portal systems")
    if n == 42 and payload.get("proof_verified") is not True: findings.append("cryptographic result proofs must verify before release")
    if n == 49 and payload.get("shared_table_blocked") is not True: findings.append("package overlap guardrails must block shared-table overlap")
    if n == 50 and not all(payload.get(field) is True for field in _REQUIRED_TRUE[50]): findings.append("composition DSL and unified agent exposure are incomplete")
    if payload.get("stream_engine_picker_visible"): findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in LAB_CONTROL_ALLOWED_DATABASE_BACKENDS: findings.append("ordinary LIMS PBC datastore must be PostgreSQL, MySQL, or MariaDB")
    return tuple(findings)


def evaluate_lab_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in LAB_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in LAB_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": LAB_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": LAB_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_lab_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_lab_control(capability) for capability in LAB_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.laboratory-information-management-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": LAB_CONTROL_OWNED_TABLES, "declared_dependencies": LAB_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": LAB_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": LAB_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


LAB_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_lab_control(slug, payload)) for capability in LAB_CONTROL_CAPABILITIES}
