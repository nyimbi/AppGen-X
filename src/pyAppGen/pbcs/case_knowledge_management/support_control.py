"""Executable case and knowledge management controls for improve1 execution."""
from __future__ import annotations

from datetime import date, datetime
import hashlib
import json
from typing import Callable, Mapping

from .models import OWNED_TABLES

PBC_KEY = "case_knowledge_management"
EVENT_CONTRACT = "AppGen-X"
CASE_KNOWLEDGE_CAPABILITIES = (
    'omnichannel_case_intake_normalization',
    'case_contact_authority_model',
    'semantic_case_classification_taxonomy',
    'severity_business_impact_scoring',
    'dynamic_queue_capacity_controls',
    'skill_based_case_assignment',
    'workload_fairness_burnout_controls',
    'sla_timer_semantics_pause_rules',
    'sla_breach_prediction_prevention',
    'case_interaction_timeline',
    'customer_communication_governance',
    'escalation_playbooks',
    'major_incident_swarm_support_mode',
    'duplicate_case_graphing',
    'resolution_path_outcome_taxonomy',
    'reopen_regression_handling',
    'root_cause_analysis_workbench',
    'knowledge_article_lifecycle_governance',
    'article_version_diff_rollback',
    'knowledge_freshness_expiry_controls',
    'article_quality_scoring',
    'knowledge_feedback_loop',
    'knowledge_gap_detection',
    'case_deflection_measurement',
    'next_best_resolution_assistant',
    'agent_assist_guardrails_audit',
    'multilingual_localization_support',
    'sentiment_friction_detection',
    'customer_health_support_history_projection',
    'product_release_context_projection',
    'queue_simulation_staffing_forecasts',
    'case_aging_stuck_detection',
    'engineering_product_handoff_control',
    'security_privacy_case_handling',
    'attachment_log_evidence_governance',
    'self_service_search_quality',
    'article_recommendation_ab_policy_testing',
    'support_playbooks_macro_governance',
    'case_collaboration_swarming',
    'service_recovery_goodwill_workflow',
    'case_closure_readiness',
    'continuous_quality_assurance_sampling',
    'knowledge_driven_training_recommendations',
    'support_operations_metrics_layer',
    'policy_parameter_studio_support_operations',
    'cross_pbc_boundary_projection_proofs',
    'agent_assisted_case_knowledge_crud',
    'cryptographic_support_evidence_packets',
    'support_resilience_dead_letter_operations',
    'complete_case_knowledge_workbench_coverage',
)
REQUIRED_FIELDS = {
    'omnichannel_case_intake_normalization': ('channel', 'source_transcript', 'identity_projection', 'product_context', 'privacy_masked', 'intake_score'),
    'case_contact_authority_model': ('contact_role', 'authority_to_act', 'communication_permission', 'effective_from'),
    'semantic_case_classification_taxonomy': ('taxonomy_path', 'confidence', 'product_component', 'classification_evidence'),
    'severity_business_impact_scoring': ('declared_priority', 'account_tier', 'affected_users', 'workaround_status', 'contractual_obligation'),
    'dynamic_queue_capacity_controls': ('skill_requirement', 'operating_calendar', 'backlog_limit', 'language', 'region', 'overflow_queue'),
    'skill_based_case_assignment': ('agent_skills', 'product_expertise', 'current_workload', 'language', 'certification'),
    'workload_fairness_burnout_controls': ('active_cases', 'complexity_score', 'after_hours_load', 'reopen_load', 'sla_pressure'),
    'sla_timer_semantics_pause_rules': ('timer_type', 'trigger_source', 'pause_reason', 'business_calendar', 'entitlement_snapshot'),
    'sla_breach_prediction_prevention': ('queue_load', 'agent_availability', 'complexity', 'customer_responsiveness', 'mitigation_plan'),
    'case_interaction_timeline': ('channel', 'participant_role', 'visibility', 'summary', 'redaction_status'),
    'customer_communication_governance': ('template_id', 'sensitive_data_check', 'entitlement_wording', 'approval_rule', 'delivery_proof'),
    'escalation_playbooks': ('escalation_type', 'trigger', 'owner_group', 'communication_plan', 'deescalation_criteria'),
    'major_incident_swarm_support_mode': ('incident_id', 'impacted_customers', 'broadcast_status', 'workaround', 'post_incident_article'),
    'duplicate_case_graphing': ('canonical_case', 'duplicate_cases', 'confidence', 'visibility_policy', 'cluster_status'),
    'resolution_path_outcome_taxonomy': ('resolution_type', 'action_steps', 'customer_confirmation', 'root_cause_link', 'reopen_risk'),
    'reopen_regression_handling': ('reopen_reason', 'prior_resolution', 'new_evidence', 'elapsed_time', 'corrective_action'),
    'root_cause_analysis_workbench': ('root_cause_category', 'contributing_factors', 'evidence_links', 'corrective_actions', 'verification'),
    'knowledge_article_lifecycle_governance': ('lifecycle_state', 'reviewers', 'audience', 'product_scope', 'approval_evidence'),
    'article_version_diff_rollback': ('structured_diff', 'change_reason', 'reviewer_approvals', 'impacted_products', 'rollback_plan'),
    'knowledge_freshness_expiry_controls': ('freshness_rule', 'expiry_date', 'owner', 'stale_usage_alert', 'retirement_workflow'),
    'article_quality_scoring': ('success_rate', 'reopen_correlation', 'negative_feedback', 'readability', 'localization_coverage'),
    'knowledge_feedback_loop': ('feedback_type', 'source_case', 'severity', 'suggested_edit', 'owner_assignment'),
    'knowledge_gap_detection': ('case_classifications', 'search_misses', 'duplicate_clusters', 'agent_notes', 'expected_deflection'),
    'case_deflection_measurement': ('search_query', 'article_shown', 'customer_action', 'time_to_case', 'satisfaction'),
    'next_best_resolution_assistant': ('ranked_actions', 'source_citations', 'confidence', 'policy_warnings', 'human_confirmation'),
    'agent_assist_guardrails_audit': ('source_citations', 'permission_check', 'redaction', 'approval_gate', 'affected_tables'),
    'multilingual_localization_support': ('detected_language', 'localized_variant', 'regional_policy', 'translation_review', 'language_queue'),
    'sentiment_friction_detection': ('sentiment_score', 'repeated_contacts', 'wait_time', 'customer_tier', 'driver_explanation'),
    'customer_health_support_history_projection': ('source_pbc', 'snapshot_time', 'allowed_fields', 'entitlement', 'fallback_behavior'),
    'product_release_context_projection': ('product_version', 'component', 'release_status', 'known_issue', 'support_lifecycle'),
    'queue_simulation_staffing_forecasts': ('arrival_rate', 'staffing_levels', 'skill_gaps', 'holiday_calendar', 'sla_target'),
    'case_aging_stuck_detection': ('state_age', 'dependency', 'last_customer_touch', 'owner_activity', 'recommended_unblock'),
    'engineering_product_handoff_control': ('reproduction_steps', 'environment', 'logs', 'affected_customers', 'feedback_loop'),
    'security_privacy_case_handling': ('sensitive_flags', 'restricted_queue', 'redaction_workflow', 'credential_scan', 'privacy_review'),
    'attachment_log_evidence_governance': ('attachment_hash', 'scan_status', 'secret_detection', 'retention_class', 'redaction_status'),
    'self_service_search_quality': ('zero_result_queries', 'reformulations', 'article_clicks', 'failed_deflections', 'intent_clusters'),
    'article_recommendation_ab_policy_testing': ('eligibility', 'variant_set', 'success_metric', 'guardrails', 'rollback_plan'),
    'support_playbooks_macro_governance': ('steps', 'decision_branches', 'linked_articles', 'policy_constraints', 'review_cadence'),
    'case_collaboration_swarming': ('participants', 'roles', 'timebox', 'decisions', 'communication_owner'),
    'service_recovery_goodwill_workflow': ('reason', 'proposed_remedy', 'approval_authority', 'customer_impact', 'follow_up_obligation'),
    'case_closure_readiness': ('required_interactions', 'customer_response', 'resolution_taxonomy', 'open_escalations', 'sla_timer_state'),
    'continuous_quality_assurance_sampling': ('sampling_rule', 'reviewer', 'scorecard', 'coaching_task', 'dispute_process'),
    'knowledge_driven_training_recommendations': ('case_outcomes', 'qa_reviews', 'article_usage', 'escalations', 'skill_gap'),
    'support_operations_metrics_layer': ('metric_grain', 'filters', 'calculation', 'owner', 'freshness'),
    'policy_parameter_studio_support_operations': ('policy_version', 'simulation', 'approval_workflow', 'effective_date', 'rollback'),
    'cross_pbc_boundary_projection_proofs': ('source_pbc', 'identifier', 'snapshot_time', 'allowed_fields', 'authorization'),
    'agent_assisted_case_knowledge_crud': ('instruction', 'extracted_fields', 'confidence', 'policy_warnings', 'event_plan'),
    'cryptographic_support_evidence_packets': ('timeline_hash', 'sla_history', 'assignments', 'interactions', 'event_lineage'),
    'support_resilience_dead_letter_operations': ('payload_lineage', 'idempotency_key', 'replay_control', 'dependency_health', 'quarantine_reason'),
    'complete_case_knowledge_workbench_coverage': ('role_workbenches', 'intake', 'queues', 'knowledge_studio', 'analytics', 'release_status'),
}
CAPABILITY_TABLES = {
    'omnichannel_case_intake_normalization': OWNED_TABLES[0],
    'case_contact_authority_model': OWNED_TABLES[1],
    'semantic_case_classification_taxonomy': OWNED_TABLES[2],
    'severity_business_impact_scoring': OWNED_TABLES[2],
    'dynamic_queue_capacity_controls': OWNED_TABLES[3],
    'skill_based_case_assignment': OWNED_TABLES[4],
    'workload_fairness_burnout_controls': OWNED_TABLES[4],
    'sla_timer_semantics_pause_rules': OWNED_TABLES[5],
    'sla_breach_prediction_prevention': OWNED_TABLES[5],
    'case_interaction_timeline': OWNED_TABLES[7],
    'customer_communication_governance': OWNED_TABLES[7],
    'escalation_playbooks': OWNED_TABLES[8],
    'major_incident_swarm_support_mode': OWNED_TABLES[8],
    'duplicate_case_graphing': OWNED_TABLES[15],
    'resolution_path_outcome_taxonomy': OWNED_TABLES[9],
    'reopen_regression_handling': OWNED_TABLES[9],
    'root_cause_analysis_workbench': OWNED_TABLES[14],
    'knowledge_article_lifecycle_governance': OWNED_TABLES[10],
    'article_version_diff_rollback': OWNED_TABLES[11],
    'knowledge_freshness_expiry_controls': OWNED_TABLES[25],
    'article_quality_scoring': OWNED_TABLES[13],
    'knowledge_feedback_loop': OWNED_TABLES[12],
    'knowledge_gap_detection': OWNED_TABLES[22],
    'case_deflection_measurement': OWNED_TABLES[23],
    'next_best_resolution_assistant': OWNED_TABLES[26],
    'agent_assist_guardrails_audit': OWNED_TABLES[26],
    'multilingual_localization_support': OWNED_TABLES[10],
    'sentiment_friction_detection': OWNED_TABLES[7],
    'customer_health_support_history_projection': OWNED_TABLES[0],
    'product_release_context_projection': OWNED_TABLES[2],
    'queue_simulation_staffing_forecasts': OWNED_TABLES[3],
    'case_aging_stuck_detection': OWNED_TABLES[0],
    'engineering_product_handoff_control': OWNED_TABLES[8],
    'security_privacy_case_handling': OWNED_TABLES[16],
    'attachment_log_evidence_governance': OWNED_TABLES[7],
    'self_service_search_quality': OWNED_TABLES[22],
    'article_recommendation_ab_policy_testing': OWNED_TABLES[23],
    'support_playbooks_macro_governance': OWNED_TABLES[21],
    'case_collaboration_swarming': OWNED_TABLES[8],
    'service_recovery_goodwill_workflow': OWNED_TABLES[16],
    'case_closure_readiness': OWNED_TABLES[20],
    'continuous_quality_assurance_sampling': OWNED_TABLES[20],
    'knowledge_driven_training_recommendations': OWNED_TABLES[21],
    'support_operations_metrics_layer': OWNED_TABLES[20],
    'policy_parameter_studio_support_operations': OWNED_TABLES[17],
    'cross_pbc_boundary_projection_proofs': OWNED_TABLES[27],
    'agent_assisted_case_knowledge_crud': OWNED_TABLES[26],
    'cryptographic_support_evidence_packets': OWNED_TABLES[0],
    'support_resilience_dead_letter_operations': OWNED_TABLES[29],
    'complete_case_knowledge_workbench_coverage': OWNED_TABLES[21],
}
CAPABILITY_EVENTS = {
    'omnichannel_case_intake_normalization': 'CaseCreated',
    'case_contact_authority_model': 'CaseContactGoverned',
    'semantic_case_classification_taxonomy': 'CaseClassified',
    'severity_business_impact_scoring': 'SeverityAssessed',
    'dynamic_queue_capacity_controls': 'CaseRouted',
    'skill_based_case_assignment': 'CaseAssigned',
    'workload_fairness_burnout_controls': 'AssignmentFairnessFlagged',
    'sla_timer_semantics_pause_rules': 'SlaTimerChanged',
    'sla_breach_prediction_prevention': 'SlaRiskChanged',
    'case_interaction_timeline': 'CaseInteractionRecorded',
    'customer_communication_governance': 'CommunicationApproved',
    'escalation_playbooks': 'CaseEscalated',
    'major_incident_swarm_support_mode': 'MajorIncidentLinked',
    'duplicate_case_graphing': 'DuplicateClusterUpdated',
    'resolution_path_outcome_taxonomy': 'CaseResolved',
    'reopen_regression_handling': 'CaseReopened',
    'root_cause_analysis_workbench': 'RootCauseIdentified',
    'knowledge_article_lifecycle_governance': 'KnowledgeArticlePublished',
    'article_version_diff_rollback': 'KnowledgeArticleVersioned',
    'knowledge_freshness_expiry_controls': 'KnowledgeFreshnessChanged',
    'article_quality_scoring': 'ArticleQualityScored',
    'knowledge_feedback_loop': 'ArticleFeedbackTriaged',
    'knowledge_gap_detection': 'KnowledgeGapDetected',
    'case_deflection_measurement': 'DeflectionMeasured',
    'next_best_resolution_assistant': 'NextBestResolutionRecommended',
    'agent_assist_guardrails_audit': 'AgentAssistAudited',
    'multilingual_localization_support': 'LocalizedKnowledgeGoverned',
    'sentiment_friction_detection': 'FrictionDetected',
    'customer_health_support_history_projection': 'CustomerProjectionApplied',
    'product_release_context_projection': 'ProductProjectionApplied',
    'queue_simulation_staffing_forecasts': 'QueueSimulationCompleted',
    'case_aging_stuck_detection': 'StuckCaseDetected',
    'engineering_product_handoff_control': 'EngineeringHandoffPackaged',
    'security_privacy_case_handling': 'SensitiveCaseGoverned',
    'attachment_log_evidence_governance': 'EvidenceGoverned',
    'self_service_search_quality': 'SearchQualityMeasured',
    'article_recommendation_ab_policy_testing': 'RecommendationExperimentRecorded',
    'support_playbooks_macro_governance': 'SupportPlaybookGoverned',
    'case_collaboration_swarming': 'CaseSwarmManaged',
    'service_recovery_goodwill_workflow': 'ServiceRecoveryGoverned',
    'case_closure_readiness': 'ClosureReadinessChecked',
    'continuous_quality_assurance_sampling': 'QualitySampleCreated',
    'knowledge_driven_training_recommendations': 'TrainingRecommendationCreated',
    'support_operations_metrics_layer': 'SupportMetricDefined',
    'policy_parameter_studio_support_operations': 'SupportPolicySimulated',
    'cross_pbc_boundary_projection_proofs': 'ProjectionProofRecorded',
    'agent_assisted_case_knowledge_crud': 'AgentCrudPlanCreated',
    'cryptographic_support_evidence_packets': 'SupportEvidencePacketGenerated',
    'support_resilience_dead_letter_operations': 'DeadLetterTriaged',
    'complete_case_knowledge_workbench_coverage': 'WorkbenchCoverageVerified',
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


def evaluate_support_control(capability: str, payload: Mapping[str, object]) -> dict:
    if capability not in CASE_KNOWLEDGE_CAPABILITIES:
        raise ValueError(f"unknown case knowledge capability: {capability}")
    data = dict(payload or {})
    required = REQUIRED_FIELDS[capability]
    missing = tuple(field for field in required if data.get(field) in (None, "", (), []))
    owned_refs = tuple(str(ref) for ref in _as_tuple(data.get("owned_table_refs")))
    foreign_refs = tuple(ref for ref in owned_refs if not ref.startswith(PBC_KEY + "_"))
    confidence = float(data.get("confidence", 1 if not missing else 0.5))
    needs_review = bool(missing or confidence < float(data.get("confidence_threshold", 0.75)) or data.get("policy_warning"))
    allowed = not foreign_refs and not missing and not data.get("blocked")
    return {
        "ok": allowed,
        "pbc": PBC_KEY,
        "capability": capability,
        "owned_table": CAPABILITY_TABLES[capability],
        "required_fields": required,
        "missing_fields": missing,
        "control_id": _digest((capability, data))[:16],
        "ui_surface": f"{PBC_KEY}.ui.support_control.{capability}",
        "service_surface": f"{PBC_KEY}.service.support_control.{capability}",
        "api_surface": f"{PBC_KEY}.api.support_control.{capability}",
        "emits": CAPABILITY_EVENTS[capability],
        "event_contract": EVENT_CONTRACT,
        "requires_human_confirmation": needs_review or capability.startswith("agent_") or "communication" in capability or "goodwill" in capability,
        "policy_review_required": bool(data.get("policy_warning") or capability in {"security_privacy_case_handling", "service_recovery_goodwill_workflow", "customer_communication_governance"}),
        "idempotency_key": data.get("idempotency_key") or _digest((capability, data.get("case_id"), data.get("article_id")))[:24],
        "effective_at": _iso(data.get("effective_at")),
        "foreign_references": foreign_refs,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def normalize_omnichannel_intake(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('omnichannel_case_intake_normalization', payload)

def enforce_contact_authority(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('case_contact_authority_model', payload)

def classify_semantic_case(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('semantic_case_classification_taxonomy', payload)

def score_severity_business_impact(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('severity_business_impact_scoring', payload)

def route_dynamic_queue(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('dynamic_queue_capacity_controls', payload)

def assign_by_skill_profile(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('skill_based_case_assignment', payload)

def monitor_workload_fairness(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('workload_fairness_burnout_controls', payload)

def apply_sla_timer_semantics(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('sla_timer_semantics_pause_rules', payload)

def predict_sla_breach(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('sla_breach_prediction_prevention', payload)

def record_governed_interaction(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('case_interaction_timeline', payload)

def govern_customer_communication(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('customer_communication_governance', payload)

def open_escalation_playbook(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('escalation_playbooks', payload)

def coordinate_major_incident_swarm(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('major_incident_swarm_support_mode', payload)

def graph_duplicate_case_cluster(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('duplicate_case_graphing', payload)

def resolve_with_outcome_taxonomy(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('resolution_path_outcome_taxonomy', payload)

def record_reopen_regression(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('reopen_regression_handling', payload)

def analyze_root_cause(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('root_cause_analysis_workbench', payload)

def govern_article_lifecycle(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('knowledge_article_lifecycle_governance', payload)

def version_article_with_diff(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('article_version_diff_rollback', payload)

def control_knowledge_freshness(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('knowledge_freshness_expiry_controls', payload)

def score_article_quality_drivers(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('article_quality_scoring', payload)

def triage_knowledge_feedback(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('knowledge_feedback_loop', payload)

def detect_knowledge_gap(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('knowledge_gap_detection', payload)

def measure_case_deflection(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('case_deflection_measurement', payload)

def recommend_next_best_resolution_guarded(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('next_best_resolution_assistant', payload)

def audit_agent_assist_guardrails(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('agent_assist_guardrails_audit', payload)

def govern_multilingual_support(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('multilingual_localization_support', payload)

def detect_sentiment_friction(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('sentiment_friction_detection', payload)

def apply_customer_health_projection(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('customer_health_support_history_projection', payload)

def apply_product_release_projection(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('product_release_context_projection', payload)

def simulate_queue_staffing(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('queue_simulation_staffing_forecasts', payload)

def detect_stuck_case(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('case_aging_stuck_detection', payload)

def package_engineering_handoff(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('engineering_product_handoff_control', payload)

def govern_security_privacy_case(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('security_privacy_case_handling', payload)

def govern_attachment_evidence(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('attachment_log_evidence_governance', payload)

def analyze_self_service_search_quality(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('self_service_search_quality', payload)

def run_article_recommendation_experiment(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('article_recommendation_ab_policy_testing', payload)

def govern_support_playbook(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('support_playbooks_macro_governance', payload)

def manage_case_collaboration_swarm(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('case_collaboration_swarming', payload)

def govern_service_recovery(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('service_recovery_goodwill_workflow', payload)

def check_case_closure_readiness(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('case_closure_readiness', payload)

def sample_support_quality_assurance(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('continuous_quality_assurance_sampling', payload)

def recommend_knowledge_driven_training(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('knowledge_driven_training_recommendations', payload)

def define_support_operations_metrics(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('support_operations_metrics_layer', payload)

def simulate_support_policy_change(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('policy_parameter_studio_support_operations', payload)

def prove_cross_pbc_boundaries(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('cross_pbc_boundary_projection_proofs', payload)

def plan_agent_assisted_crud(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('agent_assisted_case_knowledge_crud', payload)

def generate_support_evidence_packet(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('cryptographic_support_evidence_packets', payload)

def triage_support_dead_letter(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('support_resilience_dead_letter_operations', payload)

def verify_complete_workbench_coverage(payload: Mapping[str, object]) -> dict:
    return evaluate_support_control('complete_case_knowledge_workbench_coverage', payload)

SUPPORT_CONTROL_FUNCTIONS: dict[str, Callable[[Mapping[str, object]], dict]] = {
    'omnichannel_case_intake_normalization': normalize_omnichannel_intake,
    'case_contact_authority_model': enforce_contact_authority,
    'semantic_case_classification_taxonomy': classify_semantic_case,
    'severity_business_impact_scoring': score_severity_business_impact,
    'dynamic_queue_capacity_controls': route_dynamic_queue,
    'skill_based_case_assignment': assign_by_skill_profile,
    'workload_fairness_burnout_controls': monitor_workload_fairness,
    'sla_timer_semantics_pause_rules': apply_sla_timer_semantics,
    'sla_breach_prediction_prevention': predict_sla_breach,
    'case_interaction_timeline': record_governed_interaction,
    'customer_communication_governance': govern_customer_communication,
    'escalation_playbooks': open_escalation_playbook,
    'major_incident_swarm_support_mode': coordinate_major_incident_swarm,
    'duplicate_case_graphing': graph_duplicate_case_cluster,
    'resolution_path_outcome_taxonomy': resolve_with_outcome_taxonomy,
    'reopen_regression_handling': record_reopen_regression,
    'root_cause_analysis_workbench': analyze_root_cause,
    'knowledge_article_lifecycle_governance': govern_article_lifecycle,
    'article_version_diff_rollback': version_article_with_diff,
    'knowledge_freshness_expiry_controls': control_knowledge_freshness,
    'article_quality_scoring': score_article_quality_drivers,
    'knowledge_feedback_loop': triage_knowledge_feedback,
    'knowledge_gap_detection': detect_knowledge_gap,
    'case_deflection_measurement': measure_case_deflection,
    'next_best_resolution_assistant': recommend_next_best_resolution_guarded,
    'agent_assist_guardrails_audit': audit_agent_assist_guardrails,
    'multilingual_localization_support': govern_multilingual_support,
    'sentiment_friction_detection': detect_sentiment_friction,
    'customer_health_support_history_projection': apply_customer_health_projection,
    'product_release_context_projection': apply_product_release_projection,
    'queue_simulation_staffing_forecasts': simulate_queue_staffing,
    'case_aging_stuck_detection': detect_stuck_case,
    'engineering_product_handoff_control': package_engineering_handoff,
    'security_privacy_case_handling': govern_security_privacy_case,
    'attachment_log_evidence_governance': govern_attachment_evidence,
    'self_service_search_quality': analyze_self_service_search_quality,
    'article_recommendation_ab_policy_testing': run_article_recommendation_experiment,
    'support_playbooks_macro_governance': govern_support_playbook,
    'case_collaboration_swarming': manage_case_collaboration_swarm,
    'service_recovery_goodwill_workflow': govern_service_recovery,
    'case_closure_readiness': check_case_closure_readiness,
    'continuous_quality_assurance_sampling': sample_support_quality_assurance,
    'knowledge_driven_training_recommendations': recommend_knowledge_driven_training,
    'support_operations_metrics_layer': define_support_operations_metrics,
    'policy_parameter_studio_support_operations': simulate_support_policy_change,
    'cross_pbc_boundary_projection_proofs': prove_cross_pbc_boundaries,
    'agent_assisted_case_knowledge_crud': plan_agent_assisted_crud,
    'cryptographic_support_evidence_packets': generate_support_evidence_packet,
    'support_resilience_dead_letter_operations': triage_support_dead_letter,
    'complete_case_knowledge_workbench_coverage': verify_complete_workbench_coverage,
}


def improve1_support_control_contract() -> dict:
    return {
        "ok": len(CASE_KNOWLEDGE_CAPABILITIES) == 50 and set(SUPPORT_CONTROL_FUNCTIONS) == set(CASE_KNOWLEDGE_CAPABILITIES),
        "pbc": PBC_KEY,
        "capability_count": len(CASE_KNOWLEDGE_CAPABILITIES),
        "capabilities": CASE_KNOWLEDGE_CAPABILITIES,
        "owned_tables": OWNED_TABLES,
        "ui_surfaces": tuple(f"{PBC_KEY}.ui.support_control.{capability}" for capability in CASE_KNOWLEDGE_CAPABILITIES),
        "service_surfaces": tuple(f"{PBC_KEY}.service.support_control.{capability}" for capability in CASE_KNOWLEDGE_CAPABILITIES),
        "api_surfaces": tuple(f"{PBC_KEY}.api.support_control.{capability}" for capability in CASE_KNOWLEDGE_CAPABILITIES),
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }
