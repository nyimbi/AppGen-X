"""API Gateway Mesh PBC implementation package."""

from ..source_contract import source_pbc_package_contract

PBC_KEY = "api_gateway_mesh"


def implementation_contract() -> dict:
    return source_pbc_package_contract(PBC_KEY)
