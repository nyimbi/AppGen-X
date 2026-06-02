"""Service layer for the energy_trading_risk one-PBC app."""
from __future__ import annotations

from .agent import assistant_help_manifest
from .agent import build_operator_guidance
from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES
from .domain_depth import execute_domain_operation as execute_domain_depth_operation
from .runtime import energy_trading_risk_build_workbench_view
from .runtime import energy_trading_risk_command_energy_contract
from .runtime import energy_trading_risk_command_exposure_limit
from .runtime import energy_trading_risk_command_market_price_curve
from .runtime import energy_trading_risk_command_nomination
from .runtime import energy_trading_risk_command_schedule
from .runtime import energy_trading_risk_command_settlement
from .runtime import energy_trading_risk_command_trade_position
from .runtime import energy_trading_risk_empty_state
from .runtime import energy_trading_risk_query_workbench
from .ui import energy_trading_risk_control_manifest
from .ui import energy_trading_risk_form_contract
from .ui import energy_trading_risk_single_pbc_app_ui_contract
from .ui import energy_trading_risk_wizard_contract

PBC_KEY = "energy_trading_risk"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "command_energy_contract",
            "command_trade_position",
            "command_nomination",
            "command_schedule",
            "command_settlement",
            "command_market_price_curve",
            "command_exposure_limit",
        )
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = (
    "query_workbench",
    "trade_capture_form",
    "nomination_form",
    "curve_form",
    "limit_form",
    "energy_risk_wizard",
    "energy_risk_controls",
    "assistant_help",
    "single_pbc_app",
)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES



def _operation_contract(name, kind):
    command_map = {
        "command_energy_contract": ("energy_trading_risk_energy_contract", "EnergyTradingRiskCreated"),
        "command_trade_position": ("energy_trading_risk_trade_position", "EnergyTradingRiskCreated"),
        "command_nomination": ("energy_trading_risk_nomination", "EnergyTradingRiskUpdated"),
        "command_schedule": ("energy_trading_risk_schedule", "EnergyTradingRiskApproved"),
        "command_settlement": ("energy_trading_risk_settlement", "EnergyTradingRiskUpdated"),
        "command_market_price_curve": ("energy_trading_risk_market_price_curve", "EnergyTradingRiskUpdated"),
        "command_exposure_limit": ("energy_trading_risk_exposure_limit", "EnergyTradingRiskUpdated"),
    }
    if name in command_map:
        table_name, emitted_event = command_map[name]
        return {
            "operation": name,
            "operation_kind": kind,
            "owned_tables": (table_name, EVENT_CONTRACT["outbox_table"]),
            "read_tables": (),
            "emitted_event": emitted_event,
            "transaction_boundary": "owned_datastore_plus_outbox",
        }
    if name == "query_workbench":
        return {
            "operation": name,
            "operation_kind": kind,
            "owned_tables": (),
            "read_tables": (
                "energy_trading_risk_trade_position",
                "energy_trading_risk_nomination",
                "energy_trading_risk_market_price_curve",
                "energy_trading_risk_exposure_limit",
            ),
            "emitted_event": None,
            "transaction_boundary": "read_only_projection",
        }
    if name in {"trade_capture_form", "nomination_form", "curve_form", "limit_form", "energy_risk_wizard", "energy_risk_controls", "assistant_help", "single_pbc_app"}:
        return {
            "operation": name,
            "operation_kind": kind,
            "owned_tables": (),
            "read_tables": (),
            "emitted_event": None,
            "transaction_boundary": "contract_only",
        }
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES[:2] if kind == "command" else (),
        "read_tables": OWNED_TABLES[:2] if kind == "query" else (),
        "emitted_event": "EnergyTradingRiskCreated" if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class EnergyTradingRiskService:
    def __init__(self, state=None):
        self.state = state or energy_trading_risk_empty_state()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _wrap_command(self, name, payload, result):
        return {
            **result,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "command"),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": tuple(event["event_type"] for event in result.get("events_emitted", ())),
            "transaction_boundary": "owned_datastore_plus_outbox",
        }

    def _command(self, name, payload):
        runtime_commands = {
            "command_energy_contract": energy_trading_risk_command_energy_contract,
            "command_trade_position": energy_trading_risk_command_trade_position,
            "command_nomination": energy_trading_risk_command_nomination,
            "command_schedule": energy_trading_risk_command_schedule,
            "command_settlement": energy_trading_risk_command_settlement,
            "command_market_price_curve": energy_trading_risk_command_market_price_curve,
            "command_exposure_limit": energy_trading_risk_command_exposure_limit,
        }
        if name in runtime_commands:
            result = runtime_commands[name](self.state, payload)
            self.state = result["state"]
            return self._wrap_command(name, payload, result)
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {
                "ok": plan["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": {
                    "operation": name,
                    "operation_kind": "command",
                    "owned_tables": plan.get("owned_tables", ()),
                    "read_tables": (),
                    "emitted_event": plan.get("emitted_event"),
                    "transaction_boundary": "owned_datastore_plus_outbox",
                },
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (plan.get("emitted_event"),),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_depth": plan,
                "side_effects": (),
            }
        contract = _operation_contract(name, "command")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract["emitted_event"],),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "side_effects": (),
        }

    def _query(self, name, payload):
        if name == "query_workbench":
            result = energy_trading_risk_query_workbench(self.state, payload)
            return {
                **result,
                "operation": name,
                "operation_kind": "query",
                "operation_contract": _operation_contract(name, "query"),
                "workbench_view": energy_trading_risk_build_workbench_view(payload.get("tenant", "default")),
            }
        if name == "trade_capture_form":
            return {"ok": True, "operation": name, "operation_kind": "query", "payload": dict(payload), "operation_contract": _operation_contract(name, "query"), "form": energy_trading_risk_form_contract("energy_trade_capture"), "side_effects": ()}
        if name == "nomination_form":
            return {"ok": True, "operation": name, "operation_kind": "query", "payload": dict(payload), "operation_contract": _operation_contract(name, "query"), "form": energy_trading_risk_form_contract("nomination_submission"), "side_effects": ()}
        if name == "curve_form":
            return {"ok": True, "operation": name, "operation_kind": "query", "payload": dict(payload), "operation_contract": _operation_contract(name, "query"), "form": energy_trading_risk_form_contract("price_curve_publish"), "side_effects": ()}
        if name == "limit_form":
            return {"ok": True, "operation": name, "operation_kind": "query", "payload": dict(payload), "operation_contract": _operation_contract(name, "query"), "form": energy_trading_risk_form_contract("exposure_limit_setup"), "side_effects": ()}
        if name == "energy_risk_wizard":
            wizard_id = payload.get("wizard_id", "trade_capture_release")
            return {"ok": True, "operation": name, "operation_kind": "query", "payload": dict(payload), "operation_contract": _operation_contract(name, "query"), "wizard": energy_trading_risk_wizard_contract(wizard_id), "side_effects": ()}
        if name == "energy_risk_controls":
            return {"ok": True, "operation": name, "operation_kind": "query", "payload": dict(payload), "operation_contract": _operation_contract(name, "query"), "controls": energy_trading_risk_control_manifest(), "side_effects": ()}
        if name == "assistant_help":
            return {"ok": True, "operation": name, "operation_kind": "query", "payload": dict(payload), "operation_contract": _operation_contract(name, "query"), "assistant_help": {**assistant_help_manifest(), "guidance": build_operator_guidance(workbench=payload)}, "side_effects": ()}
        if name == "single_pbc_app":
            return {"ok": True, "operation": name, "operation_kind": "query", "payload": dict(payload), "operation_contract": _operation_contract(name, "query"), "app_shell": energy_trading_risk_single_pbc_app_ui_contract(), "side_effects": ()}
        contract = _operation_contract(name, "query")
        return {"ok": True, "operation": name, "operation_kind": "query", "read_only": True, "payload": dict(payload), "operation_contract": contract, "outbox_table": None, "emits": (), "side_effects": ()}



def service_operation_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "EnergyTradingRiskService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }



def service_operation_contracts():
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, "query") for name in QUERY_OPERATIONS)
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}



def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {"ok": operation in manifest["query_operations"] + manifest["command_operations"], "operation": operation, "operation_kind": kind, "payload": dict(payload or {}), "side_effects": ()}



def smoke_test():
    service = EnergyTradingRiskService()
    limit = service.command_exposure_limit({
        "tenant": "tenant-smoke",
        "commodity": "power",
        "market_hub": "PJM",
        "book": "BOOK-1",
        "max_net_exposure_mwh": 250.0,
        "max_projected_mtm": 5000.0,
        "severity": "hard_stop",
        "owner": "risk",
        "effective_from": "2026-05-29T00:00:00Z",
    })
    curve = service.command_market_price_curve({
        "tenant": "tenant-smoke",
        "commodity": "power",
        "market_hub": "PJM",
        "delivery_period": "2026-06",
        "strip_start": "2026-06-01",
        "strip_end": "2026-06-30",
        "curve_price": 41.5,
        "as_of": "2026-05-29T08:00:00Z",
        "source_name": "ICE",
    })
    trade = service.command_trade_position({
        "tenant": "tenant-smoke",
        "commodity": "power",
        "market_hub": "PJM",
        "book": "BOOK-1",
        "trader": "alice",
        "strategy": "prompt-shape",
        "counterparty": "Counterparty-A",
        "side": "BUY",
        "position_type": "physical",
        "delivery_start": "2026-06-01",
        "delivery_end": "2026-06-30",
        "delivery_profile": "baseload",
        "pricing_formula": "fixed",
        "volume_mwh": 75.0,
        "fixed_price": 39.0,
        "submitted_at": "2026-05-29T09:00:00Z",
        "approval_state": "approved",
    })
    query = service.query_workbench({"tenant": "tenant-smoke"})
    form = service.trade_capture_form()
    wizard = service.energy_risk_wizard({"wizard_id": "trade_capture_release"})
    controls = service.energy_risk_controls()
    help_contract = service.assistant_help(query)
    return {
        "ok": limit["ok"] and curve["ok"] and trade["ok"] and query["ok"] and form["form"]["ok"] and wizard["wizard"]["ok"] and controls["controls"]["ok"] and help_contract["assistant_help"]["ok"] and service_operation_contracts()["ok"],
        "command": trade,
        "query": query,
        "side_effects": (),
    }
