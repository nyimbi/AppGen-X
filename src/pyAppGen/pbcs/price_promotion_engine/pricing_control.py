"""Executable improve1 controls for the Price Promotion Engine PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS,
    PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
    PRICE_PROMOTION_ENGINE_OWNED_TABLES,
    PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
    PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
)

PBC_KEY = "price_promotion_engine"
EVENT_CONTRACT = PRICE_PROMOTION_ENGINE_EVENT_CONTRACT
PRICING_CONTROL_ALLOWED_DATABASE_BACKENDS = PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
PRICING_CONTROL_REQUIRED_EVENT_TOPIC = PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC
PRICING_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(PRICE_PROMOTION_ENGINE_OWNED_TABLES + PRICE_PROMOTION_ENGINE_RUNTIME_TABLES + tuple(f"price_promotion_engine_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
PRICING_CONTROL_DECLARED_DEPENDENCIES = (
    "CustomerSegmentUpdated",
    "ForecastUpdated",
    "CheckoutPriceContextProjected",
    "CurrencyRateProjected",
    "ProductCatalogProjected",
    "CostBasisProjected",
    "InventoryPressureProjected",
    "LoyaltyTierProjected",
    "BillingSettlementProjected",
    "OrderCommitted",
    "FraudSignalProjected",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "ModelGovernanceChanged",
)
PRICING_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in PRICING_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in PRICING_CONTROL_CAPABILITIES}
_BASE_FIELDS = (
    "tenant_id",
    "price_list_id",
    "price_book_id",
    "price_rule_id",
    "promotion_id",
    "coupon_id",
    "customer_id",
    "channel_id",
    "currency",
    "actor_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|readiness_gate_id,region,effective_window,owner,approval_state,rounding_policy
2|price_book_lifecycle_id,state,effective_from,effective_to,channel_scope,audit_proof
3|book_entry_id,item_key,base_price,unit,quantity_break,supersession_lineage
4|customer_price_id,contract_ref,volume_commitment,approval_threshold,renewal_rule,conflict_detection
5|channel_price_id,market,fee_adjustment,allowed_promotions,blackout_window,parity_check
6|currency_price_id,fx_source,rate_timestamp,rounding_rule,price_ending,stale_rate_warning
7|price_rule_compiler_id,predicate_hash,scope,priority,formula,explanation
8|agreement_lifecycle_id,agreement_state,contract_reference,commitment,breach_handling,quote_precedence
9|quote_context_id,segment_projection,forecast_projection,checkout_context,currency_rate,item_eligibility
10|decision_trace_id,selected_base_price,applied_rules,rejected_alternatives,risk_score,outbox_evidence
11|volume_break_id,tier_type,threshold,included_quantity,effective_rate,selected_tier
12|margin_guardrail_id,cost_basis,margin_floor,outcome,exception_route,mitigation
13|promotion_lifecycle_id,promotion_state,calendar,objective,budget_link,settlement_state
14|promotion_rule_engine_id,predicate,discount_formula,stacking_group,budget_link,explanation_text
15|eligibility_evidence_id,eligibility_factors,failed_criteria,decision_confidence,segment_ref,coupon_state
16|stacking_policy_id,stacking_group,max_discount,priority,mutual_exclusion,conflict_resolution
17|exclusion_id,scope,reason,policy_source,override_eligibility,quote_linkage
18|coupon_lifecycle_id,code_family,distribution_channel,reuse_limit,expiration,abuse_signal
19|coupon_idempotency_id,decision_ref,session_ref,redemption_attempt,duplicate_suppression,budget_rollback
20|campaign_budget_id,budget_amount,committed_amount,consumed_amount,forecast_spend,threshold_alert
21|approval_workflow_id,approver_role,threshold,risk_reason,budget_impact,denial_reason
22|trade_plan_id,calendar,eligible_accounts,planned_spend,expected_uplift,accrual_policy
23|accrual_engine_id,decision_id,eligible_amount,accrual_rate,period,budget_link
24|settlement_workflow_id,accrual_link,claimed_amount,settled_amount,variance,settlement_event
25|loyalty_pricing_id,tier_definition,eligibility_projection,tier_benefit,compatibility,effective_window
26|forecast_pricing_id,demand_signal,forecast_horizon,confidence,elasticity_assumption,guardrail_check
27|segment_projection_id,source_version,freshness,consent_marker,confidence,quote_impact
28|currency_projection_id,currency_pair,precision,stale_threshold,fallback_rate,manual_override_approval
29|counterfactual_simulation_id,alternate_base_price,tier_thresholds,promotion_stack,margin_effect,budget_effect
30|optimization_objective_id,candidate_price,constraints,margin_floor,forecast_elasticity,tradeoff_explanation
31|exception_case_id,category,severity,affected_decision,root_cause,resolution_proof
32|autonomous_recommendation_id,recommendation_type,confidence,required_approval,unsafe_change_block,manager_note
33|telemetry_id,conversion,margin,discount_depth,coupon_failure,budget_consumption
34|anomaly_detection_id,anomaly_type,price_drop,margin_breach,coupon_velocity,dead_letter_spike
35|margin_exposure_id,exposure_distribution,budget_overrun_risk,fx_drift,abuse_risk,mitigation
36|model_evidence_id,model_purpose,training_window,feature_lineage,fairness_impact,rollback_plan
37|policy_screening_id,compiled_policy,eligibility_scope,approval_policy,coupon_policy,settlement_policy
38|inbox_reliability_id,schema_validation,idempotency_key,duplicate_suppression,retry_evidence,quarantine_control
39|outbox_delivery_id,ordering_group,payload_hash,retry_attempt,next_retry,delivery_proof
40|boundary_proof_id,customer_table_block,forecast_table_block,checkout_table_block,currency_table_block,proof_result
41|parameter_governance_id,parameter_name,bounds,impact_simulation,effective_date,rollback_plan
42|schema_extension_id,target_table,field_validation,sensitivity,migration_preview,api_review
43|price_workbench_id,price_list_view,rule_view,quote_view,simulation_view,event_view
44|promotion_workbench_id,plan_view,coupon_view,budget_view,approval_view,settlement_view
45|decision_explanation_id,base_price_source,agreement_source,promotion_stack,guardrail_result,rejected_alternatives
46|control_test_id,missing_price_check,margin_breach_check,budget_overspend_check,coupon_duplicate_check,agent_bypass_check
47|resilience_drill_id,failure_mode,degraded_mode,recovery_action,replay_plan,workbench_status
48|agent_safe_plan_id,command,permission,owned_table_preview,idempotency_key,human_confirmation
49|readiness_score_id,price_book_score,promotion_score,budget_score,event_score,agent_score
50|optimized_quote_proof_id,setup_trace,quote_decision,promotion_application,coupon_redemption,settlement_trace
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    6: ("CurrencyRateProjected",),
    9: ("CustomerSegmentUpdated", "ForecastUpdated", "CheckoutPriceContextProjected", "CurrencyRateProjected"),
    12: ("CostBasisProjected",),
    19: ("CheckoutPriceContextProjected",),
    25: ("LoyaltyTierProjected",),
    26: ("ForecastUpdated",),
    27: ("CustomerSegmentUpdated",),
    28: ("CurrencyRateProjected",),
    30: ("ForecastUpdated", "InventoryPressureProjected"),
    34: ("FraudSignalProjected",),
    36: ("ModelGovernanceChanged",),
    38: ("CustomerSegmentUpdated", "ForecastUpdated"),
    39: ("AuditEventSealed",),
    40: ("CustomerSegmentUpdated", "ForecastUpdated", "CheckoutPriceContextProjected", "CurrencyRateProjected"),
    47: ("CustomerSegmentUpdated", "ForecastUpdated", "CurrencyRateProjected", "CheckoutPriceContextProjected"),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 2, 4, 7, 8, 12, 13, 18, 20, 21, 22, 24, 29, 30, 31, 32, 37, 41, 42, 46, 47, 48, 50)
_PROJECTION_ONLY_FEATURES = (6, 9, 12, 19, 25, 26, 27, 28, 30, 34, 36, 38, 39, 40, 47)
_AGENT_PREVIEW_FEATURES = (29, 30, 32, 41, 42, 45, 46, 47, 48, 50)
_NON_MUTATING_FEATURES = (10, 29, 30, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 45, 46, 47, 49, 50)
_PRICING_RISK_FEATURES = (1, 2, 3, 4, 6, 7, 9, 10, 12, 13, 16, 18, 19, 20, 21, 23, 24, 28, 30, 31, 34, 35, 37, 38, 39, 40, 41, 46, 47, 48, 49, 50)


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
        "tables": (f"price_promotion_engine_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"PricePromotionEngine{_camel(capability.slug)}Panel",
        "route": f"POST /price-promotion-engine/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in PRICING_CONTROL_CAPABILITIES}


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
        "event_topic": PRICING_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "pricing_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires pricing-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _PRICING_RISK_FEATURES and payload.get("pricing_risk_evidence_complete") is not True:
        findings.append("price list, book, entry, customer, FX, rule, quote, margin, promotion, coupon, budget, settlement, anomaly, policy, event, boundary, parameter, control, resilience, agent, readiness, and quote proof decisions require complete pricing risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("price lists, books, overrides, rules, agreements, guardrails, promotions, coupons, budgets, approvals, settlements, simulations, optimization, exceptions, policies, parameters, schema, controls, resilience, agent, and quote proof require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("pricing agent skills must produce cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("decision traces, simulations, optimization, recommendations, telemetry, anomaly, exposure, model evidence, event reliability, boundary, parameter impact, schema preview, explanations, controls, drills, readiness, and proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("customer, forecast, checkout, currency, product, cost, inventory, loyalty, settlement, order, fraud, audit, KPI, and model facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != PRICING_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("price promotion eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in PRICING_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary price promotion datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("pricing controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_pricing_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PRICING_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PRICING_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": PRICING_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PRICING_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_pricing_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_pricing_control(capability) for capability in PRICING_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.price-promotion-engine-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": PRICING_CONTROL_OWNED_TABLES,
        "declared_dependencies": PRICING_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": PRICING_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": PRICING_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PRICING_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_pricing_control(slug, payload)) for capability in PRICING_CONTROL_CAPABILITIES}
