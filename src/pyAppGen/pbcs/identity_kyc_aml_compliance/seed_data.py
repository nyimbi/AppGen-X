"""Seed fixtures for the identity KYC / AML slice."""

from __future__ import annotations

PBC_KEY = "identity_kyc_aml_compliance"


def seed_plan():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": "identity_kyc_aml_compliance_kyc_profile",
                "id": "kyc-seed-0001",
                "tenant": "seed-tenant",
                "subject_name": "Seed Entity Ltd",
                "customer_type": "entity",
                "jurisdiction": "KE",
                "product_exposure": "trade_finance",
                "channel": "branch",
                "status": "pending_edd",
            },
            {
                "table": "identity_kyc_aml_compliance_runtime_parameter",
                "id": "param-workbench-limit",
                "tenant": "global",
                "parameter_name": "workbench_limit",
                "value": 50,
            },
            {
                "table": "identity_kyc_aml_compliance_policy_rule",
                "id": "rule-edd-trigger",
                "tenant": "global",
                "rule_name": "enhanced_due_diligence_trigger_matrix",
                "severity": "blocking",
            },
        ),
        "side_effects": (),
    }


def validate_seed_data():
    records = seed_plan()["records"]
    invalid = tuple(record for record in records if not record["table"].startswith("identity_kyc_aml_compliance_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_records": invalid, "side_effects": ()}


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
