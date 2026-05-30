"""Agent and chatbot assistance for the insurance_claims_policy PBC."""

from __future__ import annotations

from .models import OWNED_TABLES
from .standalone import InsuranceClaimsPolicyStandaloneApp

PBC_KEY = "insurance_claims_policy"

SKILLS = (
    {
        "name": "insurance_claims_policy_intake_fnol",
        "scope": PBC_KEY,
        "description": "Extract FNOL details, triage severity, and propose claim-opening actions.",
        "read": ("document_intake", "get_claim_snapshot", "workbench"),
        "write": ("open_claim", "record_loss_event", "attach_claim_document"),
        "requires_confirmation_for_mutation": True,
        "uses_appgen_event_contract": True,
    },
    {
        "name": "insurance_claims_policy_coverage_reasoner",
        "scope": PBC_KEY,
        "description": "Explain policy, peril, deductible, premium, and evidence factors behind a coverage decision.",
        "read": ("get_policy_snapshot", "get_claim_snapshot", "simulate_loss_exposure"),
        "write": ("determine_coverage", "set_claim_reserve"),
        "requires_confirmation_for_mutation": True,
        "uses_appgen_event_contract": True,
    },
    {
        "name": "insurance_claims_policy_settlement_copilot",
        "scope": PBC_KEY,
        "description": "Prepare settlement, payment, fraud, and recovery next-step plans with release-safe previews.",
        "read": ("get_claim_snapshot", "workbench", "release_snapshot"),
        "write": ("adjudicate_claim", "create_settlement_offer", "execute_settlement_payment", "record_subrogation_recovery"),
        "requires_confirmation_for_mutation": True,
        "uses_appgen_event_contract": True,
    },
)


def agent_skill_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "skills": SKILLS, "side_effects": ()}


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "coverage_reasoning",
            "settlement_strategy_preview",
            "governed_datastore_crud",
            "mutation_preview",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp()
    return {"ok": True, "pbc": PBC_KEY, **app.document_intake(document, instruction), "side_effects": ()}


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp()
    target = table or OWNED_TABLES[0]
    return app.crud_mutation_plan(action, target, payload)


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_coverage", f"{PBC_KEY}_settlement"),
        "side_effects": (),
    }


def smoke_test() -> dict:
    plan = document_instruction_plan("Fire loss notice with invoice and reserve request.", "open the claim and prepare a coverage summary")
    allowed = datastore_crud_plan("create", OWNED_TABLES[0], {"policy_number": "POL-1"})
    rejected = datastore_crud_plan("update", "foreign_table", {})
    return {
        "ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"] and plan["ok"] and allowed["ok"] and rejected["ok"] is False and composed_agent_contribution()["ok"],
        "plan": plan,
        "allowed": allowed,
        "rejected": rejected,
        "side_effects": (),
    }
