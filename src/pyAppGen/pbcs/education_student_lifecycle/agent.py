from hashlib import sha256

from .student_lifecycle_app import OWNED_TABLES as APP_OWNED_TABLES, document_instruction_mutation_plan

PBC_KEY = "education_student_lifecycle"
OWNED_TABLES = APP_OWNED_TABLES + (
    "education_student_lifecycle_education_student_lifecycle_policy_rule",
    "education_student_lifecycle_education_student_lifecycle_runtime_parameter",
    "education_student_lifecycle_education_student_lifecycle_schema_extension",
    "education_student_lifecycle_education_student_lifecycle_control_assertion",
    "education_student_lifecycle_education_student_lifecycle_governed_model",
    "education_student_lifecycle_appgen_outbox_event",
    "education_student_lifecycle_appgen_inbox_event",
    "education_student_lifecycle_appgen_dead_letter_event",
)


def agent_skill_manifest():
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
            f"{PBC_KEY}_degree_audit_explainer",
            f"{PBC_KEY}_registration_blocker_summary",
            f"{PBC_KEY}_graduation_readiness",
        )
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": ("task_guidance", "document_instruction_intake", "governed_datastore_crud", "mutation_preview", "degree_audit_explanation"),
        "side_effects": (),
    }


def _stable_digest(value):
    return sha256(repr(value).encode("utf-8")).hexdigest()


def document_instruction_plan(document, instruction):
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
        "crud_preview": {"operation": domain_plan["proposed_operation"], "target_table": domain_plan["target_table"], "event_contract": "AppGen-X"},
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


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {"ok": True, "pbc": PBC_KEY, "single_agent_skill_namespace": namespace, "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"), "side_effects": ()}


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("degree audit memo", "prepare graduation review")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
