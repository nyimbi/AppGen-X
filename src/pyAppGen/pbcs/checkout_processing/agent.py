"""AI agent and chatbot skill contract for the checkout_processing PBC."""

from __future__ import annotations

import hashlib
import re

from .controls import checkout_processing_mutation_preview


PBC_KEY = "checkout_processing"
AGENT_NAME = "CheckoutProcessingAgent"
_DOCUMENT_ACTIONS = ("summarize", "extract_checkout_facts", "validate_against_rules", "draft_crud_plan")
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
_ENTITY_TO_TABLE = {
    "checkout_rule": "checkout_processing_checkout_rule",
    "checkout_parameter": "checkout_processing_checkout_parameter",
    "checkout_configuration": "checkout_processing_checkout_configuration",
    "checkout_session": "checkout_processing_checkout_session",
    "promotion_redemption": "checkout_processing_promotion_redemption",
}
_ENTITY_TO_PERMISSION = {
    "checkout_rule": "checkout_processing.configure",
    "checkout_parameter": "checkout_processing.configure",
    "checkout_configuration": "checkout_processing.configure",
    "checkout_session": "checkout_processing.checkout",
    "promotion_redemption": "checkout_processing.promotion",
}
_ENTITY_TO_EVENT = {
    "checkout_rule": None,
    "checkout_parameter": None,
    "checkout_configuration": None,
    "checkout_session": "CheckoutCompleted",
    "promotion_redemption": "OrderPriced",
}


def _owned_tables() -> tuple[str, ...]:
    return tuple(_ENTITY_TO_TABLE.values())


def _query_operations() -> tuple[str, ...]:
    from .services import service_operation_manifest

    return service_operation_manifest().get("query_operations", ())


def _command_operations() -> tuple[str, ...]:
    from .services import service_operation_manifest

    return service_operation_manifest().get("command_operations", ())


def _infer_entity(document_text: str, instruction_text: str, requested: str | None = None) -> str:
    if requested in _ENTITY_TO_TABLE:
        return requested
    combined = f"{document_text}\n{instruction_text}".lower()
    if "parameter" in combined or "threshold" in combined or "ttl" in combined:
        return "checkout_parameter"
    if "config" in combined or "currency" in combined or "country" in combined:
        return "checkout_configuration"
    if "coupon" in combined or "promotion" in combined:
        return "promotion_redemption"
    if "session" in combined or "checkout" in combined:
        return "checkout_session"
    return "checkout_rule"


def _infer_action(instruction_text: str, requested: str | None = None) -> str:
    if requested in _CRUD_ACTIONS:
        return requested
    lowered = instruction_text.lower()
    if re.search(r"\b(create|add|open)\b", lowered):
        return "create"
    if re.search(r"\b(update|change|revise|adjust)\b", lowered):
        return "update"
    if re.search(r"\b(delete|remove|drop)\b", lowered):
        return "delete"
    return "read"


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
            "mutation_preview_before_commit",
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


def document_instruction_plan(document=None, instructions=None, *, target_entity: str | None = None, requested_action: str | None = None) -> dict:
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    entity = _infer_entity(document_text, instruction_text, target_entity)
    action = _infer_action(instruction_text, requested_action)
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}:{entity}:{action}".encode("utf-8")).hexdigest()
    sensitive_fields = ("customer_id", "payment_intent_id", "authorization_id", "capture_id") if entity == "checkout_session" else ()
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "target_entity": entity,
        "requested_action": action,
        "candidate_table": _ENTITY_TO_TABLE[entity],
        "candidate_permission": _ENTITY_TO_PERMISSION[entity],
        "expected_event": _ENTITY_TO_EVENT[entity],
        "sensitive_fields": sensitive_fields,
        "candidate_operations": _command_operations() + _query_operations(),
        "requires_human_confirmation": action != "read",
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None) -> dict:
    """Plan governed CRUD against owned tables only."""
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    entity = next((name for name, candidate in _ENTITY_TO_TABLE.items() if candidate == selected_table), None)
    return {
        "ok": allowed,
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": owned_tables,
        "candidate_operations": _query_operations() if normalized_action == "read" else _command_operations(),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "permission": _ENTITY_TO_PERMISSION.get(entity),
        "expected_event": _ENTITY_TO_EVENT.get(entity),
        "side_effects": (),
    }


def checkout_processing_assistant_preview(payload: dict | None = None) -> dict:
    """Build a bounded assistant preview for document/instruction CRUD requests."""
    supplied = dict(payload or {})
    plan = document_instruction_plan(
        supplied.get("document_text"),
        supplied.get("instructions"),
        target_entity=supplied.get("target_entity"),
        requested_action=supplied.get("requested_action"),
    )
    crud = datastore_crud_plan(plan["requested_action"], plan["candidate_table"], supplied.get("payload"))
    mutation = checkout_processing_mutation_preview(plan["requested_action"], plan["candidate_table"], supplied.get("payload"))
    return {
        "ok": plan["ok"] and crud["ok"] and mutation["ok"],
        "pbc": PBC_KEY,
        "target_entity": plan["target_entity"],
        "action": plan["requested_action"],
        "candidate_table": plan["candidate_table"],
        "permission": plan["candidate_permission"],
        "expected_event": plan["expected_event"],
        "document_digest": plan["document_digest"],
        "requires_confirmation": plan["requires_human_confirmation"],
        "sensitive_fields": plan["sensitive_fields"],
        "crud_plan": crud,
        "mutation_preview": mutation,
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
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise guidance, document intake, CRUD planning, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        "Promo memo: SAVE15 remains web-only.",
        "Update the rule to keep SAVE15 web-only.",
        target_entity="checkout_rule",
        requested_action="update",
    )
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", table="checkout_processing_checkout_parameter", payload={"name": "risk_threshold"})
    preview = checkout_processing_assistant_preview(
        {
            "document_text": "Increase the retry limit to 4.",
            "instructions": "Update the checkout parameter for retry limit.",
            "target_entity": "checkout_parameter",
            "requested_action": "update",
            "payload": {"name": "max_retry_attempts", "value": 4},
        }
    )
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and preview["ok"]
        and contribution["ok"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "preview": preview,
        "contribution": contribution,
        "side_effects": (),
    }



def _standalone_operations() -> tuple[str, ...]:
    from .services import standalone_service_operation_contracts

    return standalone_service_operation_contracts()["operations"]


def standalone_agent_workspace_contract() -> dict:
    """Return the checkout-only app assistant workspace contract."""
    from .routes import standalone_route_contracts
    from .ui import checkout_processing_standalone_workbench_blueprint

    routes = standalone_route_contracts()
    workbench = checkout_processing_standalone_workbench_blueprint()
    return {
        "format": "appgen.checkout-processing-agent-workspace.v1",
        "ok": routes["ok"] and workbench["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": "/app/checkout-processing/assistant/sessions",
        "skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (f"{PBC_KEY}_skills", f"{PBC_KEY}_documents", f"{PBC_KEY}_crud", f"{PBC_KEY}_workflows"),
        "standalone_operations": _standalone_operations(),
        "standalone_routes": routes["routes"],
        "forms": tuple(form["form_id"] for form in workbench["forms"]),
        "wizards": tuple(wizard["wizard_id"] for wizard in workbench["wizards"]),
        "controls": tuple(control["control_id"] for control in workbench["controls"]),
        "professional_controls": chatbot_interface_contract()["professional_controls"],
        "side_effects": (),
    }


_BASE_DOCUMENT_INSTRUCTION_PLAN = document_instruction_plan
_BASE_DATASTORE_CRUD_PLAN = datastore_crud_plan


def document_instruction_plan(document=None, instructions=None, *, target_entity: str | None = None, requested_action: str | None = None) -> dict:
    """Plan document/instruction handling with standalone route and wizard context."""
    plan = _BASE_DOCUMENT_INSTRUCTION_PLAN(
        document,
        instructions,
        target_entity=target_entity,
        requested_action=requested_action,
    )
    try:
        from .wizards import checkout_processing_wizard_catalog
        from .routes import standalone_route_contracts

        wizards = checkout_processing_wizard_catalog()["wizard_ids"]
        routes = standalone_route_contracts()["routes"]
    except Exception:
        wizards = ()
        routes = ()
    return {
        **plan,
        "wizard_candidates": wizards,
        "standalone_routes": routes,
        "workspace": "checkout_processing_standalone_app",
    }


def datastore_crud_plan(action="read", table=None, payload=None) -> dict:
    """Plan governed CRUD with package-owned standalone tables included."""
    base = _BASE_DATASTORE_CRUD_PLAN(action, table, payload)
    standalone_tables = (
        "checkout_processing_runtime_state",
        "checkout_processing_form_submission",
        "checkout_processing_workflow_run",
        "checkout_processing_control_execution",
        "checkout_processing_agent_session",
        "checkout_processing_workbench_read_model",
    )
    selected_table = base.get("table") or table
    allowed = base.get("ok") is True or (str(action).lower() in _CRUD_ACTIONS and selected_table in standalone_tables)
    return {
        **base,
        "ok": allowed,
        "owned_tables": tuple(dict.fromkeys(tuple(base.get("owned_tables", ())) + standalone_tables)),
        "standalone_tables": standalone_tables,
        "standalone_operations": _standalone_operations(),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
