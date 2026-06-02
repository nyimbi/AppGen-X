"""Executable improve1 controls for the Fraud Anomaly Detection PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .runtime import (
    FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
    FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
    FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES,
    FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
    FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
    FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
)
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "fraud_anomaly_detection"
EVENT_CONTRACT = "AppGen-X"
FRAUD_CONTROL_ALLOWED_DATABASE_BACKENDS = FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS
FRAUD_CONTROL_REQUIRED_EVENT_TOPIC = FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC
FRAUD_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(FRAUD_ANOMALY_DETECTION_OWNED_TABLES) + tuple(FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES) + (
    "fraud_anomaly_detection_risk_signal_envelope",
    "fraud_anomaly_detection_signal_quality_score",
    "fraud_anomaly_detection_signal_timeline_entry",
    "fraud_anomaly_detection_behavior_baseline_segment",
    "fraud_anomaly_detection_cold_start_strategy",
    "fraud_anomaly_detection_identity_graph_edge",
    "fraud_anomaly_detection_synthetic_identity_pattern",
    "fraud_anomaly_detection_device_spoofing_signal",
    "fraud_anomaly_detection_network_proxy_indicator",
    "fraud_anomaly_detection_velocity_window_definition",
    "fraud_anomaly_detection_multi_entity_velocity_correlation",
    "fraud_anomaly_detection_score_composition",
    "fraud_anomaly_detection_score_calibration_backtest",
    "fraud_anomaly_detection_rule_lifecycle",
    "fraud_anomaly_detection_counterfactual_simulation",
    "fraud_anomaly_detection_policy_aware_decision",
    "fraud_anomaly_detection_decision_explanation_ledger",
    "fraud_anomaly_detection_human_override_governance",
    "fraud_anomaly_detection_risk_case_typology",
    "fraud_anomaly_detection_analyst_queue_priority",
    "fraud_anomaly_detection_case_workspace",
    "fraud_anomaly_detection_loss_exposure_projection",
    "fraud_anomaly_detection_outcome_label_governance",
    "fraud_anomaly_detection_false_positive_management",
    "fraud_anomaly_detection_missed_fraud_review",
    "fraud_anomaly_detection_adversarial_campaign",
    "fraud_anomaly_detection_bot_pattern_signal",
    "fraud_anomaly_detection_ato_playbook",
    "fraud_anomaly_detection_payment_chargeback_intelligence",
    "fraud_anomaly_detection_refund_return_promo_abuse",
    "fraud_anomaly_detection_access_policy_change_intelligence",
    "fraud_anomaly_detection_privileged_user_anomaly",
    "fraud_anomaly_detection_tenant_region_isolation",
    "fraud_anomaly_detection_privacy_minimization_control",
    "fraud_anomaly_detection_fairness_safeguard",
    "fraud_anomaly_detection_customer_appeal_review",
    "fraud_anomaly_detection_friction_strategy",
    "fraud_anomaly_detection_threshold_recommendation",
    "fraud_anomaly_detection_rule_conflict_analysis",
    "fraud_anomaly_detection_explanation_quality_test",
    "fraud_anomaly_detection_analyst_coaching_metric",
    "fraud_anomaly_detection_operations_metric",
    "fraud_anomaly_detection_configuration_impact",
    "fraud_anomaly_detection_agent_investigation_skill",
    "fraud_anomaly_detection_semantic_signal_feature",
    "fraud_anomaly_detection_evidence_packet",
    "fraud_anomaly_detection_cross_pbc_projection_contract",
    "fraud_anomaly_detection_dead_letter_replay_operation",
    "fraud_anomaly_detection_release_evidence_pack",
    "fraud_anomaly_detection_complete_workbench_coverage",

)))
FRAUD_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES) + tuple(FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES) + (
    "RiskSignalProjected", "FraudOutcomeLabelUpdated", "ChargebackOutcomeUpdated",
    "CustomerAppealSubmitted", "ReturnsSignalProjected", "LoyaltySignalProjected",
)))
FRAUD_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in FRAUD_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in FRAUD_CONTROL_CAPABILITIES}
_SPEC_ROWS: tuple[tuple[int, str, str, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = [(1, 'Risk Signal Canonicalization and Provenance', 'risk_signal_canonicalization_and_provenance', ('fraud_anomaly_detection_risk_signal_envelope',), ('source_event', 'source_pbc', 'actor', 'entity', 'channel', 'signal_type', 'capture_time', 'received_time', 'confidence', 'provenance_hash', 'tenant', 'idempotency_key'), 'RiskSignalCanonicalizationAndProvenance', 'POST /fraud-anomaly-detection/improve1/risk_signal_canonicalization_and_provenance', ()), (2, 'Signal Quality and Trust Scoring', 'signal_quality_and_trust_scoring', ('fraud_anomaly_detection_signal_quality_score',), ('completeness', 'freshness', 'source_reliability', 'schema_validity', 'duplicate_status', 'replay_suspicion', 'confidence', 'quality_score', 'quarantine_required'), 'SignalQualityAndTrustScoring', 'POST /fraud-anomaly-detection/improve1/signal_quality_and_trust_scoring', ()), (3, 'Event-Sourced Fraud Signal Timeline', 'event_sourced_fraud_signal_timeline', ('fraud_anomaly_detection_signal_timeline_entry',), ('timeline_id', 'signal_version', 'score_version', 'rule_execution_id', 'analyst_action_id', 'decision_id', 'event_lineage', 'immutable_hash', 'projection_current'), 'EventSourcedFraudSignalTimeline', 'POST /fraud-anomaly-detection/improve1/event_sourced_fraud_signal_timeline', ()), (4, 'Behavior Baseline Segmentation', 'behavior_baseline_segmentation', ('fraud_anomaly_detection_behavior_baseline_segment',), ('segment', 'cohort', 'entity_type', 'channel', 'seasonality', 'baseline_window', 'decay_factor', 'confidence', 'drift_status', 'influencing_layer'), 'BehaviorBaselineSegmentation', 'POST /fraud-anomaly-detection/improve1/behavior_baseline_segmentation', ()), (5, 'Cold-Start Risk Handling', 'cold_start_risk_handling', ('fraud_anomaly_detection_cold_start_strategy',), ('entity_id', 'entity_type', 'cohort_baseline', 'bootstrap_threshold', 'progressive_trust', 'required_evidence', 'step_up_review', 'confidence_band', 'graduation_state'), 'ColdStartRiskHandling', 'POST /fraud-anomaly-detection/improve1/cold_start_risk_handling', ()), (6, 'Identity Link Graph Confidence', 'identity_link_graph_confidence', ('fraud_anomaly_detection_identity_graph_edge',), ('edge_type', 'source_evidence', 'confidence', 'decay', 'first_seen', 'last_seen', 'contradiction_flags', 'risk_contribution', 'cluster_id'), 'IdentityLinkGraphConfidence', 'POST /fraud-anomaly-detection/improve1/identity_link_graph_confidence', ()), (7, 'Synthetic Identity and Mule Network Detection', 'synthetic_identity_and_mule_network_detection', ('fraud_anomaly_detection_synthetic_identity_pattern',), ('thin_file_signal', 'attribute_reuse', 'credential_change_velocity', 'shared_device', 'payment_reuse', 'shipping_payment_mismatch', 'ring_expansion', 'graph_case_opened', 'evidence_bundle'), 'SyntheticIdentityAndMuleNetworkDetection', 'POST /fraud-anomaly-detection/improve1/synthetic_identity_and_mule_network_detection', ()), (8, 'Device Fingerprint Stability and Spoofing Signals', 'device_fingerprint_stability_and_spoofing_signals', ('fraud_anomaly_detection_device_spoofing_signal',), ('device_confidence', 'entropy', 'spoofing_indicators', 'emulator_hint', 'proxy_hint', 'fingerprint_drift', 'cookie_reset_pattern', 'contradictions', 'known_good_history'), 'DeviceFingerprintStabilityAndSpoofingSignals', 'POST /fraud-anomaly-detection/improve1/device_fingerprint_stability_and_spoofing_signals', ()), (9, 'Network Intelligence and Proxy Risk', 'network_intelligence_and_proxy_risk', ('fraud_anomaly_detection_network_proxy_indicator',), ('asn', 'proxy_type', 'hosting_risk', 'geolocation_confidence', 'reputation', 'impossible_travel_score', 'shared_network_context', 'historical_behavior', 'network_risk'), 'NetworkIntelligenceAndProxyRisk', 'POST /fraud-anomaly-detection/improve1/network_intelligence_and_proxy_risk', ()), (10, 'Velocity Window Library', 'velocity_window_library', ('fraud_anomaly_detection_velocity_window_definition',), ('window_key', 'time_bucket', 'sliding_window', 'threshold', 'reset_rule', 'entity_scope', 'rule_binding', 'window_state', 'decision_reference'), 'VelocityWindowLibrary', 'POST /fraud-anomaly-detection/improve1/velocity_window_library', ()), (11, 'Multi-Entity Velocity Correlation', 'multi_entity_velocity_correlation', ('fraud_anomaly_detection_multi_entity_velocity_correlation',), ('linked_identities', 'shared_devices', 'shipping_addresses', 'payment_instruments', 'network_ranges', 'rule_trigger_clusters', 'correlated_velocity', 'threshold_exceeded', 'case_opened'), 'MultiEntityVelocityCorrelation', 'POST /fraud-anomaly-detection/improve1/multi_entity_velocity_correlation', ()), (12, 'Probabilistic Anomaly Score Composition', 'probabilistic_anomaly_score_composition', ('fraud_anomaly_detection_score_composition',), ('score_components', 'posterior_probability', 'confidence_interval', 'uncertainty_drivers', 'calibration_version', 'score_decomposition', 'raw_score', 'adjusted_score', 'decision_ready_score'), 'ProbabilisticAnomalyScoreComposition', 'POST /fraud-anomaly-detection/improve1/probabilistic_anomaly_score_composition', ()), (13, 'Score Calibration and Backtesting', 'score_calibration_and_backtesting', ('fraud_anomaly_detection_score_calibration_backtest',), ('calibration_dataset', 'backtest_id', 'precision', 'recall', 'false_positive_cost', 'missed_fraud_cost', 'threshold_impact', 'approval_evidence', 'production_change_allowed'), 'ScoreCalibrationAndBacktesting', 'POST /fraud-anomaly-detection/improve1/score_calibration_and_backtesting', ()), (14, 'Fraud Rule Lifecycle Governance', 'fraud_rule_lifecycle_governance', ('fraud_anomaly_detection_rule_lifecycle',), ('rule_state', 'owner', 'allowed_event_types', 'score_adjustment_bounds', 'decision_intent', 'effective_window', 'rollback_plan', 'impact_evidence', 'activation_allowed'), 'FraudRuleLifecycleGovernance', 'POST /fraud-anomaly-detection/improve1/fraud_rule_lifecycle_governance', ()), (15, 'Counterfactual Rule Simulation', 'counterfactual_rule_simulation', ('fraud_anomaly_detection_counterfactual_simulation',), ('historical_signals', 'affected_approvals', 'affected_reviews', 'affected_denials', 'cases_opened', 'false_positives', 'losses_prevented', 'queue_load', 'live_mutation_blocked'), 'CounterfactualRuleSimulation', 'POST /fraud-anomaly-detection/improve1/counterfactual_rule_simulation', ()), (16, 'Policy-Aware Decisioning', 'policy_aware_decisioning', ('fraud_anomaly_detection_policy_aware_decision',), ('fraud_score', 'rule_intent', 'access_policy_projection', 'payment_policy', 'checkout_policy', 'regional_restrictions', 'appeal_rights', 'policy_blockers', 'human_approval_required'), 'PolicyAwareDecisioning', 'POST /fraud-anomaly-detection/improve1/policy_aware_decisioning', ('AccessPolicyChanged', 'PaymentCaptured', 'CheckoutCompleted')), (17, 'Decision Explanation Ledger', 'decision_explanation_ledger', ('fraud_anomaly_detection_decision_explanation_ledger',), ('top_factors', 'rule_hits', 'baseline_deltas', 'graph_links', 'velocity_windows', 'policy_constraints', 'uncertainty', 'model_version', 'tactic_leakage_blocked'), 'DecisionExplanationLedger', 'POST /fraud-anomaly-detection/improve1/decision_explanation_ledger', ()), (18, 'Human Override Governance', 'human_override_governance', ('fraud_anomaly_detection_human_override_governance',), ('analyst_id', 'override_reason', 'authority', 'original_decision', 'new_decision', 'evidence', 'expiration', 'review_requirement', 'outcome_feedback'), 'HumanOverrideGovernance', 'POST /fraud-anomaly-detection/improve1/human_override_governance', ()), (19, 'Risk Case Typology and Severity', 'risk_case_typology_and_severity', ('fraud_anomaly_detection_risk_case_typology',), ('case_type', 'severity', 'affected_entities', 'suspected_tactic', 'urgency', 'queue', 'financial_exposure', 'customer_impact', 'required_playbook'), 'RiskCaseTypologyAndSeverity', 'POST /fraud-anomaly-detection/improve1/risk_case_typology_and_severity', ()), (20, 'Analyst Queue Prioritization', 'analyst_queue_prioritization', ('fraud_anomaly_detection_analyst_queue_priority',), ('priority_score', 'due_time', 'queue_reason', 'skill_requirement', 'linked_cases', 'expected_loss', 'false_positive_risk', 'recommended_action', 'priority_explanation'), 'AnalystQueuePrioritization', 'POST /fraud-anomaly-detection/improve1/analyst_queue_prioritization', ()), (21, 'Case Investigation Workspace', 'case_investigation_workspace', ('fraud_anomaly_detection_case_workspace',), ('evidence_timeline', 'entity_graph', 'score_decomposition', 'rule_hits', 'related_cases', 'communications', 'analyst_notes', 'actions', 'outcome_capture'), 'CaseInvestigationWorkspace', 'POST /fraud-anomaly-detection/improve1/case_investigation_workspace', ()), (22, 'Loss Exposure Projection', 'loss_exposure_projection', ('fraud_anomaly_detection_loss_exposure_projection',), ('gross_exposure', 'probable_loss', 'recoverability', 'linked_transactions', 'customer_friction_cost', 'operational_cost', 'confidence', 'case_priority_effect', 'simulation_input'), 'LossExposureProjection', 'POST /fraud-anomaly-detection/improve1/loss_exposure_projection', ()), (23, 'Outcome Feedback and Label Governance', 'outcome_feedback_and_label_governance', ('fraud_anomaly_detection_outcome_label_governance',), ('label_source', 'confidence', 'finality', 'dispute_status', 'label_delay', 'reviewer', 'contradiction_handling', 'backtest_eligible', 'model_governance_link'), 'OutcomeFeedbackAndLabelGovernance', 'POST /fraud-anomaly-detection/improve1/outcome_feedback_and_label_governance', ()), (24, 'False Positive Management', 'false_positive_management', ('fraud_anomaly_detection_false_positive_management',), ('rule_id', 'model_id', 'cohort', 'channel', 'region', 'device', 'analyst', 'decision_type', 'recovery_workflow'), 'FalsePositiveManagement', 'POST /fraud-anomaly-detection/improve1/false_positive_management', ()), (25, 'Missed Fraud and Loss Root Cause', 'missed_fraud_and_loss_root_cause', ('fraud_anomaly_detection_missed_fraud_review',), ('loss_source', 'detection_gap', 'contributing_signals', 'failed_controls', 'remediation', 'rule_change', 'model_change', 'prevention_estimate', 'configuration_backlog_link'), 'MissedFraudAndLossRootCause', 'POST /fraud-anomaly-detection/improve1/missed_fraud_and_loss_root_cause', ()), (26, 'Adversarial Drift and Attack Campaign Detection', 'adversarial_drift_and_attack_campaign_detection', ('fraud_anomaly_detection_adversarial_campaign',), ('campaign_id', 'tactic', 'entity_graph', 'network_pattern', 'device_pattern', 'timing_pattern', 'rule_evasion', 'countermeasures', 'effectiveness'), 'AdversarialDriftAndAttackCampaignDetection', 'POST /fraud-anomaly-detection/improve1/adversarial_drift_and_attack_campaign_detection', ()), (27, 'Bot and Automation Pattern Detection', 'bot_and_automation_pattern_detection', ('fraud_anomaly_detection_bot_pattern_signal',), ('timing_regularity', 'browser_automation_hint', 'interaction_speed', 'repeated_paths', 'ip_rotation', 'device_entropy', 'failure_cadence', 'campaign_case', 'specialized_queue'), 'BotAndAutomationPatternDetection', 'POST /fraud-anomaly-detection/improve1/bot_and_automation_pattern_detection', ()), (28, 'Account Takeover Playbooks', 'account_takeover_playbooks', ('fraud_anomaly_detection_ato_playbook',), ('identity_changes', 'impossible_travel', 'device_change', 'payment_change', 'unusual_checkout', 'access_event_linkage', 'containment_actions', 'customer_recovery_steps', 'declared_api_event_use'), 'AccountTakeoverPlaybooks', 'POST /fraud-anomaly-detection/improve1/account_takeover_playbooks', ('AccessPolicyChanged',)), (29, 'Payment Fraud and Chargeback Intelligence', 'payment_fraud_and_chargeback_intelligence', ('fraud_anomaly_detection_payment_chargeback_intelligence',), ('payment_projection', 'method_risk', 'auth_capture_timing', 'refund_pattern', 'chargeback_label', 'dispute_outcome', 'recovery_action', 'payment_boundary_safe', 'risk_feature_ready'), 'PaymentFraudAndChargebackIntelligence', 'POST /fraud-anomaly-detection/improve1/payment_fraud_and_chargeback_intelligence', ('PaymentCaptured',)), (30, 'Refund, Return, and Promotion Abuse Detection', 'refund_return_and_promotion_abuse_detection', ('fraud_anomaly_detection_refund_return_promo_abuse',), ('refund_frequency', 'return_reason_inconsistency', 'promotion_stacking', 'loyalty_linking', 'suspicious_reversals', 'policy_edge_behavior', 'commerce_mutation_blocked', 'risk_case_opened', 'abuse_pattern'), 'RefundReturnAndPromotionAbuseDetection', 'POST /fraud-anomaly-detection/improve1/refund_return_and_promotion_abuse_detection', ('CheckoutCompleted',)), (31, 'Access Policy Change Intelligence', 'access_policy_change_intelligence', ('fraud_anomaly_detection_access_policy_change_intelligence',), ('access_policy_event', 'actor', 'timing', 'privilege_delta', 'device', 'network', 'velocity', 'prior_behavior', 'risk_case_projection'), 'AccessPolicyChangeIntelligence', 'POST /fraud-anomaly-detection/improve1/access_policy_change_intelligence', ('AccessPolicyChanged',)), (32, 'Insider and Privileged User Anomaly Detection', 'insider_and_privileged_user_anomaly_detection', ('fraud_anomaly_detection_privileged_user_anomaly',), ('privileged_actor_baseline', 'sensitive_action_risk', 'unusual_access_path', 'separation_of_duty_signal', 'peer_group_comparison', 'human_review_required', 'impact_level', 'anomaly_score', 'case_opened'), 'InsiderAndPrivilegedUserAnomalyDetection', 'POST /fraud-anomaly-detection/improve1/insider_and_privileged_user_anomaly_detection', ()), (33, 'Tenant and Region Isolation Controls', 'tenant_and_region_isolation_controls', ('fraud_anomaly_detection_tenant_region_isolation',), ('tenant_id', 'region', 'signal_scope', 'scoring_scope', 'rule_scope', 'case_scope', 'queue_scope', 'cross_tenant_mutation_blocked', 'region_authorized'), 'TenantAndRegionIsolationControls', 'POST /fraud-anomaly-detection/improve1/tenant_and_region_isolation_controls', ()), (34, 'Privacy and Data Minimization Controls', 'privacy_and_data_minimization_controls', ('fraud_anomaly_detection_privacy_minimization_control',), ('data_category', 'masking_policy', 'retention_policy', 'purpose', 'access_policy', 'export_policy', 'deletion_policy', 'agent_redaction', 'minimization_ok'), 'PrivacyAndDataMinimizationControls', 'POST /fraud-anomaly-detection/improve1/privacy_and_data_minimization_controls', ()), (35, 'Fairness and Protected-Class Safeguards', 'fairness_and_protected_class_safeguards', ('fraud_anomaly_detection_fairness_safeguard',), ('fairness_metric', 'proxy_attribute_review', 'protected_class_exclusion', 'threshold_impact', 'appeal_tracking', 'human_review_required', 'disparate_impact_flag', 'adverse_decision_guard', 'approval_required'), 'FairnessAndProtectedClassSafeguards', 'POST /fraud-anomaly-detection/improve1/fairness_and_protected_class_safeguards', ()), (36, 'Customer Appeal and Review Workflow', 'customer_appeal_and_review_workflow', ('fraud_anomaly_detection_customer_appeal_review',), ('appeal_id', 'customer_claim', 'supporting_evidence', 'reviewer', 'original_explanation', 'decision_outcome', 'correction_actions', 'label_feedback', 'false_positive_link'), 'CustomerAppealAndReviewWorkflow', 'POST /fraud-anomaly-detection/improve1/customer_appeal_and_review_workflow', ()), (37, 'Step-Up and Friction Strategy', 'step_up_and_friction_strategy', ('fraud_anomaly_detection_friction_strategy',), ('decision_action', 'friction_strategy', 'eligibility', 'customer_impact', 'policy_basis', 'outcome_measurement', 'conversion_effect', 'loss_effect', 'strategy_allowed'), 'StepUpAndFrictionStrategy', 'POST /fraud-anomaly-detection/improve1/step_up_and_friction_strategy', ()), (38, 'Self-Healing Threshold Recommendations', 'self_healing_threshold_recommendations', ('fraud_anomaly_detection_threshold_recommendation',), ('recommendation_id', 'evidence', 'expected_loss_reduction', 'false_positive_impact', 'queue_impact', 'backtest_results', 'confidence', 'approval_workflow', 'unattended_change_blocked'), 'SelfHealingThresholdRecommendations', 'POST /fraud-anomaly-detection/improve1/self_healing_threshold_recommendations', ()), (39, 'Fraud Rule Conflict and Shadowing Detection', 'fraud_rule_conflict_and_shadowing_detection', ('fraud_anomaly_detection_rule_conflict_analysis',), ('overlapping_predicates', 'contradictory_decisions', 'redundant_triggers', 'score_saturation', 'dead_rules', 'priority_inversions', 'activation_blocked', 'conflict_report', 'reviewer_decision'), 'FraudRuleConflictAndShadowingDetection', 'POST /fraud-anomaly-detection/improve1/fraud_rule_conflict_and_shadowing_detection', ()), (40, 'Explainability Quality Testing', 'explainability_quality_testing', ('fraud_anomaly_detection_explanation_quality_test',), ('factor_accuracy', 'sensitive_tactic_leakage', 'completeness', 'role_detail_level', 'score_consistency', 'rule_consistency', 'quality_score', 'release_evidence_included', 'explanation_allowed'), 'ExplainabilityQualityTesting', 'POST /fraud-anomaly-detection/improve1/explainability_quality_testing', ()), (41, 'Analyst Performance and Coaching', 'analyst_performance_and_coaching', ('fraud_anomaly_detection_analyst_coaching_metric',), ('decision_accuracy', 'override_quality', 'review_time', 'appeal_outcomes', 'queue_complexity', 'false_positives', 'missed_fraud', 'coaching_recommendation', 'workload_balance'), 'AnalystPerformanceAndCoaching', 'POST /fraud-anomaly-detection/improve1/analyst_performance_and_coaching', ()), (42, 'Fraud Operations Metrics Layer', 'fraud_operations_metrics_layer', ('fraud_anomaly_detection_operations_metric',), ('metric_name', 'grain', 'numerator', 'denominator', 'exclusions', 'latency', 'owner', 'freshness', 'dashboard_scope'), 'FraudOperationsMetricsLayer', 'POST /fraud-anomaly-detection/improve1/fraud_operations_metrics_layer', ()), (43, 'Fraud Configuration Change Impact', 'fraud_configuration_change_impact', ('fraud_anomaly_detection_configuration_impact',), ('affected_signals', 'affected_decisions', 'affected_queues', 'loss_impact', 'false_positive_impact', 'case_volume_impact', 'fairness_impact', 'friction_impact', 'approval_required'), 'FraudConfigurationChangeImpact', 'POST /fraud-anomaly-detection/improve1/fraud_configuration_change_impact', ()), (44, 'Agent-Assisted Fraud Investigation', 'agent_assisted_fraud_investigation', ('fraud_anomaly_detection_agent_investigation_skill',), ('source_citations', 'investigation_summary', 'proposed_risk_case', 'draft_notes', 'recommended_actions', 'crud_plan', 'affected_tables', 'event_plan', 'human_confirmation'), 'AgentAssistedFraudInvestigation', 'POST /fraud-anomaly-detection/improve1/agent_assisted_fraud_investigation', ()), (45, 'Semantic Signal Interpretation', 'semantic_signal_interpretation', ('fraud_anomaly_detection_semantic_signal_feature',), ('unstructured_text', 'intent', 'tactic_hints', 'contradiction', 'urgency', 'sensitive_data_redacted', 'evidence_citations', 'confidence', 'reviewer_feedback'), 'SemanticSignalInterpretation', 'POST /fraud-anomaly-detection/improve1/semantic_signal_interpretation', ()), (46, 'Cryptographic Fraud Evidence Packets', 'cryptographic_fraud_evidence_packets', ('fraud_anomaly_detection_evidence_packet',), ('signal_hashes', 'rule_versions', 'score_decomposition', 'decision_explanation', 'case_actions', 'analyst_notes', 'event_lineage', 'export_manifest', 'redaction_profile'), 'CryptographicFraudEvidencePackets', 'POST /fraud-anomaly-detection/improve1/cryptographic_fraud_evidence_packets', ()), (47, 'Cross-PBC Boundary Proofs', 'cross_pbc_boundary_proofs', ('fraud_anomaly_detection_cross_pbc_projection_contract',), ('source_pbc', 'allowed_fields', 'freshness', 'authorization', 'idempotency', 'fallback', 'owned_mutation_only', 'appgen_runtime_tables_only', 'dependency_declared'), 'CrossPbcBoundaryProofs', 'POST /fraud-anomaly-detection/improve1/cross_pbc_boundary_proofs', ('CheckoutCompleted', 'PaymentCaptured', 'AccessPolicyChanged')), (48, 'Dead-Letter and Replay Operations', 'dead_letter_and_replay_operations', ('fraud_anomaly_detection_dead_letter_replay_operation',), ('inbox_status', 'outbox_status', 'retry_reason', 'dead_letter_reason', 'quarantine_status', 'payload_lineage', 'idempotency_key', 'replay_eligible', 'unknown_event_no_mutation'), 'DeadLetterAndReplayOperations', 'POST /fraud-anomaly-detection/improve1/dead_letter_and_replay_operations', ('CheckoutCompleted', 'PaymentCaptured', 'AccessPolicyChanged')), (49, 'Fraud Release Evidence Packs', 'fraud_release_evidence_packs', ('fraud_anomaly_detection_release_evidence_pack',), ('schema_hashes', 'migration_manifests', 'service_contracts', 'route_contracts', 'event_schemas', 'handler_idempotency_proofs', 'retry_dead_letter_tests', 'scoring_backtests', 'fairness_checks', 'ui_coverage', 'agent_manifests'), 'FraudReleaseEvidencePacks', 'POST /fraud-anomaly-detection/improve1/fraud_release_evidence_packs', ()), (50, 'Complete Fraud Workbench Coverage', 'complete_fraud_workbench_coverage', ('fraud_anomaly_detection_complete_workbench_coverage',), ('analyst_workbench', 'queue_manager_workbench', 'rule_owner_workbench', 'model_reviewer_workbench', 'compliance_reviewer_workbench', 'operations_lead_workbench', 'executive_sponsor_workbench', 'signals_coverage', 'scores_coverage', 'rules_coverage', 'cases_coverage', 'graphs_coverage', 'devices_coverage', 'networks_coverage', 'velocity_coverage', 'explanations_coverage', 'loss_coverage', 'queues_coverage', 'metrics_coverage', 'configuration_coverage', 'agent_panels_coverage', 'release_evidence_coverage'), 'CompleteFraudWorkbenchCoverage', 'POST /fraud-anomaly-detection/improve1/complete_fraud_workbench_coverage', ())]
CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"title": title, "slug": slug, "tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, title, slug, tables, fields, ui, route, deps in _SPEC_ROWS}
_EMPTY_ALLOWED_FIELDS = ("contradiction_flags", "policy_blockers", "disparate_impact_flag", "dead_letter_reason", "quarantine_status", "spoofing_indicators", "contradictions")


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
        "source_event": "CheckoutCompleted", "source_pbc": "checkout_processing", "actor": "cust-1", "entity": "checkout-1", "channel": "web", "signal_type": "checkout_velocity", "confidence": 0.86, "provenance_hash": "sha256:signal", "tenant": "tenant-a", "idempotency_key": "fraud-idem-1",
        "completeness": 1.0, "freshness": "fresh", "source_reliability": "trusted", "schema_validity": True, "duplicate_status": "unique", "replay_suspicion": False, "quality_score": 0.92, "quarantine_required": False,
        "immutable_hash": "sha256:timeline", "projection_current": True, "drift_status": "stable", "confidence_band": (0.7, 0.9), "graduation_state": "graduated",
        "edge_type": "device_account", "source_evidence": "event_lineage", "decay": "normal", "risk_contribution": 0.2, "graph_case_opened": True,
        "device_confidence": 0.82, "entropy": 0.74, "spoofing_indicators": (), "emulator_hint": False, "proxy_hint": False, "fingerprint_drift": "expected", "contradictions": (), "known_good_history": True,
        "proxy_type": "residential", "hosting_risk": "low", "geolocation_confidence": 0.88, "reputation": "neutral", "impossible_travel_score": 0.1, "network_risk": 0.18,
        "threshold": 5, "window_state": "within_limit", "correlated_velocity": 0.4, "threshold_exceeded": False, "case_opened": True,
        "posterior_probability": 0.67, "confidence_interval": (0.58, 0.75), "calibration_version": "cal-v1", "raw_score": 0.62, "adjusted_score": 0.67, "decision_ready_score": 0.67,
        "precision": 0.81, "recall": 0.76, "false_positive_cost": 120.0, "missed_fraud_cost": 450.0, "approval_evidence": "backtest-approved", "production_change_allowed": True,
        "rule_state": "approved", "score_adjustment_bounds": (-0.25, 0.25), "activation_allowed": True, "live_mutation_blocked": True,
        "human_approval_required": True, "tactic_leakage_blocked": True, "authority": "fraud_manager", "review_requirement": "required",
        "priority_score": 0.93, "expected_loss": 1200.0, "false_positive_risk": 0.12, "recommended_action": "review",
        "recoverability": 0.4, "backtest_eligible": True, "recovery_workflow": "customer_recovery", "prevention_estimate": 3500.0,
        "countermeasures": ("tighten_velocity",), "effectiveness": "monitored", "specialized_queue": "bot_ops",
        "declared_api_event_use": True, "payment_boundary_safe": True, "risk_feature_ready": True, "commerce_mutation_blocked": True,
        "privilege_delta": 0.8, "human_review_required": True, "cross_tenant_mutation_blocked": True, "region_authorized": True,
        "agent_redaction": True, "minimization_ok": True, "protected_class_exclusion": True, "adverse_decision_guard": True, "approval_required": True,
        "strategy_allowed": True, "unattended_change_blocked": True, "activation_blocked": True, "quality_score": 0.9, "sensitive_tactic_leakage": False, "explanation_allowed": True,
        "metric_name": "fraud_precision", "freshness": "fresh", "source_citations": ("signal-1", "score-1"), "human_confirmation": True,
        "sensitive_data_redacted": True, "evidence_citations": ("note-1",), "proof_verified": True, "redaction_profile": "role_scoped",
        "owned_mutation_only": True, "appgen_runtime_tables_only": True, "dependency_declared": True,
        "replay_eligible": True, "unknown_event_no_mutation": True,
        "schema_hashes": True, "migration_manifests": True, "service_contracts": True, "route_contracts": True, "event_schemas": True, "handler_idempotency_proofs": True, "retry_dead_letter_tests": True, "scoring_backtests": True, "fairness_checks": True, "ui_coverage": True, "agent_manifests": True,
        "analyst_workbench": True, "queue_manager_workbench": True, "rule_owner_workbench": True, "model_reviewer_workbench": True, "compliance_reviewer_workbench": True, "operations_lead_workbench": True, "executive_sponsor_workbench": True, "signals_coverage": True, "scores_coverage": True, "rules_coverage": True, "cases_coverage": True, "graphs_coverage": True, "devices_coverage": True, "networks_coverage": True, "velocity_coverage": True, "explanations_coverage": True, "loss_coverage": True, "queues_coverage": True, "metrics_coverage": True, "configuration_coverage": True, "agent_panels_coverage": True, "release_evidence_coverage": True,
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and (not payload.get("provenance_hash") or not payload.get("idempotency_key") or payload.get("confidence", 0) <= 0):
        findings.append("risk signal canonicalization requires provenance, confidence, and idempotency")
    if n == 2 and (payload.get("schema_validity") is not True or payload.get("duplicate_status") != "unique" or payload.get("quarantine_required") is True):
        findings.append("signal quality gate must quarantine invalid, duplicate, or suspicious signals")
    if n == 3 and (not payload.get("immutable_hash") or payload.get("projection_current") is not True):
        findings.append("fraud signal timeline requires immutable event lineage and current projection")
    if n == 6 and payload.get("confidence", 0) < 0.5:
        findings.append("identity graph links require sufficient confidence before risk contribution")
    if n == 8 and (payload.get("emulator_hint") or payload.get("proxy_hint") or payload.get("contradictions")):
        findings.append("device spoofing evidence must affect risk before decisioning")
    if n == 10 and payload.get("window_state") != "within_limit":
        findings.append("velocity window breach must be captured in decision state")
    if n == 13 and payload.get("production_change_allowed") is not True:
        findings.append("score calibration blocks production threshold change without approved backtest")
    if n == 14 and (payload.get("rule_state") not in ("approved", "active") or payload.get("activation_allowed") is not True):
        findings.append("fraud rule lifecycle blocks unapproved activation")
    if n == 15 and payload.get("live_mutation_blocked") is not True:
        findings.append("counterfactual rule simulation must be side-effect free")
    if n == 16 and payload.get("human_approval_required") is not True:
        findings.append("policy-aware decisioning requires human approval for blocked decisions")
    if n == 17 and payload.get("tactic_leakage_blocked") is not True:
        findings.append("decision explanations must not leak sensitive fraud tactics")
    if n == 20 and payload.get("priority_score", 0) <= 0:
        findings.append("analyst queue priority requires positive explainable priority")
    if n == 29 and payload.get("payment_boundary_safe") is not True:
        findings.append("payment fraud intelligence must use payment projections without mutating payment data")
    if n == 30 and payload.get("commerce_mutation_blocked") is not True:
        findings.append("refund and promotion abuse detection cannot mutate commerce domains")
    if n == 33 and (payload.get("cross_tenant_mutation_blocked") is not True or payload.get("region_authorized") is not True):
        findings.append("tenant and region isolation failed")
    if n == 34 and (payload.get("agent_redaction") is not True or payload.get("minimization_ok") is not True):
        findings.append("privacy and data minimization controls require redaction and retention governance")
    if n == 35 and (payload.get("protected_class_exclusion") is not True or payload.get("adverse_decision_guard") is not True):
        findings.append("fairness safeguards require proxy review and adverse decision guardrails")
    if n == 38 and payload.get("unattended_change_blocked") is not True:
        findings.append("self-healing threshold recommendations cannot change production unattended")
    if n == 40 and (payload.get("sensitive_tactic_leakage") or payload.get("explanation_allowed") is not True):
        findings.append("explainability quality test blocks leaky or inconsistent explanations")
    if n == 44 and (not payload.get("source_citations") or payload.get("human_confirmation") is not True):
        findings.append("agent-assisted fraud investigation requires citations and human confirmation")
    if n == 47 and (payload.get("owned_mutation_only") is not True or payload.get("appgen_runtime_tables_only") is not True or payload.get("dependency_declared") is not True):
        findings.append("cross-PBC boundary proofs require declared projections and owned mutations only")
    if n == 48 and payload.get("unknown_event_no_mutation") is not True:
        findings.append("dead-letter replay operations must not mutate state for unknown events")
    if n == 49 and not all(payload.get(field) is True for field in ("schema_hashes", "migration_manifests", "service_contracts", "route_contracts", "event_schemas", "handler_idempotency_proofs", "retry_dead_letter_tests", "scoring_backtests", "fairness_checks", "ui_coverage", "agent_manifests")):
        findings.append("fraud release evidence pack is incomplete")
    if n == 50 and not all(payload.get(field) is True for field in ("analyst_workbench", "queue_manager_workbench", "rule_owner_workbench", "model_reviewer_workbench", "compliance_reviewer_workbench", "operations_lead_workbench", "executive_sponsor_workbench", "signals_coverage", "scores_coverage", "rules_coverage", "cases_coverage", "graphs_coverage", "devices_coverage", "networks_coverage", "velocity_coverage", "explanations_coverage", "loss_coverage", "queues_coverage", "metrics_coverage", "configuration_coverage", "agent_panels_coverage", "release_evidence_coverage")):
        findings.append("complete fraud workbench coverage is incomplete")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_fraud_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in FRAUD_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in FRAUD_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": FRAUD_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": FRAUD_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_fraud_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_fraud_control(capability) for capability in FRAUD_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.fraud-anomaly-detection-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": FRAUD_CONTROL_OWNED_TABLES, "declared_dependencies": FRAUD_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": FRAUD_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": FRAUD_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


FRAUD_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_fraud_control(slug, payload)) for capability in FRAUD_CONTROL_CAPABILITIES}
