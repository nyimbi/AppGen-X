"""Executable improve1 controls for the Enterprise Risk Controls PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "enterprise_risk_controls"
EVENT_CONTRACT = "AppGen-X"
RISK_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
RISK_REQUIRED_EVENT_TOPIC = "pbc.enterprise_risk_controls.events"
RISK_OWNED_TABLES = tuple(DOMAIN_OWNED_TABLES) + (
    "enterprise_risk_controls_appgen_outbox_event",
    "enterprise_risk_controls_appgen_inbox_event",
    "enterprise_risk_controls_appgen_dead_letter_event",
)
RISK_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + (
    "PolicyChanged",
    "AuditProofGenerated",
    "AccessPolicyChanged",
    "WorkflowTaskCompleted",
    "RiskRegistered",
    "RiskAssessed",
    "ControlTested",
    "ControlExceptionOpened",
    "RemediationOpened",
    "AssurancePacketGenerated",
    "POST /notifications/messages",
    "GET /policies/obligations/{id}",
    "GET /audit/proofs/{id}",
    "GET /identity/access-policies/{id}",
    "GET /workflow/tasks/{id}",
    "GET /sustainability/esg-projections/{id}",
    "GET /vendors/exposures/{id}",
    "GET /incidents/operational-events/{id}",
)))

RISK_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in RISK_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in RISK_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = (
    (1, ("enterprise_risk_controls_risk_taxonomy", "enterprise_risk_controls_risk_register"), ("taxonomy_version", "risk_categories", "causal_drivers", "impacted_objectives", "affected_pbcs", "regulatory_domains", "relationship_graph", "approval_status"), "RiskTaxonomyOntologyStudio", "POST /risk-taxonomies/classify", ()),
    (2, ("enterprise_risk_controls_risk_register", "enterprise_risk_controls_audit_evidence_packet"), ("risk_statement", "cause", "event", "impact", "owner", "taxonomy", "affected_pbc", "inherent_exposure", "evidence_attachments", "readiness_status"), "RiskIntakeReadinessGate", "POST /risks/readiness-check", ()),
    (3, ("enterprise_risk_controls_risk_assessment", "enterprise_risk_controls_control_library"), ("inherent_likelihood", "inherent_impact", "residual_likelihood", "residual_impact", "target_likelihood", "target_impact", "velocity", "persistence", "confidence", "reviewer_approval"), "RiskAssessmentDeltaStudio", "POST /risk-assessments/separate-posture", ()),
    (4, ("enterprise_risk_controls_risk_appetite_statement", "enterprise_risk_controls_risk_policy_rule"), ("appetite_text", "thresholds", "qualitative_tolerances", "indicator_limits", "escalation_rules", "reporting_obligations", "simulation_result", "active_version"), "RiskAppetiteCompiler", "POST /risk-appetite/compile", ("PolicyChanged",)),
    (5, ("enterprise_risk_controls_risk_indicator", "enterprise_risk_controls_risk_indicator_observation"), ("formula", "source_projection", "measurement_grain", "frequency", "thresholds", "owner", "stale_data_rules", "quality_checks", "quarantine_status"), "KriDefinitionQualityConsole", "POST /risk-indicators/observe", ()),
    (6, ("enterprise_risk_controls_risk_indicator_observation", "enterprise_risk_controls_risk_assessment"), ("trend", "acceleration", "threshold_proximity", "correlated_indicators", "seasonality", "cross_pbc_signals", "breach_drivers", "posture_event"), "KriEarlyWarningEngine", "POST /risk-indicators/early-warning", ("WorkflowTaskCompleted",)),
    (7, ("enterprise_risk_controls_control_library", "enterprise_risk_controls_control_objective"), ("control_type", "control_objective", "risk_linkage", "frequency", "control_nature", "automation_level", "key_control", "system_dependency", "evidence_expectation", "owner", "reviewer", "version_lineage"), "ControlLibraryArchitectureStudio", "POST /controls/define", ()),
    (8, ("enterprise_risk_controls_control_objective", "enterprise_risk_controls_control_library"), ("assertions", "coverage_gaps", "duplicate_controls", "compensating_controls", "unsupported_risks", "policy_coverage", "risk_coverage"), "ControlAssertionCoverageMap", "POST /control-objectives/map", ()),
    (9, ("enterprise_risk_controls_policy_control_mapping", "enterprise_risk_controls_control_library"), ("policy_clause", "obligation_taxonomy", "semantic_similarity", "mapping_confidence", "reviewer_approval", "effective_dates", "orphan_obligations", "mapping_rationale", "policy_version"), "PolicyControlSemanticMapper", "POST /policy-control-mappings/semantic-map", ("PolicyChanged", "GET /policies/obligations/{id}")),
    (10, ("enterprise_risk_controls_control_test", "enterprise_risk_controls_control_library"), ("procedure_steps", "scope_period", "sample_population", "sampling_strategy", "expected_evidence", "tester_role", "independence_check", "due_date", "test_objective"), "ControlTestPlanGenerator", "POST /control-tests/generate-plan", ()),
    (11, ("enterprise_risk_controls_control_test_evidence", "enterprise_risk_controls_risk_control_assertion"), ("source", "source_api", "source_event", "timestamp", "evidence_hash", "freshness", "completeness", "collection_status", "owned_metadata_only"), "AutomatedEvidenceCollector", "POST /control-evidence/collect", ("AuditProofGenerated", "GET /audit/proofs/{id}")),
    (12, ("enterprise_risk_controls_control_test_evidence", "enterprise_risk_controls_control_test"), ("sufficiency", "relevance", "period_coverage", "source_authenticity", "tamper_hash", "completeness_score", "exception_flags", "reviewer_notes", "completion_gate"), "EvidenceQualityScoringPanel", "POST /control-evidence/score", ("AuditProofGenerated",)),
    (13, ("enterprise_risk_controls_risk_control_assertion", "enterprise_risk_controls_control_exception"), ("monitoring_mode", "subscribed_event_types", "assertion_expression", "observation_result", "exception_policy", "evidence_trail", "failure_route"), "ContinuousControlMonitor", "POST /controls/continuous-monitoring/run", tuple(DOMAIN_CONSUMED_EVENTS)),
    (14, ("enterprise_risk_controls_control_test", "enterprise_risk_controls_risk_model_output"), ("risk_rating", "population_size", "anomaly_score", "failure_history", "regulatory_importance", "confidence_level", "sample_size", "sampling_rationale", "auditor_override"), "RiskBasedSamplingWorkbench", "POST /control-tests/sampling-plan", ()),
    (15, ("enterprise_risk_controls_control_test", "enterprise_risk_controls_control_test_evidence"), ("test_steps", "evidence_checklist", "sample_list", "pass_fail_criteria", "observed_deviations", "reviewer_comments", "retest_tasks", "final_conclusion", "tester_identity"), "ControlTestExecutionWorkbench", "POST /control-tests/execute", ()),
    (16, ("enterprise_risk_controls_control_attestation", "enterprise_risk_controls_control_owner_assignment"), ("campaign_scope", "attestor_role", "control_set", "certification_text", "evidence_summary", "known_exceptions", "delegation_rules", "reminders", "legal_acknowledgement", "late_response_status"), "AttestationCampaignConsole", "POST /attestations/campaigns", ("WorkflowTaskCompleted",)),
    (17, ("enterprise_risk_controls_control_owner_assignment", "enterprise_risk_controls_control_library"), ("owner_history", "delegate_authority", "backup_owner", "effective_dates", "segregation_rules", "role_requirements", "vacancy_alert", "independence_preserved"), "ControlOwnerDelegationConsole", "POST /control-owners/assign", ("AccessPolicyChanged",)),
    (18, ("enterprise_risk_controls_control_exception", "enterprise_risk_controls_remediation_issue"), ("exception_type", "exposure", "materiality", "compensating_control", "risk_acceptance", "expiry", "owner", "approval_chain", "retest_requirement", "residual_risk_impact"), "ControlExceptionLifecycle", "POST /control-exceptions/open", ()),
    (19, ("enterprise_risk_controls_incident_record", "enterprise_risk_controls_risk_assessment"), ("realized_risk", "affected_controls", "loss_estimate", "operational_impact", "root_cause", "detection_method", "time_to_detect", "time_to_contain", "lessons_learned", "reassessment_required"), "IncidentRiskLinkageStudio", "POST /incidents/link-risk", ("GET /incidents/operational-events/{id}",)),
    (20, ("enterprise_risk_controls_remediation_issue", "enterprise_risk_controls_remediation_action"), ("issue_severity", "root_cause", "risk_linkage", "control_linkage", "target_state", "owner", "sponsor", "milestones", "budget", "dependencies", "validation_plan", "acceptance_criteria"), "RemediationGovernanceTracker", "POST /remediations/open", ()),
    (21, ("enterprise_risk_controls_remediation_action", "enterprise_risk_controls_control_test"), ("action_evidence", "completion_criteria", "blocker_reasons", "due_date_changes", "implementation_proof", "retest_schedule", "validation_owner", "closure_approval"), "RemediationRetestBoard", "POST /remediation-actions/track", ("WorkflowTaskCompleted",)),
    (22, ("enterprise_risk_controls_control_exception", "enterprise_risk_controls_risk_appetite_statement"), ("approver_authority", "scope", "duration", "rationale", "residual_exposure", "compensating_controls", "review_date", "revocation_triggers", "accepted_risk_flag"), "RiskAcceptanceWaiverConsole", "POST /risk-acceptances", ()),
    (23, ("enterprise_risk_controls_risk_heatmap_snapshot", "enterprise_risk_controls_risk_assessment"), ("heatmap_methodology", "source_risks", "scoring_version", "appetite_overlays", "trend_arrows", "confidence", "stale_data_flags", "drilldown_evidence", "immutable_snapshot"), "ExecutiveRiskHeatmap", "POST /risk-heatmaps/publish", ()),
    (24, ("enterprise_risk_controls_risk_scenario", "enterprise_risk_controls_risk_model_output"), ("scenario_library", "assumptions", "affected_pbcs", "risk_drivers", "control_responses", "impact_ranges", "recovery_times", "dependencies", "executive_summary", "version_comparison"), "RiskScenarioStressLab", "POST /risk-scenarios/simulate", ()),
    (25, ("enterprise_risk_controls_control_exception", "enterprise_risk_controls_risk_control_assertion"), ("failed_key_control", "affected_risks", "policy_obligations", "owners", "evidence_packets", "open_attestations", "remediations", "executive_reports", "review_tasks"), "ControlFailureBlastRadius", "POST /controls/blast-radius", ()),
    (26, ("enterprise_risk_controls_audit_evidence_packet", "enterprise_risk_controls_control_test_evidence"), ("packet_scope", "included_controls", "included_tests", "evidence_hashes", "attestations", "exceptions", "remediation_status", "event_lineage", "reviewer_signoff", "export_manifest", "integrity_proof"), "AssuranceEvidencePacketRoom", "POST /assurance-packets/generate", ("AuditProofGenerated",)),
    (27, ("enterprise_risk_controls_risk_committee_packet", "enterprise_risk_controls_risk_heatmap_snapshot"), ("agenda", "narrative", "exhibits", "heatmaps", "issue_decisions", "voting_records", "action_items", "follow_up_tracking", "decision_linkages"), "RiskCommitteePacketBuilder", "POST /risk-committee-packets", ("WorkflowTaskCompleted",)),
    (28, ("enterprise_risk_controls_risk_register", "enterprise_risk_controls_risk_model_output"), ("source_signals", "candidate_confidence", "affected_objectives", "proposed_taxonomy", "owner", "promotion_workflow", "uncertainty", "registration_plan"), "EmergingRiskRadar", "POST /emerging-risks/promote", ("PolicyChanged", "WorkflowTaskCompleted")),
    (29, ("enterprise_risk_controls_risk_model_output", "enterprise_risk_controls_risk_governed_model"), ("model_version", "input_data", "assumptions", "validation_status", "drift_metrics", "limitations", "reviewer_approval", "override_records", "posture_change_gate"), "ModelRiskGovernanceConsole", "POST /risk-models/govern", ()),
    (30, ("enterprise_risk_controls_risk_assessment", "enterprise_risk_controls_risk_control_assertion"), ("external_entity_reference", "exposure_type", "dependency_strength", "criticality", "freshness", "concentration_heatmap", "scenario_impact", "declared_projection_only"), "ThirdPartyConcentrationView", "POST /risk-concentrations/assess", ("GET /vendors/exposures/{id}",)),
    (31, ("enterprise_risk_controls_risk_control_assertion", "enterprise_risk_controls_control_attestation"), ("access_policy_event", "identity_control_map", "privileged_access_attestation", "segregation_failure", "access_review_failure", "local_observation", "evidence_record"), "CyberAccessControlCoverage", "POST /access-control-observations", ("AccessPolicyChanged", "GET /identity/access-policies/{id}")),
    (32, ("enterprise_risk_controls_policy_control_mapping", "enterprise_risk_controls_control_objective"), ("obligation_source", "clause", "effective_date", "mapped_control", "test_frequency", "evidence_requirement", "owner", "gap_status", "recommended_control"), "RegulatoryObligationCoverageMatrix", "POST /obligations/coverage-matrix", ("PolicyChanged", "GET /policies/obligations/{id}")),
    (33, ("enterprise_risk_controls_control_library", "enterprise_risk_controls_risk_model_output"), ("manual_effort", "automation_level", "preventive_detective_balance", "evidence_automation", "failure_history", "monitoring_coverage", "modernization_actions", "effort_reduction_estimate"), "ControlAutomationMaturityScore", "POST /controls/maturity-score", ()),
    (34, ("enterprise_risk_controls_remediation_issue", "enterprise_risk_controls_remediation_action"), ("weighted_risk_impact", "appetite_breach", "due_dates", "dependencies", "cost", "owners", "blockers", "expected_residual_reduction", "funding_scenario"), "RemediationPortfolioPrioritizer", "POST /remediations/prioritize", ()),
    (35, ("enterprise_risk_controls_incident_record", "enterprise_risk_controls_risk_assessment"), ("financial_loss", "non_financial_impact", "avoided_loss", "cause", "business_line", "insurance_recovery", "control_failure", "lessons_learned", "calibration_update"), "LossNearMissCapture", "POST /loss-events/capture", ("GET /incidents/operational-events/{id}",)),
    (36, ("enterprise_risk_controls_risk_appetite_statement", "enterprise_risk_controls_remediation_issue"), ("breach_source", "severity", "owner", "required_action", "escalation_level", "committee_visibility", "acceptance_option", "closure_evidence", "heatmap_linkage"), "RiskAppetiteBreachWorkflow", "POST /risk-appetite/breaches", ("WorkflowTaskCompleted",)),
    (37, ("enterprise_risk_controls_control_owner_assignment", "enterprise_risk_controls_control_test"), ("tester", "reviewer", "control_owner", "remediation_owner", "attestor", "conflict_rule", "approved_exception", "assignment_gate"), "AssuranceIndependenceChecker", "POST /assurance/independence-check", ("AccessPolicyChanged",)),
    (38, ("enterprise_risk_controls_risk_register", "enterprise_risk_controls_risk_control_assertion"), ("sensitive_partition", "access_groups", "field_masking", "export_controls", "break_glass", "agent_restrictions", "audit_alerts", "api_enforcement"), "SensitiveRiskPartitionConsole", "POST /risks/sensitive-partitions", ("AccessPolicyChanged",)),
    (39, ("enterprise_risk_controls_risk_register", "enterprise_risk_controls_risk_control_assertion"), ("source_document", "extracted_risks", "extracted_controls", "extracted_mappings", "extracted_tests", "confidence", "affected_tables", "event_plan", "human_confirmation"), "AgentRiskControlIntake", "POST /assistant/risk-control-intake", ()),
    (40, ("enterprise_risk_controls_risk_policy_rule", "enterprise_risk_controls_risk_runtime_parameter"), ("rule_version", "simulation_scope", "historical_test_set", "approval_workflow", "effective_dates", "rollback_plan", "test_cases", "agent_explanation"), "PolicyControlRuleStudio", "POST /rules/simulate", ("PolicyChanged",)),
    (41, ("enterprise_risk_controls_risk_control_assertion", "enterprise_risk_controls_control_test_evidence"), ("source_pbc", "observed_event_api", "expected_invariant", "evidence_window", "freshness", "failure_handling", "owned_mutation_only", "appgen_event_plan"), "CrossPbcControlAssertionConsole", "POST /control-assertions/cross-pbc", tuple(DOMAIN_CONSUMED_EVENTS)),
    (42, ("enterprise_risk_controls_control_exception", "enterprise_risk_controls_remediation_issue"), ("failure_severity", "confidence", "duplicate_grouping", "owner", "compensating_control", "false_positive_reason", "remediation_link", "feedback_to_rule"), "ContinuousControlFailureTriage", "POST /control-failures/triage", ()),
    (43, ("enterprise_risk_controls_risk_assessment", "enterprise_risk_controls_risk_heatmap_snapshot", "enterprise_risk_controls_risk_committee_packet"), ("source_records", "versions", "timestamps", "transformations", "confidence", "lineage_graph", "material_output", "traceability_proof"), "RiskDataLineageViewer", "GET /risk-lineage/{output_id}", ("AuditProofGenerated",)),
    (44, ("enterprise_risk_controls_risk_taxonomy", "enterprise_risk_controls_control_objective"), ("sustainability_category", "climate_scenario", "carbon_control_objective", "esg_control_mapping", "indicator_templates", "evidence_requirements", "executive_view", "projection_freshness"), "SustainabilityRiskControls", "POST /sustainability-risk-controls", ("GET /sustainability/esg-projections/{id}",)),
    (45, ("enterprise_risk_controls_risk_policy_rule", "enterprise_risk_controls_policy_control_mapping"), ("changed_object", "affected_risks", "affected_controls", "affected_mappings", "affected_tests", "affected_packets", "dashboards", "rules", "external_dependencies", "material_approval"), "RiskControlChangeImpactAnalysis", "POST /risk-control-change-impact", ("PolicyChanged",)),
    (46, ("enterprise_risk_controls_risk_assessment", "enterprise_risk_controls_risk_indicator_observation", "enterprise_risk_controls_control_exception"), ("transaction_time", "valid_time", "reporting_time", "as_of_risk_scores", "as_of_kri_values", "as_of_control_status", "as_of_exceptions", "as_of_remediation", "temporal_consistency"), "RiskPostureTimeTravel", "GET /risk-posture/as-of", ()),
    (47, ("enterprise_risk_controls_risk_scenario", "enterprise_risk_controls_incident_record"), ("critical_service", "dependency", "rto_target", "rpo_target", "scenario_stress", "continuity_plan", "crisis_owner", "resilience_posture_update"), "OperationalResilienceRiskLinks", "POST /resilience-risk-links", ("GET /incidents/operational-events/{id}",)),
    (48, ("enterprise_risk_controls_risk_committee_packet", "enterprise_risk_controls_risk_heatmap_snapshot"), ("narrative_type", "source_citations", "confidence", "stale_data_flags", "uncertainty_disclosure", "owner_approval", "publication_gate", "evidence_links"), "ExecutiveNarrativeEvidenceGenerator", "POST /executive-risk-narratives", ()),
    (49, ("enterprise_risk_controls_audit_evidence_packet", "enterprise_risk_controls_risk_control_assertion"), ("schema_hashes", "migration_manifest", "service_contract", "route_contract", "event_schemas", "handler_idempotency", "retry_dead_letter_tests", "rule_simulations", "ui_coverage", "agent_skill_manifest"), "RiskControlReleaseEvidence", "POST /release/risk-control-integrity", tuple(DOMAIN_EVENTS)),
    (50, ("enterprise_risk_controls_risk_register", "enterprise_risk_controls_control_library", "enterprise_risk_controls_risk_committee_packet"), ("risk_manager_view", "control_owner_view", "tester_view", "attestor_view", "remediation_owner_view", "auditor_view", "committee_secretary_view", "executive_sponsor_view", "administrator_view", "release_evidence_status"), "CompleteEnterpriseRiskWorkbench", "GET /enterprise-risk-controls-workbench", ()),
)

CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, tables, fields, ui, route, deps in _SPEC_ROWS}
_EMPTY_ALLOWED_FIELDS = (
    "approved_exception",
    "blocker_reasons",
    "coverage_gaps",
    "duplicate_controls",
    "exception_flags",
    "false_positive_reason",
    "foreign_table_access",
    "known_exceptions",
    "open_attestations",
    "orphan_obligations",
    "override_records",
    "stale_data_flags",
    "unsupported_risks",
    "retest_tasks",
    "exceptions",
    "blockers",
)


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
        "taxonomy_version": "risk-tax-2026.05", "risk_categories": ("operational", "financial", "technology"), "causal_drivers": ("process_breakdown",), "impacted_objectives": ("cash_integrity",), "affected_pbcs": ("ap_automation",), "regulatory_domains": ("SOX",), "relationship_graph": "acyclic", "approval_status": "approved",
        "risk_statement": "Cause event impact statement", "cause": "manual_override", "event": "unauthorized_change", "impact": "material_misstatement", "owner": "risk-owner", "taxonomy": "operational", "affected_pbc": "ap_automation", "inherent_exposure": "high", "evidence_attachments": ("doc-1",), "readiness_status": "ready",
        "inherent_likelihood": 4, "inherent_impact": 5, "residual_likelihood": 2, "residual_impact": 3, "target_likelihood": 1, "target_impact": 2, "velocity": "fast", "persistence": "medium", "confidence": 0.91, "reviewer_approval": True,
        "appetite_text": "No unapproved privileged access", "thresholds": {"breach": 1}, "qualitative_tolerances": ("zero tolerance for fraud",), "indicator_limits": {"kri": 0}, "escalation_rules": ("committee",), "reporting_obligations": ("monthly",), "simulation_result": "pass", "active_version": "2026.05",
        "formula": "failed_controls / key_controls", "source_projection": "control_projection", "measurement_grain": "daily", "frequency": "daily", "thresholds": {"amber": 0.05, "red": 0.1}, "stale_data_rules": "PT24H", "quality_checks": "passed", "quarantine_status": "clear",
        "trend": "stable", "acceleration": 0.0, "threshold_proximity": "green", "correlated_indicators": ("access_review",), "seasonality": "adjusted", "cross_pbc_signals": ("AccessPolicyChanged",), "breach_drivers": ("none",), "posture_event": "RiskAssessed",
        "control_type": "approval", "control_objective": "authorized_changes", "risk_linkage": "risk-1", "control_nature": "preventive", "automation_level": "automated", "key_control": True, "system_dependency": "workflow_orchestration", "evidence_expectation": "event_proof", "reviewer": "assurance-reviewer", "version_lineage": ("v1", "v2"),
        "assertions": ("authorization", "accuracy"), "coverage_gaps": (), "duplicate_controls": (), "compensating_controls": ("manual_review",), "unsupported_risks": (), "policy_coverage": "complete", "risk_coverage": "complete",
        "policy_clause": "Access must be reviewed quarterly", "obligation_taxonomy": "access_review", "semantic_similarity": 0.88, "mapping_confidence": 0.9, "effective_dates": ("2026-05-30", "2027-05-30"), "orphan_obligations": (), "mapping_rationale": "semantic obligation match", "policy_version": "policy-2026.05",
        "procedure_steps": ("obtain population", "sample", "inspect evidence"), "scope_period": "2026-Q2", "sample_population": 1200, "sampling_strategy": "risk_weighted", "expected_evidence": ("approval_event",), "tester_role": "independent_tester", "independence_check": "passed", "due_date": "2026-06-30", "test_objective": "operating_effectiveness",
        "source": "audit_ledger", "source_api": "GET /audit/proofs/{id}", "source_event": "AuditProofGenerated", "timestamp": "2026-05-30T00:00:00Z", "evidence_hash": "sha256:evidence", "freshness": "fresh", "completeness": "complete", "collection_status": "collected", "owned_metadata_only": True,
        "sufficiency": "sufficient", "relevance": "relevant", "period_coverage": "complete", "source_authenticity": "verified", "tamper_hash": "sha256:tamper", "completeness_score": 0.96, "exception_flags": (), "reviewer_notes": "accepted", "completion_gate": "open",
        "monitoring_mode": "continuous", "subscribed_event_types": tuple(DOMAIN_CONSUMED_EVENTS), "assertion_expression": "segregation_preserved", "observation_result": "passed", "exception_policy": "open_exception_on_fail", "evidence_trail": ("evt-1",), "failure_route": "triage",
        "risk_rating": "high", "population_size": 1000, "anomaly_score": 0.12, "failure_history": "low", "regulatory_importance": "key", "confidence_level": 0.95, "sample_size": 75, "sampling_rationale": "risk weighted", "auditor_override": "not_used",
        "test_steps": ("step1", "step2"), "evidence_checklist": ("approval", "timestamp"), "sample_list": ("sample-1",), "pass_fail_criteria": "no_exceptions", "observed_deviations": 0, "reviewer_comments": "clear", "retest_tasks": (), "final_conclusion": "effective", "tester_identity": "tester-1",
        "campaign_scope": "SOX-Q2", "attestor_role": "control_owner", "control_set": ("ctrl-1",), "certification_text": "I certify", "evidence_summary": "complete", "known_exceptions": (), "delegation_rules": "approved_delegate_only", "reminders": "sent", "legal_acknowledgement": True, "late_response_status": "none",
        "owner_history": ("owner-a",), "delegate_authority": "documented", "backup_owner": "backup-owner", "segregation_rules": "preserved", "role_requirements": ("risk_owner",), "vacancy_alert": False, "independence_preserved": True,
        "exception_type": "operating_failure", "exposure": "medium", "materiality": "non_material", "compensating_control": "manager_review", "risk_acceptance": "not_required", "expiry": "2026-09-30", "approval_chain": ("owner", "risk"), "retest_requirement": True, "residual_risk_impact": "moderate",
        "realized_risk": "risk-1", "affected_controls": ("ctrl-1",), "loss_estimate": 10000, "operational_impact": "contained", "root_cause": "process_gap", "detection_method": "monitoring", "time_to_detect": "PT2H", "time_to_contain": "PT6H", "lessons_learned": "tighten workflow", "reassessment_required": True,
        "issue_severity": "high", "control_linkage": "ctrl-1", "target_state": "automated_control", "sponsor": "cfo", "milestones": ("design", "implement", "validate"), "budget": 50000, "dependencies": ("workflow",), "validation_plan": "retest", "acceptance_criteria": "no_repeat_failure",
        "action_evidence": ("ticket-1",), "completion_criteria": "implemented", "blocker_reasons": (), "due_date_changes": ("approved_extension",), "implementation_proof": "deployment-proof", "retest_schedule": "2026-07-15", "validation_owner": "assurance", "closure_approval": True,
        "approver_authority": "risk_committee", "scope": "risk-1", "duration": "P90D", "rationale": "temporary compensating control", "residual_exposure": "accepted-medium", "compensating_controls": ("manual_review",), "review_date": "2026-08-30", "revocation_triggers": ("new_incident",), "accepted_risk_flag": True,
        "heatmap_methodology": "likelihood_impact_velocity", "source_risks": ("risk-1",), "scoring_version": "score-2026.05", "appetite_overlays": "visible", "trend_arrows": "stable", "stale_data_flags": (), "drilldown_evidence": ("assessment-1",), "immutable_snapshot": True,
        "scenario_library": "enterprise_scenarios", "assumptions": ("supplier_outage",), "risk_drivers": ("single_supplier",), "control_responses": ("alternate_supplier",), "impact_ranges": {"low": 1000, "high": 100000}, "recovery_times": "PT24H", "executive_summary": "resilient", "version_comparison": "improved",
        "failed_key_control": "ctrl-1", "affected_risks": ("risk-1",), "policy_obligations": ("SOX-1",), "owners": ("owner",), "evidence_packets": ("packet-1",), "open_attestations": (), "remediations": ("rem-1",), "executive_reports": ("packet-committee",), "review_tasks": ("review-1",),
        "packet_scope": "SOX-Q2", "included_controls": ("ctrl-1",), "included_tests": ("test-1",), "evidence_hashes": ("sha256:e1",), "attestations": ("att-1",), "exceptions": (), "remediation_status": "on_track", "event_lineage": ("evt-1",), "reviewer_signoff": True, "export_manifest": "manifest.json", "integrity_proof": "sha256:packet",
        "agenda": ("top risks",), "narrative": "risk posture stable", "exhibits": ("heatmap",), "heatmaps": ("heatmap-1",), "issue_decisions": ("accept",), "voting_records": ("approved",), "action_items": ("follow-up",), "follow_up_tracking": "open", "decision_linkages": ("risk_acceptance",),
        "source_signals": ("incident", "kri"), "candidate_confidence": 0.82, "affected_objectives": ("availability",), "proposed_taxonomy": "technology", "promotion_workflow": "review", "uncertainty": "medium", "registration_plan": "draft-risk",
        "model_version": "model-1", "input_data": "lineage-documented", "validation_status": "approved", "drift_metrics": {"psi": 0.05}, "limitations": "not autonomous", "override_records": (), "posture_change_gate": "approved_models_only",
        "external_entity_reference": "vendor:123", "exposure_type": "outsourced_process", "dependency_strength": "high", "criticality": "critical", "concentration_heatmap": "visible", "scenario_impact": "moderate", "declared_projection_only": True,
        "access_policy_event": "AccessPolicyChanged", "identity_control_map": "mapped", "privileged_access_attestation": "complete", "segregation_failure": False, "access_review_failure": False, "local_observation": "passed", "evidence_record": "evidence-1",
        "obligation_source": "regulation", "clause": "SOX 404", "effective_date": "2026-05-30", "mapped_control": "ctrl-1", "test_frequency": "quarterly", "evidence_requirement": "approval_proof", "gap_status": "closed", "recommended_control": "none",
        "manual_effort": "low", "preventive_detective_balance": "balanced", "evidence_automation": "high", "monitoring_coverage": "continuous", "modernization_actions": ("increase_preventive",), "effort_reduction_estimate": "30%",
        "weighted_risk_impact": 0.9, "appetite_breach": False, "due_dates": ("2026-07-30",), "cost": 25000, "blockers": (), "expected_residual_reduction": 0.4, "funding_scenario": "approved",
        "financial_loss": 0, "non_financial_impact": "near_miss", "avoided_loss": 50000, "business_line": "finance", "insurance_recovery": 0, "control_failure": "none", "calibration_update": "scenario_adjusted",
        "breach_source": "KRI", "severity": "medium", "required_action": "mitigate", "escalation_level": "risk_committee", "committee_visibility": True, "acceptance_option": "available_with_authority", "closure_evidence": "closed", "heatmap_linkage": "updated",
        "tester": "tester-a", "control_owner": "owner-b", "remediation_owner": "owner-c", "attestor": "owner-d", "conflict_rule": "no_same_owner_tester", "approved_exception": (), "assignment_gate": "passed",
        "sensitive_partition": "investigation", "access_groups": ("legal", "risk"), "field_masking": "enabled", "export_controls": "restricted", "break_glass": "audited", "agent_restrictions": "summary_only", "audit_alerts": "enabled", "api_enforcement": "enabled",
        "source_document": "audit-report.pdf", "extracted_risks": ("risk-1",), "extracted_controls": ("ctrl-1",), "extracted_mappings": ("map-1",), "extracted_tests": ("test-1",), "affected_tables": ("enterprise_risk_controls_risk_register",), "event_plan": "AppGen-X outbox preview", "human_confirmation": True,
        "rule_version": "rule-2026.05", "simulation_scope": "all_open_risks", "historical_test_set": ("test-case-1",), "approval_workflow": "dual_approval", "rollback_plan": "restore_previous", "test_cases": ("breach", "normal"), "agent_explanation": "threshold impact summarized",
        "source_pbc": "federated_iam", "observed_event_api": "AccessPolicyChanged", "expected_invariant": "segregation_preserved", "evidence_window": "PT24H", "failure_handling": "open_exception", "owned_mutation_only": True, "appgen_event_plan": "consume_event_only",
        "failure_severity": "high", "duplicate_grouping": "grp-1", "false_positive_reason": (), "remediation_link": "rem-1", "feedback_to_rule": "threshold_adjustment",
        "source_records": ("risk-1", "control-1"), "versions": ("v1",), "timestamps": ("2026-05-30T00:00:00Z",), "transformations": ("score",), "lineage_graph": "complete", "material_output": "committee_packet", "traceability_proof": "sha256:lineage",
        "sustainability_category": "climate", "climate_scenario": "flood", "carbon_control_objective": "verified_emissions", "esg_control_mapping": "mapped", "indicator_templates": ("scope1",), "evidence_requirements": ("meter_proof",), "executive_view": "visible", "projection_freshness": "fresh",
        "changed_object": "control_frequency", "affected_mappings": ("map-1",), "affected_tests": ("test-1",), "affected_packets": ("packet-1",), "dashboards": ("heatmap",), "rules": ("risk_appetite_policy",), "external_dependencies": ("PolicyChanged",), "material_approval": True,
        "transaction_time": "2026-05-30T00:00:00Z", "valid_time": "2026-05-30", "reporting_time": "2026-Q2", "as_of_risk_scores": "available", "as_of_kri_values": "available", "as_of_control_status": "available", "as_of_exceptions": "available", "as_of_remediation": "available", "temporal_consistency": True,
        "critical_service": "payments", "dependency": "gateway", "rto_target": "PT4H", "rpo_target": "PT15M", "scenario_stress": "supplier_outage", "continuity_plan": "BCP-1", "crisis_owner": "coo", "resilience_posture_update": "updated",
        "narrative_type": "committee_summary", "source_citations": ("risk-1", "heatmap-1"), "uncertainty_disclosure": "included", "owner_approval": True, "publication_gate": "approved", "evidence_links": ("packet-1",),
        "schema_hashes": ("sha256:schema",), "migration_manifest": "001_initial.sql", "service_contract": "valid", "route_contract": "valid", "event_schemas": "valid", "handler_idempotency": "proved", "retry_dead_letter_tests": "passed", "rule_simulations": "passed", "ui_coverage": "complete", "agent_skill_manifest": "complete",
        "risk_manager_view": "visible", "control_owner_view": "visible", "tester_view": "visible", "attestor_view": "visible", "remediation_owner_view": "visible", "auditor_view": "visible", "committee_secretary_view": "visible", "executive_sponsor_view": "visible", "administrator_view": "visible", "release_evidence_status": "visible",
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and payload.get("approval_status") != "approved":
        findings.append("risk taxonomy ontology changes require approval")
    if n == 2 and payload.get("readiness_status") != "ready":
        findings.append("risk intake cannot promote incomplete draft risk")
    if n == 3 and not (payload.get("inherent_impact", 0) >= payload.get("residual_impact", 0) >= payload.get("target_impact", 0)):
        findings.append("risk assessment must separate inherent, residual, and target posture")
    if n == 4 and payload.get("simulation_result") != "pass":
        findings.append("appetite statement must simulate successfully before activation")
    if n == 5 and payload.get("quarantine_status") != "clear":
        findings.append("KRI observations that fail quality checks must be quarantined")
    if n == 6 and not payload.get("breach_drivers"):
        findings.append("early warning output requires explainable breach drivers")
    if n == 7 and not payload.get("owner"):
        findings.append("controls require accountable owner")
    if n == 8 and payload.get("coverage_gaps"):
        findings.append("control objective mapping has unresolved coverage gaps")
    if n == 9 and float(payload.get("mapping_confidence", 0)) < 0.75:
        findings.append("policy-control semantic mapping confidence below threshold")
    if n == 10 and payload.get("independence_check") != "passed":
        findings.append("control test plan failed independence check")
    if n == 11 and payload.get("owned_metadata_only") is not True:
        findings.append("automated evidence collection must store only package-owned evidence metadata")
    if n == 12 and float(payload.get("completeness_score", 0)) < 0.9:
        findings.append("evidence sufficiency score is below completion threshold")
    if n == 13 and payload.get("monitoring_mode") not in {"continuous", "hybrid"}:
        findings.append("continuous control monitoring requires continuous or hybrid mode")
    if n == 14 and not payload.get("sampling_rationale"):
        findings.append("risk-based assurance sampling requires rationale")
    if n == 15 and payload.get("final_conclusion") not in {"effective", "ineffective", "needs_retest"}:
        findings.append("control test workbench conclusion is invalid")
    if n == 16 and payload.get("legal_acknowledgement") is not True:
        findings.append("attestation requires legal acknowledgement")
    if n == 17 and payload.get("independence_preserved") is not True:
        findings.append("control owner assignment breaks independence")
    if n == 18 and not payload.get("approval_chain"):
        findings.append("control exceptions require approval chain")
    if n == 19 and payload.get("reassessment_required") is not True:
        findings.append("incidents linked to risks must trigger reassessment")
    if n == 20 and not payload.get("validation_plan"):
        findings.append("remediation issue requires validation plan")
    if n == 21 and payload.get("closure_approval") is not True:
        findings.append("remediation action cannot close without validation approval")
    if n == 22 and not payload.get("approver_authority"):
        findings.append("risk acceptance requires approving authority")
    if n == 23 and payload.get("immutable_snapshot") is not True:
        findings.append("executive heatmap must be immutable once published")
    if n == 24 and not payload.get("version_comparison"):
        findings.append("risk scenario simulation requires version comparison")
    if n == 25 and not payload.get("review_tasks"):
        findings.append("key control failure must trigger review tasks")
    if n == 26 and not payload.get("integrity_proof"):
        findings.append("assurance evidence packet requires integrity proof")
    if n == 27 and not payload.get("decision_linkages"):
        findings.append("committee packet decisions must link to risk actions")
    if n == 28 and float(payload.get("candidate_confidence", 0)) < 0.6:
        findings.append("emerging risk candidate confidence too low for promotion workflow")
    if n == 29 and payload.get("validation_status") != "approved":
        findings.append("unapproved model cannot change risk posture")
    if n == 30 and payload.get("declared_projection_only") is not True:
        findings.append("third-party concentration must use declared projections only")
    if n == 31 and (payload.get("segregation_failure") or payload.get("access_review_failure")):
        findings.append("cyber/access control coverage has unresolved failure")
    if n == 32 and payload.get("gap_status") not in {"closed", "accepted_with_authority"}:
        findings.append("regulatory obligation coverage has unresolved gap")
    if n == 33 and payload.get("monitoring_coverage") not in {"continuous", "hybrid"}:
        findings.append("control maturity score requires monitoring coverage evidence")
    if n == 34 and payload.get("expected_residual_reduction", 0) <= 0:
        findings.append("remediation prioritization requires measurable residual-risk reduction")
    if n == 35 and "lessons_learned" not in payload:
        findings.append("loss and near-miss capture requires lessons learned")
    if n == 36 and payload.get("committee_visibility") is not True:
        findings.append("appetite breach must be visible to committee when material")
    if n == 37 and payload.get("approved_exception") and payload.get("assignment_gate") != "approved_exception":
        findings.append("conflicted assurance assignment requires approved exception gate")
    if n == 38 and payload.get("api_enforcement") != "enabled":
        findings.append("sensitive risk partitions must be enforced in APIs")
    if n == 39 and payload.get("human_confirmation") is not True:
        findings.append("agent risk/control intake must require human confirmation")
    if n == 40 and not payload.get("rollback_plan"):
        findings.append("policy and control rule studio requires rollback plan")
    if n == 41 and payload.get("owned_mutation_only") is not True:
        findings.append("cross-PBC assertions may not mutate foreign PBC state")
    if n == 42 and not payload.get("feedback_to_rule"):
        findings.append("continuous failure triage must feed adjudication back into rules")
    if n == 43 and not payload.get("traceability_proof"):
        findings.append("risk lineage output requires traceability proof")
    if n == 44 and payload.get("projection_freshness") != "fresh":
        findings.append("sustainability risk projection is stale")
    if n == 45 and payload.get("material_approval") is not True:
        findings.append("material risk/control impact requires approval")
    if n == 46 and payload.get("temporal_consistency") is not True:
        findings.append("risk posture time travel requires temporal consistency")
    if n == 47 and not payload.get("continuity_plan"):
        findings.append("resilience risk links require continuity plan")
    if n == 48 and payload.get("owner_approval") is not True:
        findings.append("executive narrative cannot publish without owner approval")
    if n == 49 and payload.get("retry_dead_letter_tests") != "passed":
        findings.append("release evidence requires retry/dead-letter test proof")
    if n == 50 and not all(payload.get(field) == "visible" for field in ("risk_manager_view", "control_owner_view", "tester_view", "attestor_view", "remediation_owner_view", "auditor_view", "committee_secretary_view", "executive_sponsor_view", "administrator_view", "release_evidence_status")):
        findings.append("complete enterprise risk workbench must expose every role-specific surface")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_risk_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in RISK_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in RISK_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": RISK_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": RISK_ALLOWED_DATABASE_BACKENDS,
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


def improve1_risk_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_risk_control(capability) for capability in RISK_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.enterprise-risk-controls-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": RISK_OWNED_TABLES,
        "declared_dependencies": RISK_DECLARED_DEPENDENCIES,
        "allowed_database_backends": RISK_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": RISK_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


RISK_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_risk_control(slug, payload)) for capability in RISK_CONTROL_CAPABILITIES}
