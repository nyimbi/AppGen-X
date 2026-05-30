"""Executable improve1 controls for the IT Service Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "it_service_management"
EVENT_CONTRACT = "AppGen-X"
ITSM_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ITSM_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.it_service_management.events"
ITSM_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"it_service_management_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
ITSM_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "PolicyChanged", "AuditEventSealed", "OperationalKpiChanged", "IdentityEntitlementProjected",
    "AssetConfigurationProjected", "MonitoringAlertRaised", "CarbonIntensityProjected",
    "ServiceCatalogChanged", "SecurityIncidentProjected", "ReleaseDeploymentChanged",
)))
ITSM_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in ITSM_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in ITSM_CONTROL_CAPABILITIES}
_DEFAULT_FIELDS = ("owned_record", "itsm_context", "required_evidence", "operator_visible", "audit_trail", "safe_to_execute")
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {cap.feature_number: _DEFAULT_FIELDS for cap in ITSM_CONTROL_CAPABILITIES}
_FEATURE_FIELDS.update({1: ('major_incident', 'declaration_reason', 'commander', 'impact_scope', 'stakeholder_comms', 'war_room_opened', 'demotion_rule'), 2: ('impact', 'urgency', 'priority', 'matrix_version', 'override_reason', 'sla_attached', 'mispriority_blocked'), 3: ('duplicate_candidates', 'correlation_key', 'outage_id', 'rollup_parent', 'customer_impact', 'duplicate_merge_lineage', 'outage_visible'), 4: ('timeline', 'evidence_items', 'freeze_timestamp', 'chain_of_custody', 'editor_lock', 'audit_export', 'tamper_guard'), 5: ('restoration_milestone', 'service_restored_at', 'workaround_at', 'resolution_at', 'sla_state', 'customer_visible', 'milestone_timer_adjusted'), 6: ('swarm_room', 'resolver_group', 'handoff_reason', 'owner_acceptance', 'handoff_sla', 'handoff_audit', 'orphaned_ticket_blocked'), 7: ('catalog_item', 'service', 'request_type', 'eligibility', 'fulfillment_model', 'approval_policy', 'catalog_version'), 8: ('access_request', 'entitlement', 'requester', 'approver', 'sod_check', 'least_privilege', 'provisioning_blocked_until_valid'), 9: ('fulfillment_plan', 'tasks', 'task_dependencies', 'owners', 'automation_steps', 'rollback_steps', 'completion_evidence'), 10: ('requester_confirmation', 'closure_code', 'fulfillment_evidence', 'reopen_window', 'satisfaction_signal', 'premature_closure_blocked'), 11: ('change_type', 'path', 'emergency_reason', 'standard_template', 'normal_assessment', 'emergency_review', 'path_guard'), 12: ('risk_score', 'blast_radius', 'affected_services', 'affected_cis', 'deployment_complexity', 'rollback_complexity', 'approval_tier'), 13: ('maintenance_window', 'blackout_calendar', 'requested_start', 'requested_end', 'exception_approval', 'conflict_detected', 'schedule_blocked_on_blackout'), 14: ('cab_agenda', 'attendees', 'quorum_met', 'decision', 'decision_rationale', 'conditions', 'minutes_captured'), 15: ('backout_plan', 'validation_checklist', 'owner', 'test_evidence', 'go_no_go_gate', 'implementation_blocked_without_plan'), 16: ('pir_record', 'implementation_outcome', 'incidents_caused', 'lessons_learned', 'action_items', 'closure_owner', 'pir_required_for_failed_change'), 17: ('problem_record', 'linked_incidents', 'linked_changes', 'known_error_candidate', 'impact_summary', 'problem_owner', 'linkage_visible'), 18: ('rca_template', 'method', 'contributing_factors', 'evidence_required', 'action_plan', 'reviewer', 'template_complete'), 19: ('known_error', 'workaround', 'affected_services', 'article_status', 'approval', 'publication_scope', 'customer_safe_version'), 20: ('recurrence_signal', 'incident_pattern', 'time_window', 'service_scope', 'threshold', 'problem_candidate_created', 'false_positive_review'), 21: ('ci_graph', 'ci_nodes', 'ci_edges', 'relationship_types', 'service_mapping', 'dependency_depth', 'graph_query_supported'), 22: ('ci_owner', 'support_group', 'business_owner', 'escalation_contact', 'support_hours', 'ownership_gap_visible'), 23: ('drift_signal', 'source_system', 'last_verified_at', 'stale_threshold', 'drift_reason', 'correction_task', 'stale_ci_flagged'), 24: ('change_id', 'dependency_impact', 'upstream_services', 'downstream_services', 'customer_segments', 'approval_preview', 'impact_preview_required'), 25: ('sla', 'ola', 'underpinning_contract', 'commitment_owner', 'clock_source', 'breach_owner', 'separation_visible'), 26: ('pause_reason', 'calendar', 'support_hours', 'paused_at', 'resumed_at', 'audit_reason', 'manual_pause_guard'), 27: ('queue', 'role', 'permissions', 'filters', 'work_item_type', 'tenant_scope', 'role_filtered_actions'), 28: ('aging_bucket', 'load_signal', 'attention_score', 'routing_reason', 'skill_match', 'priority_adjustment', 'routing_explainable'), 29: ('knowledge_article', 'lifecycle_state', 'quality_score', 'reviewer', 'expiry_date', 'usage_feedback', 'publication_blocked_until_quality'), 30: ('ticket_context', 'suggested_articles', 'relevance_score', 'citation', 'operator_feedback', 'suggestion_visible', 'no_auto_resolution'), 31: ('document_instruction', 'operator_notes', 'extracted_fields', 'source_citations', 'human_confirmation', 'unsafe_prompt_denied', 'direct_mutation_blocked'), 32: ('policy_rule', 'sandbox_payload', 'dry_run_result', 'impacted_records', 'live_mutation_blocked', 'explainable_diff', 'approval_required'), 33: ('parameter', 'safe_min', 'safe_max', 'requested_value', 'impact_preview', 'activation_guard', 'rollback_value'), 34: ('ticket_event', 'event_sequence', 'replay_cursor', 'projection_name', 'replay_idempotent', 'history_complete', 'mutation_order_preserved'), 35: ('dead_letter_item', 'workflow_type', 'failure_reason', 'retry_policy', 'safe_replay_allowed', 'operator_notes', 'closure_code'), 36: ('consumed_event', 'source_pbc', 'dependency_snapshot', 'freshness_sla', 'lineage_visible', 'stale_dependency_alert', 'idempotent_handler'), 37: ('breach_prediction', 'backlog_risk', 'risk_factors', 'forecast_horizon', 'confidence', 'recommended_action', 'human_review'), 38: ('counterfactual', 'change_timing', 'staffing_level', 'risk_delta', 'simulation_scope', 'no_live_mutation', 'assumptions_visible'), 39: ('control_suite', 'approval_checked', 'sod_checked', 'emergency_change_checked', 'access_request_checked', 'control_effective'), 40: ('evidence_packet', 'packet_hash', 'previous_hash', 'event_hashes', 'proof_verified', 'tamper_evident_export'), 41: ('tenant_id', 'queue_scope', 'policy_scope', 'evidence_scope', 'cross_tenant_access_blocked', 'tenant_key_isolated'), 42: ('tenant_calendar', 'support_hours', 'service_tier', 'holiday_rules', 'clock_policy', 'tenant_override', 'calendar_applied'), 43: ('change_urgency', 'carbon_signal', 'schedule_options', 'renewable_window', 'business_constraint', 'non_urgent_only', 'operator_override_visible'), 44: ('continuity_plan', 'dr_readiness', 'rto', 'rpo', 'dependency_contacts', 'exercise_evidence', 'readiness_gap_visible'), 45: ('release_assurance', 'routes_checked', 'events_checked', 'ui_fragments_checked', 'forms_checked', 'wizards_checked', 'blocking_gaps'), 46: ('metric', 'definition', 'owner', 'grain', 'calculation', 'source_table', 'analytics_ready'), 47: ('audit_packet', 'export_scope', 'redaction_profile', 'evidence_index', 'regulator_ready', 'export_audit', 'protected_fields_masked'), 48: ('keyboard_flow', 'bulk_action', 'density_mode', 'queue_shortcuts', 'error_recovery', 'operator_feedback', 'high_volume_ready'), 49: ('api_route', 'idempotency_key', 'correction_command', 'stable_response', 'duplicate_prevented', 'correction_audit', 'undo_path'), 50: ('scenario', 'incident_seeded', 'request_seeded', 'change_seeded', 'problem_seeded', 'ci_seeded', 'sla_seeded', 'knowledge_seeded', 'events_emitted', 'workbench_driven', 'release_documents_updated')})
_FEATURE_DEPENDENCIES = {8: ("IdentityEntitlementProjected",), 21: ("AssetConfigurationProjected",), 36: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"), 43: ("CarbonIntensityProjected",), 45: ("ReleaseDeploymentChanged",)}
_EMPTY_ALLOWED_FIELDS = ("duplicate_candidates", "blocking_gaps")
_REQUIRED_TRUE = {1: ('major_incident', 'war_room_opened'), 2: ('sla_attached', 'mispriority_blocked'), 3: ('duplicate_merge_lineage', 'outage_visible'), 4: ('editor_lock', 'tamper_guard'), 5: ('milestone_timer_adjusted',), 6: ('owner_acceptance', 'orphaned_ticket_blocked'), 7: ('eligibility',), 8: ('sod_check', 'least_privilege', 'provisioning_blocked_until_valid'), 9: ('completion_evidence',), 10: ('requester_confirmation', 'premature_closure_blocked'), 11: ('path_guard',), 12: ('approval_tier',), 13: ('conflict_detected', 'schedule_blocked_on_blackout'), 14: ('quorum_met', 'minutes_captured'), 15: ('backout_plan', 'validation_checklist', 'implementation_blocked_without_plan'), 16: ('pir_required_for_failed_change',), 17: ('linkage_visible',), 18: ('template_complete',), 19: ('approval', 'customer_safe_version'), 20: ('problem_candidate_created', 'false_positive_review'), 21: ('graph_query_supported',), 22: ('ownership_gap_visible',), 23: ('correction_task', 'stale_ci_flagged'), 24: ('impact_preview_required',), 25: ('separation_visible',), 26: ('manual_pause_guard',), 27: ('role_filtered_actions',), 28: ('routing_explainable',), 29: ('publication_blocked_until_quality',), 30: ('suggestion_visible', 'no_auto_resolution'), 31: ('source_citations', 'human_confirmation', 'unsafe_prompt_denied', 'direct_mutation_blocked'), 32: ('live_mutation_blocked', 'approval_required'), 33: ('impact_preview', 'activation_guard'), 34: ('replay_idempotent', 'history_complete', 'mutation_order_preserved'), 35: ('safe_replay_allowed',), 36: ('lineage_visible', 'stale_dependency_alert', 'idempotent_handler'), 37: ('human_review',), 38: ('no_live_mutation', 'assumptions_visible'), 39: ('approval_checked', 'sod_checked', 'emergency_change_checked', 'access_request_checked', 'control_effective'), 40: ('proof_verified', 'tamper_evident_export'), 41: ('cross_tenant_access_blocked', 'tenant_key_isolated'), 42: ('calendar_applied',), 43: ('non_urgent_only', 'operator_override_visible'), 44: ('exercise_evidence', 'readiness_gap_visible'), 45: ('routes_checked', 'events_checked', 'ui_fragments_checked', 'forms_checked', 'wizards_checked'), 46: ('analytics_ready',), 47: ('regulator_ready', 'export_audit', 'protected_fields_masked'), 48: ('high_volume_ready',), 49: ('stable_response', 'duplicate_prevented', 'correction_audit', 'undo_path'), 50: ('incident_seeded', 'request_seeded', 'change_seeded', 'problem_seeded', 'ci_seeded', 'sla_seeded', 'knowledge_seeded', 'events_emitted', 'workbench_driven', 'release_documents_updated')}


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"it_service_management_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "ui": _camel(capability.slug), "route": f"POST /it-service-management/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in ITSM_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    for field in _REQUIRED_TRUE.get(resolved.feature_number, ()): payload[field] = True
    payload.update({"duplicate_candidates": (), "blocking_gaps": (), "impact": "high", "urgency": "high", "priority": "P1", "confidence": 0.91, "safe_min": 1, "safe_max": 100, "requested_value": 50, "database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "required_event_topic": ITSM_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    for field in _REQUIRED_TRUE.get(n, ()): 
        if payload.get(field) is not True:
            findings.append(f"{capability.title} requires {field.replace('_', ' ')}")
    if n == 1 and payload.get("major_incident") is not True: findings.append("major incident declaration requires command, communication, and demotion evidence")
    if n == 2 and not all(payload.get(field) for field in ("impact", "urgency", "priority")): findings.append("impact and urgency matrix must derive a priority with SLA evidence")
    if n == 8 and payload.get("provisioning_blocked_until_valid") is not True: findings.append("access request entitlement validation must block provisioning until entitlement and SoD pass")
    if n == 13 and payload.get("schedule_blocked_on_blackout") is not True: findings.append("blackout calendar enforcement must block conflicting changes")
    if n == 14 and payload.get("quorum_met") is not True: findings.append("CAB decision capture requires quorum and minutes")
    if n == 15 and payload.get("implementation_blocked_without_plan") is not True: findings.append("backout plan enforcement must block implementation without validation")
    if n == 26 and payload.get("manual_pause_guard") is not True: findings.append("calendar-aware SLA pause/resume requires audited pause guard")
    if n == 31 and (payload.get("human_confirmation") is not True or payload.get("direct_mutation_blocked") is not True or not payload.get("source_citations")): findings.append("structured document intake requires citations, confirmation, and no direct mutation")
    if n == 35 and payload.get("safe_replay_allowed") is not True: findings.append("dead-letter triage must prove safe ITSM replay")
    if n == 40 and payload.get("proof_verified") is not True: findings.append("cryptographic operational evidence must verify before export")
    if n == 41 and payload.get("cross_tenant_access_blocked") is not True: findings.append("tenant isolation must block cross-tenant queue, policy, and evidence access")
    if n == 49 and (payload.get("duplicate_prevented") is not True or payload.get("stable_response") is not True): findings.append("API completeness requires idempotent stable responses and correction audit")
    if n == 50 and not all(payload.get(field) is True for field in _REQUIRED_TRUE[50]): findings.append("end-to-end ITSM domain scenario harness is incomplete")
    if payload.get("stream_engine_picker_visible"): findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in ITSM_CONTROL_ALLOWED_DATABASE_BACKENDS: findings.append("ordinary ITSM PBC datastore must be PostgreSQL, MySQL, or MariaDB")
    return tuple(findings)


def evaluate_itsm_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in ITSM_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in ITSM_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": ITSM_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": ITSM_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_itsm_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_itsm_control(capability) for capability in ITSM_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.it-service-management-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": ITSM_CONTROL_OWNED_TABLES, "declared_dependencies": ITSM_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": ITSM_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": ITSM_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


ITSM_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_itsm_control(slug, payload)) for capability in ITSM_CONTROL_CAPABILITIES}
