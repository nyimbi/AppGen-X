"""Assistant planning surface for the standalone aviation slice."""
from __future__ import annotations

import hashlib

from .models import BUSINESS_TABLES, OWNED_TABLES
from .permissions import OPERATION_PERMISSIONS, permission_manifest
from .workflows import document_instruction_workflow_contract, release_to_service_workflow_contract, workflow_catalog

PBC_KEY = "aviation_maintenance_repair"
KEYWORD_TARGETS = (
    ("work card", "record_work_card", f"{PBC_KEY}_work_card"),
    ("workcard", "record_work_card", f"{PBC_KEY}_work_card"),
    ("component", "record_component", f"{PBC_KEY}_component"),
    ("aircraft", "record_aircraft", f"{PBC_KEY}_aircraft"),
    ("defect", "record_deferred_defect", f"{PBC_KEY}_deferred_defect"),
    ("directive", "record_airworthiness_directive", f"{PBC_KEY}_airworthiness_directive"),
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()[:16]


def _action_from_instruction(instruction: str) -> str:
    lowered = instruction.lower()
    if any(word in lowered for word in ("update", "revise", "change", "correct")):
        return "update"
    if any(word in lowered for word in ("delete", "remove", "cancel")):
        return "delete"
    return "create"


def _candidate_mutations(instruction: str) -> tuple[dict, ...]:
    lowered = instruction.lower()
    mutations = []
    for keyword, operation, table in KEYWORD_TARGETS:
        if keyword in lowered:
            mutations.append(
                {
                    "operation": operation,
                    "table": table,
                    "action": _action_from_instruction(lowered),
                    "required_permission": OPERATION_PERMISSIONS.get(operation, f"{PBC_KEY}.update"),
                }
            )
    if not mutations:
        mutations.append(
            {
                "operation": "record_aircraft",
                "table": BUSINESS_TABLES[0],
                "action": _action_from_instruction(lowered),
                "required_permission": OPERATION_PERMISSIONS["record_aircraft"],
            }
        )
    return tuple(mutations)


def agent_skill_manifest():
    skills = (
        {
            "name": f"{PBC_KEY}_preview_document_instruction",
            "scope": PBC_KEY,
            "description": "Preview governed CRUD mutations from maintenance documents or instructions.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_plan_release_to_service",
            "scope": PBC_KEY,
            "description": "Preview release readiness, blockers, and the next release workflow action.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_explain_release_blockers",
            "scope": PBC_KEY,
            "description": "Summarize blocked release evidence for a human maintainer or certifier.",
            "requires_confirmation_for_mutation": False,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
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
            "release_to_service_evidence_preview",
            "certifier_guardrails",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document, instruction, context=None):
    instruction = str(instruction or "")
    lowered = instruction.lower()
    mutations = _candidate_mutations(instruction)
    release_hint = any(word in lowered for word in ("release", "signoff", "airworthy", "return to service"))
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest((document, instruction, context)),
        "instruction": instruction,
        "candidate_tables": tuple(dict.fromkeys(mutation["table"] for mutation in mutations)),
        "candidate_mutations": mutations,
        "requires_human_confirmation": True,
        "crud_preview": {
            "operations": tuple(mutation["operation"] for mutation in mutations),
            "event_contract": "AppGen-X",
        },
        "workflow": document_instruction_workflow_contract(),
        "release_to_service_preview": {
            "suggested": release_hint,
            "workflow": release_to_service_workflow_contract(),
            "assistant_can_certify": False,
            "human_certifier_required": True,
        }
        if release_hint
        else None,
        "context": dict(context or {}),
        "side_effects": (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or BUSINESS_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_") or target not in OWNED_TABLES:
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    permission = {
        "create": f"{PBC_KEY}.create",
        "update": f"{PBC_KEY}.update",
        "delete": f"{PBC_KEY}.admin",
        "read": f"{PBC_KEY}.read",
    }.get(action, f"{PBC_KEY}.update")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "required_permission": permission,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def assistant_planning_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": permission_manifest()["operation_permissions"],
        "workflows": workflow_catalog()["workflows"],
        "guardrails": {
            "assistant_can_certify": False,
            "human_confirmation_required_for_mutations": True,
            "owned_tables_only": True,
        },
        "side_effects": (),
    }


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_release_to_service"),
        "side_effects": (),
    }


def smoke_test():
    plan = document_instruction_plan("scan", "Create work card release signoff package", {"tail_number": "5Y-ABC"})
    crud = datastore_crud_plan("create")
    return {
        "ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"] and plan["ok"] and crud["ok"] and datastore_crud_plan("update", table="foreign_table")["ok"] is False and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
