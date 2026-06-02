"""Executable seed-data contract for the fraud_anomaly_detection PBC."""

PBC_KEY = 'fraud_anomaly_detection'
SEED_DATA = ({'table': 'fraud_anomaly_detection_risk_signal', 'rows': ({'code': 'FRAUD_ANOMALY_DETECTION-001', 'status': 'active'},)}, {'table': 'fraud_anomaly_detection_anomaly_score', 'rows': ({'code': 'FRAUD_ANOMALY_DETECTION-002', 'status': 'active'},)})


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


def standalone_seed_bundle():
    """Return seed rows that make a one-PBC fraud operations app immediately usable."""
    rows = (
        {"table": "fraud_anomaly_detection_fraud_rule", "rows": ({"code": "HIGH-RISK-CHECKOUT", "status": "active", "risk_domain": "checkout"},)},
        {"table": "fraud_anomaly_detection_fraud_parameter", "rows": ({"code": "CASE-OPEN-THRESHOLD", "status": "active", "value": "0.82"},)},
        {"table": "fraud_anomaly_detection_fraud_configuration", "rows": ({"code": "DEFAULT-SCORING", "status": "active", "database_backend": "postgresql", "event_contract": "AppGen-X"},)},
        {"table": "fraud_anomaly_detection_behavior_baseline", "rows": ({"code": "NEW-SUBJECT-BASELINE", "status": "active", "metric": "checkout_velocity"},)},
        {"table": "fraud_anomaly_detection_analyst_queue_item", "rows": ({"code": "DEFAULT-QUEUE", "status": "active", "queue": "fraud_review"},)},
    )
    invalid_tables = tuple(item["table"] for item in rows if not item["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": bool(rows) and not invalid_tables, "pbc": PBC_KEY, "rows": rows, "invalid_tables": invalid_tables, "side_effects": ()}


def smoke_test():
    """Exercise seed validation without writing rows."""
    validation = validate_seed_data()
    standalone = standalone_seed_bundle()
    return {**validation, "ok": validation["ok"] and standalone["ok"], "standalone_seed_bundle": standalone}
