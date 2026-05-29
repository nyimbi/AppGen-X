"""Executable seed-data contract for the returns_reverse_logistics PBC."""

PBC_KEY = 'returns_reverse_logistics'
SEED_DATA = ({'table': 'returns_reverse_logistics_return_authorization', 'rows': ({'code': 'RETURNS_REVERSE_LOGISTICS-001', 'status': 'active'},)}, {'table': 'returns_reverse_logistics_return_label', 'rows': ({'code': 'RETURNS_REVERSE_LOGISTICS-002', 'status': 'active'},)})


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
        "configuration": {"database_backend": "postgresql", "event_topic": "appgen.returns.events", "retry_limit": 3, "default_currency": "USD", "supported_carriers": ("parcel_green",), "supported_dispositions": ("restock", "refurbish", "scrap"), "workbench_limit": 100},
        "parameters": {"eligibility_window_days": 30, "fraud_threshold": 0.8, "recovery_floor": 0.3, "carrier_handoff_hours": 24, "carbon_weight": 0.2, "route_switch_threshold": 0.1, "forecast_horizon_days": 14, "anomaly_zscore_threshold": 2.5, "workbench_limit": 100},
        "rule": {"rule_id": "rule_demo", "tenant": tenant, "scope": "return_policy", "status": "active", "eligibility_policy": {"max_days_since_shipment": 30, "blocked_reasons": (), "minimum_payment_capture_ratio": 1.0}, "label_policy": {"preferred_carriers": ("parcel_green",), "max_cost": 15.0}, "inspection_policy": {"restock_min": 0.85, "refurbish_min": 0.55}, "credit_policy": {"restock_factor": 0.9, "refurbish_factor": 0.65, "scrap_factor": 0.25}},
        "order_event": {"event_id": "evt_order_demo", "event_type": "OrderShipped", "idempotency_key": "order_demo:v1", "payload": {"tenant": tenant, "order_id": "order_demo_100", "payment_id": "pay_demo_100", "customer_id": "cust_demo_100", "shipped_at": "2026-05-20", "days_since_shipped": 4, "return_window_days": 30, "final_sale": False, "items": ({"sku": "sku_demo_100", "quantity": 1, "unit_price": 80.0},)}},
        "payment_event": {"event_id": "evt_payment_demo", "event_type": "PaymentCaptured", "idempotency_key": "payment_demo:v1", "payload": {"tenant": tenant, "payment_id": "pay_demo_100", "order_id": "order_demo_100", "captured_amount": 80.0, "currency": "USD", "ledger_account": "refund_liability"}},
        "invalid_event": {"event_id": "evt_invalid_demo", "event_type": "UnsupportedEvent", "idempotency_key": "invalid_demo:v1", "attempts": 3, "payload": {"tenant": tenant}},
        "return_authorization": {"return_id": "ret_demo_100", "rma": "RMA-DEMO-100", "tenant": tenant, "order_id": "order_demo_100", "payment_id": "pay_demo_100", "customer_id": "cust_demo_100", "reason": "damaged", "requested_at": "2026-05-24", "days_since_shipped": 4, "items": ({"sku": "sku_demo_100", "quantity": 1},)},
        "label": {"label_id": "lbl_demo_100", "return_id": "ret_demo_100", "tenant": tenant, "origin": "Nairobi", "destination": "Mombasa", "package_weight_kg": 1.0},
        "receipt": {"receipt_id": "rcpt_demo_100", "return_id": "ret_demo_100", "tenant": tenant, "received_at": "2026-05-25T10:00:00Z", "receiving_site": "returns_dc", "package_condition": "intact"},
        "inspection": {"inspection_id": "insp_demo_100", "return_id": "ret_demo_100", "tenant": tenant, "condition_score": 0.93, "completeness_score": 1.0, "packaging_intact": True, "notes": "ready"},
        "credit": {"adjustment_id": "adj_demo_100", "return_id": "ret_demo_100", "tenant": tenant},
        "resolution_mode": "refund",
        "claim_reason": "late_scan",
        "exception": {"exception_type": "carrier_timeout", "severity": "medium", "owner": "ops"},
        "document": "RMA RMA-DEMO-100 for order_demo_100 and payment pay_demo_100: authorize damaged return, create label, receive, inspect, restock, credit, refund, and open carrier claim.",
        "instructions": "Authorize return ret_demo_100, create label, receive package, inspect, resolve disposition, issue credit adjustment, queue refund and open carrier timeout exception.",
    }
