"""Product Catalog PIM PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
from .runtime import PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES
from .runtime import PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES
from .runtime import PRODUCT_CATALOG_PIM_OWNED_TABLES
from .runtime import PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
from .runtime import PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS
from .runtime import PRODUCT_CATALOG_PIM_RUNTIME_TABLES
from .runtime import PRODUCT_CATALOG_PIM_STANDARD_FEATURE_KEYS
from .runtime import product_catalog_pim_add_compliance_claim
from .runtime import product_catalog_pim_add_localized_content
from .runtime import product_catalog_pim_add_price_metadata
from .runtime import product_catalog_pim_attach_product_media
from .runtime import product_catalog_pim_binding_evidence
from .runtime import product_catalog_pim_build_api_contract
from .runtime import product_catalog_pim_build_workbench_view
from .runtime import product_catalog_pim_configure_runtime
from .runtime import product_catalog_pim_create_product_family
from .runtime import product_catalog_pim_define_attribute_schema
from .runtime import product_catalog_pim_empty_state
from .runtime import product_catalog_pim_permissions_contract
from .runtime import product_catalog_pim_publish_product
from .runtime import product_catalog_pim_receive_event
from .runtime import product_catalog_pim_register_product
from .runtime import product_catalog_pim_register_rule
from .runtime import product_catalog_pim_register_schema_extension
from .runtime import product_catalog_pim_runtime_capabilities
from .runtime import product_catalog_pim_runtime_smoke
from .runtime import product_catalog_pim_set_parameter
from .runtime import product_catalog_pim_set_product_attribute
from .runtime import product_catalog_pim_verify_owned_table_boundary
from .ui import PRODUCT_CATALOG_PIM_UI_FRAGMENT_KEYS
from .ui import product_catalog_pim_render_workbench
from .ui import product_catalog_pim_ui_contract

PBC_KEY = "product_catalog_pim"


def implementation_contract() -> dict:
    runtime = product_catalog_pim_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": product_catalog_pim_ui_contract(),
        "api_contract": product_catalog_pim_build_api_contract(),
        "permissions_contract": product_catalog_pim_permissions_contract(),
        "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES,
        "allowed_database_backends": PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS,
        "runtime_tables": PRODUCT_CATALOG_PIM_RUNTIME_TABLES,
        "required_event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
    }
