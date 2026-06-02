"""Seed data for electronic health records core."""
from __future__ import annotations

PBC_KEY = "electronic_health_records_core"


def seed_plan() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": "electronic_health_records_core_patient_chart",
                "chart_id": "seed-chart-001",
                "tenant": "seed-tenant",
                "patient_ref": "patient-seed-001",
                "legal_name": "Seed Patient",
                "date_of_birth": "1980-01-01",
            },
            {
                "table": "electronic_health_records_core_electronic_health_records_core_policy_rule",
                "rule_id": "summary_redaction_policy",
                "severity": "high",
            },
            {
                "table": "electronic_health_records_core_electronic_health_records_core_runtime_parameter",
                "name": "critical_result_ack_minutes",
                "value": 15,
            },
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    records = seed_plan()["records"]
    invalid = tuple(record for record in records if not str(record["table"]).startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_records": invalid, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
