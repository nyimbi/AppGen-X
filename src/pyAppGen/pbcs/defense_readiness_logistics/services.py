"""Service layer for the defense_readiness_logistics PBC."""

from __future__ import annotations

from copy import deepcopy

from .config import compile_rule, set_parameter as validate_parameter, validate_configuration
from .defense_app import (
    allocate_fuel_reserve,
    assess_unit_readiness,
    build_defense_workbench,
    build_mission_capability,
    create_readiness_inspection,
    document_instruction_mutation_plan,
    empty_defense_state,
    plan_logistics_movement,
    project_maintenance_status,
    record_mission_asset,
    release_deployment_plan,
    request_theater_support,
    run_movement_release_workflow,
    run_readiness_validation_workflow,
    score_supply_readiness,
    triage_readiness_exception,
    validate_deployment_kit,
    validate_movement_load_plan,
    verify_controlled_item_custody,
    verify_personnel_qualification,
    workflow_contracts,
)
from .events import CONSUMED
from .models import OWNED_TABLES, PBC_KEY

EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
APP_COMMAND_HANDLERS = {
    "assess_unit_readiness": assess_unit_readiness,
    "record_mission_asset": record_mission_asset,
    "create_readiness_inspection": create_readiness_inspection,
    "verify_personnel_qualification": verify_personnel_qualification,
    "project_maintenance_status": project_maintenance_status,
    "score_supply_readiness": score_supply_readiness,
    "allocate_fuel_reserve": allocate_fuel_reserve,
    "validate_deployment_kit": validate_deployment_kit,
    "validate_movement_load_plan": validate_movement_load_plan,
    "verify_controlled_item_custody": verify_controlled_item_custody,
    "request_theater_support": request_theater_support,
    "plan_logistics_movement": plan_logistics_movement,
    "triage_readiness_exception": triage_readiness_exception,
    "release_deployment_plan": release_deployment_plan,
    "run_readiness_validation_workflow": run_readiness_validation_workflow,
    "run_movement_release_workflow": run_movement_release_workflow,
}
APP_QUERY_HANDLERS = {
    "build_defense_workbench": build_defense_workbench,
    "build_mission_capability": build_mission_capability,
    "document_instruction_plan": document_instruction_mutation_plan,
}
SERVICE_OPERATION_TARGETS = {
    "assess_unit_readiness": f"{PBC_KEY}_unit_readiness",
    "record_mission_asset": f"{PBC_KEY}_mission_asset",
    "create_readiness_inspection": f"{PBC_KEY}_readiness_inspection",
    "verify_personnel_qualification": f"{PBC_KEY}_personnel_qualification",
    "project_maintenance_status": f"{PBC_KEY}_maintenance_status",
    "score_supply_readiness": f"{PBC_KEY}_supply_request",
    "allocate_fuel_reserve": f"{PBC_KEY}_fuel_allocation",
    "validate_deployment_kit": f"{PBC_KEY}_deployment_plan",
    "validate_movement_load_plan": f"{PBC_KEY}_movement_load_plan",
    "verify_controlled_item_custody": f"{PBC_KEY}_controlled_item_custody",
    "request_theater_support": f"{PBC_KEY}_theater_support_request",
    "plan_logistics_movement": f"{PBC_KEY}_logistics_movement",
    "triage_readiness_exception": f"{PBC_KEY}_readiness_exception",
    "release_deployment_plan": f"{PBC_KEY}_deployment_plan",
    "run_readiness_validation_workflow": f"{PBC_KEY}_unit_readiness",
    "run_movement_release_workflow": f"{PBC_KEY}_logistics_movement",
}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
        )
        + tuple(APP_COMMAND_HANDLERS)
    )
)
QUERY_OPERATIONS = tuple(APP_QUERY_HANDLERS)


def _copy_state(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _operation_contract(name: str, kind: str) -> dict:
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": (SERVICE_OPERATION_TARGETS[name],) if kind == "command" and name in SERVICE_OPERATION_TARGETS else (),
        "read_tables": OWNED_TABLES if kind == "query" else (),
        "emitted_event": "DefenseReadinessLogisticsUpdated" if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class DefenseReadinessLogisticsService:
    def __init__(self, state: dict | None = None):
        self.state = state or empty_defense_state()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name == "configure_runtime":
            next_state = _copy_state(self.state)
            validation = validate_configuration(payload)
            next_state["configuration"] = {**dict(payload), "ok": validation["ok"], "event_contract": "AppGen-X"}
            self.state = next_state
            return {
                "ok": validation["ok"],
                "operation": name,
                "operation_kind": "command",
                "payload": dict(payload),
                "operation_contract": _operation_contract(name, "command"),
                "domain_app": {"configuration": next_state["configuration"]},
                "side_effects": (),
            }
        if name == "set_parameter":
            next_state = _copy_state(self.state)
            parameter = validate_parameter(payload["name"], payload["value"])
            if parameter["ok"]:
                next_state["parameters"][payload["name"]] = parameter
            self.state = next_state
            return {
                "ok": parameter["ok"],
                "operation": name,
                "operation_kind": "command",
                "payload": dict(payload),
                "operation_contract": _operation_contract(name, "command"),
                "domain_app": {"parameter": parameter},
                "side_effects": (),
            }
        if name == "register_rule":
            next_state = _copy_state(self.state)
            rule = compile_rule(payload)
            rule_id = payload.get("rule_id") or payload.get("name") or f"rule-{len(next_state['rules']) + 1}"
            next_state["rules"][rule_id] = rule["rule"]
            self.state = next_state
            return {
                "ok": True,
                "operation": name,
                "operation_kind": "command",
                "payload": dict(payload),
                "operation_contract": _operation_contract(name, "command"),
                "domain_app": {"rule": rule["rule"]},
                "side_effects": (),
            }
        if name == "register_schema_extension":
            next_state = _copy_state(self.state)
            table_name = payload.get("table_name") or payload.get("table")
            ok = bool(table_name and str(table_name).startswith(f"{PBC_KEY}_"))
            if ok:
                next_state["schema_extensions"][table_name] = dict(payload.get("field_manifest", {}))
            self.state = next_state
            return {
                "ok": ok,
                "operation": name,
                "operation_kind": "command",
                "payload": dict(payload),
                "operation_contract": _operation_contract(name, "command"),
                "domain_app": {"schema_extension": next_state["schema_extensions"].get(table_name)},
                "side_effects": (),
            }
        if name == "receive_event":
            next_state = _copy_state(self.state)
            idempotency_key = payload.get("idempotency_key") or payload.get("event_id") or repr(payload)
            duplicate = idempotency_key in next_state["idempotency_keys"]
            if not duplicate:
                next_state["idempotency_keys"].add(idempotency_key)
                if payload.get("event_type") in CONSUMED:
                    next_state["inbox"].append(dict(payload))
                else:
                    next_state["dead_letter"].append(dict(payload))
            self.state = next_state
            ok = payload.get("event_type") in CONSUMED
            return {
                "ok": ok or duplicate,
                "operation": name,
                "operation_kind": "command",
                "payload": dict(payload),
                "operation_contract": _operation_contract(name, "command"),
                "duplicate": duplicate,
                "domain_app": {"inbox_size": len(next_state["inbox"]), "dead_letter_size": len(next_state["dead_letter"])},
                "side_effects": (),
            }
        handler = APP_COMMAND_HANDLERS[name]
        result = handler(self.state, payload)
        if "state" in result:
            self.state = result["state"]
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "command",
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "command"),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": ("DefenseReadinessLogisticsUpdated",),
            "domain_app": result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        handler = APP_QUERY_HANDLERS[name]
        result = handler(self.state, payload) if name != "build_defense_workbench" else handler(self.state)
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "query",
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "query"),
            "outbox_table": None,
            "emits": (),
            "domain_app": result,
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "DefenseReadinessLogisticsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "workflows": tuple(workflow["workflow_id"] for workflow in workflow_contracts()["workflows"]),
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation in COMMAND_OPERATIONS:
        kind = "command"
    elif operation in QUERY_OPERATIONS:
        kind = "query"
    else:
        kind = "unknown"
    return {"ok": kind != "unknown", "operation": operation, "operation_kind": kind, "payload": payload, "side_effects": ()}


def smoke_test() -> dict:
    service = DefenseReadinessLogisticsService()
    configured = service.configure_runtime({"database_backend": "postgresql", "event_topic": f"pbc.{PBC_KEY}.events"})
    parameter = service.set_parameter({"name": "workbench_limit", "value": 50})
    rule = service.register_rule({"rule_id": "unit_readiness_policy", "scope": "readiness"})
    readiness = service.assess_unit_readiness(
        {
            "tenant_id": "tenant-smoke",
            "unit_id": "unit-smoke",
            "unit_code": "smoke-1",
            "personnel": {"available": 12, "required": 10, "certified_roles": 4, "required_certified_roles": 3},
            "serviceable_assets": 3,
            "required_assets": 2,
            "supply": {"critical_fill_rate": 0.95},
            "ammo_fill_rate": 0.9,
            "fuel_days": 2,
            "inspection_evidence": ("pack-1",),
            "commander_approved": True,
        }
    )
    workbench = service.build_defense_workbench({})
    return {
        "ok": configured["ok"] and parameter["ok"] and rule["ok"] and readiness["ok"] and workbench["ok"],
        "side_effects": (),
    }
