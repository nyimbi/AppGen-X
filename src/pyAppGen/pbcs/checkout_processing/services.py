"""Command and query service layer for the checkout_processing PBC."""

from __future__ import annotations

from .agent import checkout_processing_assistant_preview
from .controls import checkout_processing_control_center
from .events import EVENT_CONTRACT
from .forms import checkout_processing_form_catalog
from .wizards import checkout_processing_wizard_catalog


OPERATION_CONTRACTS = (
    {
        "operation": "command_carts",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/checkout_processing/carts",
        "permission": "checkout_processing.cart",
        "owned_tables": ("checkout_processing_cart", "checkout_processing_cart_line"),
        "read_tables": (),
        "emitted_event": "OrderPriced",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_checkout",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/checkout_processing/checkout",
        "permission": "checkout_processing.checkout",
        "owned_tables": (
            "checkout_processing_checkout_session",
            "checkout_processing_checkout_pricing_handoff",
            "checkout_processing_checkout_tax_handoff",
            "checkout_processing_checkout_address_validation",
        ),
        "read_tables": (),
        "emitted_event": "CheckoutCompleted",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_inventory_confirmations",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/checkout_processing/inventory-confirmations",
        "permission": "checkout_processing.inventory",
        "owned_tables": ("checkout_processing_checkout_inventory_reservation_handoff", "checkout_processing_checkout_session"),
        "read_tables": (),
        "emitted_event": "OrderPriced",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_payment_authorizations",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/checkout_processing/payment-authorizations",
        "permission": "checkout_processing.payment",
        "owned_tables": ("checkout_processing_checkout_payment_intent_handoff", "checkout_processing_checkout_session"),
        "read_tables": (),
        "emitted_event": "OrderPriced",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_payment_captures",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/checkout_processing/payment-captures",
        "permission": "checkout_processing.payment",
        "owned_tables": ("checkout_processing_checkout_payment_intent_handoff", "checkout_processing_checkout_session"),
        "read_tables": (),
        "emitted_event": "CheckoutCompleted",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_coupons",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/checkout_processing/coupons",
        "permission": "checkout_processing.promotion",
        "owned_tables": ("checkout_processing_cart", "checkout_processing_promotion_redemption"),
        "read_tables": (),
        "emitted_event": "OrderPriced",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_checkout_processing_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/checkout_processing/checkout-processing-workbench",
        "permission": "checkout_processing.audit",
        "owned_tables": (),
        "read_tables": (
            "checkout_processing_cart",
            "checkout_processing_cart_line",
            "checkout_processing_checkout_session",
            "checkout_processing_promotion_redemption",
            "checkout_processing_appgen_inbox_event",
            "checkout_processing_appgen_outbox_event",
        ),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_checkout_processing_controls",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/checkout_processing/controls",
        "permission": "checkout_processing.audit",
        "owned_tables": (),
        "read_tables": (
            "checkout_processing_checkout_session",
            "checkout_processing_checkout_rule",
            "checkout_processing_checkout_parameter",
            "checkout_processing_checkout_configuration",
            "checkout_processing_dead_letter_event",
        ),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_checkout_processing_assistant_preview",
        "operation_kind": "query",
        "method": "POST",
        "path": "/api/pbc/checkout_processing/assistant/document-preview",
        "permission": "checkout_processing.audit",
        "owned_tables": (),
        "read_tables": (
            "checkout_processing_checkout_rule",
            "checkout_processing_checkout_parameter",
            "checkout_processing_checkout_configuration",
            "checkout_processing_checkout_session",
        ),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
)


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item["operation"] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["emitted_event"] for item in command_contracts)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["emitted_event"] is None for item in query_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": "checkout_processing",
        "operations": operations,
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    table_scope = contract["owned_tables"] or contract["read_tables"]
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": "checkout_processing",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
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


class CheckoutProcessingService:
    """Side-effect-free package-local service facade."""

    def _execute(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": "checkout_processing",
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
        else:
            result.update(
                {
                    "query": operation_name,
                    "read_only": True,
                    "outbox_table": None,
                    "emits": (),
                }
            )
        return result

    def command_carts(self, payload: dict | None = None) -> dict:
        return self._execute("command_carts", payload or {})

    def command_checkout(self, payload: dict | None = None) -> dict:
        return self._execute("command_checkout", payload or {})

    def command_inventory_confirmations(self, payload: dict | None = None) -> dict:
        return self._execute("command_inventory_confirmations", payload or {})

    def command_payment_authorizations(self, payload: dict | None = None) -> dict:
        return self._execute("command_payment_authorizations", payload or {})

    def command_payment_captures(self, payload: dict | None = None) -> dict:
        return self._execute("command_payment_captures", payload or {})

    def command_coupons(self, payload: dict | None = None) -> dict:
        return self._execute("command_coupons", payload or {})

    def query_checkout_processing_workbench(self, payload: dict | None = None) -> dict:
        base = self._execute("query_checkout_processing_workbench", payload or {})
        return {
            **base,
            "app_surface": {
                "form_count": len(checkout_processing_form_catalog()["forms"]),
                "wizard_count": len(checkout_processing_wizard_catalog()["wizards"]),
            },
        }

    def query_checkout_processing_controls(self, payload: dict | None = None) -> dict:
        base = self._execute("query_checkout_processing_controls", payload or {})
        control_center = checkout_processing_control_center()
        return {
            **base,
            "control_center": {
                "ok": control_center["ok"],
                "completion_gate": control_center["completion_gate"],
                "assistant_guardrails": control_center["assistant_guardrails"],
            },
        }

    def query_checkout_processing_assistant_preview(self, payload: dict | None = None) -> dict:
        base = self._execute("query_checkout_processing_assistant_preview", payload or {})
        preview = checkout_processing_assistant_preview(payload or {})
        return {
            **base,
            "preview": preview,
        }


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    service = CheckoutProcessingService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith("command_") or name.startswith("query_"))
        and callable(getattr(service, name))
    )
    return {
        "ok": bool(operations) and service_operation_contracts()["ok"],
        "pbc": "checkout_processing",
        "service_class": service.__class__.__name__,
        "operations": operations,
        "command_operations": service_operation_contracts()["command_operations"],
        "query_operations": service_operation_contracts()["query_operations"],
        "operation_contracts": service_operation_contracts()["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = CheckoutProcessingService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = getattr(service, operation)({"smoke": True}) if operation else {"ok": False}
    return {
        "ok": manifest["ok"]
        and result.get("ok") is True
        and result.get("operation_contract", {}).get("ok") is True,
        "manifest": manifest,
        "result": result,
        "side_effects": (),
    }



# Standalone one-PBC application service surface. These operations delegate to the
# package-local repository and produce durable forms, workflow runs, controls, read
# models, and agent sessions for a checkout-only composed app.
STANDALONE_OPERATION_CONTRACTS = (
    {
        "operation": "seed_demo_workspace",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/checkout-processing/demo-workspace",
        "permission": "checkout_processing.configure",
        "owned_tables": (
            "checkout_processing_runtime_state",
            "checkout_processing_form_submission",
            "checkout_processing_workflow_run",
            "checkout_processing_control_execution",
            "checkout_processing_agent_session",
            "checkout_processing_workbench_read_model",
        ),
        "read_tables": (),
        "emitted_event": "CheckoutCompleted",
    },
    {
        "operation": "build_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/checkout-processing/workbench",
        "permission": "checkout_processing.audit",
        "owned_tables": (),
        "read_tables": ("checkout_processing_workbench_read_model",),
        "emitted_event": None,
    },
    {
        "operation": "create_cart",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/checkout-processing/carts",
        "permission": "checkout_processing.cart",
        "owned_tables": ("checkout_processing_runtime_state", "checkout_processing_form_submission"),
        "read_tables": (),
        "emitted_event": "CartCreated",
    },
    {
        "operation": "open_checkout_session",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/checkout-processing/sessions",
        "permission": "checkout_processing.checkout",
        "owned_tables": ("checkout_processing_runtime_state", "checkout_processing_workflow_run"),
        "read_tables": (),
        "emitted_event": "CheckoutStarted",
    },
    {
        "operation": "complete_checkout",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/checkout-processing/checkouts/complete",
        "permission": "checkout_processing.checkout",
        "owned_tables": ("checkout_processing_runtime_state", "checkout_processing_workflow_run"),
        "read_tables": (),
        "emitted_event": "CheckoutCompleted",
    },
    {
        "operation": "generate_checkout_proof",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/checkout-processing/proofs",
        "permission": "checkout_processing.audit",
        "owned_tables": ("checkout_processing_control_execution",),
        "read_tables": (),
        "emitted_event": "CheckoutProofGenerated",
    },
    {
        "operation": "run_agent_skill",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/checkout-processing/assistant/sessions",
        "permission": "checkout_processing.audit",
        "owned_tables": ("checkout_processing_agent_session",),
        "read_tables": (),
        "emitted_event": "CheckoutAssistantSessionRecorded",
    },
)


def standalone_service_operation_contracts() -> dict:
    commands = tuple(item for item in STANDALONE_OPERATION_CONTRACTS if item["operation_kind"] == "command")
    queries = tuple(item for item in STANDALONE_OPERATION_CONTRACTS if item["operation_kind"] == "query")
    all_tables = tuple(table for item in STANDALONE_OPERATION_CONTRACTS for table in item["owned_tables"] + item["read_tables"])
    return {
        "format": "appgen.checkout-processing-standalone-services.v1",
        "ok": bool(STANDALONE_OPERATION_CONTRACTS)
        and all(table.startswith("checkout_processing_") for table in all_tables)
        and all(item["emitted_event"] for item in commands)
        and all(item["emitted_event"] is None for item in queries),
        "pbc": "checkout_processing",
        "service_class": "CheckoutProcessingStandaloneService",
        "operations": tuple(item["operation"] for item in STANDALONE_OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in commands),
        "query_operations": tuple(item["operation"] for item in queries),
        "contracts": STANDALONE_OPERATION_CONTRACTS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


class CheckoutProcessingStandaloneService:
    """Stateful service facade for a standalone checkout application."""

    def __init__(self, repository=None, *, database_path=":memory:"):
        if repository is None:
            from .repository import CheckoutProcessingStandaloneRepository

            repository = CheckoutProcessingStandaloneRepository(database_path=database_path)
        self.repository = repository

    def close(self):
        close = getattr(self.repository, "close", None)
        if callable(close):
            close()

    def seed_demo_workspace(self, tenant="tenant_demo") -> dict:
        return self.repository.seed_demo_workspace(tenant=tenant)

    def build_workbench(self, tenant="tenant_demo") -> dict:
        return self.repository.build_workbench(tenant)

    def create_cart(self, payload: dict | None = None, *, tenant="tenant_demo") -> dict:
        supplied = dict(payload or {})
        return self.repository.create_cart(supplied.get("tenant", tenant), supplied)

    def open_checkout_session(self, payload: dict | None = None, *, tenant="tenant_demo") -> dict:
        supplied = dict(payload or {})
        return self.repository.open_checkout_session(supplied.get("tenant", tenant), supplied)

    def complete_checkout(self, session_id: str, *, tenant="tenant_demo") -> dict:
        return self.repository.complete_checkout(tenant, session_id)

    def generate_checkout_proof(self, session_id: str, disclosure=("session_id", "order_id", "status"), *, tenant="tenant_demo") -> dict:
        return self.repository.generate_checkout_proof(tenant, session_id, tuple(disclosure))

    def run_agent_skill(self, payload: dict | None = None, *, skill="checkout_processing.document_instruction_intake", tenant="tenant_demo") -> dict:
        supplied = dict(payload or {})
        return self.repository.run_agent_skill(supplied.get("tenant", tenant), supplied.get("skill", skill), supplied)
