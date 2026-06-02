"""Model contracts for the advertising campaign standalone slice."""

from __future__ import annotations

from .runtime import advertising_campaign_operations_build_schema_contract

PBC_KEY = "advertising_campaign_operations"

DOMAIN_MODELS = (
    {
        "name": "CampaignBrief",
        "description": "Canonical brief used to normalize one advertising plan.",
        "fields": (
            "objective",
            "offer",
            "audience_promise",
            "channels",
            "primary_kpi",
            "guardrails",
            "launch_dependencies",
        ),
    },
    {
        "name": "CampaignPlan",
        "description": "Deterministic draft plan generated from a structured brief.",
        "fields": (
            "campaign_id",
            "tenant",
            "code",
            "status",
            "brief",
            "brief_fingerprint",
            "primary_channel",
            "planning_summary",
            "launch_gate",
        ),
    },
    {
        "name": "LaunchReadinessReport",
        "description": "Itemized launch gate output for one campaign plan.",
        "fields": ("campaign_id", "ready", "checklist", "blockers", "summary"),
    },
    {
        "name": "DocumentInstructionPlan",
        "description": "Assistant CRUD planning output for governed document intake.",
        "fields": (
            "document_digest",
            "instruction",
            "action",
            "target_table",
            "candidate_tables",
            "requires_human_confirmation",
            "crud_preview",
        ),
    },
)


def model_contracts() -> dict:
    schema_contract = advertising_campaign_operations_build_schema_contract()
    return {
        "ok": schema_contract["ok"],
        "pbc": PBC_KEY,
        "domain_models": DOMAIN_MODELS,
        "schema_models": schema_contract["models"],
        "owned_tables": schema_contract["owned_tables"],
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def smoke_test() -> dict:
    contracts = model_contracts()
    return {
        "ok": contracts["ok"] and bool(contracts["domain_models"]) and bool(contracts["schema_models"]),
        "contracts": contracts,
        "side_effects": (),
    }
