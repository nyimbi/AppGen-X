"""Assistant and document-planning helpers for the advertising campaign slice."""

from __future__ import annotations

from .campaign_planning import build_campaign_plan
from .campaign_planning import review_launch_readiness
from .permissions import ACTION_PERMISSIONS
from .runtime import ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES
from .runtime import advertising_campaign_operations_parse_document_instruction
from .workflows import workflow_catalog

PBC_KEY = "advertising_campaign_operations"
OWNED_TABLES = ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES
TABLE_ALIASES = {
    "campaign": "advertising_campaign_operations_ad_campaign",
    "audience": "advertising_campaign_operations_audience_segment",
    "placement": "advertising_campaign_operations_media_placement",
    "creative": "advertising_campaign_operations_creative_asset",
    "budget": "advertising_campaign_operations_campaign_budget",
}


def _infer_action(instruction: str) -> str:
    normalized = instruction.lower()
    if "delete" in normalized or "remove" in normalized:
        return "delete"
    if "update" in normalized or "edit" in normalized:
        return "update"
    if "read" in normalized or "show" in normalized or "review" in normalized:
        return "read"
    return "create"


def _infer_target_table(instruction: str) -> str:
    normalized = instruction.lower()
    for keyword, table in TABLE_ALIASES.items():
        if keyword in normalized:
            return table
    return OWNED_TABLES[0]


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_preview_campaign_brief",
            "scope": PBC_KEY,
            "description": "Preview one campaign brief before creating a plan.",
            "requires_confirmation_for_mutation": False,
        },
        {
            "name": f"{PBC_KEY}_review_launch_readiness",
            "scope": PBC_KEY,
            "description": "Review launch blockers for one campaign plan.",
            "requires_confirmation_for_mutation": False,
        },
        {
            "name": f"{PBC_KEY}_document_instruction_plan",
            "scope": PBC_KEY,
            "description": "Plan CRUD work from one brief, email, or creative request document.",
            "requires_confirmation_for_mutation": True,
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "skills": skills,
        "workflow_support": workflow_catalog()["workflows"],
        "side_effects": (),
    }


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
            "campaign_brief_preview",
            "launch_readiness_review",
        ),
        "document_routes": (
            f"/api/pbc/{PBC_KEY}/assistant/document-plans",
            f"/api/pbc/{PBC_KEY}/assistant/brief-previews",
            f"/api/pbc/{PBC_KEY}/assistant/launch-previews",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    runtime_plan = advertising_campaign_operations_parse_document_instruction(document, instruction)
    action = _infer_action(instruction)
    target_table = _infer_target_table(instruction)
    return {
        "ok": runtime_plan["ok"],
        "pbc": PBC_KEY,
        "document_digest": runtime_plan["document_digest"],
        "instruction": instruction,
        "action": action,
        "target_table": target_table,
        "candidate_tables": runtime_plan["candidate_tables"],
        "requires_human_confirmation": True,
        "crud_preview": {
            "action": action,
            "table": target_table,
            "required_permission": ACTION_PERMISSIONS["document_instruction_plan"],
            "event_contract": "AppGen-X",
        },
        "side_effects": (),
    }


def campaign_brief_preview(payload: dict | None = None) -> dict:
    plan = build_campaign_plan(payload or {})
    return {
        "ok": plan["ok"],
        "pbc": PBC_KEY,
        "campaign_plan": plan.get("campaign_plan"),
        "missing_fields": plan.get("missing_fields", ()),
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def launch_readiness_preview(payload: dict | None = None) -> dict:
    review = review_launch_readiness(payload or {})
    return {
        "ok": review["ok"],
        "pbc": PBC_KEY,
        "launch_report": review["launch_report"],
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {
            "ok": False,
            "reason": "foreign_table_rejected",
            "table": target,
            "side_effects": (),
        }
    return {
        "ok": action in {"create", "read", "update", "delete"},
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "required_permission": ACTION_PERMISSIONS["document_instruction_plan"],
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "workflow_catalog": workflow_catalog()["workflows"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    preview = campaign_brief_preview(
        {
            "brief": {
                "objective": "Acquire signups",
                "offer": "Trial",
                "audience_promise": "Show to in-market buyers",
                "channels": ("search",),
                "primary_kpi": "signups",
                "guardrails": ("cpa",),
                "launch_dependencies": ("tracking",),
            }
        }
    )
    launch = launch_readiness_preview(
        {
            "campaign_plan": preview["campaign_plan"],
            "readiness": {
                "budget_approved": True,
                "creative_approved": True,
                "audience_ready": True,
                "placements_ready": True,
                "tracking_ready": True,
                "suppliers_eligible": True,
                "policy_compliant": True,
                "dependency_status": {"tracking": True},
            },
        }
    )
    document = document_instruction_plan("Campaign brief for social launch.", "Create campaign plan")
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and preview["ok"]
        and launch["ok"]
        and document["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "preview": preview,
        "launch": launch,
        "document": document,
        "side_effects": (),
    }
