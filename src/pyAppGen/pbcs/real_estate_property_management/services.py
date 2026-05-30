"""Service layer for the real_estate_property_management PBC."""
from .standalone import (
    PBC_KEY,
    QUERY_OPERATIONS,
    REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES as OWNED_TABLES,
    RealEstatePropertyManagementService,
    SERVICE_COMMAND_OPERATIONS as COMMAND_OPERATIONS,
    service_operation_manifest,
    service_operation_contracts,
    operation_plan,
    service_smoke_test,
)

EVENT_CONTRACT = {
    'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
    'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
    'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
    'event_contract': 'AppGen-X',
}


def smoke_test():
    return service_smoke_test()
