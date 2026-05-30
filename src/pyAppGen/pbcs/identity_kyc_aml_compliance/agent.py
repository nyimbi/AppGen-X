"""Agent and chatbot skills for the identity KYC / AML slice."""

from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS
from .runtime import (
    IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES,
    PBC_KEY,
    identity_kyc_aml_compliance_parse_document_instruction,
)


def agent_skill_manifest():
    skills = tuple(
        {
            "name": f"{PBC_KEY}_skills.{name}",
            "scope": PBC_KEY,
            "description": f"Governed {name} workflow for {PBC_KEY}",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for name in DOMAIN_OPERATIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract():
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
            "screening_resolution_guidance",
            "edd_packet_preparation",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document, instruction):
    plan = identity_kyc_aml_compliance_parse_document_instruction(document, instruction)
    return {
        "ok": plan["ok"],
        "pbc": PBC_KEY,
        "document_digest": plan["document_digest"],
        "instruction": instruction,
        "candidate_tables": plan["candidate_tables"],
        "candidate_operations": plan["candidate_operations"],
        "requires_human_confirmation": plan["requires_human_confirmation"],
        "crud_preview": {"operation": plan["candidate_operations"][0], "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES[0]
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


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_screening"),
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("passport scan", "screen and onboard")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
