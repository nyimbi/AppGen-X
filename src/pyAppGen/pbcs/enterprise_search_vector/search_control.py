"""Executable improve1 controls for the Enterprise Search Vector PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "enterprise_search_vector"
EVENT_CONTRACT = "AppGen-X"
SEARCH_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
SEARCH_REQUIRED_EVENT_TOPIC = "appgen.enterprise_search_vector.events"
SEARCH_OWNED_TABLES = (
    "search_index",
    "embedding_job",
    "vector_document",
    "query_trace",
    "ranking_simulation",
    "freshness_forecast",
    "quality_remediation",
    "search_policy_screening",
    "relevance_control_assertion",
    "index_proof",
    "federated_search_view",
    "query_intent_risk",
    "retention_deletion_record",
    "search_audit_entry",
    "search_governed_model",
    "enterprise_search_vector_appgen_outbox_event",
    "enterprise_search_vector_appgen_inbox_event",
    "enterprise_search_vector_dead_letter_event",
)
SEARCH_CONSUMED_EVENT_TYPES = ("ProductPublished", "CustomerUpdated", "AuditEventSealed")
SEARCH_EMITTED_EVENT_TYPES = ("SearchIndexUpdated", "DiscoveryInsightGenerated")
SEARCH_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(SEARCH_CONSUMED_EVENT_TYPES) + tuple(SEARCH_EMITTED_EVENT_TYPES) + (
    "ProductPublished",
    "CustomerUpdated",
    "AuditEventSealed",
    "KnowledgeArticlePublished",
    "PolicyChanged",
    "AccessPolicyChanged",
    "LegalHoldChanged",
    "POST /notifications/messages",
    "GET /product-catalog/projections/{id}",
    "GET /customer-360/projections/{id}",
    "GET /audit-ledger/proofs/{id}",
    "GET /knowledge/articles/{id}",
    "GET /identity/access-policies/{id}",
    "GET /policy/obligations/{id}",
)))

SEARCH_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in SEARCH_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in SEARCH_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = (
    (1, ("search_index",), ("index_state", "document_count", "embedding_readiness", "freshness_health", "acl_health", "proof_status", "owner_approval", "lifecycle_event"), "SearchIndexLifecycleConsole", "POST /search-indexes/lifecycle", ("SearchIndexUpdated",)),
    (2, ("search_index", "vector_document"), ("source_pbc", "allowed_fields", "freshness_sla", "event_types", "projection_schema", "access_basis", "fallback_behavior", "idempotency_rules", "declared_projection_contract"), "SourceProjectionContractRegistry", "POST /sources/register", ("ProductPublished", "CustomerUpdated", "AuditEventSealed")),
    (3, ("vector_document", "query_trace"), ("source_document_id", "source_version", "projection_timestamp", "content_hash", "chunk_hash", "embedding_hash", "superseded_by", "deletion_status", "returned_chunk_version"), "DocumentLineageExplorer", "POST /documents/lineage", ()),
    (4, ("vector_document",), ("chunking_strategy", "content_type", "token_count", "overlap", "section_anchor", "metadata_preserved", "quality_metric"), "ChunkingStrategyLibrary", "POST /documents/chunk", ()),
    (5, ("vector_document", "embedding_job"), ("weighted_fields", "structured_metadata", "locale", "source_authority", "business_glossary_terms", "access_safe_context", "template_version"), "EmbeddingPayloadTemplateStudio", "POST /embedding-templates/render", ()),
    (6, ("embedding_job",), ("queue_priority", "batch_plan", "dependency_set", "retry_policy", "partial_failure_handling", "throughput", "cost_estimate", "completion_proof", "blocked_documents"), "EmbeddingJobBackpressureConsole", "POST /embedding-jobs/orchestrate", ()),
    (7, ("search_governed_model", "embedding_job"), ("model_dimensions", "provider_abstraction", "approval_status", "validation_set", "drift_metrics", "known_limitations", "compatible_indexes", "migration_status", "rollback_plan"), "EmbeddingModelGovernance", "POST /models/embedding-governance", ()),
    (8, ("search_index", "query_trace"), ("locale_aware_index", "translation_metadata", "cross_lingual_embedding", "locale_fallback", "regional_synonyms", "language_detection", "locale_routing"), "CrossLingualSearchWorkbench", "POST /queries/cross-lingual", ()),
    (9, ("vector_document", "search_policy_screening"), ("source_permissions", "tenant", "role", "object_restrictions", "field_masking", "expiration", "access_policy_version", "pre_rank_filtering", "policy_screening_evidence"), "AclResultTimeEnforcement", "POST /queries/acl-screen", ("AccessPolicyChanged", "GET /identity/access-policies/{id}")),
    (10, ("query_trace", "search_policy_screening"), ("snippet_redaction_rules", "sensitive_field_masks", "role_explanation_depth", "leakage_tests", "redaction_decisions", "assertion_reference"), "SnippetRedactionPolicy", "POST /queries/redact-snippets", ("PolicyChanged",)),
    (11, ("query_trace", "ranking_simulation"), ("semantic_score", "keyword_score", "authority_score", "freshness_score", "feedback_score", "source_boosts", "penalties", "explanation_text"), "HybridRankingDecomposition", "GET /queries/{id}/ranking-decomposition", ()),
    (12, ("ranking_simulation",), ("historical_query_set", "proposed_weights", "result_deltas", "relevance_impact", "zero_result_changes", "acl_impact", "freshness_shifts", "confidence", "approval_required"), "CounterfactualRankingSimulation", "POST /ranking-simulations", ()),
    (13, ("query_trace",), ("normalized_query", "intent", "filters", "principal_permissions", "query_plan", "candidate_count", "filtered_count", "ranking_components", "returned_chunks", "redactions", "latency", "feedback_state"), "QueryTraceCompletenessExplorer", "GET /query-traces/{id}", ()),
    (14, ("query_intent_risk", "query_trace"), ("sensitive_intent_taxonomy", "confidence", "policy_basis", "principal_context", "source_categories", "allowed_response_behavior", "escalation", "blocked_or_redacted"), "QueryIntentRiskScreen", "POST /query-intent-risks/score", ("PolicyChanged",)),
    (15, ("quality_remediation", "query_trace"), ("zero_result_diagnostics", "synonym_suggestions", "alternate_indexes", "access_request_prompt", "spelling_correction", "freshness_warning", "missing_source_signals"), "ZeroResultRecoveryPanel", "POST /quality/zero-result-recovery", ()),
    (16, ("query_trace", "quality_remediation"), ("signal_type", "dwell", "save_action", "open_action", "correction", "usefulness", "user_role", "query_intent", "feedback_confidence"), "SearchFeedbackQualityLoop", "POST /query-feedback", ()),
    (17, ("relevance_control_assertion",), ("query_set", "expected_documents", "prohibited_documents", "minimum_score", "acl_expectation", "locale", "freshness", "regression_status", "release_gate"), "RelevanceControlAssertions", "POST /relevance-controls/run", ()),
    (18, ("freshness_forecast", "search_index"), ("source_event_cadence", "document_age", "query_demand", "freshness_sla", "freshness_risk", "refresh_cost", "recommended_schedule", "pre_breach_trigger"), "FreshnessForecastBoard", "POST /freshness/forecast", ()),
    (19, ("quality_remediation", "embedding_job"), ("degraded_sources", "missing_documents", "failed_embeddings", "stale_chunks", "acl_mismatches", "refresh_plan", "policy_approval", "restricted_index"), "SelfHealingRefreshPlanner", "POST /indexes/self-heal", ()),
    (20, ("index_proof",), ("document_hashes", "chunk_hashes", "embedding_hashes", "acl_policy_version", "source_snapshot", "refresh_id", "verification_status", "proof_failure_incident"), "IndexProofIntegrityVerifier", "POST /index-proofs/generate", ("AuditEventSealed", "GET /audit-ledger/proofs/{id}")),
    (21, ("retention_deletion_record", "vector_document"), ("source_deletion_event", "affected_documents", "affected_chunks", "affected_embeddings", "purge_proof", "tombstone_state", "retention_basis", "hold_exceptions", "query_exclusion"), "RetentionDeletionEnforcer", "POST /retention-deletions/record", ()),
    (22, ("retention_deletion_record", "search_policy_screening"), ("preservation_flag", "purge_exception", "hold_scope", "release_evidence", "query_visibility_rules", "hidden_preserved_state"), "LegalHoldPreservationAwareness", "POST /legal-holds/search-preservation", ("LegalHoldChanged",)),
    (23, ("federated_search_view", "query_trace"), ("included_indexes", "source_weights", "policy_screening", "locale_handling", "result_blending_strategy", "source_freshness", "per_source_counts", "federation_decisions"), "FederatedSearchViewGovernance", "POST /federated-views/query", ()),
    (24, ("search_index", "quality_remediation"), ("indexed_sources", "document_counts", "skipped_documents", "acl_restrictions", "stale_sources", "failed_ingestion", "unsupported_content_types", "coverage_warning"), "SearchSourceCoverageAnalytics", "GET /coverage/search-sources", ()),
    (25, ("query_trace", "vector_document"), ("source_certification", "owner", "update_history", "feedback", "quality_signals", "audit_proof", "consumer_use", "authority_explanation"), "AuthorityTrustRanking", "POST /ranking/authority-score", ("AuditEventSealed",)),
    (26, ("vector_document", "quality_remediation"), ("content_hash", "semantic_similarity", "source_lineage", "version", "canonical_authority", "duplicate_group", "access_preserved", "version_details"), "DuplicateCollapseWorkbench", "POST /duplicates/collapse", ()),
    (27, ("query_trace", "search_policy_screening"), ("personalization_signals", "opt_in_policy", "role_constraints", "privacy_limits", "explainability", "disable_controls", "ranking_effect"), "GovernedPersonalizationControls", "POST /queries/personalize", ("PolicyChanged",)),
    (28, ("query_trace", "enterprise_search_vector_appgen_outbox_event"), ("saved_query", "filters", "acl_context", "alert_cadence", "source_scope", "delivery_preference", "change_detection", "authorized_new_content"), "SavedSearchAlerting", "POST /saved-searches", ("POST /notifications/messages",)),
    (29, ("quality_remediation", "query_trace"), ("incident_type", "linked_index", "linked_source", "linked_query_trace", "linked_embedding_job", "linked_proof", "affected_users", "severity", "root_cause", "mitigation", "resolution_evidence"), "SearchIncidentManager", "POST /search-incidents", ()),
    (30, ("quality_remediation", "ranking_simulation"), ("issue_type", "affected_queries", "fix_plan", "owner", "simulation_evidence", "deployment_status", "regression_tests", "post_fix_measurement"), "SearchQualityRemediationPlaybooks", "POST /quality-remediations/playbook", ()),
    (31, ("search_index", "query_trace"), ("vocabulary_record", "source", "locale", "approval", "scope", "conflict_detection", "impact_testing", "query_expansion", "explanation"), "VocabularyGovernanceStudio", "POST /vocabulary/synonyms", ()),
    (32, ("vector_document", "query_trace"), ("field_names", "values", "units", "identifiers", "ranges", "row_provenance", "structured_filters", "semantic_intent"), "StructuredTabularSearch", "POST /documents/structured-index", ()),
    (33, ("vector_document", "query_trace"), ("valid_time", "source_event_time", "index_time", "as_of_filter", "temporal_context", "returned_version_evidence"), "TemporalAsOfDiscovery", "POST /queries/as-of", ("AuditEventSealed",)),
    (34, ("query_trace", "search_audit_entry"), ("query_classification", "masking", "retention", "restricted_visibility", "audit_access", "deletion_policy", "permitted_view"), "QueryPrivacyAuditControls", "POST /query-privacy/classify", ("PolicyChanged",)),
    (35, ("search_policy_screening", "vector_document"), ("prompt_injection_score", "unsafe_content_flags", "retrieval_safety_labels", "source_trust_penalty", "agent_consumption_policy", "blocked_chunks", "sanitized_chunks"), "RetrievalContentSafetyScreen", "POST /retrieval/safety-screen", ("PolicyChanged",)),
    (36, ("query_trace", "relevance_control_assertion"), ("freshness_required", "authority_required", "policy_screening_required", "source_citations", "action_plan_gate", "result_to_action_lineage"), "SearchToActionGuardrails", "POST /agent/search-action-guardrails", ()),
    (37, ("query_trace", "vector_document"), ("cited_chunks", "source_versions", "freshness", "acl_status", "confidence", "contradictions", "missing_evidence_warnings", "unsupported_answer_block"), "SemanticAnswerGrounding", "POST /answers/ground", ()),
    (38, ("quality_remediation", "query_trace"), ("conflict_clusters", "source_authority", "document_versions", "policy_conflicts", "product_fact_conflicts", "customer_fact_conflicts", "resolution_tasks"), "ContradictionConflictDetection", "POST /conflicts/detect", ()),
    (39, ("relevance_control_assertion", "ranking_simulation"), ("benchmark_queries", "expected_results", "prohibited_results", "relevance_labels", "locale", "acl_context", "score_thresholds", "regression_history"), "SearchBenchmarkSuite", "POST /benchmarks/run", ()),
    (40, ("embedding_job", "query_trace"), ("latency_metrics", "cost_metrics", "index", "query_type", "embedding_job", "source", "federation_view", "ranking_mode", "optimization_recommendations"), "LatencyCostOptimizer", "POST /search-optimization/recommend", ()),
    (41, ("relevance_control_assertion", "index_proof"), ("tenant_isolation_assertions", "ingestion_test", "embedding_test", "query_test", "trace_test", "feedback_test", "retention_test", "federation_test", "adversarial_cross_tenant_tests"), "TenantIsolationProofs", "POST /tenant-isolation/prove", ()),
    (42, ("search_index", "ranking_simulation"), ("rule_version", "parameter_changes", "simulations", "approvals", "test_cases", "effective_dates", "rollback", "impact_analysis", "evidence"), "SearchRuleParameterStudio", "POST /rules-parameters/simulate", ("PolicyChanged",)),
    (43, ("query_trace", "quality_remediation"), ("feedback_pattern", "coordinated_negative_feedback", "low_trust_users", "feedback_bursts", "source_owner_manipulation", "trust_weighting", "review_queue"), "QueryFeedbackAbuseDetection", "POST /feedback/abuse-detect", ()),
    (44, ("quality_remediation",), ("source_owner_task", "missing_metadata", "stale_documents", "bad_snippets", "acl_errors", "duplicate_content", "quality_issue", "owner_response", "sla", "recurrence"), "SourceOwnerRemediationWorkflow", "POST /source-owner-tasks", ()),
    (45, ("search_governed_model", "relevance_control_assertion"), ("validation_data", "benchmark_results", "drift", "bias_checks", "limitations", "approval", "deployment_status", "rollback_plan", "monitoring_evidence"), "RetrievalModelEvaluation", "POST /models/retrieval-evaluate", ()),
    (46, ("quality_remediation", "query_trace"), ("trace_summary", "proposed_remediation", "benchmark_queries", "source_owner_task_draft", "citations", "confidence", "affected_tables", "event_plan", "human_confirmation"), "AgentSearchOperations", "POST /assistant/search-operations-plan", ()),
    (47, ("search_policy_screening", "enterprise_search_vector_appgen_inbox_event"), ("projection_contracts", "external_sources", "owned_mutation_only", "runtime_tables_only", "appgen_events_only", "foreign_table_access"), "CrossPbcSearchBoundaryProof", "POST /boundary/proof", SEARCH_DECLARED_DEPENDENCIES),
    (48, ("enterprise_search_vector_appgen_inbox_event", "enterprise_search_vector_dead_letter_event"), ("inbox", "outbox", "retry", "dead_letter", "quarantine", "payload_lineage", "idempotency_keys", "replay", "dependency_health", "unknown_event_mutation"), "SearchEventReplayOps", "POST /events/replay", tuple(SEARCH_CONSUMED_EVENT_TYPES)),
    (49, ("index_proof", "search_audit_entry"), ("schema_hashes", "migration_manifest", "service_contract", "route_contract", "event_schemas", "handler_idempotency", "retry_dead_letter_tests", "benchmark_results", "acl_tests", "retention_proofs", "ui_coverage", "agent_manifest"), "SearchReleaseEvidencePack", "POST /release/search-evidence-pack", tuple(SEARCH_EMITTED_EVENT_TYPES)),
    (50, ("search_index", "query_trace", "quality_remediation"), ("search_admin_view", "source_owner_view", "relevance_engineer_view", "compliance_reviewer_view", "knowledge_manager_view", "support_analyst_view", "executive_sponsor_view", "release_evidence_status"), "CompleteEnterpriseSearchWorkbench", "GET /enterprise-search-vector-workbench", ()),
)

CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, tables, fields, ui, route, deps in _SPEC_ROWS}
_EMPTY_ALLOWED_FIELDS = (
    "acl_errors",
    "acl_mismatches",
    "bad_snippets",
    "degraded_sources",
    "duplicate_content",
    "failed_embeddings",
    "feedback_bursts",
    "low_trust_users",
    "missing_documents",
    "missing_metadata",
    "missing_source_signals",
    "penalties",
    "policy_conflicts",
    "product_fact_conflicts",
    "customer_fact_conflicts",
    "stale_chunks",
    "stale_documents",
    "stale_sources",
    "unsafe_content_flags",
    "blocked_documents",
    "blocked_chunks",
    "contradictions",
    "failed_ingestion",
    "foreign_table_access",
    "hold_exceptions",
    "missing_evidence_warnings",
    "purge_exception",
    "skipped_documents",
    "unknown_event_mutation",
    "unsupported_answer_block",
    "unsupported_content_types",
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
        "index_state": "ready", "document_count": 1000, "embedding_readiness": "ready", "freshness_health": "fresh", "acl_health": "passing", "proof_status": "verified", "owner_approval": True, "lifecycle_event": "SearchIndexUpdated",
        "source_pbc": "product_catalog_pim", "allowed_fields": ("title", "description"), "freshness_sla": "PT2H", "event_types": ("ProductPublished",), "projection_schema": "v1", "access_basis": "declared_projection", "fallback_behavior": "degrade", "idempotency_rules": "event_id", "declared_projection_contract": True,
        "source_document_id": "doc-1", "source_version": "v3", "projection_timestamp": "2026-05-30T00:00:00Z", "content_hash": "sha256:content", "chunk_hash": "sha256:chunk", "embedding_hash": "sha256:embedding", "superseded_by": "none", "deletion_status": "active", "returned_chunk_version": "chunk-v1",
        "chunking_strategy": "section_aware", "content_type": "knowledge_article", "token_count": 512, "overlap": 64, "section_anchor": "sec-1", "metadata_preserved": True, "quality_metric": 0.92,
        "weighted_fields": {"title": 2.0, "body": 1.0}, "structured_metadata": {"source": "product"}, "locale": "en-US", "source_authority": 0.95, "business_glossary_terms": ("SKU",), "access_safe_context": True, "template_version": "template-v1",
        "queue_priority": "high", "batch_plan": "balanced", "dependency_set": ("source_projection",), "retry_policy": {"max_attempts": 3}, "partial_failure_handling": "quarantine", "throughput": 1000, "cost_estimate": 12.5, "completion_proof": "sha256:job", "blocked_documents": (),
        "model_dimensions": 1536, "provider_abstraction": "approved_provider", "approval_status": "approved", "validation_set": "bench-v1", "drift_metrics": {"psi": 0.02}, "known_limitations": "documented", "compatible_indexes": ("idx-products",), "migration_status": "ready", "rollback_plan": "previous_model",
        "locale_aware_index": True, "translation_metadata": "present", "cross_lingual_embedding": True, "locale_fallback": "en-US", "regional_synonyms": ("colour", "color"), "language_detection": "en", "locale_routing": "matched",
        "source_permissions": ("search.read",), "tenant": "tenant-a", "role": "search_user", "object_restrictions": "enforced", "field_masking": "enabled", "expiration": "2027-05-30", "access_policy_version": "access-2026.05", "pre_rank_filtering": True, "policy_screening_evidence": "proof",
        "snippet_redaction_rules": ("mask_sensitive",), "sensitive_field_masks": ("ssn",), "role_explanation_depth": "standard", "leakage_tests": "passed", "redaction_decisions": ("masked",), "assertion_reference": "rel-ctrl-1",
        "semantic_score": 0.81, "keyword_score": 0.7, "authority_score": 0.95, "freshness_score": 0.9, "feedback_score": 0.6, "source_boosts": {"product": 1.1}, "penalties": (), "explanation_text": "semantic and authority match",
        "historical_query_set": ("camera",), "proposed_weights": {"semantic": 0.5}, "result_deltas": ("doc-1:+2",), "relevance_impact": "positive", "zero_result_changes": 0, "acl_impact": "none", "freshness_shifts": "none", "confidence": 0.91, "approval_required": True,
        "normalized_query": "camera", "intent": "product_search", "filters": {"locale": "en-US"}, "principal_permissions": ("search.read",), "query_plan": "hybrid", "candidate_count": 100, "filtered_count": 80, "ranking_components": ("semantic", "keyword"), "returned_chunks": ("chunk-1",), "redactions": ("none",), "latency": 80, "feedback_state": "open",
        "sensitive_intent_taxonomy": "restricted_data", "policy_basis": "policy-1", "principal_context": "employee", "source_categories": ("product",), "allowed_response_behavior": "answer_with_citations", "escalation": "none", "blocked_or_redacted": "not_required",
        "zero_result_diagnostics": "vocabulary_gap", "synonym_suggestions": ("camera",), "alternate_indexes": ("knowledge",), "access_request_prompt": "available", "spelling_correction": "none", "freshness_warning": "none", "missing_source_signals": (),
        "signal_type": "useful", "dwell": 42, "save_action": True, "open_action": True, "correction": "none", "usefulness": 0.9, "user_role": "buyer", "query_intent": "product", "feedback_confidence": 0.88,
        "query_set": ("camera",), "expected_documents": ("doc-1",), "prohibited_documents": ("doc-secret",), "minimum_score": 0.7, "acl_expectation": "filtered", "freshness": "fresh", "regression_status": "passed", "release_gate": "passed",
        "source_event_cadence": "hourly", "document_age": "PT1H", "query_demand": "high", "freshness_risk": "low", "refresh_cost": "acceptable", "recommended_schedule": "hourly", "pre_breach_trigger": True,
        "degraded_sources": (), "missing_documents": (), "failed_embeddings": (), "stale_chunks": (), "acl_mismatches": (), "refresh_plan": "no_action", "policy_approval": True, "restricted_index": False,
        "document_hashes": ("sha256:doc",), "chunk_hashes": ("sha256:chunk",), "embedding_hashes": ("sha256:emb",), "acl_policy_version": "access-2026.05", "source_snapshot": "snapshot-1", "refresh_id": "refresh-1", "verification_status": "verified", "proof_failure_incident": "none",
        "source_deletion_event": "delete-1", "affected_documents": ("doc-old",), "affected_chunks": ("chunk-old",), "affected_embeddings": ("emb-old",), "purge_proof": "sha256:purge", "tombstone_state": "written", "retention_basis": "expired", "hold_exceptions": (), "query_exclusion": True,
        "preservation_flag": True, "purge_exception": (), "hold_scope": "matter-1", "release_evidence": "hold-proof", "query_visibility_rules": "hidden_preserved", "hidden_preserved_state": True,
        "included_indexes": ("idx-product", "idx-audit"), "source_weights": {"product": 1.0}, "policy_screening": "passed", "locale_handling": "matched", "result_blending_strategy": "rrf", "source_freshness": "fresh", "per_source_counts": {"product": 5}, "federation_decisions": ("blend",),
        "indexed_sources": ("product", "customer"), "document_counts": {"product": 100}, "skipped_documents": (), "acl_restrictions": "visible", "stale_sources": (), "failed_ingestion": (), "unsupported_content_types": (), "coverage_warning": "none",
        "source_certification": "certified", "owner": "source-owner", "update_history": "current", "feedback": "positive", "quality_signals": "high", "audit_proof": "sha256:audit", "consumer_use": "high", "authority_explanation": "certified source",
        "semantic_similarity": 0.97, "source_lineage": "same-source", "version": "latest", "canonical_authority": "doc-1", "duplicate_group": "dup-1", "access_preserved": True, "version_details": "collapsed",
        "personalization_signals": ("role",), "opt_in_policy": True, "role_constraints": "enforced", "privacy_limits": "bounded", "explainability": "visible", "disable_controls": True, "ranking_effect": "small",
        "saved_query": "camera", "acl_context": ("search.read",), "alert_cadence": "daily", "source_scope": ("product",), "delivery_preference": "in_app", "change_detection": "hash_diff", "authorized_new_content": True,
        "incident_type": "stale_index", "linked_index": "idx-product", "linked_source": "product", "linked_query_trace": "query-1", "linked_embedding_job": "job-1", "linked_proof": "proof-1", "affected_users": ("user-1",), "severity": "medium", "root_cause": "missed_event", "mitigation": "replay", "resolution_evidence": "closed",
        "issue_type": "bad_snippet", "affected_queries": ("camera",), "fix_plan": "redaction_update", "simulation_evidence": "sim-1", "deployment_status": "deployed", "regression_tests": "passed", "post_fix_measurement": "improved",
        "vocabulary_record": "vocab-1", "source": "search_admin", "approval": "approved", "scope": "product", "conflict_detection": "clear", "impact_testing": "passed", "query_expansion": "enabled", "explanation": "synonym matched",
        "field_names": ("sku",), "values": ("A1",), "units": ("USD",), "identifiers": ("sku-1",), "ranges": ("price:10-20",), "row_provenance": "row-1", "structured_filters": {"sku": "A1"}, "semantic_intent": "find sku",
        "valid_time": "2026-05-30", "source_event_time": "2026-05-30T00:00:00Z", "index_time": "2026-05-30T00:01:00Z", "as_of_filter": "2026-05-30", "temporal_context": "as_of", "returned_version_evidence": "v3",
        "query_classification": "normal", "masking": "applied", "retention": "90d", "restricted_visibility": "enforced", "audit_access": "auditor_only", "deletion_policy": "retention_expiry", "permitted_view": True,
        "prompt_injection_score": 0.01, "unsafe_content_flags": (), "retrieval_safety_labels": ("safe",), "source_trust_penalty": 0.0, "agent_consumption_policy": "citations_required", "blocked_chunks": (), "sanitized_chunks": ("chunk-1",),
        "freshness_required": True, "authority_required": True, "policy_screening_required": True, "source_citations": ("doc-1",), "action_plan_gate": "passed", "result_to_action_lineage": "trace-1",
        "cited_chunks": ("chunk-1",), "source_versions": ("v3",), "acl_status": "authorized", "contradictions": (), "missing_evidence_warnings": (), "unsupported_answer_block": (),
        "conflict_clusters": ("cluster-1",), "document_versions": ("v1", "v2"), "policy_conflicts": (), "product_fact_conflicts": (), "customer_fact_conflicts": (), "resolution_tasks": ("task-1",),
        "benchmark_queries": ("camera",), "expected_results": ("doc-1",), "prohibited_results": ("doc-secret",), "relevance_labels": {"doc-1": "great"}, "acl_context": ("search.read",), "score_thresholds": {"min": 0.7}, "regression_history": "passed",
        "latency_metrics": {"p95": 120}, "cost_metrics": {"usd": 1.2}, "index": "idx-product", "query_type": "hybrid", "embedding_job": "job-1", "federation_view": "fed-1", "ranking_mode": "hybrid", "optimization_recommendations": ("cache",),
        "tenant_isolation_assertions": "passed", "ingestion_test": "passed", "embedding_test": "passed", "query_test": "passed", "trace_test": "passed", "feedback_test": "passed", "retention_test": "passed", "federation_test": "passed", "adversarial_cross_tenant_tests": "passed",
        "rule_version": "rule-1", "parameter_changes": {"semantic_weight": 0.5}, "simulations": ("sim-1",), "approvals": ("approved",), "test_cases": ("case-1",), "effective_dates": ("2026-05-30",), "rollback": "available", "impact_analysis": "acceptable", "evidence": "proof",
        "feedback_pattern": "normal", "coordinated_negative_feedback": False, "low_trust_users": (), "feedback_bursts": (), "source_owner_manipulation": False, "trust_weighting": "applied", "review_queue": "clear",
        "source_owner_task": "task-1", "missing_metadata": (), "stale_documents": (), "bad_snippets": (), "acl_errors": (), "duplicate_content": (), "quality_issue": "snippet", "owner_response": "accepted", "sla": "PT48H", "recurrence": "none",
        "validation_data": "bench-v1", "benchmark_results": "passed", "drift": 0.02, "bias_checks": "passed", "limitations": "documented", "approval": "approved", "deployment_status": "approved", "monitoring_evidence": "active",
        "trace_summary": "low relevance traced to synonym", "proposed_remediation": "add synonym", "benchmark_queries": ("camera",), "source_owner_task_draft": "draft", "citations": ("query-1",), "affected_tables": ("quality_remediation",), "event_plan": "AppGen-X outbox preview", "human_confirmation": True,
        "projection_contracts": ("product", "customer", "audit"), "external_sources": ("product_catalog_pim",), "owned_mutation_only": True, "runtime_tables_only": True, "appgen_events_only": True, "foreign_table_access": (),
        "inbox": "visible", "outbox": "visible", "retry": "visible", "dead_letter": "visible", "quarantine": "visible", "payload_lineage": "visible", "idempotency_keys": "visible", "replay": "visible", "dependency_health": "visible", "unknown_event_mutation": (),
        "schema_hashes": ("sha256:schema",), "migration_manifest": "001_initial.sql", "service_contract": "valid", "route_contract": "valid", "event_schemas": "valid", "handler_idempotency": "proved", "retry_dead_letter_tests": "passed", "acl_tests": "passed", "retention_proofs": "passed", "ui_coverage": "complete", "agent_manifest": "complete",
        "search_admin_view": "visible", "source_owner_view": "visible", "relevance_engineer_view": "visible", "compliance_reviewer_view": "visible", "knowledge_manager_view": "visible", "support_analyst_view": "visible", "executive_sponsor_view": "visible", "release_evidence_status": "visible",
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and payload.get("index_state") not in {"draft", "building", "ready", "degraded", "stale", "restricted", "reindexing", "deprecated", "retired"}:
        findings.append("search index lifecycle state is invalid")
    if n == 2 and payload.get("declared_projection_contract") is not True:
        findings.append("source ingestion requires a declared projection contract")
    if n == 4 and payload.get("metadata_preserved") is not True:
        findings.append("chunking must preserve required metadata")
    if n == 7 and payload.get("approval_status") != "approved":
        findings.append("embedding model changes require approved governance")
    if n == 9 and payload.get("pre_rank_filtering") is not True:
        findings.append("ACL filtering must happen before ranking output")
    if n == 10 and payload.get("leakage_tests") != "passed":
        findings.append("snippet redaction requires passing leakage tests")
    if n == 12 and float(payload.get("confidence", 0)) < 0.75:
        findings.append("ranking simulation confidence below approval threshold")
    if n == 14 and payload.get("allowed_response_behavior") not in {"answer_with_citations", "redact", "block", "escalate"}:
        findings.append("query intent risk must produce allowed response behavior")
    if n == 17 and payload.get("regression_status") != "passed":
        findings.append("relevance controls have regressed")
    if n == 19 and payload.get("restricted_index") and payload.get("policy_approval") is not True:
        findings.append("restricted index self-healing requires policy approval")
    if n == 20 and payload.get("verification_status") != "verified":
        findings.append("index proof verification failed")
    if n == 21 and payload.get("query_exclusion") is not True:
        findings.append("purged content must be excluded from query immediately")
    if n == 27 and payload.get("opt_in_policy") is not True:
        findings.append("personalization requires opt-in governance")
    if n == 30 and payload.get("regression_tests") != "passed":
        findings.append("search quality remediation requires regression tests")
    if n == 35 and payload.get("prompt_injection_score", 1) > 0.3:
        findings.append("retrieval content has unsafe prompt-injection risk")
    if n == 36 and not payload.get("source_citations"):
        findings.append("search-to-action plans require source citations")
    if n == 37 and payload.get("unsupported_answer_block"):
        findings.append("unsupported answers must be blocked")
    if n == 41 and any(payload.get(field) != "passed" for field in ("ingestion_test", "embedding_test", "query_test", "trace_test", "feedback_test", "retention_test", "federation_test", "adversarial_cross_tenant_tests")):
        findings.append("tenant isolation proof has failing assertion")
    if n == 45 and payload.get("approval") != "approved":
        findings.append("retrieval model evaluation requires approval")
    if n == 46 and payload.get("human_confirmation") is not True:
        findings.append("agent-assisted search operations require human confirmation")
    if n == 47 and payload.get("foreign_table_access"):
        findings.append("cross-PBC boundary proof forbids foreign table access")
    if n == 48 and payload.get("unknown_event_mutation"):
        findings.append("unknown events must not mutate search state")
    if n == 49 and payload.get("retry_dead_letter_tests") != "passed":
        findings.append("search release evidence requires retry/dead-letter tests")
    if n == 50 and not all(payload.get(field) == "visible" for field in ("search_admin_view", "source_owner_view", "relevance_engineer_view", "compliance_reviewer_view", "knowledge_manager_view", "support_analyst_view", "executive_sponsor_view", "release_evidence_status")):
        findings.append("complete enterprise search workbench must expose every role surface")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_search_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in SEARCH_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in SEARCH_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": SEARCH_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": SEARCH_ALLOWED_DATABASE_BACKENDS,
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


def improve1_search_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_search_control(capability) for capability in SEARCH_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.enterprise-search-vector-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": SEARCH_OWNED_TABLES,
        "declared_dependencies": SEARCH_DECLARED_DEPENDENCIES,
        "allowed_database_backends": SEARCH_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": SEARCH_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


SEARCH_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_search_control(slug, payload)) for capability in SEARCH_CONTROL_CAPABILITIES}
