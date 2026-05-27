"""Schema contract facade for the multi_sided_market PBC."""
from .runtime import multi_sided_market_build_schema_contract


def build_schema_contract():
    return multi_sided_market_build_schema_contract()


def validate_schema_contract():
    contract = build_schema_contract()
    return {'ok': contract['ok'] and not contract['shared_table_access'], 'contract': contract, 'side_effects': ()}


def smoke_test():
    return validate_schema_contract()
