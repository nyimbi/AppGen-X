"""AI agent and chatbot skill contract for trade_finance_operations."""

from __future__ import annotations

import hashlib

from .forms import trade_finance_operations_form_contracts
from .services import standalone_service_operation_contracts
from .wizards import trade_finance_operations_wizard_contracts

PBC_KEY = "trade_finance_operations"
AGENT_NAME = "TradeFinanceOperationsAgent"
OWNED_TABLES = (
    "trade_finance_operations_letter_of_credit",
    "trade_finance_operations_bank_guarantee",
    "trade_finance_operations_documentary_collection",
    "trade_finance_operations_trade_bill",
    "trade_finance_operations_trade_loan",
    "trade_finance_operations_trade_document",
    "trade_finance_operations_shipment_evidence",
    "trade_finance_operations_sanctions_check",
    "trade_finance_operations_discrepancy_case",
    "trade_finance_operations_collateral_margin",
    "trade_finance_operations_limit_reservation",
    "trade_finance_operations_fee_accrual",
    "trade_finance_operations_trade_settlement",
    "trade_finance_operations_swift_message_evidence",
    "trade_finance_operations_trade_finance_operations_policy_rule",
    "trade_finance_operations_trade_finance_operations_runtime_parameter",
    "trade_finance_operations_trade_finance_operations_schema_extension",
    "trade_finance_operations_trade_finance_operations_control_assertion",
    "trade_finance_operations_trade_finance_operations_governed_model",
    "trade_finance_operations_appgen_outbox_event",
    "trade_finance_operations_appgen_inbox_event",
    "trade_finance_operations_appgen_dead_letter_event",
)
_DOCUMENT_ACTIONS = (
    "summarize_terms",
    "extract_trade_clauses",
    "suggest_discrepancy_codes",
    "draft_refusal_or_waiver_text",
    "preview_governed_mutation",
)
_CRUD_ACTIONS = ("create", "read", "update", "delete")


def _standalone_operations() -> tuple[dict, ...]:
    return tuple(standalone_service_operation_contracts()["contracts"])


def agent_skill_manifest() -> dict:
    skills = tuple(
        {
            "name": f"{PBC_KEY}.{item['operation']}",
            "scope": PBC_KEY,
            "owned_tables": OWNED_TABLES,
            "allowed_crud_actions": _CRUD_ACTIONS,
            "document_actions": _DOCUMENT_ACTIONS,
            "required_permission": item["permission"],
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for item in _standalone_operations()
    )
    return {
        "ok": bool(skills),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": skills,
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
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "sanctions_boundary_guidance",
            "release_evidence_explanation",
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


def document_instruction_plan(document, instruction):
    document_text = str(document or "")
    instruction_text = str(instruction or "")
    combined = f"{document_text} {instruction_text}".lower()
    wizard_manifest = trade_finance_operations_wizard_contracts()["contracts"]
    form_manifest = trade_finance_operations_form_contracts()["contracts"]
    wizard_candidates = tuple(
        item["key"]
        for item in wizard_manifest
        if any(keyword in combined for keyword in item.get("keywords", ()))
    ) or ("TradeLetterOfCreditIssuanceWizard",)
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in _standalone_operations()
        if item.get("wizard") in wizard_candidates
    )
    form_candidates = tuple(
        form["key"] for form in form_manifest if form["operation"] in tuple(item["operation"] for item in _standalone_operations() if f"{item['method']} {item['path']}" in route_candidates)
    ) or ("TradeLetterOfCreditIssuanceForm",)
    extracted = {
        "mentions_sanctions": any(term in combined for term in ("sanction", "aml", "restricted")),
        "mentions_discrepancy": any(term in combined for term in ("discrepancy", "waiver", "refusal")),
        "mentions_swift": any(term in combined for term in ("swift", "mt700", "mt760")),
    }
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest(),
        "instruction": instruction_text,
        "candidate_tables": OWNED_TABLES[:14],
        "wizard_candidates": wizard_candidates,
        "form_candidates": form_candidates,
        "route_candidates": route_candidates,
        "extracted": extracted,
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None):
    normalized_action = str(action).lower()
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in _standalone_operations()
        if item["table"] == target and ((normalized_action == "read" and item["operation_kind"] == "query") or (normalized_action != "read" and item["operation_kind"] == "command"))
    )
    return {
        "ok": normalized_action in _CRUD_ACTIONS,
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "route_candidates": route_candidates,
        "side_effects": (),
    }


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "side_effects": (),
    }


def smoke_test():
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan("lc application with mt700 evidence", "create a governed draft and explain sanctions requirements")
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", payload={"status": "draft"})
    rejected = datastore_crud_plan("update", table="foreign_table")
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"] and chatbot["ok"] and document["ok"] and read_plan["ok"] and create_plan["ok"] and rejected["ok"] is False and contribution["ok"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "rejected": rejected,
        "contribution": contribution,
        "side_effects": (),
    }
