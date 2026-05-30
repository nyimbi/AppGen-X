"""AI agent and chatbot skill contract for provider_revenue_cycle."""

from __future__ import annotations

import hashlib
import re

from .controls import provider_revenue_cycle_mutation_preview
from .runtime import PBC_KEY
from .runtime import provider_revenue_cycle_parse_document_instruction

AGENT_NAME = "ProviderRevenueCycleAgent"
_DOCUMENT_ACTIONS = (
    "summarize_account_stall_reasons",
    "extract_eligibility_or_authorization_facts",
    "draft_claim_scrub_or_appeal_plan",
    "draft_patient_balance_resolution_plan",
)
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_ENTITY_TO_TABLE = {
    "patient_account": "provider_revenue_cycle_patient_account",
    "charge_capture": "provider_revenue_cycle_charge_capture",
    "coding_case": "provider_revenue_cycle_coding_workqueue",
    "claim_batch": "provider_revenue_cycle_claim_batch",
    "denial_case": "provider_revenue_cycle_denial_case",
    "payment_posting": "provider_revenue_cycle_payment_posting",
    "collection_account": "provider_revenue_cycle_collection_account",
    "payer_contract": "provider_revenue_cycle_provider_revenue_cycle_policy_rule",
    "runtime_parameter": "provider_revenue_cycle_provider_revenue_cycle_runtime_parameter",
    "control_assertion": "provider_revenue_cycle_provider_revenue_cycle_control_assertion",
}
_ENTITY_TO_PERMISSION = {
    "patient_account": "provider_revenue_cycle.create",
    "charge_capture": "provider_revenue_cycle.update",
    "coding_case": "provider_revenue_cycle.update",
    "claim_batch": "provider_revenue_cycle.update",
    "denial_case": "provider_revenue_cycle.approve",
    "payment_posting": "provider_revenue_cycle.update",
    "collection_account": "provider_revenue_cycle.update",
    "payer_contract": "provider_revenue_cycle.admin",
    "runtime_parameter": "provider_revenue_cycle.admin",
    "control_assertion": "provider_revenue_cycle.admin",
}
_ENTITY_TO_EVENT = {
    "patient_account": "ProviderRevenueCycleCreated",
    "charge_capture": "ProviderRevenueCycleUpdated",
    "coding_case": "ProviderRevenueCycleUpdated",
    "claim_batch": "ProviderRevenueCycleApproved",
    "denial_case": "ProviderRevenueCycleExceptionOpened",
    "payment_posting": "ProviderRevenueCycleUpdated",
    "collection_account": "ProviderRevenueCycleUpdated",
    "payer_contract": None,
    "runtime_parameter": None,
    "control_assertion": None,
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
    if "appeal" in combined or "denial" in combined or "underpayment" in combined:
        return "denial_case"
    if "era" in combined or "remit" in combined or "refund" in combined:
        return "payment_posting"
    if "payment plan" in combined or "charity" in combined or "collection" in combined or "ar" in combined:
        return "collection_account"
    if "claim" in combined or "scrub" in combined:
        return "claim_batch"
    if "coding" in combined or "cdi" in combined:
        return "coding_case"
    if "charge" in combined:
        return "charge_capture"
    if "contract" in combined or "payer" in combined or "rule" in combined:
        return "payer_contract"
    if "parameter" in combined or "threshold" in combined:
        return "runtime_parameter"
    if "control" in combined or "compliance" in combined:
        return "control_assertion"
    return "patient_account"


def _infer_action(instruction_text: str, requested: str | None = None) -> str:
    if requested in _CRUD_ACTIONS:
        return requested
    lowered = instruction_text.lower()
    if re.search(r"\b(create|add|open|record|issue|enroll)\b", lowered):
        return "create"
    if re.search(r"\b(update|change|revise|amend|edit|link)\b", lowered):
        return "update"
    if re.search(r"\b(delete|remove|drop)\b", lowered):
        return "delete"
    return "read"


def agent_skill_manifest() -> dict:
    skills = tuple(
        {
            "name": name,
            "scope": PBC_KEY,
            "owned_tables": _owned_tables(),
            "allowed_crud_actions": _CRUD_ACTIONS,
            "document_actions": _DOCUMENT_ACTIONS,
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for name in (
            f"{PBC_KEY}.task_guidance",
            f"{PBC_KEY}.document_instruction_intake",
            f"{PBC_KEY}.governed_create",
            f"{PBC_KEY}.governed_read",
            f"{PBC_KEY}.governed_update",
            f"{PBC_KEY}.governed_delete",
            f"{PBC_KEY}.workbench_navigation",
            f"{PBC_KEY}.revenue_cycle_explanation",
        )
    )
    return {
        "ok": bool(skills) and bool(_owned_tables()) and bool(_query_operations()),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": skills,
        "query_operations": _query_operations(),
        "command_operations": _command_operations(),
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict:
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
            "mutation_preview_before_commit",
            "revenue_cycle_stall_explanation",
            "workbench_navigation",
        ),
        "professional_controls": (
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "appeal_packet_preview_only",
            "patient_protection_hold_awareness",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document=None, instructions=None, *, target_entity: str | None = None, requested_action: str | None = None) -> dict:
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    inferred = provider_revenue_cycle_parse_document_instruction(document_text, instruction_text)
    entity = _infer_entity(document_text, instruction_text, target_entity)
    action = _infer_action(instruction_text, requested_action)
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}:{entity}:{action}".encode("utf-8")).hexdigest()
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
        "candidate_operations": _command_operations() + _query_operations(),
        "inferred_tables": inferred["candidate_tables"],
        "requires_human_confirmation": action != "read",
        "side_effects": (),
    }


def datastore_crud_plan(action: str = "read", table: str | None = None, payload: dict | None = None) -> dict:
    normalized = str(action).lower()
    selected = table or _owned_tables()[0]
    entity = next((name for name, candidate in _ENTITY_TO_TABLE.items() if candidate == selected), None)
    return {
        "ok": normalized in _CRUD_ACTIONS and selected in _owned_tables(),
        "pbc": PBC_KEY,
        "action": normalized,
        "table": selected,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "candidate_operations": _query_operations() if normalized == "read" else _command_operations(),
        "requires_confirmation": normalized != "read",
        "event_contract": "AppGen-X",
        "permission": _ENTITY_TO_PERMISSION.get(entity),
        "expected_event": _ENTITY_TO_EVENT.get(entity),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def provider_revenue_cycle_assistant_preview(payload: dict | None = None) -> dict:
    supplied = dict(payload or {})
    plan = document_instruction_plan(
        supplied.get("document_text"),
        supplied.get("instructions"),
        target_entity=supplied.get("target_entity"),
        requested_action=supplied.get("requested_action"),
    )
    crud = datastore_crud_plan(plan["requested_action"], plan["candidate_table"], supplied.get("payload"))
    mutation = provider_revenue_cycle_mutation_preview(plan["requested_action"], plan["candidate_table"], supplied.get("payload"))
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
        "crud_plan": crud,
        "mutation_preview": mutation,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
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
    preview = provider_revenue_cycle_assistant_preview(
        {
            "document_text": "ERA shows an underpayment on claim claim_100",
            "instructions": "update the denial appeal plan and preview the refund hold",
            "requested_action": "update",
        }
    )
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and preview["ok"]
        and datastore_crud_plan("update", table="provider_revenue_cycle_patient_account")["ok"],
        "side_effects": (),
    }
