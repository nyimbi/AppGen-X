"""Tax Localization PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import TAX_LOCALIZATION_RUNTIME_CAPABILITY_KEYS
from .runtime import TAX_LOCALIZATION_STANDARD_FEATURE_KEYS
from .runtime import tax_localization_build_workbench_view
from .runtime import tax_localization_calculate_tax_quote
from .runtime import tax_localization_classify_product
from .runtime import tax_localization_empty_state
from .runtime import tax_localization_prepare_tax_filing
from .runtime import tax_localization_record_invoice_tax
from .runtime import tax_localization_register_jurisdiction
from .runtime import tax_localization_register_tax_rule
from .runtime import tax_localization_runtime_capabilities
from .runtime import tax_localization_runtime_smoke
from .runtime import tax_localization_validate_exemption_certificate

PBC_KEY = "tax_localization"


def implementation_contract() -> dict:
    runtime = tax_localization_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
    }
