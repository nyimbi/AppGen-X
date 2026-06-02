"""Executable improve1 controls for the MRP Engine PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "mrp_engine"
EVENT_CONTRACT = "AppGen-X"
MRP_ENGINE_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
MRP_ENGINE_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.mrp_engine.events"
_BASE_OWNED_TABLES = (
    "mrp_engine_bill_of_material",
    "mrp_engine_bom_revision",
    "mrp_engine_bom_component",
    "mrp_engine_material_demand",
    "mrp_engine_inventory_projection",
    "mrp_engine_mrp_run",
    "mrp_engine_planned_order",
    "mrp_engine_shortage",
    "mrp_engine_shortage_pegging",
    "mrp_engine_supply_demand_pegging",
    "mrp_engine_planning_exception",
    "mrp_engine_policy_rule",
    "mrp_engine_runtime_parameter",
    "mrp_engine_schema_extension",
    "mrp_engine_control_assertion",
    "mrp_engine_governed_model",
    "mrp_engine_appgen_outbox_event",
    "mrp_engine_appgen_inbox_event",
    "mrp_engine_dead_letter_event",
)
MRP_ENGINE_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"mrp_engine_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
MRP_ENGINE_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "InventoryProjectionChanged",
    "OrderDemandProjectionChanged",
    "ForecastSnapshotChanged",
    "ProductionCapacityChanged",
    "QualityHoldChanged",
    "SupplierLeadTimeChanged",
    "ProcurementRouteChanged",
    "ProductionRouteChanged",
)))
MRP_ENGINE_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MRP_ENGINE_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MRP_ENGINE_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "item_id", "site_id", "plan_version_id", "mrp_run_id", "policy_version", "planner_id", "audit_trail", "evidence_references")
_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: 'bom_master_readiness_gate_verified',
    2: 'bom_revision_effectivity_control_verified',
    3: 'bom_component_quantity_governance_verified',
    4: 'alternate_bom_and_routing_selection_verified',
    5: 'substitution_rule_engine_verified',
    6: 'item_planning_profile_completeness_verified',
    7: 'source_rule_governance_verified',
    8: 'demand_projection_normalization_verified',
    9: 'forecast_snapshot_versioning_verified',
    10: 'sales_order_demand_pegging_verified',
    11: 'inventory_projection_freshness_verified',
    12: 'lot_and_reservation_aware_planning_verified',
    13: 'quality_hold_projection_integration_verified',
    14: 'capacity_bucket_modeling_verified',
    15: 'supplier_lead_time_projection_governance_verified',
    16: 'planning_horizon_and_time_bucket_strategy_verified',
    17: 'mrp_run_lifecycle_state_machine_verified',
    18: 'input_snapshot_freeze_verified',
    19: 'multi_scenario_planning_verified',
    20: 'plan_version_control_verified',
    21: 'supply_and_demand_netting_trace_verified',
    22: 'safety_stock_policy_intelligence_verified',
    23: 'lot_sizing_and_rounding_engine_verified',
    24: 'planned_purchase_suggestion_lifecycle_verified',
    25: 'planned_production_order_lifecycle_verified',
    26: 'planned_transfer_order_lifecycle_verified',
    27: 'shortage_severity_model_verified',
    28: 'pegging_graph_explorer_verified',
    29: 'exception_resolution_planning_verified',
    30: 'planned_order_release_governance_verified',
    31: 'release_route_resilience_verified',
    32: 'planning_policy_screening_verified',
    33: 'material_risk_forecasting_verified',
    34: 'capacity_allocation_mechanism_verified',
    35: 'material_allocation_optimization_verified',
    36: 'carbon_aware_planning_windows_verified',
    37: 'supply_availability_proof_verified',
    38: 'immutable_planning_audit_trace_verified',
    39: 'appgen_x_event_reliability_cockpit_verified',
    40: 'boundary_proof_for_mrp_ownership_verified',
    41: 'mrp_workbench_coverage_verified',
    42: 'agent_safe_planning_instruction_intake_verified',
    43: 'agent_safe_release_and_exception_planning_verified',
    44: 'counterfactual_planning_policy_simulation_verified',
    45: 'semantic_bom_and_demand_parsing_verified',
    46: 'shortage_anomaly_detection_verified',
    47: 'planning_mlops_governance_verified',
    48: 'continuous_mrp_control_testing_verified',
    49: 'mrp_readiness_score_verified',
    50: 'end_to_end_material_plan_proof_verified',
}
_DOMAIN_FIELDS: dict[int, tuple[str, ...]] = {
    1: ('bom_id', 'parent_item', 'site', 'revision', 'component_completeness', 'uom_consistency', 'scrap_yield_checked', 'alternate_links', 'lifecycle_status', 'approval_state'),
    2: ('revision_id', 'effectivity_date', 'site', 'lot_range', 'serial_range', 'product_configuration', 'approval_state', 'supersession', 'snapshot_used'),
    3: ('component_id', 'component_uom', 'quantity_basis', 'scrap_percent', 'yield_percent', 'phantom_flag', 'rounding_rule', 'optional_flag', 'effective_dates'),
    4: ('alternate_bom_id', 'selection_policy', 'site', 'demand_type', 'capacity_signal', 'component_availability', 'cost_score', 'quality_hold_status', 'approval_state'),
    5: ('substitution_rule_id', 'substitute_item', 'eligibility', 'priority', 'equivalence_quantity', 'site_restriction', 'customer_restriction', 'quality_status', 'expiry', 'approval_state'),
    6: ('planning_profile_id', 'make_buy_code', 'source_rule', 'lead_time', 'lot_size_policy', 'min_max', 'safety_stock', 'scrap_factor', 'planning_fence', 'planner_owner'),
    7: ('source_rule_id', 'item', 'site', 'source_type', 'supplier_or_site', 'effective_dates', 'capacity', 'lead_time', 'minimum_quantity', 'priority', 'release_route'),
    8: ('demand_projection_id', 'source_type', 'item', 'site', 'quantity', 'due_date', 'priority', 'confidence', 'consumption_policy', 'event_lineage', 'stale_status'),
    9: ('forecast_snapshot_id', 'version', 'horizon', 'bucket', 'model_source', 'confidence', 'override_reason', 'supersession'),
    10: ('sales_order_projection_id', 'source_event', 'due_date', 'priority', 'promised_date', 'quantity', 'projection_freshness', 'pegged_supply'),
    11: ('inventory_projection_id', 'source', 'position_timestamp', 'available_quantity', 'reservations', 'in_transit', 'quality_holds', 'confidence', 'freshness'),
    12: ('lot_id', 'lot_attributes', 'expiry_date', 'reservation_status', 'hold_state', 'fefo_policy', 'allocation_confidence', 'planning_eligible'),
    13: ('quality_hold_projection_id', 'affected_item', 'site', 'lot', 'status', 'release_confidence', 'expected_release_date', 'reason', 'policy_allowed'),
    14: ('capacity_bucket_id', 'work_center', 'site', 'bucket_date', 'available_hours', 'constraints', 'load', 'downtime_projection', 'confidence', 'bottleneck_status'),
    15: ('supplier_lead_time_projection_id', 'supplier', 'source', 'confidence', 'minimum_days', 'expected_days', 'worst_case_days', 'validity', 'risk'),
    16: ('horizon_policy_id', 'item_class', 'site', 'demand_type', 'planner', 'horizon_days', 'bucket_size', 'impact_simulation'),
    17: ('mrp_run_id', 'run_state', 'planner', 'scenario', 'input_snapshot_hashes', 'rule_version', 'parameter_version', 'start_time', 'end_time', 'exception_count', 'approval_state'),
    18: ('input_snapshot_id', 'bom_snapshot', 'demand_snapshot', 'inventory_snapshot', 'reservation_snapshot', 'quality_hold_snapshot', 'capacity_snapshot', 'lead_time_snapshot', 'rule_snapshot', 'parameter_snapshot'),
    19: ('scenario_id', 'input_deltas', 'assumptions', 'owner', 'status', 'comparison_metrics', 'recommended_action'),
    20: ('plan_version_id', 'parent_run', 'scenario', 'input_snapshots', 'calculation_algorithm', 'changed_orders', 'supersession', 'release_status'),
    21: ('netting_trace_id', 'item', 'site', 'bucket', 'gross_demand', 'on_hand_projection', 'reservations', 'scheduled_receipts', 'planned_receipts', 'safety_stock', 'shortage'),
    22: ('safety_stock_policy_id', 'item', 'site', 'bucket', 'demand_variability', 'service_level', 'lead_time_variability', 'seasonality', 'override_reason'),
    23: ('lot_sizing_policy_id', 'minimum_quantity', 'maximum_quantity', 'multiple_quantity', 'fixed_order_quantity', 'rounding_rule', 'source_constraints', 'cost_impact'),
    24: ('purchase_suggestion_id', 'suggestion_state', 'item', 'site', 'supplier', 'quantity', 'due_date', 'lead_time', 'pegged_demand', 'approval', 'consolidation_group'),
    25: ('production_order_id', 'parent_item', 'site', 'quantity', 'start_date', 'due_date', 'bom_revision', 'component_requirements', 'capacity_feasibility', 'release_route'),
    26: ('transfer_order_id', 'source_site', 'destination_site', 'transit_lead_time', 'availability_confidence', 'transportation_projection', 'carbon_impact', 'release_route'),
    27: ('shortage_id', 'quantity', 'days_late', 'demand_priority', 'pegged_orders', 'substitute_options', 'capacity_risk', 'supplier_lead_time', 'customer_impact'),
    28: ('pegging_graph_id', 'demand_node', 'bom_levels', 'supply_projections', 'planned_orders', 'shortages', 'reservations', 'release_routes', 'plan_version'),
    29: ('resolution_plan_id', 'option_type', 'impacted_demand', 'feasibility', 'cost', 'risk', 'lead_time', 'policy_requirements', 'owner', 'expected_event_effects'),
    30: ('release_validation_id', 'release_route', 'source_rule', 'approval_threshold', 'pegging', 'quantity', 'due_date', 'capacity_feasibility', 'material_feasibility', 'stale_input_status'),
    31: ('release_route_health_id', 'route', 'fallback_path', 'retry_policy', 'dead_letter_linkage', 'requeue_logic', 'safe_replay'),
    32: ('policy_screening_id', 'screened_action', 'policy_version', 'attributes_evaluated', 'decision', 'explanation', 'override_path'),
    33: ('material_risk_forecast_id', 'item', 'site', 'bucket', 'demand_variability', 'supplier_lead_time', 'inventory_confidence', 'quality_holds', 'capacity', 'confidence'),
    34: ('capacity_allocation_policy_id', 'priority_rule', 'due_date_rule', 'service_class', 'fairness', 'setup_efficiency', 'contractual_demand', 'simulation_output'),
    35: ('material_allocation_plan_id', 'pegged_demands', 'planned_orders', 'substitutions', 'transfers', 'safety_stock', 'constraints', 'sensitivity_analysis'),
    36: ('carbon_window_id', 'batch_run_window', 'release_timing', 'transfer_choice', 'production_suggestion', 'cost_tradeoff', 'service_tradeoff', 'carbon_tradeoff'),
    37: ('supply_proof_id', 'availability_hash', 'shortage_hash', 'pegging_hash', 'input_freshness_hash', 'planned_supply_hash', 'plan_version', 'verification_api'),
    38: ('audit_trace_id', 'hash_chain', 'bom_change_hash', 'projection_hash', 'run_snapshot_hash', 'netting_hash', 'planned_order_hash', 'release_hash', 'agent_preview_hash'),
    39: ('event_cockpit_id', 'inbox_status', 'outbox_status', 'dead_letter_status', 'idempotency_key', 'retry_count', 'handler_version', 'payload_lineage', 'replay_eligibility'),
    40: ('boundary_proof_id', 'owned_command_tables', 'runtime_tables', 'inventory_table_check', 'order_table_check', 'supplier_table_check', 'production_table_check', 'quality_table_check', 'audit_table_check'),
    41: ('workbench_surface_id', 'bom_explorer', 'revision_control', 'demand_console', 'capacity_board', 'run_control', 'scenario_comparison', 'shortage_board', 'pegging_graph', 'release_queue', 'agent_panels'),
    42: ('instruction_intake_id', 'candidate_facts', 'owned_table_mapping', 'rule_validation', 'permission_check', 'projection_check', 'foreign_mutation_rejection', 'preview_confidence', 'expected_events'),
    43: ('agent_release_plan_id', 'command', 'permission', 'owned_tables', 'idempotency_key', 'emitted_event', 'affected_demand', 'rollback_limits', 'human_approval'),
    44: ('policy_simulation_id', 'parameter_change', 'historical_run', 'active_run', 'shortage_delta', 'planned_order_delta', 'inventory_exposure', 'capacity_load', 'carbon_delta', 'dead_letter_delta'),
    45: ('semantic_parse_id', 'bom_components', 'demand_deltas', 'lead_time_updates', 'substitution_proposals', 'exception_notes', 'confidence', 'validation_results', 'reviewer_approval'),
    46: ('shortage_anomaly_id', 'demand_change_signal', 'component_usage_signal', 'lead_time_signal', 'inventory_drop_signal', 'quality_hold_signal', 'capacity_change_signal', 'release_failure_signal', 'explanation'),
    47: ('planning_model_id', 'model_registry', 'feature_lineage', 'training_window', 'approval_status', 'drift_monitoring', 'explainability', 'fairness_coverage', 'rollback'),
    48: ('control_assertion_id', 'inactive_bom_check', 'stale_inventory_check', 'negative_component_demand_check', 'lot_size_violation_check', 'release_without_pegging_check', 'quality_supply_block_check', 'dead_letter_aging_check', 'agent_preview_bypass_check'),
    49: ('readiness_score_id', 'bom_completeness', 'planning_profiles', 'demand_projection_quality', 'inventory_freshness', 'capacity_coverage', 'source_rules', 'event_reliability', 'ui_coverage', 'boundary_proof', 'agent_safety'),
    50: ('material_plan_proof_id', 'bom_registration', 'demand_projection_ingestion', 'inventory_projection_ingestion', 'capacity_projection', 'mrp_run', 'bom_explosion', 'netting', 'shortage_detection', 'pegging', 'planned_supply_suggestions', 'release_route', 'emitted_events', 'ui_evidence'),
}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {feature_number: _BASE_FIELDS + _DOMAIN_FIELDS[feature_number] + (primary_proof,) for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    8: ("OrderDemandProjectionChanged", "ForecastSnapshotChanged"),
    10: ("OrderDemandProjectionChanged",),
    11: ("InventoryProjectionChanged",),
    13: ("QualityHoldChanged",),
    14: ("ProductionCapacityChanged",),
    15: ("SupplierLeadTimeChanged",),
    26: ("InventoryProjectionChanged",),
    30: ("ProcurementRouteChanged", "ProductionRouteChanged"),
    39: ("AuditEventSealed",),
    40: ("PolicyChanged", "AuditEventSealed"),
    50: ("InventoryProjectionChanged", "OrderDemandProjectionChanged", "ProductionCapacityChanged"),
}
_DOMAIN_MESSAGES: dict[int, str] = {
    1: 'Add BOM readiness checks for parent item, site, revision, component completeness, UOM consistency, scrap/yield, alternate links, lifecycle status, and approval. Block planning against unapproved or incomplete BOMs.',
    2: 'Model revision effectivity by date, site, lot/serial range, product configuration, approval state, and supersession. MRP runs should cite the revision snapshot used for every explosion.',
    3: 'Add component-level UOM, quantity basis, scrap percent, yield, phantom flag, rounding, optionality, and effective dates. Explosion traces should show every quantity transformation.',
    4: 'Add alternate BOM selection policies by site, demand type, capacity, component availability, cost, quality hold, and approval. Simulate alternate selection before changing active planning rules.',
    5: 'Model substitutions with eligibility, priority, equivalence quantity, site/channel/customer restrictions, quality status, expiry, and approval. Shortage recommendations should explain substitute acceptance or rejection.',
    6: 'Add profile readiness checks for make/buy, source rule, lead time, lot-size policy, min/max, safety stock, scrap factor, planning fence, time bucket, and planner ownership.',
    7: 'Define source rules by item, site, supplier/source site, effective dates, capacity, lead time, minimum quantity, priority, cost, and release route. Planned order release should cite source rule evidence.',
    8: 'Normalize demand with source type, item, site, quantity, due date, priority, confidence, consumption policy, event lineage, and stale status. MRP should preserve source demand identity for pegging.',
    9: 'Store forecast snapshots with version, horizon, bucket, model/source, confidence, override reason, and supersession. Scenario runs should compare forecast versions.',
    10: 'Store sales-order demand projections with source event, due date, priority, promised date, quantity, and projection freshness. Peg planned supply and shortages back to these projections.',
    11: 'Track inventory projection source, position timestamp, available quantity, reservations, in-transit, quality holds, confidence, and freshness. Warn or hold runs when critical projections are stale.',
    12: 'Include lot attributes, expiry, reservation status, hold state, FEFO policy, and allocation confidence in supply netting. Planned orders should not consume projected supply that is not planning-eligible.',
    13: 'Project quality holds with affected item/site/lot, status, release confidence, expected release date, and reason. Planning should include conditional supply only when policy allows.',
    14: 'Model capacity buckets by work center/site/date, available hours, constraints, load, downtime projection, confidence, and bottleneck status. Planned production orders should show capacity feasibility.',
    15: 'Store supplier lead-time projection with source, confidence, minimum/expected/worst-case days, supplier/source rule, validity, and risk. Purchase suggestions should include lead-time confidence.',
    16: 'Add horizon/bucket policies by item class, site, demand type, and planner. Simulate changes to show shortage, planned-order count, and release workload impact.',
    17: 'Add run transitions with planner, scenario, input snapshot hashes, rule/parameter versions, start/end time, exception count, approval state, and audit trace.',
    18: 'Create immutable run snapshots for BOM revisions, demand, inventory, reservations, quality holds, capacity, lead times, rules, and parameters. Recalculation should create a new plan version.',
    19: 'Add scenarios with input deltas, assumptions, owner, status, comparison metrics, and recommended action. Workbench should compare shortages, supply orders, capacity load, cost, and carbon.',
    20: 'Version MRP plans with parent run, scenario, input snapshots, calculation algorithm, changed orders, supersession, and release status. Pegging and approvals should reference plan version.',
    21: 'Store netting traces by item/site/bucket showing gross demand, on-hand projection, reservations, scheduled receipts, planned receipts, safety stock, lot size, shortage, and recommended supply.',
    22: 'Model safety stock by item/site/bucket, demand variability, service level, lead-time variability, seasonality, and override reason. Show shortages caused solely by safety-stock policy.',
    23: 'Add lot-sizing policies with minimum, maximum, multiple, fixed order quantity, rounding, source constraints, and cost impact. Planned order traces should show lot-size transformations.',
    24: 'Model suggestion states, item/site, supplier/source, quantity, due date, lead time, pegged demand, approval, consolidation group, and release evidence to procurement.',
    25: 'Model planned production orders with parent item, site, quantity, start/due date, BOM revision, component requirements, capacity feasibility, release route, and production handoff evidence.',
    26: 'Add transfer suggestions with source site, destination site, transit lead time, availability confidence, transportation projection, carbon impact, and release route. Respect site policies and reservations.',
    27: 'Score shortages with quantity, days late, demand priority, pegged orders, substitute options, capacity risk, supplier lead time, and customer/service impact. Workbench should rank shortage resolution.',
    28: 'Build pegging graph views for demand, BOM levels, supply projections, planned orders, shortages, reservations, and release routes. Support upstream/downstream trace by plan version.',
    29: 'Generate resolution plans with option type, impacted demand, feasibility, cost, risk, lead time, policy requirements, owner, and expected event effects. Require approval for high-impact actions.',
    30: 'Validate release route, source rule, approval threshold, pegging, quantity, due date, capacity/material feasibility, and stale input status. Emit `PlannedOrderReleased` with idempotent evidence.',
    31: 'Add release route health, fallback path, retry policy, dead-letter linkage, and requeue logic. Workbench should show route failures and safe replay options.',
    32: 'Screen BOM registration, projection ingestion, run creation, calculation, planned-order release, and exception closure. Store policy version, attributes evaluated, decision, explanation, and override path.',
    33: 'Forecast shortage probability by item/site/bucket using demand variability, supplier lead time, inventory confidence, quality holds, capacity, and historical plan stability. Provide mitigation and confidence.',
    34: 'Add capacity allocation policies for priority, due date, margin/service class, fairness, setup efficiency, and contractual demand. Simulate outcomes before activation.',
    35: 'Optimize material allocation across pegged demands, planned orders, substitutions, transfers, and safety stock with explainable constraints and sensitivity analysis.',
    36: 'Add carbon planning windows for batch runs, release timing, transfer choices, and production suggestions. Show cost/service/carbon tradeoffs rather than silently delaying supply.',
    37: 'Generate redacted proofs for availability, shortage, pegging, input freshness, and planned supply with hash, plan version, and verification API.',
    38: 'Hash-chain BOM changes, projection ingestion, run snapshots, netting, planned orders, shortages, exceptions, releases, agent previews, and event handling. Support temporal reconstruction.',
    39: 'Add inbox/outbox/dead-letter views for idempotency, duplicates, retries, handler version, payload lineage, projection freshness, replay eligibility, and downstream release effects.',
    40: 'Add static/runtime checks proving commands touch only MRP-owned tables plus AppGen-X runtime tables. Include failing fixtures for direct inventory balance, customer order, supplier, production, quality, and audit table access.',
    41: 'Expand UI into BOM explorer, revision control, demand console, forecast snapshots, inventory projections, capacity board, run control, scenario comparison, shortage board, pegging graph, planned order board, release queue, exception resolution, rules, parameters, configuration, events, and agent panels.',
    42: 'Add intake skills that extract candidate planning facts, map them to owned MRP tables, validate rules/permissions/projections, reject foreign-table mutations, and produce side-effect-free previews with confidence, risks, approvals, and expected AppGen-X events.',
    43: 'Require agent plans for BOM registration, projection ingestion, run calculation, planned-order release, substitution, transfer, and exception closure to list command, permission, owned tables, idempotency key, emitted event, affected demand, rollback limits, and human approval.',
    44: 'Simulate parameter and rule changes against historical and active runs, showing shortages, planned orders, inventory exposure, capacity load, release volume, carbon, and dead-letter volume.',
    45: 'Parse instructions into candidate BOM components, demand deltas, lead-time updates, substitution proposals, and exception notes with confidence, validation results, and reviewer approval.',
    46: 'Detect anomalies in demand changes, component usage, lead time, inventory projection drops, quality holds, capacity changes, and release failures. Route findings to planners with explanations.',
    47: 'Add model registry, feature lineage, training windows, approval status, drift monitoring, explainability, fairness/coverage checks, rollback, and release evidence for every planning model.',
    48: 'Add assertions for inactive BOM planning, stale inventory projections, negative component demand, lot-size violations, release without pegging, blocked quality supply use, dead-letter aging, direct foreign-table access, and agent-preview bypass.',
    49: 'Compute readiness from BOM completeness, planning profiles, demand projections, inventory freshness, capacity coverage, source rules, parameter validation, event reliability, UI coverage, boundary proof, controls, model governance, and agent safety.',
    50: 'Add an executable proof scenario covering BOM registration, demand projection ingestion, inventory projection ingestion, capacity projection, MRP run, BOM explosion, netting, shortage detection, pegging, planned purchase and production suggestions, release route, emitted events, UI evidence, controls, and agent explanation.',
}
_HUMAN_CONFIRMATION_FEATURES = (4, 5, 16, 19, 24, 25, 26, 29, 30, 34, 35, 42, 43, 44, 45, 50)
_PROJECTION_ONLY_FEATURES = (8, 10, 11, 13, 14, 15, 26, 30, 39, 40, 50)
_AGENT_PREVIEW_FEATURES = (42, 43, 45, 50)
_NON_MUTATING_FEATURES = (16, 19, 34, 35, 37, 40, 44, 48, 49, 50)
SUPPLY_COMMITMENT_FEATURES = (24, 25, 26, 29, 30, 35, 42, 43, 50)


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
    proof = _PRIMARY_PROOF_FIELDS[capability.feature_number]
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"mrp_engine_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": proof,
        "ui": f"MrpEngine{_camel(capability.slug)}Panel",
        "route": f"POST /mrp-engine/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in MRP_ENGINE_CONTROL_CAPABILITIES}


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
        "event_topic": MRP_ENGINE_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "supply_commitment_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    feature_number = capability.feature_number
    spec = CONTROL_SPECS[feature_number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[feature_number])
    if feature_number in SUPPLY_COMMITMENT_FEATURES and payload.get("supply_commitment_evidence_complete") is not True:
        findings.append("supply-commitment planning actions require pegging, source, feasibility, approval, and release-route evidence")
    if feature_number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("MRP decisions that alter planning policy, substitutions, release, allocation, or supply commitments require human approval before mutation")
    if feature_number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("MRP assistant skills must return side-effect-free previews with owned-table mapping, rule checks, and approval gates")
    if feature_number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("MRP simulations, proofs, controls, readiness scores, and end-to-end proofs must be side-effect-free artifacts")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("inventory, order, forecast, capacity, quality, supplier, procurement, production, policy, and audit context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MRP_ENGINE_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("MRP eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MRP_ENGINE_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary MRP datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("MRP controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_mrp_engine_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MRP_ENGINE_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MRP_ENGINE_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": MRP_ENGINE_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": MRP_ENGINE_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_mrp_engine_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_mrp_engine_control(capability) for capability in MRP_ENGINE_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.mrp-engine-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": MRP_ENGINE_CONTROL_OWNED_TABLES, "declared_dependencies": MRP_ENGINE_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": MRP_ENGINE_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": MRP_ENGINE_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


MRP_ENGINE_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_mrp_engine_control(slug, payload)) for capability in MRP_ENGINE_CONTROL_CAPABILITIES}
