"""Agent and document-instruction support for electronic health records core."""
from __future__ import annotations

from hashlib import sha256

from .ehr_core_app import document_instruction_mutation_plan

PBC_KEY = "electronic_health_records_core"
OWNED_TABLES = (
    "electronic_health_records_core_patient_chart",
    "electronic_health_records_core_clinical_encounter",
    "electronic_health_records_core_clinical_order",
    "electronic_health_records_core_observation",
    "electronic_health_records_core_allergy",
    "electronic_health_records_core_medication_list",
    "electronic_health_records_core_care_note",
    "electronic_health_records_core_electronic_health_records_core_policy_rule",
    "electronic_health_records_core_electronic_health_records_core_runtime_parameter",
    "electronic_health_records_core_electronic_health_records_core_schema_extension",
    "electronic_health_records_core_electronic_health_records_core_control_assertion",
    "electronic_health_records_core_electronic_health_records_core_governed_model",
    "electronic_health_records_core_appgen_outbox_event",
    "electronic_health_records_core_appgen_inbox_event",
    "electronic_health_records_core_appgen_dead_letter_event",
)


def agent_skill_manifest() -> dict:
    skills = tuple(
        {
            "name": name,
            "scope": PBC_KEY,
            "description": f"{name} for {PBC_KEY}",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for name in (
            f"{PBC_KEY}_guide_user",
            f"{PBC_KEY}_read_records",
            f"{PBC_KEY}_create_record",
            f"{PBC_KEY}_update_record",
            f"{PBC_KEY}_summarize_chart",
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
            "summary_redaction_preview",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    domain_plan = document_instruction_mutation_plan(document, instruction)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": sha256(str(document).encode("utf-8")).hexdigest(),
        "instruction": instruction,
        "candidate_tables": OWNED_TABLES[:5],
        "requires_human_confirmation": True,
        "domain_plan": domain_plan,
        "crud_preview": {
            "operation": domain_plan["proposed_action"],
            "table": domain_plan["target_table"],
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
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_summary"),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("doc", "acknowledge critical potassium result")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
