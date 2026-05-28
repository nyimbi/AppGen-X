"""Service contract for the insurance_claims_policy PBC."""


def build_service_contract():
    return {'format': 'appgen.insurance-claims-policy-service-contract.v1', 'ok': True, 'pbc': 'insurance_claims_policy', 'command_methods': ('command_insurance_policy', 'configure_runtime', 'set_parameter', 'register_rule'), 'query_methods': ('query_workbench',), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def insurance_claims_policy_build_service_contract():
    return build_service_contract()


def validate_service_contract():
    contract = build_service_contract()
    return {'ok': contract['ok'] and bool(contract['command_methods']) and bool(contract['query_methods']) and contract['shared_table_access'] is False, 'contract': contract, 'side_effects': ()}


def smoke_test():
    return validate_service_contract()
