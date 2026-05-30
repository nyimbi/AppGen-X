"""Executable seed-data contract for the payment_orchestration PBC."""

PBC_KEY = 'payment_orchestration'
SEED_DATA = ({'table': 'payment_orchestration_payment_gateway', 'rows': ({'code': 'PAYMENT_ORCHESTRATION-001', 'status': 'active'},)}, {'table': 'payment_orchestration_payment_intent', 'rows': ({'code': 'PAYMENT_ORCHESTRATION-002', 'status': 'active'},)})


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
        "configuration": {"database_backend": "postgresql", "event_topic": "appgen.payment.events", "retry_limit": 3, "default_currency": "USD", "supported_currencies": ("USD",), "supported_regions": ("US",), "supported_methods": ("card", "wallet"), "settlement_windows": ("night",), "default_timezone": "UTC", "workbench_limit": 100},
        "parameters": {"authorization_threshold": 0.7, "fraud_review_threshold": 0.7, "capture_amount_tolerance": 0.5, "retry_limit": 3, "gateway_latency_weight": 0.2, "gateway_cost_weight": 0.2, "gateway_auth_weight": 0.5, "settlement_risk_weight": 0.1, "max_capture_attempts": 3, "workbench_limit": 100},
        "rule": {"rule_id": "rule_demo", "tenant": tenant, "rule_type": "gateway_routing", "allowed_gateways": ("gateway_demo",), "allowed_currencies": ("USD",), "allowed_regions": ("US",), "risk_ceiling": 0.8, "capture_policy": "authorize_then_capture", "status": "active"},
        "gateway": {"gateway_id": "gateway_demo", "tenant": tenant, "provider": "demopay", "regions": ("US",), "currencies": ("USD",), "methods": ("card", "wallet"), "latency_ms": 120, "fee_bps": 65, "authorization_rate": 0.94, "settlement_risk": 0.04, "capacity": 100, "carbon_score": 30, "status": "active"},
        "checkout_event": {"event_id": "checkout_demo_100", "event_type": "CheckoutCompleted", "payload": {"tenant": tenant, "checkout_id": "checkout_demo_100", "customer_id": "customer_demo_100", "amount": 125.5, "currency": "USD", "region": "US"}},
        "token": {"token_id": "tok_demo_100", "tenant": tenant, "customer_id": "customer_demo_100", "method_type": "card", "network": "card_network", "issuer_country": "US", "vault_ref": "vault://tok_demo_100"},
        "intent": {"intent_id": "pi_demo_100", "tenant": tenant, "checkout_id": "checkout_demo_100", "customer_id": "customer_demo_100", "amount": 125.5, "currency": "USD", "region": "US", "token_id": "tok_demo_100"},
        "fraud_event": {"event_id": "fraud_demo_100", "event_type": "FraudRiskScored", "payload": {"tenant": tenant, "intent_id": "pi_demo_100", "risk_score": 0.18, "decision": "approve"}},
        "settlement_reference": "batch_demo_100",
        "payout_account": "merchant_demo_account",
        "refund": {"amount": 10.0, "reason": "goodwill"},
        "dispute": {"amount": 5.0, "reason": "customer_question", "evidence": ("delivery_proof", "customer_acknowledgement")},
        "document": "Payment instructions for pi_demo_100: capture amount 125.5, settle to batch_demo_100, schedule payout, process refund and dispute evidence.",
        "instructions": "Capture payment pi_demo_100 amount 125.5, settle, payout, refund goodwill, and open then resolve the dispute.",
    }
