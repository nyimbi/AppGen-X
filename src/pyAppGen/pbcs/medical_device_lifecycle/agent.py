"""AI agent and chatbot skill contract for the Medical Device Lifecycle PBC."""

from __future__ import annotations

import hashlib

from .runtime import MEDICAL_DEVICE_LIFECYCLE_OWNED_TABLES

PBC_KEY = "medical_device_lifecycle"
OWNED_TABLES = MEDICAL_DEVICE_LIFECYCLE_OWNED_TABLES
AGENT_NAME = "MedicalDeviceLifecycleAgent"
_DOCUMENT_ACTIONS = ("summarize", "extract_fields", "validate_against_rules", "draft_crud_plan")
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.recall_containment_guidance",
    f"{PBC_KEY}.workbench_navigation",
)


def _owned_tables() -> tuple[str, ...]:
    return tuple(table for table in OWNED_TABLES if table.startswith(f"{PBC_KEY}_"))


def _standalone_routes() -> tuple[dict, ...]:
    from .standalone import standalone_route_contracts

    return standalone_route_contracts()["contracts"]


def standalone_agent_workspace_contract() -> dict:
    """Return the package-local assistant surface for the standalone one-PBC app."""
    from .forms import medical_device_lifecycle_form_catalog
    from .wizards import medical_device_lifecycle_wizard_catalog

    forms = medical_device_lifecycle_form_catalog()
    wizards = medical_device_lifecycle_wizard_catalog()
    routes = _standalone_routes()
    return {
        "format": "appgen.medical-device-lifecycle-standalone-agent-workspace.v1",
        "ok": forms["ok"] and wizards["ok"] and bool(routes),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "forms": forms["form_ids"],
        "wizards": wizards["wizard_ids"],
        "routes": tuple(f"{item['method']} {item['path']}" for item in routes),
        "tables": _owned_tables(),
        "side_effects": (),
    }


def agent_skill_manifest() -> dict:
    """Return the skills this PBC contributes to the composed application assistant."""
    return {
        "ok": bool(_SKILL_NAMES) and bool(_owned_tables()),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": skill,
                "scope": PBC_KEY,
                "owned_tables": _owned_tables(),
                "allowed_crud_actions": _CRUD_ACTIONS,
                "document_actions": _DOCUMENT_ACTIONS,
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for skill in _SKILL_NAMES
        ),
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict:
    """Return the professional help/chatbot surface contract for this PBC."""
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
            "mutation_preview",
            "workbench_navigation",
        ),
        "professional_controls": (
            "citation_required_for_regulatory_text",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "patient_safety_gate",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document=None, instruction=None) -> dict:
    """Plan document/instruction handling without mutating state."""
    from .forms import medical_device_lifecycle_form_catalog
    from .wizards import medical_device_lifecycle_wizard_catalog

    document_text = str(document or "")
    instruction_text = str(instruction or "")
    combined = f"{document_text} {instruction_text}".lower()
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest()

    keyword_to_tables = (
        (("recall", "field safety notice", "quarantine"), ("medical_device_lifecycle_recall_notice", "medical_device_lifecycle_medical_device")),
        (("calibration", "out of tolerance"), ("medical_device_lifecycle_calibration", "medical_device_lifecycle_medical_device")),
        (("maintenance", "repair", "vendor"), ("medical_device_lifecycle_maintenance_event", "medical_device_lifecycle_medical_device")),
        (("assign", "patient", "room", "implant"), ("medical_device_lifecycle_device_assignment", "medical_device_lifecycle_medical_device")),
        (("usage", "trace", "operator"), ("medical_device_lifecycle_usage_trace",)),
        (("evidence", "certificate", "manual", "service record"), ("medical_device_lifecycle_regulatory_evidence",)),
    )
    candidate_tables = next(
        (tables for keywords, tables in keyword_to_tables if any(keyword in combined for keyword in keywords)),
        ("medical_device_lifecycle_medical_device",),
    )

    wizard_catalog = medical_device_lifecycle_wizard_catalog()["wizards"]
    wizard_candidates = tuple(
        wizard["wizard_id"]
        for wizard in wizard_catalog
        if any(keyword in combined for keyword in wizard.get("keywords", ()))
    ) or ("assistant_change_preview",)

    routes = _standalone_routes()
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in routes
        if item["operation_kind"] == "command"
        and (
            item["table"] in candidate_tables
            or item.get("wizard") in wizard_candidates
            or item["operation"].replace("_", " ") in combined
        )
    )

    forms = medical_device_lifecycle_form_catalog()["forms"]
    form_candidates = tuple(
        form["form_id"]
        for form in forms
        if any(table in form["owned_tables"] for table in candidate_tables)
    ) or ("assistant_document_intake",)

    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": candidate_tables,
        "wizard_candidates": wizard_candidates,
        "form_candidates": form_candidates,
        "route_candidates": route_candidates,
        "requires_human_confirmation": True,
        "preview_only": True,
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None) -> dict:
    """Plan governed CRUD against owned tables only."""
    from .controls import medical_device_lifecycle_mutation_preview
    from .forms import medical_device_lifecycle_form_catalog

    normalized_action = str(action).lower()
    selected_table = table or _owned_tables()[0]
    if selected_table in {
        "medical_device",
        "device_assignment",
        "calibration",
        "maintenance_event",
        "recall_notice",
        "usage_trace",
        "regulatory_evidence",
    }:
        selected_table = f"{PBC_KEY}_{selected_table}"
    if selected_table not in _owned_tables():
        return {"ok": False, "reason": "foreign_table_rejected", "table": selected_table, "side_effects": ()}

    routes = _standalone_routes()
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in routes
        if item["table"] == selected_table
        and ((normalized_action == "read" and item["operation_kind"] == "query") or (normalized_action != "read" and item["operation_kind"] == "command"))
    )
    forms = medical_device_lifecycle_form_catalog()["forms"]
    form_candidates = tuple(form["form_id"] for form in forms if selected_table in form["owned_tables"])
    wizard_candidates = tuple(
        dict.fromkeys(item["wizard"] for item in routes if item["table"] == selected_table and item.get("wizard"))
    )
    preview = medical_device_lifecycle_mutation_preview(normalized_action, selected_table, payload)
    return {
        "ok": preview["ok"] and normalized_action in _CRUD_ACTIONS,
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "route_candidates": route_candidates,
        "form_candidates": form_candidates,
        "wizard_candidates": wizard_candidates,
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "preview": preview,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    """Return the package contribution to the application's single assistant."""
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
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan("field safety notice", "launch a recall and attach evidence")
    read_plan = datastore_crud_plan("read", "medical_device_lifecycle_medical_device")
    create_plan = datastore_crud_plan("create", "medical_device_lifecycle_recall_notice", {"status": "open"})
    contribution = composed_agent_contribution()
    workspace = standalone_agent_workspace_contract()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and contribution["ok"]
        and workspace["ok"]
        and bool(document["wizard_candidates"])
        and bool(create_plan["route_candidates"])
        and not create_plan["stream_engine_picker_visible"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "contribution": contribution,
        "workspace": workspace,
        "side_effects": (),
    }
