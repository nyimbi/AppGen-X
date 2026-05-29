"""Package manifest for the Loyalty Rewards PBC."""

from __future__ import annotations

from .runtime import LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
from .runtime import LOYALTY_REWARDS_EMITTED_EVENT_TYPES
from .runtime import LOYALTY_REWARDS_OWNED_TABLES
from .runtime import LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS
from .runtime import LOYALTY_REWARDS_STANDARD_FEATURE_KEYS
from .runtime import loyalty_rewards_build_api_contract
from .runtime import loyalty_rewards_runtime_capabilities
from .ui import LOYALTY_REWARDS_UI_FRAGMENT_KEYS


PBC_KEY = "loyalty_rewards"

PBC_MANIFEST = {
    "pbc": "loyalty_rewards",
    "label": "Customer Loyalty Points and Rewards",
    "mesh": "relationship",
    "description": (
        "Member wallets, point accrual, adjustments, redemptions, tiers, "
        "earning rules, referrals, partner accruals, fraud controls, liability, "
        "forecasting, governance, and AppGen-X event orchestration."
    ),
    "datastore_backend": "postgresql",
    "tables": LOYALTY_REWARDS_OWNED_TABLES,
    "apis": tuple(route["route"] for route in loyalty_rewards_build_api_contract()["routes"]),
    "emits": LOYALTY_REWARDS_EMITTED_EVENT_TYPES,
    "consumes": LOYALTY_REWARDS_CONSUMED_EVENT_TYPES,
    "template": "standalone_one_pbc_app",
    "ui_fragments": LOYALTY_REWARDS_UI_FRAGMENT_KEYS,
    "permissions": tuple(sorted(loyalty_rewards_build_api_contract()["permissions"])),
    "configuration": (
        "LOYALTY_REWARDS_DATABASE_URL",
        "LOYALTY_REWARDS_EVENT_TOPIC",
        "LOYALTY_REWARDS_RETRY_LIMIT",
        "LOYALTY_REWARDS_DEFAULT_CURRENCY",
        "LOYALTY_REWARDS_DEFAULT_TIMEZONE",
        "LOYALTY_REWARDS_LIABILITY_MODE",
    ),
    "capabilities": tuple(f"loyalty_rewards.{table}" for table in LOYALTY_REWARDS_OWNED_TABLES),
    "standard_features": LOYALTY_REWARDS_STANDARD_FEATURE_KEYS,
    "workflows": loyalty_rewards_runtime_capabilities()["operations"],
    "analytics": (
        "points_earned",
        "points_redeemed",
        "liability_amount",
        "breakage_risk",
        "fraud_review_rate",
        "tier_progression",
        "reward_balance_changed_throughput",
        "customer_segment_updated_throughput",
    ),
    "advanced_capabilities": LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py", "tests/test_standalone.py"),
    "docs": ("RELEASE_EVIDENCE.md", "SPECIFICATION.md"),
}
