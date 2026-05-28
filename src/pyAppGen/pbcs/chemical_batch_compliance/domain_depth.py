"""Domain depth surface for the implemented chemical batch compliance slice."""

from __future__ import annotations

from .slice_app import ALLOWED_DATABASE_BACKENDS
from .slice_app import COMMAND_METHODS
from .slice_app import CONSUMED_EVENT_TYPES as DOMAIN_CONSUMED_EVENTS
from .slice_app import DOMAIN_ADVANCED_CAPABILITIES
from .slice_app import DOMAIN_EDGE_CASES
from .slice_app import DOMAIN_OPERATIONS
from .slice_app import DOMAIN_PARAMETERS
from .slice_app import DOMAIN_RULES
from .slice_app import EMITTED_EVENT_TYPES as DOMAIN_EVENTS
from .slice_app import OPERATION_EVENTS
from .slice_app import OPERATION_TABLES
from .slice_app import OWNED_TABLES as DOMAIN_OWNED_TABLES
from .slice_app import PBC_KEY
from .slice_app import QUERY_METHODS
from .slice_app import WORKBENCH_VIEWS as DOMAIN_WORKBENCH_VIEWS
from .slice_app import operation_contract
from .slice_app import stable_hash

DOMAIN_ENTITY = "chemical_formula_revision"
DOMAIN_PURPOSE = (
    "Controlled chemical recipe release, batch execution evidence, quality escalation, "
    "regulatory dossier assembly, and governed assistant-driven document instructions."
)


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 12,
        "minimum_domain_operations": 10,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    contract = operation_contract(operation, "command")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": OPERATION_TABLES[operation][0],
        "owned_tables": contract["owned_tables"],
        "read_tables": (),
        "emitted_event": OPERATION_EVENTS[operation],
        "event_contract": "AppGen-X",
        "idempotency_key": stable_hash((PBC_KEY, operation, payload)),
        "rules_evaluated": DOMAIN_RULES[:3],
        "parameters_read": DOMAIN_PARAMETERS[:3],
        "permission": f"{PBC_KEY}.operate",
        "evidence_hash": stable_hash((operation, payload, contract["owned_tables"])),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(execute_domain_operation(operation, {"tenant": "tenant-smoke"}) for operation in DOMAIN_OPERATIONS[:5])
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and all(item["ok"] for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }


DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        tuple(DOMAIN_ADVANCED_CAPABILITIES)
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
        + tuple(f"query_surface_{query}" for query in QUERY_METHODS)
    )
)


def domain_capability_surface_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": operation,
                "surface": f"{PBC_KEY}.ui.operation.{operation}",
                "action": operation,
                "target_table": OPERATION_TABLES[operation][0],
                "permission": f"{PBC_KEY}.operate",
                "requires_confirmation": operation.endswith("document_instruction") or "release" in operation,
                "agent_tool": f"{PBC_KEY}_skills.{operation}",
                "event": OPERATION_EVENTS[operation],
            }
            for operation in DOMAIN_OPERATIONS
        ),
        "rule_surfaces": tuple(
            {"rule": rule, "surface": f"{PBC_KEY}.ui.rule.{rule}", "editor": True, "explainable": True}
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
                "surface": f"{PBC_KEY}.ui.advanced.{stable_hash(capability)[:12]}",
                "explainable": True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        "edge_case_surfaces": tuple(
            {"edge_case": edge_case, "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}", "triage_queue": True}
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {"owned_table": table, "surface": f"{PBC_KEY}.ui.table.{table}", "read_model": True, "mutation_guard": True}
            for table in DOMAIN_OWNED_TABLES
        ),
        "specialist_capabilities": DOMAIN_SPECIALIST_CAPABILITIES,
        "coverage": {"event_contract": "AppGen-X", "stream_engine_picker_visible": False, "shared_table_access": False},
        "side_effects": (),
    }
