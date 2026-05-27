from .runtime import NOTIFICATIONS_CONSUMED_EVENT_TYPES
from .runtime import NOTIFICATIONS_EMITTED_EVENT_TYPES
from .runtime import NOTIFICATIONS_OWNED_TABLES
from .runtime import NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS
from .runtime import NOTIFICATIONS_STANDARD_FEATURE_KEYS
from .runtime import notifications_build_api_contract
from .runtime import notifications_runtime_capabilities
from .ui import NOTIFICATIONS_UI_FRAGMENT_KEYS


PBC_KEY = 'notifications'

PBC_MANIFEST = {
    "pbc": "notifications",
    "label": "Omni-Channel Communication and Notifications",
    "mesh": "relationship",
    "description": "Omnichannel templates, localized variants, channels, recipients, consent, schedules, throttles, provider routing, delivery lifecycle, campaigns, transactional notifications, audit, analytics, and governed notification operations.",
    "datastore_backend": "postgresql",
    "tables": NOTIFICATIONS_OWNED_TABLES,
    "apis": tuple(route["route"] for route in notifications_build_api_contract()["routes"]),
    "emits": NOTIFICATIONS_EMITTED_EVENT_TYPES,
    "consumes": NOTIFICATIONS_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": NOTIFICATIONS_UI_FRAGMENT_KEYS,
    "permissions": tuple(sorted(notifications_build_api_contract()["permissions"])),
    "configuration": (
        "NOTIFICATIONS_DATABASE_URL",
        "NOTIFICATIONS_EVENT_TOPIC",
        "NOTIFICATIONS_RETRY_LIMIT",
        "NOTIFICATIONS_DEFAULT_LOCALE",
        "NOTIFICATIONS_DEFAULT_TIMEZONE",
        "NOTIFICATIONS_DELIVERY_MODE",
    ),
    "capabilities": tuple(f"notifications.{table}" for table in NOTIFICATIONS_OWNED_TABLES),
    "standard_features": NOTIFICATIONS_STANDARD_FEATURE_KEYS,
    "workflows": notifications_runtime_capabilities()["operations"],
    "analytics": (
        "delivery_success_rate",
        "bounce_rate",
        "fatigue_risk",
        "provider_route_score",
        "channel_health",
        "campaign_dispatch_rate",
        "transactional_dispatch_rate",
        "message_delivered_throughput",
        "message_failed_throughput",
    ),
    "advanced_capabilities": NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py",),
    "docs": ("RELEASE_EVIDENCE.md", "SPECIFICATION.md"),
}
