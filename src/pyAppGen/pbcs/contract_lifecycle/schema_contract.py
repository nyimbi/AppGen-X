"""Generated owned schema evidence for the contract_lifecycle PBC."""

from .application import PBC_KEY, schema_contract


def build_schema_contract():
    return schema_contract()


def contract_lifecycle_build_schema_contract():
    return build_schema_contract()


def validate_schema_contract():
    contract = build_schema_contract()
    missing_models = tuple(table for table in contract["tables"] if not table["owned_table"].startswith(f"{PBC_KEY}_"))
    return {
        "ok": contract["ok"] and not missing_models and contract["shared_table_access"] is False,
        "contract": contract,
        "missing_models": missing_models,
    }


def smoke_test():
    return validate_schema_contract()
