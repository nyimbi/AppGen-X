"""Executable improve1 controls for the Streaming Analytics PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
    STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES,
    STREAMING_ANALYTICS_OWNED_TABLES,
    STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
    STREAMING_ANALYTICS_RUNTIME_TABLES,
)

PBC_KEY = "streaming_analytics"
EVENT_CONTRACT = "AppGen-X"
STREAMING_ALLOWED_DATABASE_BACKENDS = STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
STREAMING_REQUIRED_EVENT_TOPIC = STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC
STREAMING_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in STREAMING_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in STREAMING_CAPABILITIES}
STREAMING_OWNED_TABLES = tuple(
    dict.fromkeys(
        STREAMING_ANALYTICS_OWNED_TABLES
        + STREAMING_ANALYTICS_RUNTIME_TABLES
        + tuple(f"streaming_analytics_{capability.slug}_control" for capability in STREAMING_CAPABILITIES)
    )
)
STREAMING_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES
        + (
            "AuditEventSealed",
            "OrderShipped",
            "PaymentCaptured",
            "PolicyChanged",
            "MetricContractChanged",
            "MetricSourceLagged",
            "MetricSourceRecovered",
            "DashboardConsumerChanged",
            "PrivacyPolicyChanged",
            "RetentionPolicyChanged",
            "ModelDriftDetected",
            "ProjectionDriftDetected",
            "DeadLetterEventRaised",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "stream_id",
    "metric_id",
    "window_id",
    "projection_id",
    "policy_version",
    "event_time",
    "evidence_references",
)
_FIELD_ROWS = """
1|semantic_contract_id,metric_definition,unit,dimension_key_set,allowed_aggregation_set,owner,compatibility_policy
2|event_time_model_id,event_timestamp,ingestion_timestamp,processing_timestamp,allowed_lateness,timezone_normalization,finality_state
3|window_taxonomy_id,window_type,alignment_rule,duration,slide_interval,session_gap,finalization_policy
4|cardinality_policy_id,dimension_key,max_distinct_count,top_k_retention,bucketing_policy,privacy_threshold,exception_state
5|event_identity_id,source_event_id,appgen_event_id,business_key,sequence_number,correction_marker,idempotency_result
6|backpressure_policy_id,overload_state,queue_depth,ingestion_lag,throttling_policy,priority_class,recovery_evidence
7|source_completeness_id,expected_source_count,received_source_count,missing_source_list,freshness_score,confidence_reduction,kpi_effect
8|quality_rule_id,rule_type,evaluated_field,expected_range,observed_value,severity,disposition
9|late_event_impact_id,affected_window_set,affected_snapshot_set,affected_projection_set,affected_alert_set,apply_strategy,replay_requirement
10|watermark_drift_id,source_watermark_lag,drift_reason,clock_skew_estimate,stalled_source,advancement_policy,override_approval
11|replay_plan_id,source_range,target_window_set,expected_event_count,dry_run_delta,alert_suppression,rollback_evidence
12|recomputation_proof_id,input_event_hash,stream_contract_hash,window_definition_hash,quality_rule_hash,output_snapshot_hash,divergence_reason
13|snapshot_finality_id,finality_state,completeness_score,supersession_link,certification_proof,late_adjustment_amount,publication_policy
14|lineage_graph_id,dashboard_projection_ref,kpi_snapshot_ref,aggregation_window_ref,metric_stream_ref,quality_decision_ref,evidence_export
15|projection_dependency_id,stream_dependency_set,compatibility_requirement,freshness_sla,projection_owner,consumer_impact,change_alert
16|projection_permission_id,role_filter,tenant_partition,region_partition,masked_dimension_set,purpose_tag,suppression_proof
17|alert_governance_id,threshold_rationale,hysteresis,cooldown,suppression_policy,escalation_path,backtest_result
18|dynamic_baseline_id,historical_profile,seasonality_key,daypart,calendar_context,baseline_value,abnormality_explanation
19|metric_exception_id,exception_category,severity,owner,remediation_step,closure_proof,evidence_bundle
20|risk_score_explanation_id,contributing_metric_set,weight_set,baseline,trend,quality_penalty,recommended_action
21|forecast_horizon_id,horizon_type,model_family,training_window,forecast_quantile,prediction_interval,validity_limit
22|forecast_backtest_id,model_version,horizon,error_metric,bias,interval_coverage,drift_evidence
23|policy_screening_id,screening_reason,matched_rule,affected_dimension_set,publication_decision,masking_strategy,waiver_expiry
24|retention_simulation_id,affected_stream_set,historical_window_coverage,replay_loss,audit_risk,storage_savings,approval_requirement
25|low_count_suppression_id,threshold,rare_dimension,aggregation_fallback,noise_policy,suppression_metadata,proof_hash
26|tenant_isolation_proof_id,tenant_partition_hash,stream_definition_hash,event_id_hash,snapshot_hash,projection_hash,emission_policy
27|federation_contract_id,external_event_type,schema_version,semantic_mapping,freshness_sla,quality_expectation,failure_mode
28|schema_compatibility_id,change_type,consumer_impact,migration_plan,compatibility_result,breaking_change_flag,activation_gate
29|unit_currency_normalization_id,source_unit,target_unit,currency_code,conversion_policy,precision_rule,normalization_audit
30|derived_metric_graph_id,numerator_stream,denominator_stream,calculation_formula,null_zero_policy,finality_rule,lineage_state
31|projection_refresh_strategy_id,refresh_strategy,refresh_cost,freshness_state,affected_snapshot_set,fallback_state,latency_impact
32|sla_monitor_id,ingestion_latency,window_finalization_latency,snapshot_publication_latency,projection_refresh_latency,query_response_latency,alert_delivery_latency
33|cost_governance_id,storage_usage,compute_cost,event_volume,query_cost,stream_value_score,retirement_option
34|approximation_control_id,sampling_policy,algorithm_type,error_bound,confidence,eligibility_rule,uncertainty_disclosure
35|distribution_metric_id,aggregation_type,percentile_set,histogram_bucket_set,unique_count_strategy,rate_formula,validity_check
36|replay_narrative_id,replay_cause,authorizer,data_range,before_after_snapshot,downstream_event_set,validation_result
37|audit_ledger_id,chain_hash,actor,command,affected_object_set,policy_version_hash,verification_api
38|kpi_proof_packet_id,stream_contract_hash,window_hash,accepted_event_hash_set,quality_decision_hash,policy_screen_hash,publication_signature
39|control_assertion_id,control_objective,stream_scope,test_method,sample_window,failure_evidence,remediation_owner
40|governed_model_id,model_purpose,feature_set,training_data_range,evaluation_metric_set,drift_check,approval_state
41|recomputation_playbook_id,playbook_trigger,dry_run_required,approval_need,recomputation_step_set,validation_rule,publication_behavior
42|analytics_degradation_id,degradation_scope,reason,start_time,affected_consumer_set,confidence_impact,recovery_condition
43|exception_collaboration_id,participant_set,comment_thread,task_set,decision_log,handoff_state,closure_evidence
44|metric_catalog_id,stream_definition,owner,quality_score,usage_count,lineage_link,certified_status
45|metric_definition_assistant_id,natural_language_request,proposed_dimension_set,proposed_window_set,quality_rule_set,policy_screen_set,approval_preview
46|dashboard_story_id,kpi_movement,source_fact_set,provisional_value_flag,forecast_flag,recommendation,source_citation
47|operator_command_center_id,stream_health,ingestion_lag,watermark_status,quality_failure_count,dead_letter_count,safe_remediation_command
48|contract_change_workflow_id,affected_projection_set,affected_api_set,affected_event_set,affected_model_set,notification_state,controlled_activation
49|agent_command_skill_id,skill_name,typed_preview,rbac_check,human_confirmation,audit_evidence,command_result
50|release_evidence_matrix_id,owned_table_mapping,command_mapping,route_mapping,event_contract_mapping,workbench_panel_mapping,boundary_check
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    5: ("AuditEventSealed", "OrderShipped", "PaymentCaptured"),
    6: ("MetricSourceLagged",),
    11: ("AuditEventSealed",),
    15: ("DashboardConsumerChanged",),
    23: ("PrivacyPolicyChanged",),
    24: ("RetentionPolicyChanged",),
    27: ("AuditEventSealed", "OrderShipped", "PaymentCaptured"),
    28: ("MetricContractChanged",),
    38: ("AuditEventSealed",),
    40: ("ModelDriftDetected",),
    42: ("MetricSourceLagged", "MetricSourceRecovered"),
    47: ("DeadLetterEventRaised",),
    48: ("DashboardConsumerChanged", "MetricContractChanged"),
}
_STREAM_CONTRACT_FEATURES = (1, 4, 15, 16, 23, 25, 26, 27, 28, 29, 30, 44, 45, 48, 50)
_EVENT_TIME_FEATURES = (2, 3, 5, 7, 9, 10, 11, 12, 13, 14, 36, 38, 41, 42, 50)
_QUALITY_REPLAY_FEATURES = (6, 8, 9, 10, 11, 12, 19, 24, 28, 32, 36, 37, 39, 41, 42, 43, 47, 50)
_FORECAST_MODEL_FEATURES = (18, 20, 21, 22, 34, 35, 40, 46, 49, 50)
_GOVERNANCE_FEATURES = (16, 17, 23, 24, 25, 26, 27, 33, 37, 38, 39, 40, 44, 48, 49, 50)
_AGENT_FEATURES = (36, 43, 44, 45, 46, 47, 49, 50)
_HUMAN_CONFIRMATION_FEATURES = (11, 17, 23, 24, 28, 33, 36, 39, 40, 41, 45, 48, 49, 50)
_APPROVAL_REQUIRED_FEATURES = (11, 17, 23, 24, 26, 28, 33, 36, 38, 39, 40, 41, 45, 48, 49, 50)
_NON_MUTATING_FEATURES = (1, 4, 9, 10, 11, 15, 17, 18, 20, 21, 22, 24, 27, 28, 33, 34, 36, 38, 40, 41, 44, 45, 46, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (5, 7, 15, 23, 24, 27, 28, 38, 40, 42, 47, 48)


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
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"streaming_analytics_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"StreamingAnalytics{_camel(capability.slug)}Panel",
        "route": f"POST /streaming-analytics/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in STREAMING_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({
        "database_backend": "postgresql",
        "event_contract": EVENT_CONTRACT,
        "event_topic": STREAMING_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "stream_contract_evidence_complete": True,
        "event_time_evidence_complete": True,
        "quality_replay_evidence_complete": True,
        "forecast_model_evidence_complete": True,
        "governance_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned analytics model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _STREAM_CONTRACT_FEATURES and payload.get("stream_contract_evidence_complete") is not True:
        findings.append("stream contracts, cardinality, projections, permissions, policy screening, suppression, tenancy, federation, compatibility, normalization, derived metrics, catalog, assistant definitions, contract changes, and release matrix require stream contract evidence")
    if number in _EVENT_TIME_FEATURES and payload.get("event_time_evidence_complete") is not True:
        findings.append("event-time models, window taxonomy, event identity, completeness, late events, watermarks, replay, recomputation, finality, lineage, narratives, KPI proofs, playbooks, degradation, and release matrix require event time evidence")
    if number in _QUALITY_REPLAY_FEATURES and payload.get("quality_replay_evidence_complete") is not True:
        findings.append("backpressure, quality rules, late impact, watermark drift, replay planning, recomputation proofs, exceptions, retention, schema compatibility, SLA monitoring, replay narratives, audit ledger, controls, playbooks, degradation, collaboration, command center, and release matrix require quality replay evidence")
    if number in _FORECAST_MODEL_FEATURES and payload.get("forecast_model_evidence_complete") is not True:
        findings.append("dynamic baselines, risk explainability, forecast horizons, backtesting, approximation, distribution metrics, governed models, dashboard storytelling, agent commands, and release matrix require forecast model evidence")
    if number in _GOVERNANCE_FEATURES and payload.get("governance_evidence_complete") is not True:
        findings.append("permission safety, alert governance, policy screening, retention, suppression, tenant isolation, federation, cost governance, audit ledgers, proof packets, controls, governed models, catalog, contract-change workflows, agent commands, and release matrix require governance evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("replay, alert policy, publication, retention, schema changes, cost retirement, narratives, controls, governed models, recomputation playbooks, metric definitions, contract activation, agent commands, and release gates require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk analytics actions require separated approval for replay, alert activation, sensitive publication, retention changes, isolation policies, schema changes, proof packets, controls, model lifecycle, recomputation, metric definitions, contract changes, agent commands, and release evidence")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("streaming analytics agent skills must cite evidence, emit typed previews, pass RBAC, require confirmation, and remain approval-gated before CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("contracts, cardinality, late-impact analysis, watermarks, replay dry-runs, projection impact, alert backtests, baselines, risk/forecast/cost simulations, replay narratives, proofs, models, playbooks, catalog discovery, metric definition, storytelling, contract changes, agent commands, and release matrix must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("audit, order, payment, policy, source, dashboard, privacy, retention, model drift, projection drift, and dead-letter context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != STREAMING_REQUIRED_EVENT_TOPIC:
        findings.append("streaming analytics eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in STREAMING_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary streaming analytics datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("streaming analytics controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_streaming_analytics_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in STREAMING_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in STREAMING_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "primary_proof": spec["primary_proof"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": STREAMING_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": STREAMING_ALLOWED_DATABASE_BACKENDS,
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


def improve1_streaming_analytics_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_streaming_analytics_control(capability) for capability in STREAMING_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.streaming-analytics-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": STREAMING_OWNED_TABLES,
        "declared_dependencies": STREAMING_DECLARED_DEPENDENCIES,
        "allowed_database_backends": STREAMING_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": STREAMING_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


STREAMING_ANALYTICS_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_streaming_analytics_control(slug, payload))
    for capability in STREAMING_CAPABILITIES
}
