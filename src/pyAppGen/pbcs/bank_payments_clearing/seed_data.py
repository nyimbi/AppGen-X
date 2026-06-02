"""Package-local seed data plans for bank_payments_clearing."""

from __future__ import annotations


PBC_KEY = "bank_payments_clearing"


def seed_plan() -> dict:
    records = (
        {
            "table": "bank_payments_clearing_participant_bank",
            "payload": {
                "participant_bank_id": "seed_bank_a",
                "routing_identifier": "021000021",
                "supported_rails": ("ach", "wire"),
                "status": "active",
            },
        },
        {
            "table": "bank_payments_clearing_payment_instruction",
            "payload": {
                "instruction_id": "seed_payment_1",
                "tenant": "seed_tenant",
                "rail": "ach",
                "participant_bank_id": "seed_bank_a",
                "amount": 125.0,
                "currency": "USD",
                "beneficiary_account": "123456789",
                "originator_authorized": True,
                "external_reference": "SEED-001",
                "screening_evidence": {"decision": "clear", "freshness": "current"},
            },
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "records": records, "side_effects": ()}


def validate_seed_data() -> dict:
    plan = seed_plan()
    invalid_tables = tuple(
        record["table"]
        for record in plan["records"]
        if not record["table"].startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": plan["ok"] and not invalid_tables,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_seed_data()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
