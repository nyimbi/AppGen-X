"""Executable improve1 controls for the Food Safety Quality Compliance PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "food_safety_quality_compliance"
EVENT_CONTRACT = "AppGen-X"
FOOD_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
FOOD_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.food_safety_quality_compliance.events"
FOOD_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + (
    "food_safety_quality_compliance_haccp_plan_version",
    "food_safety_quality_compliance_process_hazard_map",
    "food_safety_quality_compliance_ccp_limit_control",
    "food_safety_quality_compliance_monitoring_record",
    "food_safety_quality_compliance_corrective_action",
    "food_safety_quality_compliance_quality_hold_lifecycle",
    "food_safety_quality_compliance_lot_genealogy_projection",
    "food_safety_quality_compliance_allergen_control",
    "food_safety_quality_compliance_sanitation_verification",
    "food_safety_quality_compliance_environmental_monitoring",
    "food_safety_quality_compliance_inspection_program",
    "food_safety_quality_compliance_supplier_audit_program",
    "food_safety_quality_compliance_certificate_specification",
    "food_safety_quality_compliance_nonconformance_taxonomy",
    "food_safety_quality_compliance_capa_linkage",
    "food_safety_quality_compliance_recall_classification",
    "food_safety_quality_compliance_recall_impact_analysis",
    "food_safety_quality_compliance_mock_recall_drill",
    "food_safety_quality_compliance_product_disposition",
    "food_safety_quality_compliance_label_packaging_verification",
    "food_safety_quality_compliance_foreign_material_control",
    "food_safety_quality_compliance_shelf_life_stability",
    "food_safety_quality_compliance_sensory_quality_panel",
    "food_safety_quality_compliance_cold_chain_compliance",
    "food_safety_quality_compliance_regulatory_obligation",
    "food_safety_quality_compliance_audit_evidence_room",
    "food_safety_quality_compliance_training_projection",
    "food_safety_quality_compliance_workbench_queue",
    "food_safety_quality_compliance_agent_review_skill",
    "food_safety_quality_compliance_agent_crud_preview",
    "food_safety_quality_compliance_haccp_change_simulation",
    "food_safety_quality_compliance_predictive_risk_score",
    "food_safety_quality_compliance_quality_trend_analytics",
    "food_safety_quality_compliance_complaint_projection",
    "food_safety_quality_compliance_incident_escalation_matrix",
    "food_safety_quality_compliance_market_localization",
    "food_safety_quality_compliance_continuous_control_assertion",
    "food_safety_quality_compliance_dead_letter_retry",
    "food_safety_quality_compliance_crypto_evidence_chain",
    "food_safety_quality_compliance_permission_model",
    "food_safety_quality_compliance_supplier_capa_workflow",
    "food_safety_quality_compliance_product_release_gate",
    "food_safety_quality_compliance_regulatory_reporting_trigger",
    "food_safety_quality_compliance_disposal_evidence",
    "food_safety_quality_compliance_seed_scenario_library",
    "food_safety_quality_compliance_claim_certification",
    "food_safety_quality_compliance_customer_spec_projection",
    "food_safety_quality_compliance_release_simulation",
    "food_safety_quality_compliance_overlap_guardrail",
    "food_safety_quality_compliance_dsl_agent_exposure",

)))
FOOD_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "InventoryLotProjected", "ProductionLotProjected", "ShipmentScopeProjected",
    "CustomerProjectionUpdated", "SupplierStatusChanged", "TrainingCompetencyProjected",
    "CustomerComplaintProjected", "ColdChainTelemetryProjected", "CustomerSpecProjected",
    "RegulatoryFilingProjected", "FoodSafetyQualityComplianceHoldOpened",
    "FoodSafetyQualityComplianceRecallImpactProjected",
)))
FOOD_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in FOOD_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in FOOD_CONTROL_CAPABILITIES}
_SPEC_ROWS: tuple[tuple[int, str, str, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = [(1, 'HACCP Plan Version Governance', 'haccp_plan_version_governance', ('food_safety_quality_compliance_haccp_plan_version',), ('plan_code', 'product_scope', 'process_flow', 'hazard_analysis', 'approved_controls', 'effective_window', 'reviewer', 'supersession_reason', 'historical_reference_pinned'), 'HaccpPlanVersionGovernance', 'POST /food-safety-quality-compliance/improve1/haccp_plan_version_governance', ()), (2, 'Process Flow and Hazard Mapping', 'process_flow_and_hazard_mapping', ('food_safety_quality_compliance_process_hazard_map',), ('process_step', 'hazard_type', 'likelihood', 'severity', 'preventive_control', 'prerequisite_program', 'linked_ccp', 'mapping_complete', 'definition_allowed'), 'ProcessFlowAndHazardMapping', 'POST /food-safety-quality-compliance/improve1/process_flow_and_hazard_mapping', ()), (3, 'Critical Control Point Limits', 'critical_control_point_limits', ('food_safety_quality_compliance_ccp_limit_control',), ('ccp_id', 'limit_type', 'limit_min', 'limit_max', 'unit', 'monitoring_method', 'frequency_minutes', 'responsible_role', 'verification_requirement'), 'CriticalControlPointLimits', 'POST /food-safety-quality-compliance/improve1/critical_control_point_limits', ()), (4, 'Monitoring Record Intake', 'monitoring_record_intake', ('food_safety_quality_compliance_monitoring_record',), ('ccp_id', 'value', 'unit', 'timestamp', 'device_id', 'operator_id', 'source_evidence', 'pass_fail', 'review_state'), 'MonitoringRecordIntake', 'POST /food-safety-quality-compliance/improve1/monitoring_record_intake', ()), (5, 'Corrective Action for CCP Failure', 'corrective_action_for_ccp_failure', ('food_safety_quality_compliance_corrective_action',), ('affected_product', 'immediate_action', 'disposition', 'root_cause', 'verifier', 'restart_criteria', 'evidence_complete', 'release_blocked', 'quantity_scope'), 'CorrectiveActionForCcpFailure', 'POST /food-safety-quality-compliance/improve1/corrective_action_for_ccp_failure', ()), (6, 'Quality Hold Lifecycle', 'quality_hold_lifecycle', ('food_safety_quality_compliance_quality_hold_lifecycle',), ('hold_reason', 'affected_lot_projection', 'quantity', 'location', 'release_criteria', 'disposition', 'approver', 'release_event', 'quantity_reconciled'), 'QualityHoldLifecycle', 'POST /food-safety-quality-compliance/improve1/quality_hold_lifecycle', ()), (7, 'Lot Genealogy Boundary', 'lot_genealogy_boundary', ('food_safety_quality_compliance_lot_genealogy_projection',), ('source_lot', 'finished_lot', 'transformation_step', 'quantity', 'location', 'projection_freshness', 'declared_event_source', 'direct_inventory_read_blocked', 'trace_complete'), 'LotGenealogyBoundary', 'POST /food-safety-quality-compliance/improve1/lot_genealogy_boundary', ('InventoryLotProjected', 'ProductionLotProjected')), (8, 'Allergen Control Program', 'allergen_control_program', ('food_safety_quality_compliance_allergen_control',), ('allergen_profile', 'line_clearance_check', 'changeover_validation', 'label_verification', 'rework_restriction', 'cross_contact_risk', 'nonconformance_opened', 'release_allowed', 'evidence_citations'), 'AllergenControlProgram', 'POST /food-safety-quality-compliance/improve1/allergen_control_program', ()), (9, 'Sanitation Verification', 'sanitation_verification', ('food_safety_quality_compliance_sanitation_verification',), ('sanitation_schedule', 'method', 'chemical', 'concentration', 'swab_result', 'visual_check', 'pre_op_approval', 'failed_cleaning_action', 'release_allowed'), 'SanitationVerification', 'POST /food-safety-quality-compliance/improve1/sanitation_verification', ()), (10, 'Environmental Monitoring', 'environmental_monitoring', ('food_safety_quality_compliance_environmental_monitoring',), ('zone', 'site', 'sample_type', 'organism', 'result', 'trend', 'corrective_action', 'product_impact_assessment', 'escalation_level'), 'EnvironmentalMonitoring', 'POST /food-safety-quality-compliance/improve1/environmental_monitoring', ()), (11, 'Inspection Program', 'inspection_program', ('food_safety_quality_compliance_inspection_program',), ('checklist', 'area', 'inspector', 'severity', 'finding', 'score', 'action_required', 'repeat_finding_marker', 'due_corrective_action'), 'InspectionProgram', 'POST /food-safety-quality-compliance/improve1/inspection_program', ()), (12, 'Supplier Audit Program', 'supplier_audit_program', ('food_safety_quality_compliance_supplier_audit_program',), ('supplier_projection', 'commodity', 'audit_type', 'finding', 'risk_rating', 'corrective_action', 'approval_status', 'expiry', 'supplier_use_blocked'), 'SupplierAuditProgram', 'POST /food-safety-quality-compliance/improve1/supplier_audit_program', ('SupplierStatusChanged',)), (13, 'Certificate and Specification Compliance', 'certificate_and_specification_compliance', ('food_safety_quality_compliance_certificate_specification',), ('certificate_evidence', 'specification_version', 'tested_attributes', 'pass_fail', 'deviation', 'waiver_approval', 'lot_hold_required', 'micro_limit_status', 'chemical_limit_status'), 'CertificateAndSpecificationCompliance', 'POST /food-safety-quality-compliance/improve1/certificate_and_specification_compliance', ()), (14, 'Nonconformance Taxonomy', 'nonconformance_taxonomy', ('food_safety_quality_compliance_nonconformance_taxonomy',), ('category', 'severity', 'product_impact', 'process_step', 'root_cause', 'containment', 'corrective_action', 'recurrence_flag', 'route_queue'), 'NonconformanceTaxonomy', 'POST /food-safety-quality-compliance/improve1/nonconformance_taxonomy', ()), (15, 'Root Cause and CAPA Linkage', 'root_cause_and_capa_linkage', ('food_safety_quality_compliance_capa_linkage',), ('root_cause_method', 'confirmed_cause', 'corrective_action', 'preventive_action', 'owner', 'due_date', 'effectiveness_check', 'closure_evidence', 'closure_allowed'), 'RootCauseAndCapaLinkage', 'POST /food-safety-quality-compliance/improve1/root_cause_and_capa_linkage', ()), (16, 'Recall Event Classification', 'recall_event_classification', ('food_safety_quality_compliance_recall_classification',), ('classification', 'reason', 'affected_lots', 'distribution_scope', 'consumer_risk', 'regulator_notification', 'communication_plan', 'market_scope', 'mock_or_actual'), 'RecallEventClassification', 'POST /food-safety-quality-compliance/improve1/recall_event_classification', ()), (17, 'Recall Impact Analysis', 'recall_impact_analysis', ('food_safety_quality_compliance_recall_impact_analysis',), ('genealogy_projection', 'supplier_lots', 'production_windows', 'holds', 'shipment_projection', 'customer_projection', 'affected_lot_list', 'direct_external_read_blocked', 'analysis_complete'), 'RecallImpactAnalysis', 'POST /food-safety-quality-compliance/improve1/recall_impact_analysis', ('InventoryLotProjected', 'ShipmentScopeProjected', 'CustomerProjectionUpdated')), (18, 'Mock Recall Drill', 'mock_recall_drill', ('food_safety_quality_compliance_mock_recall_drill',), ('selected_product', 'trace_start', 'elapsed_minutes', 'completeness', 'gaps', 'corrective_actions', 'live_recall_mutation_blocked', 'evidence_packet', 'target_met'), 'MockRecallDrill', 'POST /food-safety-quality-compliance/improve1/mock_recall_drill', ()), (19, 'Product Disposition Controls', 'product_disposition_controls', ('food_safety_quality_compliance_product_disposition',), ('disposition_option', 'approval_authority', 'quantity_reconciliation', 'destination', 'destruction_proof', 'event_emission', 'authorization_valid', 'original_quantity', 'disposed_quantity'), 'ProductDispositionControls', 'POST /food-safety-quality-compliance/improve1/product_disposition_controls', ()), (20, 'Label and Packaging Verification', 'label_and_packaging_verification', ('food_safety_quality_compliance_label_packaging_verification',), ('label_version', 'packaging_line_check', 'barcode_check', 'allergen_statement', 'date_code', 'market_language', 'packaging_count_reconciliation', 'hold_opened', 'release_allowed'), 'LabelAndPackagingVerification', 'POST /food-safety-quality-compliance/improve1/label_and_packaging_verification', ()), (21, 'Foreign Material Control', 'foreign_material_control', ('food_safety_quality_compliance_foreign_material_control',), ('detector_check', 'sieve_inspection', 'magnet_inspection', 'brittle_material_register', 'finding', 'affected_lots', 'corrective_action', 'disposition_complete', 'release_blocked'), 'ForeignMaterialControl', 'POST /food-safety-quality-compliance/improve1/foreign_material_control', ()), (22, 'Shelf-Life and Stability Verification', 'shelf_life_and_stability_verification', ('food_safety_quality_compliance_shelf_life_stability',), ('shelf_life_protocol', 'sample_pulls', 'test_results', 'sensory_outcomes', 'storage_condition', 'date_code_rule', 'extension_approval', 'supporting_evidence', 'extension_allowed'), 'ShelfLifeAndStabilityVerification', 'POST /food-safety-quality-compliance/improve1/shelf_life_and_stability_verification', ()), (23, 'Sensory and Quality Attribute Panels', 'sensory_and_quality_attribute_panels', ('food_safety_quality_compliance_sensory_quality_panel',), ('sensory_panel_record', 'attribute_scores', 'trained_panelist_evidence', 'defect_type', 'release_recommendation', 'trend', 'hold_link', 'nonconformance_link', 'quality_route'), 'SensoryAndQualityAttributePanels', 'POST /food-safety-quality-compliance/improve1/sensory_and_quality_attribute_panels', ()), (24, 'Temperature and Cold Chain Compliance', 'temperature_and_cold_chain_compliance', ('food_safety_quality_compliance_cold_chain_compliance',), ('temperature_profile_projection', 'excursion_duration', 'product_tolerance', 'corrective_action', 'disposition_review', 'evidence_present', 'out_of_tolerance', 'hold_required', 'release_allowed'), 'TemperatureAndColdChainCompliance', 'POST /food-safety-quality-compliance/improve1/temperature_and_cold_chain_compliance', ('ColdChainTelemetryProjected',)), (25, 'Regulatory Obligation Register', 'regulatory_obligation_register', ('food_safety_quality_compliance_regulatory_obligation',), ('jurisdiction', 'requirement', 'evidence', 'due_date', 'owner', 'status', 'noncompliance_consequence', 'task_opened', 'evidence_packet_link'), 'RegulatoryObligationRegister', 'POST /food-safety-quality-compliance/improve1/regulatory_obligation_register', ()), (26, 'Audit Evidence Room', 'audit_evidence_room', ('food_safety_quality_compliance_audit_evidence_room',), ('facility', 'product', 'lot', 'period', 'audit_type', 'finding', 'redaction_applied', 'source_links', 'packet_complete'), 'AuditEvidenceRoom', 'POST /food-safety-quality-compliance/improve1/audit_evidence_room', ()), (27, 'Training and Competency Boundary', 'training_and_competency_boundary', ('food_safety_quality_compliance_training_projection',), ('role', 'course', 'expiry', 'competency_status', 'freshness', 'task_authorization_effect', 'direct_training_read_blocked', 'projection_source', 'authorization_allowed'), 'TrainingAndCompetencyBoundary', 'POST /food-safety-quality-compliance/improve1/training_and_competency_boundary', ('TrainingCompetencyProjected',)), (28, 'Food Safety Workbench', 'food_safety_workbench', ('food_safety_quality_compliance_workbench_queue',), ('ccp_failure_queue', 'hold_queue', 'inspection_queue', 'nonconformance_queue', 'supplier_gap_queue', 'recall_task_queue', 'sanitation_failure_queue', 'obligation_expiry_queue', 'permission_actions'), 'FoodSafetyWorkbench', 'POST /food-safety-quality-compliance/improve1/food_safety_workbench', ()), (29, 'Agent-Assisted Food Safety Review', 'agent_assisted_food_safety_review', ('food_safety_quality_compliance_agent_review_skill',), ('skill_name', 'haccp_summary', 'recall_impact_draft', 'root_cause_outline', 'audit_checklist', 'hold_disposition_summary', 'source_citations', 'human_approval_required', 'release_impact_action_blocked'), 'AgentAssistedFoodSafetyReview', 'POST /food-safety-quality-compliance/improve1/agent_assisted_food_safety_review', ()), (30, 'Governed Agent CRUD Commands', 'governed_agent_crud_commands', ('food_safety_quality_compliance_agent_crud_preview',), ('intent', 'entity_identity', 'evidence', 'preview', 'confirmation', 'authority', 'audit_trail', 'owned_table_target', 'mutation_allowed'), 'GovernedAgentCrudCommands', 'POST /food-safety-quality-compliance/improve1/governed_agent_crud_commands', ()), (31, 'HACCP Change Impact Simulation', 'haccp_change_impact_simulation', ('food_safety_quality_compliance_haccp_change_simulation',), ('product_families', 'ccp_records', 'holds', 'nonconformances', 'supplier_lots', 'impact_report', 'live_mutation_blocked', 'activation_required', 'risk_level'), 'HaccpChangeImpactSimulation', 'POST /food-safety-quality-compliance/improve1/haccp_change_impact_simulation', ()), (32, 'Predictive Food Safety Risk', 'predictive_food_safety_risk', ('food_safety_quality_compliance_predictive_risk_score',), ('product', 'line', 'supplier', 'facility', 'process_step', 'risk_score', 'explainable_factors', 'human_review_required', 'automated_hold_blocked'), 'PredictiveFoodSafetyRisk', 'POST /food-safety-quality-compliance/improve1/predictive_food_safety_risk', ()), (33, 'Quality Trend Analytics', 'quality_trend_analytics', ('food_safety_quality_compliance_quality_trend_analytics',), ('complaint_projection', 'hold_trend', 'nonconformance_trend', 'ccp_failure_trend', 'supplier_finding_trend', 'environmental_positive_trend', 'recall_drill_gap_trend', 'tenant_scope', 'evidence_drilldown'), 'QualityTrendAnalytics', 'POST /food-safety-quality-compliance/improve1/quality_trend_analytics', ()), (34, 'Complaint and Adverse Feedback Boundary', 'complaint_and_adverse_feedback_boundary', ('food_safety_quality_compliance_complaint_projection',), ('product', 'lot', 'allegation', 'severity', 'source', 'freshness', 'linked_investigation', 'direct_service_read_blocked', 'projection_valid'), 'ComplaintAndAdverseFeedbackBoundary', 'POST /food-safety-quality-compliance/improve1/complaint_and_adverse_feedback_boundary', ('CustomerComplaintProjected',)), (35, 'Incident Escalation Matrix', 'incident_escalation_matrix', ('food_safety_quality_compliance_incident_escalation_matrix',), ('severity', 'product_risk', 'market', 'regulator_duty', 'media_exposure', 'notification_list', 'deadline', 'required_approvals', 'acknowledgement_evidence'), 'IncidentEscalationMatrix', 'POST /food-safety-quality-compliance/improve1/incident_escalation_matrix', ()), (36, 'Multi-Facility and Market Localization', 'multi_facility_and_market_localization', ('food_safety_quality_compliance_market_localization',), ('facility_variant', 'product_policy', 'customer_restriction', 'jurisdiction', 'market_language', 'label_requirement', 'recall_workflow', 'policy_outcome', 'localized_decision'), 'MultiFacilityAndMarketLocalization', 'POST /food-safety-quality-compliance/improve1/multi_facility_and_market_localization', ()), (37, 'Continuous Control Assertions', 'continuous_control_assertions', ('food_safety_quality_compliance_continuous_control_assertion',), ('population', 'threshold', 'failing_records', 'owner', 'remediation', 'recurrence', 'closure_evidence', 'control_failure_opened', 'remediation_proof'), 'ContinuousControlAssertions', 'POST /food-safety-quality-compliance/improve1/continuous_control_assertions', ()), (38, 'Dead-Letter and Retry Operations', 'dead_letter_and_retry_operations', ('food_safety_quality_compliance_dead_letter_retry',), ('retry_reason', 'risk', 'idempotency_key', 'replay_checkpoint', 'remediation_action', 'dead_letter_queue', 'duplicate_hold_prevented', 'duplicate_recall_prevented', 'replay_result'), 'DeadLetterAndRetryOperations', 'POST /food-safety-quality-compliance/improve1/dead_letter_and_retry_operations', ('PolicyChanged',)), (39, 'Cryptographic Food Safety Evidence', 'cryptographic_food_safety_evidence', ('food_safety_quality_compliance_crypto_evidence_chain',), ('record_type', 'payload_hash', 'previous_hash', 'sequence_number', 'signature', 'timestamp', 'proof_verified', 'tamper_detected', 'ordering_valid'), 'CryptographicFoodSafetyEvidence', 'POST /food-safety-quality-compliance/improve1/cryptographic_food_safety_evidence', ()), (40, 'Role-Based Permission Model', 'role_based_permission_model', ('food_safety_quality_compliance_permission_model',), ('role', 'command', 'required_permission', 'authorized', 'disabled_ui_action', 'authority_scope', 'approval_needed', 'audit_subject', 'permission_result'), 'RoleBasedPermissionModel', 'POST /food-safety-quality-compliance/improve1/role_based_permission_model', ()), (41, 'Supplier Corrective Action Workflow', 'supplier_corrective_action_workflow', ('food_safety_quality_compliance_supplier_capa_workflow',), ('supplier_finding', 'due_date', 'response', 'evidence', 'effectiveness', 'repeat_finding', 'supplier_approval_status', 'overdue', 'approval_suspended'), 'SupplierCorrectiveActionWorkflow', 'POST /food-safety-quality-compliance/improve1/supplier_corrective_action_workflow', ()), (42, 'Product Release Gate', 'product_release_gate', ('food_safety_quality_compliance_product_release_gate',), ('haccp_check', 'ccp_check', 'inspection_check', 'quality_check', 'label_check', 'hold_status', 'blocking_exceptions', 'approver', 'release_event'), 'ProductReleaseGate', 'POST /food-safety-quality-compliance/improve1/product_release_gate', ()), (43, 'Regulatory Reporting Triggers', 'regulatory_reporting_triggers', ('food_safety_quality_compliance_regulatory_reporting_trigger',), ('report_trigger', 'jurisdiction', 'recipient', 'deadline', 'required_fields', 'submission_status', 'correction_history', 'report_candidate_created', 'submission_evidence'), 'RegulatoryReportingTriggers', 'POST /food-safety-quality-compliance/improve1/regulatory_reporting_triggers', ('AuditEventSealed',)), (44, 'Waste and Disposal Evidence', 'waste_and_disposal_evidence', ('food_safety_quality_compliance_disposal_evidence',), ('disposal_method', 'quantity', 'vendor_projection', 'witness', 'certificate', 'environmental_category', 'reconciliation', 'original_held_quantity', 'disposed_quantity'), 'WasteAndDisposalEvidence', 'POST /food-safety-quality-compliance/improve1/waste_and_disposal_evidence', ()), (45, 'Seeded Food Safety Scenario Library', 'seeded_food_safety_scenario_library', ('food_safety_quality_compliance_seed_scenario_library',), ('ccp_failure_seed', 'allergen_label_seed', 'supplier_audit_seed', 'environmental_positive_seed', 'quality_hold_seed', 'mock_recall_seed', 'product_disposition_seed', 'audit_request_seed', 'side_effect_free_loaded'), 'SeededFoodSafetyScenarioLibrary', 'POST /food-safety-quality-compliance/improve1/seeded_food_safety_scenario_library', ()), (46, 'Product Claim and Certification Evidence', 'product_claim_and_certification_evidence', ('food_safety_quality_compliance_claim_certification',), ('claim_type', 'certification_scope', 'certificate', 'expiry', 'product_applicability', 'lot_applicability', 'label_linkage', 'claim_evidence_valid', 'label_release_allowed'), 'ProductClaimAndCertificationEvidence', 'POST /food-safety-quality-compliance/improve1/product_claim_and_certification_evidence', ()), (47, 'Customer Specification Compliance', 'customer_specification_compliance', ('food_safety_quality_compliance_customer_spec_projection',), ('customer_spec_projection', 'required_attributes', 'effective_period', 'tested_result', 'waiver', 'shipment_eligibility', 'direct_customer_master_read_blocked', 'spec_result', 'release_allowed'), 'CustomerSpecificationCompliance', 'POST /food-safety-quality-compliance/improve1/customer_specification_compliance', ('CustomerSpecProjected',)), (48, 'Full Food Safety Release Simulation', 'full_food_safety_release_simulation', ('food_safety_quality_compliance_release_simulation',), ('haccp_activated', 'ccp_monitoring_recorded', 'inspection_defect_found', 'product_held', 'nonconformance_opened', 'supplier_evidence_reviewed', 'recall_drill_run', 'disposition_closed', 'all_surfaces_validated'), 'FullFoodSafetyReleaseSimulation', 'POST /food-safety-quality-compliance/improve1/full_food_safety_release_simulation', ()), (49, 'Package Overlap Guardrails', 'package_overlap_guardrails', ('food_safety_quality_compliance_overlap_guardrail',), ('lot_genealogy_dependency', 'production_event_dependency', 'supplier_status_dependency', 'complaint_signal_dependency', 'shipment_scope_dependency', 'filing_dependency', 'external_table_reference_blocked', 'declared_dependency_used', 'boundary_valid'), 'PackageOverlapGuardrails', 'POST /food-safety-quality-compliance/improve1/package_overlap_guardrails', ('InventoryLotProjected', 'ProductionLotProjected', 'SupplierStatusChanged', 'CustomerComplaintProjected', 'ShipmentScopeProjected', 'RegulatoryFilingProjected')), (50, 'Composition DSL and Unified Agent Exposure', 'composition_dsl_and_unified_agent_exposure', ('food_safety_quality_compliance_dsl_agent_exposure',), ('dsl_models', 'dsl_routes', 'dsl_services', 'event_contracts', 'ui_artifacts', 'assistant_skills', 'unified_agent_contribution', 'stream_engine_picker_hidden', 'composition_valid'), 'CompositionDslAndUnifiedAgentExposure', 'POST /food-safety-quality-compliance/improve1/composition_dsl_and_unified_agent_exposure', ())]
CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"title": title, "slug": slug, "tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, title, slug, tables, fields, ui, route, deps in _SPEC_ROWS}
_EMPTY_ALLOWED_FIELDS = ("supersession_reason", "finding", "deviation", "waiver_approval", "gaps", "correction_history", "tamper_detected", "blocking_exceptions")


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({
        "approved_controls": ("validated_ccp",), "effective_window": "2026-05-30/2027-05-30", "historical_reference_pinned": True,
        "hazard_type": "biological", "likelihood": "medium", "severity": "high", "linked_ccp": "ccp-cook-temp", "mapping_complete": True, "definition_allowed": True,
        "limit_min": 72, "limit_max": 78, "unit": "C", "frequency_minutes": 30, "verification_requirement": "qa_review",
        "value": 74, "timestamp": "2026-05-30T08:00:00Z", "source_evidence": "device-log", "pass_fail": "pass", "review_state": "reviewed",
        "disposition": "hold_until_verified", "root_cause": "identified", "verifier": "qa-manager", "restart_criteria": "met", "evidence_complete": True, "release_blocked": False,
        "quantity_reconciled": True, "projection_freshness": "fresh", "declared_event_source": "InventoryLotProjected", "direct_inventory_read_blocked": True, "trace_complete": True,
        "line_clearance_check": "pass", "label_verification": "match", "cross_contact_risk": "controlled", "nonconformance_opened": False, "release_allowed": True,
        "swab_result": "pass", "visual_check": "pass", "pre_op_approval": True, "failed_cleaning_action": "not_required",
        "result": "negative", "trend": "stable", "product_impact_assessment": "not_impacted", "escalation_level": "normal",
        "severity": "minor", "action_required": False, "repeat_finding_marker": False, "due_corrective_action": "none",
        "risk_rating": "low", "approval_status": "approved", "expiry": "2027-05-30", "supplier_use_blocked": False,
        "pass_fail": "pass", "lot_hold_required": False, "micro_limit_status": "pass", "chemical_limit_status": "pass",
        "closure_allowed": True, "classification": "mock_recall", "consumer_risk": "low", "regulator_notification": "not_required",
        "affected_lot_list": ("lot-1",), "direct_external_read_blocked": True, "analysis_complete": True,
        "elapsed_minutes": 60, "completeness": 1.0, "live_recall_mutation_blocked": True, "target_met": True,
        "authorization_valid": True, "original_quantity": 100, "disposed_quantity": 100, "packaging_count_reconciliation": True, "hold_opened": False,
        "disposition_complete": True, "extension_approval": "approved", "supporting_evidence": "stability-study", "extension_allowed": True,
        "trained_panelist_evidence": "current", "release_recommendation": "release", "hold_link": "none", "temperature_profile_projection": "within_tolerance", "evidence_present": True, "out_of_tolerance": False, "hold_required": False,
        "status": "current", "task_opened": False, "redaction_applied": True, "source_links": ("haccp-plan", "ccp-record"), "packet_complete": True,
        "competency_status": "current", "freshness": "fresh", "direct_training_read_blocked": True, "authorization_allowed": True,
        "ccp_failure_queue": True, "hold_queue": True, "inspection_queue": True, "nonconformance_queue": True, "supplier_gap_queue": True, "recall_task_queue": True, "sanitation_failure_queue": True, "obligation_expiry_queue": True, "permission_actions": "role_filtered",
        "source_citations": ("record-1",), "human_approval_required": True, "release_impact_action_blocked": True,
        "preview": True, "confirmation": True, "authority": "authorized", "audit_trail": "captured", "owned_table_target": True, "mutation_allowed": False,
        "impact_report": "generated", "live_mutation_blocked": True, "activation_required": True, "risk_level": "review",
        "risk_score": 0.42, "explainable_factors": ("sanitation_trend",), "human_review_required": True, "automated_hold_blocked": True,
        "tenant_scope": "tenant-a", "evidence_drilldown": True, "direct_service_read_blocked": True, "projection_valid": True,
        "regulator_duty": "evaluate", "notification_list": ("qa",), "deadline": "2026-05-31", "required_approvals": ("qa_manager",), "acknowledgement_evidence": "captured",
        "localized_decision": "market_specific", "control_failure_opened": False, "remediation_proof": "captured",
        "idempotency_key": "food-idem-1", "duplicate_hold_prevented": True, "duplicate_recall_prevented": True, "replay_result": "succeeded",
        "payload_hash": "sha256:payload", "previous_hash": "sha256:previous", "sequence_number": 1, "signature": "signed", "proof_verified": True, "tamper_detected": False, "ordering_valid": True,
        "authorized": True, "disabled_ui_action": False, "permission_result": "allowed", "overdue": False, "approval_suspended": False,
        "haccp_check": True, "ccp_check": True, "inspection_check": True, "quality_check": True, "label_check": True, "hold_status": "clear", "release_event": "FoodSafetyQualityComplianceApproved",
        "report_candidate_created": True, "submission_evidence": "captured", "reconciliation": True, "original_held_quantity": 100,
        "ccp_failure_seed": True, "allergen_label_seed": True, "supplier_audit_seed": True, "environmental_positive_seed": True, "quality_hold_seed": True, "mock_recall_seed": True, "product_disposition_seed": True, "audit_request_seed": True, "side_effect_free_loaded": True,
        "claim_evidence_valid": True, "label_release_allowed": True, "customer_spec_projection": "declared", "direct_customer_master_read_blocked": True, "spec_result": "pass",
        "haccp_activated": True, "ccp_monitoring_recorded": True, "inspection_defect_found": True, "product_held": True, "nonconformance_opened": True, "supplier_evidence_reviewed": True, "recall_drill_run": True, "disposition_closed": True, "all_surfaces_validated": True,
        "external_table_reference_blocked": True, "declared_dependency_used": True, "boundary_valid": True,
        "dsl_models": True, "dsl_routes": True, "dsl_services": True, "event_contracts": True, "ui_artifacts": True, "assistant_skills": True, "unified_agent_contribution": True, "stream_engine_picker_hidden": True, "composition_valid": True,
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and payload.get("historical_reference_pinned") is not True:
        findings.append("HACCP version governance must pin historical inspections and holds to the active version")
    if n == 2 and (payload.get("mapping_complete") is not True or payload.get("linked_ccp") in (None, "")):
        findings.append("CCP definition requires a mapped process step and hazard")
    if n == 3 and not (payload.get("limit_min") <= payload.get("value", payload.get("limit_min")) <= payload.get("limit_max")):
        findings.append("critical control point reading is outside measurable limits")
    if n == 4 and (payload.get("unit") not in ("C", "pH", "ppm", "minutes") or payload.get("pass_fail") != "pass" or payload.get("review_state") != "reviewed"):
        findings.append("monitoring record requires valid unit, passing result, and review")
    if n == 5 and (payload.get("evidence_complete") is not True or payload.get("release_blocked") is True):
        findings.append("CCP failure corrective action must complete evidence before release")
    if n == 6 and (payload.get("approver") in (None, "") or payload.get("quantity_reconciled") is not True):
        findings.append("quality hold release requires approval and quantity reconciliation")
    if n == 7 and payload.get("direct_inventory_read_blocked") is not True:
        findings.append("lot genealogy must use declared projections, not direct inventory reads")
    if n == 8 and (payload.get("line_clearance_check") != "pass" or payload.get("label_verification") != "match"):
        findings.append("allergen clearance or label mismatch opens nonconformance")
    if n == 9 and (payload.get("swab_result") != "pass" or payload.get("pre_op_approval") is not True):
        findings.append("failed sanitation verification blocks start or release")
    if n == 10 and payload.get("result") == "positive" and payload.get("product_impact_assessment") in (None, ""):
        findings.append("positive environmental monitoring requires product risk review")
    if n == 12 and (payload.get("approval_status") != "approved" or payload.get("supplier_use_blocked") is True):
        findings.append("supplier use is blocked until audit approval is current")
    if n == 15 and (payload.get("root_cause") in (None, "") or payload.get("effectiveness_check") in (None, "") or payload.get("closure_allowed") is not True):
        findings.append("major nonconformance closure requires root cause and effectiveness evidence")
    if n == 17 and payload.get("direct_external_read_blocked") is not True:
        findings.append("recall impact analysis cannot read external tables directly")
    if n == 18 and payload.get("live_recall_mutation_blocked") is not True:
        findings.append("mock recall drill must not mutate live recall state")
    if n == 19 and (payload.get("authorization_valid") is not True or payload.get("quantity_reconciliation") in (None, "") or payload.get("original_quantity") != payload.get("disposed_quantity")):
        findings.append("product disposition requires authority and full quantity accounting")
    if n == 24 and (payload.get("evidence_present") is not True or payload.get("out_of_tolerance") is True):
        findings.append("cold-chain excursion or missing evidence requires hold")
    if n == 29 and (not payload.get("source_citations") or payload.get("human_approval_required") is not True or payload.get("release_impact_action_blocked") is not True):
        findings.append("agent food safety review requires citations and human release approval")
    if n == 30 and (payload.get("preview") is not True or payload.get("confirmation") is not True or payload.get("owned_table_target") is not True or payload.get("mutation_allowed") is True):
        findings.append("governed agent CRUD commands must be previewed, confirmed, and owned-table scoped")
    if n == 31 and payload.get("live_mutation_blocked") is not True:
        findings.append("HACCP change impact simulation must be side-effect free")
    if n == 34 and payload.get("direct_service_read_blocked") is not True:
        findings.append("complaint boundary must use declared projections instead of service table reads")
    if n == 38 and (payload.get("duplicate_hold_prevented") is not True or payload.get("duplicate_recall_prevented") is not True):
        findings.append("dead-letter replay must not create duplicate holds or recalls")
    if n == 39 and (payload.get("proof_verified") is not True or payload.get("tamper_detected") is True or payload.get("ordering_valid") is not True):
        findings.append("cryptographic food safety evidence chain failed verification")
    if n == 40 and payload.get("authorized") is not True:
        findings.append("role-based permission model blocks unauthorized command")
    if n == 42 and not all(payload.get(field) is True for field in ("haccp_check", "ccp_check", "inspection_check", "quality_check", "label_check")):
        findings.append("product release gate requires every safety and quality check")
    if n == 48 and not all(payload.get(field) is True for field in ("haccp_activated", "ccp_monitoring_recorded", "inspection_defect_found", "product_held", "nonconformance_opened", "supplier_evidence_reviewed", "recall_drill_run", "disposition_closed", "all_surfaces_validated")):
        findings.append("full food safety release simulation is incomplete")
    if n == 49 and (payload.get("external_table_reference_blocked") is not True or payload.get("declared_dependency_used") is not True or payload.get("boundary_valid") is not True):
        findings.append("package overlap guardrails require declared dependencies and blocked external table references")
    if n == 50 and (payload.get("composition_valid") is not True or payload.get("stream_engine_picker_hidden") is not True):
        findings.append("composition DSL and unified agent exposure must include all artifacts without stream picker")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_food_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in FOOD_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in FOOD_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": FOOD_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": FOOD_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_food_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_food_control(capability) for capability in FOOD_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.food-safety-quality-compliance-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": FOOD_CONTROL_OWNED_TABLES, "declared_dependencies": FOOD_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": FOOD_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": FOOD_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


FOOD_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_food_control(slug, payload)) for capability in FOOD_CONTROL_CAPABILITIES}
