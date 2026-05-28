"""Generated service evidence for the dom PBC."""

from __future__ import annotations

from . import services


SERVICE_CONTRACT = {
    **services.service_operation_manifest()["standalone_service"],
    "format": "appgen.dom-service-contract.v1",
    "transaction_boundary": "dom_owned_datastore_plus_appgen_outbox",
    "command_methods": tuple(
        method for method in services.standalone_service_manifest()["service_methods"] if method not in {"workbench", "crud_mutation_plan", "get_order_snapshot"}
    ),
    "query_methods": services.standalone_service_manifest()["query_methods"],
    "mutates_only": (
        "sales_order",
        "order_line",
        "order_status",
        "order_hold",
        "order_promise",
        "tax_projection",
        "fraud_screen",
        "inventory_allocation_projection",
        "fulfillment_plan",
        "split_shipment",
        "backorder",
        "substitution",
        "cancellation_request",
        "shipment_projection",
        "order_exception",
        "dom_appgen_outbox_event",
        "dom_appgen_inbox_event",
        "dom_dead_letter_event",
    ),
    "external_dependencies": {
        "apis": (
            "GET /inventory/allocations/{id}",
            "GET /tax/calculations/{id}",
            "GET /customers/{id}",
            "GET /payments/authorizations/{id}",
            "GET /shipments/{id}",
            "POST /audit/order-events",
        ),
        "events": (
            "InventoryAllocated",
            "TaxCalculated",
            "CustomerUpdated",
            "PaymentAuthorized",
            "ShipmentDelivered",
        ),
        "api_projections": (
            "inventory_allocation_projection",
            "tax_calculation_projection",
            "customer_profile_projection",
            "payment_authorization_projection",
            "shipment_delivery_projection",
        ),
        "shared_tables": (),
    },
    "pbc": "dom",
    "shared_table_access": False,
}


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)
