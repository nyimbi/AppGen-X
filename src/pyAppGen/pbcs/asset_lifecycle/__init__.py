"""Asset Lifecycle PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import ASSET_LIFECYCLE_RUNTIME_CAPABILITY_KEYS
from .runtime import ASSET_LIFECYCLE_STANDARD_FEATURE_KEYS
from .runtime import asset_lifecycle_build_depreciation_schedule
from .runtime import asset_lifecycle_build_workbench_view
from .runtime import asset_lifecycle_configure_runtime
from .runtime import asset_lifecycle_empty_state
from .runtime import asset_lifecycle_place_asset_in_service
from .runtime import asset_lifecycle_register_asset
from .runtime import asset_lifecycle_register_rule
from .runtime import asset_lifecycle_retire_asset
from .runtime import asset_lifecycle_run_depreciation
from .runtime import asset_lifecycle_runtime_capabilities
from .runtime import asset_lifecycle_runtime_smoke
from .runtime import asset_lifecycle_set_parameter
from .runtime import asset_lifecycle_transfer_asset
from .ui import ASSET_LIFECYCLE_UI_FRAGMENT_KEYS
from .ui import asset_lifecycle_render_workbench
from .ui import asset_lifecycle_ui_contract

PBC_KEY = "asset_lifecycle"


def implementation_contract() -> dict:
    runtime = asset_lifecycle_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": asset_lifecycle_ui_contract(),
    }
