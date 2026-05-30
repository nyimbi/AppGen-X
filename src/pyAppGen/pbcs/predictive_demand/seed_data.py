"""Executable seed-data contract for the predictive_demand PBC."""

PBC_KEY = 'predictive_demand'
SEED_DATA = ({'table': 'predictive_demand_forecast_model', 'rows': ({'code': 'PREDICTIVE_DEMAND-001', 'status': 'active'},)}, {'table': 'predictive_demand_forecast_run', 'rows': ({'code': 'PREDICTIVE_DEMAND-002', 'status': 'active'},)})


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
    """Return seed rows that make a one-PBC predictive demand app immediately usable."""
    rows = (
        {"table": "predictive_demand_forecast_model", "rows": ({"code": "BASELINE-STATISTICAL", "status": "active", "algorithm": "ensemble_timeseries"},)},
        {"table": "predictive_demand_planning_horizon", "rows": ({"code": "WEEKLY-13", "status": "active", "granularity": "week", "service_level_target": "0.95"},)},
        {"table": "predictive_demand_forecast_driver", "rows": ({"code": "PROMOTION-LIFT", "status": "active", "driver_type": "promotion"},)},
        {"table": "predictive_demand_planning_rule", "rows": ({"code": "BIAS-GATE", "status": "active", "scope": "model_governance"},)},
        {"table": "predictive_demand_planning_parameter", "rows": ({"code": "BIAS-TOLERANCE", "status": "active", "value": "5"},)},
    )
    invalid_tables = tuple(item["table"] for item in rows if not item["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": bool(rows) and not invalid_tables, "pbc": PBC_KEY, "rows": rows, "invalid_tables": invalid_tables, "side_effects": ()}


def smoke_test():
    """Exercise seed validation without writing rows."""
    validation = validate_seed_data()
    standalone = standalone_seed_bundle()
    return {**validation, "ok": validation["ok"] and standalone["ok"], "standalone_seed_bundle": standalone}
