"""Service contract for the planning_budgeting_forecasting PBC."""


def build_service_contract():
    return {'format': 'appgen.planning-budgeting-forecasting-service-contract.v1', 'ok': True, 'pbc': 'planning_budgeting_forecasting', 'command_methods': ('command_planning_model', 'configure_runtime', 'set_parameter', 'register_rule'), 'query_methods': ('query_workbench',), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def planning_budgeting_forecasting_build_service_contract():
    return build_service_contract()


def validate_service_contract():
    contract = build_service_contract()
    return {'ok': contract['ok'] and bool(contract['command_methods']) and bool(contract['query_methods']) and contract['shared_table_access'] is False, 'contract': contract, 'side_effects': ()}


def smoke_test():
    return validate_service_contract()
