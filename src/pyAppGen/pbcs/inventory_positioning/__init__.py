"""Inventory Positioning PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
from .runtime import INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_OWNED_TABLES
from .runtime import INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC
from .runtime import INVENTORY_POSITIONING_RUNTIME_CAPABILITY_KEYS
from .runtime import INVENTORY_POSITIONING_STANDARD_FEATURE_KEYS
from .runtime import inventory_positioning_allocate_inventory
from .runtime import inventory_positioning_build_api_contract
from .runtime import inventory_positioning_build_release_evidence
from .runtime import inventory_positioning_build_schema_contract
from .runtime import inventory_positioning_build_service_contract
from .runtime import inventory_positioning_build_workbench_view
from .runtime import inventory_positioning_calculate_availability
from .runtime import inventory_positioning_configure_runtime
from .runtime import inventory_positioning_empty_state
from .runtime import inventory_positioning_permissions_contract
from .runtime import inventory_positioning_post_goods_receipt
from .runtime import inventory_positioning_receive_event
from .runtime import inventory_positioning_release_allocation
from .runtime import inventory_positioning_register_item
from .runtime import inventory_positioning_register_node
from .runtime import inventory_positioning_register_rule
from .runtime import inventory_positioning_register_schema_extension
from .runtime import inventory_positioning_runtime_capabilities
from .runtime import inventory_positioning_runtime_smoke
from .runtime import inventory_positioning_set_parameter
from .runtime import inventory_positioning_verify_owned_table_boundary
from .ui import INVENTORY_POSITIONING_UI_FRAGMENT_KEYS
from .ui import inventory_positioning_render_workbench
from .ui import inventory_positioning_ui_contract

PBC_KEY = "inventory_positioning"


def implementation_contract() -> dict:
    runtime = inventory_positioning_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
        "allowed_database_backends": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS,
        "api_contract": inventory_positioning_build_api_contract(),
        "schema_contract": inventory_positioning_build_schema_contract(),
        "service_contract": inventory_positioning_build_service_contract(),
        "release_evidence_contract": inventory_positioning_build_release_evidence(),
        "permissions_contract": inventory_positioning_permissions_contract(),
        "required_event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
        "consumes": INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES,
        "emits": INVENTORY_POSITIONING_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime,
        "ui_contract": inventory_positioning_ui_contract(),
    }
