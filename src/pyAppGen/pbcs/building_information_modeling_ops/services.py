"""Stateful service layer for the executable BIM federation slice."""
from __future__ import annotations

from .domain_depth import (
    DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS,
    DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES,
    execute_domain_operation as execute_domain_depth_operation,
)
from .runtime import (
    PBC_KEY,
    BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC,
    building_information_modeling_ops_assemble_federation,
    building_information_modeling_ops_build_controls_contract,
    building_information_modeling_ops_build_federation_release_evidence,
    building_information_modeling_ops_build_forms_contract,
    building_information_modeling_ops_build_single_pbc_app_contract,
    building_information_modeling_ops_build_wizard_contract,
    building_information_modeling_ops_command_bim_model,
    building_information_modeling_ops_configure_project_coordinates,
    building_information_modeling_ops_configure_runtime,
    building_information_modeling_ops_empty_state,
    building_information_modeling_ops_parse_document_instruction,
    building_information_modeling_ops_query_workbench,
    building_information_modeling_ops_receive_event,
    building_information_modeling_ops_register_model_package,
    building_information_modeling_ops_register_rule,
    building_information_modeling_ops_register_schema_extension,
    building_information_modeling_ops_run_advanced_assessment,
    building_information_modeling_ops_set_parameter,
)

EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
    "topic": BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC,
}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "command_bim_model",
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "configure_project_coordinates",
            "register_model_package",
            "assemble_federation",
            "run_advanced_assessment",
        )
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = (
    "query_workbench",
    "build_forms_contract",
    "build_wizard_contract",
    "build_controls_contract",
    "build_single_pbc_app_contract",
    "build_federation_release_evidence",
    "parse_document_instruction",
)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    read_tables = OWNED_TABLES[:4] if kind == "query" else ()
    owned_tables = OWNED_TABLES[:4] if kind == "command" else ()
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": owned_tables,
        "read_tables": read_tables,
        "emitted_event": "BuildingInformationModelingOpsUpdated" if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox"
        if kind == "command"
        else "read_only_projection",
        "shared_table_access": False,
        "single_pbc_app": True,
    }


class BuildingInformationModelingOpsService:
    def __init__(self, state: dict | None = None):
        self.state = state or building_information_modeling_ops_empty_state()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _store_state(self, result: dict) -> dict:
        if "state" in result:
            self.state = result["state"]
        return result

    def _command(self, name: str, payload: dict) -> dict:
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
                    "shared_table_access": False,
                },
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (plan.get("emitted_event"),),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_depth": plan,
                "side_effects": (),
            }

        runtime_commands = {
            "command_bim_model": building_information_modeling_ops_command_bim_model,
            "configure_runtime": lambda state, item: building_information_modeling_ops_configure_runtime(
                state, item
            ),
            "set_parameter": lambda state, item: building_information_modeling_ops_set_parameter(
                state, item["name"], item["value"]
            ),
            "register_rule": lambda state, item: building_information_modeling_ops_register_rule(
                state, item
            ),
            "register_schema_extension": lambda state, item: building_information_modeling_ops_register_schema_extension(
                state, item["table"], item["fields"]
            ),
            "receive_event": building_information_modeling_ops_receive_event,
            "configure_project_coordinates": building_information_modeling_ops_configure_project_coordinates,
            "register_model_package": building_information_modeling_ops_register_model_package,
            "assemble_federation": building_information_modeling_ops_assemble_federation,
            "run_advanced_assessment": building_information_modeling_ops_run_advanced_assessment,
        }
        result = runtime_commands[name](self.state, payload)
        self._store_state(result)
        contract = _operation_contract(name, "command")
        return {
            **result,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (result.get("event", {}).get("event_type"),)
            if result.get("event")
            else (),
            "transaction_boundary": contract["transaction_boundary"],
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        query_contract = _operation_contract(name, "query")
        if name == "query_workbench":
            result = building_information_modeling_ops_query_workbench(self.state, payload)
        elif name == "build_forms_contract":
            result = building_information_modeling_ops_build_forms_contract()
        elif name == "build_wizard_contract":
            result = building_information_modeling_ops_build_wizard_contract()
        elif name == "build_controls_contract":
            result = building_information_modeling_ops_build_controls_contract()
        elif name == "build_single_pbc_app_contract":
            result = building_information_modeling_ops_build_single_pbc_app_contract()
        elif name == "build_federation_release_evidence":
            result = building_information_modeling_ops_build_federation_release_evidence(
                self.state,
                payload["federation_id"],
            )
        else:
            result = building_information_modeling_ops_parse_document_instruction(
                payload.get("document", ""),
                payload.get("instruction", ""),
            )
        return {
            **result,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": query_contract,
            "outbox_table": None,
            "emits": (),
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "BuildingInformationModelingOpsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "single_pbc_app": True,
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
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "single_pbc_app": True,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = BuildingInformationModelingOpsService()
    service.configure_runtime(
        {
            "database_backend": "postgresql",
            "event_topic": BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC,
        }
    )
    service.configure_project_coordinates(
        {
            "coordinate_basis": "project-grid-a",
            "survey_point": {"x": 0, "y": 0, "z": 0},
            "project_base_point": {"x": 0, "y": 0, "z": 0},
            "true_north_degrees": 0,
            "elevation_datum": "msl",
            "unit_scale": 1.0,
        }
    )
    command = service.register_model_package(
        {
            "model_id": "MODEL-A",
            "version_id": "VER-A1",
            "discipline": "architectural",
            "authoring_party": "Design Studio",
            "coordinate_basis": "project-grid-a",
            "survey_point": {"x": 0, "y": 0, "z": 0},
            "project_base_point": {"x": 0, "y": 0, "z": 0},
            "true_north_degrees": 0,
            "elevation_datum": "msl",
            "unit_scale": 1.0,
            "issue_purpose": "shared",
            "spatial_coverage": ("tower-a",),
            "lod_target": "LOD-300",
            "approval_state": "approved",
            "checksum": "sha256:ver-a1",
        }
    )
    query = service.query_workbench({})
    return {
        "ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "side_effects": (),
    }
