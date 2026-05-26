"""Customer 360 PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import CUSTOMER_360_RUNTIME_CAPABILITY_KEYS
from .runtime import CUSTOMER_360_STANDARD_FEATURE_KEYS
from .runtime import customer_360_build_timeline
from .runtime import customer_360_build_workbench_view
from .runtime import customer_360_capture_touchpoint
from .runtime import customer_360_configure_runtime
from .runtime import customer_360_create_profile
from .runtime import customer_360_empty_state
from .runtime import customer_360_ingest_engagement_event
from .runtime import customer_360_link_identity
from .runtime import customer_360_open_merge_case
from .runtime import customer_360_record_consent
from .runtime import customer_360_register_rule
from .runtime import customer_360_resolve_merge_case
from .runtime import customer_360_runtime_capabilities
from .runtime import customer_360_runtime_smoke
from .runtime import customer_360_set_parameter
from .runtime import customer_360_set_preference
from .ui import CUSTOMER_360_UI_FRAGMENT_KEYS
from .ui import customer_360_render_workbench
from .ui import customer_360_ui_contract

PBC_KEY = "customer_360"


def implementation_contract() -> dict:
    runtime = customer_360_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": customer_360_ui_contract(),
    }
