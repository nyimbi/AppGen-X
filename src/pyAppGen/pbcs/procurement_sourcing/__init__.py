"""Procurement Sourcing PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import PROCUREMENT_SOURCING_RUNTIME_CAPABILITY_KEYS
from .runtime import PROCUREMENT_SOURCING_STANDARD_FEATURE_KEYS
from .runtime import procurement_sourcing_approve_requisition
from .runtime import procurement_sourcing_build_workbench_view
from .runtime import procurement_sourcing_capture_bid
from .runtime import procurement_sourcing_configure_runtime
from .runtime import procurement_sourcing_create_contract
from .runtime import procurement_sourcing_create_requisition
from .runtime import procurement_sourcing_create_rfq
from .runtime import procurement_sourcing_empty_state
from .runtime import procurement_sourcing_issue_purchase_order
from .runtime import procurement_sourcing_register_rule
from .runtime import procurement_sourcing_runtime_capabilities
from .runtime import procurement_sourcing_runtime_smoke
from .runtime import procurement_sourcing_score_suppliers
from .runtime import procurement_sourcing_select_supplier
from .runtime import procurement_sourcing_set_parameter

PBC_KEY = "procurement_sourcing"


def implementation_contract() -> dict:
    runtime = procurement_sourcing_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
    }
