"""AI agent and chatbot skill contract for the dam_core PBC."""

from __future__ import annotations

import hashlib
import re

from .manifest import PBC_MANIFEST
from . import routes
from . import services


PBC_KEY = "dam_core"
AGENT_NAME = "DamCoreAgent"
_DOCUMENT_ACTIONS = ("summarize", "extract_fields", "validate_against_rules", "draft_crud_plan")
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.policy_explanation",
    f"{PBC_KEY}.workbench_navigation",
)


def _owned_tables() -> tuple[str, ...]:
    return tuple(f"{PBC_KEY}_{table}" for table in PBC_MANIFEST.get("tables", ()))


def _route_index() -> dict[str, dict]:
    return {contract["operation"]: contract for contract in routes.api_route_contracts()["contracts"]}


def _candidate_operations_for_table(table: str, *, action: str) -> tuple[dict, ...]:
    route_contracts = tuple(_route_index().values())
    if action == "read":
        return tuple(contract for contract in route_contracts if contract["operation_kind"] == "query")
    return tuple(contract for contract in route_contracts if table in contract["owned_tables"])


def _extract_candidate_fields(text: str) -> dict:
    patterns = {
        "asset_id": r"asset[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
        "tenant": r"tenant[:=]\s*([a-zA-Z0-9_.-]+)",
        "filename": r"filename[:=]\s*([a-zA-Z0-9_.-]+)",
        "mime_type": r"mime[_\s-]*type[:=]\s*([a-zA-Z0-9/_.+-]+)",
        "policy_id": r"policy[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
        "taxonomy": r"taxonomy[:=]\s*([a-zA-Z0-9_.-]+)",
        "value": r"value[:=]\s*([a-zA-Z0-9_.-]+)",
    }
    return {
        key: match.group(1)
        for key, pattern in patterns.items()
        if (match := re.search(pattern, text, flags=re.IGNORECASE))
    }


def agent_skill_manifest() -> dict:
    """Return the skills this PBC contributes to the composed application assistant."""
    route_contracts = routes.api_route_contracts()["contracts"]
    return {
        "ok": bool(_SKILL_NAMES) and bool(_owned_tables()) and bool(route_contracts),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": skill,
                "scope": PBC_KEY,
                "owned_tables": _owned_tables(),
                "allowed_crud_actions": _CRUD_ACTIONS,
                "document_actions": _DOCUMENT_ACTIONS,
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for skill in _SKILL_NAMES
        ),
        "query_operations": services.service_operation_manifest().get("query_operations", ()),
        "command_operations": services.service_operation_manifest().get("command_operations", ()),
        "route_count": len(route_contracts),
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict:
    """Return the professional help/chatbot surface contract for this PBC."""
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_and_instruction_intake",
            "governed_datastore_crud",
            "policy_and_permission_explanation",
            "workbench_navigation",
            "release_gate_explanation",
        ),
        "professional_controls": (
            "citation_required_for_document_facts",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "audit_event_plan",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str | None = None, instructions: str | None = None) -> dict:
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    combined_text = f"{document_text}\n{instruction_text}".strip()
    digest = hashlib.sha256(f"{PBC_KEY}:{combined_text}".encode("utf-8")).hexdigest()
    extracted = _extract_candidate_fields(combined_text)
    candidate_records = []
    if {"asset_id", "tenant", "filename", "mime_type"} <= set(extracted):
        candidate_records.append({"table": "dam_core_asset", "fields": extracted})
    if {"policy_id", "asset_id", "tenant"} <= set(extracted):
        candidate_records.append({"table": "dam_core_rights_policy", "fields": extracted})
    if {"taxonomy", "value", "asset_id", "tenant"} <= set(extracted):
        candidate_records.append({"table": "dam_core_metadata_tag", "fields": extracted})
    mutation_preview = []
    keywords = {
        "register": "command_register_asset",
        "rights": "command_attach_rights_policy",
        "tag": "command_add_metadata_tag",
        "render": "command_request_rendition",
        "workflow": "command_start_asset_workflow",
    }
    operation_hints = {
        operation
        for keyword, operation in keywords.items()
        if keyword in combined_text.lower()
    }
    operation_hints = operation_hints or {"command_register_asset"} if candidate_records else set()
    route_index = _route_index()
    for operation in sorted(operation_hints):
        contract = route_index.get(operation)
        if contract:
            mutation_preview.append(
                {
                    "operation": operation,
                    "route": f"{contract['method']} {contract['path']}",
                    "permission": contract["permission"],
                    "idempotency_key": contract["idempotency_key"],
                    "emitted_event": contract["emitted_event"],
                }
            )
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": _owned_tables(),
        "candidate_records": tuple(candidate_records),
        "candidate_operations": tuple(sorted(operation_hints)),
        "mutation_preview": tuple(mutation_preview),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action: str = "read", table: str | None = None, payload: dict | None = None) -> dict:
    """Plan governed CRUD against owned tables only."""
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    candidate_operations = _candidate_operations_for_table(selected_table, action=normalized_action) if allowed else ()
    return {
        "ok": allowed and bool(candidate_operations),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": owned_tables,
        "candidate_operations": tuple(item["operation"] for item in candidate_operations),
        "candidate_routes": tuple(f"{item['method']} {item['path']}" for item in candidate_operations),
        "required_permissions": tuple(dict.fromkeys(item["permission"] for item in candidate_operations)),
        "idempotency_keys": tuple(item["idempotency_key"] for item in candidate_operations if item["idempotency_key"]),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    """Return the package contribution to the application's single assistant."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    return {
        "ok": skills["ok"] and chatbot["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (f"{PBC_KEY}_skills", f"{PBC_KEY}_documents", f"{PBC_KEY}_crud"),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "route_count": skills["route_count"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise guidance, document intake, CRUD planning, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        "asset_id=asset_smoke tenant=tenant_smoke filename=asset.jpg mime_type=image/jpeg taxonomy=product value=bag",
        "register asset then tag product bag",
    )
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", "dam_core_asset", payload={"status": "draft"})
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and contribution["ok"]
        and not create_plan["stream_engine_picker_visible"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "contribution": contribution,
        "side_effects": (),
    }
