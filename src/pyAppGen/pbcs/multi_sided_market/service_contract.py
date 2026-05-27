"""Service contract facade for the multi_sided_market PBC."""
from .runtime import multi_sided_market_build_service_contract


def build_service_contract():
    return multi_sided_market_build_service_contract()


def validate_service_contract():
    contract = build_service_contract()
    return {'ok': contract['ok'] and contract['transaction_boundary'] == 'owned_datastore_plus_outbox', 'contract': contract, 'side_effects': ()}


def smoke_test():
    return validate_service_contract()
