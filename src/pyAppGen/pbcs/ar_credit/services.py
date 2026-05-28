"""Executable service layer for the ar_credit PBC."""

from __future__ import annotations

from .runtime import AR_CREDIT_ALLOWED_DATABASE_BACKENDS
from .runtime import AR_CREDIT_CONSUMED_EVENT_TYPES
from .runtime import AR_CREDIT_EMITTED_EVENT_TYPES
from .runtime import AR_CREDIT_OWNED_TABLES
from .runtime import AR_CREDIT_REQUIRED_EVENT_TOPIC
from .runtime import ar_credit_build_workbench_view
from .runtime import ar_credit_calculate_aging
from .runtime import ar_credit_create_credit_memo
from .runtime import ar_credit_generate_customer_statement
from .runtime import ar_credit_issue_refund
from .runtime import ar_credit_recognize_revenue_schedule
from .runtime import ar_credit_record_delivery_confirmation
from .runtime import ar_credit_record_unapplied_cash
from .runtime import ar_credit_resolve_dispute
from .runtime import ar_credit_schedule_collection_action
from .runtime import ar_credit_submit_e_invoice
from .runtime import ar_credit_write_off_receivable
from .receivables_workflows import AR_CREDIT_WORKFLOW_OPERATIONS
from .receivables_workflows import ar_credit_build_collections_follow_up
from .receivables_workflows import ar_credit_execute_customer_onboarding
from .receivables_workflows import ar_credit_execute_invoice_issuance
from .receivables_workflows import ar_credit_execute_receipt_application
from .receivables_workflows import ar_credit_review_credit_onboarding
from .receivables_workflows import ar_credit_review_invoice_readiness


EVENT_CONTRACT = {
    "contract": "AppGen-X",
    "topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
    "outbox_table": "ar_credit_appgen_outbox_event",
    "inbox_table": "ar_credit_appgen_inbox_event",
    "dead_letter_table": "ar_credit_dead_letter_event",
}


_COMMAND_OPERATION_DEFS = (
    {
        "operation": "command_ar_customers",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/customers",
        "permission": "ar_credit.command.1",
        "owned_tables": (
            "ar_customer",
            "ar_customer_graph",
            "ar_customer_credit_profile",
            "ar_customer_payment_terms",
            "ar_customer_risk_signal",
            "ar_credit_decision",
            EVENT_CONTRACT["outbox_table"],
        ),
        "emitted_event": "CustomerOnboarded",
    },
    {
        "operation": "command_ar_invoices",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/invoices",
        "permission": "ar_credit.command.2",
        "owned_tables": (
            "ar_invoice",
            "ar_invoice_line",
            "ar_invoice_tax",
            "ar_invoice_performance_obligation",
            EVENT_CONTRACT["outbox_table"],
        ),
        "emitted_event": "InvoiceIssued",
    },
    {
        "operation": "command_ar_deliveries",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/deliveries",
        "permission": "ar_credit.command.3",
        "owned_tables": ("ar_delivery_confirmation", EVENT_CONTRACT["outbox_table"]),
        "emitted_event": "DeliveryConfirmed",
    },
    {
        "operation": "command_ar_remittances_parse",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/remittances/parse",
        "permission": "ar_credit.command.4",
        "owned_tables": ("ar_remittance_advice",),
        "emitted_event": None,
    },
    {
        "operation": "command_ar_cash_applications",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/cash-applications",
        "permission": "ar_credit.command.5",
        "owned_tables": (
            "ar_cash_receipt",
            "ar_cash_application",
            "ar_unapplied_cash",
            "ar_cash_pool",
            "ar_invoice",
            EVENT_CONTRACT["outbox_table"],
        ),
        "emitted_event": "PaymentReceived",
    },
    {
        "operation": "command_ar_unapplied_cash",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/unapplied-cash",
        "permission": "ar_credit.command.6",
        "owned_tables": ("ar_unapplied_cash", "ar_cash_pool", EVENT_CONTRACT["outbox_table"]),
        "emitted_event": "UnappliedCashRecorded",
    },
    {
        "operation": "command_ar_credit_memos",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/credit-memos",
        "permission": "ar_credit.command.7",
        "owned_tables": ("ar_credit_memo", "ar_invoice", EVENT_CONTRACT["outbox_table"]),
        "emitted_event": "CreditMemoIssued",
    },
    {
        "operation": "command_ar_write_offs",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/write-offs",
        "permission": "ar_credit.command.8",
        "owned_tables": ("ar_write_off", "ar_invoice", EVENT_CONTRACT["outbox_table"]),
        "emitted_event": "ReceivableWrittenOff",
    },
    {
        "operation": "command_ar_refunds",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/refunds",
        "permission": "ar_credit.command.9",
        "owned_tables": ("ar_refund", EVENT_CONTRACT["outbox_table"]),
        "emitted_event": "CustomerRefundScheduled",
    },
    {
        "operation": "command_ar_disputes",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/disputes",
        "permission": "ar_credit.command.10",
        "owned_tables": ("ar_dispute_case", "ar_credit_memo"),
        "emitted_event": None,
    },
    {
        "operation": "command_ar_collections",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/collections",
        "permission": "ar_credit.command.11",
        "owned_tables": ("ar_collection_action", "ar_dunning_notice", "ar_statement", EVENT_CONTRACT["outbox_table"]),
        "emitted_event": "CollectionActionScheduled",
    },
    {
        "operation": "command_ar_e_invoices",
        "method": "POST",
        "path": "/api/pbc/ar_credit/ar/e-invoices",
        "permission": "ar_credit.command.12",
        "owned_tables": ("ar_e_invoice_submission",),
        "emitted_event": None,
    },
)

_QUERY_OPERATION_DEFS = (
    {
        "operation": "query_ar_aging",
        "method": "GET",
        "path": "/api/pbc/ar_credit/ar/aging",
        "permission": "ar_credit.query.13",
        "read_tables": ("ar_invoice", "ar_credit_memo", "ar_unapplied_cash"),
    },
    {
        "operation": "query_ar_statements_customer_id",
        "method": "GET",
        "path": "/api/pbc/ar_credit/ar/statements/{customer_id}",
        "permission": "ar_credit.query.14",
        "read_tables": ("ar_invoice", "ar_credit_memo", "ar_statement"),
    },
    {
        "operation": "query_ar_revenue_schedules_invoice_id",
        "method": "GET",
        "path": "/api/pbc/ar_credit/ar/revenue-schedules/{invoice_id}",
        "permission": "ar_credit.query.15",
        "read_tables": ("ar_invoice", "ar_revenue_schedule", "ar_revenue_schedule_line"),
    },
    {
        "operation": "query_ar_workbench",
        "method": "GET",
        "path": "/api/pbc/ar_credit/ar/workbench",
        "permission": "ar_credit.query.16",
        "read_tables": AR_CREDIT_OWNED_TABLES,
    },
)

_COMMAND_CONTRACTS = tuple(
    {
        **definition,
        "operation_kind": "command",
        "read_tables": (),
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }
    for definition in _COMMAND_OPERATION_DEFS
)
_QUERY_CONTRACTS = tuple(
    {
        **definition,
        "operation_kind": "query",
        "owned_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }
    for definition in _QUERY_OPERATION_DEFS
)
OPERATION_CONTRACTS = _COMMAND_CONTRACTS + _QUERY_CONTRACTS
_OPERATION_INDEX = {item["operation"]: item for item in OPERATION_CONTRACTS}


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(not item["read_tables"] for item in command_contracts)
        and all(not item["owned_tables"] for item in query_contracts),
        "pbc": "ar_credit",
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "workflow_operations": AR_CREDIT_WORKFLOW_OPERATIONS,
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = _OPERATION_INDEX.get(operation_name)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": True,
        "pbc": "ar_credit",
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


class ArCreditService:
    """Executable facade over the runtime and workflow slice."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        if plan["ok"] is not True:
            return plan
        result = {
            "ok": True,
            "pbc": "ar_credit",
            "operation": operation_name,
            "operation_kind": plan["operation_kind"],
            "payload": dict(payload or {}),
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "event_contract": plan["event_contract"],
            "side_effects": (),
        }
        if plan["operation_kind"] == "command":
            result["read_only"] = False
            result["outbox_table"] = EVENT_CONTRACT["outbox_table"]
            result["emits"] = (plan["emitted_event"],) if plan["emitted_event"] else ()
        else:
            result["read_only"] = True
            result["outbox_table"] = None
            result["emits"] = ()
        return result

    def _command(self, operation_name, payload):
        payload = dict(payload or {})
        result = self._execute(operation_name, payload)
        if result["ok"] is not True:
            return result
        state, record = _extract_state_and_record(payload)
        if operation_name == "command_ar_customers":
            review = ar_credit_review_credit_onboarding(record)
            result["review"] = review
            if state is not None and record:
                execution = ar_credit_execute_customer_onboarding(state, record)
                result.update(
                    {
                        "ok": execution["ok"],
                        "state": execution.get("state"),
                        "customer": execution.get("customer"),
                        "review": execution.get("review", review),
                        "blockers": execution.get("blockers", review.get("blockers", ())),
                    }
                )
            else:
                result["ok"] = review["ok"]
            return result
        if operation_name == "command_ar_invoices":
            readiness = ar_credit_review_invoice_readiness(state or {}, record)
            result["readiness"] = readiness
            if state is not None and record:
                execution = ar_credit_execute_invoice_issuance(state, record)
                result.update(
                    {
                        "ok": execution["ok"],
                        "state": execution.get("state"),
                        "invoice": execution.get("invoice"),
                        "readiness": execution.get("readiness", readiness),
                        "blockers": execution.get("blockers", readiness.get("blockers", ())),
                    }
                )
            else:
                result["ok"] = readiness["ok"]
            return result
        if operation_name == "command_ar_cash_applications" and state is not None and record:
            execution = ar_credit_execute_receipt_application(state, record)
            result.update(execution)
            return result
        if operation_name == "command_ar_unapplied_cash" and state is not None and record:
            execution = ar_credit_record_unapplied_cash(state, record)
            result.update(execution)
            return result
        if operation_name == "command_ar_deliveries" and state is not None and record:
            execution = ar_credit_record_delivery_confirmation(state, record)
            result.update(execution)
            return result
        if operation_name == "command_ar_credit_memos" and state is not None and record:
            execution = ar_credit_create_credit_memo(state, record)
            result.update(execution)
            return result
        if operation_name == "command_ar_write_offs" and state is not None and record:
            execution = ar_credit_write_off_receivable(state, record)
            result.update(execution)
            return result
        if operation_name == "command_ar_refunds" and state is not None and record:
            execution = ar_credit_issue_refund(state, record)
            result.update(execution)
            return result
        if operation_name == "command_ar_disputes" and record:
            dispute = record.get("dispute") or record
            result["dispute"] = ar_credit_resolve_dispute(state or {}, dispute)
            result["ok"] = result["dispute"]["ok"]
            return result
        if operation_name == "command_ar_collections" and state is not None and record:
            if record.get("customer_id") and record.get("as_of"):
                result["follow_up"] = ar_credit_build_collections_follow_up(
                    state,
                    customer_id=record["customer_id"],
                    as_of=record["as_of"],
                )
                result["ok"] = result["follow_up"]["ok"]
                return result
            execution = ar_credit_schedule_collection_action(state, record)
            result.update(execution)
            return result
        if operation_name == "command_ar_e_invoices" and state is not None and record:
            invoice_id = record.get("invoice_id")
            jurisdiction = record.get("jurisdiction", "UNSPECIFIED")
            execution = ar_credit_submit_e_invoice(state, invoice_id, jurisdiction=jurisdiction)
            result.update(execution)
            return result
        return result

    def _query(self, operation_name, payload):
        payload = dict(payload or {})
        result = self._execute(operation_name, payload)
        if result["ok"] is not True:
            return result
        state = payload.get("state")
        if state is None:
            return result
        if operation_name == "query_ar_aging":
            result["aging"] = ar_credit_calculate_aging(
                state,
                tenant=payload["tenant"],
                as_of=payload["as_of"],
            )
            result["ok"] = result["aging"]["ok"]
            return result
        if operation_name == "query_ar_statements_customer_id":
            result["statement"] = ar_credit_generate_customer_statement(
                state,
                customer_id=payload["customer_id"],
                as_of=payload["as_of"],
            )
            result["ok"] = result["statement"]["ok"]
            return result
        if operation_name == "query_ar_revenue_schedules_invoice_id":
            invoice_id = payload["invoice_id"]
            schedule = next(
                (
                    value
                    for value in state.get("revenue_schedules", {}).values()
                    if value.get("invoice_id") == invoice_id
                ),
                None,
            )
            if schedule is None and payload.get("build_if_missing"):
                recognized = ar_credit_recognize_revenue_schedule(state, invoice_id)
                result["state"] = recognized["state"]
                schedule = recognized["schedule"]
            result["ok"] = schedule is not None
            result["schedule"] = schedule
            return result
        if operation_name == "query_ar_workbench":
            workbench = ar_credit_build_workbench_view(
                state,
                tenant=payload["tenant"],
                as_of=payload["as_of"],
            )
            follow_up = None
            if payload.get("customer_id"):
                follow_up = ar_credit_build_collections_follow_up(
                    state,
                    customer_id=payload["customer_id"],
                    as_of=payload["as_of"],
                )
            result["workbench"] = workbench
            result["follow_up"] = follow_up
            result["ok"] = workbench["ok"] and (follow_up is None or follow_up["ok"])
            return result
        return result

    def review_credit_onboarding(self, payload=None):
        return ar_credit_review_credit_onboarding(_extract_record_only(payload))

    def execute_customer_onboarding(self, payload=None):
        payload = dict(payload or {})
        state, record = _extract_state_and_record(payload)
        if state is None:
            return {"ok": False, "reason": "missing_state", "side_effects": ()}
        return ar_credit_execute_customer_onboarding(state, record)

    def review_invoice_readiness(self, payload=None):
        payload = dict(payload or {})
        return ar_credit_review_invoice_readiness(payload.get("state") or {}, _extract_record_only(payload))

    def execute_invoice_issuance(self, payload=None):
        payload = dict(payload or {})
        state, record = _extract_state_and_record(payload)
        if state is None:
            return {"ok": False, "reason": "missing_state", "side_effects": ()}
        return ar_credit_execute_invoice_issuance(state, record)

    def execute_receipt_application(self, payload=None):
        payload = dict(payload or {})
        state, record = _extract_state_and_record(payload)
        if state is None:
            return {"ok": False, "reason": "missing_state", "side_effects": ()}
        return ar_credit_execute_receipt_application(state, record)

    def build_collections_follow_up(self, payload=None):
        payload = dict(payload or {})
        state = payload.get("state")
        if state is None:
            return {"ok": False, "reason": "missing_state", "side_effects": ()}
        return ar_credit_build_collections_follow_up(
            state,
            customer_id=payload["customer_id"],
            as_of=payload["as_of"],
        )

    def command_ar_customers(self, payload=None):
        return self._command("command_ar_customers", payload or {})

    def command_ar_invoices(self, payload=None):
        return self._command("command_ar_invoices", payload or {})

    def command_ar_deliveries(self, payload=None):
        return self._command("command_ar_deliveries", payload or {})

    def command_ar_remittances_parse(self, payload=None):
        return self._command("command_ar_remittances_parse", payload or {})

    def command_ar_cash_applications(self, payload=None):
        return self._command("command_ar_cash_applications", payload or {})

    def command_ar_unapplied_cash(self, payload=None):
        return self._command("command_ar_unapplied_cash", payload or {})

    def command_ar_credit_memos(self, payload=None):
        return self._command("command_ar_credit_memos", payload or {})

    def command_ar_write_offs(self, payload=None):
        return self._command("command_ar_write_offs", payload or {})

    def command_ar_refunds(self, payload=None):
        return self._command("command_ar_refunds", payload or {})

    def command_ar_disputes(self, payload=None):
        return self._command("command_ar_disputes", payload or {})

    def command_ar_collections(self, payload=None):
        return self._command("command_ar_collections", payload or {})

    def command_ar_e_invoices(self, payload=None):
        return self._command("command_ar_e_invoices", payload or {})

    def query_ar_aging(self, payload=None):
        return self._query("query_ar_aging", payload or {})

    def query_ar_statements_customer_id(self, payload=None):
        return self._query("query_ar_statements_customer_id", payload or {})

    def query_ar_revenue_schedules_invoice_id(self, payload=None):
        return self._query("query_ar_revenue_schedules_invoice_id", payload or {})

    def query_ar_workbench(self, payload=None):
        return self._query("query_ar_workbench", payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": "ar_credit",
        "service_class": "ArCreditService",
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "workflow_operations": contracts["workflow_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": EVENT_CONTRACT,
        "database_backends": AR_CREDIT_ALLOWED_DATABASE_BACKENDS,
        "emits": AR_CREDIT_EMITTED_EVENT_TYPES,
        "consumes": AR_CREDIT_CONSUMED_EVENT_TYPES,
        "owned_tables": AR_CREDIT_OWNED_TABLES,
        "side_effects": (),
    }


def smoke_test():
    """Execute the core workflow-enabled service operations without side effects."""
    service = ArCreditService()
    customer_preview = service.command_ar_customers(
        {
            "customer_id": "smoke_customer",
            "tenant": "smoke",
            "name": "Smoke Customer",
            "terms": {"net_days": 30},
            "risk_signals": {"payment_latency": 0.05},
            "identity": {"did": "did:appgen:smoke_customer", "issuer": "trusted_registry", "status": "active"},
            "requested_limit": 1000,
        }
    )
    query = service.query_ar_workbench({})
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"]
        and customer_preview["ok"] is True
        and customer_preview["review"]["event_contract"] == "AppGen-X"
        and query["ok"] is True,
        "result": customer_preview,
        "customer_preview": customer_preview,
        "query": query,
        "contracts": contracts,
        "side_effects": (),
    }


def _extract_state_and_record(payload: dict) -> tuple[dict | None, dict]:
    state = payload.get("state")
    if "customer" in payload:
        return state, dict(payload["customer"] or {})
    if "invoice" in payload:
        return state, dict(payload["invoice"] or {})
    if "receipt" in payload:
        return state, dict(payload["receipt"] or {})
    if "action" in payload:
        return state, dict(payload["action"] or {})
    if "refund" in payload:
        return state, dict(payload["refund"] or {})
    if "memo" in payload:
        return state, dict(payload["memo"] or {})
    if "write_off" in payload:
        return state, dict(payload["write_off"] or {})
    if "dispute" in payload:
        return state, dict(payload["dispute"] or {})
    return state, {key: value for key, value in payload.items() if key != "state"}


def _extract_record_only(payload) -> dict:
    return _extract_state_and_record(dict(payload or {}))[1]
