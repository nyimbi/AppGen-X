"""AI agent and CRUD planning surface for standalone master_data_governance."""
from __future__ import annotations

from .routes import standalone_route_contracts
from .services import service_operation_manifest
from .standalone import AGENT_NAME
from .standalone import CRUD_ACTIONS
from .standalone import FORM_DEFINITIONS
from .standalone import WIZARD_DEFINITIONS
from .standalone import build_datastore_crud_plan
from .standalone import build_document_instruction_plan
from .standalone import master_data_governance_standalone_app_contract
from .standalone import standalone_model_contract

PBC_KEY = "master_data_governance"
SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_datastore_crud",
    f"{PBC_KEY}.workbench_navigation",
    f"{PBC_KEY}.merge_and_survivorship_planning",
    f"{PBC_KEY}.audit_evidence_preview",
)



def _owned_tables() -> tuple[str, ...]:
    return tuple(standalone_model_contract()["table_keys"])



def standalone_agent_workspace_contract():
    routes = standalone_route_contracts()
    app = master_data_governance_standalone_app_contract()
    return {
        "format": f"appgen.{PBC_KEY}.standalone-agent-workspace.v1",
        "ok": routes["ok"] and app["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "forms": tuple(item["key"] for item in FORM_DEFINITIONS),
        "wizards": tuple(item["key"] for item in WIZARD_DEFINITIONS),
        "routes": routes["routes"],
        "tables": _owned_tables(),
        "controls": app["ui"]["controls"],
        "side_effects": (),
    }



def agent_skill_manifest():
    manifest = service_operation_manifest()
    return {
        "ok": bool(SKILL_NAMES) and bool(_owned_tables()) and manifest["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": skill,
                "scope": PBC_KEY,
                "owned_tables": _owned_tables(),
                "allowed_crud_actions": CRUD_ACTIONS,
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for skill in SKILL_NAMES
        ),
        "query_operations": manifest["query_operations"],
        "command_operations": manifest["command_operations"],
        "side_effects": (),
    }



def chatbot_interface_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "merge_and_survivorship_planning",
            "release_evidence_navigation",
        ),
        "professional_controls": (
            "citation_required_for_document_facts",
            "owned_table_boundary_check",
            "mutation_preview_before_commit",
            "policy_approval_before_publish",
            "audit_proof_before_release",
        ),
        "side_effects": (),
    }



def document_instruction_plan(document=None, instructions=None):
    return build_document_instruction_plan(document, instructions)



def datastore_crud_plan(action="read", table=None, payload=None):
    return build_datastore_crud_plan(action, table, payload)



def composed_agent_contribution():
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    workspace = standalone_agent_workspace_contract()
    return {
        "ok": skills["ok"] and chatbot["ok"] and workspace["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (f"{PBC_KEY}_skills", f"{PBC_KEY}_documents", f"{PBC_KEY}_crud"),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "standalone_workspace": workspace,
        "side_effects": (),
    }



def smoke_test():
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        "customer master data merge packet",
        "match duplicates, apply survivorship, publish golden record, and capture audit proof",
    )
    crud = datastore_crud_plan("create", _owned_tables()[2], {"golden_code": "GOLD-SMOKE"})
    workspace = standalone_agent_workspace_contract()
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"] and chatbot["ok"] and document["ok"] and crud["ok"] and workspace["ok"] and contribution["ok"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "crud": crud,
        "workspace": workspace,
        "contribution": contribution,
        "side_effects": (),
    }
