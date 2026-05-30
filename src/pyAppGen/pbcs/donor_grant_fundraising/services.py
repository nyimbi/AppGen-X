"""Service layer for the donor_grant_fundraising PBC."""

from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS, DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES, execute_domain_operation as execute_domain_depth_operation
from .fundraising_app import (
    advance_prospect_stage,
    build_fundraising_workbench,
    compose_proposal_workspace,
    create_campaign,
    create_pledge,
    create_restriction,
    empty_fundraising_state,
    generate_briefing_packet,
    manage_grant_application,
    manage_review_chain,
    map_donor_relationship,
    post_gift,
    record_stewardship_touchpoint,
    register_donor_profile,
    score_fundraising_opportunity,
    track_acknowledgement,
    validate_grant_budget,
)
from .runtime import (
    DONOR_GRANT_FUNDRAISING_APP_COMMANDS,
    DONOR_GRANT_FUNDRAISING_APP_QUERY_METHODS,
    donor_grant_fundraising_build_workbench_view,
    donor_grant_fundraising_command_donor,
    donor_grant_fundraising_configure_runtime,
    donor_grant_fundraising_parse_document_instruction,
    donor_grant_fundraising_query_workbench,
    donor_grant_fundraising_receive_event,
    donor_grant_fundraising_register_rule,
    donor_grant_fundraising_register_schema_extension,
    donor_grant_fundraising_run_advanced_assessment,
    donor_grant_fundraising_set_parameter,
)

PBC_KEY = "donor_grant_fundraising"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
APP_COMMAND_HANDLERS = {
    "register_donor_profile": register_donor_profile,
    "advance_prospect_stage": advance_prospect_stage,
    "create_campaign": create_campaign,
    "create_pledge": create_pledge,
    "create_restriction": create_restriction,
    "post_gift": post_gift,
    "manage_grant_application": manage_grant_application,
    "record_stewardship_touchpoint": record_stewardship_touchpoint,
    "map_donor_relationship": map_donor_relationship,
    "compose_proposal_workspace": compose_proposal_workspace,
    "track_acknowledgement": track_acknowledgement,
    "generate_briefing_packet": generate_briefing_packet,
    "score_fundraising_opportunity": score_fundraising_opportunity,
    "manage_review_chain": manage_review_chain,
    "validate_grant_budget": validate_grant_budget,
}
RUNTIME_COMMAND_HANDLERS = {
    "configure_runtime": lambda state, payload: donor_grant_fundraising_configure_runtime(state, payload),
    "set_parameter": lambda state, payload: donor_grant_fundraising_set_parameter(state, payload["name"], payload.get("value")),
    "register_rule": lambda state, payload: donor_grant_fundraising_register_rule(state, payload),
    "register_schema_extension": lambda state, payload: donor_grant_fundraising_register_schema_extension(state, payload["table"], payload.get("fields", {})),
    "receive_event": lambda state, payload: donor_grant_fundraising_receive_event(state, payload),
    "command_donor": lambda state, payload: donor_grant_fundraising_command_donor(state, payload),
    "run_advanced_assessment": lambda state, payload: donor_grant_fundraising_run_advanced_assessment(state, payload),
    "parse_document_instruction": lambda state, payload: donor_grant_fundraising_parse_document_instruction(payload.get("document", ""), payload.get("instruction", "")),
}
APP_QUERY_HANDLERS = {
    "build_fundraising_workbench": lambda state, payload: build_fundraising_workbench(state),
    "build_workbench_view": lambda state, payload: donor_grant_fundraising_build_workbench_view(payload.get("tenant", "default")),
    "query_workbench": lambda state, payload: donor_grant_fundraising_query_workbench(state, payload),
}
COMMAND_TABLE_SCOPE = {
    "register_donor_profile": ("donor_grant_fundraising_donor",),
    "advance_prospect_stage": ("donor_grant_fundraising_donor",),
    "create_campaign": ("donor_grant_fundraising_campaign",),
    "create_pledge": ("donor_grant_fundraising_pledge",),
    "create_restriction": ("donor_grant_fundraising_restriction",),
    "post_gift": ("donor_grant_fundraising_gift", "donor_grant_fundraising_pledge", "donor_grant_fundraising_campaign"),
    "manage_grant_application": ("donor_grant_fundraising_grant_application",),
    "record_stewardship_touchpoint": ("donor_grant_fundraising_stewardship_touchpoint",),
    "map_donor_relationship": ("donor_grant_fundraising_donor_relationship",),
    "compose_proposal_workspace": ("donor_grant_fundraising_proposal_workspace",),
    "track_acknowledgement": ("donor_grant_fundraising_acknowledgement",),
    "generate_briefing_packet": ("donor_grant_fundraising_briefing_packet",),
    "score_fundraising_opportunity": ("donor_grant_fundraising_opportunity_score",),
    "manage_review_chain": ("donor_grant_fundraising_review_chain",),
    "validate_grant_budget": ("donor_grant_fundraising_budget_validation",),
    "configure_runtime": (),
    "set_parameter": ("donor_grant_fundraising_runtime_parameter",),
    "register_rule": ("donor_grant_fundraising_policy_rule",),
    "register_schema_extension": ("donor_grant_fundraising_schema_extension",),
    "receive_event": ("donor_grant_fundraising_appgen_inbox_event",),
    "command_donor": ("donor_grant_fundraising_donor",),
    "run_advanced_assessment": (),
    "parse_document_instruction": (),
}
QUERY_TABLE_SCOPE = {
    "build_fundraising_workbench": DOMAIN_DEPTH_OWNED_TABLES[:14],
    "build_workbench_view": DOMAIN_DEPTH_OWNED_TABLES[:14],
    "query_workbench": ("donor_grant_fundraising_donor",),
}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        tuple(RUNTIME_COMMAND_HANDLERS)
        + DONOR_GRANT_FUNDRAISING_APP_COMMANDS
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = tuple(dict.fromkeys(("query_workbench",) + DONOR_GRANT_FUNDRAISING_APP_QUERY_METHODS))
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    if kind == "command":
        owned_tables = COMMAND_TABLE_SCOPE.get(name, ())
        return {
            "operation": name,
            "operation_kind": kind,
            "owned_tables": owned_tables,
            "read_tables": (),
            "emitted_event": "DonorGrantFundraisingUpdated" if owned_tables else None,
            "transaction_boundary": "owned_datastore_plus_outbox",
        }
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": (),
        "read_tables": QUERY_TABLE_SCOPE.get(name, OWNED_TABLES[:4]),
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
    }


class DonorGrantFundraisingService:
    def __init__(self, state: dict | None = None):
        self.state = state or empty_fundraising_state()

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name in APP_COMMAND_HANDLERS:
            result = APP_COMMAND_HANDLERS[name](self.state, payload)
            self.state = result["state"]
            contract = _operation_contract(name, "command")
            emits = ("DonorGrantFundraisingUpdated",) if contract["owned_tables"] else ()
            return {
                "ok": result["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": contract,
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": emits,
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_app": result,
                "side_effects": (),
            }
        if name in RUNTIME_COMMAND_HANDLERS:
            result = RUNTIME_COMMAND_HANDLERS[name](self.state, payload)
            if "state" in result:
                self.state = result["state"]
            contract = _operation_contract(name, "command")
            emits = (contract["emitted_event"],) if contract["emitted_event"] else ()
            return {
                "ok": result["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": contract,
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": emits,
                "transaction_boundary": "owned_datastore_plus_outbox",
                "runtime": result,
                "side_effects": (),
            }
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
            "emits": (),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name in APP_QUERY_HANDLERS:
            result = APP_QUERY_HANDLERS[name](self.state, payload)
            return {
                "ok": result["ok"],
                "operation": name,
                "operation_kind": "query",
                "read_only": True,
                "payload": dict(payload),
                "operation_contract": _operation_contract(name, "query"),
                "outbox_table": None,
                "emits": (),
                "domain_app": result,
                "side_effects": (),
            }
        contract = _operation_contract(name, "query")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "DonorGrantFundraisingService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {"ok": operation in manifest["query_operations"] + manifest["command_operations"], "operation": operation, "operation_kind": kind, "payload": dict(payload or {}), "side_effects": ()}


def smoke_test() -> dict:
    service = DonorGrantFundraisingService()
    command = service.register_donor_profile({"tenant": "tenant-smoke", "donor_id": "svc-smoke", "donor_type": "foundation", "recognition_preference": "named"})
    query = service.build_fundraising_workbench({"tenant": "tenant-smoke"})
    route_query = service.build_workbench_view({"tenant": "tenant-smoke"})
    return {
        "ok": command["ok"] and query["ok"] and route_query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "route_query": route_query,
        "side_effects": (),
    }
