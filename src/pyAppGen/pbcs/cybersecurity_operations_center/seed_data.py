"""Package-local seed data for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .models import default_parameter_records, default_policy_bundle

PBC_KEY = "cybersecurity_operations_center"


def seed_plan() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": f"{PBC_KEY}_security_alert",
                "code": "ALERT-SEED-001",
                "status": "new",
                "payload": {
                    "severity": "high",
                    "asset_ref": "srv-seed-01",
                    "principal_ref": "seed-user",
                    "indicator_value": "203.0.113.77",
                },
            },
            {
                "table": f"{PBC_KEY}_cybersecurity_operations_center_policy_rule",
                "code": "SECURITY_ALERT_POLICY",
                "status": "active",
                "payload": default_policy_bundle(),
            },
            {
                "table": f"{PBC_KEY}_cybersecurity_operations_center_runtime_parameter",
                "code": "WORKBENCH_LIMIT",
                "status": "active",
                "payload": default_parameter_records()[0],
            },
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict[str, Any]:
    plan = seed_plan()
    invalid_tables = tuple(record for record in plan["records"] if not record["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid_tables, "pbc": PBC_KEY, "invalid_tables": invalid_tables, "side_effects": ()}


def smoke_test() -> dict[str, Any]:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
