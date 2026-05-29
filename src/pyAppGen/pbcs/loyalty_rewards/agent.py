"""AI agent and chatbot skill contract for the loyalty_rewards PBC."""

from __future__ import annotations

import hashlib
import re

from .manifest import PBC_MANIFEST
from . import routes
from . import services


PBC_KEY = "loyalty_rewards"
AGENT_NAME = "LoyaltyRewardsAgent"
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


_FIELD_PATTERNS = {
    "account_id": r"account[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
    "tenant": r"tenant[:=]\s*([a-zA-Z0-9_.-]+)",
    "customer_id": r"customer[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
    "partner_id": r"partner[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
    "offer_id": r"offer[_\s-]*id[:=]\s*([a-zA-Z0-9_.-]+)",
    "points": r"points[:=]\s*([0-9]+)",
    "currency": r"currency[:=]\s*([A-Z]{3})",
    "region": r"region[:=]\s*([A-Z]{2})",
    "consent_status": r"consent[_\s-]*status[:=]\s*([a-zA-Z0-9_.-]+)",
}


_KEYWORD_TO_OPERATION = {
    "enroll": "enroll_member",
    "earn": "issue_points",
    "burn": "create_redemption",
    "redeem": "create_redemption",
    "tier": "qualify_tier",
    "partner": "record_partner_accrual",
    "referral": "grant_referral_reward",
    "offer": "evaluate_offer_eligibility",
    "promotion": "evaluate_offer_eligibility",
    "consent": "screen_rewards_policy",
    "fraud": "review_fraud_risk",
    "expire": "schedule_expiration",
    "liability": "snapshot_liability",
    "reconcile": "reconcile_balance",
    "proof": "generate_balance_proof",
    "audit": "generate_balance_proof",
}


_TABLE_TO_OPERATIONS = {
    "loyalty_rewards_reward_account": ("enroll_member", "issue_points", "adjust_points", "create_redemption"),
    "loyalty_rewards_partner_accrual": ("record_partner_accrual",),
    "loyalty_rewards_referral_reward": ("grant_referral_reward",),
    "loyalty_rewards_offer_eligibility": ("evaluate_offer_eligibility", "simulate_offer"),
    "loyalty_rewards_rewards_policy_screening": ("screen_rewards_policy",),
    "loyalty_rewards_balance_reconciliation": ("reconcile_balance",),
    "loyalty_rewards_reward_balance_proof": ("generate_balance_proof",),
}


def _owned_tables() -> tuple[str, ...]:
    return tuple(f"{PBC_KEY}_{table}" for table in PBC_MANIFEST.get("tables", ()))


def _route_index() -> dict[str, dict]:
    contracts = services.service_operation_contracts().get("contracts", ())
    return {contract["operation"]: contract for contract in contracts}


def _candidate_operations_for_table(table: str, *, action: str) -> tuple[dict, ...]:
    route_contracts = tuple(_route_index().values())
    if action == "read":
        return tuple(contract for contract in route_contracts if contract["operation_kind"] == "query")
    allowed = set(_TABLE_TO_OPERATIONS.get(table, ()))
    if not allowed:
        return tuple(contract for contract in route_contracts if table in contract.get("owned_tables", ()))
    return tuple(contract for contract in route_contracts if contract["operation"] in allowed)


def _extract_candidate_fields(text: str) -> dict:
    extracted = {}
    for key, pattern in _FIELD_PATTERNS.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            extracted[key] = match.group(1)
    if "points" in extracted:
        extracted["points"] = int(extracted["points"])
    return extracted


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
    """Plan loyalty document and instruction handling without mutating state."""
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    combined_text = (document_text + "\n" + instruction_text).strip()
    digest = hashlib.sha256(f"{PBC_KEY}:{combined_text}".encode("utf-8")).hexdigest()
    extracted = _extract_candidate_fields(combined_text)

    candidate_records = []
    if {"account_id", "tenant", "customer_id", "currency", "region"} <= set(extracted):
        candidate_records.append({"table": "loyalty_rewards_reward_account", "fields": extracted})
    if {"account_id", "tenant", "partner_id", "points"} <= set(extracted):
        candidate_records.append({"table": "loyalty_rewards_partner_accrual", "fields": extracted})
    if {"account_id", "tenant", "offer_id"} <= set(extracted):
        candidate_records.append({"table": "loyalty_rewards_offer_eligibility", "fields": extracted})
    if {"account_id", "tenant", "points"} <= set(extracted) and "consent_status" in extracted:
        candidate_records.append({"table": "loyalty_rewards_rewards_policy_screening", "fields": extracted})

    candidate_operations = {
        operation
        for keyword, operation in _KEYWORD_TO_OPERATION.items()
        if keyword in combined_text.lower()
    }
    for record in candidate_records:
        candidate_operations.update(_TABLE_TO_OPERATIONS.get(record["table"], ()))
    mutation_preview = []
    route_index = _route_index()
    for operation in sorted(candidate_operations):
        contract = route_index.get(operation)
        if contract:
            mutation_preview.append(
                {
                    "operation": operation,
                    "route": f"{contract['method']} {contract['path']}",
                    "permission": contract["permission"],
                    "idempotency_key": contract.get("idempotency_key"),
                    "emitted_event": contract.get("emitted_event"),
                    "routed": contract.get("routed", True),
                }
            )

    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": _owned_tables(),
        "candidate_records": tuple(candidate_records),
        "candidate_operations": tuple(sorted(candidate_operations)),
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
        "candidate_routes": tuple(
            f"{item['method']} {item['path']}" if item.get("method") and item.get("path") else item["operation"]
            for item in candidate_operations
        ),
        "required_permissions": tuple(dict.fromkeys(item["permission"] for item in candidate_operations if item.get("permission"))),
        "idempotency_keys": tuple(item.get("idempotency_key") for item in candidate_operations if item.get("idempotency_key")),
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
        "account_id=acct_smoke tenant=tenant_smoke customer_id=cust_smoke currency=USD region=US offer_id=offer_smoke points=250 consent_status=granted",
        "enroll the member, evaluate the offer, and prepare a reconciliation proof",
    )
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", "loyalty_rewards_reward_account", payload={"status": "active"})
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
