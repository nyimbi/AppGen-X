"""Service layer for the real_estate_property_management PBC."""
from .standalone import (
    PBC_KEY,
    QUERY_OPERATIONS,
    REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES as OWNED_TABLES,
    RealEstatePropertyManagementService,
    SERVICE_COMMAND_OPERATIONS as COMMAND_OPERATIONS,
    service_operation_manifest as _service_operation_manifest,
    service_operation_contracts as _service_operation_contracts,
    operation_plan as _operation_plan,
    service_smoke_test,
)

TRANSACTION_BOUNDARY = 'owned_datastore_plus_outbox'


class RealEstatePropertyManagementServiceFacade(RealEstatePropertyManagementService):
    transaction_boundary = TRANSACTION_BOUNDARY


def service_operation_manifest():
    return _service_operation_manifest()


def service_operation_contracts():
    contracts = _service_operation_contracts()
    contracts['transaction_boundary'] = TRANSACTION_BOUNDARY
    return contracts


def operation_plan(operation, payload=None):
    plan = _operation_plan(operation, payload)
    plan['transaction_boundary'] = TRANSACTION_BOUNDARY
    return plan


def smoke_test():
    return service_smoke_test()
