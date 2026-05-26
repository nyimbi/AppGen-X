"""Loyalty Rewards PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
from .runtime import LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
from .runtime import LOYALTY_REWARDS_EMITTED_EVENT_TYPES
from .runtime import LOYALTY_REWARDS_OWNED_TABLES
from .runtime import LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
from .runtime import LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS
from .runtime import LOYALTY_REWARDS_RUNTIME_TABLES
from .runtime import LOYALTY_REWARDS_STANDARD_FEATURE_KEYS
from .runtime import loyalty_rewards_adjust_points
from .runtime import loyalty_rewards_build_api_contract
from .runtime import loyalty_rewards_build_release_evidence
from .runtime import loyalty_rewards_build_schema_contract
from .runtime import loyalty_rewards_build_service_contract
from .runtime import loyalty_rewards_build_workbench_view
from .runtime import loyalty_rewards_configure_runtime
from .runtime import loyalty_rewards_create_redemption
from .runtime import loyalty_rewards_empty_state
from .runtime import loyalty_rewards_enroll_member
from .runtime import loyalty_rewards_expire_points
from .runtime import loyalty_rewards_issue_points
from .runtime import loyalty_rewards_permissions_contract
from .runtime import loyalty_rewards_receive_event
from .runtime import loyalty_rewards_register_earning_rule
from .runtime import loyalty_rewards_register_rule
from .runtime import loyalty_rewards_register_schema_extension
from .runtime import loyalty_rewards_runtime_capabilities
from .runtime import loyalty_rewards_runtime_smoke
from .runtime import loyalty_rewards_set_parameter
from .runtime import loyalty_rewards_verify_owned_table_boundary
from .ui import LOYALTY_REWARDS_UI_FRAGMENT_KEYS
from .ui import loyalty_rewards_render_workbench
from .ui import loyalty_rewards_ui_contract

PBC_KEY = "loyalty_rewards"


def implementation_contract() -> dict:
    runtime = loyalty_rewards_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": loyalty_rewards_ui_contract(),
        "api_contract": loyalty_rewards_build_api_contract(),
        "schema_contract": loyalty_rewards_build_schema_contract(),
        "service_contract": loyalty_rewards_build_service_contract(),
        "release_evidence_contract": loyalty_rewards_build_release_evidence(),
        "permissions_contract": loyalty_rewards_permissions_contract(),
        "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
        "runtime_tables": LOYALTY_REWARDS_RUNTIME_TABLES,
        "allowed_database_backends": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
        "consumes": LOYALTY_REWARDS_CONSUMED_EVENT_TYPES,
        "emits": LOYALTY_REWARDS_EMITTED_EVENT_TYPES,
    }
