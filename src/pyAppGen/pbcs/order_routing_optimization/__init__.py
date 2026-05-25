"""Order Routing Optimization PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "order_routing_optimization"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
