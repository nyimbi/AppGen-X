"""AI agent and chatbot skill contract for the ar_credit PBC."""

from __future__ import annotations

import hashlib

from .runtime import AR_CREDIT_OWNED_TABLES
from .receivables_workflows import ar_credit_build_collections_follow_up
from .receivables_workflows import ar_credit_execute_receipt_application
from .receivables_workflows import ar_credit_review_credit_onboarding
from .receivables_workflows import ar_credit_review_invoice_readiness
from .services import service_operation_manifest


PBC_KEY = "ar_credit"
AGENT_NAME = "ArCreditAgent"
_DOCUMENT_ACTIONS = ("summarize", "extract_fields", "validate_against_rules", "draft_crud_plan")
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_PREVIEW_OPERATIONS = (
    "review_credit_onboarding",
    "review_invoice_readiness",
    "execute_receipt_application",
    "build_collections_follow_up",
)
_SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.policy_explanation",
    f"{PBC_KEY}.workbench_navigation",
    f"{PBC_KEY}.credit_onboarding_preview",
    f"{PBC_KEY}.invoice_readiness_preview",
    f"{PBC_KEY}.cash_application_preview",
    f"{PBC_KEY}.collections_follow_up_preview",
)


def _query_operations():
    return service_operation_manifest().get("query_operations", ())


def _command_operations():
    return service_operation_manifest().get("command_operations", ())


def agent_skill_manifest():
    """Return the skills this PBC contributes to the composed application assistant."""
    return {
        "ok": bool(_SKILL_NAMES) and bool(AR_CREDIT_OWNED_TABLES) and bool(_query_operations()),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": skill,
                "scope": PBC_KEY,
                "owned_tables": AR_CREDIT_OWNED_TABLES,
                "allowed_crud_actions": _CRUD_ACTIONS,
                "document_actions": _DOCUMENT_ACTIONS,
                "preview_operations": _PREVIEW_OPERATIONS,
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


def chatbot_interface_contract():
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
            "credit_onboarding_preview",
            "invoice_readiness_preview",
            "cash_application_preview",
            "collections_follow_up_preview",
        ),
        "professional_controls": (
            "citation_required_for_document_facts",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "audit_event_plan",
            "appgen_x_event_contract_only",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document=None, instructions=None):
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    lowered = instruction_text.lower()
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest()
    suggestions = []
    if any(token in lowered for token in ("credit", "onboard", "customer", "limit")):
        suggestions.append({"operation": "review_credit_onboarding", "suggested": True})
    if any(token in lowered for token in ("invoice", "bill", "tax", "readiness")):
        suggestions.append({"operation": "review_invoice_readiness", "suggested": True})
    if any(token in lowered for token in ("remittance", "cash", "receipt", "apply")):
        suggestions.append({"operation": "execute_receipt_application", "suggested": True})
    if any(token in lowered for token in ("collect", "dunning", "statement", "aging")):
        suggestions.append({"operation": "build_collections_follow_up", "suggested": True})
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": AR_CREDIT_OWNED_TABLES,
        "candidate_operations": _command_operations() + _query_operations(),
        "workflow_suggestions": tuple(suggestions),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None):
    """Plan governed CRUD against owned tables only."""
    normalized_action = str(action).lower()
    selected_table = table or (AR_CREDIT_OWNED_TABLES[0] if AR_CREDIT_OWNED_TABLES else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in AR_CREDIT_OWNED_TABLES
    operation_pool = _query_operations() if normalized_action == "read" else _command_operations()
    return {
        "ok": allowed and bool(operation_pool),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": AR_CREDIT_OWNED_TABLES,
        "candidate_operations": operation_pool,
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def credit_onboarding_preview(payload=None):
    """Preview the onboarding evidence pack and credit decision."""
    review = ar_credit_review_credit_onboarding(dict(payload or {}).get("customer") or dict(payload or {}))
    return {
        "ok": review["ok"],
        "pbc": PBC_KEY,
        "review": review,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def invoice_readiness_preview(payload=None):
    """Preview invoice readiness without issuing the invoice."""
    supplied = dict(payload or {})
    review = ar_credit_review_invoice_readiness(
        supplied.get("state") or {},
        supplied.get("invoice") or supplied,
    )
    return {
        "ok": review["ok"],
        "pbc": PBC_KEY,
        "readiness": review,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def cash_application_preview(payload=None):
    """Preview executable receipt application for AR workbench assistants."""
    supplied = dict(payload or {})
    state = supplied.get("state")
    if state is None:
        return {"ok": False, "reason": "missing_state", "side_effects": ()}
    preview = ar_credit_execute_receipt_application(state, supplied.get("receipt") or supplied)
    return {
        "ok": preview["ok"],
        "pbc": PBC_KEY,
        "preview": preview,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def collections_follow_up_preview(payload=None):
    """Preview aging, statement, and dunning follow-up guidance."""
    supplied = dict(payload or {})
    state = supplied.get("state")
    if state is None:
        return {"ok": False, "reason": "missing_state", "side_effects": ()}
    follow_up = ar_credit_build_collections_follow_up(
        state,
        customer_id=supplied["customer_id"],
        as_of=supplied["as_of"],
    )
    return {
        "ok": follow_up["ok"],
        "pbc": PBC_KEY,
        "follow_up": follow_up,
        "event_contract": "AppGen-X",
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
            f"{PBC_KEY}_documents",
            f"{PBC_KEY}_crud",
            f"{PBC_KEY}_workflow_previews",
        ),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "side_effects": (),
    }


def smoke_test():
    """Exercise guidance, document intake, CRUD planning, and preview surfaces."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan("sample instruction", "review invoice readiness and cash application")
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", payload={"status": "draft"})
    onboarding = credit_onboarding_preview(
        {
            "customer_id": "smoke_customer",
            "tenant": "smoke",
            "name": "Smoke Customer",
            "terms": {"net_days": 30},
            "risk_signals": {"payment_latency": 0.03},
            "identity": {"did": "did:appgen:smoke_customer", "issuer": "trusted_registry", "status": "active"},
            "requested_limit": 1000,
        }
    )
    invoice_preview = invoice_readiness_preview(
        {
            "invoice_id": "smoke_invoice",
            "customer_id": "missing_customer",
            "invoice_date": "2026-05-28",
            "due_date": "2026-06-27",
            "lines": ({"sku": "svc", "quantity": 1, "unit_price": 100, "account": "revenue"},),
            "tax": {"jurisdiction": "KE", "amount": 16},
            "performance_obligations": ({"obligation": "svc", "allocation": 100, "satisfied": True},),
        }
    )
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and onboarding["ok"]
        and invoice_preview["ok"]
        and contribution["ok"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "onboarding": onboarding,
        "invoice_preview": invoice_preview,
        "contribution": contribution,
        "side_effects": (),
    }
