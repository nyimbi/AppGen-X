from . import operations_engine as engine

PBC_KEY = engine.PBC_KEY
OWNED_TABLES = engine.OWNED_TABLES


def agent_skill_manifest():
    skills = tuple(
        {
            "name": skill["name"],
            "scope": PBC_KEY,
            "description": skill["purpose"],
            "requires_confirmation": True,
            "requires_confirmation_for_mutation": True,
            "confirmation_gate": "human_required",
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for skill in engine.AGENT_SKILLS
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": ("task_guidance", "document_instruction_intake", "governed_datastore_crud", "mutation_preview", "sample_interpretation", "incident_narration"),
        "confirmation_gate": "all_skills_require_human_confirmation",
        "side_effects": (),
    }


def document_instruction_plan(document, instruction):
    return engine.parse_document_instruction(document, instruction)


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
        "requires_confirmation": True,
        "confirmation_gate": "human_required",
        "event_contract": "AppGen-X",
        "crud_mode": "governed_datastore_crud",
        "side_effects": (),
    }


def sample_interpretation_preview(state=None, sample_code="SAMPLE-1"):
    return engine.build_sample_interpretation_preview(state or engine.empty_state(), sample_code)


def incident_narration_preview(state=None, incident_code="INC-1"):
    return engine.build_incident_narrative_preview(state or engine.empty_state(), incident_code)


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {"ok": True, "pbc": PBC_KEY, "single_agent_skill_namespace": namespace, "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"), "side_effects": ()}


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"] and document_instruction_plan("doc", "create governed_datastore_crud incident")['ok'] and datastore_crud_plan("create")['ok'] and datastore_crud_plan("update", table="foreign_table")['ok'] is False and composed_agent_contribution()['ok'],
        "side_effects": (),
    }
