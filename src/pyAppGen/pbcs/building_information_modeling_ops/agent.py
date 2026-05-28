"""Agent-help surfaces for the single-PBC BIM operations app."""
from __future__ import annotations

import hashlib

PBC_KEY = "building_information_modeling_ops"
OWNED_TABLES = (
    f"{PBC_KEY}_bim_model",
    f"{PBC_KEY}_model_version",
    f"{PBC_KEY}_clash_issue",
    f"{PBC_KEY}_asset_object",
    f"{PBC_KEY}_handover_package",
    f"{PBC_KEY}_model_review",
    f"{PBC_KEY}_digital_twin_link",
    f"{PBC_KEY}_building_information_modeling_ops_policy_rule",
    f"{PBC_KEY}_building_information_modeling_ops_runtime_parameter",
    f"{PBC_KEY}_building_information_modeling_ops_schema_extension",
    f"{PBC_KEY}_building_information_modeling_ops_control_assertion",
    f"{PBC_KEY}_building_information_modeling_ops_governed_model",
    f"{PBC_KEY}_appgen_outbox_event",
    f"{PBC_KEY}_appgen_inbox_event",
    f"{PBC_KEY}_appgen_dead_letter_event",
)


def agent_help_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "help_topics": (
            "coordinate_baseline_setup",
            "model_package_registration",
            "federation_assembly",
            "release_evidence_review",
            "control_explanations",
        ),
        "assistant_flows": (
            "guide_coordinate_wizard",
            "explain_blocked_package",
            "draft_release_readiness_summary",
        ),
        "single_pbc_app": True,
        "side_effects": (),
    }


def agent_skill_manifest() -> dict:
    skills = tuple(
        {
            "name": name,
            "scope": PBC_KEY,
            "description": f"{name} for the single-PBC BIM federation app",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for name in (
            f"{PBC_KEY}_guide_user",
            f"{PBC_KEY}_read_records",
            f"{PBC_KEY}_create_record",
            f"{PBC_KEY}_update_record",
            f"{PBC_KEY}_explain_controls",
        )
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
            "wizard_guidance",
            "control_explanations",
        ),
        "single_pbc_app": True,
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": hashlib.sha256(document.encode("utf-8")).hexdigest(),
        "instruction": instruction,
        "candidate_tables": OWNED_TABLES[:3],
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "recommended_wizard": "federation_setup_wizard",
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


def assistant_help(topic: str | None = None) -> dict:
    manifest = agent_help_manifest()
    selected = topic or manifest["help_topics"][0]
    return {
        "ok": selected in manifest["help_topics"],
        "topic": selected,
        "guidance": (
            "Use the project coordinate baseline form first.",
            "Register each model package with checksum, discipline, and issue purpose.",
            "Run the federation setup wizard to validate controls before approval.",
        ),
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "help": agent_help_manifest()["help_topics"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("doc", "create")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"]
        and assistant_help()["ok"],
        "side_effects": (),
    }
