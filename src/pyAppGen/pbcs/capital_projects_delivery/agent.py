from __future__ import annotations

import hashlib
import re

from .routes import api_route_contracts
from .runtime import (
    CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES,
    capital_projects_delivery_build_agent_help_contract,
    capital_projects_delivery_build_workflow_contracts,
)

PBC_KEY = "capital_projects_delivery"
AGENT_NAME = "CapitalProjectsDeliveryAgent"
OWNED_TABLES = CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES
_DOCUMENT_ACTIONS = ("summarize", "extract_fields", "validate_against_rules", "draft_crud_plan")
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.gate_review_preparation",
    f"{PBC_KEY}.workbench_navigation",
)


def _route_index() -> dict[str, dict]:
    return {contract["operation"]: contract for contract in api_route_contracts()["contracts"]}


def _candidate_operations_for_table(table: str, *, action: str) -> tuple[dict, ...]:
    route_contracts = tuple(_route_index().values())
    if action == "read":
        return tuple(contract for contract in route_contracts if contract["operation_kind"] == "query")
    return tuple(contract for contract in route_contracts if table in contract["owned_tables"])


def _extract_candidate_fields(text: str) -> dict:
    patterns = {
        "project_id": r"project[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
        "project_code": r"(?:project[_\s-]*code|code)[:=]\s*([a-zA-Z0-9_.-]+)",
        "tenant": r"tenant[:=]\s*([a-zA-Z0-9_.-]+)",
        "package_code": r"package[_\s-]*code[:=]\s*([a-zA-Z0-9_.-]+)",
        "permit_code": r"permit[_\s-]*code[:=]\s*([a-zA-Z0-9_.-]+)",
        "risk_code": r"risk[_\s-]*code[:=]\s*([a-zA-Z0-9_.-]+)",
    }
    return {key: match.group(1) for key, pattern in patterns.items() if (match := re.search(pattern, text, flags=re.IGNORECASE))}


def agent_skill_manifest():
    route_contracts = api_route_contracts()["contracts"]
    return {
        "ok": bool(_SKILL_NAMES) and bool(OWNED_TABLES) and bool(route_contracts),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": skill,
                "scope": PBC_KEY,
                "owned_tables": OWNED_TABLES,
                "allowed_crud_actions": _CRUD_ACTIONS,
                "document_actions": _DOCUMENT_ACTIONS,
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for skill in _SKILL_NAMES
        ),
        "route_count": len(route_contracts),
        "side_effects": (),
    }


def chatbot_interface_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "gate_approval_assistance",
            "workflow_navigation",
        ),
        "help_contract": capital_projects_delivery_build_agent_help_contract(),
        "side_effects": (),
    }


def document_instruction_plan(document, instruction):
    document_text = str(document or "")
    instruction_text = str(instruction or "")
    combined_text = f"{document_text}\n{instruction_text}".strip()
    digest = hashlib.sha256(f"{PBC_KEY}:{combined_text}".encode("utf-8")).hexdigest()
    extracted = _extract_candidate_fields(combined_text)
    candidate_records = []
    lowered = combined_text.lower()
    if any(term in lowered for term in ("project", "gate", "phase")):
        candidate_records.append({"table": f"{PBC_KEY}_capital_project", "fields": extracted})
    if any(term in lowered for term in ("package", "epc", "contractor")):
        candidate_records.append({"table": f"{PBC_KEY}_epc_package", "fields": extracted})
    if any(term in lowered for term in ("permit", "authority", "expiry")):
        candidate_records.append({"table": f"{PBC_KEY}_permit_milestone", "fields": extracted})
    if any(term in lowered for term in ("risk", "issue", "threat")):
        candidate_records.append({"table": f"{PBC_KEY}_project_risk", "fields": extracted})
    if any(term in lowered for term in ("handover", "turnover", "dossier")):
        candidate_records.append({"table": f"{PBC_KEY}_turnover_package", "fields": extracted})
    operation_hints = []
    if any(term in lowered for term in ("create", "open", "new project", "charter")):
        operation_hints.append("command_capital_project")
    if any(term in lowered for term in ("checklist", "criteria", "blocker")):
        operation_hints.append("record_gate_checklist")
    if any(term in lowered for term in ("approve", "gate", "rebaseline", "rollback")):
        operation_hints.append("approve_capital_project_gate")
    if "workbench" in lowered or "queue" in lowered:
        operation_hints.append("query_workbench")
    operation_hints = tuple(dict.fromkeys(operation_hints or ["command_capital_project"]))
    route_index = _route_index()
    mutation_preview = tuple(
        {
            "operation": operation,
            "route": f"{route_index[operation]['method']} {route_index[operation]['path']}",
            "permission": route_index[operation]["permission"],
            "idempotency_key": route_index[operation]["idempotency_key"],
            "emitted_event": route_index[operation]["emitted_event"],
        }
        for operation in operation_hints
        if operation in route_index
    )
    workflows = tuple(item["name"] for item in capital_projects_delivery_build_workflow_contracts()["workflows"] if any(token in lowered for token in item["name"].replace(PBC_KEY + "_", "").split("_")))
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": tuple(dict.fromkeys([record["table"] for record in candidate_records] or [OWNED_TABLES[0]])),
        "candidate_records": tuple(candidate_records),
        "candidate_operations": operation_hints,
        "candidate_workflows": workflows or ("capital_projects_delivery_gate_approval_workflow",),
        "mutation_preview": mutation_preview,
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    normalized_action = str(action).lower()
    target = table or OWNED_TABLES[0]
    if normalized_action not in _CRUD_ACTIONS or not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    candidate_operations = _candidate_operations_for_table(target, action=normalized_action)
    return {
        "ok": bool(candidate_operations),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": target,
        "payload": dict(payload or {}),
        "candidate_operations": tuple(item["operation"] for item in candidate_operations),
        "candidate_routes": tuple(f"{item['method']} {item['path']}" for item in candidate_operations),
        "required_permissions": tuple(dict.fromkeys(item["permission"] for item in candidate_operations)),
        "idempotency_keys": tuple(item["idempotency_key"] for item in candidate_operations if item["idempotency_key"]),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    return {
        "ok": skills["ok"] and chatbot["ok"],
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "assistant_help": capital_projects_delivery_build_agent_help_contract(),
        "route_count": skills["route_count"],
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"] and document_instruction_plan("project_id=PRJ-1 tenant=tenant_smoke", "approve gate after checklist")["ok"] and datastore_crud_plan("create")["ok"] and datastore_crud_plan("update", table="foreign_table")["ok"] is False and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
