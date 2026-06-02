"""AI agent and chatbot skill contract for the streaming_analytics PBC."""

from __future__ import annotations

import hashlib
import re

from .manifest import PBC_MANIFEST
from . import routes
from . import services


PBC_KEY = "streaming_analytics"
AGENT_NAME = "StreamingAnalyticsAgent"
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
        "stream_id": r"stream[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
        "window_id": r"window[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
        "projection_id": r"projection[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
        "tenant": r"tenant[:=]\s*([a-zA-Z0-9_.-]+)",
        "event_type": r"event[_\s-]*type[:=]\s*([a-zA-Z0-9_.-]+)",
        "metric_field": r"metric[_\s-]*field[:=]\s*([a-zA-Z0-9_.-]+)",
        "aggregation": r"aggregation[:=]\s*([a-zA-Z0-9_.-]+)",
        "region": r"region[:=]\s*([a-zA-Z0-9_.-]+)",
        "model_id": r"model[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
    }
    return {
        key: match.group(1)
        for key, pattern in patterns.items()
        if (match := re.search(pattern, text, flags=re.IGNORECASE))
    }


def agent_skill_manifest() -> dict:
    """Return the skills this PBC contributes to the composed application assistant."""
    route_contracts = routes.api_route_contracts()["contracts"]
    service_manifest = services.service_operation_manifest()
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
        "query_operations": service_manifest.get("query_operations", ()),
        "command_operations": service_manifest.get("command_operations", ()),
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
    if {"stream_id", "tenant", "event_type", "metric_field", "aggregation", "region"} <= set(extracted):
        candidate_records.append({"table": "streaming_analytics_metric_stream", "fields": extracted})
    if {"window_id", "tenant", "stream_id"} <= set(extracted):
        candidate_records.append({"table": "streaming_analytics_aggregation_window", "fields": extracted})
    if {"projection_id", "tenant", "stream_id"} <= set(extracted):
        candidate_records.append({"table": "streaming_analytics_dashboard_projection", "fields": extracted})
    if {"model_id", "tenant"} <= set(extracted):
        candidate_records.append({"table": "streaming_analytics_analytics_governed_model", "fields": extracted})
    keywords = {
        "ingestion": "register_metric_stream",
        "contract": "register_rule",
        "window": "define_window",
        "dashboard": "create_dashboard_projection",
        "replay": "open_replay_job",
        "watermark": "advance_watermark",
        "anomaly": "evaluate_threshold_alert",
        "forecast": "forecast_metric",
        "privacy": "screen_metric_policy",
        "model": "register_governed_model",
    }
    operation_hints = {
        operation
        for keyword, operation in keywords.items()
        if keyword in combined_text.lower()
    }
    operation_hints = operation_hints or ({"register_metric_stream"} if candidate_records else set())
    route_index = _route_index()
    mutation_preview = []
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
        "stream_id=stream_smoke tenant=tenant_smoke event_type=operational metric_field=latency_ms aggregation=avg region=US model_id=model_streaming_v1",
        "create ingestion contract, anomaly dashboard, replay policy, watermark and privacy controls",
    )
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", "streaming_analytics_metric_stream", {"status": "draft"})
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
