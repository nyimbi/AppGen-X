"""World-class domain depth contract for the real_estate_property_management PBC."""
from .standalone import (
    PARAMETERS as DOMAIN_PARAMETERS,
    RULES as DOMAIN_RULES,
    REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_CAPABILITY_KEYS as DOMAIN_ADVANCED_CAPABILITIES,
    REAL_ESTATE_PROPERTY_MANAGEMENT_BUSINESS_TABLES as DOMAIN_OWNED_TABLES,
    DOMAIN_OPERATIONS,
    DOMAIN_EDGE_CASES,
    domain_depth_contract,
    execute_domain_operation,
    domain_depth_smoke_test,
    domain_capability_surface_contract,
)

DOMAIN_EVENTS = domain_depth_contract()['emitted_events']
DOMAIN_CONSUMED_EVENTS = domain_depth_contract()['consumed_events']
DOMAIN_WORKBENCH_VIEWS = domain_depth_contract()['workbench_views']
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        tuple(DOMAIN_ADVANCED_CAPABILITIES)
        + tuple(f'specialist_{operation}' for operation in DOMAIN_OPERATIONS)
        + tuple(f'rule_driven_{rule}' for rule in DOMAIN_RULES)
    )
)
