"""Executable service layer for the bank_payments_clearing PBC."""

from __future__ import annotations

from copy import deepcopy

from . import runtime, ui
from .events import EVENT_CONTRACT
from .payment_operations import (
    assemble_clearing_batch,
    build_payment_operations_workbench,
    create_payment_instruction,
    empty_operations_state,
    generate_settlement_file,
    handle_settlement_acknowledgement,
    process_return_item,
    reconcile_bank_statement,
    register_participant_bank,
    release_payment_instruction,
)


PBC_KEY = "bank_payments_clearing"
OWNED_TABLES = runtime.BANK_PAYMENTS_CLEARING_OWNED_TABLES
_COMMAND_OPERATION_SPECS = (
    {
        "operation": "configure_runtime",
        "method": "POST",
        "path": "/runtime/configuration",
        "permission": "bank_payments_clearing.admin",
        "owned_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "set_parameter",
        "method": "POST",
        "path": "/runtime/parameters",
        "permission": "bank_payments_clearing.admin",
        "owned_tables": ("bank_payments_clearing_bank_payments_clearing_runtime_parameter",),
        "emitted_event": None,
    },
    {
        "operation": "register_rule",
        "method": "POST",
        "path": "/runtime/rules",
        "permission": "bank_payments_clearing.admin",
        "owned_tables": ("bank_payments_clearing_bank_payments_clearing_policy_rule",),
        "emitted_event": None,
    },
    {
        "operation": "receive_event",
        "method": "POST",
        "path": "/events/inbox",
        "permission": "bank_payments_clearing.admin",
        "owned_tables": (
            "bank_payments_clearing_appgen_inbox_event",
            "bank_payments_clearing_appgen_dead_letter_event",
        ),
        "emitted_event": None,
    },
    {
        "operation": "register_participant_bank",
        "method": "POST",
        "path": "/participant-banks",
        "permission": "bank_payments_clearing.create",
        "owned_tables": (
            "bank_payments_clearing_participant_bank",
            "bank_payments_clearing_appgen_outbox_event",
        ),
        "emitted_event": "BankPaymentsClearingCreated",
    },
    {
        "operation": "create_validated_payment_instruction",
        "method": "POST",
        "path": "/payment-instructions",
        "permission": "bank_payments_clearing.create",
        "owned_tables": (
            "bank_payments_clearing_payment_instruction",
            "bank_payments_clearing_exception_case",
            "bank_payments_clearing_appgen_outbox_event",
        ),
        "emitted_event": "BankPaymentsClearingCreated",
    },
    {
        "operation": "release_payment_instruction",
        "method": "POST",
        "path": "/payment-instructions/release",
        "permission": "bank_payments_clearing.approve",
        "owned_tables": (
            "bank_payments_clearing_payment_instruction",
            "bank_payments_clearing_exception_case",
            "bank_payments_clearing_appgen_outbox_event",
        ),
        "emitted_event": "BankPaymentsClearingApproved",
    },
    {
        "operation": "assemble_clearing_batch",
        "method": "POST",
        "path": "/clearing-batches",
        "permission": "bank_payments_clearing.update",
        "owned_tables": (
            "bank_payments_clearing_clearing_batch",
            "bank_payments_clearing_payment_instruction",
            "bank_payments_clearing_appgen_outbox_event",
        ),
        "emitted_event": "BankPaymentsClearingUpdated",
    },
    {
        "operation": "generate_settlement_file",
        "method": "POST",
        "path": "/settlement-files",
        "permission": "bank_payments_clearing.update",
        "owned_tables": (
            "bank_payments_clearing_settlement_file",
            "bank_payments_clearing_appgen_outbox_event",
        ),
        "emitted_event": "BankPaymentsClearingUpdated",
    },
    {
        "operation": "handle_settlement_acknowledgement",
        "method": "POST",
        "path": "/settlement-acknowledgements",
        "permission": "bank_payments_clearing.update",
        "owned_tables": (
            "bank_payments_clearing_settlement_file",
            "bank_payments_clearing_exception_case",
        ),
        "emitted_event": "BankPaymentsClearingUpdated",
    },
    {
        "operation": "process_return_item",
        "method": "POST",
        "path": "/return-items",
        "permission": "bank_payments_clearing.update",
        "owned_tables": (
            "bank_payments_clearing_return_item",
            "bank_payments_clearing_payment_instruction",
            "bank_payments_clearing_appgen_outbox_event",
        ),
        "emitted_event": "BankPaymentsClearingExceptionOpened",
    },
    {
        "operation": "reconcile_bank_statement",
        "method": "POST",
        "path": "/reconciliations",
        "permission": "bank_payments_clearing.update",
        "owned_tables": (
            "bank_payments_clearing_bank_reconciliation",
            "bank_payments_clearing_payment_instruction",
        ),
        "emitted_event": "BankPaymentsClearingUpdated",
    },
)
_QUERY_OPERATION_SPECS = (
    {
        "operation": "query_workbench",
        "method": "GET",
        "path": "/bank-payments-clearing-workbench",
        "permission": "bank_payments_clearing.read",
        "read_tables": OWNED_TABLES,
    },
    {
        "operation": "build_workbench_view",
        "method": "GET",
        "path": "/bank-payments-clearing-workbench/view",
        "permission": "bank_payments_clearing.read",
        "read_tables": OWNED_TABLES,
    },
    {
        "operation": "release_snapshot",
        "method": "GET",
        "path": "/bank-payments-clearing-release-evidence",
        "permission": "bank_payments_clearing.read",
        "read_tables": (),
    },
)


def service_empty_state() -> dict:
    return {
        "runtime": runtime.bank_payments_clearing_empty_state(),
        "operations": empty_operations_state(),
    }


def _copy_state(state: dict) -> dict:
    return deepcopy(state)


def _operation_contract(spec: dict, operation_kind: str) -> dict:
    read_tables = tuple(spec.get("read_tables", ()))
    owned_tables = tuple(spec.get("owned_tables", ()))
    return {
        "operation": spec["operation"],
        "operation_kind": operation_kind,
        "method": spec["method"],
        "path": spec["path"],
        "permission": spec["permission"],
        "owned_tables": owned_tables,
        "read_tables": read_tables,
        "emitted_event": spec.get("emitted_event"),
        "event_contract": "AppGen-X",
        "transaction_boundary": "owned_datastore_plus_outbox" if operation_kind == "command" else "read_only_projection",
        "idempotency_key": f"{PBC_KEY}:{spec['method']}:{spec['path']}",
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


def _wrap_result(service: "BankPaymentsClearingService", spec: dict, operation_kind: str, result: dict) -> dict:
    contract = _operation_contract(spec, operation_kind)
    return {
        "ok": result.get("ok") is True,
        "operation": spec["operation"],
        "operation_kind": operation_kind,
        "payload": result.get("payload", {}),
        "result": result,
        "operation_contract": contract,
        "state": service.snapshot(),
        "outbox_table": EVENT_CONTRACT["outbox_table"] if operation_kind == "command" else None,
        "emits": (contract["emitted_event"],) if contract["emitted_event"] else (),
        "transaction_boundary": contract["transaction_boundary"],
        "side_effects": (),
    }


class BankPaymentsClearingService:
    """Side-effect-free in-memory service for the standalone PBC slice."""

    def __init__(self, state: dict | None = None):
        self._state = _copy_state(state or service_empty_state())

    def snapshot(self) -> dict:
        return _copy_state(self._state)

    def configure_runtime(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[0]
        configuration = dict((payload or {}).get("configuration", payload or {}))
        result = runtime.bank_payments_clearing_configure_runtime(self._state["runtime"], configuration)
        self._state["runtime"] = result["state"]
        result["payload"] = configuration
        return _wrap_result(self, spec, "command", result)

    def set_parameter(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[1]
        payload = dict(payload or {})
        result = runtime.bank_payments_clearing_set_parameter(
            self._state["runtime"],
            payload["name"],
            payload["value"],
        )
        self._state["runtime"] = result["state"]
        result["payload"] = payload
        return _wrap_result(self, spec, "command", result)

    def register_rule(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[2]
        payload = dict(payload or {})
        result = runtime.bank_payments_clearing_register_rule(self._state["runtime"], payload)
        self._state["runtime"] = result["state"]
        result["payload"] = payload
        return _wrap_result(self, spec, "command", result)

    def receive_event(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[3]
        payload = dict(payload or {})
        result = runtime.bank_payments_clearing_receive_event(self._state["runtime"], payload)
        self._state["runtime"] = result["state"]
        result["payload"] = payload
        return _wrap_result(self, spec, "command", result)

    def register_participant_bank(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[4]
        profile = dict((payload or {}).get("participant_bank", payload or {}))
        result = register_participant_bank(self._state["operations"], profile)
        self._state["operations"] = result["state"]
        result["payload"] = profile
        return _wrap_result(self, spec, "command", result)

    def create_validated_payment_instruction(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[5]
        instruction = dict((payload or {}).get("instruction", payload or {}))
        result = create_payment_instruction(self._state["operations"], instruction)
        self._state["operations"] = result["state"]
        result["payload"] = instruction
        return _wrap_result(self, spec, "command", result)

    def release_payment_instruction(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[6]
        payload = dict(payload or {})
        result = release_payment_instruction(
            self._state["operations"],
            payload["instruction_id"],
            maker=payload["maker"],
            checker=payload["checker"],
            liquidity=dict(payload.get("liquidity", {})),
        )
        self._state["operations"] = result["state"]
        result["payload"] = payload
        return _wrap_result(self, spec, "command", result)

    def assemble_clearing_batch(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[7]
        payload = dict(payload or {})
        result = assemble_clearing_batch(
            self._state["operations"],
            payload["batch_id"],
            rail=payload["rail"],
            participant_bank_id=payload["participant_bank_id"],
            cutoff_context=dict(payload.get("cutoff_context", {})),
        )
        self._state["operations"] = result["state"]
        result["payload"] = payload
        return _wrap_result(self, spec, "command", result)

    def generate_settlement_file(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[8]
        payload = dict(payload or {})
        result = generate_settlement_file(
            self._state["operations"],
            payload["file_id"],
            payload["batch_id"],
            sequence=payload["sequence"],
            channel=payload["channel"],
        )
        self._state["operations"] = result["state"]
        result["payload"] = payload
        return _wrap_result(self, spec, "command", result)

    def handle_settlement_acknowledgement(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[9]
        acknowledgement = dict((payload or {}).get("acknowledgement", payload or {}))
        result = handle_settlement_acknowledgement(self._state["operations"], acknowledgement)
        self._state["operations"] = result["state"]
        result["payload"] = acknowledgement
        return _wrap_result(self, spec, "command", result)

    def process_return_item(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[10]
        return_item = dict((payload or {}).get("return_item", payload or {}))
        result = process_return_item(self._state["operations"], return_item)
        self._state["operations"] = result["state"]
        result["payload"] = return_item
        return _wrap_result(self, spec, "command", result)

    def reconcile_bank_statement(self, payload: dict | None = None) -> dict:
        spec = _COMMAND_OPERATION_SPECS[11]
        payload = dict(payload or {})
        result = reconcile_bank_statement(
            self._state["operations"],
            payload["reconciliation_id"],
            tuple(payload.get("statement_lines", ())),
        )
        self._state["operations"] = result["state"]
        result["payload"] = payload
        return _wrap_result(self, spec, "command", result)

    def query_workbench(self, payload: dict | None = None) -> dict:
        spec = _QUERY_OPERATION_SPECS[0]
        filters = dict(payload or {})
        result = build_payment_operations_workbench(self._state["operations"])
        result["filters"] = filters
        result["payload"] = filters
        return _wrap_result(self, spec, "query", result)

    def build_workbench_view(self, payload: dict | None = None) -> dict:
        spec = _QUERY_OPERATION_SPECS[1]
        filters = dict(payload or {})
        result = ui.bank_payments_clearing_render_workbench(self._state["operations"])
        result["filters"] = filters
        result["payload"] = filters
        return _wrap_result(self, spec, "query", result)

    def release_snapshot(self, payload: dict | None = None) -> dict:
        from .release_evidence import build_release_evidence

        spec = _QUERY_OPERATION_SPECS[2]
        snapshot = build_release_evidence()
        snapshot["payload"] = dict(payload or {})
        return _wrap_result(self, spec, "query", snapshot)


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "BankPaymentsClearingService",
        "command_operations": tuple(spec["operation"] for spec in _COMMAND_OPERATION_SPECS),
        "payment_operations": tuple(spec["operation"] for spec in _COMMAND_OPERATION_SPECS[4:]),
        "query_operations": tuple(spec["operation"] for spec in _QUERY_OPERATION_SPECS),
        "workflow_operations": (
            "instruction_intake_to_release",
            "batch_settlement_to_acknowledgement",
            "return_to_reconciliation",
            "assistant_document_to_crud_preview",
        ),
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(
        _operation_contract(spec, "command") for spec in _COMMAND_OPERATION_SPECS
    ) + tuple(_operation_contract(spec, "query") for spec in _QUERY_OPERATION_SPECS)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    index = {item["operation"]: item for item in service_operation_contracts()["contracts"]}
    contract = index.get(operation)
    return {
        "ok": contract is not None,
        "operation": operation,
        "operation_kind": contract["operation_kind"] if contract else None,
        "payload": dict(payload or {}),
        "contract": contract,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = BankPaymentsClearingService()
    configure = service.configure_runtime(
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": runtime.BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 5,
                "default_policy": "balanced",
            }
        }
    )
    participant = service.register_participant_bank(
        {
            "participant_bank": {
                "participant_bank_id": "bank_service_smoke",
                "routing_identifier": "021000021",
                "supported_rails": ("ach", "wire"),
                "status": "active",
            }
        }
    )
    instruction = service.create_validated_payment_instruction(
        {
            "instruction": {
                "instruction_id": "pay_service_smoke",
                "tenant": "tenant_smoke",
                "rail": "ach",
                "participant_bank_id": "bank_service_smoke",
                "amount": 120.0,
                "currency": "USD",
                "beneficiary_account": "123456789",
                "beneficiary_name": "Smoke Supplier",
                "originator_authorized": True,
                "external_reference": "SMOKE-001",
                "screening_evidence": {"decision": "clear", "freshness": "current"},
            }
        }
    )
    workbench = service.build_workbench_view({"tenant": "tenant_smoke"})
    return {
        "ok": configure["ok"] and participant["ok"] and instruction["ok"] and workbench["ok"],
        "configure": configure,
        "participant": participant,
        "instruction": instruction,
        "workbench": workbench,
        "side_effects": (),
    }
