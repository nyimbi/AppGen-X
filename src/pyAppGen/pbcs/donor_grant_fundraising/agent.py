from __future__ import annotations

from hashlib import sha256

from .fundraising_app import OWNED_TABLES as APP_OWNED_TABLES, document_instruction_mutation_plan

PBC_KEY = "donor_grant_fundraising"
OWNED_TABLES = APP_OWNED_TABLES + (
    "donor_grant_fundraising_policy_rule",
    "donor_grant_fundraising_runtime_parameter",
    "donor_grant_fundraising_schema_extension",
    "donor_grant_fundraising_control_assertion",
    "donor_grant_fundraising_governed_model",
    "donor_grant_fundraising_appgen_outbox_event",
    "donor_grant_fundraising_appgen_inbox_event",
    "donor_grant_fundraising_appgen_dead_letter_event",
)


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_guide_user",
            "scope": PBC_KEY,
            "description": "Guide fundraising operators through donor, grant, and stewardship actions",
            "requires_confirmation_for_mutation": False,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_proposal_support",
            "scope": PBC_KEY,
            "description": "Summarize fit, missing proposal artifacts, reviewer blockers, and submission readiness",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_stewardship_drafting",
            "scope": PBC_KEY,
            "description": "Draft acknowledgements, impact updates, and renewal prompts using owned fundraising records",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_mutation_preview",
            "scope": PBC_KEY,
            "description": "Show a governed owned-table mutation preview before any write is approved",
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
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "proposal_support",
            "stewardship_drafting",
            "briefing_packet_guidance",
        ),
        "side_effects": (),
    }


def _stable_digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def document_instruction_plan(document: str, instruction: str) -> dict:
    domain_plan = document_instruction_mutation_plan(document, instruction)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _stable_digest(document),
        "instruction": instruction,
        "candidate_tables": (domain_plan["target_table"],),
        "requires_human_confirmation": True,
        "requires_citations": True,
        "domain_plan": domain_plan,
        "crud_preview": {
            "operation": domain_plan["proposed_operation"],
            "target_table": domain_plan["target_table"],
            "event_contract": "AppGen-X",
        },
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
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


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_briefings"),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("board briefing", "prepare packet")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
