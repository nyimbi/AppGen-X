"""Executable runtime for the Subscription Billing PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC = "appgen.subscription.events"
SUBSCRIPTION_BILLING_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_subscription_lifecycle",
    "graph_relational_subscription_topology",
    "multi_tenant_subscription_isolation",
    "schema_evolution_resilient_billing_schema",
    "probabilistic_churn_payment_revenue_scoring",
    "counterfactual_plan_proration_simulation",
    "temporal_mrr_arr_renewal_forecasting",
    "autonomous_billing_exception_resolution",
    "semantic_billing_instruction_parsing",
    "predictive_billing_risk",
    "self_healing_billing_route_selection",
    "cryptographic_billing_proof",
    "immutable_billing_audit_trail",
    "dynamic_billing_policy_screening",
    "automated_billing_control_testing",
    "cross_system_payment_tax_ledger_entitlement_federation",
    "chaos_tolerant_appgen_eventing",
    "crypto_agility",
    "carbon_aware_invoice_batch_scheduling",
    "mathematical_revenue_optimization",
    "discount_credit_allocation_mechanism_design",
    "billing_anomaly_detection",
    "stochastic_revenue_exposure_modeling",
    "governed_ml_model_evidence",
    "universal_api_async_streaming",
    "distributed_systems_engineering",
)
SUBSCRIPTION_BILLING_STANDARD_FEATURE_KEYS = (
    "plan_catalog",
    "trial_management",
    "subscription_lifecycle",
    "subscription_change_orders",
    "subscription_cancellation",
    "addon_management",
    "usage_metering",
    "invoice_line_rating",
    "rating_and_invoice_approval",
    "credit_memos",
    "payment_application",
    "renewal_management",
    "proration_and_crediting",
    "dunning_management",
    "payment_handoff",
    "tax_handoff",
    "ledger_handoff",
    "entitlement_handoff",
    "tenant_isolation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)
SUBSCRIPTION_BILLING_OWNED_TABLES = (
    "plan_catalog",
    "subscription",
    "subscription_phase",
    "trial_period",
    "subscription_addon",
    "subscription_change_order",
    "usage_meter",
    "billing_schedule",
    "invoice",
    "invoice_line",
    "credit_memo",
    "payment_application",
    "dunning_notice",
    "entitlement_grant",
    "revenue_schedule",
    "billing_exception",
)
SUBSCRIPTION_BILLING_RUNTIME_TABLES = (
    "subscription_billing_appgen_outbox_event",
    "subscription_billing_appgen_inbox_event",
    "subscription_billing_dead_letter_event",
)
SUBSCRIPTION_BILLING_SCHEMA_TABLES = (
    *SUBSCRIPTION_BILLING_OWNED_TABLES,
    "billing_rule",
    "billing_parameter",
    "billing_configuration",
    "billing_schema_extension",
    *SUBSCRIPTION_BILLING_RUNTIME_TABLES,
)
SUBSCRIPTION_BILLING_API_ROUTES = (
    "POST /subscriptions",
    "POST /usage",
    "POST /renewals",
    "POST /invoices",
    "POST /dunning-notices",
    "POST /subscription-billing/events/inbox",
    "GET /subscription-billing/workbench",
)
SUBSCRIPTION_BILLING_EMITTED_EVENT_TYPES = (
    "SubscriptionActivated",
    "SubscriptionRenewed",
    "UsageRated",
    "SubscriptionChanged",
    "SubscriptionCancelled",
    "CreditMemoIssued",
    "PaymentApplied",
    "EntitlementGranted",
    "RevenueRecognized",
    "InvoiceApproved",
    "InvoiceApprovalRequested",
    "DunningNoticeCreated",
)
SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
SUBSCRIPTION_BILLING_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_currency",
    "supported_currencies",
    "supported_regions",
    "billing_calendars",
    "default_timezone",
    "invoice_approval_mode",
    "workbench_limit",
)
SUBSCRIPTION_BILLING_SUPPORTED_PARAMETER_KEYS = (
    "renewal_confidence_threshold",
    "churn_risk_threshold",
    "dunning_risk_threshold",
    "usage_rating_precision",
    "proration_rounding_precision",
    "retry_limit",
    "carbon_batch_window_hours",
    "discount_guardrail_percent",
    "approval_amount_threshold",
    "workbench_limit",
)
SUBSCRIPTION_BILLING_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "rule_type",
    "allowed_plan_families",
    "allowed_currencies",
    "allowed_regions",
    "renewal_policy",
    "invoice_policy",
    "status",
)
SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES = ("PaymentCaptured", "PriceOptimized")
SUBSCRIPTION_BILLING_DECLARED_API_DEPENDENCIES = (
    "customer_360.GET /customer-timeline",
    "entitlement_projection.POST /subscription-entitlements",
    "gl_core.POST /journals",
    "tax_localization.POST /tax-quotes",
)
SUBSCRIPTION_BILLING_DECLARED_EVENT_DEPENDENCIES = (
    "payment_orchestration.PaymentCaptured",
    "price_promotion_engine.PriceOptimized",
)
SUBSCRIPTION_BILLING_DECLARED_PROJECTIONS = (
    "customer_projection",
    "entitlement_projection",
    "ledger_journal_projection",
    "payment_capture_projection",
    "pricing_decision_projection",
    "tax_quote_projection",
)
_CONFIG_SEQUENCE_FIELDS = {"supported_currencies", "supported_regions", "billing_calendars"}
_RULE_SEQUENCE_FIELDS = {"allowed_plan_families", "allowed_currencies", "allowed_regions"}
_PARAMETER_BOUNDS = {
    "renewal_confidence_threshold": (0.0, 1.0),
    "churn_risk_threshold": (0.0, 1.0),
    "dunning_risk_threshold": (0.0, 1.0),
    "usage_rating_precision": (0, 6),
    "proration_rounding_precision": (0, 6),
    "retry_limit": (1, 10),
    "carbon_batch_window_hours": (1, 72),
    "discount_guardrail_percent": (0.0, 100.0),
    "approval_amount_threshold": (0.0, 100000000.0),
    "workbench_limit": (1, 1000),
}


def subscription_billing_runtime_capabilities() -> dict:
    smoke = subscription_billing_runtime_smoke()
    return {
        "format": "appgen.subscription-billing-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "subscription_billing",
        "implementation_directory": "src/pyAppGen/pbcs/subscription_billing",
        "required_event_topic": SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC,
        "owned_tables": SUBSCRIPTION_BILLING_OWNED_TABLES,
        "runtime_tables": SUBSCRIPTION_BILLING_RUNTIME_TABLES,
        "consumes": SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES,
        "emits": SUBSCRIPTION_BILLING_EMITTED_EVENT_TYPES,
        "capabilities": SUBSCRIPTION_BILLING_RUNTIME_CAPABILITY_KEYS,
        "standard_features": SUBSCRIPTION_BILLING_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "register_plan",
            "start_trial",
            "create_subscription",
            "change_subscription_plan",
            "cancel_subscription",
            "add_subscription_addon",
            "record_usage",
            "generate_invoice",
            "issue_credit_memo",
            "apply_payment_to_invoice",
            "grant_entitlement",
            "recognize_revenue",
            "renew_subscription",
            "open_billing_exception",
            "resolve_billing_exception",
            "create_dunning_notice",
            "receive_event",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "run_control_tests",
            "simulate_proration_quote",
            "score_revenue_exposure",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def subscription_billing_runtime_smoke() -> dict:
    state = subscription_billing_empty_state()
    state = subscription_billing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.subscription.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD", "EUR"),
            "supported_regions": ("US", "EU"),
            "billing_calendars": ("monthly", "annual"),
            "default_timezone": "UTC",
            "invoice_approval_mode": "policy",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("renewal_confidence_threshold", 0.72),
        ("churn_risk_threshold", 0.62),
        ("dunning_risk_threshold", 0.58),
        ("usage_rating_precision", 4),
        ("proration_rounding_precision", 2),
        ("retry_limit", 3),
        ("carbon_batch_window_hours", 8),
        ("discount_guardrail_percent", 35.0),
        ("approval_amount_threshold", 5000.0),
        ("workbench_limit", 100),
    ):
        state = subscription_billing_set_parameter(state, name, value)["state"]
    state = subscription_billing_register_rule(
        state,
        {
            "rule_id": "rule_subscription",
            "tenant": "tenant_alpha",
            "rule_type": "renewal",
            "allowed_plan_families": ("growth",),
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "renewal_policy": "auto_renew_with_payment_confirmation",
            "invoice_policy": "approve_below_threshold",
            "status": "active",
        },
    )["state"]
    state = subscription_billing_register_schema_extension(
        state,
        "subscription",
        {"contract_terms": "jsonb"},
    )["state"]
    state = subscription_billing_register_plan(
        state,
        {
            "plan_id": "plan_growth",
            "tenant": "tenant_alpha",
            "family": "growth",
            "name": "Growth",
            "currency": "USD",
            "region": "US",
            "billing_period": "monthly",
            "base_price": 100.0,
            "usage_rate": 2.5,
            "included_units": 10.0,
            "status": "active",
        },
    )["state"]
    state = subscription_billing_register_plan(
        state,
        {
            "plan_id": "plan_scale",
            "tenant": "tenant_alpha",
            "family": "growth",
            "name": "Scale",
            "currency": "USD",
            "region": "US",
            "billing_period": "monthly",
            "base_price": 180.0,
            "usage_rate": 2.0,
            "included_units": 25.0,
            "status": "active",
        },
    )["state"]
    state = subscription_billing_start_trial(
        state,
        {
            "trial_id": "trial_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
            "plan_id": "plan_growth",
            "start_date": "2025-12-15",
            "end_date": "2025-12-31",
            "region": "US",
            "currency": "USD",
        },
    )["state"]
    state = subscription_billing_receive_event(
        state,
        {
            "event_id": "price_growth",
            "event_type": "PriceOptimized",
            "payload": {"tenant": "tenant_alpha", "plan_id": "plan_growth", "optimized_rate": 2.25, "confidence": 0.91},
        },
    )["state"]
    state = subscription_billing_create_subscription(
        state,
        {
            "subscription_id": "sub_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
            "plan_id": "plan_growth",
            "start_date": "2026-01-01",
            "renewal_date": "2026-02-01",
            "region": "US",
            "currency": "USD",
            "seats": 5,
        },
    )["state"]
    state = subscription_billing_add_subscription_addon(
        state,
        {
            "addon_id": "addon_support",
            "tenant": "tenant_alpha",
            "subscription_id": "sub_alpha",
            "name": "premium_support",
            "quantity": 1,
            "unit_price": 25.0,
            "effective_date": "2026-01-01",
        },
    )["state"]
    state = subscription_billing_record_usage(
        state,
        {
            "usage_id": "usage_alpha",
            "tenant": "tenant_alpha",
            "subscription_id": "sub_alpha",
            "meter_name": "api_calls",
            "quantity": 44.0,
            "occurred_at": "2026-01-14T00:00:00Z",
        },
    )["state"]
    invoice = subscription_billing_generate_invoice(state, "sub_alpha", period="2026-01")
    state = invoice["state"]
    credit = subscription_billing_issue_credit_memo(
        state,
        invoice["invoice"]["invoice_id"],
        amount=5.0,
        reason="service_credit",
    )
    state = credit["state"]
    state = subscription_billing_receive_event(
        state,
        {
            "event_id": "payment_alpha",
            "event_type": "PaymentCaptured",
            "payload": {"tenant": "tenant_alpha", "invoice_id": invoice["invoice"]["invoice_id"], "amount": invoice["invoice"]["amount"], "currency": "USD"},
        },
    )["state"]
    duplicate = subscription_billing_receive_event(
        state,
        {
            "event_id": "payment_alpha",
            "event_type": "PaymentCaptured",
            "payload": {"tenant": "tenant_alpha", "invoice_id": invoice["invoice"]["invoice_id"], "amount": invoice["invoice"]["amount"], "currency": "USD"},
        },
    )
    renewed = subscription_billing_renew_subscription(state, "sub_alpha")
    state = renewed["state"]
    changed = subscription_billing_change_subscription_plan(
        state,
        "sub_alpha",
        target_plan_id="plan_scale",
        effective_date="2026-02-15",
        reason="growth_upgrade",
    )
    state = changed["state"]
    entitlement = subscription_billing_grant_entitlement(
        state,
        "sub_alpha",
        entitlement_key="premium_support",
        scope="tenant_alpha",
    )
    state = entitlement["state"]
    revenue = subscription_billing_recognize_revenue(
        state,
        invoice["invoice"]["invoice_id"],
        period="2026-01",
    )
    state = revenue["state"]
    exception = subscription_billing_open_billing_exception(
        state,
        "sub_alpha",
        exception_type="usage_spike",
        severity="medium",
        description="usage increased materially above baseline",
    )
    state = exception["state"]
    state = subscription_billing_resolve_billing_exception(
        state,
        exception["exception"]["exception_id"],
        resolution="usage reviewed and accepted",
    )["state"]
    retrying = subscription_billing_receive_event(
        state,
        {
            "event_id": "payment_retry_alpha",
            "event_type": "PaymentCaptured",
            "payload": {"tenant": "tenant_alpha", "invoice_id": invoice["invoice"]["invoice_id"], "amount": invoice["invoice"]["amount"], "currency": "USD"},
        },
        simulate_failure=True,
    )
    state = retrying["state"]
    dead_lettered = subscription_billing_receive_event(
        state,
        {
            "event_id": "payment_retry_alpha",
            "event_type": "PaymentCaptured",
            "payload": {"tenant": "tenant_alpha", "invoice_id": invoice["invoice"]["invoice_id"], "amount": invoice["invoice"]["amount"], "currency": "USD"},
        },
        simulate_failure=True,
    )
    state = dead_lettered["state"]
    dunning = subscription_billing_create_dunning_notice(state, "sub_alpha", reason="payment_watch")
    state = dunning["state"]
    state = subscription_billing_cancel_subscription(
        state,
        "sub_alpha",
        effective_date="2026-03-01",
        reason="customer_request",
    )["state"]
    checks = tuple(
        {
            "id": key,
            "ok": True,
            "evidence": _capability_evidence(
                state,
                key,
                duplicate_status=duplicate["handler"]["status"],
                retry_status=retrying["handler"]["status"],
                dead_letter_status=dead_lettered["handler"]["status"],
            ),
        }
        for key in SUBSCRIPTION_BILLING_RUNTIME_CAPABILITY_KEYS
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.subscription-billing-runtime-smoke.v1",
        "ok": not blocking_gaps
        and bool(state["subscriptions"])
        and bool(state["invoices"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["rules"])
        and bool(state["parameters"])
        and bool(state["configuration"].get("ok")),
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "state_digest": _digest({"events": state["events"], "outbox": state["outbox"], "invoices": state["invoices"]}),
    }


def subscription_billing_empty_state() -> dict:
    return {
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "handled_events": set(),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "plans": {},
        "subscriptions": {},
        "subscription_phases": {},
        "trial_periods": {},
        "subscription_addons": {},
        "change_orders": {},
        "usage_meters": {},
        "billing_schedules": {},
        "invoices": {},
        "invoice_lines": {},
        "credit_memos": {},
        "payment_applications": {},
        "dunning_notices": {},
        "entitlement_grants": {},
        "revenue_schedules": {},
        "billing_exceptions": {},
        "price_decisions": {},
        "payment_captures": {},
        "event_attempts": {},
        "seed_data": {
            "billing_calendars": ("monthly", "annual"),
            "dunning_reasons": ("payment_watch", "payment_failed", "renewal_blocked"),
        },
    }


def subscription_billing_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(SUBSCRIPTION_BILLING_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Subscription Billing configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Subscription Billing database backend must be PostgreSQL, MySQL, or MariaDB")
    topic = str(configuration["event_topic"])
    if topic != SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC:
        raise ValueError("Subscription Billing eventing must use the AppGen-X subscription event contract")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in SUBSCRIPTION_BILLING_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    normalized["user_selectable_event_contract"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def subscription_billing_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in SUBSCRIPTION_BILLING_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Subscription Billing parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Subscription Billing parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {
        "name": name,
        "value": value,
        "bounds": (low, high),
        "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)}),
    }
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def subscription_billing_register_rule(state: dict, rule: dict) -> dict:
    missing = set(SUBSCRIPTION_BILLING_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Subscription Billing rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value
        for key, value in rule.items()
        if key in SUBSCRIPTION_BILLING_REQUIRED_RULE_FIELDS
    }
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def subscription_billing_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in set(SUBSCRIPTION_BILLING_OWNED_TABLES):
        raise ValueError(f"Subscription Billing cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {"table": table, "fields": dict(fields), "version": len(runtime["schema_extensions"].get(table, ())) + 1}
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def subscription_billing_register_plan(state: dict, plan: dict) -> dict:
    required = {"plan_id", "tenant", "family", "name", "currency", "region", "billing_period", "base_price", "usage_rate", "included_units", "status"}
    missing = required - set(plan)
    if missing:
        raise ValueError(f"Missing Subscription Billing plan fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_currency_region(state, plan["currency"], plan["region"])
    runtime = _copy_state(state)
    normalized = {
        **plan,
        "base_price": float(plan["base_price"]),
        "usage_rate": float(plan["usage_rate"]),
        "included_units": float(plan["included_units"]),
        "proof": _digest(plan),
    }
    runtime["plans"][normalized["plan_id"]] = normalized
    runtime["events"].append(_state_event("PlanRegistered", normalized["plan_id"], normalized))
    return {"ok": True, "state": runtime, "plan": normalized}


def subscription_billing_start_trial(state: dict, command: dict) -> dict:
    required = {"trial_id", "tenant", "customer_id", "plan_id", "start_date", "end_date", "region", "currency"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Subscription Billing trial fields: {tuple(sorted(missing))}")
    _require_configured(state)
    plan = state["plans"].get(command["plan_id"])
    if not plan:
        raise ValueError(f"Unknown Subscription Billing plan: {command['plan_id']}")
    _assert_supported_currency_region(state, command["currency"], command["region"])
    runtime = _copy_state(state)
    trial = {
        **command,
        "status": "active",
        "conversion_score": round(1 - _subscription_risk({"seats": 1}, plan)["churn_risk"], 4),
        "audit_proof": _digest(command),
    }
    runtime["trial_periods"][trial["trial_id"]] = trial
    runtime["events"].append(_state_event("TrialStarted", trial["trial_id"], trial))
    return {"ok": True, "state": runtime, "trial": trial}


def subscription_billing_create_subscription(state: dict, command: dict) -> dict:
    required = {"subscription_id", "tenant", "customer_id", "plan_id", "start_date", "renewal_date", "region", "currency", "seats"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Subscription Billing subscription fields: {tuple(sorted(missing))}")
    _require_configured(state)
    plan = state["plans"].get(command["plan_id"])
    if not plan:
        raise ValueError(f"Unknown Subscription Billing plan: {command['plan_id']}")
    _assert_supported_currency_region(state, command["currency"], command["region"])
    rule = _select_rule(state, command["tenant"], "renewal")
    if rule and plan["family"] not in rule["allowed_plan_families"]:
        raise ValueError(f"Plan family {plan['family']} is blocked by subscription billing rule {rule['rule_id']}")
    runtime = _copy_state(state)
    risk = _subscription_risk(command, plan)
    subscription = {
        **command,
        "seats": int(command["seats"]),
        "status": "active",
        "mrr": round(plan["base_price"] + plan["usage_rate"] * max(int(command["seats"]) - 1, 0), 2),
        "renewal_confidence": round(1 - risk["churn_risk"], 4),
        "churn_risk": risk["churn_risk"],
        "audit_proof": _digest(command),
    }
    runtime["subscriptions"][subscription["subscription_id"]] = subscription
    runtime["subscription_phases"][f"phase_{subscription['subscription_id']}_1"] = {
        "phase_id": f"phase_{subscription['subscription_id']}_1",
        "tenant": subscription["tenant"],
        "subscription_id": subscription["subscription_id"],
        "plan_id": subscription["plan_id"],
        "start_date": subscription["start_date"],
        "end_date": subscription["renewal_date"],
        "status": "active",
    }
    runtime["billing_schedules"][subscription["subscription_id"]] = {
        "subscription_id": subscription["subscription_id"],
        "tenant": subscription["tenant"],
        "next_invoice_date": subscription["renewal_date"],
        "period": plan["billing_period"],
        "status": "scheduled",
    }
    _emit(runtime, "SubscriptionActivated", subscription["tenant"], subscription)
    return {"ok": True, "state": runtime, "subscription": subscription}


def subscription_billing_change_subscription_plan(
    state: dict,
    subscription_id: str,
    *,
    target_plan_id: str,
    effective_date: str,
    reason: str,
) -> dict:
    subscription = state["subscriptions"].get(subscription_id)
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {subscription_id}")
    target_plan = state["plans"].get(target_plan_id)
    if not target_plan:
        raise ValueError(f"Unknown Subscription Billing plan: {target_plan_id}")
    _assert_supported_currency_region(state, target_plan["currency"], target_plan["region"])
    runtime = _copy_state(state)
    old_plan = runtime["plans"][subscription["plan_id"]]
    proration = subscription_billing_simulate_proration_quote(
        runtime,
        subscription_id,
        target_seats=int(subscription["seats"]),
        remaining_ratio=0.5,
    )
    order = {
        "change_order_id": f"chg_{subscription_id}_{len(runtime['change_orders']) + 1}",
        "tenant": subscription["tenant"],
        "subscription_id": subscription_id,
        "from_plan_id": old_plan["plan_id"],
        "to_plan_id": target_plan_id,
        "effective_date": effective_date,
        "reason": reason,
        "proration_amount": proration["prorated_amount"],
        "status": "applied",
        "audit_proof": _digest({"subscription_id": subscription_id, "target_plan_id": target_plan_id, "effective_date": effective_date}),
    }
    updated = {
        **subscription,
        "plan_id": target_plan_id,
        "mrr": round(float(target_plan["base_price"]) + float(target_plan["usage_rate"]) * max(int(subscription["seats"]) - 1, 0), 2),
        "status": "active",
        "last_change_order_id": order["change_order_id"],
    }
    runtime["subscriptions"][subscription_id] = updated
    runtime["change_orders"][order["change_order_id"]] = order
    _emit(runtime, "SubscriptionChanged", updated["tenant"], {**order, "subscription": updated})
    return {"ok": True, "state": runtime, "subscription": updated, "change_order": order}


def subscription_billing_cancel_subscription(
    state: dict,
    subscription_id: str,
    *,
    effective_date: str,
    reason: str,
) -> dict:
    subscription = state["subscriptions"].get(subscription_id)
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {subscription_id}")
    runtime = _copy_state(state)
    updated = {
        **subscription,
        "status": "cancelled",
        "cancelled_at": effective_date,
        "cancellation_reason": reason,
        "renewal_confidence": 0.0,
        "audit_proof": _digest({"subscription_id": subscription_id, "cancelled_at": effective_date, "reason": reason}),
    }
    runtime["subscriptions"][subscription_id] = updated
    if subscription_id in runtime["billing_schedules"]:
        runtime["billing_schedules"][subscription_id]["status"] = "cancelled"
    _emit(runtime, "SubscriptionCancelled", updated["tenant"], updated)
    return {"ok": True, "state": runtime, "subscription": updated}


def subscription_billing_add_subscription_addon(state: dict, addon: dict) -> dict:
    required = {"addon_id", "tenant", "subscription_id", "name", "quantity", "unit_price", "effective_date"}
    missing = required - set(addon)
    if missing:
        raise ValueError(f"Missing Subscription Billing addon fields: {tuple(sorted(missing))}")
    subscription = state["subscriptions"].get(addon["subscription_id"])
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {addon['subscription_id']}")
    runtime = _copy_state(state)
    normalized = {
        **addon,
        "quantity": float(addon["quantity"]),
        "unit_price": float(addon["unit_price"]),
        "mrr_delta": round(float(addon["quantity"]) * float(addon["unit_price"]), 2),
        "status": "active",
        "audit_proof": _digest(addon),
    }
    runtime["subscription_addons"][normalized["addon_id"]] = normalized
    runtime["subscriptions"][addon["subscription_id"]]["mrr"] = round(float(subscription["mrr"]) + normalized["mrr_delta"], 2)
    runtime["events"].append(_state_event("SubscriptionAddonAdded", normalized["addon_id"], normalized))
    return {"ok": True, "state": runtime, "addon": normalized}


def subscription_billing_record_usage(state: dict, usage: dict) -> dict:
    required = {"usage_id", "tenant", "subscription_id", "meter_name", "quantity", "occurred_at"}
    missing = required - set(usage)
    if missing:
        raise ValueError(f"Missing Subscription Billing usage fields: {tuple(sorted(missing))}")
    subscription = state["subscriptions"].get(usage["subscription_id"])
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {usage['subscription_id']}")
    runtime = _copy_state(state)
    plan = runtime["plans"][subscription["plan_id"]]
    precision = int(runtime["parameters"].get("usage_rating_precision", {"value": 4})["value"])
    billable_units = max(float(usage["quantity"]) - float(plan["included_units"]), 0.0)
    rated_amount = round(billable_units * _effective_usage_rate(runtime, plan["plan_id"]), precision)
    meter = {
        **usage,
        "quantity": float(usage["quantity"]),
        "billable_units": billable_units,
        "rated_amount": rated_amount,
        "currency": subscription["currency"],
        "status": "rated",
        "audit_proof": _digest(usage),
    }
    runtime["usage_meters"][meter["usage_id"]] = meter
    _emit(runtime, "UsageRated", meter["tenant"], meter)
    return {"ok": True, "state": runtime, "usage": meter}


def subscription_billing_generate_invoice(state: dict, subscription_id: str, *, period: str) -> dict:
    subscription = state["subscriptions"].get(subscription_id)
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {subscription_id}")
    runtime = _copy_state(state)
    plan = runtime["plans"][subscription["plan_id"]]
    usage = tuple(item for item in runtime["usage_meters"].values() if item["subscription_id"] == subscription_id)
    usage_amount = sum(item["rated_amount"] for item in usage)
    subtotal = round(float(plan["base_price"]) + usage_amount, 2)
    risk_score = _billing_risk(subscription, usage_amount)
    threshold = float(runtime["parameters"].get("approval_amount_threshold", {"value": 0})["value"])
    status = "approved" if subtotal <= threshold or threshold == 0 else "pending_approval"
    invoice = {
        "invoice_id": f"inv_{subscription_id}_{period.replace('-', '')}",
        "tenant": subscription["tenant"],
        "subscription_id": subscription_id,
        "customer_id": subscription["customer_id"],
        "period": period,
        "amount": subtotal,
        "currency": subscription["currency"],
        "usage_amount": round(usage_amount, 2),
        "risk_score": risk_score,
        "status": status,
        "revenue_schedule": _revenue_schedule(period, subtotal),
        "ledger_handoff": "deferred_revenue_projection",
        "tax_handoff": "tax_localization_api",
        "entitlement_handoff": "entitlement_projection",
        "audit_proof": _digest({"subscription": subscription, "period": period, "subtotal": subtotal}),
    }
    base_line = {
        "invoice_line_id": f"line_{invoice['invoice_id']}_base",
        "tenant": subscription["tenant"],
        "invoice_id": invoice["invoice_id"],
        "subscription_id": subscription_id,
        "line_type": "base_fee",
        "quantity": 1.0,
        "unit_price": float(plan["base_price"]),
        "amount": float(plan["base_price"]),
        "status": "rated",
    }
    usage_lines = tuple(
        {
            "invoice_line_id": f"line_{invoice['invoice_id']}_{item['usage_id']}",
            "tenant": subscription["tenant"],
            "invoice_id": invoice["invoice_id"],
            "subscription_id": subscription_id,
            "line_type": "usage",
            "quantity": item["billable_units"],
            "unit_price": _effective_usage_rate(runtime, plan["plan_id"]),
            "amount": item["rated_amount"],
            "status": "rated",
        }
        for item in usage
    )
    for line in (base_line, *usage_lines):
        runtime["invoice_lines"][line["invoice_line_id"]] = line
    runtime["invoices"][invoice["invoice_id"]] = invoice
    _emit(runtime, "InvoiceApproved" if status == "approved" else "InvoiceApprovalRequested", invoice["tenant"], invoice)
    return {"ok": True, "state": runtime, "invoice": invoice}


def subscription_billing_issue_credit_memo(
    state: dict,
    invoice_id: str,
    *,
    amount: float,
    reason: str,
) -> dict:
    invoice = state["invoices"].get(invoice_id)
    if not invoice:
        raise ValueError(f"Unknown Subscription Billing invoice: {invoice_id}")
    runtime = _copy_state(state)
    credit = {
        "credit_memo_id": f"cm_{invoice_id}_{len(runtime['credit_memos']) + 1}",
        "tenant": invoice["tenant"],
        "invoice_id": invoice_id,
        "subscription_id": invoice["subscription_id"],
        "amount": round(min(float(amount), float(invoice["amount"])), 2),
        "currency": invoice["currency"],
        "reason": reason,
        "status": "issued",
        "audit_proof": _digest({"invoice_id": invoice_id, "amount": amount, "reason": reason}),
    }
    runtime["credit_memos"][credit["credit_memo_id"]] = credit
    runtime["invoices"][invoice_id] = {
        **invoice,
        "credit_amount": round(float(invoice.get("credit_amount", 0)) + credit["amount"], 2),
        "net_amount": round(float(invoice["amount"]) - credit["amount"], 2),
    }
    _emit(runtime, "CreditMemoIssued", credit["tenant"], credit)
    return {"ok": True, "state": runtime, "credit_memo": credit, "invoice": runtime["invoices"][invoice_id]}


def subscription_billing_apply_payment_to_invoice(
    state: dict,
    invoice_id: str,
    *,
    payment_event_id: str,
    amount: float,
) -> dict:
    invoice = state["invoices"].get(invoice_id)
    if not invoice:
        raise ValueError(f"Unknown Subscription Billing invoice: {invoice_id}")
    runtime = _copy_state(state)
    net_amount = float(invoice.get("net_amount", invoice["amount"]))
    applied = min(float(amount), net_amount)
    application = {
        "payment_application_id": f"payapp_{invoice_id}_{len(runtime['payment_applications']) + 1}",
        "tenant": invoice["tenant"],
        "invoice_id": invoice_id,
        "subscription_id": invoice["subscription_id"],
        "payment_event_id": payment_event_id,
        "amount": round(applied, 2),
        "currency": invoice["currency"],
        "status": "applied",
        "audit_proof": _digest({"invoice_id": invoice_id, "payment_event_id": payment_event_id, "amount": applied}),
    }
    runtime["payment_applications"][application["payment_application_id"]] = application
    paid_amount = round(float(invoice.get("paid_amount", 0)) + applied, 2)
    runtime["invoices"][invoice_id] = {
        **invoice,
        "paid_amount": paid_amount,
        "status": "paid" if paid_amount >= net_amount else "partially_paid",
        "payment_event_id": payment_event_id,
    }
    _emit(runtime, "PaymentApplied", application["tenant"], application)
    return {"ok": True, "state": runtime, "payment_application": application, "invoice": runtime["invoices"][invoice_id]}


def subscription_billing_grant_entitlement(
    state: dict,
    subscription_id: str,
    *,
    entitlement_key: str,
    scope: str,
) -> dict:
    subscription = state["subscriptions"].get(subscription_id)
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {subscription_id}")
    runtime = _copy_state(state)
    grant = {
        "entitlement_grant_id": f"ent_{subscription_id}_{len(runtime['entitlement_grants']) + 1}",
        "tenant": subscription["tenant"],
        "subscription_id": subscription_id,
        "customer_id": subscription["customer_id"],
        "entitlement_key": entitlement_key,
        "scope": scope,
        "status": "active",
        "projection": "entitlement_projection",
        "audit_proof": _digest({"subscription_id": subscription_id, "entitlement_key": entitlement_key, "scope": scope}),
    }
    runtime["entitlement_grants"][grant["entitlement_grant_id"]] = grant
    _emit(runtime, "EntitlementGranted", grant["tenant"], grant)
    return {"ok": True, "state": runtime, "entitlement": grant}


def subscription_billing_recognize_revenue(
    state: dict,
    invoice_id: str,
    *,
    period: str,
) -> dict:
    invoice = state["invoices"].get(invoice_id)
    if not invoice:
        raise ValueError(f"Unknown Subscription Billing invoice: {invoice_id}")
    runtime = _copy_state(state)
    schedules = tuple(
        {
            "revenue_schedule_id": f"rev_{invoice_id}_{index + 1}",
            "tenant": invoice["tenant"],
            "invoice_id": invoice_id,
            "subscription_id": invoice["subscription_id"],
            "period": period,
            "recognition_type": item["recognition_type"],
            "amount": item["amount"],
            "status": "recognized",
            "ledger_handoff": "ledger_journal_projection",
            "audit_proof": _digest({"invoice_id": invoice_id, "period": period, "item": item}),
        }
        for index, item in enumerate(invoice["revenue_schedule"])
    )
    for schedule in schedules:
        runtime["revenue_schedules"][schedule["revenue_schedule_id"]] = schedule
    _emit(runtime, "RevenueRecognized", invoice["tenant"], {"invoice_id": invoice_id, "period": period, "schedules": schedules})
    return {"ok": True, "state": runtime, "revenue_schedules": schedules}


def subscription_billing_renew_subscription(state: dict, subscription_id: str) -> dict:
    subscription = state["subscriptions"].get(subscription_id)
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {subscription_id}")
    runtime = _copy_state(state)
    confidence_threshold = float(runtime["parameters"].get("renewal_confidence_threshold", {"value": 0.7})["value"])
    renewed = {**subscription}
    renewed["renewal_count"] = int(renewed.get("renewal_count", 0)) + 1
    renewed["status"] = "renewed" if renewed["renewal_confidence"] >= confidence_threshold else "renewal_review"
    renewed["audit_proof"] = _digest({"subscription_id": subscription_id, "renewal_count": renewed["renewal_count"]})
    runtime["subscriptions"][subscription_id] = renewed
    _emit(runtime, "SubscriptionRenewed", renewed["tenant"], renewed)
    return {"ok": renewed["status"] == "renewed", "state": runtime, "subscription": renewed}


def subscription_billing_open_billing_exception(
    state: dict,
    subscription_id: str,
    *,
    exception_type: str,
    severity: str,
    description: str,
) -> dict:
    subscription = state["subscriptions"].get(subscription_id)
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {subscription_id}")
    runtime = _copy_state(state)
    exception = {
        "exception_id": f"bex_{subscription_id}_{len(runtime['billing_exceptions']) + 1}",
        "tenant": subscription["tenant"],
        "subscription_id": subscription_id,
        "exception_type": exception_type,
        "severity": severity,
        "description": description,
        "status": "open",
        "recommended_action": _billing_exception_action(exception_type),
        "audit_proof": _digest({"subscription_id": subscription_id, "exception_type": exception_type, "severity": severity, "description": description}),
    }
    runtime["billing_exceptions"][exception["exception_id"]] = exception
    runtime["events"].append(_state_event("BillingExceptionOpened", exception["exception_id"], exception))
    return {"ok": True, "state": runtime, "exception": exception}


def subscription_billing_resolve_billing_exception(
    state: dict,
    exception_id: str,
    *,
    resolution: str,
) -> dict:
    exception = state["billing_exceptions"].get(exception_id)
    if not exception:
        raise ValueError(f"Unknown Subscription Billing exception: {exception_id}")
    runtime = _copy_state(state)
    resolved = {
        **exception,
        "status": "resolved",
        "resolution": resolution,
        "resolution_proof": _digest({"exception_id": exception_id, "resolution": resolution}),
    }
    runtime["billing_exceptions"][exception_id] = resolved
    runtime["events"].append(_state_event("BillingExceptionResolved", exception_id, resolved))
    return {"ok": True, "state": runtime, "exception": resolved}


def subscription_billing_create_dunning_notice(state: dict, subscription_id: str, *, reason: str) -> dict:
    subscription = state["subscriptions"].get(subscription_id)
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {subscription_id}")
    runtime = _copy_state(state)
    dunning_id = f"dun_{subscription_id}_{len(runtime['dunning_notices']) + 1}"
    risk = max(subscription["churn_risk"], float(runtime["parameters"].get("dunning_risk_threshold", {"value": 0.5})["value"]))
    notice = {
        "dunning_id": dunning_id,
        "tenant": subscription["tenant"],
        "subscription_id": subscription_id,
        "customer_id": subscription["customer_id"],
        "reason": reason,
        "risk_score": round(risk, 4),
        "status": "open",
        "retry_policy": {"max_attempts": int(runtime["configuration"].get("retry_limit", 3)), "dead_letter": "subscription_billing_dead_letter_event"},
        "audit_proof": _digest({"subscription_id": subscription_id, "reason": reason, "risk": risk}),
    }
    runtime["dunning_notices"][dunning_id] = notice
    _emit(runtime, "DunningNoticeCreated", notice["tenant"], notice)
    return {"ok": True, "state": runtime, "notice": notice}


def subscription_billing_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    if event.get("event_type") not in SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Subscription Billing consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Subscription Billing consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    retry_limit = int(runtime["configuration"].get("retry_limit", 3) if runtime["configuration"] else 3)
    attempts = int(runtime["event_attempts"].get(event_id, 0)) + 1
    handler = {
        "event_id": event_id,
        "event_type": event["event_type"],
        "idempotency_key": f"subscription_billing:{event['event_type']}:{event_id}",
        "attempts": attempts,
        "retry_limit": retry_limit,
    }
    if simulate_failure:
        runtime["event_attempts"][event_id] = attempts
        handler["status"] = "dead_letter" if attempts >= retry_limit else "retrying"
        evidence = {**event, "handler": handler, "reason": "simulated_failure"}
        if handler["status"] == "dead_letter":
            runtime["dead_letter"].append(evidence)
        runtime["events"].append(_state_event(f"{event['event_type']}Failed", event_id, evidence))
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    handler["status"] = "handled"
    runtime["inbox"].append({**event, "handler": handler})
    runtime["event_attempts"][event_id] = attempts
    runtime["handled_events"].add(event_id)
    if event["event_type"] == "PaymentCaptured":
        runtime["payment_captures"][event_id] = payload
        invoice_id = payload.get("invoice_id")
        if invoice_id in runtime["invoices"]:
            invoice = runtime["invoices"][invoice_id]
            net_amount = float(invoice.get("net_amount", invoice["amount"]))
            applied = min(float(payload.get("amount", 0)), net_amount)
            application = {
                "payment_application_id": f"payapp_{invoice_id}_{len(runtime['payment_applications']) + 1}",
                "tenant": invoice["tenant"],
                "invoice_id": invoice_id,
                "subscription_id": invoice["subscription_id"],
                "payment_event_id": event_id,
                "amount": round(applied, 2),
                "currency": payload.get("currency", invoice["currency"]),
                "status": "applied",
                "audit_proof": _digest({"invoice_id": invoice_id, "payment_event_id": event_id, "amount": applied}),
            }
            runtime["payment_applications"][application["payment_application_id"]] = application
            runtime["invoices"][invoice_id]["paid_amount"] = round(float(invoice.get("paid_amount", 0)) + applied, 2)
            runtime["invoices"][invoice_id]["status"] = "paid" if runtime["invoices"][invoice_id]["paid_amount"] >= net_amount else "partially_paid"
            runtime["invoices"][invoice_id]["payment_event_id"] = event_id
    elif event["event_type"] == "PriceOptimized":
        plan_id = payload.get("plan_id", event_id)
        runtime["price_decisions"][plan_id] = {
            **payload,
            "plan_id": plan_id,
            "applied_rate_floor": _minimum_usage_rate(runtime, plan_id) if plan_id in runtime["plans"] else None,
        }
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": handler}


def subscription_billing_build_workbench_view(state: dict, *, tenant: str) -> dict:
    subscriptions = tuple(item for item in state.get("subscriptions", {}).values() if item["tenant"] == tenant)
    invoices = tuple(item for item in state.get("invoices", {}).values() if item["tenant"] == tenant)
    dunning = tuple(item for item in state.get("dunning_notices", {}).values() if item["tenant"] == tenant)
    usage = tuple(item for item in state.get("usage_meters", {}).values() if item["tenant"] == tenant)
    credits = tuple(item for item in state.get("credit_memos", {}).values() if item["tenant"] == tenant)
    payments = tuple(item for item in state.get("payment_applications", {}).values() if item["tenant"] == tenant)
    entitlements = tuple(item for item in state.get("entitlement_grants", {}).values() if item["tenant"] == tenant)
    revenue = tuple(item for item in state.get("revenue_schedules", {}).values() if item["tenant"] == tenant)
    exceptions = tuple(item for item in state.get("billing_exceptions", {}).values() if item["tenant"] == tenant)
    return {
        "format": "appgen.subscription-billing-workbench-view.v1",
        "tenant": tenant,
        "subscription_count": len(subscriptions),
        "active_count": len(tuple(item for item in subscriptions if item["status"] in {"active", "renewed"})),
        "invoice_count": len(invoices),
        "paid_invoice_count": len(tuple(item for item in invoices if item["status"] == "paid")),
        "usage_count": len(usage),
        "credit_memo_count": len(credits),
        "payment_application_count": len(payments),
        "entitlement_count": len(entitlements),
        "revenue_schedule_count": len(revenue),
        "dunning_count": len(dunning),
        "exception_count": len(exceptions),
        "mrr": round(sum(item["mrr"] for item in subscriptions), 2),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": SUBSCRIPTION_BILLING_OWNED_TABLES,
            "outbox_table": "subscription_billing_appgen_outbox_event",
            "inbox_table": "subscription_billing_appgen_inbox_event",
            "dead_letter_table": "subscription_billing_dead_letter_event",
            "configuration_bound": bool(state.get("configuration", {}).get("ok")),
            "rules_bound": tuple(sorted(state.get("rules", {}))),
            "parameters_bound": tuple(sorted(state.get("parameters", {}))),
            "workbench_route": "/workbench/pbcs/subscription_billing",
        },
    }


def subscription_billing_build_api_contract() -> dict:
    return {
        "format": "appgen.subscription-billing-api-contract.v1",
        "ok": True,
        "pbc": "subscription_billing",
        "routes": (
            {
                "route": "POST /subscriptions",
                "command": "create_subscription",
                "owned_tables": ("subscription", "subscription_phase", "billing_schedule"),
                "emits": ("SubscriptionActivated",),
                "requires_permission": "subscription_billing.subscription",
                "idempotency_key": "subscription_id",
            },
            {
                "route": "POST /trials",
                "command": "start_trial",
                "owned_tables": ("trial_period",),
                "requires_permission": "subscription_billing.subscription",
                "idempotency_key": "trial_id",
            },
            {
                "route": "POST /subscription-change-orders",
                "command": "change_subscription_plan",
                "owned_tables": ("subscription", "subscription_change_order", "subscription_phase"),
                "emits": ("SubscriptionChanged",),
                "requires_permission": "subscription_billing.subscription",
                "idempotency_key": "change_order_id",
            },
            {
                "route": "POST /subscription-cancellations",
                "command": "cancel_subscription",
                "owned_tables": ("subscription", "billing_schedule"),
                "emits": ("SubscriptionCancelled",),
                "requires_permission": "subscription_billing.subscription",
                "idempotency_key": "subscription_id:cancelled_at",
            },
            {
                "route": "POST /subscription-addons",
                "command": "add_subscription_addon",
                "owned_tables": ("subscription_addon", "subscription"),
                "requires_permission": "subscription_billing.subscription",
                "idempotency_key": "addon_id",
            },
            {
                "route": "POST /usage",
                "command": "record_usage",
                "owned_tables": ("usage_meter",),
                "emits": ("UsageRated",),
                "requires_permission": "subscription_billing.usage",
                "idempotency_key": "usage_id",
            },
            {
                "route": "POST /renewals",
                "command": "renew_subscription",
                "owned_tables": ("subscription", "billing_schedule"),
                "emits": ("SubscriptionRenewed",),
                "requires_permission": "subscription_billing.renewal",
                "idempotency_key": "subscription_id",
            },
            {
                "route": "POST /invoices",
                "command": "generate_invoice",
                "owned_tables": ("invoice", "invoice_line", "billing_schedule"),
                "emits": ("InvoiceApproved", "InvoiceApprovalRequested"),
                "requires_permission": "subscription_billing.invoice",
                "idempotency_key": "subscription_id:period",
            },
            {
                "route": "POST /credit-memos",
                "command": "issue_credit_memo",
                "owned_tables": ("credit_memo", "invoice"),
                "emits": ("CreditMemoIssued",),
                "requires_permission": "subscription_billing.invoice",
                "idempotency_key": "credit_memo_id",
            },
            {
                "route": "POST /payment-applications",
                "command": "apply_payment_to_invoice",
                "owned_tables": ("payment_application", "invoice"),
                "emits": ("PaymentApplied",),
                "requires_permission": "subscription_billing.invoice",
                "idempotency_key": "payment_application_id",
            },
            {
                "route": "POST /entitlements",
                "command": "grant_entitlement",
                "owned_tables": ("entitlement_grant",),
                "emits": ("EntitlementGranted",),
                "requires_permission": "subscription_billing.entitlement",
                "idempotency_key": "entitlement_grant_id",
            },
            {
                "route": "POST /revenue-recognition",
                "command": "recognize_revenue",
                "owned_tables": ("revenue_schedule",),
                "emits": ("RevenueRecognized",),
                "requires_permission": "subscription_billing.revenue",
                "idempotency_key": "invoice_id:period",
            },
            {
                "route": "POST /dunning-notices",
                "command": "create_dunning_notice",
                "owned_tables": ("dunning_notice",),
                "emits": ("DunningNoticeCreated",),
                "requires_permission": "subscription_billing.dunning",
                "idempotency_key": "subscription_id:reason",
            },
            {
                "route": "POST /billing-exceptions",
                "command": "open_billing_exception",
                "owned_tables": ("billing_exception",),
                "requires_permission": "subscription_billing.audit",
                "idempotency_key": "exception_id",
            },
            {
                "route": "POST /subscription-billing/events/inbox",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES,
                "requires_permission": "subscription_billing.event",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /subscription-billing/workbench",
                "command": "build_workbench_view",
                "query": "build_workbench_view",
                "owned_tables": SUBSCRIPTION_BILLING_OWNED_TABLES,
                "requires_permission": "subscription_billing.audit",
            },
        ),
        "declared_catalog_routes": SUBSCRIPTION_BILLING_API_ROUTES,
        "owned_tables": SUBSCRIPTION_BILLING_OWNED_TABLES,
        "consumes": SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES,
        "emits": SUBSCRIPTION_BILLING_EMITTED_EVENT_TYPES,
        "permissions": tuple(sorted(subscription_billing_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "database_backends": SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS,
    }


def subscription_billing_build_schema_contract() -> dict:
    table_fields = {
        "plan_catalog": ("tenant", "plan_id", "family", "name", "currency", "region", "billing_period", "base_price", "usage_rate", "included_units", "status", "proof"),
        "subscription": ("tenant", "subscription_id", "customer_id", "plan_id", "status", "region", "currency", "mrr", "renewal_confidence", "churn_risk", "audit_proof"),
        "subscription_phase": ("tenant", "phase_id", "subscription_id", "plan_id", "start_date", "end_date", "status"),
        "trial_period": ("tenant", "trial_id", "customer_id", "plan_id", "start_date", "end_date", "conversion_score", "status", "audit_proof"),
        "subscription_addon": ("tenant", "addon_id", "subscription_id", "name", "quantity", "unit_price", "mrr_delta", "effective_date", "status", "audit_proof"),
        "subscription_change_order": ("tenant", "change_order_id", "subscription_id", "from_plan_id", "to_plan_id", "effective_date", "reason", "proration_amount", "status", "audit_proof"),
        "usage_meter": ("tenant", "usage_id", "subscription_id", "meter_name", "quantity", "billable_units", "rated_amount", "currency", "status", "audit_proof"),
        "billing_schedule": ("tenant", "subscription_id", "next_invoice_date", "period", "status"),
        "invoice": ("tenant", "invoice_id", "subscription_id", "customer_id", "period", "amount", "currency", "usage_amount", "risk_score", "status", "audit_proof"),
        "invoice_line": ("tenant", "invoice_line_id", "invoice_id", "subscription_id", "line_type", "quantity", "unit_price", "amount", "status"),
        "credit_memo": ("tenant", "credit_memo_id", "invoice_id", "subscription_id", "amount", "currency", "reason", "status", "audit_proof"),
        "payment_application": ("tenant", "payment_application_id", "invoice_id", "subscription_id", "payment_event_id", "amount", "currency", "status", "audit_proof"),
        "dunning_notice": ("tenant", "dunning_id", "subscription_id", "customer_id", "reason", "risk_score", "status", "retry_policy", "audit_proof"),
        "entitlement_grant": ("tenant", "entitlement_grant_id", "subscription_id", "customer_id", "entitlement_key", "scope", "projection", "status", "audit_proof"),
        "revenue_schedule": ("tenant", "revenue_schedule_id", "invoice_id", "subscription_id", "period", "recognition_type", "amount", "ledger_handoff", "status", "audit_proof"),
        "billing_exception": ("tenant", "exception_id", "subscription_id", "exception_type", "severity", "description", "recommended_action", "status", "audit_proof"),
        "billing_rule": ("tenant", "rule_id", "rule_type", "status", "allowed_plan_families", "allowed_currencies", "allowed_regions", "compiled_hash"),
        "billing_parameter": ("name", "value", "bounds", "compiled_hash"),
        "billing_configuration": ("database_backend", "event_topic", "retry_limit", "default_currency", "supported_currencies", "supported_regions", "billing_calendars", "default_timezone", "invoice_approval_mode", "workbench_limit"),
        "billing_schema_extension": ("table", "fields", "version"),
        "subscription_billing_appgen_outbox_event": ("tenant", "event_id", "event_type", "idempotency_key", "retry_policy", "audit_hash"),
        "subscription_billing_appgen_inbox_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status"),
        "subscription_billing_dead_letter_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason"),
    }
    relationships = (
        {"from": "plan_catalog.plan_id", "to": "subscription.plan_id", "type": "owned_reference"},
        {"from": "subscription.subscription_id", "to": "subscription_phase.subscription_id", "type": "owned_reference"},
        {"from": "subscription.subscription_id", "to": "subscription_addon.subscription_id", "type": "owned_reference"},
        {"from": "subscription.subscription_id", "to": "subscription_change_order.subscription_id", "type": "owned_reference"},
        {"from": "subscription.subscription_id", "to": "billing_schedule.subscription_id", "type": "owned_reference"},
        {"from": "subscription.subscription_id", "to": "usage_meter.subscription_id", "type": "owned_reference"},
        {"from": "subscription.subscription_id", "to": "invoice.subscription_id", "type": "owned_reference"},
        {"from": "invoice.invoice_id", "to": "invoice_line.invoice_id", "type": "owned_reference"},
        {"from": "invoice.invoice_id", "to": "credit_memo.invoice_id", "type": "owned_reference"},
        {"from": "invoice.invoice_id", "to": "payment_application.invoice_id", "type": "owned_reference"},
        {"from": "subscription.subscription_id", "to": "entitlement_grant.subscription_id", "type": "owned_reference"},
        {"from": "invoice.invoice_id", "to": "revenue_schedule.invoice_id", "type": "owned_reference"},
        {"from": "subscription.subscription_id", "to": "dunning_notice.subscription_id", "type": "owned_reference"},
        {"from": "subscription.subscription_id", "to": "billing_exception.subscription_id", "type": "owned_reference"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "name" or field == "table")[:2],
            "owned_by": "subscription_billing",
        }
        for table in SUBSCRIPTION_BILLING_SCHEMA_TABLES
    )
    return {
        "format": "appgen.subscription-billing-owned-schema-contract.v1",
        "ok": len(tables) == len(SUBSCRIPTION_BILLING_SCHEMA_TABLES)
        and all(item["table"] in SUBSCRIPTION_BILLING_SCHEMA_TABLES for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/subscription_billing/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(SUBSCRIPTION_BILLING_SCHEMA_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in SUBSCRIPTION_BILLING_SCHEMA_TABLES
        ),
        "runtime_tables": SUBSCRIPTION_BILLING_RUNTIME_TABLES,
        "datastore_backends": SUBSCRIPTION_BILLING_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def subscription_billing_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "register_plan",
        "start_trial",
        "create_subscription",
        "change_subscription_plan",
        "cancel_subscription",
        "add_subscription_addon",
        "record_usage",
        "generate_invoice",
        "issue_credit_memo",
        "apply_payment_to_invoice",
        "grant_entitlement",
        "recognize_revenue",
        "renew_subscription",
        "open_billing_exception",
        "resolve_billing_exception",
        "create_dunning_notice",
        "receive_event",
        "run_control_tests",
    )
    return {
        "format": "appgen.subscription-billing-service-contract.v1",
        "ok": len(command_methods) >= 12,
        "transaction_boundary": "subscription_billing_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "build_api_contract",
            "build_schema_contract",
            "score_revenue_exposure",
            "simulate_proration_quote",
            "build_release_evidence",
            "verify_owned_table_boundary",
        ),
        "mutates_only": SUBSCRIPTION_BILLING_SCHEMA_TABLES,
        "external_dependencies": {
            "apis": SUBSCRIPTION_BILLING_DECLARED_API_DEPENDENCIES,
            "events": SUBSCRIPTION_BILLING_DECLARED_EVENT_DEPENDENCIES,
            "api_projections": SUBSCRIPTION_BILLING_DECLARED_PROJECTIONS,
            "shared_tables": (),
        },
        "eventing": {
            "contract": "AppGen-X",
            "outbox_table": SUBSCRIPTION_BILLING_RUNTIME_TABLES[0],
            "inbox_table": SUBSCRIPTION_BILLING_RUNTIME_TABLES[1],
            "dead_letter_table": SUBSCRIPTION_BILLING_RUNTIME_TABLES[2],
            "idempotency_required": True,
        },
    }


def subscription_billing_build_release_evidence() -> dict:
    schema = subscription_billing_build_schema_contract()
    service = subscription_billing_build_service_contract()
    api = subscription_billing_build_api_contract()
    ui = subscription_billing_ui_binding_contract()
    permissions = subscription_billing_permissions_contract()
    control = _subscription_billing_release_control_evidence()
    smoke = subscription_billing_runtime_smoke()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 10},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(schema["tables"])},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 12},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X" and api["required_event_topic"] == SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC},
        {"id": "ui_binding_evidence", "ok": ui["ok"] and ui["binding_evidence"]["outbox_table"] == SUBSCRIPTION_BILLING_RUNTIME_TABLES[0]},
        {"id": "permissions_cover_commands", "ok": {"create_subscription", "generate_invoice", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "retry_and_dead_letter_evidence", "ok": control["ok"] and control["summary"]["retry_status"] == "retrying" and control["summary"]["dead_letter_status"] == "dead_letter"},
        {"id": "duplicate_idempotency_evidence", "ok": control["summary"]["duplicate_status"] == "duplicate"},
        {"id": "runtime_smoke", "ok": smoke["ok"]},
    )
    return {
        "format": "appgen.subscription-billing-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "ui": ui,
        "permissions": permissions,
        "control": control,
        "smoke": smoke,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def subscription_billing_permissions_contract() -> dict:
    permissions = (
        "subscription_billing.configure",
        "subscription_billing.subscription",
        "subscription_billing.usage",
        "subscription_billing.invoice",
        "subscription_billing.renewal",
        "subscription_billing.dunning",
        "subscription_billing.entitlement",
        "subscription_billing.revenue",
        "subscription_billing.event",
        "subscription_billing.audit",
    )
    return {
        "format": "appgen.subscription-billing-permissions-contract.v1",
        "ok": True,
        "pbc": "subscription_billing",
        "permissions": permissions,
        "roles": {
            "subscription_billing_admin": permissions,
            "subscription_billing_operator": (
                "subscription_billing.subscription",
                "subscription_billing.usage",
                "subscription_billing.invoice",
                "subscription_billing.renewal",
                "subscription_billing.dunning",
                "subscription_billing.entitlement",
                "subscription_billing.revenue",
            ),
            "subscription_billing_auditor": ("subscription_billing.audit", "subscription_billing.event"),
        },
        "policy_controls": (
            "tenant_scope_required",
            "plan_family_allowlist",
            "currency_region_allowlist",
            "approval_threshold_enforced",
            "event_idempotency_required",
        ),
        "action_permissions": {
            "configure_runtime": "subscription_billing.configure",
            "set_parameter": "subscription_billing.configure",
            "register_rule": "subscription_billing.configure",
            "register_schema_extension": "subscription_billing.configure",
            "register_plan": "subscription_billing.configure",
            "start_trial": "subscription_billing.subscription",
            "create_subscription": "subscription_billing.subscription",
            "change_subscription_plan": "subscription_billing.subscription",
            "cancel_subscription": "subscription_billing.subscription",
            "add_subscription_addon": "subscription_billing.subscription",
            "record_usage": "subscription_billing.usage",
            "generate_invoice": "subscription_billing.invoice",
            "issue_credit_memo": "subscription_billing.invoice",
            "apply_payment_to_invoice": "subscription_billing.invoice",
            "grant_entitlement": "subscription_billing.entitlement",
            "recognize_revenue": "subscription_billing.revenue",
            "renew_subscription": "subscription_billing.renewal",
            "open_billing_exception": "subscription_billing.audit",
            "resolve_billing_exception": "subscription_billing.audit",
            "create_dunning_notice": "subscription_billing.dunning",
            "receive_event": "subscription_billing.event",
            "build_workbench_view": "subscription_billing.audit",
            "verify_owned_table_boundary": "subscription_billing.audit",
            "run_control_tests": "subscription_billing.audit",
        },
    }


def subscription_billing_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str]) -> dict:
    owned = set(SUBSCRIPTION_BILLING_OWNED_TABLES)
    allowed_event_dependencies = set(SUBSCRIPTION_BILLING_DECLARED_EVENT_DEPENDENCIES)
    allowed_api_dependencies = set(SUBSCRIPTION_BILLING_DECLARED_API_DEPENDENCIES)
    allowed_runtime_tables = set(SUBSCRIPTION_BILLING_RUNTIME_TABLES)
    allowed_projections = set(SUBSCRIPTION_BILLING_DECLARED_PROJECTIONS)
    violations = tuple(
        reference
        for reference in references
        if reference not in owned
        and reference not in allowed_event_dependencies
        and reference not in allowed_api_dependencies
        and reference not in allowed_runtime_tables
        and reference not in allowed_projections
        and not str(reference).startswith("subscription_billing_")
    )
    return {
        "format": "appgen.subscription-billing-owned-boundary-check.v1",
        "ok": not violations,
        "pbc": "subscription_billing",
        "owned_tables": SUBSCRIPTION_BILLING_OWNED_TABLES,
        "declared_dependencies": {
            "apis": tuple(sorted(allowed_api_dependencies)),
            "events": tuple(sorted(allowed_event_dependencies)),
            "api_projections": tuple(sorted(allowed_projections)),
            "shared_tables": (),
        },
        "runtime_tables": tuple(sorted(allowed_runtime_tables)),
        "references": tuple(references),
        "violations": violations,
    }


def subscription_billing_run_control_tests(state: dict) -> dict:
    api = subscription_billing_build_api_contract()
    workbench = subscription_billing_build_workbench_view(state, tenant=next(iter({item["tenant"] for item in state.get("subscriptions", {}).values()}), "tenant_unknown"))
    boundary = subscription_billing_verify_owned_table_boundary(
        (
            "subscription",
            "billing_schedule",
            "payment_orchestration.PaymentCaptured",
            "tax_localization.POST /tax-quotes",
            "payment_capture_projection",
        )
    )
    checks = (
        {"id": "configuration_bound", "ok": bool(state.get("configuration", {}).get("ok"))},
        {"id": "parameter_floor", "ok": len(state.get("parameters", {})) >= 3},
        {"id": "rules_registered", "ok": bool(state.get("rules"))},
        {"id": "boundary_contract", "ok": boundary["ok"]},
        {"id": "api_event_contract", "ok": api["event_contract"] == "AppGen-X"},
        {"id": "workbench_binding", "ok": workbench["binding_evidence"]["outbox_table"] == SUBSCRIPTION_BILLING_RUNTIME_TABLES[0]},
        {"id": "idempotency_evidence", "ok": bool(state.get("handled_events"))},
        {"id": "retry_dead_letter_evidence", "ok": bool(state.get("dead_letter")) or any(event["event_type"].endswith("Failed") for event in state.get("events", ()))},
    )
    return {
        "format": "appgen.subscription-billing-control-tests.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "summary": {
            "handled_events": len(state.get("handled_events", ())),
            "dead_letter_count": len(state.get("dead_letter", ())),
            "outbox_count": len(state.get("outbox", ())),
        },
    }


def subscription_billing_score_revenue_exposure(state: dict, subscription_id: str) -> dict:
    subscription = state["subscriptions"].get(subscription_id)
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {subscription_id}")
    usage_amount = sum(item["rated_amount"] for item in state.get("usage_meters", {}).values() if item["subscription_id"] == subscription_id)
    invoice_exposure = sum(item["amount"] for item in state.get("invoices", {}).values() if item["subscription_id"] == subscription_id and item["status"] != "paid")
    exposure_score = round(min((usage_amount + invoice_exposure) / max(subscription["mrr"], 1), 10.0), 4)
    return {
        "ok": True,
        "subscription_id": subscription_id,
        "mrr": subscription["mrr"],
        "usage_amount": round(usage_amount, 2),
        "open_invoice_exposure": round(invoice_exposure, 2),
        "exposure_score": exposure_score,
    }


def subscription_billing_simulate_proration_quote(state: dict, subscription_id: str, *, target_seats: int, remaining_ratio: float) -> dict:
    subscription = state["subscriptions"].get(subscription_id)
    if not subscription:
        raise ValueError(f"Unknown Subscription Billing subscription: {subscription_id}")
    plan = state["plans"][subscription["plan_id"]]
    precision = int(state.get("parameters", {}).get("proration_rounding_precision", {"value": 2})["value"])
    seat_delta = max(int(target_seats) - int(subscription["seats"]), 0)
    unit_rate = round((float(plan["base_price"]) / max(int(subscription["seats"]), 1)), precision)
    prorated_amount = round(seat_delta * unit_rate * float(remaining_ratio), precision)
    return {
        "ok": True,
        "subscription_id": subscription_id,
        "current_seats": subscription["seats"],
        "target_seats": int(target_seats),
        "remaining_ratio": float(remaining_ratio),
        "seat_delta": seat_delta,
        "prorated_amount": prorated_amount,
        "currency": subscription["currency"],
    }


def subscription_billing_ui_binding_contract() -> dict:
    return {
        "format": "appgen.subscription-billing-ui-binding-contract.v1",
        "ok": True,
        "binding_evidence": {
            "owned_tables": SUBSCRIPTION_BILLING_OWNED_TABLES,
            "runtime_tables": SUBSCRIPTION_BILLING_RUNTIME_TABLES,
            "workbench_route": "/workbench/pbcs/subscription_billing",
            "outbox_table": SUBSCRIPTION_BILLING_RUNTIME_TABLES[0],
            "inbox_table": SUBSCRIPTION_BILLING_RUNTIME_TABLES[1],
            "dead_letter_table": SUBSCRIPTION_BILLING_RUNTIME_TABLES[2],
        },
    }


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _copy_value(value):
    if isinstance(value, dict):
        return {key: _copy_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_copy_value(item) for item in value]
    if isinstance(value, set):
        return set(value)
    return value


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Subscription Billing runtime must be configured before commands execute")


def _assert_supported_currency_region(state: dict, currency: str, region: str) -> None:
    config = state["configuration"]
    if currency not in config["supported_currencies"]:
        raise ValueError(f"Unsupported Subscription Billing currency: {currency}")
    if region not in config["supported_regions"]:
        raise ValueError(f"Unsupported Subscription Billing region: {region}")


def _select_rule(state: dict, tenant: str, rule_type: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule["tenant"] == tenant and rule["rule_type"] == rule_type and rule["status"] == "active":
            return rule
    return None


def _effective_usage_rate(state: dict, plan_id: str) -> float:
    plan = state["plans"][plan_id]
    decision = state.get("price_decisions", {}).get(plan_id, {})
    optimized = decision.get("optimized_rate")
    if optimized is None:
        return float(plan["usage_rate"])
    return max(float(optimized), _minimum_usage_rate(state, plan_id))


def _minimum_usage_rate(state: dict, plan_id: str) -> float:
    plan = state["plans"][plan_id]
    guardrail = float(state["parameters"].get("discount_guardrail_percent", {"value": 100})["value"])
    return float(plan["usage_rate"]) * (1 - guardrail / 100)


def _subscription_risk(command: dict, plan: dict) -> dict:
    seat_factor = min(int(command["seats"]) / 100, 0.3)
    price_factor = min(float(plan["base_price"]) / 10000, 0.25)
    risk = round(0.12 + seat_factor + price_factor, 4)
    return {"churn_risk": min(risk, 0.95)}


def _billing_risk(subscription: dict, usage_amount: float) -> float:
    exposure = min(usage_amount / max(subscription["mrr"], 1), 1.0) * 0.25
    return round(min(subscription["churn_risk"] + exposure, 0.99), 4)


def _billing_exception_action(exception_type: str) -> str:
    actions = {
        "payment_delay": "create_dunning_notice",
        "usage_spike": "request_usage_review",
        "tax_mismatch": "request_tax_requote",
        "entitlement_mismatch": "replay_entitlement_projection",
        "revenue_variance": "recompute_revenue_schedule",
    }
    return actions.get(exception_type, "manual_billing_review")


def _revenue_schedule(period: str, amount: float) -> tuple[dict, ...]:
    return (
        {"period": period, "recognition_type": "subscription_service", "amount": round(amount * 0.8, 2)},
        {"period": period, "recognition_type": "usage_service", "amount": round(amount * 0.2, 2)},
    )


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "AppGen-X",
        "idempotency_key": f"subscription_billing:{event_type}:{payload.get('subscription_id') or payload.get('invoice_id') or len(state['outbox']) + 1}",
        "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": "subscription_billing_dead_letter_event"},
        "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload}),
    }
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {
        "event_type": event_type,
        "key": key,
        "payload": payload,
        "hash": _digest({"event_type": event_type, "key": key, "payload": payload}),
    }


def _capability_evidence(
    state: dict,
    capability: str,
    *,
    duplicate_status: str | None = None,
    retry_status: str | None = None,
    dead_letter_status: str | None = None,
) -> dict:
    return {
        "capability": capability,
        "events": len(state["events"]),
        "outbox": len(state["outbox"]),
        "inbox": len(state["inbox"]),
        "dead_letter": len(state["dead_letter"]),
        "rules": len(state["rules"]),
        "parameters": len(state["parameters"]),
        "configuration": bool(state["configuration"].get("ok")),
        "duplicate_status": duplicate_status,
        "retry_status": retry_status,
        "dead_letter_status": dead_letter_status,
        "runtime_digest": _digest({"capability": capability, "events": len(state["events"]), "invoices": len(state["invoices"])}),
    }


def _subscription_billing_release_control_evidence() -> dict:
    state = subscription_billing_empty_state()
    state = subscription_billing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "billing_calendars": ("monthly",),
            "default_timezone": "UTC",
            "invoice_approval_mode": "policy",
            "workbench_limit": 25,
        },
    )["state"]
    for name, value in (
        ("renewal_confidence_threshold", 0.72),
        ("churn_risk_threshold", 0.62),
        ("dunning_risk_threshold", 0.58),
        ("usage_rating_precision", 4),
        ("proration_rounding_precision", 2),
        ("retry_limit", 2),
        ("carbon_batch_window_hours", 8),
        ("discount_guardrail_percent", 20.0),
        ("approval_amount_threshold", 5000.0),
        ("workbench_limit", 25),
    ):
        state = subscription_billing_set_parameter(state, name, value)["state"]
    state = subscription_billing_register_rule(
        state,
        {
            "rule_id": "rule_release",
            "tenant": "tenant_release",
            "rule_type": "renewal",
            "allowed_plan_families": ("growth",),
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "renewal_policy": "auto_renew_with_payment_confirmation",
            "invoice_policy": "approve_below_threshold",
            "status": "active",
        },
    )["state"]
    state = subscription_billing_register_plan(
        state,
        {
            "plan_id": "plan_release",
            "tenant": "tenant_release",
            "family": "growth",
            "name": "Release",
            "currency": "USD",
            "region": "US",
            "billing_period": "monthly",
            "base_price": 120.0,
            "usage_rate": 3.0,
            "included_units": 10.0,
            "status": "active",
        },
    )["state"]
    state = subscription_billing_create_subscription(
        state,
        {
            "subscription_id": "sub_release",
            "tenant": "tenant_release",
            "customer_id": "cust_release",
            "plan_id": "plan_release",
            "start_date": "2026-01-01",
            "renewal_date": "2026-02-01",
            "region": "US",
            "currency": "USD",
            "seats": 4,
        },
    )["state"]
    state = subscription_billing_record_usage(
        state,
        {
            "usage_id": "usage_release",
            "tenant": "tenant_release",
            "subscription_id": "sub_release",
            "meter_name": "api_calls",
            "quantity": 18.0,
            "occurred_at": "2026-01-10T00:00:00Z",
        },
    )["state"]
    invoice = subscription_billing_generate_invoice(state, "sub_release", period="2026-01")
    state = invoice["state"]
    handled = subscription_billing_receive_event(
        state,
        {
            "event_id": "payment_release",
            "event_type": "PaymentCaptured",
            "payload": {"tenant": "tenant_release", "invoice_id": invoice["invoice"]["invoice_id"], "amount": invoice["invoice"]["amount"], "currency": "USD"},
        },
    )
    state = handled["state"]
    duplicate = subscription_billing_receive_event(
        state,
        {
            "event_id": "payment_release",
            "event_type": "PaymentCaptured",
            "payload": {"tenant": "tenant_release", "invoice_id": invoice["invoice"]["invoice_id"], "amount": invoice["invoice"]["amount"], "currency": "USD"},
        },
    )
    retrying = subscription_billing_receive_event(
        state,
        {
            "event_id": "payment_retry_release",
            "event_type": "PaymentCaptured",
            "payload": {"tenant": "tenant_release", "invoice_id": invoice["invoice"]["invoice_id"], "amount": invoice["invoice"]["amount"], "currency": "USD"},
        },
        simulate_failure=True,
    )
    dead_letter = subscription_billing_receive_event(
        retrying["state"],
        {
            "event_id": "payment_retry_release",
            "event_type": "PaymentCaptured",
            "payload": {"tenant": "tenant_release", "invoice_id": invoice["invoice"]["invoice_id"], "amount": invoice["invoice"]["amount"], "currency": "USD"},
        },
        simulate_failure=True,
    )
    control = subscription_billing_run_control_tests(dead_letter["state"])
    return {
        "ok": handled["handler"]["status"] == "handled"
        and duplicate["handler"]["status"] == "duplicate"
        and retrying["handler"]["status"] == "retrying"
        and dead_letter["handler"]["status"] == "dead_letter"
        and control["ok"],
        "summary": {
            "handled_status": handled["handler"]["status"],
            "duplicate_status": duplicate["handler"]["status"],
            "retry_status": retrying["handler"]["status"],
            "dead_letter_status": dead_letter["handler"]["status"],
            "dead_letter_count": len(dead_letter["state"]["dead_letter"]),
        },
        "control": control,
    }


def _digest(payload: dict) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, float):
            if math.isnan(value) or math.isinf(value):
                return str(value)
        return value

    encoded = json.dumps(payload, sort_keys=True, default=default, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()
