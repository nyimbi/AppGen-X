"""Package-local workflows for the advertising campaign standalone slice."""

from __future__ import annotations

from .campaign_planning import build_campaign_plan
from .campaign_planning import review_launch_readiness

PBC_KEY = "advertising_campaign_operations"

WORKFLOWS = (
    {
        "key": "campaign_brief_to_plan",
        "label": "Campaign Brief To Plan",
        "entrypoint": "create_campaign_plan",
        "steps": ("capture_brief", "normalize_brief", "generate_plan", "queue_launch_review"),
    },
    {
        "key": "launch_gate_review",
        "label": "Launch Gate Review",
        "entrypoint": "review_launch_readiness",
        "steps": ("collect_readiness", "evaluate_gate", "summarize_blockers"),
    },
    {
        "key": "assistant_document_instruction",
        "label": "Assistant Document Instruction Planning",
        "entrypoint": "document_instruction_plan",
        "steps": ("ingest_document", "classify_action", "map_target", "draft_crud_preview"),
    },
)


def workflow_catalog() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "workflows": WORKFLOWS,
        "side_effects": (),
    }


def run_campaign_brief_workflow(payload: dict | None = None) -> dict:
    plan = build_campaign_plan(payload or {})
    return {
        "ok": plan["ok"],
        "workflow": WORKFLOWS[0],
        "result": plan,
        "side_effects": (),
    }


def run_launch_gate_workflow(payload: dict | None = None) -> dict:
    report = review_launch_readiness(payload or {})
    return {
        "ok": report["ok"],
        "workflow": WORKFLOWS[1],
        "result": report,
        "side_effects": (),
    }


def run_document_instruction_workflow(document: str, instruction: str) -> dict:
    from .agent import document_instruction_plan

    plan = document_instruction_plan(document, instruction)
    return {
        "ok": plan["ok"],
        "workflow": WORKFLOWS[2],
        "result": plan,
        "side_effects": (),
    }


def smoke_test() -> dict:
    plan = run_campaign_brief_workflow(
        {
            "tenant": "tenant-smoke",
            "code": "SMOKE",
            "brief": {
                "objective": "Acquire qualified signups",
                "offer": "30 day trial",
                "audience_promise": "Reach in-market buyers",
                "channels": ("search", "social"),
                "primary_kpi": "qualified_signups",
                "guardrails": ("cpa",),
                "launch_dependencies": ("tracking",),
            },
        }
    )
    launch = run_launch_gate_workflow(
        {
            "campaign_plan": plan["result"]["campaign_plan"],
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
    document = run_document_instruction_workflow("Brief for Q4 launch.", "Create campaign plan")
    return {
        "ok": workflow_catalog()["ok"] and plan["ok"] and launch["ok"] and document["ok"],
        "plan": plan,
        "launch": launch,
        "document": document,
        "side_effects": (),
    }
