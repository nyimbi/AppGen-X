from .runtime import (
    SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    SPORTS_VENUE_EVENT_OPERATIONS_BUSINESS_TABLES,
    SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES,
    sports_venue_event_operations_build_schema_contract,
)


def model_contracts():
    return sports_venue_event_operations_build_schema_contract()["models"]


def standalone_model_contract():
    return {
        "ok": True,
        "pbc": "sports_venue_event_operations",
        "table_keys": SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES,
        "business_table_keys": SPORTS_VENUE_EVENT_OPERATIONS_BUSINESS_TABLES,
        "database_backends": SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def standalone_store_smoke_test():
    contract = standalone_model_contract()
    return {
        "ok": contract["ok"]
        and len(contract["business_table_keys"]) >= 20
        and contract["event_contract"] == "AppGen-X",
        "contract": contract,
        "side_effects": (),
    }
