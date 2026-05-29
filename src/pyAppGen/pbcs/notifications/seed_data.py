"""Executable seed-data contract for the notifications PBC."""

PBC_KEY = 'notifications'
SEED_DATA = ({'table': 'notifications_notification_template', 'rows': ({'code': 'NOTIFICATIONS-001', 'status': 'active'},)}, {'table': 'notifications_delivery_channel', 'rows': ({'code': 'NOTIFICATIONS-002', 'status': 'active'},)})


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
    """Return seed rows that make a one-PBC notification app immediately usable."""
    rows = (
        {"table": "notifications_notification_template", "rows": ({"code": "WELCOME-EMAIL", "status": "active", "message_type": "transactional", "locale": "en-US"},)},
        {"table": "notifications_delivery_channel", "rows": ({"code": "EMAIL-PRIMARY", "status": "active", "channel_type": "email", "provider": "primary"}, {"code": "SMS-PRIMARY", "status": "active", "channel_type": "sms", "provider": "primary"})},
        {"table": "notifications_notification_rule", "rows": ({"code": "CONSENT-FIRST", "status": "active", "scope": "consent"},)},
        {"table": "notifications_notification_parameter", "rows": ({"code": "MAX-DAILY-MESSAGES", "status": "active", "value": "5"},)},
        {"table": "notifications_notification_configuration", "rows": ({"code": "DEFAULT-CONFIG", "status": "active", "database_backend": "postgresql", "event_contract": "AppGen-X"},)},
    )
    invalid_tables = tuple(item["table"] for item in rows if not item["table"].startswith(f"{PBC_KEY}_"))
    return {
        "ok": bool(rows) and not invalid_tables,
        "pbc": PBC_KEY,
        "rows": rows,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    validation = validate_seed_data()
    standalone = standalone_seed_bundle()
    return {**validation, "ok": validation["ok"] and standalone["ok"], "standalone_seed_bundle": standalone}
