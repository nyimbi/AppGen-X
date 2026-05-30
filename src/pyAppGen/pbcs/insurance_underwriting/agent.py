"""AI agent and chatbot contracts for insurance underwriting."""

from __future__ import annotations

import hashlib

from .models import OWNED_TABLES, standalone_model_contract
from .routes import standalone_route_contracts
from .services import service_operation_manifest, standalone_service_operation_contracts
from .ui import insurance_underwriting_form_contracts, insurance_underwriting_wizard_contracts


PBC_KEY = "insurance_underwriting"
AGENT_NAME = "InsuranceUnderwritingAgent"
DOCUMENT_ACTIONS = (
    "summarize_submission",
    "extract_underwriting_facts",
    "draft_referral_memo",
    "compare_quote_scenarios",
    "build_bind_readiness_checklist",
)
CRUD_ACTIONS = ("create", "read", "update", "delete")
SKILL_NAMES = (
    f"{PBC_KEY}.submission_summary",
    f"{PBC_KEY}.risk_profile_explainer",
    f"{PBC_KEY}.referral_memo_draft",
    f"{PBC_KEY}.quote_scenario_compare",
    f"{PBC_KEY}.bind_readiness_review",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_datastore_crud",
    f"{PBC_KEY}.workbench_navigation",
)


def _stable_hash(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def standalone_agent_workspace_contract() -> dict:
    forms = insurance_underwriting_form_contracts()
    wizards = insurance_underwriting_wizard_contracts()
    routes = standalone_route_contracts()
    model = standalone_model_contract()
    return {
        "format": "appgen.insurance-underwriting-standalone-agent-workspace.v1",
        "ok": forms["ok"] and wizards["ok"] and routes["ok"] and model["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "forms": tuple(item["key"] for item in forms["contracts"]),
        "wizards": tuple(item["key"] for item in wizards["contracts"]),
        "routes": routes["routes"],
        "tables": model["table_keys"],
        "side_effects": (),
    }


def agent_skill_manifest() -> dict:
    service_manifest = service_operation_manifest()
    return {
        "ok": service_manifest["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": name,
                "scope": PBC_KEY,
                "owned_tables": OWNED_TABLES,
                "document_actions": DOCUMENT_ACTIONS,
                "allowed_crud_actions": CRUD_ACTIONS,
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for name in SKILL_NAMES
        ),
        "query_operations": service_manifest["query_operations"],
        "command_operations": service_manifest["command_operations"],
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_and_instruction_intake",
            "governed_datastore_crud",
            "policy_and_permission_explanation",
            "workbench_navigation",
        ),
        "professional_controls": (
            "citations_required_for_document_facts",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "audit_event_plan",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str | None = None, instructions: str | None = None) -> dict:
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    combined = f"{document_text} {instruction_text}".lower()
    wizard_manifest = insurance_underwriting_wizard_contracts()["contracts"]
    standalone_operations = standalone_service_operation_contracts()["contracts"]
    wizard_candidates = tuple(
        item["key"] for item in wizard_manifest if any(keyword in combined for keyword in item["keywords"])
    ) or ("AssistantDocumentIntakeWizard",)
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in standalone_operations
        if item["operation_kind"] == "command"
        and (
            item.get("wizard") in wizard_candidates
            or item["operation"].replace("_", " ") in combined
            or item["table"].split("_")[-1] in combined
        )
    )
    form_candidates = tuple(
        form["key"]
        for form in insurance_underwriting_form_contracts()["contracts"]
        if form["operation"] in tuple(
            item["operation"]
            for item in standalone_operations
            if f"{item['method']} {item['path']}" in route_candidates
        )
    ) or ("EventInboxForm",)
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": _stable_hash((document_text, instruction_text)),
        "document_actions": DOCUMENT_ACTIONS,
        "candidate_tables": OWNED_TABLES,
        "candidate_operations": service_operation_manifest()["command_operations"] + service_operation_manifest()["query_operations"],
        "wizard_candidates": wizard_candidates,
        "form_candidates": form_candidates,
        "route_candidates": route_candidates,
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action: str = "read", table: str | None = None, payload: dict | None = None) -> dict:
    normalized_action = str(action).lower()
    selected_table = table or OWNED_TABLES[0]
    standalone_operations = standalone_service_operation_contracts()["contracts"]
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in standalone_operations
        if item["table"] == selected_table
        and ((normalized_action == "read" and item["operation_kind"] == "query") or (normalized_action != "read" and item["operation_kind"] == "command"))
    )
    wizard_candidates = tuple(
        dict.fromkeys(item["wizard"] for item in standalone_operations if item["table"] == selected_table and item.get("wizard"))
    )
    form_candidates = tuple(
        form["key"]
        for form in insurance_underwriting_form_contracts()["contracts"]
        if form["table"] == selected_table
    )
    return {
        "ok": normalized_action in CRUD_ACTIONS and selected_table in OWNED_TABLES,
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "route_candidates": route_candidates,
        "wizard_candidates": wizard_candidates,
        "form_candidates": form_candidates,
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
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


def smoke_test() -> dict:
    document = document_instruction_plan(
        "loss run and application",
        "create submission, compare quote scenarios, and check bind readiness",
    )
    crud = datastore_crud_plan("create", "insurance_underwriting_underwriting_submission", {"submission_id": "sub-1"})
    contribution = composed_agent_contribution()
    return {
        "ok": agent_skill_manifest()["ok"] and document["ok"] and crud["ok"] and contribution["ok"],
        "document": document,
        "crud": crud,
        "contribution": contribution,
        "side_effects": (),
    }
