"""Tax Localization PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS
from .runtime import TAX_LOCALIZATION_CONSUMED_EVENT_TYPES
from .runtime import TAX_LOCALIZATION_EMITTED_EVENT_TYPES
from .runtime import TAX_LOCALIZATION_OWNED_TABLES
from .runtime import TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC
from .runtime import TAX_LOCALIZATION_RUNTIME_CAPABILITY_KEYS
from .runtime import TAX_LOCALIZATION_STANDARD_FEATURE_KEYS
from .runtime import tax_localization_build_api_contract
from .runtime import tax_localization_build_release_evidence
from .runtime import tax_localization_build_schema_contract
from .runtime import tax_localization_build_service_contract
from .runtime import tax_localization_build_workbench_view
from .runtime import tax_localization_calculate_tax_quote
from .runtime import tax_localization_classify_product
from .runtime import tax_localization_configure_runtime
from .runtime import tax_localization_empty_state
from .runtime import tax_localization_permissions_contract
from .runtime import tax_localization_prepare_tax_filing
from .runtime import tax_localization_receive_event
from .runtime import tax_localization_record_invoice_tax
from .runtime import tax_localization_register_jurisdiction
from .runtime import tax_localization_register_rule
from .runtime import tax_localization_register_schema_extension
from .runtime import tax_localization_register_tax_rule
from .runtime import tax_localization_runtime_capabilities
from .runtime import tax_localization_runtime_smoke
from .runtime import tax_localization_set_parameter
from .runtime import tax_localization_validate_exemption_certificate
from .runtime import tax_localization_verify_owned_table_boundary
from .ui import TAX_LOCALIZATION_UI_FRAGMENT_KEYS
from .ui import tax_localization_render_workbench
from .ui import tax_localization_ui_contract

PBC_KEY = "tax_localization"


def implementation_contract() -> dict:
    runtime = tax_localization_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": TAX_LOCALIZATION_OWNED_TABLES,
        "allowed_database_backends": TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS,
        "api_contract": tax_localization_build_api_contract(),
        "schema_contract": tax_localization_build_schema_contract(),
        "service_contract": tax_localization_build_service_contract(),
        "release_evidence_contract": tax_localization_build_release_evidence(),
        "permissions_contract": tax_localization_permissions_contract(),
        "required_event_topic": TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC,
        "consumes": TAX_LOCALIZATION_CONSUMED_EVENT_TYPES,
        "emits": TAX_LOCALIZATION_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime,
        "ui_contract": tax_localization_ui_contract(),
    }
