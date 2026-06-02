"""AI agent and assistant skill contract for the workflow_orchestration PBC."""

from __future__ import annotations

import hashlib
import re

from .manifest import PBC_MANIFEST
from .repository import workflow_orchestration_repository_contract
from .services import service_operation_manifest
from .ui import workflow_orchestration_standalone_app_contract


PBC_KEY = "workflow_orchestration"
AGENT_NAME = "WorkflowOrchestrationAgent"
_DOCUMENT_ACTIONS = ("summarize", "extract_workflow_structure", "validate_against_rules", "draft_publication_plan")
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.workflow_authoring",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.policy_explanation",
    f"{PBC_KEY}.operational_action_preview",
    f"{PBC_KEY}.workbench_navigation",
)


def _owned_tables() -> tuple[str, ...]:
    repository = workflow_orchestration_repository_contract()
    return repository["owned_tables"] + repository["runtime_tables"]


def _query_operations() -> tuple[str, ...]:
    return service_operation_manifest().get("query_operations", ())


def _command_operations() -> tuple[str, ...]:
    return service_operation_manifest().get("command_operations", ())


def _route_candidates() -> tuple[str, ...]:
    return tuple(contract["path"] for contract in service_operation_manifest().get("operation_contracts", ()))


def agent_skill_manifest() -> dict:
    """Return the skills this PBC contributes to the composed application assistant."""
    return {
        "ok": bool(_SKILL_NAMES) and bool(_owned_tables()) and bool(_query_operations()),
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
        "query_operations": _query_operations(),
        "command_operations": _command_operations(),
        "route_candidates": _route_candidates(),
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
            "workflow_authoring",
            "document_and_instruction_intake",
            "governed_datastore_crud",
            "policy_and_permission_explanation",
            "operational_action_preview",
            "workbench_navigation",
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


def workflow_authoring_preview(document: str | None = None, instructions: str | None = None) -> dict:
    """Extract likely workflow authoring structure from operator text."""
    text = f"{document or ''}\n{instructions or ''}".strip()
    states = tuple(dict.fromkeys(re.findall(r"state[s]?[:\s]+([a-zA-Z0-9_,\s-]+)", text)))
    timers = tuple(dict.fromkeys(re.findall(r"(\d+\s*(?:seconds|minutes|hours|days))", text)))
    participants = tuple(dict.fromkeys(re.findall(r"\b([a-z]+_[a-z0-9_]+)\b", text)))
    approvals = tuple(dict.fromkeys(re.findall(r"\b(approve|approval|reject|escalate)\b", text.lower())))
    return {
        "ok": bool(text),
        "pbc": PBC_KEY,
        "draft_workflow_id": re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:48] or "workflow_draft",
        "states_detected": states,
        "timers_detected": timers,
        "participants_detected": participants,
        "approval_terms": approvals,
        "route_candidates": _route_candidates(),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def document_instruction_plan(document: str | None = None, instructions: str | None = None) -> dict:
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest()
    authoring = workflow_authoring_preview(document_text, instruction_text)
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": _owned_tables(),
        "candidate_operations": _command_operations() + _query_operations(),
        "route_candidates": _route_candidates(),
        "wizard_candidates": workflow_orchestration_standalone_app_contract()["wizards"],
        "authoring_preview": authoring,
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action: str = "read", table: str | None = None, payload: dict | None = None) -> dict:
    """Plan governed CRUD against owned tables only."""
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    operation_pool = _query_operations() if normalized_action == "read" else _command_operations()
    return {
        "ok": allowed and bool(operation_pool),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": owned_tables,
        "candidate_operations": operation_pool,
        "route_candidates": _route_candidates(),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def operational_action_preview(action: str, *, tenant: str, instance_id: str | None = None, reason: str | None = None) -> dict:
    """Preview a high-risk operational action without mutating state."""
    action_map = {
        "replay_signal": {"permission": "workflow_orchestration.signal", "operation": "signal_instance", "records_touched": ("workflow_signal", "workflow_instance")},
        "reschedule_timer": {"permission": "workflow_orchestration.start", "operation": "schedule_timer", "records_touched": ("timer_task",)},
        "reassign_task": {"permission": "workflow_orchestration.signal", "operation": "assign_human_task", "records_touched": ("human_task", "human_task_assignment")},
        "execute_compensation": {"permission": "workflow_orchestration.compensate", "operation": "execute_compensation", "records_touched": ("compensation", "saga_step")},
        "close_exception": {"permission": "workflow_orchestration.compensate", "operation": "open_exception_case", "records_touched": ("workflow_exception_case",)},
    }
    selected = action_map.get(action)
    if selected is None:
        return {"ok": False, "reason": "unknown_action", "action": action, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "tenant": tenant,
        "instance_id": instance_id,
        "reason": reason,
        "required_permission": selected["permission"],
        "candidate_operation": selected["operation"],
        "records_touched": tuple(f"{PBC_KEY}_{name}" for name in selected["records_touched"]),
        "rollback_strategy": "operator_review_before_mutation",
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def standalone_agent_workspace_contract() -> dict:
    """Return the package-local assistant workspace contract."""
    skills = agent_skill_manifest()
    return {
        "ok": skills["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_namespace": f"{PBC_KEY}_skills",
        "skill_names": tuple(item["name"] for item in skills["skills"]),
        "wizards": workflow_orchestration_standalone_app_contract()["wizards"],
        "route_candidates": skills["route_candidates"],
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    """Return the package contribution to the application's single assistant."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    workspace = standalone_agent_workspace_contract()
    return {
        "ok": skills["ok"] and chatbot["ok"] and workspace["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (f"{PBC_KEY}_skills", f"{PBC_KEY}_documents", f"{PBC_KEY}_crud", f"{PBC_KEY}_operations"),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "workspace": workspace,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise guidance, document intake, CRUD planning, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    authoring = workflow_authoring_preview("states: draft, approved, completed", "workflow invoice recovery with 4 hours timer and approve step")
    document = document_instruction_plan("workflow instruction", "create an approval workflow with escalation")
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", payload={"status": "draft"})
    action_preview = operational_action_preview("execute_compensation", tenant="tenant_demo", instance_id="instance_demo", reason="participant_timeout")
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and authoring["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and action_preview["ok"]
        and contribution["ok"]
        and not create_plan["stream_engine_picker_visible"],
        "skills": skills,
        "chatbot": chatbot,
        "authoring": authoring,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "action_preview": action_preview,
        "contribution": contribution,
        "side_effects": (),
    }
