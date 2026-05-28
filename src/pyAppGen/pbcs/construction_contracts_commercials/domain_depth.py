"""Domain depth contract for the construction_contracts_commercials PBC."""
from __future__ import annotations

from .core import (
    CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS,
    CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES,
    CONSTRUCTION_CONTRACTS_COMMERCIALS_RUNTIME_CAPABILITY_KEYS,
    CONSTRUCTION_CONTRACTS_COMMERCIALS_UI_FRAGMENT_KEYS,
    CONTROLS,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    PBC_KEY,
    SERVICE_COMMAND_OPERATIONS,
    WIZARDS,
    _operation_contract,
    construction_contracts_commercials_build_workbench_view,
    construction_contracts_commercials_runtime_smoke,
)
from .core import CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES as DOMAIN_OWNED_TABLES

DOMAIN_ENTITY = "construction_contract"
DOMAIN_PURPOSE = (
    "Construction contracts, pay applications, retainage, variations, claims, "
    "lien waivers, subcontract compliance, and commercial control governance"
)
DOMAIN_EVENTS = (
    "ConstructionContractsCommercialsCreated",
    "ConstructionContractsCommercialsUpdated",
    "ConstructionContractsCommercialsApproved",
    "ConstructionContractsCommercialsExceptionOpened",
)
DOMAIN_CONSUMED_EVENTS = CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES
DOMAIN_ADVANCED_CAPABILITIES = CONSTRUCTION_CONTRACTS_COMMERCIALS_RUNTIME_CAPABILITY_KEYS
DOMAIN_WORKBENCH_VIEWS = (
    "pay apps awaiting certification",
    "missing waivers",
    "expiring guarantees",
    "notice deadlines",
    "retainage release blockers",
    "final account blockers",
)


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "service_surface": SERVICE_COMMAND_OPERATIONS,
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "forms": (
            "construction_contract_create_form",
            "pay_application_intake_form",
            "retainage_release_form",
        ),
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "database_backends": CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 12,
        "minimum_domain_operations": 12,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    contract = _operation_contract(operation, "command")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": contract["owned_tables"][0] if contract["owned_tables"] else None,
        "owned_tables": contract["owned_tables"],
        "read_tables": (),
        "emitted_event": contract["emitted_event"],
        "event_contract": "AppGen-X",
        "permission": contract["permission"],
        "payload": payload,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_capability_surface_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": operation,
                "surface": f"{PBC_KEY}.ui.operation.{operation}",
                "action": operation,
                "target_table": execute_domain_operation(operation)["target_table"],
                "permission": execute_domain_operation(operation)["permission"],
                "requires_confirmation": operation not in ("generate_cash_flow_forecast", "generate_contractor_scorecard"),
                "event": execute_domain_operation(operation)["emitted_event"],
            }
            for operation in DOMAIN_OPERATIONS
        ),
        "rule_surfaces": tuple(
            {
                "rule": rule,
                "surface": f"{PBC_KEY}.ui.rule.{rule}",
                "editor": True,
                "explainable": True,
            }
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": parameter,
                "surface": f"{PBC_KEY}.ui.parameter.{parameter}",
                "bounded": True,
                "editable": True,
            }
            for parameter in DOMAIN_PARAMETERS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{index}",
                "explainable": True,
            }
            for index, capability in enumerate(DOMAIN_ADVANCED_CAPABILITIES, start=1)
        ),
        "edge_case_surfaces": tuple(
            {
                "edge_case": edge_case,
                "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}",
                "triage_queue": True,
            }
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        "coverage": {
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "ui_fragments": CONSTRUCTION_CONTRACTS_COMMERCIALS_UI_FRAGMENT_KEYS,
        },
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    workbench = construction_contracts_commercials_build_workbench_view()
    runtime = construction_contracts_commercials_runtime_smoke()
    contract = domain_depth_contract()
    return {
        "ok": contract["ok"] and workbench["ok"] and runtime["ok"] and len(contract["operations"]) >= contract["minimum_domain_operations"],
        "contract": contract,
        "workbench": workbench,
        "runtime": runtime,
        "side_effects": (),
    }
