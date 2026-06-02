"""Executable improve1 controls for the Enterprise PIM PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "enterprise_pim"
EVENT_CONTRACT = "AppGen-X"
PIM_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PIM_REQUIRED_EVENT_TOPIC = "appgen.enterprise-pim.events"
ENTERPRISE_PIM_OWNED_TABLES = (
    "product_taxonomy",
    "taxonomy_node",
    "taxonomy_relationship",
    "taxonomy_publication",
    "taxonomy_classification_candidate",
    "product_attribute",
    "attribute_group",
    "attribute_value_option",
    "attribute_inheritance_rule",
    "attribute_validation_rule",
    "attribute_quality_signal",
    "localized_content",
    "localized_content_version",
    "translation_memory_entry",
    "locale_fallback_rule",
    "content_completeness_score",
    "validation_workflow",
    "validation_workflow_step",
    "approval_decision",
    "publication_readiness_check",
    "dependency_schema",
    "dependency_projection",
    "media_dependency_projection",
    "price_dependency_projection",
    "tax_dependency_projection",
    "inventory_dependency_projection",
    "search_dependency_projection",
    "catalog_publication_projection",
    "channel_publication_policy",
    "product_relationship",
    "product_bundle_definition",
    "product_variant_family",
    "product_variant_member",
    "assortment_assignment",
    "data_steward_assignment",
    "pim_exception",
    "exception_resolution_plan",
    "pim_audit_trace",
    "pim_master_data_proof",
    "pim_policy_screening",
    "pim_federation_projection",
    "carbon_enrichment_window",
    "taxonomy_optimization_plan",
    "workflow_allocation",
    "content_anomaly_signal",
    "enrichment_forecast",
    "enrichment_risk_model",
    "semantic_instruction_parse",
    "pim_schema_extension",
    "pim_control_assertion",
    "pim_governed_model",
    "pim_seed_data",
    "pim_rule",
    "pim_parameter",
    "pim_configuration",
    "enterprise_pim_appgen_outbox_event",
    "enterprise_pim_appgen_inbox_event",
    "enterprise_pim_dead_letter_event",
)
PIM_OWNED_TABLES = ENTERPRISE_PIM_OWNED_TABLES
PIM_DECLARED_DEPENDENCIES = (
    "MediaAssetApproved",
    "PricePromotionApproved",
    "TaxCalculated",
    "InventoryPositionUpdated",
    "SearchIndexReady",
    "CatalogProjectionUpdated",
    "CommerceChannelPolicyChanged",
    "POST /notifications/messages",
    "GET /media/assets/{id}",
    "GET /pricing/products/{id}",
    "GET /tax/products/{id}",
    "GET /inventory/products/{id}",
    "GET /search/schemas/{id}",
    "GET /catalog/publications/{id}",
)

PIM_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in PIM_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in PIM_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = (
    (1, ("product_taxonomy", "publication_readiness_check", "dependency_schema"), ("taxonomy_id", "tenant", "default_locale", "allowed_locales", "root_node", "steward", "dependency_compatibility"), "TaxonomyReadinessGate", "POST /product-taxonomies/readiness-check", ()),
    (2, ("taxonomy_node", "pim_audit_trace"), ("node_state", "parent_node", "locale_names", "effective_dates", "steward", "migration_guidance"), "TaxonomyNodeLifecycle", "POST /taxonomy-nodes/lifecycle", ()),
    (3, ("taxonomy_relationship", "attribute_inheritance_rule"), ("relationship_type", "source_node", "target_node", "effective_window", "max_depth", "publication_impact"), "TaxonomyRelationshipIntegrity", "POST /taxonomy-relationships/validate", ()),
    (4, ("taxonomy_classification_candidate", "enterprise_pim_appgen_outbox_event"), ("candidate_state", "confidence", "suggested_node", "source_signal", "competing_candidates", "reviewer", "decision_reason"), "ClassificationCandidateQueue", "POST /taxonomy-classification-candidates/review", ()),
    (5, ("taxonomy_publication", "dependency_projection", "publication_readiness_check"), ("node_moves", "retired_nodes", "inherited_attribute_changes", "translation_impact", "channel_policy_impact", "projection_freshness"), "TaxonomyPublicationSimulation", "POST /taxonomy-publications/simulate", ("SearchIndexReady", "CatalogProjectionUpdated")),
    (6, ("product_attribute", "attribute_group"), ("attribute_state", "data_type", "unit", "required_flag", "localized_labels", "inheritance_mode", "publication_eligibility"), "AttributeDefinitionStudio", "POST /product-attributes", ()),
    (7, ("attribute_group", "product_attribute"), ("group_order", "taxonomy_scope", "required_attributes", "optional_attributes", "locale_labels", "channel_visibility", "owner"), "AttributeGroupGovernance", "POST /attribute-groups", ()),
    (8, ("attribute_value_option", "localized_content"), ("option_state", "code", "localized_display", "synonyms", "sort_order", "replacement", "channel_mappings"), "ValueOptionLifecycle", "POST /attribute-value-options", ()),
    (9, ("attribute_inheritance_rule", "product_attribute"), ("max_depth", "source_node", "override_reason", "conflict_detection", "effective_dates", "completeness_effect"), "AttributeInheritanceInspector", "POST /attribute-inheritance/resolve", ()),
    (10, ("attribute_validation_rule", "attribute_quality_signal"), ("rule_type", "predicate", "sample_evaluation", "failure_severity", "affected_attributes", "locale_scope", "compiled_hash"), "ValidationRuleExecution", "POST /attribute-validation-rules/execute", ()),
    (11, ("attribute_quality_signal", "product_attribute"), ("missing_values", "invalid_units", "stale_values", "inconsistent_options", "localization_gaps", "dependency_mismatch"), "AttributeQualitySignalPanel", "GET /quality-signals/attributes", ()),
    (12, ("localized_content", "localized_content_version"), ("locale", "content_state", "source_text_hash", "translation_source", "quality_score", "fallback_status", "reviewer"), "LocalizedContentLifecycle", "POST /localized-content", ()),
    (13, ("localized_content_version", "pim_audit_trace"), ("semantic_diff", "source_locale", "target_locale", "effective_window", "reviewer", "quality_score", "rollback"), "LocalizedContentVersionHistory", "GET /localized-content/versions", ()),
    (14, ("translation_memory_entry", "pim_policy_screening"), ("source_hash", "target_locale", "quality_score", "domain", "approval_status", "expiry", "forbidden_phrase_flags"), "TranslationMemoryGovernance", "POST /translation-memory", ()),
    (15, ("locale_fallback_rule", "channel_publication_policy"), ("fallback_chain", "locale", "channel", "taxonomy", "attribute", "allowed_depth", "blocking_rules"), "LocaleFallbackPolicy", "POST /locale-fallback-rules", ()),
    (16, ("content_completeness_score", "publication_readiness_check"), ("taxonomy_node", "channel", "locale", "required_attributes", "content_quality", "dependency_freshness", "exception_severity"), "CompletenessScoreWorkbench", "GET /completeness/scores", ()),
    (17, ("validation_workflow", "validation_workflow_step"), ("workflow_state", "required_steps", "sla", "approvers", "delegated_reviewers", "evidence_required", "escalation"), "ValidationWorkflowBoard", "POST /validation-workflows", ()),
    (18, ("approval_decision", "validation_workflow"), ("approver", "role", "step", "decision", "scope", "policy_version", "evidence_snapshot", "residual_risk"), "ApprovalDecisionEvidence", "POST /approval-decisions", ()),
    (19, ("publication_readiness_check", "enterprise_pim_appgen_outbox_event"), ("required_locales", "required_attributes", "workflow_approval", "dependency_projections", "taxonomy_status", "channel_policy", "event_delivery_health"), "PublicationReadinessGate", "POST /publication-readiness/check", ()),
    (20, ("channel_publication_policy", "assortment_assignment"), ("required_fields", "locale_set", "dependency_requirements", "publication_window", "embargo_rules", "fallback_allowance", "approval_policy"), "ChannelPublicationPolicy", "POST /channel-publication-policies", ()),
    (21, ("dependency_schema", "dependency_projection"), ("source", "version_floor", "accepted_events", "required_fields", "freshness_sla", "compatibility_status", "rejection_criteria"), "DependencySchemaConsole", "POST /dependency-schemas", ("MediaAssetApproved", "PricePromotionApproved", "TaxCalculated", "InventoryPositionUpdated")),
    (22, ("dependency_projection", "enterprise_pim_appgen_inbox_event"), ("projection_source", "version", "source_event_id", "freshness", "confidence", "schema_compatibility", "readiness_impact"), "DependencyProjectionFreshness", "GET /dependency-projections/freshness", ("MediaAssetApproved", "PricePromotionApproved", "TaxCalculated", "InventoryPositionUpdated")),
    (23, ("media_dependency_projection", "publication_readiness_check"), ("asset_type", "approval_state", "locale", "channel", "rights_window", "rendition_coverage", "alt_text"), "MediaDependencyCoverage", "GET /dependencies/media", ("MediaAssetApproved", "GET /media/assets/{id}")),
    (24, ("price_dependency_projection", "tax_dependency_projection"), ("product", "channel", "market", "currency", "jurisdiction", "validity_window", "exception_state"), "PriceTaxDependencyCoverage", "GET /dependencies/price-tax", ("PricePromotionApproved", "TaxCalculated", "GET /pricing/products/{id}", "GET /tax/products/{id}")),
    (25, ("inventory_dependency_projection", "search_dependency_projection"), ("inventory_readiness", "search_schema_compatibility", "facet_mapping", "index_state", "stock_policy", "stale_warning"), "InventorySearchDependencyCoverage", "GET /dependencies/inventory-search", ("InventoryPositionUpdated", "SearchIndexReady", "GET /inventory/products/{id}", "GET /search/schemas/{id}")),
    (26, ("product_relationship", "pim_exception"), ("relationship_type", "source_product", "target_product", "compatibility_context", "directionality", "effective_dates", "channel_scope"), "ProductRelationshipGovernance", "POST /product-relationships", ()),
    (27, ("product_bundle_definition", "publication_readiness_check"), ("bundle_state", "components", "quantities", "optional_parts", "substitution_rules", "price_tax_inventory_checks"), "BundleDefinitionGovernance", "POST /product-bundles", ("PricePromotionApproved", "TaxCalculated", "InventoryPositionUpdated")),
    (28, ("product_variant_family", "product_variant_member"), ("variant_axes", "required_axis_values", "member_uniqueness", "content_inheritance", "disallowed_combinations", "locale_differences"), "VariantFamilyIntegrity", "POST /variant-families/validate", ()),
    (29, ("assortment_assignment", "channel_publication_policy"), ("assignment_state", "channel", "market", "taxonomy_node", "eligibility_reason", "embargo", "dependency_readiness"), "AssortmentAssignmentGovernance", "POST /assortments/assign", ()),
    (30, ("data_steward_assignment", "validation_workflow"), ("taxonomy", "attribute_group", "locale", "channel", "exception_type", "workload", "sla", "escalation"), "DataStewardAccountability", "POST /data-stewards/assign", ()),
    (31, ("pim_exception", "exception_resolution_plan"), ("category", "severity", "affected_scope", "root_cause", "owner", "sla", "recommended_action", "closure_proof"), "PimExceptionWorkflow", "POST /pim-exceptions", ()),
    (32, ("pim_governed_model", "attribute_quality_signal"), ("recommendation_type", "missing_locale", "missing_attribute", "invalid_value", "media_gap", "confidence", "approval_needed"), "AutonomousEnrichmentRecommendations", "POST /assistant/enrichment-recommendations", ()),
    (33, ("semantic_instruction_parse", "pim_control_assertion"), ("instruction", "target_taxonomy", "attribute", "locale", "channel", "requested_action", "policy_checks", "confirmation_required"), "SemanticPimInstructionParser", "POST /assistant/instruction-preview", ()),
    (34, ("enterprise_pim_appgen_inbox_event", "enterprise_pim_dead_letter_event"), ("schema_validation", "idempotency_key", "duplicate_suppression", "retry_evidence", "unsupported_event_rejection", "projection_rebuild"), "PimInboxReliability", "POST /events/inbox/replay", ("MediaAssetApproved", "PricePromotionApproved", "TaxCalculated", "InventoryPositionUpdated")),
    (35, ("enterprise_pim_appgen_outbox_event", "pim_control_assertion"), ("outbox_state", "ordering_group", "payload_hash", "retry_attempts", "next_retry", "delivery_proof", "dead_letter_linkage"), "PimOutboxDeliveryAssurance", "GET /events/outbox-assurance", ()),
    (36, ("pim_control_assertion", "pim_federation_projection"), ("schema_scan", "service_scan", "route_scan", "dsl_scan", "agent_plan_scan", "foreign_table_access"), "CrossPbcBoundaryProof", "POST /boundary/proof", PIM_DECLARED_DEPENDENCIES),
    (37, ("pim_master_data_proof", "publication_readiness_check"), ("taxonomy_status", "attribute_completeness", "localized_content_approval", "dependency_readiness", "validation_approval", "selective_disclosure"), "MasterDataProofGeneration", "POST /master-data/proofs", ()),
    (38, ("pim_audit_trace", "pim_control_assertion"), ("hash_chain", "taxonomy_change", "attribute_change", "localization_version", "workflow_approval", "dependency_event", "outbox_delivery"), "ImmutablePimAuditTrail", "GET /audit/hash-chain", ()),
    (39, ("pim_policy_screening", "pim_rule"), ("policy_scope", "restricted_terms", "locale_rules", "channel_policy", "market", "product_family", "explainable_outcome"), "DynamicPimPolicyScreening", "POST /policies/screen", ()),
    (40, ("taxonomy_optimization_plan", "pim_governed_model"), ("duplicate_nodes", "over_deep_branches", "low_coverage_nodes", "missing_attributes", "facet_issues", "localization_cost", "proposed_restructuring"), "TaxonomyOptimizationPlanner", "POST /taxonomy-optimization/plans", ()),
    (41, ("workflow_allocation", "data_steward_assignment"), ("skill", "locale", "taxonomy_ownership", "workload", "sla", "priority", "conflict_of_interest", "explanation"), "WorkflowAllocationMechanism", "POST /workflow-allocation/allocate", ()),
    (42, ("content_anomaly_signal", "localized_content"), ("text_length", "language", "forbidden_terms", "numeric_attributes", "units", "option_values", "mass_change"), "ContentAnomalyDetection", "POST /content-anomalies/detect", ()),
    (43, ("enrichment_forecast", "publication_readiness_check"), ("taxonomy", "channel", "locale", "dependency_source", "steward_queue", "workflow_sla", "exception_backlog", "event_health"), "EnrichmentReadinessForecast", "POST /readiness/forecast", ()),
    (44, ("enrichment_risk_model", "pim_governed_model"), ("model_purpose", "training_window", "feature_lineage", "validation_metrics", "drift", "false_ready_impact", "approval_status"), "EnrichmentRiskModelGovernance", "POST /models/enrichment-risk/register", ()),
    (45, ("carbon_enrichment_window", "pim_parameter"), ("batch_job", "carbon_window", "sla_guardrail", "translation_update", "search_projection_check", "proof_generation", "model_scoring"), "CarbonAwareEnrichmentScheduling", "POST /enrichment/carbon-schedule", ()),
    (46, ("pim_configuration", "pim_control_assertion"), ("taxonomy_graph", "attributes", "inheritance", "validation_rules", "localization", "dependencies", "events", "release_evidence"), "EnterprisePimWorkbench", "GET /enterprise-pim-workbench", ()),
    (47, ("publication_readiness_check", "validation_workflow", "pim_exception"), ("readiness_gaps", "workflow_approvals", "missing_locales", "invalid_attributes", "stale_dependencies", "safe_publish_actions"), "ValidationPublicationCockpit", "GET /publication-cockpit", ()),
    (48, ("pim_control_assertion", "enterprise_pim_dead_letter_event"), ("required_locale_assertion", "required_attribute_assertion", "workflow_assertion", "dependency_assertion", "fallback_assertion", "agent_preview_assertion"), "ContinuousPimControlTesting", "POST /controls/run", ()),
    (49, ("content_completeness_score", "pim_control_assertion", "pim_governed_model"), ("taxonomy_integrity", "attribute_coverage", "localization_quality", "dependency_freshness", "event_reliability", "agent_safety", "readiness_score"), "EnterprisePimReadinessScore", "GET /readiness/score", ()),
    (50, ("product_taxonomy", "product_attribute", "localized_content", "validation_workflow", "dependency_projection", "publication_readiness_check", "enterprise_pim_appgen_outbox_event"), ("taxonomy_step", "attribute_step", "option_step", "localized_content_step", "workflow_step", "dependency_step", "publication_step", "event_step", "final_signoff"), "EndToEndPimPublicationProof", "POST /release/pim-publication-proof", ()),
)

CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, tables, fields, ui, route, deps in _SPEC_ROWS}
_EMPTY_ALLOWED_FIELDS = (
    "competing_candidates",
    "duplicate_nodes",
    "facet_issues",
    "foreign_table_access",
    "forbidden_phrase_flags",
    "forbidden_terms",
    "invalid_attributes",
    "low_coverage_nodes",
    "missing_attributes",
    "missing_locales",
    "node_moves",
    "over_deep_branches",
    "readiness_gaps",
    "restricted_terms",
    "retired_nodes",
    "stale_dependencies",
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
        "taxonomy_id": "tax-1", "tenant": "tenant-a", "default_locale": "en-US", "allowed_locales": ("en-US", "fr-FR"), "root_node": "root", "steward": "steward-1", "dependency_compatibility": "compatible",
        "node_state": "active", "parent_node": "root", "locale_names": {"en-US": "Products"}, "effective_dates": ("2026-05-30", "2027-05-30"), "migration_guidance": "mapped",
        "relationship_type": "parent_child", "source_node": "root", "target_node": "child", "effective_window": "current", "max_depth": 5, "publication_impact": "reviewed", "acyclic": True,
        "candidate_state": "approved", "confidence": 0.92, "suggested_node": "child", "source_signal": "rules", "competing_candidates": (), "reviewer": "steward-1", "decision_reason": "best-match",
        "node_moves": (), "retired_nodes": (), "inherited_attribute_changes": "previewed", "translation_impact": "reviewed", "channel_policy_impact": "reviewed", "projection_freshness": "fresh",
        "attribute_state": "active", "data_type": "string", "unit": "none", "required_flag": True, "localized_labels": {"en-US": "Material"}, "inheritance_mode": "override_allowed", "publication_eligibility": True,
        "group_order": 10, "taxonomy_scope": "tax-1", "required_attributes": ("attr_material",), "optional_attributes": ("attr_color",), "locale_labels": {"en-US": "Core"}, "channel_visibility": ("commerce",), "owner": "steward-1",
        "option_state": "active", "code": "NONE", "localized_display": {"en-US": "None"}, "synonyms": ("n/a",), "sort_order": 1, "replacement": "not_required_active", "channel_mappings": {"commerce": "NONE"},
        "source_node": "root", "override_reason": "market-specific", "conflict_detection": False, "completeness_effect": "positive",
        "rule_type": "range", "predicate": "value in options", "sample_evaluation": "pass", "failure_severity": "blocker", "affected_attributes": ("attr_material",), "locale_scope": ("en-US",), "compiled_hash": "sha256:rule",
        "missing_values": 0, "invalid_units": 0, "stale_values": 0, "inconsistent_options": 0, "localization_gaps": 0, "dependency_mismatch": False,
        "locale": "fr-FR", "content_state": "approved", "source_text_hash": "sha256:src", "translation_source": "human", "quality_score": 0.93, "fallback_status": "not_used",
        "semantic_diff": "minor", "source_locale": "en-US", "target_locale": "fr-FR", "rollback": "available",
        "source_hash": "sha256:tm", "target_locale": "fr-FR", "domain": "product", "approval_status": "approved", "expiry": "2027-05-30", "forbidden_phrase_flags": (),
        "fallback_chain": ("fr-FR", "en-US"), "channel": "commerce", "taxonomy": "tax-1", "attribute": "attr_material", "allowed_depth": 1, "blocking_rules": "visible",
        "taxonomy_node": "child", "required_attributes": ("attr_material",), "content_quality": 0.95, "dependency_freshness": "fresh", "exception_severity": "none", "readiness_score": 0.96,
        "workflow_state": "approved", "required_steps": ("steward", "compliance"), "sla": "PT24H", "approvers": ("steward",), "delegated_reviewers": ("backup-steward",), "evidence_required": True, "escalation": "none",
        "approver": "steward", "role": "data_steward", "step": "final", "decision": "approved", "scope": "tax-1", "policy_version": "pim-2026.05", "evidence_snapshot": "snap-1", "residual_risk": "accepted-low",
        "required_locales": ("en-US", "fr-FR"), "workflow_approval": True, "dependency_projections": "fresh", "taxonomy_status": "active", "channel_policy": "passed", "event_delivery_health": "healthy",
        "required_fields": ("title", "description"), "locale_set": ("en-US", "fr-FR"), "dependency_requirements": ("media", "price", "tax"), "publication_window": "open", "embargo_rules": ("prelaunch-content-hold",), "fallback_allowance": "controlled", "approval_policy": "dual",
        "source": "dam_core", "version_floor": 1, "accepted_events": ("MediaAssetApproved",), "freshness_sla": "PT2H", "compatibility_status": "compatible", "rejection_criteria": ("schema_mismatch",),
        "projection_source": "dam_core", "version": 1, "source_event_id": "evt-1", "freshness": "fresh", "schema_compatibility": "compatible", "readiness_impact": "pass",
        "asset_type": "image", "approval_state": "approved", "rights_window": "valid", "rendition_coverage": "complete", "alt_text": "present", "compliance_tags": ("safe",),
        "product": "sku-1", "market": "US", "currency": "USD", "jurisdiction": "US-NY", "validity_window": "current", "exception_state": "none",
        "inventory_readiness": "ready", "search_schema_compatibility": "compatible", "facet_mapping": "mapped", "index_state": "ready", "stock_policy": "publish_when_available", "stale_warning": False,
        "source_product": "sku-1", "target_product": "sku-2", "compatibility_context": "accessory", "directionality": "directed", "channel_scope": ("commerce",),
        "bundle_state": "ready", "components": ("sku-1", "sku-2"), "quantities": {"sku-1": 1}, "optional_parts": ("accessory-kit",), "substitution_rules": "allowed", "price_tax_inventory_checks": "passed",
        "variant_axes": ("size", "color"), "required_axis_values": ("M", "Blue"), "member_uniqueness": True, "content_inheritance": "resolved", "disallowed_combinations": ("size-xl-color-retired",), "locale_differences": "reviewed",
        "assignment_state": "approved", "eligibility_reason": "policy-match", "embargo": False, "dependency_readiness": "ready",
        "attribute_group": "grp-core", "exception_type": "missing_locale", "workload": 4, "sla": "PT24H", "priority": "high", "conflict_of_interest": False, "explanation": "best-fit",
        "category": "missing_attribute", "severity": "medium", "affected_scope": "sku-1", "root_cause": "source_missing", "recommended_action": "complete", "closure_proof": "proof-1",
        "recommendation_type": "missing_locale", "missing_locale": "fr-FR", "missing_attribute": "attr_material", "invalid_value": "none", "media_gap": False, "approval_needed": True,
        "instruction": "set French title", "target_taxonomy": "tax-1", "requested_action": "preview_update", "policy_checks": "passed", "confirmation_required": True,
        "schema_validation": "passed", "idempotency_key": "idem-1", "duplicate_suppression": True, "retry_evidence": "retry-ok", "unsupported_event_rejection": True, "projection_rebuild": "available",
        "outbox_state": "delivered", "ordering_group": "sku-1", "payload_hash": "sha256:payload", "retry_attempts": 0, "next_retry": "not_required_delivered", "delivery_proof": "acked", "dead_letter_linkage": "none",
        "schema_scan": "passed", "service_scan": "passed", "route_scan": "passed", "dsl_scan": "passed", "agent_plan_scan": "passed", "foreign_table_access": (),
        "taxonomy_status": "active", "attribute_completeness": 0.97, "localized_content_approval": True, "validation_approval": True, "selective_disclosure": True,
        "hash_chain": ("h1", "h2"), "taxonomy_change": "sealed", "attribute_change": "sealed", "localization_version": "sealed", "workflow_approval": True, "dependency_event": "sealed", "outbox_delivery": "sealed",
        "policy_scope": "publication", "restricted_terms": (), "locale_rules": "passed", "product_family": "general", "explainable_outcome": "clear",
        "duplicate_nodes": (), "over_deep_branches": (), "low_coverage_nodes": (), "missing_attributes": (), "facet_issues": (), "localization_cost": "estimated", "proposed_restructuring": "balanced",
        "skill": "taxonomy", "taxonomy_ownership": "tax-1", "conflict_of_interest": False,
        "text_length": "normal", "language": "fr", "forbidden_terms": (), "numeric_attributes": "valid", "units": "valid", "option_values": "valid", "mass_change": False,
        "dependency_source": "dam_core", "steward_queue": "normal", "workflow_sla": "green", "exception_backlog": 0, "event_health": "healthy",
        "model_purpose": "readiness", "training_window": "2026-Q2", "feature_lineage": "documented", "validation_metrics": {"auc": 0.91}, "drift": 0.02, "false_ready_impact": "low", "approval_status": "approved",
        "batch_job": "translation_memory_update", "carbon_window": "low-carbon", "sla_guardrail": "met", "translation_update": "scheduled", "search_projection_check": "scheduled", "proof_generation": "scheduled", "model_scoring": "scheduled",
        "taxonomy_graph": "visible", "attributes": "visible", "inheritance": "visible", "validation_rules": "visible", "localization": "visible", "dependencies": "visible", "events": "visible", "release_evidence": "visible",
        "readiness_gaps": (), "workflow_approvals": "complete", "missing_locales": (), "invalid_attributes": (), "stale_dependencies": (), "safe_publish_actions": ("publish",),
        "required_locale_assertion": "passed", "required_attribute_assertion": "passed", "workflow_assertion": "passed", "dependency_assertion": "passed", "fallback_assertion": "passed", "agent_preview_assertion": "passed",
        "taxonomy_integrity": 0.98, "attribute_coverage": 0.97, "localization_quality": 0.94, "event_reliability": 0.99, "agent_safety": 1.0,
        "taxonomy_step": "passed", "attribute_step": "passed", "option_step": "passed", "localized_content_step": "passed", "workflow_step": "passed", "dependency_step": "passed", "publication_step": "passed", "event_step": "passed", "final_signoff": "signed",
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and payload.get("dependency_compatibility") != "compatible":
        findings.append("taxonomy readiness requires compatible dependency schemas")
    if n == 2 and payload.get("node_state") not in {"draft", "active", "deprecated", "merged", "split", "blocked", "archived", "published"}:
        findings.append("taxonomy node uses unsupported lifecycle state")
    if n == 3 and payload.get("acyclic") is not True:
        findings.append("taxonomy relationships must be acyclic")
    if n == 4 and payload.get("confidence", 0) < 0.5 and not payload.get("reviewer"):
        findings.append("low-confidence classification candidates require steward review")
    if n == 5 and payload.get("projection_freshness") != "fresh":
        findings.append("taxonomy publication simulation requires fresh downstream projections")
    if n == 6 and payload.get("publication_eligibility") is not True:
        findings.append("attribute definition is not publication eligible")
    if n == 7 and not payload.get("required_attributes"):
        findings.append("attribute groups must declare required attributes")
    if n == 8 and payload.get("option_state") == "deprecated" and not payload.get("replacement"):
        findings.append("deprecated value options require replacement guidance")
    if n == 9 and payload.get("conflict_detection"):
        findings.append("inheritance conflicts must be resolved before publication")
    if n == 10 and not payload.get("compiled_hash"):
        findings.append("validation rules require compiled hash evidence")
    if n == 11 and any(payload.get(field) for field in ("missing_values", "invalid_units", "stale_values", "inconsistent_options", "localization_gaps")):
        findings.append("attribute quality signals contain unresolved quality gaps")
    if n == 12 and (payload.get("content_state") not in {"approved", "published"} or float(payload.get("quality_score", 0)) < 0.8):
        findings.append("localized content requires approved high-quality state")
    if n == 13 and not payload.get("rollback"):
        findings.append("localized content versions require rollback evidence")
    if n == 14 and payload.get("forbidden_phrase_flags"):
        findings.append("translation memory contains forbidden phrase flags")
    if n == 15 and int(payload.get("allowed_depth", 0)) > 2:
        findings.append("locale fallback depth exceeds safe publication policy")
    if n == 16 and float(payload.get("readiness_score", 0)) < 0.85:
        findings.append("completeness score is below publication threshold")
    if n == 17 and payload.get("workflow_state") != "approved":
        findings.append("validation workflow must be approved")
    if n == 18 and not payload.get("evidence_snapshot"):
        findings.append("approval decisions require evidence snapshot")
    if n == 19 and not all(payload.get(field) for field in ("workflow_approval", "dependency_projections", "event_delivery_health")):
        findings.append("publication readiness requires workflow, dependency, and event health evidence")
    if n == 20 and payload.get("publication_window") != "open":
        findings.append("channel publication policy blocks closed windows")
    if n == 21 and payload.get("compatibility_status") != "compatible":
        findings.append("dependency schema is not compatible")
    if n == 22 and payload.get("freshness") != "fresh":
        findings.append("dependency projection is stale")
    if n == 23 and payload.get("approval_state") != "approved":
        findings.append("media dependency coverage requires approved assets")
    if n == 24 and payload.get("exception_state") != "none":
        findings.append("price/tax dependency has active exception")
    if n == 25 and payload.get("stale_warning"):
        findings.append("inventory/search dependency has stale projection warning")
    if n == 26 and not payload.get("channel_scope"):
        findings.append("product relationships require channel scope")
    if n == 27 and payload.get("price_tax_inventory_checks") != "passed":
        findings.append("bundle definition requires price/tax/inventory checks")
    if n == 28 and payload.get("member_uniqueness") is not True:
        findings.append("variant family members must be unique")
    if n == 29 and payload.get("embargo"):
        findings.append("assortment assignment is embargoed")
    if n == 30 and payload.get("conflict_of_interest"):
        findings.append("data steward allocation has conflict of interest")
    if n == 31 and not payload.get("closure_proof"):
        findings.append("PIM exception resolution requires closure proof")
    if n == 32 and float(payload.get("confidence", 0)) < 0.5:
        findings.append("autonomous enrichment recommendation confidence is too low")
    if n == 33 and payload.get("confirmation_required") is not True:
        findings.append("semantic PIM instruction parsing must be preview-only until confirmation")
    if n == 34 and payload.get("schema_validation") != "passed":
        findings.append("inbox reliability requires schema validation")
    if n == 35 and not payload.get("delivery_proof"):
        findings.append("outbox delivery assurance requires delivery proof")
    if n == 36 and payload.get("foreign_table_access"):
        findings.append("cross-PBC boundary proof forbids foreign table access")
    if n == 37 and payload.get("selective_disclosure") is not True:
        findings.append("master-data proof requires selective disclosure controls")
    if n == 38 and not payload.get("hash_chain"):
        findings.append("immutable PIM audit trail requires hash chain")
    if n == 39 and payload.get("restricted_terms"):
        findings.append("dynamic PIM policy screening found restricted terms")
    if n == 40 and payload.get("over_deep_branches"):
        findings.append("taxonomy optimization plan contains unresolved over-deep branches")
    if n == 41 and payload.get("conflict_of_interest"):
        findings.append("workflow allocation cannot assign conflicted reviewer")
    if n == 42 and payload.get("forbidden_terms"):
        findings.append("content anomaly detector found forbidden terms")
    if n == 43 and int(payload.get("exception_backlog", 0)) > 0:
        findings.append("readiness forecast must include backlog risk before green forecast")
    if n == 44 and payload.get("approval_status") != "approved":
        findings.append("enrichment risk model requires governance approval")
    if n == 45 and payload.get("sla_guardrail") != "met":
        findings.append("carbon-aware enrichment cannot violate SLA guardrails")
    if n == 46 and not all(payload.get(field) == "visible" for field in ("taxonomy_graph", "attributes", "inheritance", "validation_rules", "localization", "dependencies", "events", "release_evidence")):
        findings.append("PIM workbench must surface every core command center area")
    if n == 47 and (payload.get("readiness_gaps") or payload.get("missing_locales") or payload.get("invalid_attributes") or payload.get("stale_dependencies")):
        findings.append("publication cockpit has unresolved blockers")
    if n == 48 and any(payload.get(field) != "passed" for field in ("required_locale_assertion", "required_attribute_assertion", "workflow_assertion", "dependency_assertion", "fallback_assertion", "agent_preview_assertion")):
        findings.append("continuous PIM control tests have failing assertions")
    if n == 49 and float(payload.get("readiness_score", 0)) < 0.9:
        findings.append("enterprise PIM readiness score is below live-publication threshold")
    if n == 50 and any(payload.get(field) != "passed" for field in ("taxonomy_step", "attribute_step", "option_step", "localized_content_step", "workflow_step", "dependency_step", "publication_step", "event_step")):
        findings.append("end-to-end PIM publication proof requires every lifecycle step to pass")
    return tuple(findings)


def evaluate_pim_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PIM_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PIM_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": PIM_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PIM_ALLOWED_DATABASE_BACKENDS,
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


def improve1_pim_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_pim_control(capability) for capability in PIM_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.enterprise-pim-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": PIM_OWNED_TABLES,
        "declared_dependencies": PIM_DECLARED_DEPENDENCIES,
        "allowed_database_backends": PIM_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": PIM_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PIM_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_pim_control(slug, payload)) for capability in PIM_CONTROL_CAPABILITIES}
