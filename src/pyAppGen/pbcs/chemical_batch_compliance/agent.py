"""Assistant and document-instruction contracts for chemical_batch_compliance."""

from __future__ import annotations

from .slice_app import BUSINESS_TABLES
from .slice_app import COMMAND_METHODS
from .slice_app import GOVERNED_MODEL_TABLE
from .slice_app import PBC_KEY
from .slice_app import parse_document_instruction


def agent_skill_manifest() -> dict:
    mutation_skills = (
        f"{PBC_KEY}_guide_formula_release",
        f"{PBC_KEY}_triage_quality_hold",
        f"{PBC_KEY}_assemble_submission",
        f"{PBC_KEY}_manage_document_instruction",
    )
    skills = tuple(
        {
            "name": name,
            "scope": PBC_KEY,
            "description": name.replace("_", " "),
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for name in mutation_skills
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "command_operations": COMMAND_METHODS, "side_effects": ()}


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "release_gate_explanation",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    return parse_document_instruction(document, instruction)


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or GOVERNED_MODEL_TABLE
    if target not in BUSINESS_TABLES:
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


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "domain_focus": "controlled formulas, batch review, quality holds, and submission dossiers",
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("Formula Code: CBR-77", "update the formula")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
