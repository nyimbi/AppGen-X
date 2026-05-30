"""Agent and chatbot support for governed claims adjudication document workflows."""

from __future__ import annotations

from typing import Any

from .models import BUSINESS_TABLES
from .models import OWNED_TABLES
from .models import PBC_KEY
from .runtime import claims_adjudication_healthcare_parse_document_instruction


def agent_skill_manifest() -> dict[str, Any]:
    skills = (
        {
            "name": f"{PBC_KEY}_guide_user",
            "scope": PBC_KEY,
            "description": "Explain intake, adjudication, denial, and appeal workflows.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_parse_document_instruction",
            "scope": PBC_KEY,
            "description": "Parse coverage memos and appeal packets into governed CRUD previews.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_governed_datastore_crud",
            "scope": PBC_KEY,
            "description": "Preview create, update, and delete plans for owned adjudication tables.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_review_release_evidence",
            "scope": PBC_KEY,
            "description": "Summarize runtime, test, and release evidence for the adjudication slice.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "stream_engine_picker_visible": False,
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "release_evidence_summary",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict[str, Any]:
    parsed = claims_adjudication_healthcare_parse_document_instruction(document, instruction)
    return {
        "ok": parsed["ok"],
        "pbc": PBC_KEY,
        "document_digest": parsed["document_digest"],
        "instruction": instruction,
        "candidate_tables": BUSINESS_TABLES,
        "target_table": parsed["target_table"],
        "action": parsed["action"],
        "crud_preview": {
            "operation": parsed["action"],
            "table": parsed["target_table"],
            "structured_fields": parsed["extracted_fields"],
            "event_contract": "AppGen-X",
        },
        "requires_human_confirmation": parsed["requires_human_confirmation"],
        "side_effects": (),
    }


def datastore_crud_plan(
    action: str,
    table: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    target = table or BUSINESS_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {
            "ok": False,
            "reason": "foreign_table_rejected",
            "table": target,
            "side_effects": (),
        }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "allowed_tables": OWNED_TABLES,
        "requires_confirmation": action in ("create", "update", "delete"),
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def document_instruction_crud_support(document: str, instruction: str) -> dict[str, Any]:
    plan = document_instruction_plan(document, instruction)
    crud = datastore_crud_plan(plan["action"], table=plan["target_table"], payload=plan["crud_preview"]["structured_fields"])
    return {
        "ok": plan["ok"] and crud["ok"],
        "pbc": PBC_KEY,
        "document_plan": plan,
        "crud_plan": crud,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict[str, Any]:
    from .standalone import single_pbc_app_contract
    namespace = f"{PBC_KEY}_skills"
    app = single_pbc_app_contract()
    return {
        "ok": True and app["ok"],
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "standalone_app": app["dsl_exposure"],
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    support = document_instruction_crud_support(
        "coverage memo",
        "Create a new benefit rule for procedure 99213 and update the threshold.",
    )
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and support["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
