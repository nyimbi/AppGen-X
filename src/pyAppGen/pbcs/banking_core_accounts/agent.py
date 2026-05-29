import hashlib

from .permissions import permission_plan
from .runtime import (
    BANKING_CORE_ACCOUNTS_BUSINESS_TABLES,
    BANKING_CORE_ACCOUNTS_CONTROLS,
    BANKING_CORE_ACCOUNTS_FORMS,
    BANKING_CORE_ACCOUNTS_WIZARDS,
)
from .workflows import WORKFLOWS, plan_workflow

PBC_KEY = "banking_core_accounts"
OWNED_TABLES = BANKING_CORE_ACCOUNTS_BUSINESS_TABLES + (
    "banking_core_accounts_appgen_outbox_event",
    "banking_core_accounts_appgen_inbox_event",
    "banking_core_accounts_appgen_dead_letter_event",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def agent_skill_manifest():
    skills = (
        {
            "name": f"{PBC_KEY}_guide_user",
            "scope": PBC_KEY,
            "description": "Guide a user through lifecycle forms, wizard steps, and required controls",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_open_deposit_account",
            "scope": PBC_KEY,
            "description": "Prepare the deposit account opening form and wizard",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_transition_lifecycle",
            "scope": PBC_KEY,
            "description": "Explain lifecycle transitions and maker-checker control requirements",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_read_records",
            "scope": PBC_KEY,
            "description": "Read lifecycle records and workbench summaries",
            "requires_confirmation_for_mutation": False,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def assistant_help_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "help_cards": (
            {
                "topic": "opening",
                "form_id": BANKING_CORE_ACCOUNTS_FORMS[0]["form_id"],
                "wizard_id": BANKING_CORE_ACCOUNTS_WIZARDS[0]["wizard_id"],
                "workflow_id": WORKFLOWS[0]["workflow_id"],
                "controls": ("tenant_boundary_check", "mandatory_field_check"),
            },
            {
                "topic": "lifecycle_transition",
                "form_id": BANKING_CORE_ACCOUNTS_FORMS[1]["form_id"],
                "wizard_id": BANKING_CORE_ACCOUNTS_WIZARDS[1]["wizard_id"],
                "workflow_id": WORKFLOWS[1]["workflow_id"],
                "controls": (
                    "state_transition_guard",
                    "maker_checker_gate",
                    "reason_required_guard",
                ),
            },
        ),
        "side_effects": (),
    }


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
            "form_guidance",
            "wizard_guidance",
            "control_explanation",
            "workflow_guidance",
            "permission_preview",
        ),
        "assistant_help": assistant_help_manifest(),
        "side_effects": (),
    }


def _workflow_for_action(action, instruction):
    normalized = str(instruction).lower()
    if action == "create":
        return WORKFLOWS[0]["workflow_id"]
    if "document" in normalized or "instruction" in normalized:
        return WORKFLOWS[2]["workflow_id"]
    return WORKFLOWS[1]["workflow_id"]


def document_instruction_plan(document, instruction, action="create", table=None, payload=None):
    workflow_id = _workflow_for_action(action, instruction)
    workflow = plan_workflow(workflow_id, payload)
    crud_plan = datastore_crud_plan(action, table=table, payload=payload)
    permission = permission_plan(
        crud_plan["operation"], actor={"roles": ("operator", "approver")}
    )
    return {
        "ok": workflow["ok"] and crud_plan["ok"] and permission["ok"],
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "instruction": instruction,
        "suggested_action": action,
        "candidate_tables": OWNED_TABLES[:3],
        "candidate_forms": tuple(form["form_id"] for form in BANKING_CORE_ACCOUNTS_FORMS),
        "candidate_wizards": tuple(
            wizard["wizard_id"] for wizard in BANKING_CORE_ACCOUNTS_WIZARDS
        ),
        "required_controls": tuple(
            control["control_id"] for control in BANKING_CORE_ACCOUNTS_CONTROLS
        ),
        "recommended_workflow": workflow["workflow"],
        "crud_plan": crud_plan,
        "required_permission": permission["required_permission"],
        "permission_preview": permission,
        "requires_human_confirmation": True,
        "crud_preview": {
            "operation": crud_plan["action"],
            "route": crud_plan["route"],
            "event_contract": "AppGen-X",
        },
        "side_effects": (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {
            "ok": False,
            "reason": "foreign_table_rejected",
            "table": target,
            "side_effects": (),
        }
    operation = {
        "create": "open_deposit_account",
        "read": "query_account_detail",
        "update": "transition_deposit_account",
        "delete": "transition_deposit_account",
    }.get(action, "query_workbench")
    route = {
        "open_deposit_account": "POST /deposit-accounts",
        "query_account_detail": "GET /deposit-accounts/{account_id}",
        "transition_deposit_account": "POST /deposit-accounts/{account_id}/transitions",
        "query_workbench": "GET /banking-core-accounts-workbench",
    }[operation]
    workflow_id = _workflow_for_action(action, action)
    permission = permission_plan(operation, actor={"roles": ("operator", "approver")})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "operation": operation,
        "route": route,
        "workflow_id": workflow_id,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "required_permission": permission["required_permission"],
        "permission_preview": permission,
        "domain_action": "close_account" if action == "delete" else action,
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "side_effects": (),
    }


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "assistant_help": assistant_help_manifest(),
        "workflow_ids": tuple(item["workflow_id"] for item in WORKFLOWS),
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"]
        and assistant_help_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("doc", "open account")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
