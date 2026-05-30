"""Service layer for the dom PBC."""

from __future__ import annotations

from typing import Any

from . import standalone
from .runtime import DOM_REQUIRED_EVENT_TOPIC


EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": DOM_REQUIRED_EVENT_TOPIC,
    "inbox_topic": DOM_REQUIRED_EVENT_TOPIC,
    "outbox_table": "dom_appgen_outbox_event",
    "inbox_table": "dom_appgen_inbox_event",
    "dead_letter_table": "dom_dead_letter_event",
    "retry_policy": {"name": "dom_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": "dom_appgen_inbox_event"},
}


OPERATION_CONTRACTS = (
    {
        "operation": "command_dom_orders",
        "operation_kind": "command",
        "service_method": "capture_order",
        "method": "POST",
        "path": "/dom/orders",
        "permission": "dom.create",
        "owned_tables": ("dom_sales_order", "dom_order_line", "dom_order_status", "dom_order_promise", "dom_order_channel_context", "dom_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "OrderCaptured",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_orders_id_tax_projection",
        "operation_kind": "command",
        "service_method": "apply_tax_projection",
        "method": "POST",
        "path": "/dom/orders/{id}/tax-projection",
        "permission": "dom.verify",
        "owned_tables": ("dom_tax_projection", "dom_order_exception", "dom_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "TaxProjectionApplied",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_orders_id_fraud_screen",
        "operation_kind": "command",
        "service_method": "screen_fraud",
        "method": "POST",
        "path": "/dom/orders/{id}/fraud-screen",
        "permission": "dom.verify",
        "owned_tables": ("dom_fraud_screen", "dom_order_hold", "dom_order_exception", "dom_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "FraudScreened",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_orders_id_verify",
        "operation_kind": "command",
        "service_method": "verify_order",
        "method": "POST",
        "path": "/dom/orders/{id}/verify",
        "permission": "dom.verify",
        "owned_tables": ("dom_sales_order", "dom_order_status", "dom_order_verification", "dom_order_exception", "dom_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "OrderVerified",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_orders_id_price",
        "operation_kind": "command",
        "service_method": "price_order",
        "method": "POST",
        "path": "/dom/orders/{id}/price",
        "permission": "dom.price",
        "owned_tables": ("dom_sales_order", "dom_order_price_component", "dom_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "OrderPriced",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_orders_id_allocation",
        "operation_kind": "command",
        "service_method": "apply_inventory_allocation",
        "method": "POST",
        "path": "/dom/orders/{id}/allocation",
        "permission": "dom.allocate",
        "owned_tables": ("dom_inventory_allocation_projection", "dom_backorder", "dom_order_exception", "dom_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "InventoryAllocationProjected",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_orders_id_release_hold",
        "operation_kind": "command",
        "service_method": "release_hold",
        "method": "POST",
        "path": "/dom/orders/{id}/holds/{hold_id}/release",
        "permission": "dom.plan",
        "owned_tables": ("dom_order_hold", "dom_order_status", "dom_order_exception"),
        "read_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_orders_id_cancellations",
        "operation_kind": "command",
        "service_method": "request_cancellation",
        "method": "POST",
        "path": "/dom/orders/{id}/cancellations",
        "permission": "dom.cancel",
        "owned_tables": ("dom_cancellation_request", "dom_sales_order", "dom_order_exception"),
        "read_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_orders_id_substitutions",
        "operation_kind": "command",
        "service_method": "apply_substitution",
        "method": "POST",
        "path": "/dom/orders/{id}/substitutions",
        "permission": "dom.plan",
        "owned_tables": ("dom_substitution", "dom_backorder"),
        "read_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_fulfillment_plans",
        "operation_kind": "command",
        "service_method": "create_fulfillment_plan",
        "method": "POST",
        "path": "/dom/fulfillment-plans",
        "permission": "dom.plan",
        "owned_tables": ("dom_fulfillment_plan", "dom_fulfillment_plan_line", "dom_split_shipment", "dom_route_selection", "dom_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "FulfillmentPlanCreated",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_shipments",
        "operation_kind": "command",
        "service_method": "confirm_order_shipped",
        "method": "POST",
        "path": "/dom/shipments",
        "permission": "dom.ship",
        "owned_tables": ("dom_shipment_projection", "dom_shipment_status_projection", "dom_sales_order", "dom_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "OrderShipped",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_dom_events_inbox",
        "operation_kind": "command",
        "service_method": "receive_event",
        "method": "POST",
        "path": "/dom/events/inbox",
        "permission": "dom.event",
        "owned_tables": ("dom_appgen_inbox_event", "dom_dead_letter_event"),
        "read_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_dom_workbench",
        "operation_kind": "query",
        "service_method": "workbench",
        "method": "GET",
        "path": "/dom/workbench",
        "permission": "dom.audit",
        "owned_tables": (),
        "read_tables": ("dom_sales_order", "dom_order_hold", "dom_backorder", "dom_substitution", "dom_cancellation_request", "dom_order_exception"),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
)


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item["operation"] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": "dom",
        "operations": operations,
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    table_scope = contract["owned_tables"] or contract["read_tables"]
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": "dom",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "service_method": contract["service_method"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "side_effects": (),
    }


class DomService:
    """Side-effect-free generated command facade kept for compatibility."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": "dom",
            "operation": operation_name,
            "operation_kind": operation_kind,
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if operation_kind == "command":
            event_type = plan.get("emitted_event")
            result.update(
                {
                    "command": operation_name,
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (event_type,) if event_type else (),
                }
            )
        elif operation_kind == "query":
            result.update(
                {
                    "query": operation_name,
                    "read_only": True,
                    "outbox_table": None,
                    "emits": (),
                }
            )
        return result

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

    def command_dom_orders(self, payload=None):
        return self._command("command_dom_orders", payload or {})

    def command_dom_orders_id_tax_projection(self, payload=None):
        return self._command("command_dom_orders_id_tax_projection", payload or {})

    def command_dom_orders_id_fraud_screen(self, payload=None):
        return self._command("command_dom_orders_id_fraud_screen", payload or {})

    def command_dom_orders_id_verify(self, payload=None):
        return self._command("command_dom_orders_id_verify", payload or {})

    def command_dom_orders_id_price(self, payload=None):
        return self._command("command_dom_orders_id_price", payload or {})

    def command_dom_orders_id_allocation(self, payload=None):
        return self._command("command_dom_orders_id_allocation", payload or {})

    def command_dom_orders_id_release_hold(self, payload=None):
        return self._command("command_dom_orders_id_release_hold", payload or {})

    def command_dom_orders_id_cancellations(self, payload=None):
        return self._command("command_dom_orders_id_cancellations", payload or {})

    def command_dom_orders_id_substitutions(self, payload=None):
        return self._command("command_dom_orders_id_substitutions", payload or {})

    def command_dom_fulfillment_plans(self, payload=None):
        return self._command("command_dom_fulfillment_plans", payload or {})

    def command_dom_shipments(self, payload=None):
        return self._command("command_dom_shipments", payload or {})

    def command_dom_events_inbox(self, payload=None):
        return self._command("command_dom_events_inbox", payload or {})

    def query_dom_workbench(self, payload=None):
        return self._query("query_dom_workbench", payload or {})


class DomStandaloneService:
    """Executable standalone service wrapper for the one-PBC application."""

    def __init__(self, *, tenant: str = "default") -> None:
        self.app = standalone.DomStandaloneApplication(tenant=tenant)

    @property
    def state(self) -> dict[str, Any]:
        return self.app.snapshot()

    def configure(self, configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.app.configure(configuration)

    def register_defaults(self, *, tenant: str | None = None) -> dict[str, Any]:
        return self.app.register_defaults(tenant=tenant)

    def upsert_customer_projection(self, customer: dict[str, Any]) -> dict[str, Any]:
        return self.app.upsert_customer_projection(customer)

    def capture_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.capture_order(payload)

    def apply_tax_projection(self, order_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.apply_tax_projection(order_id, payload)

    def screen_fraud(self, order_id: str, *, signals: dict[str, Any]) -> dict[str, Any]:
        return self.app.screen_fraud(order_id, signals=signals)

    def verify_order(self, order_id: str) -> dict[str, Any]:
        return self.app.verify_order(order_id)

    def price_order(self, order_id: str) -> dict[str, Any]:
        return self.app.price_order(order_id)

    def apply_inventory_allocation(self, order_id: str, allocations: dict[str, Any] | tuple[dict[str, Any], ...]) -> dict[str, Any]:
        return self.app.apply_inventory_allocation(order_id, allocations)

    def create_fulfillment_plan(self, order_id: str) -> dict[str, Any]:
        return self.app.create_fulfillment_plan(order_id)

    def route_fulfillment(self, order_id: str, *, rails: tuple[dict[str, Any], ...] | None = None) -> dict[str, Any]:
        return self.app.route_fulfillment(order_id, rails=rails)

    def release_hold(self, *, order_id: str, hold_id: str, released_by: str, note: str = "") -> dict[str, Any]:
        return self.app.release_hold(order_id=order_id, hold_id=hold_id, released_by=released_by, note=note)

    def request_cancellation(self, *, order_id: str, reason: str, actor: str = "user") -> dict[str, Any]:
        return self.app.request_cancellation(order_id=order_id, reason=reason, actor=actor)

    def create_backorder(self, *, order_id: str, line_id: str, quantity: float, reason: str) -> dict[str, Any]:
        return self.app.create_backorder(order_id=order_id, line_id=line_id, quantity=quantity, reason=reason)

    def apply_substitution(self, *, order_id: str, line_id: str, substitute_item_id: str, reason: str = "equivalent_inventory") -> dict[str, Any]:
        return self.app.apply_substitution(order_id=order_id, line_id=line_id, substitute_item_id=substitute_item_id, reason=reason)

    def record_exception(self, *, order_id: str, exception_type: str, reason: str, severity: str = "medium") -> dict[str, Any]:
        return self.app.record_exception(order_id=order_id, exception_type=exception_type, reason=reason, severity=severity)

    def receive_event(self, event: dict[str, Any]) -> dict[str, Any]:
        return self.app.receive_event(event)

    def confirm_order_shipped(self, order_id: str, *, shipment_id: str) -> dict[str, Any]:
        return self.app.confirm_order_shipped(order_id, shipment_id=shipment_id)

    def document_intake(self, document: str, instructions: str = "") -> dict[str, Any]:
        return self.app.document_intake(document, instructions)

    def crud_mutation_plan(self, *, action_name: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.app.crud_mutation_plan(action_name=action_name, table=table, payload=payload)

    def workbench(self, *, tenant: str | None = None, permissions: tuple[str, ...] | None = None) -> dict[str, Any]:
        return self.app.workbench(tenant=tenant, permissions=permissions)

    def repository_manifest(self) -> dict[str, Any]:
        return self.app.repository_manifest()

    def read_model_snapshot(self) -> dict[str, Any]:
        return self.app.read_model_snapshot()

    def load_demo_workspace(self, seed_bundle: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.app.load_demo_workspace(seed_bundle=seed_bundle)

    def get_order_snapshot(self, order_id: str) -> dict[str, Any]:
        order = self.app.snapshot().get("orders", {}).get(order_id)
        return {"ok": order is not None, "order": order, "state": self.state}


def standalone_service_manifest() -> dict[str, Any]:
    manifest = standalone.standalone_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": "dom",
        "service_class": "DomStandaloneService",
        "service_methods": manifest["service_methods"],
        "query_methods": ("workbench", "repository_manifest", "read_model_snapshot", "get_order_snapshot", "crud_mutation_plan"),
        "event_contract": "AppGen-X",
        "event_topic": DOM_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def service_operation_manifest():
    """Return the executable descriptor surface plus standalone service evidence."""
    service = DomService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith("command_") or name.startswith("query_"))
        and callable(getattr(service, name))
    )
    return {
        "ok": bool(operations) and service_operation_contracts()["ok"],
        "pbc": "dom",
        "service_class": service.__class__.__name__,
        "operations": operations,
        "command_operations": service_operation_contracts()["command_operations"],
        "query_operations": service_operation_contracts()["query_operations"],
        "operation_contracts": service_operation_contracts()["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "standalone_service": standalone_service_manifest(),
        "side_effects": (),
    }


def smoke_test():
    """Exercise the descriptor facade and the standalone service."""
    manifest = service_operation_manifest()
    service = DomService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = getattr(service, operation)({"smoke": True}) if operation else {"ok": False}
    standalone_smoke = standalone.standalone_smoke_test()
    return {
        "ok": manifest["ok"]
        and result.get("ok") is True
        and result.get("operation_contract", {}).get("ok") is True
        and standalone_smoke["ok"],
        "manifest": manifest,
        "result": result,
        "standalone": standalone_smoke,
        "side_effects": (),
    }
