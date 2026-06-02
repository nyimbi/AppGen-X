"""Service layer for the environment_health_safety PBC."""

from __future__ import annotations

from .standalone import (
    CONSUMED_EVENT_TYPES,
    DOMAIN_OPERATIONS,
    EMITTED_EVENT_TYPES,
    EVENT_TABLES,
    OWNED_TABLES,
    build_detail_view,
    build_release_evidence,
    build_service_contract,
    configure_runtime,
    create_corrective_action,
    create_ehs_incident,
    capture_inspection_sync,
    handle_consumed_event,
    issue_permit,
    promote_near_miss_cluster,
    query_workbench,
    register_rule,
    register_schema_extension,
    run_advanced_assessment,
    run_dynamic_risk_assessment,
    schedule_inspection,
    send_serious_incident_notice,
    set_parameter,
    verify_corrective_action,
    advance_incident_lifecycle,
    empty_state,
)

PBC_KEY = "environment_health_safety"
EVENT_CONTRACT = {
    "outbox_table": EVENT_TABLES[0],
    "inbox_table": EVENT_TABLES[1],
    "dead_letter_table": EVENT_TABLES[2],
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "create_ehs_incident",
    "advance_incident_lifecycle",
    "send_serious_incident_notice",
    "record_hazard",
    "promote_near_miss_cluster",
    "create_corrective_action",
    "verify_corrective_action",
    "schedule_inspection",
    "capture_inspection_sync",
    "issue_permit",
    "run_dynamic_risk_assessment",
    "run_advanced_assessment",
    "handle_consumed_event",
)
QUERY_OPERATIONS = ("query_workbench", "build_detail_view", "build_release_evidence")


def _catalog() -> tuple[dict, ...]:
    return build_service_contract()["operation_catalog"]


def _operation_contract(name: str, kind: str) -> dict:
    matching = next((item for item in _catalog() if item["operation"] == name), None)
    if matching:
        return matching
    if kind == "command":
        return {
            "operation": name,
            "operation_kind": kind,
            "owned_tables": OWNED_TABLES,
            "read_tables": (),
            "emitted_event": EMITTED_EVENT_TYPES[0],
            "transaction_boundary": "owned_datastore_plus_outbox",
        }
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": (),
        "read_tables": OWNED_TABLES,
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
    }


class EnvironmentHealthSafetyService:
    def __init__(self, state: dict | None = None):
        self.state = state or empty_state()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name == "configure_runtime":
            result = configure_runtime(self.state, payload)
        elif name == "set_parameter":
            result = set_parameter(self.state, payload["name"], payload["value"])
        elif name == "register_rule":
            result = register_rule(self.state, payload)
        elif name == "register_schema_extension":
            result = register_schema_extension(self.state, payload["table"], payload["fields"])
        elif name == "create_ehs_incident":
            result = create_ehs_incident(self.state, payload)
        elif name == "advance_incident_lifecycle":
            result = advance_incident_lifecycle(
                self.state,
                payload["incident_id"],
                payload["new_status"],
                actor=payload.get("actor"),
                dossier_updates=payload.get("dossier_updates"),
            )
        elif name == "send_serious_incident_notice":
            result = send_serious_incident_notice(self.state, payload["incident_id"], payload.get("actor", {"name": "system"}), payload.get("sent_at"))
        elif name == "record_hazard":
            from .standalone import record_hazard

            result = record_hazard(self.state, payload)
        elif name == "promote_near_miss_cluster":
            result = promote_near_miss_cluster(self.state, payload)
        elif name == "create_corrective_action":
            result = create_corrective_action(self.state, payload)
        elif name == "verify_corrective_action":
            result = verify_corrective_action(self.state, payload["action_id"], payload)
        elif name == "schedule_inspection":
            result = schedule_inspection(self.state, payload)
        elif name == "capture_inspection_sync":
            result = capture_inspection_sync(self.state, payload)
        elif name == "issue_permit":
            result = issue_permit(self.state, payload)
        elif name == "run_dynamic_risk_assessment":
            result = run_dynamic_risk_assessment(self.state, payload)
        elif name == "run_advanced_assessment":
            result = run_advanced_assessment(self.state, payload)
        elif name == "handle_consumed_event":
            result = handle_consumed_event(self.state, payload["event"])
        else:
            raise AttributeError(name)
        self.state = result.get("state", self.state)
        contract = _operation_contract(name, "command")
        return {
            **result,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract.get("emitted_event"),) if contract.get("emitted_event") else (),
            "transaction_boundary": contract["transaction_boundary"],
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == "query_workbench":
            result = query_workbench(self.state, payload)
        elif name == "build_detail_view":
            result = build_detail_view(self.state, payload["record_id"])
        elif name == "build_release_evidence":
            result = build_release_evidence()
        else:
            raise AttributeError(name)
        contract = _operation_contract(name, "query")
        return {
            **result,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "side_effects": (),
        }


def service_operation_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "EnvironmentHealthSafetyService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "consumes": CONSUMED_EVENT_TYPES,
        "side_effects": (),
    }


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {"ok": operation in manifest["query_operations"] + manifest["command_operations"], "operation": operation, "operation_kind": kind, "payload": dict(payload or {}), "side_effects": ()}


def smoke_test():
    service = EnvironmentHealthSafetyService()
    command = service.create_ehs_incident(
        {
            "tenant": "tenant-smoke",
            "code": "INC-SVC",
            "site": "Plant Smoke",
            "area": "Area Smoke",
            "task": "Task Smoke",
            "severity": "near_miss",
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {"ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"], "command": command, "query": query, "side_effects": ()}
