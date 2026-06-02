"""Seed data contracts for insurance underwriting."""

from __future__ import annotations

from .config import DEFAULT_RULES, DEFAULT_RUNTIME_PARAMETERS


PBC_KEY = "insurance_underwriting"


def seed_plan() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": "insurance_underwriting_underwriting_submission",
                "code": "SEED_SUBMISSION",
                "payload": {
                    "submission_id": "seed-submission",
                    "tenant": "default",
                    "product_line": "property",
                    "applicant_name": "Seed Applicant",
                    "jurisdiction": "US-NY",
                    "requested_limit": 500000.0,
                },
            },
            {
                "table": "insurance_underwriting_insurance_underwriting_policy_rule",
                "code": "SEED_RULES",
                "payload": DEFAULT_RULES,
            },
            {
                "table": "insurance_underwriting_insurance_underwriting_runtime_parameter",
                "code": "SEED_PARAMETERS",
                "payload": DEFAULT_RUNTIME_PARAMETERS,
            },
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    plan = seed_plan()
    invalid_tables = tuple(item["table"] for item in plan["records"] if not item["table"].startswith("insurance_underwriting_"))
    return {"ok": plan["ok"] and not invalid_tables, "pbc": PBC_KEY, "invalid_tables": invalid_tables, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
