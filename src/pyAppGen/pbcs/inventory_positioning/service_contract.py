"""Executable service contract for the inventory_positioning PBC."""

from __future__ import annotations

from .events import DEAD_LETTER_TABLE
from .events import EVENT_CONTRACT
from .events import INBOX_TABLE
from .events import OUTBOX_TABLE
from .services import service_operation_contracts


PBC_KEY = "inventory_positioning"


def build_service_contract() -> dict:
    manifest = service_operation_contracts()
    command_contracts = tuple(item for item in manifest["contracts"] if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in manifest["contracts"] if item["operation_kind"] == "query")
    mutates_only = tuple(sorted({table for item in command_contracts for table in item["owned_tables"]}))
    return {
        "format": "appgen.inventory-positioning-service-contract.v1",
        "ok": manifest["ok"] and bool(command_contracts) and bool(query_contracts),
        "pbc": PBC_KEY,
        "transaction_boundary": "inventory_positioning_owned_datastore_plus_appgen_outbox",
        "command_methods": tuple(item["operation"] for item in command_contracts),
        "query_methods": tuple(item["operation"] for item in query_contracts),
        "mutates_only": mutates_only,
        "external_dependencies": {
            "apis": (
                "GET /identity/policies",
                "POST /audit/contract-events",
                "GET /schema/events",
            ),
            "events": tuple(item["event_type"] for item in EVENT_CONTRACT["consumed"]),
            "api_projections": (
                "order_demand_projection",
                "shipment_delivery_projection",
                "quality_release_projection",
                "purchase_receipt_projection",
                "demand_forecast_projection",
                "access_policy_projection",
            ),
            "shared_tables": (),
        },
        "eventing": {
            "outbox_table": OUTBOX_TABLE,
            "inbox_table": INBOX_TABLE,
            "dead_letter_table": DEAD_LETTER_TABLE,
            "event_contract": "AppGen-X",
        },
        "shared_table_access": False,
    }


SERVICE_CONTRACT = build_service_contract()
