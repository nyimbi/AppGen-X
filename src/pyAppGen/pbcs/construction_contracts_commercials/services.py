"""Service layer for the construction_contracts_commercials PBC."""
from __future__ import annotations

from .core import (
    EVENT_CONTRACT,
    PBC_KEY,
    SERVICE_COMMAND_OPERATIONS as COMMAND_OPERATIONS,
    SERVICE_QUERY_OPERATIONS as QUERY_OPERATIONS,
    _operation_contract,
    construction_contracts_commercials_approve_variation_order,
    construction_contracts_commercials_assess_notice_timeliness,
    construction_contracts_commercials_build_final_account_packet,
    construction_contracts_commercials_build_payment_certificate,
    construction_contracts_commercials_build_workbench_view,
    construction_contracts_commercials_certify_pay_application,
    construction_contracts_commercials_command_construction_contract,
    construction_contracts_commercials_configure_runtime,
    construction_contracts_commercials_create_lien_waiver,
    construction_contracts_commercials_empty_state,
    construction_contracts_commercials_generate_cash_flow_forecast,
    construction_contracts_commercials_generate_contractor_scorecard,
    construction_contracts_commercials_progress_contract_lifecycle,
    construction_contracts_commercials_query_workbench,
    construction_contracts_commercials_receive_event,
    construction_contracts_commercials_record_pay_application,
    construction_contracts_commercials_record_subcontract_package,
    construction_contracts_commercials_register_commercial_claim,
    construction_contracts_commercials_register_rule,
    construction_contracts_commercials_register_schema_extension,
    construction_contracts_commercials_release_retainage,
    construction_contracts_commercials_replay_dead_letter_event,
    construction_contracts_commercials_review_retainage,
    construction_contracts_commercials_run_change_impact_simulation,
    construction_contracts_commercials_set_parameter,
    construction_contracts_commercials_settle_commercial_claim,
)

_COMMAND_HANDLERS = {
    "configure_runtime": construction_contracts_commercials_configure_runtime,
    "set_parameter": lambda state, payload: construction_contracts_commercials_set_parameter(state, payload["name"], payload["value"]),
    "register_rule": construction_contracts_commercials_register_rule,
    "register_schema_extension": lambda state, payload: construction_contracts_commercials_register_schema_extension(
        state, payload["table"], payload["fields"]
    ),
    "receive_event": construction_contracts_commercials_receive_event,
    "command_construction_contract": construction_contracts_commercials_command_construction_contract,
    "create_construction_contract": construction_contracts_commercials_command_construction_contract,
    "progress_contract_lifecycle": construction_contracts_commercials_progress_contract_lifecycle,
    "record_pay_application": construction_contracts_commercials_record_pay_application,
    "certify_pay_application": construction_contracts_commercials_certify_pay_application,
    "review_retainage": construction_contracts_commercials_review_retainage,
    "release_retainage": construction_contracts_commercials_release_retainage,
    "approve_variation_order": construction_contracts_commercials_approve_variation_order,
    "assess_notice_timeliness": construction_contracts_commercials_assess_notice_timeliness,
    "register_commercial_claim": construction_contracts_commercials_register_commercial_claim,
    "settle_commercial_claim": construction_contracts_commercials_settle_commercial_claim,
    "create_lien_waiver": construction_contracts_commercials_create_lien_waiver,
    "record_subcontract_package": construction_contracts_commercials_record_subcontract_package,
    "run_change_impact_simulation": construction_contracts_commercials_run_change_impact_simulation,
    "replay_dead_letter_event": construction_contracts_commercials_replay_dead_letter_event,
}
_QUERY_HANDLERS = {
    "query_workbench": construction_contracts_commercials_query_workbench,
    "build_workbench_view": lambda state, payload: {
        "ok": True,
        "workbench": construction_contracts_commercials_build_workbench_view(
            state=state,
            tenant=payload.get("tenant", "default"),
            actor=payload.get("actor"),
        ),
        "side_effects": (),
    },
    "build_payment_certificate": construction_contracts_commercials_build_payment_certificate,
    "build_final_account_packet": construction_contracts_commercials_build_final_account_packet,
    "generate_cash_flow_forecast": construction_contracts_commercials_generate_cash_flow_forecast,
    "generate_contractor_scorecard": construction_contracts_commercials_generate_contractor_scorecard,
}


class ConstructionContractsCommercialsService:
    def __init__(self, state: dict | None = None):
        self.state = state or construction_contracts_commercials_empty_state()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        result = _COMMAND_HANDLERS[name](self.state, dict(payload))
        if "state" in result:
            self.state = result["state"]
        return {
            **result,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "command"),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (result.get("operation_contract", {}) or {}).get("emitted_event", _operation_contract(name, "command")["emitted_event"]),
            "transaction_boundary": "owned_datastore_plus_outbox",
        }

    def _query(self, name: str, payload: dict) -> dict:
        result = _QUERY_HANDLERS[name](self.state, dict(payload))
        return {
            **result,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "query"),
            "outbox_table": None,
            "emits": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "ConstructionContractsCommercialsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    all_operations = manifest["command_operations"] + manifest["query_operations"]
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in all_operations,
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = ConstructionContractsCommercialsService()
    contract = service.command_construction_contract(
        {
            "tenant": "tenant-smoke",
            "contract_code": "SMOKE-001",
            "contract_value": 1000.0,
            "schedule_of_values": (
                {"line_code": "S1", "work_package": "Prelims", "original_value": 600.0},
                {"line_code": "S2", "work_package": "Works", "original_value": 400.0},
            ),
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": contract["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": contract,
        "query": query,
        "side_effects": (),
    }
