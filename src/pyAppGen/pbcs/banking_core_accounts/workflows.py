"""Workflow surfaces for the banking_core_accounts standalone slice."""
from __future__ import annotations

from .lifecycle import LIFECYCLE_STATES, query_workbench

PBC_KEY = "banking_core_accounts"

WORKFLOWS = (
    {
        "workflow_id": "banking_core_accounts_create_deposit_account_workflow",
        "title": "Create Deposit Account",
        "summary": "Capture opening details, enforce opening controls, and create a pending account.",
        "entry_route": "POST /deposit-accounts",
        "primary_form": "deposit_account_opening_form",
        "wizard_id": "deposit_account_opening_wizard",
        "controls": ("tenant_boundary_check", "mandatory_field_check"),
        "operations": ("open_deposit_account", "query_workbench"),
        "required_permissions": (
            "banking_core_accounts.create",
            "banking_core_accounts.read",
        ),
        "target_states": ("pending",),
        "assistant_channel": "BankingCoreAccountsAssistantPanel",
    },
    {
        "workflow_id": "banking_core_accounts_deposit_account_lifecycle_workflow",
        "title": "Deposit Account Lifecycle",
        "summary": "Approve, activate, restrict, close, or reopen an account with maker-checker and reason controls.",
        "entry_route": "POST /deposit-accounts/{account_id}/transitions",
        "primary_form": "deposit_account_transition_form",
        "wizard_id": "deposit_account_lifecycle_wizard",
        "controls": (
            "state_transition_guard",
            "maker_checker_gate",
            "reason_required_guard",
        ),
        "operations": (
            "transition_deposit_account",
            "query_account_detail",
            "query_workbench",
        ),
        "required_permissions": (
            "banking_core_accounts.update",
            "banking_core_accounts.approve",
            "banking_core_accounts.read",
        ),
        "target_states": tuple(state for state in LIFECYCLE_STATES if state != "pending"),
        "assistant_channel": "BankingCoreAccountsAssistantPanel",
    },
    {
        "workflow_id": "banking_core_accounts_document_instruction_workflow",
        "title": "Document Instruction Intake",
        "summary": "Parse operator instructions, preview CRUD intent, and require confirmation before mutation.",
        "entry_route": "/assistant/pbc/banking_core_accounts",
        "primary_form": None,
        "wizard_id": None,
        "controls": (
            "tenant_boundary_check",
            "maker_checker_gate",
            "reason_required_guard",
        ),
        "operations": ("parse_document_instruction", "query_workbench"),
        "required_permissions": (
            "banking_core_accounts.read",
            "banking_core_accounts.update",
        ),
        "target_states": ("pending", "approved", "active", "closed", "reopened"),
        "assistant_channel": "BankingCoreAccountsAssistantPanel",
    },
)


def workflow_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "workflows": WORKFLOWS,
        "workflow_ids": tuple(item["workflow_id"] for item in WORKFLOWS),
        "single_pbc_app": True,
        "shared_table_access": False,
        "side_effects": (),
    }


def plan_workflow(workflow_id: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    workflow = next((item for item in WORKFLOWS if item["workflow_id"] == workflow_id), None)
    if workflow is None:
        return {
            "ok": False,
            "workflow_id": workflow_id,
            "reason": "unknown_workflow",
            "side_effects": (),
        }
    return {
        "ok": True,
        "workflow_id": workflow_id,
        "workflow": workflow,
        "payload": payload,
        "next_operation": workflow["operations"][0],
        "required_permissions": workflow["required_permissions"],
        "side_effects": (),
    }


def build_workflow_surface(state: dict | None = None, tenant: str = "default") -> dict:
    projected = query_workbench(state or {"records": {}}, {"tenant": tenant})
    lifecycle_counts = {
        item["lifecycle_state"]: item["count"] for item in projected["summary"]["lifecycle_counts"]
    }
    return {
        "ok": projected["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "workflows": WORKFLOWS,
        "queue_summary": projected["summary"],
        "workflow_state_coverage": tuple(
            {
                "workflow_id": workflow["workflow_id"],
                "target_states": workflow["target_states"],
                "visible_account_count": sum(
                    lifecycle_counts.get(state_name, 0) for state_name in workflow["target_states"]
                ),
            }
            for workflow in WORKFLOWS
        ),
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = workflow_manifest()
    planned = plan_workflow(WORKFLOWS[0]["workflow_id"])
    surface = build_workflow_surface()
    return {
        "ok": manifest["ok"] and planned["ok"] and surface["ok"],
        "manifest": manifest,
        "planned": planned,
        "surface": surface,
        "side_effects": (),
    }
