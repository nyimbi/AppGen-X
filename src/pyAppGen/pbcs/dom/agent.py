"""AI agent and document-intake surface for the DOM PBC."""

from __future__ import annotations

import hashlib
import re
from typing import Any

PBC_KEY = "dom"
AGENT_NAME = "DomAgent"
_DOCUMENT_ACTIONS = (
    "summarize",
    "extract_fields",
    "validate_against_rules",
    "draft_crud_plan",
    "prepare_order_capture",
    "prepare_exception_resolution",
)
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

_TABLE_OPERATION_MAP = {
    "dom_sales_order": {
        "create": ("capture_order",),
        "read": ("get_order_snapshot", "workbench"),
        "update": ("verify_order", "price_order", "request_cancellation"),
        "delete": ("request_cancellation",),
    },
    "dom_order_hold": {
        "create": ("apply_hold",),
        "read": ("workbench",),
        "update": ("release_hold",),
        "delete": ("release_hold",),
    },
    "dom_backorder": {
        "create": ("create_backorder",),
        "read": ("workbench",),
        "update": ("apply_substitution",),
        "delete": ("apply_substitution",),
    },
}


def _owned_tables() -> tuple[str, ...]:
    return (
        "dom_sales_order",
        "dom_order_line",
        "dom_order_hold",
        "dom_order_promise",
        "dom_tax_projection",
        "dom_fraud_screen",
        "dom_inventory_allocation_projection",
        "dom_fulfillment_plan",
        "dom_split_shipment",
        "dom_backorder",
        "dom_substitution",
        "dom_cancellation_request",
        "dom_shipment_projection",
        "dom_order_exception",
        "dom_appgen_outbox_event",
        "dom_appgen_inbox_event",
        "dom_dead_letter_event",
    )


def _query_operations() -> tuple[str, ...]:
    from . import services

    return services.standalone_service_manifest().get("query_methods", ())


def _command_operations() -> tuple[str, ...]:
    from . import services

    manifest = services.standalone_service_manifest()
    query_methods = set(manifest.get("query_methods", ()))
    return tuple(method for method in manifest.get("service_methods", ()) if method not in query_methods)


def _first_match(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else None


def extract_document_facts(document: str) -> dict[str, Any]:
    text = str(document or "")
    lines = []
    for raw_line in re.findall(r"([a-z0-9_\-]+)\s*x\s*(\d+(?:\.\d+)?)\s*@\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE):
        sku, quantity, unit_price = raw_line
        lines.append(
            {
                "line_id": f"line_{len(lines) + 1}",
                "item_id": sku.lower(),
                "quantity": float(quantity),
                "unit_price": float(unit_price),
            }
        )
    amount = _first_match(r"amount\s+(\d+(?:\.\d+)?)", text)
    channel = _first_match(r"channel\s+([a-z0-9_\-]+)", text)
    order_id = _first_match(r"order\s+([a-z0-9_\-]+)", text)
    customer_id = _first_match(r"customer\s+([a-z0-9_\-]+)", text)
    destination = _first_match(r"(?:destination|ship[_ ]?to)\s+([a-z0-9_\-]+)", text)
    service_level = _first_match(r"(?:service[_ ]?level|service)\s+([a-z0-9_\-]+)", text)
    cancellation = "cancel" in text.lower()
    return {
        "ok": bool(order_id or customer_id or lines),
        "order_id": order_id,
        "customer_id": customer_id,
        "channel": channel,
        "destination": destination,
        "service_level": service_level,
        "stated_amount": float(amount) if amount else None,
        "lines": tuple(lines),
        "cancellation_requested": cancellation,
    }


def agent_skill_manifest() -> dict:
    """Return the skills this PBC contributes to the composed application assistant."""
    query_operations = _query_operations()
    command_operations = _command_operations()
    return {
        "ok": bool(_SKILL_NAMES) and bool(_owned_tables()) and bool(query_operations),
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
        "query_operations": query_operations,
        "command_operations": command_operations,
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
            "order_intake_preparation",
            "exception_resolution_guidance",
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


def document_instruction_plan(document=None, instructions=None):
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    extracted = extract_document_facts(document_text)
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest()
    action = "delete" if "delete" in instruction_text.lower() else "update" if any(token in instruction_text.lower() for token in ("update", "modify", "release", "cancel")) else "create"
    candidate_table = "dom_order_hold" if "hold" in instruction_text.lower() else "dom_sales_order"
    mutation_plan = datastore_crud_plan(action, table=candidate_table, payload={"order_id": extracted.get("order_id"), "customer_id": extracted.get("customer_id")})
    missing_fields = tuple(
        field
        for field in ("order_id", "customer_id", "channel", "destination")
        if not extracted.get(field)
    )
    summary = []
    if extracted.get("order_id"):
        summary.append(f"order {extracted['order_id']}")
    if extracted.get("customer_id"):
        summary.append(f"customer {extracted['customer_id']}")
    if extracted.get("channel"):
        summary.append(f"channel {extracted['channel']}")
    if extracted.get("lines"):
        summary.append(f"{len(extracted['lines'])} line(s)")
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": _owned_tables(),
        "candidate_operations": _command_operations() + _query_operations(),
        "requires_human_confirmation": True,
        "extracted": extracted,
        "instruction_action": action,
        "missing_fields": missing_fields,
        "mutation_plan": mutation_plan,
        "summary": ", ".join(summary) if summary else "no document facts extracted",
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None):
    """Plan governed CRUD against owned tables only."""
    normalized_action = str(action).lower()
    supplied = dict(payload or {})
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    operation_pool = _TABLE_OPERATION_MAP.get(selected_table, {}).get(
        normalized_action,
        _query_operations() if normalized_action == "read" else _command_operations(),
    )
    steps = []
    if normalized_action == "create" and selected_table == "dom_sales_order":
        steps = [
            {"step": "capture_order", "reason": "create order shell and lines"},
            {"step": "apply_tax_projection", "reason": "attach external tax evidence when available"},
            {"step": "screen_fraud", "reason": "gate release and fulfillment"},
            {"step": "verify_order", "reason": "transition to verified only after holds clear"},
        ]
    elif normalized_action == "update" and selected_table == "dom_order_hold":
        steps = [{"step": "release_hold", "reason": "clear blocking hold after evidence review"}]
    elif normalized_action == "delete" and selected_table == "dom_sales_order":
        steps = [{"step": "request_cancellation", "reason": "DOM cancels instead of hard-deleting orders"}]
    else:
        steps = [{"step": operation, "reason": "governed package-local operation"} for operation in operation_pool]
    return {
        "ok": allowed and bool(operation_pool),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(supplied)),
        "owned_tables": owned_tables,
        "candidate_operations": tuple(operation_pool),
        "steps": tuple(steps),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
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
        "dsl_tools": (f"{PBC_KEY}_skills", f"{PBC_KEY}_documents", f"{PBC_KEY}_crud"),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "side_effects": (),
    }


def smoke_test():
    """Exercise guidance, document intake, CRUD planning, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        "Order order_100 customer cust_100 channel web destination BOS amount 330 sku_100 x2 @125",
        "create the order and prepare verification",
    )
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", payload={"status": "draft", "order_id": "order_100"})
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
