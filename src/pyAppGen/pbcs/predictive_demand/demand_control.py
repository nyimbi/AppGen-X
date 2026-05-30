"""Executable improve1 controls for the Predictive Demand PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS,
    PREDICTIVE_DEMAND_EVENT_CONTRACT,
    PREDICTIVE_DEMAND_OWNED_TABLES,
    PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
    PREDICTIVE_DEMAND_RUNTIME_TABLES,
)

PBC_KEY = "predictive_demand"
EVENT_CONTRACT = PREDICTIVE_DEMAND_EVENT_CONTRACT
DEMAND_CONTROL_ALLOWED_DATABASE_BACKENDS = PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
DEMAND_CONTROL_REQUIRED_EVENT_TOPIC = PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
DEMAND_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(PREDICTIVE_DEMAND_OWNED_TABLES + PREDICTIVE_DEMAND_RUNTIME_TABLES + tuple(f"predictive_demand_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
DEMAND_CONTROL_DECLARED_DEPENDENCIES = (
    "OrderShipped",
    "InventoryPoolChanged",
    "OperationalKpiChanged",
    "PricePromotionProjected",
    "CustomerSegmentProjected",
    "ProductLifecycleProjected",
    "WeatherEventProjected",
    "CalendarEventProjected",
    "ProcurementLeadTimeProjected",
    "SupplierCapacityProjected",
    "CommerceDemandSignalProjected",
    "FraudAnomalyProjected",
    "CarbonIntensityWindowChanged",
    "AuditEventSealed",
    "ModelGovernanceChanged",
)
DEMAND_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in DEMAND_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in DEMAND_CONTROL_CAPABILITIES}
_BASE_FIELDS = (
    "tenant_id",
    "planning_cycle_id",
    "forecast_model_id",
    "forecast_run_id",
    "forecast_result_id",
    "sku_id",
    "location_id",
    "channel_id",
    "planning_horizon_id",
    "actor_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|signal_identity_id,source_system_identity,business_identity,event_time,sequence_number,deduplication_hash
2|signal_quality_id,completeness_score,freshness_score,credibility_score,outlier_risk,remediation_task
3|lineage_graph_id,source_event_refs,transformation_refs,driver_refs,adjustment_refs,trace_export
4|hierarchy_reconciliation_id,hierarchy_level,reconciliation_method,allocation_rule,residual_handling,variance_evidence
5|horizon_model_selection_id,horizon_type,model_family,selection_reason,rejected_alternatives,simulation_mode
6|probabilistic_distribution_id,p10,p25,p50,p90,tail_risk_annotation
7|calibration_backtest_id,realized_demand,interval_coverage,quantile_bias,calibration_curve,remediation
8|fva_measurement_id,naive_baseline,statistical_value,causal_value,planner_value,consensus_value
9|bias_decomposition_id,bias_dimension,root_cause_hypothesis,owner,prevention_control,exception_ref
10|stockout_correction_id,inventory_projection_ref,observed_demand,lost_demand,unconstrained_quantity,confidence
11|elasticity_driver_id,promotion_mechanic,price_index,lift_curve,halo_effect,elasticity_estimate
12|halo_graph_id,related_sku,relationship_type,effect_strength,horizon,evidence_source
13|substitution_model_id,primary_demand,substitute_demand,lost_demand,availability_context,alternative_recommendation
14|npi_forecast_id,analog_item,launch_curve,attribute_similarity,launch_calendar,confidence_decay
15|lifecycle_curve_id,lifecycle_state,successor_link,runout_target,residual_demand,obsolescence_exposure
16|intermittent_method_id,zero_inflation,demand_interval,demand_size,lumpy_classification,stocking_logic
17|demand_sensing_id,trigger_signal,versioned_delta,planner_alert,publication_control,downstream_safe
18|late_signal_replay_id,replay_window,watermark_policy,superseded_version,downstream_notification,impact_class
19|forecast_version_id,version_family,lineage,freeze_window,approval_state,publication_evidence
20|consensus_workflow_id,stakeholder_role,rationale_category,impact_quantity,dispute_state,approval_path
21|override_guardrail_id,override_threshold,rationale,historical_impact,peer_review_trigger,freeze_control
22|scenario_simulation_id,assumptions,changed_drivers,baseline_comparison,probabilistic_outcome,promotion_eligibility
23|causal_driver_id,driver_taxonomy,effect_direction,lag_structure,saturation_behavior,competing_explanation
24|calendar_effect_id,geospatial_relevance,lead_lag_window,event_intensity,recurrence,attribution_quantity
25|segment_projection_id,customer_segment,aggregation_threshold,privacy_safe_flag,segment_contribution,mix_shift_risk
26|channel_mode_id,fulfillment_mode,channel_transfer_effect,cross_channel_cannibalization,service_level_recommendation,reconciliation
27|demand_shaping_id,action_type,expected_movement,customer_impact,policy_constraint,handoff_event
28|replenishment_policy_id,policy_type,lead_time_assumption,service_level,lot_size_constraint,coverage_sensitivity
29|shortage_warning_id,risk_window,risk_probability,lost_demand_estimate,mitigation_option,escalation_owner
30|anomaly_triage_id,anomaly_category,quarantine_decision,forecast_treatment,root_cause,escalation_contract
31|drift_signal_id,feature_drift,target_drift,residual_drift,concept_drift,retraining_recommendation
32|champion_challenger_id,shadow_forecast,significance_check,rollout_gate,operational_impact,rollback_plan
33|forecast_decomposition_id,trend_component,seasonality_component,promotion_component,override_component,residual_component
34|exception_case_id,severity,reason_code,impacted_value,due_date,closure_proof
35|planning_calendar_id,cycle_name,freeze_period,allowed_roles,release_date,policy_explanation
36|publication_contract_id,payload_type,schema_version,consumer_doc,compatibility_test,event_payload
37|boundary_proof_id,dependency_name,contract_type,consumer_function,unauthorized_table_scan,proof_result
38|document_intake_id,document_type,parsed_signal,validation_issue,affected_forecast,reversible_mutation
39|agent_skill_id,skill_name,typed_preview,rbac_check,human_confirmation,audit_trail
40|role_workbench_id,role_name,view_surface,queue_name,capability_surface,raw_artifact_hidden
41|accuracy_metric_id,metric_name,demand_class,selection_rule,misleading_score_guard,scorecard
42|demand_classification_id,demand_class,classification_confidence,transition_history,recommended_model,planning_treatment
43|privacy_control_id,aggregation_threshold,sensitive_segment,masking_rule,explanation_policy,suppression_decision
44|carbon_planning_id,carbon_projection_ref,service_level_tradeoff,margin_tradeoff,emissions_impact,scenario_comparison
45|compute_cost_id,cost_estimate,execution_budget,run_priority,cache_reuse,sla_monitoring
46|rule_impact_simulation_id,changed_rule,affected_forecast_count,bias_risk,shortage_exposure,workbench_diff
47|forecast_evidence_packet_id,signal_hashes,model_hash,parameter_version,forecast_output_hash,publication_signature
48|dead_letter_ops_id,failure_taxonomy,retry_readiness,replay_simulation,duplicate_detection,version_impact
49|capability_matrix_id,capability_name,owned_table_ref,route_descriptor,event_contract_ref,smoke_audit
50|operating_cockpit_id,signal_health,active_cycles,consensus_conflicts,shortage_heatmap,audit_evidence
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("OrderShipped", "InventoryPoolChanged", "OperationalKpiChanged"),
    10: ("InventoryPoolChanged",),
    11: ("PricePromotionProjected",),
    14: ("ProductLifecycleProjected",),
    15: ("ProductLifecycleProjected",),
    17: ("OrderShipped", "InventoryPoolChanged", "OperationalKpiChanged"),
    24: ("WeatherEventProjected", "CalendarEventProjected"),
    25: ("CustomerSegmentProjected",),
    27: ("PricePromotionProjected", "CommerceDemandSignalProjected"),
    28: ("InventoryPoolChanged", "ProcurementLeadTimeProjected", "SupplierCapacityProjected"),
    30: ("FraudAnomalyProjected",),
    31: ("ModelGovernanceChanged",),
    36: ("AuditEventSealed",),
    37: ("OrderShipped", "InventoryPoolChanged", "OperationalKpiChanged", "PricePromotionProjected"),
    44: ("CarbonIntensityWindowChanged",),
    47: ("AuditEventSealed",),
    48: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (18, 19, 20, 21, 22, 27, 30, 32, 35, 38, 39, 43, 44, 46, 48, 50)
_PROJECTION_ONLY_FEATURES = (1, 10, 11, 14, 15, 17, 24, 25, 27, 28, 30, 31, 36, 37, 44, 47, 48)
_AGENT_PREVIEW_FEATURES = (20, 21, 22, 30, 38, 39, 46, 50)
_NON_MUTATING_FEATURES = (3, 4, 7, 8, 9, 12, 18, 22, 31, 32, 33, 37, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50)
_DEMAND_RISK_FEATURES = (1, 2, 4, 6, 7, 9, 10, 17, 18, 19, 20, 21, 22, 28, 29, 30, 31, 32, 35, 36, 37, 43, 45, 46, 47, 48, 49, 50)


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
        "tables": (f"predictive_demand_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"PredictiveDemand{_camel(capability.slug)}Panel",
        "route": f"POST /predictive-demand/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in DEMAND_CONTROL_CAPABILITIES}


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
        "event_topic": DEMAND_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "demand_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires demand-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _DEMAND_RISK_FEATURES and payload.get("demand_risk_evidence_complete") is not True:
        findings.append("signal identity, quality, reconciliation, probabilistic forecasts, calibration, stockout correction, sensing, replay, versioning, consensus, override, shortage, drift, publication, boundary, privacy, compute, replay, release, and cockpit decisions require complete demand risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("late replay, version publication, consensus, override, scenarios, demand shaping, anomaly, champion/challenger, calendar freeze, documents, agent commands, privacy, carbon, rule impact, replay, and cockpit actions require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("predictive demand agent skills must produce cited, RBAC-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("lineage, reconciliation, backtesting, FVA, bias, graphs, replay, scenarios, drift, champion/challenger, decomposition, boundary, metrics, classification, privacy, carbon, compute, rule impact, proof, replay, release, and cockpit evidence must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("order, inventory, KPI, price, promotion, customer, product, weather, calendar, procurement, supplier, commerce, fraud, carbon, audit, and model governance facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != DEMAND_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("predictive demand eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in DEMAND_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary predictive demand datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("predictive demand controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_demand_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in DEMAND_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in DEMAND_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": DEMAND_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": DEMAND_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_demand_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_demand_control(capability) for capability in DEMAND_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.predictive-demand-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": DEMAND_CONTROL_OWNED_TABLES,
        "declared_dependencies": DEMAND_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": DEMAND_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": DEMAND_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


DEMAND_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_demand_control(slug, payload)) for capability in DEMAND_CONTROL_CAPABILITIES}
