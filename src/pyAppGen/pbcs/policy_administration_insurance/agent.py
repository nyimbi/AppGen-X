"""AI agent and document-planning contract for the policy_administration_insurance PBC."""

from __future__ import annotations

import hashlib

from .runtime import POLICY_ADMINISTRATION_INSURANCE_OWNED_TABLES
from .services import service_operation_manifest
from .ui import (
    policy_administration_insurance_control_catalog,
    policy_administration_insurance_form_contracts,
    policy_administration_insurance_wizard_contracts,
)

PBC_KEY = "policy_administration_insurance"
AGENT_NAME = "PolicyAdministrationInsuranceAgent"
OWNED_TABLES = POLICY_ADMINISTRATION_INSURANCE_OWNED_TABLES
_DOCUMENT_ACTIONS = (
    "summarize_policy_packet",
    "extract_policy_fields",
    "validate_notice_readiness",
    "draft_governed_crud_plan",
)
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.notice_compliance_review",
    f"{PBC_KEY}.workbench_navigation",
)


def _query_operations() -> tuple[str, ...]:
    return tuple(service_operation_manifest().get("query_operations", ()))


def _command_operations() -> tuple[str, ...]:
    return tuple(service_operation_manifest().get("command_operations", ()))


def standalone_agent_workspace_contract() -> dict:
    forms = policy_administration_insurance_form_contracts()
    wizards = policy_administration_insurance_wizard_contracts()
    controls = policy_administration_insurance_control_catalog()
    return {
        "format": "appgen.policy-administration-insurance-standalone-agent-workspace.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "forms": tuple(item["key"] for item in forms["contracts"]),
        "wizards": tuple(item["key"] for item in wizards["contracts"]),
        "controls": tuple(item["key"] for item in controls["contracts"]),
        "workspace_actions": _command_operations() + _query_operations(),
        "tables": OWNED_TABLES,
        "side_effects": (),
    }


def agent_skill_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": skill,
                "scope": PBC_KEY,
                "owned_tables": OWNED_TABLES,
                "allowed_crud_actions": _CRUD_ACTIONS,
                "document_actions": _DOCUMENT_ACTIONS,
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for skill in _SKILL_NAMES
        ),
        "query_operations": _query_operations(),
        "command_operations": _command_operations(),
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
            "document_instruction_intake",
            "governed_datastore_crud",
            "policy_lifecycle_explanation",
            "workbench_navigation",
        ),
        "professional_controls": (
            "mutation_preview_before_commit",
            "notice_compliance_review_required",
            "owned_table_boundary_check",
            "human_confirmation_for_writes",
        ),
        "standalone_workspace": standalone_agent_workspace_contract(),
        "side_effects": (),
    }


def _wizard_candidates(text: str) -> tuple[str, ...]:
    candidates = tuple(
        wizard["key"]
        for wizard in policy_administration_insurance_wizard_contracts()["contracts"]
        if any(keyword in text for keyword in wizard.get("keywords", ()))
    )
    return candidates or ("PolicyDocumentAssemblyWizard",)


def _form_candidates(wizard_candidates: tuple[str, ...]) -> tuple[str, ...]:
    wizard_forms = {
        form_name
        for wizard in policy_administration_insurance_wizard_contracts()["contracts"]
        if wizard["key"] in wizard_candidates
        for form_name in wizard.get("forms", ())
    }
    forms = tuple(
        form["key"]
        for form in policy_administration_insurance_form_contracts()["contracts"]
        if form["key"] in wizard_forms
    )
    return forms or ("PolicyEventInboxForm",)


def document_instruction_plan(document=None, instruction=None) -> dict:
    document_text = str(document or "")
    instruction_text = str(instruction or "")
    combined = f"{document_text} {instruction_text}".lower()
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest()
    wizard_candidates = _wizard_candidates(combined)
    form_candidates = _form_candidates(wizard_candidates)
    operation_lookup = {
        form["key"]: form["operation"]
        for form in policy_administration_insurance_form_contracts()["contracts"]
    }
    service_method_candidates = tuple(
        dict.fromkeys(operation_lookup[form_key] for form_key in form_candidates if form_key in operation_lookup)
    ) or ("query_workbench",)
    control_candidates = tuple(
        control["key"]
        for control in policy_administration_insurance_control_catalog()["contracts"]
        if "document" in combined
        or "notice" in combined
        or control["key"] in ("PolicyEventConsole", "NoticeComplianceControl")
    )
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "instruction": instruction_text,
        "candidate_tables": OWNED_TABLES[:8],
        "candidate_operations": _command_operations() + _query_operations(),
        "wizard_candidates": wizard_candidates,
        "form_candidates": form_candidates,
        "control_candidates": control_candidates or ("PolicyEventConsole",),
        "service_method_candidates": service_method_candidates,
        "requires_human_confirmation": True,
        "crud_preview": {
            "operation": "create",
            "event_contract": "AppGen-X",
            "recommended_form": form_candidates[0],
        },
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None) -> dict:
    normalized_action = str(action).lower()
    selected_table = table or OWNED_TABLES[0]
    if selected_table not in OWNED_TABLES:
        return {
            "ok": False,
            "reason": "foreign_table_rejected",
            "table": selected_table,
            "side_effects": (),
        }
    form_candidates = tuple(
        form["key"]
        for form in policy_administration_insurance_form_contracts()["contracts"]
        if form["table"] == selected_table
    )
    wizard_candidates = tuple(
        wizard["key"]
        for wizard in policy_administration_insurance_wizard_contracts()["contracts"]
        if any(form_name in form_candidates for form_name in wizard.get("forms", ()))
    )
    candidate_operations = _query_operations() if normalized_action == "read" else _command_operations()
    operation_lookup = {
        form["key"]: form["operation"]
        for form in policy_administration_insurance_form_contracts()["contracts"]
    }
    service_method_candidates = tuple(
        dict.fromkeys(operation_lookup[form_key] for form_key in form_candidates if form_key in operation_lookup)
    ) or candidate_operations[:1]
    return {
        "ok": normalized_action in _CRUD_ACTIONS and bool(candidate_operations),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": OWNED_TABLES,
        "candidate_operations": candidate_operations,
        "service_method_candidates": service_method_candidates,
        "form_candidates": form_candidates,
        "wizard_candidates": tuple(dict.fromkeys(wizard_candidates)),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    return {
        "ok": skills["ok"] and chatbot["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (f"{PBC_KEY}_skills", f"{PBC_KEY}_documents", f"{PBC_KEY}_crud"),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "standalone_workspace": standalone_agent_workspace_contract(),
        "side_effects": (),
    }


def smoke_test() -> dict:
    document = document_instruction_plan(
        "endorsement request packet",
        "review endorsement and prepare cancellation notice fallback",
    )
    create_plan = datastore_crud_plan(
        "create",
        "policy_administration_insurance_endorsement",
        {"endorsement_id": "endorsement-smoke"},
    )
    read_plan = datastore_crud_plan("read")
    contribution = composed_agent_contribution()
    workspace = standalone_agent_workspace_contract()
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document["ok"]
        and bool(document["wizard_candidates"])
        and bool(document["service_method_candidates"])
        and create_plan["ok"]
        and read_plan["ok"]
        and contribution["ok"]
        and workspace["ok"],
        "document": document,
        "create_plan": create_plan,
        "read_plan": read_plan,
        "contribution": contribution,
        "workspace": workspace,
        "side_effects": (),
    }
