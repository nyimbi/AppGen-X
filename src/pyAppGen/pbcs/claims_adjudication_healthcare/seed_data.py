"""Package-local seed data for the executable adjudication slice."""

from __future__ import annotations

from typing import Any

from .models import BUSINESS_TABLES
from .models import PBC_KEY


def seed_plan() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": BUSINESS_TABLES[3],
                "record": {
                    "rule_id": "benefit_seed_office_visit",
                    "tenant": "default",
                    "plan_id": "commercial-a",
                    "service_code": "99213",
                    "description": "Seed office visit coverage rule",
                    "covered": True,
                    "auth_required": False,
                    "allowed_percentage": 0.85,
                    "copay_amount": 20,
                    "deductible_apply": True,
                    "max_units": 4,
                    "effective_from": "2026-01-01",
                    "effective_to": "2026-12-31",
                    "status": "approved",
                },
            },
            {
                "table": BUSINESS_TABLES[8],
                "record": {
                    "parameter_name": "workbench_limit",
                    "tenant": "default",
                    "value": 25,
                    "minimum": 5,
                    "maximum": 200,
                    "unit": "rows",
                    "status": "active",
                },
            },
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict[str, Any]:
    plan = seed_plan()
    invalid_tables = tuple(entry["table"] for entry in plan["records"] if not entry["table"].startswith(f"{PBC_KEY}_"))
    return {
        "ok": not invalid_tables,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
