"""Service contract for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import EVENT_CONTRACT, OPERATION_BLUEPRINTS, PBC_KEY, QUERY_BLUEPRINTS

COMMAND_METHODS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "command_data_product",
) + tuple(item["name"] for item in OPERATION_BLUEPRINTS)
QUERY_METHODS = tuple(
    dict.fromkeys(
        (
            "query_workbench",
            "build_workbench_view",
            "list_forms",
            "list_wizards",
            "list_controls",
            "document_instruction_plan",
            "datastore_crud_plan",
            "run_advanced_assessment",
        )
        + tuple(item["name"] for item in QUERY_BLUEPRINTS if item["name"] != "query_workbench")
    )
)


def build_service_contract() -> dict:
    return {
        "format": "appgen.data-product-catalog-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": COMMAND_METHODS,
        "query_methods": QUERY_METHODS,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def data_product_catalog_build_service_contract() -> dict:
    return build_service_contract()


def validate_service_contract() -> dict:
    contract = build_service_contract()
    return {
        "ok": contract["ok"] and len(contract["command_methods"]) >= 15 and bool(contract["query_methods"]),
        "contract": contract,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_service_contract()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
