"""Service contract for the expense_management PBC."""


def build_service_contract():
    return {'format': 'appgen.expense-management-service-contract.v1', 'ok': True, 'pbc': 'expense_management', 'command_methods': ('command_expense_report', 'configure_runtime', 'set_parameter', 'register_rule'), 'query_methods': ('query_workbench',), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def expense_management_build_service_contract():
    return build_service_contract()


def validate_service_contract():
    contract = build_service_contract()
    return {'ok': contract['ok'] and bool(contract['command_methods']) and bool(contract['query_methods']) and contract['shared_table_access'] is False, 'contract': contract, 'side_effects': ()}


def smoke_test():
    return validate_service_contract()

from .domain_depth import DOMAIN_OPERATIONS, domain_depth_contract

_BASE_BUILD_SERVICE_CONTRACT = build_service_contract

def build_service_contract():
    base = dict(_BASE_BUILD_SERVICE_CONTRACT())
    domain = domain_depth_contract()
    return {
        **base,
        'ok': base.get('ok') is True and domain['ok'],
        'command_methods': tuple(dict.fromkeys(tuple(base.get('command_methods', ())) + tuple(DOMAIN_OPERATIONS))),
        'world_class_domain_depth': domain,
    }


def expense_management_build_service_contract():
    return build_service_contract()
