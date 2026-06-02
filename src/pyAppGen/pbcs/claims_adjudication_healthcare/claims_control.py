"""Executable healthcare claims adjudication controls for improve1 execution."""
from __future__ import annotations

from datetime import date, datetime
import hashlib
import json
from typing import Callable, Mapping

PBC_KEY = "claims_adjudication_healthcare"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = ('claims_adjudication_healthcare_health_claim', 'claims_adjudication_healthcare_claim_line', 'claims_adjudication_healthcare_coding_review', 'claims_adjudication_healthcare_benefit_rule', 'claims_adjudication_healthcare_denial', 'claims_adjudication_healthcare_appeal', 'claims_adjudication_healthcare_payment_integrity_case', 'claims_adjudication_healthcare_policy_rule', 'claims_adjudication_healthcare_runtime_parameter', 'claims_adjudication_healthcare_schema_extension', 'claims_adjudication_healthcare_control_assertion', 'claims_adjudication_healthcare_governed_model', 'claims_adjudication_healthcare_document_instruction', 'claims_adjudication_healthcare_appgen_outbox_event', 'claims_adjudication_healthcare_appgen_inbox_event', 'claims_adjudication_healthcare_appgen_dead_letter_event')
CLAIMS_CONTROL_CAPABILITIES = (
    'claim_intake_canonicalization',
    'claim_lifecycle_state_machine',
    'claim_line_granularity',
    'member_eligibility_projection_boundary',
    'provider_network_credential_projection_boundary',
    'benefit_rule_versioning',
    'medical_necessity_review',
    'prior_authorization_matching',
    'coding_validation_engine',
    'coordination_of_benefits',
    'deductible_coinsurance_copay_application',
    'contract_pricing_allowed_amount',
    'claim_pend_reason_taxonomy',
    'denial_reason_governance',
    'appeal_lifecycle',
    'duplicate_claim_detection',
    'payment_integrity_case_management',
    'fraud_waste_abuse_signal_review',
    'attachment_medical_record_handling',
    'corrected_replacement_claim_lineage',
    'overpayment_recovery_workflow',
    'claim_adjustment_reversal',
    'benefit_limit_tracking',
    'bundling_unbundling_detection',
    'inpatient_episode_claim_logic',
    'professional_claim_specialty_logic',
    'member_provider_notice_generation',
    'sla_timeliness_management',
    'adjudication_explainability_packet',
    'rule_conflict_impact_simulation',
    'claims_operations_workbench',
    'agent_assisted_claim_review',
    'governed_agent_crud_commands',
    'model_governance_claim_intelligence',
    'continuous_control_assertions',
    'dead_letter_retry_queue',
    'cross_pbc_dependency_freshness',
    'low_value_care_policy_analytics',
    'provider_dispute_workflow',
    'subrogation_third_party_liability',
    'claim_audit_sampling',
    'cryptographic_adjudication_proofs',
    'privacy_minimum_necessary_views',
    'correction_erroneous_denials',
    'seeded_adjudication_scenario_library',
    'financial_reconciliation_contract',
    'regulatory_reporting_extracts',
    'full_claims_release_simulation',
    'package_boundary_proofs',
    'composition_dsl_unified_agent_exposure',
)
REQUIRED_FIELDS = {
    'claim_intake_canonicalization': ('claim_type', 'source_format', 'submitter', 'batch_id', 'canonical_identity'),
    'claim_lifecycle_state_machine': ('current_state', 'target_state', 'transition_reason', 'actor', 'original_outcome'),
    'claim_line_granularity': ('service_date', 'diagnosis_pointers', 'procedure_code', 'modifier_stack', 'line_payment_state'),
    'member_eligibility_projection_boundary': ('projection_source', 'plan_version', 'source_time', 'freshness', 'fallback_behavior'),
    'provider_network_credential_projection_boundary': ('provider_status', 'contract_basis', 'network_tier', 'credential_freshness', 'projection_version'),
    'benefit_rule_versioning': ('plan_id', 'service_type', 'effective_window', 'approval_evidence', 'rule_version'),
    'medical_necessity_review': ('clinical_basis', 'documentation_required', 'reviewer_qualification', 'determination', 'appeal_rights'),
    'prior_authorization_matching': ('member_id', 'provider_id', 'service_code', 'service_date', 'remaining_units'),
    'coding_validation_engine': ('diagnosis_code', 'procedure_code', 'modifier_stack', 'place_of_service', 'documentation_support'),
    'coordination_of_benefits': ('cob_status', 'primary_payer_evidence', 'other_payer_paid', 'residual_responsibility', 'eob_status'),
    'deductible_coinsurance_copay_application': ('deductible', 'copay', 'coinsurance', 'oop_cap', 'accumulator_version'),
    'contract_pricing_allowed_amount': ('pricing_basis', 'contract_reference', 'fee_schedule_version', 'negotiated_rate', 'manual_review_state'),
    'claim_pend_reason_taxonomy': ('pend_reason', 'queue', 'owner_role', 'sla', 'resolution_action'),
    'denial_reason_governance': ('denial_code', 'rationale', 'line_mapping', 'appeal_deadline', 'policy_version'),
    'appeal_lifecycle': ('appeal_level', 'requester', 'evidence_submitted', 'reviewer_independence', 'decision'),
    'duplicate_claim_detection': ('member_id', 'provider_id', 'service_dates', 'codes', 'source_lineage'),
    'payment_integrity_case_management': ('trigger', 'suspected_issue', 'dollar_exposure', 'reviewer', 'recovery_status'),
    'fraud_waste_abuse_signal_review': ('signal_type', 'explanation', 'provider_outlier', 'risk_score', 'human_review'),
    'attachment_medical_record_handling': ('attachment_source', 'linked_lines', 'extracted_facts', 'redaction_profile', 'retention_class'),
    'corrected_replacement_claim_lineage': ('original_claim', 'correction_type', 'replaced_lines', 'financial_delta', 'submission_reason'),
    'overpayment_recovery_workflow': ('overpayment_amount', 'reason', 'notice', 'offset_status', 'dispute_state'),
    'claim_adjustment_reversal': ('adjustment_reason', 'initiator', 'affected_lines', 'before_after_amounts', 'authorization'),
    'benefit_limit_tracking': ('limit_type', 'consumed_amount', 'remaining_amount', 'time_window', 'source_freshness'),
    'bundling_unbundling_detection': ('bundling_rule', 'primary_line', 'bundled_line', 'modifier_exception', 'documentation_requirement'),
    'inpatient_episode_claim_logic': ('episode_group', 'admission_date', 'discharge_date', 'transfer_flag', 'outlier_basis'),
    'professional_claim_specialty_logic': ('provider_specialty', 'place_of_service', 'modifier', 'supervision', 'same_day_services'),
    'member_provider_notice_generation': ('notice_template', 'recipient', 'language', 'appeal_rights', 'delivery_proof'),
    'sla_timeliness_management': ('sla_clock', 'pause_reason', 'jurisdiction', 'service_category', 'escalation_state'),
    'adjudication_explainability_packet': ('input_facts', 'rule_versions', 'projections', 'pricing', 'reviewer_actions'),
    'rule_conflict_impact_simulation': ('sample_claims', 'affected_population', 'financial_impact', 'denial_changes', 'appeal_risk'),
    'claims_operations_workbench': ('intake_rejects', 'pended_claims', 'coding_review', 'appeals', 'sla_risk'),
    'agent_assisted_claim_review': ('claim_summary', 'cited_evidence', 'missing_evidence', 'recommendation', 'confirmation_required'),
    'governed_agent_crud_commands': ('intent', 'claim_reference', 'preview', 'approver', 'command_result'),
    'model_governance_claim_intelligence': ('intended_use', 'model_version', 'evaluation_evidence', 'bias_check', 'drift_status'),
    'continuous_control_assertions': ('population', 'threshold', 'owner', 'failing_sample', 'remediation'),
    'dead_letter_retry_queue': ('failure_class', 'idempotency_key', 'risk_level', 'retry_count', 'replay_checkpoint'),
    'cross_pbc_dependency_freshness': ('dependency', 'freshness_indicator', 'blocking_threshold', 'degraded_mode', 'override_evidence'),
    'low_value_care_policy_analytics': ('avoidable_service', 'denial_pattern', 'overturn_rate', 'provider_education_target', 'low_count_suppression'),
    'provider_dispute_workflow': ('dispute_type', 'disputed_lines', 'requested_correction', 'evidence', 'decision'),
    'subrogation_third_party_liability': ('liability_indicator', 'accident_date', 'third_party_evidence', 'questionnaire_status', 'recovery_amount'),
    'claim_audit_sampling': ('sample_frame', 'selection_method', 'risk_score', 'auditor_assignment', 'finding'),
    'cryptographic_adjudication_proofs': ('claim_intake_hash', 'line_edit_hash', 'pricing_hash', 'denial_hash', 'appeal_hash'),
    'privacy_minimum_necessary_views': ('role', 'diagnosis_redaction', 'attachment_redaction', 'financial_redaction', 'purpose'),
    'correction_erroneous_denials': ('denial_quality_signal', 'cohort', 'systemic_issue', 'corrective_action', 'notice_generation'),
    'seeded_adjudication_scenario_library': ('clean_claim', 'missing_eligibility', 'authorization_mismatch', 'appeal_overturn', 'stale_dependency'),
    'financial_reconciliation_contract': ('payable_event', 'adjustment_event', 'recovery_event', 'member_responsibility', 'idempotency_key'),
    'regulatory_reporting_extracts': ('measure_definition', 'numerator', 'denominator', 'exclusion', 'submission_status'),
    'full_claims_release_simulation': ('intake', 'validation', 'pricing', 'appeal', 'reporting'),
    'package_boundary_proofs': ('external_input', 'dependency_contract', 'projection_mode', 'event_mode', 'foreign_table_check'),
    'composition_dsl_unified_agent_exposure': ('models', 'routes', 'services', 'event_contracts', 'assistant_skills'),
}
CAPABILITY_TABLES = {
    'claim_intake_canonicalization': OWNED_TABLES[0],
    'claim_lifecycle_state_machine': OWNED_TABLES[0],
    'claim_line_granularity': OWNED_TABLES[1],
    'member_eligibility_projection_boundary': OWNED_TABLES[0],
    'provider_network_credential_projection_boundary': OWNED_TABLES[0],
    'benefit_rule_versioning': OWNED_TABLES[3],
    'medical_necessity_review': OWNED_TABLES[2],
    'prior_authorization_matching': OWNED_TABLES[0],
    'coding_validation_engine': OWNED_TABLES[2],
    'coordination_of_benefits': OWNED_TABLES[0],
    'deductible_coinsurance_copay_application': OWNED_TABLES[1],
    'contract_pricing_allowed_amount': OWNED_TABLES[1],
    'claim_pend_reason_taxonomy': OWNED_TABLES[0],
    'denial_reason_governance': OWNED_TABLES[4],
    'appeal_lifecycle': OWNED_TABLES[5],
    'duplicate_claim_detection': OWNED_TABLES[0],
    'payment_integrity_case_management': OWNED_TABLES[6],
    'fraud_waste_abuse_signal_review': OWNED_TABLES[6],
    'attachment_medical_record_handling': OWNED_TABLES[12],
    'corrected_replacement_claim_lineage': OWNED_TABLES[0],
    'overpayment_recovery_workflow': OWNED_TABLES[6],
    'claim_adjustment_reversal': OWNED_TABLES[0],
    'benefit_limit_tracking': OWNED_TABLES[3],
    'bundling_unbundling_detection': OWNED_TABLES[2],
    'inpatient_episode_claim_logic': OWNED_TABLES[1],
    'professional_claim_specialty_logic': OWNED_TABLES[1],
    'member_provider_notice_generation': OWNED_TABLES[4],
    'sla_timeliness_management': OWNED_TABLES[0],
    'adjudication_explainability_packet': OWNED_TABLES[0],
    'rule_conflict_impact_simulation': OWNED_TABLES[3],
    'claims_operations_workbench': OWNED_TABLES[10],
    'agent_assisted_claim_review': OWNED_TABLES[12],
    'governed_agent_crud_commands': OWNED_TABLES[12],
    'model_governance_claim_intelligence': OWNED_TABLES[11],
    'continuous_control_assertions': OWNED_TABLES[10],
    'dead_letter_retry_queue': OWNED_TABLES[15],
    'cross_pbc_dependency_freshness': OWNED_TABLES[0],
    'low_value_care_policy_analytics': OWNED_TABLES[6],
    'provider_dispute_workflow': OWNED_TABLES[5],
    'subrogation_third_party_liability': OWNED_TABLES[6],
    'claim_audit_sampling': OWNED_TABLES[10],
    'cryptographic_adjudication_proofs': OWNED_TABLES[10],
    'privacy_minimum_necessary_views': OWNED_TABLES[10],
    'correction_erroneous_denials': OWNED_TABLES[4],
    'seeded_adjudication_scenario_library': OWNED_TABLES[10],
    'financial_reconciliation_contract': OWNED_TABLES[13],
    'regulatory_reporting_extracts': OWNED_TABLES[10],
    'full_claims_release_simulation': OWNED_TABLES[10],
    'package_boundary_proofs': OWNED_TABLES[10],
    'composition_dsl_unified_agent_exposure': OWNED_TABLES[11],
}
CAPABILITY_EVENTS = {
    'claim_intake_canonicalization': 'ClaimsIntakeCanonicalized',
    'claim_lifecycle_state_machine': 'ClaimsLifecycleTransitioned',
    'claim_line_granularity': 'ClaimLineAdjudicated',
    'member_eligibility_projection_boundary': 'EligibilityProjectionValidated',
    'provider_network_credential_projection_boundary': 'ProviderProjectionValidated',
    'benefit_rule_versioning': 'BenefitRuleVersionSelected',
    'medical_necessity_review': 'MedicalNecessityReviewed',
    'prior_authorization_matching': 'PriorAuthorizationMatched',
    'coding_validation_engine': 'CodingValidationCompleted',
    'coordination_of_benefits': 'CoordinationOfBenefitsAdjudicated',
    'deductible_coinsurance_copay_application': 'CostShareApplied',
    'contract_pricing_allowed_amount': 'ContractPricingApplied',
    'claim_pend_reason_taxonomy': 'ClaimPended',
    'denial_reason_governance': 'DenialGoverned',
    'appeal_lifecycle': 'AppealManaged',
    'duplicate_claim_detection': 'DuplicateClaimScored',
    'payment_integrity_case_management': 'PaymentIntegrityCaseManaged',
    'fraud_waste_abuse_signal_review': 'FwaSignalReviewed',
    'attachment_medical_record_handling': 'AttachmentGoverned',
    'corrected_replacement_claim_lineage': 'CorrectedClaimProcessed',
    'overpayment_recovery_workflow': 'OverpaymentRecoveryManaged',
    'claim_adjustment_reversal': 'ClaimAdjustmentAuthorized',
    'benefit_limit_tracking': 'BenefitLimitEvaluated',
    'bundling_unbundling_detection': 'BundlingReviewCreated',
    'inpatient_episode_claim_logic': 'InpatientEpisodeAdjudicated',
    'professional_claim_specialty_logic': 'ProfessionalSpecialtyAdjudicated',
    'member_provider_notice_generation': 'ClaimsNoticeGenerated',
    'sla_timeliness_management': 'ClaimsSlaManaged',
    'adjudication_explainability_packet': 'AdjudicationPacketGenerated',
    'rule_conflict_impact_simulation': 'RuleImpactSimulated',
    'claims_operations_workbench': 'ClaimsOperationsWorkbenchSurfaced',
    'agent_assisted_claim_review': 'ClaimsAgentReviewPlanned',
    'governed_agent_crud_commands': 'ClaimsAgentCrudPreviewed',
    'model_governance_claim_intelligence': 'ClaimsModelGoverned',
    'continuous_control_assertions': 'ClaimsControlAsserted',
    'dead_letter_retry_queue': 'ClaimsDeadLetterTriaged',
    'cross_pbc_dependency_freshness': 'ClaimsDependencyFreshnessChecked',
    'low_value_care_policy_analytics': 'LowValueCareAnalyticsGenerated',
    'provider_dispute_workflow': 'ProviderDisputeManaged',
    'subrogation_third_party_liability': 'SubrogationManaged',
    'claim_audit_sampling': 'ClaimAuditSampleCreated',
    'cryptographic_adjudication_proofs': 'AdjudicationProofGenerated',
    'privacy_minimum_necessary_views': 'ClaimsPrivacyViewRendered',
    'correction_erroneous_denials': 'ErroneousDenialCorrected',
    'seeded_adjudication_scenario_library': 'ClaimsScenarioLibraryLoaded',
    'financial_reconciliation_contract': 'ClaimsFinancialEventEmitted',
    'regulatory_reporting_extracts': 'ClaimsRegulatoryReportGenerated',
    'full_claims_release_simulation': 'ClaimsReleaseSimulationRun',
    'package_boundary_proofs': 'ClaimsBoundaryProofGenerated',
    'composition_dsl_unified_agent_exposure': 'ClaimsDslAgentExposed',
}


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def _as_tuple(value: object) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list | set):
        return tuple(value)
    return (value,)


def _iso(value: object | None) -> str:
    if value is None:
        return date(2026, 5, 30).isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)[:10]


def evaluate_claims_control(capability: str, payload: Mapping[str, object]) -> dict:
    if capability not in CLAIMS_CONTROL_CAPABILITIES:
        raise ValueError(f"unknown claims adjudication capability: {capability}")
    data = dict(payload or {})
    required = REQUIRED_FIELDS[capability]
    missing = tuple(field for field in required if data.get(field) in (None, "", (), []))
    table_refs = tuple(str(ref) for ref in _as_tuple(data.get("table_refs")))
    foreign_refs = tuple(ref for ref in table_refs if ref not in OWNED_TABLES and not ref.startswith(PBC_KEY + "_"))
    human_decision = capability in {
        "medical_necessity_review",
        "denial_reason_governance",
        "appeal_lifecycle",
        "fraud_waste_abuse_signal_review",
        "claim_adjustment_reversal",
        "provider_dispute_workflow",
    }
    agent_planned = capability.startswith("agent_") or "agent" in capability
    privacy_sensitive = capability in {"privacy_minimum_necessary_views", "attachment_medical_record_handling"}
    confidence = float(data.get("confidence", 1 if not missing else 0.5))
    review_required = bool(missing or foreign_refs or human_decision or agent_planned or privacy_sensitive or confidence < float(data.get("confidence_threshold", 0.8)))
    return {
        "ok": not missing and not foreign_refs and not data.get("blocked"),
        "pbc": PBC_KEY,
        "capability": capability,
        "owned_table": CAPABILITY_TABLES[capability],
        "required_fields": required,
        "missing_fields": missing,
        "control_id": _digest((capability, data))[:16],
        "ui_surface": f"{PBC_KEY}.ui.claims_control.{capability}",
        "service_surface": f"{PBC_KEY}.service.claims_control.{capability}",
        "api_surface": f"{PBC_KEY}.api.claims_control.{capability}",
        "emits": CAPABILITY_EVENTS[capability],
        "event_contract": EVENT_CONTRACT,
        "idempotency_key": data.get("idempotency_key") or _digest((capability, data.get("claim_id"), data.get("line_id")))[:24],
        "effective_at": _iso(data.get("effective_at")),
        "requires_human_confirmation": review_required,
        "clinical_or_financial_review_required": human_decision,
        "privacy_review_required": privacy_sensitive,
        "agent_plan_only": agent_planned,
        "foreign_references": foreign_refs,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def canonicalize_claim_intake(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('claim_intake_canonicalization', payload)

def transition_claim_lifecycle_state(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('claim_lifecycle_state_machine', payload)

def adjudicate_claim_line_granularity(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('claim_line_granularity', payload)

def validate_member_eligibility_projection(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('member_eligibility_projection_boundary', payload)

def validate_provider_projection_boundary(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('provider_network_credential_projection_boundary', payload)

def select_benefit_rule_version(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('benefit_rule_versioning', payload)

def manage_medical_necessity_review(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('medical_necessity_review', payload)

def match_prior_authorization(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('prior_authorization_matching', payload)

def run_coding_validation_engine(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('coding_validation_engine', payload)

def adjudicate_coordination_of_benefits(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('coordination_of_benefits', payload)

def apply_cost_share_calculation(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('deductible_coinsurance_copay_application', payload)

def price_contract_allowed_amount(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('contract_pricing_allowed_amount', payload)

def route_claim_pend_reason(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('claim_pend_reason_taxonomy', payload)

def govern_denial_reason(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('denial_reason_governance', payload)

def manage_appeal_lifecycle(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('appeal_lifecycle', payload)

def score_duplicate_claim(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('duplicate_claim_detection', payload)

def manage_payment_integrity_case(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('payment_integrity_case_management', payload)

def review_fwa_signal(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('fraud_waste_abuse_signal_review', payload)

def govern_attachment_medical_record(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('attachment_medical_record_handling', payload)

def process_corrected_claim_lineage(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('corrected_replacement_claim_lineage', payload)

def manage_overpayment_recovery(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('overpayment_recovery_workflow', payload)

def authorize_claim_adjustment_reversal(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('claim_adjustment_reversal', payload)

def evaluate_benefit_limit_tracking(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('benefit_limit_tracking', payload)

def detect_bundling_unbundling(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('bundling_unbundling_detection', payload)

def adjudicate_inpatient_episode(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('inpatient_episode_claim_logic', payload)

def adjudicate_professional_specialty_logic(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('professional_claim_specialty_logic', payload)

def generate_member_provider_notice(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('member_provider_notice_generation', payload)

def manage_claim_sla_timeliness(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('sla_timeliness_management', payload)

def generate_adjudication_explainability_packet(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('adjudication_explainability_packet', payload)

def simulate_rule_conflict_impact(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('rule_conflict_impact_simulation', payload)

def surface_claims_operations_workbench(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('claims_operations_workbench', payload)

def plan_agent_assisted_claim_review(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('agent_assisted_claim_review', payload)

def preview_governed_agent_crud_command(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('governed_agent_crud_commands', payload)

def govern_claim_intelligence_model(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('model_governance_claim_intelligence', payload)

def run_claims_control_assertions(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('continuous_control_assertions', payload)

def triage_claims_dead_letter_retry(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('dead_letter_retry_queue', payload)

def check_cross_pbc_dependency_freshness(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('cross_pbc_dependency_freshness', payload)

def generate_low_value_care_analytics(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('low_value_care_policy_analytics', payload)

def manage_provider_dispute(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('provider_dispute_workflow', payload)

def manage_subrogation_tpl(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('subrogation_third_party_liability', payload)

def create_claim_audit_sample(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('claim_audit_sampling', payload)

def generate_adjudication_proof_chain(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('cryptographic_adjudication_proofs', payload)

def render_minimum_necessary_view(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('privacy_minimum_necessary_views', payload)

def correct_erroneous_denial_cohort(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('correction_erroneous_denials', payload)

def load_seeded_adjudication_scenarios(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('seeded_adjudication_scenario_library', payload)

def emit_financial_reconciliation_contract(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('financial_reconciliation_contract', payload)

def generate_regulatory_reporting_extract(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('regulatory_reporting_extracts', payload)

def run_full_claims_release_simulation(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('full_claims_release_simulation', payload)

def prove_claims_package_boundaries(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('package_boundary_proofs', payload)

def expose_claims_composition_dsl_agent(payload: Mapping[str, object]) -> dict:
    return evaluate_claims_control('composition_dsl_unified_agent_exposure', payload)

CLAIMS_CONTROL_FUNCTIONS: dict[str, Callable[[Mapping[str, object]], dict]] = {
    'claim_intake_canonicalization': canonicalize_claim_intake,
    'claim_lifecycle_state_machine': transition_claim_lifecycle_state,
    'claim_line_granularity': adjudicate_claim_line_granularity,
    'member_eligibility_projection_boundary': validate_member_eligibility_projection,
    'provider_network_credential_projection_boundary': validate_provider_projection_boundary,
    'benefit_rule_versioning': select_benefit_rule_version,
    'medical_necessity_review': manage_medical_necessity_review,
    'prior_authorization_matching': match_prior_authorization,
    'coding_validation_engine': run_coding_validation_engine,
    'coordination_of_benefits': adjudicate_coordination_of_benefits,
    'deductible_coinsurance_copay_application': apply_cost_share_calculation,
    'contract_pricing_allowed_amount': price_contract_allowed_amount,
    'claim_pend_reason_taxonomy': route_claim_pend_reason,
    'denial_reason_governance': govern_denial_reason,
    'appeal_lifecycle': manage_appeal_lifecycle,
    'duplicate_claim_detection': score_duplicate_claim,
    'payment_integrity_case_management': manage_payment_integrity_case,
    'fraud_waste_abuse_signal_review': review_fwa_signal,
    'attachment_medical_record_handling': govern_attachment_medical_record,
    'corrected_replacement_claim_lineage': process_corrected_claim_lineage,
    'overpayment_recovery_workflow': manage_overpayment_recovery,
    'claim_adjustment_reversal': authorize_claim_adjustment_reversal,
    'benefit_limit_tracking': evaluate_benefit_limit_tracking,
    'bundling_unbundling_detection': detect_bundling_unbundling,
    'inpatient_episode_claim_logic': adjudicate_inpatient_episode,
    'professional_claim_specialty_logic': adjudicate_professional_specialty_logic,
    'member_provider_notice_generation': generate_member_provider_notice,
    'sla_timeliness_management': manage_claim_sla_timeliness,
    'adjudication_explainability_packet': generate_adjudication_explainability_packet,
    'rule_conflict_impact_simulation': simulate_rule_conflict_impact,
    'claims_operations_workbench': surface_claims_operations_workbench,
    'agent_assisted_claim_review': plan_agent_assisted_claim_review,
    'governed_agent_crud_commands': preview_governed_agent_crud_command,
    'model_governance_claim_intelligence': govern_claim_intelligence_model,
    'continuous_control_assertions': run_claims_control_assertions,
    'dead_letter_retry_queue': triage_claims_dead_letter_retry,
    'cross_pbc_dependency_freshness': check_cross_pbc_dependency_freshness,
    'low_value_care_policy_analytics': generate_low_value_care_analytics,
    'provider_dispute_workflow': manage_provider_dispute,
    'subrogation_third_party_liability': manage_subrogation_tpl,
    'claim_audit_sampling': create_claim_audit_sample,
    'cryptographic_adjudication_proofs': generate_adjudication_proof_chain,
    'privacy_minimum_necessary_views': render_minimum_necessary_view,
    'correction_erroneous_denials': correct_erroneous_denial_cohort,
    'seeded_adjudication_scenario_library': load_seeded_adjudication_scenarios,
    'financial_reconciliation_contract': emit_financial_reconciliation_contract,
    'regulatory_reporting_extracts': generate_regulatory_reporting_extract,
    'full_claims_release_simulation': run_full_claims_release_simulation,
    'package_boundary_proofs': prove_claims_package_boundaries,
    'composition_dsl_unified_agent_exposure': expose_claims_composition_dsl_agent,
}


def improve1_claims_control_contract() -> dict:
    return {
        "ok": len(CLAIMS_CONTROL_CAPABILITIES) == 50 and set(CLAIMS_CONTROL_FUNCTIONS) == set(CLAIMS_CONTROL_CAPABILITIES),
        "pbc": PBC_KEY,
        "capability_count": len(CLAIMS_CONTROL_CAPABILITIES),
        "capabilities": CLAIMS_CONTROL_CAPABILITIES,
        "owned_tables": OWNED_TABLES,
        "ui_surfaces": tuple(f"{PBC_KEY}.ui.claims_control.{capability}" for capability in CLAIMS_CONTROL_CAPABILITIES),
        "service_surfaces": tuple(f"{PBC_KEY}.service.claims_control.{capability}" for capability in CLAIMS_CONTROL_CAPABILITIES),
        "api_surfaces": tuple(f"{PBC_KEY}.api.claims_control.{capability}" for capability in CLAIMS_CONTROL_CAPABILITIES),
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }
