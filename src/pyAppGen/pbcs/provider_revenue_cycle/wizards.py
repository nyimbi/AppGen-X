"""Package-local wizards for provider_revenue_cycle."""

from __future__ import annotations

WIZARDS = (
    {
        "wizard_id": "clean_claim_journey",
        "title": "Take account from intake to clean claim",
        "steps": (
            {"step_id": "register_account", "form_id": "patient_account_intake", "operation": "command_patient_account_intake"},
            {"step_id": "verify_benefits", "form_id": "eligibility_benefits_review", "operation": "command_eligibility_benefits_review"},
            {"step_id": "link_auth", "form_id": "prior_authorization_link", "operation": "command_prior_authorization_link"},
            {"step_id": "capture_charge", "form_id": "charge_capture", "operation": "command_charge_capture"},
            {"step_id": "review_coding", "form_id": "coding_cdi_review", "operation": "command_coding_review"},
            {"step_id": "create_claim", "form_id": "claim_scrub_submission", "operation": "command_claim_create"},
        ),
    },
    {
        "wizard_id": "denial_recovery_cycle",
        "title": "Recover a denial or underpayment",
        "steps": (
            {"step_id": "post_era", "form_id": "remit_era_posting", "operation": "command_remit_era_posting"},
            {"step_id": "open_case", "form_id": "denial_appeal_work", "operation": "command_denial_open"},
            {"step_id": "submit_appeal", "form_id": "denial_appeal_work", "operation": "command_denial_appeal"},
        ),
    },
    {
        "wizard_id": "patient_balance_resolution_cycle",
        "title": "Resolve patient balance with plan, refund, or assistance",
        "steps": (
            {"step_id": "issue_statement", "form_id": "patient_balance_resolution", "operation": "command_patient_statement_issue"},
            {"step_id": "evaluate_assistance", "form_id": "patient_balance_resolution", "operation": "command_financial_assistance"},
            {"step_id": "enroll_plan", "form_id": "patient_balance_resolution", "operation": "command_payment_plan_enroll"},
            {"step_id": "refund_credit", "form_id": "patient_balance_resolution", "operation": "command_refund_credit_issue"},
        ),
    },
    {
        "wizard_id": "month_end_reconciliation_close",
        "title": "Reconcile and close account",
        "steps": (
            {"step_id": "review_workqueue", "form_id": "patient_balance_resolution", "operation": "query_provider_revenue_cycle_workbench"},
            {"step_id": "reconcile_account", "form_id": "close_reconciliation", "operation": "command_reconcile_close"},
        ),
    },
    {
        "wizard_id": "assistant_change_preview",
        "title": "Use assistant for governed document preview",
        "steps": (
            {"step_id": "capture_document", "form_id": "assistant_document_instruction_preview", "operation": "query_provider_revenue_cycle_assistant_preview"},
            {"step_id": "review_preview", "form_id": "assistant_document_instruction_preview", "operation": "query_provider_revenue_cycle_assistant_preview"},
        ),
    },
)


def provider_revenue_cycle_wizard_catalog() -> dict:
    wizard_ids = tuple(wizard["wizard_id"] for wizard in WIZARDS)
    return {
        "ok": bool(WIZARDS),
        "pbc": "provider_revenue_cycle",
        "wizards": WIZARDS,
        "wizard_ids": wizard_ids,
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = provider_revenue_cycle_wizard_catalog()
    return {
        "ok": catalog["ok"] and len(catalog["wizards"]) >= 4,
        "catalog": catalog,
        "side_effects": (),
    }
