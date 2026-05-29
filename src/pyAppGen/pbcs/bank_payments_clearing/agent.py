"""AI assistant and governed planning surface for bank_payments_clearing."""

from __future__ import annotations

import hashlib
import re

from . import routes, services


PBC_KEY = "bank_payments_clearing"
AGENT_NAME = "BankPaymentsClearingAgent"
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_DOCUMENT_ACTIONS = (
    "summarize_payment_instruction",
    "extract_clearing_facts",
    "draft_mutation_preview",
    "explain_release_controls",
)
_SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.release_decision_support",
    f"{PBC_KEY}.reconciliation_triage",
)
_TABLE_OPERATION_MAP = {
    "bank_payments_clearing_participant_bank": {
        "create": "register_participant_bank",
        "read": "query_workbench",
        "update": "register_participant_bank",
    },
    "bank_payments_clearing_payment_instruction": {
        "create": "create_validated_payment_instruction",
        "read": "query_workbench",
        "update": "release_payment_instruction",
    },
    "bank_payments_clearing_return_item": {
        "create": "process_return_item",
        "read": "query_workbench",
        "update": "process_return_item",
    },
    "bank_payments_clearing_bank_reconciliation": {
        "create": "reconcile_bank_statement",
        "read": "query_workbench",
        "update": "reconcile_bank_statement",
    },
}


def _route_index() -> dict[str, dict]:
    return {
        contract["operation"]: contract
        for contract in routes.api_route_contracts()["contracts"]
    }


def _extract_candidate_fields(text: str) -> dict:
    patterns = {
        "instruction_id": r"instruction[_\s-]*id[:=]\s*([A-Za-z0-9_.-]+)",
        "participant_bank_id": r"participant[_\s-]*bank[_\s-]*id[:=]\s*([A-Za-z0-9_.-]+)",
        "routing_identifier": r"routing[_\s-]*identifier[:=]\s*([A-Za-z0-9_.-]+)",
        "rail": r"rail[:=]\s*([A-Za-z0-9_.-]+)",
        "amount": r"amount[:=]\s*([0-9.]+)",
        "currency": r"currency[:=]\s*([A-Za-z]{3})",
        "external_reference": r"external[_\s-]*reference[:=]\s*([A-Za-z0-9_.-]+)",
        "return_id": r"return[_\s-]*id[:=]\s*([A-Za-z0-9_.-]+)",
        "reconciliation_id": r"reconciliation[_\s-]*id[:=]\s*([A-Za-z0-9_.-]+)",
    }
    return {
        key: match.group(1)
        for key, pattern in patterns.items()
        if (match := re.search(pattern, text, flags=re.IGNORECASE))
    }


def _mutation_preview(operation: str | None) -> dict | None:
    if operation is None:
        return None
    contract = _route_index().get(operation)
    if contract is None:
        return None
    return {
        "operation": operation,
        "route": f"{contract['method']} {contract['path']}",
        "permission": contract["permission"],
        "idempotency_key": contract["idempotency_key"],
        "emitted_event": contract["emitted_event"],
    }


def agent_skill_manifest() -> dict:
    route_contracts = routes.api_route_contracts()["contracts"]
    manifest = services.service_operation_manifest()
    return {
        "ok": bool(_SKILL_NAMES) and bool(route_contracts),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": skill,
                "scope": PBC_KEY,
                "allowed_crud_actions": _CRUD_ACTIONS,
                "document_actions": _DOCUMENT_ACTIONS,
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for skill in _SKILL_NAMES
        ),
        "query_operations": manifest["query_operations"],
        "command_operations": manifest["command_operations"],
        "route_count": len(route_contracts),
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
            "release_gate_explanation",
        ),
        "professional_controls": (
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "idempotency_preview",
            "human_confirmation_required",
        ),
        "side_effects": (),
    }


def document_instruction_plan(
    document: str | None = None,
    instruction: str | None = None,
    *,
    instructions: str | None = None,
) -> dict:
    instruction_text = instruction if instruction is not None else instructions
    combined_text = "\n".join(part for part in (str(document or ""), str(instruction_text or "")) if part).strip()
    digest = hashlib.sha256(f"{PBC_KEY}:{combined_text}".encode("utf-8")).hexdigest()
    extracted = _extract_candidate_fields(combined_text)
    candidate_records = []
    mutation_preview = []
    if {"participant_bank_id", "routing_identifier"} <= set(extracted):
        candidate_records.append(
            {
                "table": "bank_payments_clearing_participant_bank",
                "fields": extracted,
            }
        )
        preview = _mutation_preview("register_participant_bank")
        if preview:
            mutation_preview.append(preview)
    if {"instruction_id", "participant_bank_id", "rail", "amount"} <= set(extracted):
        candidate_records.append(
            {
                "table": "bank_payments_clearing_payment_instruction",
                "fields": extracted,
            }
        )
        preview = _mutation_preview("create_validated_payment_instruction")
        if preview:
            mutation_preview.append(preview)
    if "return_id" in extracted:
        candidate_records.append(
            {
                "table": "bank_payments_clearing_return_item",
                "fields": extracted,
            }
        )
        preview = _mutation_preview("process_return_item")
        if preview:
            mutation_preview.append(preview)
    if "reconciliation_id" in extracted:
        candidate_records.append(
            {
                "table": "bank_payments_clearing_bank_reconciliation",
                "fields": extracted,
            }
        )
        preview = _mutation_preview("reconcile_bank_statement")
        if preview:
            mutation_preview.append(preview)
    if "release" in combined_text.lower() and extracted.get("instruction_id"):
        preview = _mutation_preview("release_payment_instruction")
        if preview:
            mutation_preview.append(preview)
    deduped_preview = []
    seen = set()
    for item in mutation_preview:
        key = item["operation"]
        if key not in seen:
            deduped_preview.append(item)
            seen.add(key)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": digest,
        "instruction": instruction_text,
        "extracted_fields": extracted,
        "candidate_records": tuple(candidate_records),
        "candidate_tables": tuple(record["table"] for record in candidate_records),
        "mutation_preview": tuple(deduped_preview),
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "plan", "event_contract": "AppGen-X"},
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or "bank_payments_clearing_payment_instruction"
    payload = dict(payload or {})
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    operation = _TABLE_OPERATION_MAP.get(target, {}).get(action)
    preview = _mutation_preview(operation)
    supported = action in _CRUD_ACTIONS and action != "delete" and preview is not None
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": payload,
        "supported": supported,
        "requires_confirmation": action in {"create", "update", "delete"},
        "operation_preview": preview,
        "event_contract": "AppGen-X",
        "reason": None if supported else "delete_not_supported_in_standalone_slice" if action == "delete" else "no_route_mapping",
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    manifest = services.service_operation_manifest()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (
            f"{PBC_KEY}_skills",
            f"{PBC_KEY}_crud",
            f"{PBC_KEY}_documents",
            f"{PBC_KEY}_payment_release",
        ),
        "execution_operations": manifest["payment_operations"],
        "query_operations": manifest["query_operations"],
        "workbench_route": "/bank-payments-clearing-workbench",
        "standalone_app": True,
        "side_effects": (),
    }


def smoke_test() -> dict:
    document = document_instruction_plan(
        "instruction_id=pay_smoke participant_bank_id=bank_smoke rail=ach amount=120 currency=USD external_reference=SMOKE-1",
        "release this instruction",
    )
    crud = datastore_crud_plan("create", "bank_payments_clearing_payment_instruction", {"state": "validated"})
    delete_plan = datastore_crud_plan("delete", "bank_payments_clearing_payment_instruction")
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document["ok"]
        and crud["ok"]
        and delete_plan["supported"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
