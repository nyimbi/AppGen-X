"""Executable seed-data contract for the subscription_billing PBC."""

PBC_KEY = 'subscription_billing'
SEED_DATA = ({'table': 'subscription_billing_subscription', 'rows': ({'code': 'SUBSCRIPTION_BILLING-001', 'status': 'active'},)}, {'table': 'subscription_billing_usage_meter', 'rows': ({'code': 'SUBSCRIPTION_BILLING-002', 'status': 'active'},)})


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item['table'] for item in SEED_DATA))
    return {
        'ok': bool(SEED_DATA),
        'pbc': PBC_KEY,
        'tables': tables,
        'rows': SEED_DATA,
        'side_effects': (),
    }


def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item['table'] for item in SEED_DATA if not item.get('table', '').startswith(f'{PBC_KEY}_')
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get('rows', ())
        if not row.get('code') or not row.get('status')
    )
    plan = seed_plan()
    return {
        'ok': plan['ok'] and not invalid_tables and not invalid_rows,
        'pbc': PBC_KEY,
        'plan': plan,
        'invalid_tables': invalid_tables,
        'invalid_rows': invalid_rows,
        'side_effects': (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()



def standalone_seed_bundle(tenant="tenant_demo"):
    return {
        "pbc": PBC_KEY,
        "tenant": tenant,
        "configuration": {"database_backend": "postgresql", "event_topic": "appgen.subscription.events", "retry_limit": 3, "default_currency": "USD", "supported_currencies": ("USD",), "supported_regions": ("US",), "billing_calendars": ("monthly",), "default_timezone": "UTC", "invoice_approval_mode": "policy", "workbench_limit": 100},
        "parameters": {"renewal_confidence_threshold": 0.7, "churn_risk_threshold": 0.8, "dunning_risk_threshold": 0.5, "usage_rating_precision": 2, "proration_rounding_precision": 2, "retry_limit": 3, "carbon_batch_window_hours": 8, "discount_guardrail_percent": 25.0, "approval_amount_threshold": 10000.0, "workbench_limit": 100},
        "rule": {"rule_id": "rule_demo", "tenant": tenant, "rule_type": "renewal", "allowed_plan_families": ("growth",), "allowed_currencies": ("USD",), "allowed_regions": ("US",), "renewal_policy": "auto", "invoice_policy": "approve_below_threshold", "status": "active"},
        "plans": ({"plan_id": "plan_growth", "tenant": tenant, "family": "growth", "name": "Growth", "currency": "USD", "region": "US", "billing_period": "monthly", "base_price": 100.0, "usage_rate": 2.0, "included_units": 10.0, "status": "active"}, {"plan_id": "plan_scale", "tenant": tenant, "family": "growth", "name": "Scale", "currency": "USD", "region": "US", "billing_period": "monthly", "base_price": 175.0, "usage_rate": 1.5, "included_units": 25.0, "status": "active"}),
        "trial": {"trial_id": "trial_demo_100", "tenant": tenant, "customer_id": "cust_demo_100", "plan_id": "plan_growth", "start_date": "2026-01-01", "end_date": "2026-01-15", "region": "US", "currency": "USD"},
        "subscription": {"subscription_id": "sub_demo_100", "tenant": tenant, "customer_id": "cust_demo_100", "plan_id": "plan_growth", "start_date": "2026-01-15", "renewal_date": "2026-02-15", "region": "US", "currency": "USD", "seats": 3},
        "addon": {"addon_id": "addon_demo_100", "tenant": tenant, "subscription_id": "sub_demo_100", "name": "support", "quantity": 1, "unit_price": 20.0, "effective_date": "2026-01-15"},
        "usage": {"usage_id": "usage_demo_100", "tenant": tenant, "subscription_id": "sub_demo_100", "meter_name": "api_calls", "quantity": 30.0, "occurred_at": "2026-01-20T00:00:00Z"},
        "period": "2026-01",
        "credit": {"amount": 10.0, "reason": "service_adjustment"},
        "payment_event_id": "payment_demo_100",
        "entitlement_key": "support",
        "change": {"target_plan_id": "plan_scale", "effective_date": "2026-02-01", "reason": "upgrade"},
        "exception": {"exception_type": "usage_spike", "severity": "medium", "description": "usage review"},
        "dunning_reason": "payment_watch",
        "document": "Subscription packet for sub_demo_100: register growth plans, create trial, bill usage, issue credit, apply payment, grant support entitlement and process upgrade.",
        "instructions": "Create subscription, rate usage, generate invoice, issue credit, apply payment, grant entitlement, recognize revenue, change plan and close exception.",
    }
