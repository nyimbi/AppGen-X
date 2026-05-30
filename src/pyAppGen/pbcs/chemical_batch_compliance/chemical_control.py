"""Executable chemical batch compliance controls for improve1 execution."""
from __future__ import annotations

from datetime import date, datetime
import hashlib
import json
from typing import Callable, Mapping

PBC_KEY = "chemical_batch_compliance"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = ('chemical_batch_compliance_chemical_formula', 'chemical_batch_compliance_batch_record', 'chemical_batch_compliance_sds_document', 'chemical_batch_compliance_hazardous_material', 'chemical_batch_compliance_regulatory_submission', 'chemical_batch_compliance_quality_test', 'chemical_batch_compliance_compliance_hold', 'chemical_batch_compliance_chemical_batch_compliance_policy_rule', 'chemical_batch_compliance_chemical_batch_compliance_runtime_parameter', 'chemical_batch_compliance_chemical_batch_compliance_schema_extension', 'chemical_batch_compliance_chemical_batch_compliance_control_assertion', 'chemical_batch_compliance_chemical_batch_compliance_governed_model', 'chemical_batch_compliance_appgen_outbox_event', 'chemical_batch_compliance_appgen_inbox_event', 'chemical_batch_compliance_appgen_dead_letter_event')
CHEMICAL_CONTROL_CAPABILITIES = (
    'master_recipe_versioning_effectivity_windows',
    'formula_composition_potency_tolerance_control',
    'raw_material_substitution_source_approval',
    'stepwise_electronic_batch_execution_records',
    'equipment_readiness_line_clearance_enforcement',
    'weigh_dispense_reconciliation',
    'process_parameter_action_alarm_bands',
    'risk_based_in_process_sampling_plans',
    'sample_chain_of_custody_split_management',
    'qc_specification_profiles_release_limits',
    'oos_oot_investigation_workflow',
    'deviation_incident_capa_linkage',
    'rework_reblend_yield_loss_governance',
    'end_to_end_lot_genealogy',
    'retain_samples_stability_program_tracking',
    'sds_section_obligation_extraction',
    'sds_revision_impact_assessment',
    'hazardous_material_storage_compatibility',
    'ghs_label_inventory_control',
    'exposure_ppe_permit_to_work_gating',
    'environmental_permit_discharge_emission_limits',
    'waste_stream_classification_disposal_evidence',
    'regulatory_submission_dossier_assembly',
    'jurisdiction_threshold_reporting_engine',
    'restricted_substance_impurity_surveillance',
    'incoming_coa_approved_source_control',
    'campaign_changeover_contamination_prevention',
    'cleaning_validation_residue_limit_evidence',
    'instrument_calibration_metrology_status',
    'review_by_exception_batch_records',
    'quarantine_hold_release_disposition_controls',
    'shelf_life_retest_expiry_lockouts',
    'external_lab_result_boundary_reconciliation',
    'event_boundary_material_batch_release_changes',
    'api_boundary_hardening_recipe_batch_sds_submission',
    'master_recipe_authoring_workbench',
    'batch_execution_workbench',
    'qc_sample_management_workbench',
    'ehs_hazardous_material_workbench',
    'compliance_release_audit_workbench',
    'agent_sds_permit_interpretation',
    'agent_deviation_triage_evidence_assembly',
    'governed_agent_action_guardrails',
    'counterfactual_parameter_excursion_hold_simulation',
    'predictive_anomaly_process_compliance_risk',
    'continuous_control_testing_release_readiness',
    'release_evidence_vault_sealed_audit_packs',
    'multi_tenant_policy_isolation_plant_jurisdiction',
    'recall_readiness_trace_drills',
    'domain_complete_release_gate',
)
REQUIRED_FIELDS = {
    'master_recipe_versioning_effectivity_windows': ('revision_state', 'ingredient_list', 'effectivity_window', 'approval_lanes', 'sds_or_permit_refs'),
    'formula_composition_potency_tolerance_control': ('target_concentration', 'min_max_window', 'assay_adjustment', 'density_compensation', 'ctq_attributes'),
    'raw_material_substitution_source_approval': ('planned_material', 'substitute_material', 'supplier_qualification', 'equivalence_rationale', 'sds_review'),
    'stepwise_electronic_batch_execution_records': ('phase_sequence', 'operator_action', 'checkpoint', 'supervisor_signoff', 'completion_condition'),
    'equipment_readiness_line_clearance_enforcement': ('equipment_id', 'line_clearance', 'cleaning_release', 'calibration_state', 'maintenance_lockout'),
    'weigh_dispense_reconciliation': ('planned_quantity', 'actual_quantity', 'container_id', 'balance_id', 'verifier'),
    'process_parameter_action_alarm_bands': ('setpoint', 'advisory_band', 'alarm_band', 'action_limit', 'deviation_trigger'),
    'risk_based_in_process_sampling_plans': ('sampling_trigger', 'required_tests', 'progression_minimums', 'release_relevance', 'risk_profile'),
    'sample_chain_of_custody_split_management': ('sample_id', 'storage_condition', 'custody_log', 'split_sample_link', 'disposal_record'),
    'qc_specification_profiles_release_limits': ('spec_profile', 'method_version', 'units', 'rounding_rule', 'disposition_driver'),
    'oos_oot_investigation_workflow': ('lab_assessment', 'manufacturing_assessment', 'retest_authority', 'impact_scope', 'final_disposition'),
    'deviation_incident_capa_linkage': ('deviation_classification', 'containment', 'impact_assessment', 'capa_tasks', 'effectiveness_check'),
    'rework_reblend_yield_loss_governance': ('rework_route', 'reblend_formula', 'additional_tests', 'yield_loss_reason', 'approval_threshold'),
    'end_to_end_lot_genealogy': ('incoming_lots', 'dispenses', 'intermediate_pools', 'retained_samples', 'waste_outputs'),
    'retain_samples_stability_program_tracking': ('retain_sample', 'storage_location', 'chamber_assignment', 'pull_schedule', 'shelf_life_logic'),
    'sds_section_obligation_extraction': ('sds_section', 'hazard_classification', 'ppe_obligation', 'storage_condition', 'source_citation'),
    'sds_revision_impact_assessment': ('old_version', 'new_version', 'section_diff', 'affected_formulas', 'required_actions'),
    'hazardous_material_storage_compatibility': ('compatibility_matrix', 'segregation_zone', 'quantity_limit', 'temperature_requirement', 'containment'),
    'ghs_label_inventory_control': ('signal_word', 'hazard_statements', 'pictograms', 'local_inventory_id', 'quantity_on_hand'),
    'exposure_ppe_permit_to_work_gating': ('required_ppe', 'engineering_controls', 'permit_type', 'exposure_monitoring', 'authorization'),
    'environmental_permit_discharge_emission_limits': ('permit_id', 'voc_cap', 'wastewater_limit', 'emission_calculation', 'remaining_headroom'),
    'waste_stream_classification_disposal_evidence': ('waste_code', 'hazard_class', 'accumulation_start', 'storage_area', 'disposal_certificate'),
    'regulatory_submission_dossier_assembly': ('dossier_template', 'composition_source', 'hazard_classification', 'stability_data', 'authority_commitment'),
    'jurisdiction_threshold_reporting_engine': ('jurisdiction', 'material_class', 'concentration_rule', 'quantity_rule', 'effective_date'),
    'restricted_substance_impurity_surveillance': ('restricted_list', 'impurity_limit', 'precursor_rule', 'test_result', 'theoretical_risk'),
    'incoming_coa_approved_source_control': ('coa_values', 'supplier_identity', 'internal_spec', 'approved_source', 'identity_test'),
    'campaign_changeover_contamination_prevention': ('campaign_family', 'forbidden_sequence', 'purge_steps', 'dedicated_equipment', 'heightened_sampling'),
    'cleaning_validation_residue_limit_evidence': ('cleaning_method', 'maco_limit', 'swab_plan', 'recovery_factor', 'equipment_release_authority'),
    'instrument_calibration_metrology_status': ('instrument_id', 'critical_use', 'calibration_due', 'qualification_state', 'result_context'),
    'review_by_exception_batch_records': ('parameter_excursions', 'missing_signatures', 'manual_overrides', 'abnormal_yield', 'unplanned_branching'),
    'quarantine_hold_release_disposition_controls': ('lot_id', 'target_state', 'decision_reason', 'authority_role', 'evidence_link'),
    'shelf_life_retest_expiry_lockouts': ('material_class', 'storage_condition', 'stability_outcome', 'expiry_date', 'override_justification'),
    'external_lab_result_boundary_reconciliation': ('external_lab', 'sample_match', 'unit_normalization', 'method_comparison', 'signature_verification'),
    'event_boundary_material_batch_release_changes': ('domain_event', 'producer', 'payload_schema', 'replay_rule', 'compatibility_mapping'),
    'api_boundary_hardening_recipe_batch_sds_submission': ('command_route', 'idempotency_key', 'typed_payload', 'state_transition', 'read_write_separation'),
    'master_recipe_authoring_workbench': ('composition_grid', 'revision_diff', 'approval_lanes', 'linked_hazards', 'authorized_actions'),
    'batch_execution_workbench': ('step_timeline', 'pending_actions', 'dispense_panel', 'parameter_charts', 'disposition_blockers'),
    'qc_sample_management_workbench': ('pending_samples', 'method_versions', 'instrument_state', 'custody_context', 'retest_queue'),
    'ehs_hazardous_material_workbench': ('sds_impact', 'storage_violations', 'permit_utilization', 'waste_timers', 'hazard_inventory'),
    'compliance_release_audit_workbench': ('genealogy_completeness', 'sample_disposition', 'deviation_status', 'permit_compliance', 'sds_status'),
    'agent_sds_permit_interpretation': ('document_text', 'source_citation', 'hazard_mapping', 'permit_obligation', 'confidence'),
    'agent_deviation_triage_evidence_assembly': ('excursion_timeline', 'material_lots', 'related_samples', 'prior_deviations', 'impact_scope'),
    'governed_agent_action_guardrails': ('proposed_action', 'dry_run_diff', 'policy_check', 'role_check', 'human_approval'),
    'counterfactual_parameter_excursion_hold_simulation': ('scenario', 'recipe_rules', 'spec_limits', 'permit_thresholds', 'genealogy_context'),
    'predictive_anomaly_process_compliance_risk': ('parameter_trace', 'sample_results', 'yield_trend', 'waste_generation', 'alert_priority'),
    'continuous_control_testing_release_readiness': ('control_family', 'threshold', 'owner', 'failure_state', 'remediation_record'),
    'release_evidence_vault_sealed_audit_packs': ('recipe_revision', 'batch_record', 'qc_results', 'permit_checks', 'approval_signatures'),
    'multi_tenant_policy_isolation_plant_jurisdiction': ('tenant', 'plant', 'jurisdiction', 'policy_scope', 'access_check'),
    'recall_readiness_trace_drills': ('starting_lot', 'trace_direction', 'connected_batches', 'retained_samples', 'investigation_output'),
    'domain_complete_release_gate': ('recipe_control', 'batch_execution', 'hazard_management', 'qc_controls', 'agent_skills'),
}
CAPABILITY_TABLES = {
    'master_recipe_versioning_effectivity_windows': OWNED_TABLES[0],
    'formula_composition_potency_tolerance_control': OWNED_TABLES[0],
    'raw_material_substitution_source_approval': OWNED_TABLES[0],
    'stepwise_electronic_batch_execution_records': OWNED_TABLES[1],
    'equipment_readiness_line_clearance_enforcement': OWNED_TABLES[1],
    'weigh_dispense_reconciliation': OWNED_TABLES[1],
    'process_parameter_action_alarm_bands': OWNED_TABLES[1],
    'risk_based_in_process_sampling_plans': OWNED_TABLES[5],
    'sample_chain_of_custody_split_management': OWNED_TABLES[5],
    'qc_specification_profiles_release_limits': OWNED_TABLES[5],
    'oos_oot_investigation_workflow': OWNED_TABLES[6],
    'deviation_incident_capa_linkage': OWNED_TABLES[6],
    'rework_reblend_yield_loss_governance': OWNED_TABLES[1],
    'end_to_end_lot_genealogy': OWNED_TABLES[1],
    'retain_samples_stability_program_tracking': OWNED_TABLES[5],
    'sds_section_obligation_extraction': OWNED_TABLES[2],
    'sds_revision_impact_assessment': OWNED_TABLES[2],
    'hazardous_material_storage_compatibility': OWNED_TABLES[3],
    'ghs_label_inventory_control': OWNED_TABLES[3],
    'exposure_ppe_permit_to_work_gating': OWNED_TABLES[3],
    'environmental_permit_discharge_emission_limits': OWNED_TABLES[4],
    'waste_stream_classification_disposal_evidence': OWNED_TABLES[3],
    'regulatory_submission_dossier_assembly': OWNED_TABLES[4],
    'jurisdiction_threshold_reporting_engine': OWNED_TABLES[4],
    'restricted_substance_impurity_surveillance': OWNED_TABLES[5],
    'incoming_coa_approved_source_control': OWNED_TABLES[5],
    'campaign_changeover_contamination_prevention': OWNED_TABLES[1],
    'cleaning_validation_residue_limit_evidence': OWNED_TABLES[1],
    'instrument_calibration_metrology_status': OWNED_TABLES[5],
    'review_by_exception_batch_records': OWNED_TABLES[1],
    'quarantine_hold_release_disposition_controls': OWNED_TABLES[6],
    'shelf_life_retest_expiry_lockouts': OWNED_TABLES[6],
    'external_lab_result_boundary_reconciliation': OWNED_TABLES[5],
    'event_boundary_material_batch_release_changes': OWNED_TABLES[12],
    'api_boundary_hardening_recipe_batch_sds_submission': OWNED_TABLES[10],
    'master_recipe_authoring_workbench': OWNED_TABLES[0],
    'batch_execution_workbench': OWNED_TABLES[1],
    'qc_sample_management_workbench': OWNED_TABLES[5],
    'ehs_hazardous_material_workbench': OWNED_TABLES[3],
    'compliance_release_audit_workbench': OWNED_TABLES[6],
    'agent_sds_permit_interpretation': OWNED_TABLES[2],
    'agent_deviation_triage_evidence_assembly': OWNED_TABLES[11],
    'governed_agent_action_guardrails': OWNED_TABLES[11],
    'counterfactual_parameter_excursion_hold_simulation': OWNED_TABLES[10],
    'predictive_anomaly_process_compliance_risk': OWNED_TABLES[10],
    'continuous_control_testing_release_readiness': OWNED_TABLES[10],
    'release_evidence_vault_sealed_audit_packs': OWNED_TABLES[4],
    'multi_tenant_policy_isolation_plant_jurisdiction': OWNED_TABLES[7],
    'recall_readiness_trace_drills': OWNED_TABLES[1],
    'domain_complete_release_gate': OWNED_TABLES[10],
}
CAPABILITY_EVENTS = {
    'master_recipe_versioning_effectivity_windows': 'ChemicalRecipeRevisionGoverned',
    'formula_composition_potency_tolerance_control': 'ChemicalFormulaToleranceControlled',
    'raw_material_substitution_source_approval': 'ChemicalMaterialSubstitutionApproved',
    'stepwise_electronic_batch_execution_records': 'ChemicalBatchStepRecorded',
    'equipment_readiness_line_clearance_enforcement': 'ChemicalEquipmentReadinessChecked',
    'weigh_dispense_reconciliation': 'ChemicalDispenseReconciled',
    'process_parameter_action_alarm_bands': 'ChemicalProcessParameterCaptured',
    'risk_based_in_process_sampling_plans': 'ChemicalSamplePlanGoverned',
    'sample_chain_of_custody_split_management': 'ChemicalSampleCustodyTracked',
    'qc_specification_profiles_release_limits': 'ChemicalQualitySpecEvaluated',
    'oos_oot_investigation_workflow': 'ChemicalOosInvestigationManaged',
    'deviation_incident_capa_linkage': 'ChemicalDeviationCapaLinked',
    'rework_reblend_yield_loss_governance': 'ChemicalReworkGoverned',
    'end_to_end_lot_genealogy': 'ChemicalLotGenealogyBuilt',
    'retain_samples_stability_program_tracking': 'ChemicalStabilityTracked',
    'sds_section_obligation_extraction': 'ChemicalSdsObligationExtracted',
    'sds_revision_impact_assessment': 'ChemicalSdsImpactAssessed',
    'hazardous_material_storage_compatibility': 'ChemicalStorageCompatibilityChecked',
    'ghs_label_inventory_control': 'ChemicalGhsLabelGenerated',
    'exposure_ppe_permit_to_work_gating': 'ChemicalPermitWorkGated',
    'environmental_permit_discharge_emission_limits': 'ChemicalEnvironmentalPermitChecked',
    'waste_stream_classification_disposal_evidence': 'ChemicalWasteDispositionRecorded',
    'regulatory_submission_dossier_assembly': 'ChemicalRegulatoryDossierAssembled',
    'jurisdiction_threshold_reporting_engine': 'ChemicalThresholdEvaluated',
    'restricted_substance_impurity_surveillance': 'ChemicalImpuritySurveillanceRun',
    'incoming_coa_approved_source_control': 'ChemicalCoaVerified',
    'campaign_changeover_contamination_prevention': 'ChemicalCampaignChangeoverPlanned',
    'cleaning_validation_residue_limit_evidence': 'ChemicalCleaningValidated',
    'instrument_calibration_metrology_status': 'ChemicalInstrumentCalibrationChecked',
    'review_by_exception_batch_records': 'ChemicalBatchReviewPacketBuilt',
    'quarantine_hold_release_disposition_controls': 'ChemicalLotDispositionChanged',
    'shelf_life_retest_expiry_lockouts': 'ChemicalExpiryLockoutChecked',
    'external_lab_result_boundary_reconciliation': 'ChemicalExternalResultReconciled',
    'event_boundary_material_batch_release_changes': 'ChemicalDomainEventCataloged',
    'api_boundary_hardening_recipe_batch_sds_submission': 'ChemicalApiBoundaryHardened',
    'master_recipe_authoring_workbench': 'ChemicalRecipeWorkbenchSurfaced',
    'batch_execution_workbench': 'ChemicalBatchWorkbenchSurfaced',
    'qc_sample_management_workbench': 'ChemicalQcWorkbenchSurfaced',
    'ehs_hazardous_material_workbench': 'ChemicalEhsWorkbenchSurfaced',
    'compliance_release_audit_workbench': 'ChemicalReleaseWorkbenchSurfaced',
    'agent_sds_permit_interpretation': 'ChemicalAgentSdsPermitPlanCreated',
    'agent_deviation_triage_evidence_assembly': 'ChemicalAgentDeviationPacketCreated',
    'governed_agent_action_guardrails': 'ChemicalAgentGuardrailChecked',
    'counterfactual_parameter_excursion_hold_simulation': 'ChemicalCounterfactualSimulated',
    'predictive_anomaly_process_compliance_risk': 'ChemicalProcessAnomalyDetected',
    'continuous_control_testing_release_readiness': 'ChemicalContinuousControlTested',
    'release_evidence_vault_sealed_audit_packs': 'ChemicalReleaseEvidenceSealed',
    'multi_tenant_policy_isolation_plant_jurisdiction': 'ChemicalPolicyIsolationProved',
    'recall_readiness_trace_drills': 'ChemicalRecallTraceDrillRun',
    'domain_complete_release_gate': 'ChemicalDomainReleaseGateEvaluated',
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


def evaluate_chemical_control(capability: str, payload: Mapping[str, object]) -> dict:
    if capability not in CHEMICAL_CONTROL_CAPABILITIES:
        raise ValueError(f"unknown chemical batch compliance capability: {capability}")
    data = dict(payload or {})
    required = REQUIRED_FIELDS[capability]
    missing = tuple(field for field in required if data.get(field) in (None, "", (), []))
    table_refs = tuple(str(ref) for ref in _as_tuple(data.get("table_refs")))
    foreign_refs = tuple(ref for ref in table_refs if ref not in OWNED_TABLES and not ref.startswith(PBC_KEY + "_"))
    high_risk = capability in {
        "raw_material_substitution_source_approval",
        "exposure_ppe_permit_to_work_gating",
        "quarantine_hold_release_disposition_controls",
        "governed_agent_action_guardrails",
        "domain_complete_release_gate",
    }
    agent_planned = capability.startswith("agent_") or "agent" in capability
    confidence = float(data.get("confidence", 1 if not missing else 0.5))
    review_required = bool(missing or foreign_refs or high_risk or agent_planned or confidence < float(data.get("confidence_threshold", 0.8)))
    return {
        "ok": not missing and not foreign_refs and not data.get("blocked"),
        "pbc": PBC_KEY,
        "capability": capability,
        "owned_table": CAPABILITY_TABLES[capability],
        "required_fields": required,
        "missing_fields": missing,
        "control_id": _digest((capability, data))[:16],
        "ui_surface": f"{PBC_KEY}.ui.chemical_control.{capability}",
        "service_surface": f"{PBC_KEY}.service.chemical_control.{capability}",
        "api_surface": f"{PBC_KEY}.api.chemical_control.{capability}",
        "emits": CAPABILITY_EVENTS[capability],
        "event_contract": EVENT_CONTRACT,
        "idempotency_key": data.get("idempotency_key") or _digest((capability, data.get("batch_id"), data.get("lot_id")))[:24],
        "effective_at": _iso(data.get("effective_at")),
        "requires_human_confirmation": review_required,
        "quality_or_ehs_review_required": high_risk,
        "agent_plan_only": agent_planned,
        "foreign_references": foreign_refs,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def govern_master_recipe_revision(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('master_recipe_versioning_effectivity_windows', payload)

def control_formula_composition_tolerance(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('formula_composition_potency_tolerance_control', payload)

def approve_raw_material_substitution(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('raw_material_substitution_source_approval', payload)

def record_stepwise_batch_execution(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('stepwise_electronic_batch_execution_records', payload)

def enforce_equipment_line_clearance(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('equipment_readiness_line_clearance_enforcement', payload)

def reconcile_weigh_dispense(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('weigh_dispense_reconciliation', payload)

def capture_process_parameter_bands(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('process_parameter_action_alarm_bands', payload)

def govern_in_process_sampling_plan(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('risk_based_in_process_sampling_plans', payload)

def track_sample_custody_split(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('sample_chain_of_custody_split_management', payload)

def evaluate_qc_specification_profile(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('qc_specification_profiles_release_limits', payload)

def manage_oos_oot_investigation(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('oos_oot_investigation_workflow', payload)

def link_deviation_incident_capa(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('deviation_incident_capa_linkage', payload)

def govern_rework_reblend_yield_loss(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('rework_reblend_yield_loss_governance', payload)

def build_lot_genealogy_graph(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('end_to_end_lot_genealogy', payload)

def track_retain_stability_program(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('retain_samples_stability_program_tracking', payload)

def extract_sds_section_obligations(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('sds_section_obligation_extraction', payload)

def assess_sds_revision_impact(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('sds_revision_impact_assessment', payload)

def check_hazardous_storage_compatibility(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('hazardous_material_storage_compatibility', payload)

def generate_ghs_label_inventory_control(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('ghs_label_inventory_control', payload)

def gate_exposure_ppe_permit_work(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('exposure_ppe_permit_to_work_gating', payload)

def check_environmental_permit_limits(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('environmental_permit_discharge_emission_limits', payload)

def classify_waste_stream_disposal(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('waste_stream_classification_disposal_evidence', payload)

def assemble_regulatory_dossier(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('regulatory_submission_dossier_assembly', payload)

def evaluate_jurisdiction_thresholds(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('jurisdiction_threshold_reporting_engine', payload)

def surveil_restricted_impurities(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('restricted_substance_impurity_surveillance', payload)

def verify_incoming_coa_source(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('incoming_coa_approved_source_control', payload)

def plan_campaign_changeover_control(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('campaign_changeover_contamination_prevention', payload)

def validate_cleaning_residue_limits(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('cleaning_validation_residue_limit_evidence', payload)

def check_instrument_calibration_status(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('instrument_calibration_metrology_status', payload)

def build_review_by_exception_packet(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('review_by_exception_batch_records', payload)

def govern_lot_disposition_state(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('quarantine_hold_release_disposition_controls', payload)

def enforce_shelf_life_retest_lockout(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('shelf_life_retest_expiry_lockouts', payload)

def reconcile_external_lab_result(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('external_lab_result_boundary_reconciliation', payload)

def catalog_material_batch_release_events(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('event_boundary_material_batch_release_changes', payload)

def harden_chemical_api_boundary(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('api_boundary_hardening_recipe_batch_sds_submission', payload)

def surface_recipe_authoring_workbench(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('master_recipe_authoring_workbench', payload)

def surface_batch_execution_workbench(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('batch_execution_workbench', payload)

def surface_qc_sample_workbench(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('qc_sample_management_workbench', payload)

def surface_ehs_hazard_workbench(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('ehs_hazardous_material_workbench', payload)

def surface_release_audit_workbench(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('compliance_release_audit_workbench', payload)

def plan_agent_sds_permit_interpretation(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('agent_sds_permit_interpretation', payload)

def plan_agent_deviation_triage(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('agent_deviation_triage_evidence_assembly', payload)

def enforce_governed_agent_guardrails(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('governed_agent_action_guardrails', payload)

def simulate_parameter_excursion_hold(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('counterfactual_parameter_excursion_hold_simulation', payload)

def detect_process_compliance_anomaly(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('predictive_anomaly_process_compliance_risk', payload)

def run_continuous_chemical_controls(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('continuous_control_testing_release_readiness', payload)

def seal_release_evidence_pack(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('release_evidence_vault_sealed_audit_packs', payload)

def prove_policy_isolation(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('multi_tenant_policy_isolation_plant_jurisdiction', payload)

def run_recall_trace_drill(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('recall_readiness_trace_drills', payload)

def evaluate_domain_complete_release_gate(payload: Mapping[str, object]) -> dict:
    return evaluate_chemical_control('domain_complete_release_gate', payload)

CHEMICAL_CONTROL_FUNCTIONS: dict[str, Callable[[Mapping[str, object]], dict]] = {
    'master_recipe_versioning_effectivity_windows': govern_master_recipe_revision,
    'formula_composition_potency_tolerance_control': control_formula_composition_tolerance,
    'raw_material_substitution_source_approval': approve_raw_material_substitution,
    'stepwise_electronic_batch_execution_records': record_stepwise_batch_execution,
    'equipment_readiness_line_clearance_enforcement': enforce_equipment_line_clearance,
    'weigh_dispense_reconciliation': reconcile_weigh_dispense,
    'process_parameter_action_alarm_bands': capture_process_parameter_bands,
    'risk_based_in_process_sampling_plans': govern_in_process_sampling_plan,
    'sample_chain_of_custody_split_management': track_sample_custody_split,
    'qc_specification_profiles_release_limits': evaluate_qc_specification_profile,
    'oos_oot_investigation_workflow': manage_oos_oot_investigation,
    'deviation_incident_capa_linkage': link_deviation_incident_capa,
    'rework_reblend_yield_loss_governance': govern_rework_reblend_yield_loss,
    'end_to_end_lot_genealogy': build_lot_genealogy_graph,
    'retain_samples_stability_program_tracking': track_retain_stability_program,
    'sds_section_obligation_extraction': extract_sds_section_obligations,
    'sds_revision_impact_assessment': assess_sds_revision_impact,
    'hazardous_material_storage_compatibility': check_hazardous_storage_compatibility,
    'ghs_label_inventory_control': generate_ghs_label_inventory_control,
    'exposure_ppe_permit_to_work_gating': gate_exposure_ppe_permit_work,
    'environmental_permit_discharge_emission_limits': check_environmental_permit_limits,
    'waste_stream_classification_disposal_evidence': classify_waste_stream_disposal,
    'regulatory_submission_dossier_assembly': assemble_regulatory_dossier,
    'jurisdiction_threshold_reporting_engine': evaluate_jurisdiction_thresholds,
    'restricted_substance_impurity_surveillance': surveil_restricted_impurities,
    'incoming_coa_approved_source_control': verify_incoming_coa_source,
    'campaign_changeover_contamination_prevention': plan_campaign_changeover_control,
    'cleaning_validation_residue_limit_evidence': validate_cleaning_residue_limits,
    'instrument_calibration_metrology_status': check_instrument_calibration_status,
    'review_by_exception_batch_records': build_review_by_exception_packet,
    'quarantine_hold_release_disposition_controls': govern_lot_disposition_state,
    'shelf_life_retest_expiry_lockouts': enforce_shelf_life_retest_lockout,
    'external_lab_result_boundary_reconciliation': reconcile_external_lab_result,
    'event_boundary_material_batch_release_changes': catalog_material_batch_release_events,
    'api_boundary_hardening_recipe_batch_sds_submission': harden_chemical_api_boundary,
    'master_recipe_authoring_workbench': surface_recipe_authoring_workbench,
    'batch_execution_workbench': surface_batch_execution_workbench,
    'qc_sample_management_workbench': surface_qc_sample_workbench,
    'ehs_hazardous_material_workbench': surface_ehs_hazard_workbench,
    'compliance_release_audit_workbench': surface_release_audit_workbench,
    'agent_sds_permit_interpretation': plan_agent_sds_permit_interpretation,
    'agent_deviation_triage_evidence_assembly': plan_agent_deviation_triage,
    'governed_agent_action_guardrails': enforce_governed_agent_guardrails,
    'counterfactual_parameter_excursion_hold_simulation': simulate_parameter_excursion_hold,
    'predictive_anomaly_process_compliance_risk': detect_process_compliance_anomaly,
    'continuous_control_testing_release_readiness': run_continuous_chemical_controls,
    'release_evidence_vault_sealed_audit_packs': seal_release_evidence_pack,
    'multi_tenant_policy_isolation_plant_jurisdiction': prove_policy_isolation,
    'recall_readiness_trace_drills': run_recall_trace_drill,
    'domain_complete_release_gate': evaluate_domain_complete_release_gate,
}


def improve1_chemical_control_contract() -> dict:
    return {
        "ok": len(CHEMICAL_CONTROL_CAPABILITIES) == 50 and set(CHEMICAL_CONTROL_FUNCTIONS) == set(CHEMICAL_CONTROL_CAPABILITIES),
        "pbc": PBC_KEY,
        "capability_count": len(CHEMICAL_CONTROL_CAPABILITIES),
        "capabilities": CHEMICAL_CONTROL_CAPABILITIES,
        "owned_tables": OWNED_TABLES,
        "ui_surfaces": tuple(f"{PBC_KEY}.ui.chemical_control.{capability}" for capability in CHEMICAL_CONTROL_CAPABILITIES),
        "service_surfaces": tuple(f"{PBC_KEY}.service.chemical_control.{capability}" for capability in CHEMICAL_CONTROL_CAPABILITIES),
        "api_surfaces": tuple(f"{PBC_KEY}.api.chemical_control.{capability}" for capability in CHEMICAL_CONTROL_CAPABILITIES),
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }
