"""Agent and assistant contracts for the oil_gas_field_operations PBC."""

from __future__ import annotations

from .controls import oil_gas_field_operations_mutation_preview
from .forms import oil_gas_field_operations_get_form
from .wizards import oil_gas_field_operations_plan_wizard

PBC_KEY = "oil_gas_field_operations"
OWNED_TABLES = (
    "oil_gas_field_operations_well",
    "oil_gas_field_operations_production_reading",
    "oil_gas_field_operations_field_ticket",
    "oil_gas_field_operations_workover_plan",
    "oil_gas_field_operations_hse_event",
    "oil_gas_field_operations_reserve_estimate",
    "oil_gas_field_operations_lifting_cost",
    "oil_gas_field_operations_oil_gas_field_operations_policy_rule",
    "oil_gas_field_operations_oil_gas_field_operations_runtime_parameter",
    "oil_gas_field_operations_oil_gas_field_operations_schema_extension",
    "oil_gas_field_operations_oil_gas_field_operations_control_assertion",
    "oil_gas_field_operations_oil_gas_field_operations_governed_model",
    "oil_gas_field_operations_appgen_outbox_event",
    "oil_gas_field_operations_appgen_inbox_event",
    "oil_gas_field_operations_appgen_dead_letter_event",
)
TARGET_TABLES = {
    "well": "oil_gas_field_operations_well",
    "production_reading": "oil_gas_field_operations_production_reading",
    "field_ticket": "oil_gas_field_operations_field_ticket",
    "workover_plan": "oil_gas_field_operations_workover_plan",
    "hse_event": "oil_gas_field_operations_hse_event",
}
TARGET_PERMISSIONS = {
    "well": "oil_gas_field_operations.create",
    "production_reading": "oil_gas_field_operations.create",
    "field_ticket": "oil_gas_field_operations.update",
    "workover_plan": "oil_gas_field_operations.approve",
    "hse_event": "oil_gas_field_operations.update",
}
TARGET_WIZARDS = {
    "well": "pad_startup_and_surveillance",
    "production_reading": "morning_production_review",
    "field_ticket": "morning_production_review",
    "workover_plan": "workover_readiness",
    "hse_event": "hse_boundary_response",
}


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_morning_review_brief",
            "scope": PBC_KEY,
            "description": "Summarize deferred production, invalid tests, integrity alerts, and route priority wells.",
            "requires_confirmation_for_mutation": False,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_workover_pack_preview",
            "scope": PBC_KEY,
            "description": "Prepare a cited workover readiness pack without mutating operational state.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_regulatory_draft_preview",
            "scope": PBC_KEY,
            "description": "Draft a traceable production or flare-reporting pack from approved evidence only.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "morning_production_review",
            "workover_readiness_preview",
            "regulatory_draft_preview",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document, instruction):
    target = "production_reading" if "production" in str(document).lower() or "production" in str(instruction).lower() else "field_ticket"
    wizard_id = TARGET_WIZARDS[target]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": str(abs(hash((document, instruction)))),
        "instruction": instruction,
        "target_entity": target,
        "candidate_tables": (TARGET_TABLES[target],),
        "wizard": oil_gas_field_operations_plan_wizard(wizard_id, {"well_id": "preview", "production_date": "preview"}),
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def oil_gas_field_operations_assistant_preview(request: dict | None = None) -> dict:
    payload = dict(request or {})
    target_entity = payload.get("target_entity", "production_reading")
    requested_action = str(payload.get("requested_action", "read")).lower()
    target_table = TARGET_TABLES.get(target_entity)
    form_id = "morning_review_request" if requested_action == "read" else {
        "well": "well_hierarchy_intake",
        "production_reading": "daily_production_capture",
        "field_ticket": "field_ticket_triage",
        "workover_plan": "workover_readiness_pack",
        "hse_event": "hse_boundary_event",
    }[target_entity]
    form = oil_gas_field_operations_get_form(form_id)
    mutation_preview = oil_gas_field_operations_mutation_preview(requested_action, target_table or "foreign_table", payload.get("payload"))
    wizard = oil_gas_field_operations_plan_wizard(
        TARGET_WIZARDS.get(target_entity, "morning_production_review"),
        {
            "well_id": payload.get("payload", {}).get("well_id") or payload.get("well_id") or "preview",
            "production_date": payload.get("payload", {}).get("production_date") or payload.get("production_date") or "preview",
        },
    )
    return {
        "ok": target_table is not None and requested_action in {"create", "read", "update", "delete"} and mutation_preview["ok"],
        "pbc": PBC_KEY,
        "permission": TARGET_PERMISSIONS.get(target_entity, "oil_gas_field_operations.read"),
        "target_entity": target_entity,
        "target_table": target_table,
        "form": form.get("form"),
        "mutation_preview": mutation_preview,
        "wizard": wizard,
        "requires_confirmation": requested_action != "read",
        "preview_only": True,
        "summary": f"{requested_action} preview for {target_entity} stays inside {target_table} and requires human confirmation for mutations.",
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_assistant_preview"),
        "side_effects": (),
    }


def smoke_test() -> dict:
    preview = oil_gas_field_operations_assistant_preview(
        {
            "document_text": "Review ROUTE-7 deferred production and invalid tests.",
            "instructions": "Generate a read-only morning brief.",
            "target_entity": "production_reading",
            "requested_action": "read",
            "payload": {"well_id": "WELL-7H", "production_date": "2026-05-29"},
        }
    )
    return {
        "ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"] and document_instruction_plan("doc", "create")["ok"] and datastore_crud_plan("create")["ok"] and datastore_crud_plan("update", table="foreign_table")["ok"] is False and composed_agent_contribution()["ok"] and preview["ok"],
        "side_effects": (),
    }
