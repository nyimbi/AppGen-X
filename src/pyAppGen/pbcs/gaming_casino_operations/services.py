"""Executable services for the gaming_casino_operations PBC."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from . import runtime
from .models import (
    CONTROL_ASSERTION_TABLE,
    GAMING_COMPLIANCE_TABLE,
    GOVERNED_MODEL_TABLE,
    PAYOUT_TABLE,
    PLAYER_PROFILE_TABLE,
    RESPONSIBLE_GAMING_CASE_TABLE,
    SLOT_MACHINE_TABLE,
    TABLE_GAME_TABLE,
    WAGER_SESSION_TABLE,
)
from .permissions import ACTION_PERMISSIONS


PBC_KEY = "gaming_casino_operations"
EVENT_CONTRACT = {
    "outbox_table": runtime.OUTBOX_EVENT_TABLE,
    "inbox_table": runtime.INBOX_EVENT_TABLE,
    "dead_letter_table": runtime.DEAD_LETTER_EVENT_TABLE,
    "event_contract": "AppGen-X",
}

PUBLIC_COMMAND_OPERATIONS = (
    "create_player_profile",
    "handle_table_game",
    "handle_slot_machine",
    "handle_wager_session",
    "handle_payout",
)
PUBLIC_QUERY_OPERATIONS = ("build_workbench_view",)
STANDALONE_COMMAND_OPERATIONS = (
    "register_defaults",
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "create_player_profile",
    "apply_player_restriction",
    "handle_table_game",
    "handle_slot_machine",
    "handle_wager_session",
    "handle_payout",
    "open_responsible_gaming_case",
    "record_compliance_case",
    "request_surveillance_review",
    "create_control_assertion",
    "register_governed_model",
    "run_player_enrollment_workflow",
    "run_table_shift_close_workflow",
    "run_slot_fault_recovery_workflow",
    "run_jackpot_handpay_workflow",
    "run_responsible_gaming_intervention_workflow",
)
STANDALONE_QUERY_OPERATIONS = (
    "build_workbench_view",
    "query_workbench",
    "run_advanced_assessment",
    "document_intake",
    "crud_mutation_plan",
)
SERVICE_TABLES = {
    "create_player_profile": (PLAYER_PROFILE_TABLE,),
    "apply_player_restriction": (PLAYER_PROFILE_TABLE,),
    "handle_table_game": (TABLE_GAME_TABLE,),
    "handle_slot_machine": (SLOT_MACHINE_TABLE,),
    "handle_wager_session": (WAGER_SESSION_TABLE,),
    "handle_payout": (PAYOUT_TABLE,),
    "open_responsible_gaming_case": (RESPONSIBLE_GAMING_CASE_TABLE, PLAYER_PROFILE_TABLE),
    "record_compliance_case": (GAMING_COMPLIANCE_TABLE,),
    "request_surveillance_review": (GAMING_COMPLIANCE_TABLE,),
    "create_control_assertion": (CONTROL_ASSERTION_TABLE,),
    "register_governed_model": (GOVERNED_MODEL_TABLE,),
}
SERVICE_EVENTS = {
    "create_player_profile": runtime.EMITTED[0],
    "apply_player_restriction": runtime.EMITTED[3],
    "handle_table_game": runtime.EMITTED[1],
    "handle_slot_machine": runtime.EMITTED[1],
    "handle_wager_session": runtime.EMITTED[1],
    "handle_payout": runtime.EMITTED[3],
    "open_responsible_gaming_case": runtime.EMITTED[3],
    "record_compliance_case": runtime.EMITTED[3],
    "request_surveillance_review": runtime.EMITTED[3],
}


def _operation_contract(name: str, kind: str) -> dict[str, Any]:
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": SERVICE_TABLES.get(name, ()) if kind == "command" else (),
        "read_tables": SERVICE_TABLES.get(name, ()) if kind == "query" else (),
        "emitted_event": SERVICE_EVENTS.get(name) if kind == "command" else None,
        "required_permission": ACTION_PERMISSIONS.get(name, f"{PBC_KEY}.read"),
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


def service_operation_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "GamingCasinoOperationsService",
        "command_operations": PUBLIC_COMMAND_OPERATIONS,
        "query_operations": PUBLIC_QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict[str, Any]:
    contracts = tuple(_operation_contract(name, "command") for name in PUBLIC_COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in PUBLIC_QUERY_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def standalone_service_operation_contracts() -> dict[str, Any]:
    contracts = tuple(_operation_contract(name, "command") for name in STANDALONE_COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in STANDALONE_QUERY_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "command_operations": STANDALONE_COMMAND_OPERATIONS,
        "query_operations": STANDALONE_QUERY_OPERATIONS,
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    manifest = standalone_service_operation_contracts()
    known = manifest["command_operations"] + manifest["query_operations"]
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in known,
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


class GamingCasinoOperationsService:
    """In-memory package-local service shell for standalone execution and tests."""

    def __init__(self, state: dict[str, Any] | None = None):
        self.state = deepcopy(state) if state is not None else runtime.gaming_casino_operations_empty_state()

    def _apply(self, fn, *args):
        result = fn(self.state, *args)
        self.state = result.get("state", self.state)
        return result

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.state)

    def close(self) -> None:
        return None

    def register_defaults(self) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_register_defaults)

    def configure_runtime(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_configure_runtime, payload)

    def set_parameter(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_set_parameter, payload["name"], payload["value"])

    def register_rule(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_register_rule, payload)

    def register_schema_extension(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_register_schema_extension, payload["table"], payload["fields"])

    def receive_event(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_receive_event, payload)

    def create_player_profile(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_create_player_profile, payload)

    def apply_player_restriction(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_apply_player_restriction, payload)

    def handle_table_game(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_handle_table_game, payload)

    def handle_slot_machine(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_handle_slot_machine, payload)

    def handle_wager_session(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_handle_wager_session, payload)

    def handle_payout(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_handle_payout, payload)

    def open_responsible_gaming_case(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_open_responsible_gaming_case, payload)

    def record_compliance_case(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_record_compliance_case, payload)

    def request_surveillance_review(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_request_surveillance_review, payload)

    def create_control_assertion(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_create_control_assertion, payload)

    def register_governed_model(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_register_governed_model, payload)

    def build_workbench_view(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        tenant = dict(payload or {}).get("tenant", "default")
        return runtime.gaming_casino_operations_build_workbench_view(self.state, tenant=tenant)

    def query_workbench(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return runtime.gaming_casino_operations_query_workbench(self.state, payload)

    def run_advanced_assessment(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return runtime.gaming_casino_operations_run_advanced_assessment(self.state, payload)

    def run_player_enrollment_workflow(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_run_player_enrollment_workflow, payload)

    def run_table_shift_close_workflow(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_run_table_shift_close_workflow, payload)

    def run_slot_fault_recovery_workflow(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_run_slot_fault_recovery_workflow, payload)

    def run_jackpot_handpay_workflow(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_run_jackpot_handpay_workflow, payload)

    def run_responsible_gaming_intervention_workflow(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(runtime.gaming_casino_operations_run_responsible_gaming_intervention_workflow, payload)

    def document_intake(self, payload: dict[str, Any]) -> dict[str, Any]:
        plan = runtime.gaming_casino_operations_parse_document_instruction(
            payload.get("document", ""),
            payload.get("instruction", ""),
        )
        self.state["document_intakes"].append(plan)
        return {"ok": True, "result": plan, "state": self.state, "side_effects": ()}

    def crud_mutation_plan(self, payload: dict[str, Any]) -> dict[str, Any]:
        table = payload.get("table", PLAYER_PROFILE_TABLE)
        route_map = {
            PLAYER_PROFILE_TABLE: "/app/gaming-casino-operations/player-profiles",
            TABLE_GAME_TABLE: "/app/gaming-casino-operations/table-games",
            SLOT_MACHINE_TABLE: "/app/gaming-casino-operations/slot-machines",
            WAGER_SESSION_TABLE: "/app/gaming-casino-operations/wager-sessions",
            PAYOUT_TABLE: "/app/gaming-casino-operations/payouts",
            RESPONSIBLE_GAMING_CASE_TABLE: "/app/gaming-casino-operations/responsible-gaming-cases",
            GAMING_COMPLIANCE_TABLE: "/app/gaming-casino-operations/compliance-cases",
        }
        return {
            "ok": table.startswith(f"{PBC_KEY}_") and table in runtime.GAMING_CASINO_OPERATIONS_OWNED_TABLES,
            "pbc": PBC_KEY,
            "action": payload.get("action", "create"),
            "table": table,
            "payload": dict(payload.get("payload", {})),
            "route_candidate": route_map.get(table),
            "required_permission": ACTION_PERMISSIONS.get("create_player_profile", f"{PBC_KEY}.create"),
            "requires_confirmation": payload.get("action", "create") in {"create", "update", "delete"},
            "event_contract": "AppGen-X",
            "side_effects": (),
        }


class GamingCasinoOperationsStandaloneService(GamingCasinoOperationsService):
    """Alias class used by standalone app composition."""


def smoke_test() -> dict[str, Any]:
    service = GamingCasinoOperationsStandaloneService()
    defaults = service.register_defaults()
    player = service.create_player_profile(
        {
            "tenant": "tenant-smoke",
            "player_number": "P-SERVICE",
            "legal_name": "Service Patron",
            "date_of_birth": "1990-01-01",
            "identity_confidence": 0.97,
            "age_verified": True,
        }
    )
    workbench = service.build_workbench_view({"tenant": "tenant-smoke"})
    return {
        "ok": defaults["ok"] and player["ok"] and workbench["ok"],
        "defaults": defaults,
        "player": player,
        "workbench": workbench,
        "side_effects": (),
    }
