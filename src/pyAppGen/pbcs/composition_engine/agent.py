"""AI agent and chatbot skill contract for the composition_engine PBC."""

from __future__ import annotations

from .permissions import permission_manifest
from .runtime import COMPOSITION_ENGINE_OWNED_TABLES
from .runtime import composition_engine_agent_competency_catalog
from .runtime import composition_engine_assistant_document_preview
from .runtime import composition_engine_plan_crud_action
from .runtime import composition_engine_route_agent_intent
from .services import service_operation_manifest


PBC_KEY = "composition_engine"
AGENT_NAME = "CompositionEngineAgent"
_DOCUMENT_ACTIONS = (
    "summarize",
    "extract_constraints",
    "draft_workspace_plan",
    "preview_crud_change",
    "explain_release_readiness",
)


def _owned_tables():
    return tuple(f"{PBC_KEY}_{table}" for table in COMPOSITION_ENGINE_OWNED_TABLES)


def _query_operations():
    return service_operation_manifest().get("query_operations", ())


def _command_operations():
    return service_operation_manifest().get("command_operations", ())


def agent_skill_manifest():
    """Return the skills this PBC contributes to the composed application assistant."""
    competencies = composition_engine_agent_competency_catalog()
    skills = tuple(
        {
            "name": f"{PBC_KEY}.{item['competency_id']}",
            "scope": PBC_KEY,
            "owned_tables": _owned_tables(),
            "allowed_crud_actions": ("create", "read", "update", "delete"),
            "document_actions": _DOCUMENT_ACTIONS,
            "required_permission": item["permission"],
            "safe_reads": item["safe_reads"],
            "mutation_previews": item["mutation_previews"],
            "document_inputs": item["document_inputs"],
            "emitted_events": item["emitted_events"],
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for item in competencies["competencies"]
    )
    return {
        "ok": competencies["ok"] and bool(skills) and bool(_owned_tables()) and bool(_query_operations()),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": skills,
        "query_operations": _query_operations(),
        "command_operations": _command_operations(),
        "side_effects": (),
    }


def chatbot_interface_contract():
    """Return the professional help/chatbot surface contract for this PBC."""
    permissions = permission_manifest()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "preview_route": "/api/pbc/composition_engine/composition/assistant/document-preview",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "prompt_intake",
            "selection_rationale",
            "layout_planning",
            "dsl_review",
            "dependency_solving",
            "release_readiness_explanation",
            "rollback_planning",
        ),
        "professional_controls": (
            "citation_required_for_document_facts",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "audit_event_plan",
        ),
        "roles": permissions["roles"],
        "side_effects": (),
    }


def document_instruction_plan(document=None, instructions=None):
    """Plan document/instruction handling without mutating state."""
    preview = composition_engine_assistant_document_preview(
        str(document or ""),
        str(instructions or ""),
        action="read",
        target_table="composition_engine_composition_workspace",
    )
    return {
        "ok": preview["ok"],
        "pbc": PBC_KEY,
        "document_digest": preview["document_digest"],
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": _owned_tables(),
        "candidate_operations": _command_operations() + _query_operations(),
        "facts": preview["facts"],
        "citations": preview["facts"]["citations"],
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None):
    """Plan governed CRUD against owned tables only."""
    plan = composition_engine_plan_crud_action(action, target_table=table, payload=payload)
    return {
        "ok": plan["ok"] and bool(plan["operation"]),
        "pbc": PBC_KEY,
        "action": plan["action"],
        "table": plan["table"],
        "payload_keys": plan["payload_keys"],
        "owned_tables": _owned_tables(),
        "candidate_operations": (plan["operation"],) if plan["operation"] else (),
        "requires_confirmation": plan["requires_confirmation"],
        "required_permission": plan["required_permission"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "boundary": plan["boundary"],
        "side_effects": (),
    }


def route_agent_request(intent: str, context: dict | None = None) -> dict:
    """Route an assistant request to a composition competency."""
    routed = composition_engine_route_agent_intent(intent, context=context)
    return {
        "ok": routed["ok"],
        "pbc": PBC_KEY,
        "intent": intent,
        "competency_id": routed["competency_id"],
        "operation": routed["operation"],
        "required_permission": routed["required_permission"],
        "handoff_projections": routed["handoff_projections"],
        "side_effects": (),
    }


def assistant_preview(document=None, instructions=None, *, action="read", table=None, payload=None):
    """Combine document parsing, routing, and CRUD preview into one assistant response."""
    preview = composition_engine_assistant_document_preview(
        str(document or ""),
        str(instructions or ""),
        action=action,
        target_table=table,
        payload=payload,
    )
    return {
        "ok": preview["ok"],
        "pbc": PBC_KEY,
        "preview": preview,
        "side_effects": (),
    }


def composed_agent_contribution():
    """Return the package contribution to the application's single assistant."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    return {
        "ok": skills["ok"] and chatbot["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (
            f"{PBC_KEY}_skills",
            f"{PBC_KEY}_document_preview",
            f"{PBC_KEY}_crud_preview",
            f"{PBC_KEY}_routing_policy",
        ),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "side_effects": (),
    }


def smoke_test():
    """Exercise guidance, document intake, CRUD planning, routing, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        "Compose a customer console with auditable publication controls.",
        "Preview a release-note update and keep it bounded to composition-owned evidence.",
    )
    read_plan = datastore_crud_plan("read", "composition_engine_composition_workspace")
    create_plan = datastore_crud_plan("create", "composition_engine_composition_rule", payload={"status": "draft"})
    routed = route_agent_request("draft release readiness notes for this composition")
    preview = assistant_preview(
        "Compose a governed release workspace.",
        "Update the release evidence preview only.",
        action="update",
        table="composition_engine_release_evidence",
    )
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and routed["ok"]
        and preview["ok"]
        and contribution["ok"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "routed": routed,
        "preview": preview,
        "contribution": contribution,
        "side_effects": (),
    }
