"""Schema-aligned model contracts for the identity KYC / AML slice."""

from __future__ import annotations

from .runtime import identity_kyc_aml_compliance_build_schema_contract


def model_contracts() -> tuple[dict, ...]:
    return identity_kyc_aml_compliance_build_schema_contract()["models"]


def smoke_test() -> dict:
    contracts = model_contracts()
    return {
        "ok": bool(contracts) and all(item["table"].startswith("identity_kyc_aml_compliance_") for item in contracts),
        "models": contracts,
        "side_effects": (),
    }
